import os
import re
import json
import random
import logging
import base64
import requests
import threading
from django.conf import settings
from django.urls import path, get_resolver
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.cache import cache
from django.utils import timezone
from celery import shared_task

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# 1. MONKEY-PATCHING VOD STREAM URL RESOLUTION FOR STALKER ACCOUNTS
# ----------------------------------------------------------------------
# ArgusFlix's standard VOD streaming views call get_stream_url() on the
# movie/episode relations. We patch these methods so Stalker-integrated VODs
# dynamically point to our dynamic play view route.

from apps.vod.models import M3UMovieRelation, M3UEpisodeRelation

_original_movie_get_stream_url = M3UMovieRelation.get_stream_url
_original_episode_get_stream_url = M3UEpisodeRelation.get_stream_url

def stalker_movie_get_stream_url(self):
    if self.m3u_account and self.m3u_account.name.startswith("Stalker:"):
        portal_key = self.m3u_account.custom_properties.get("portal_key", "")
        cmd = self.custom_properties.get("cmd", "")
        if portal_key and cmd:
            encoded_cmd = base64.b64encode(cmd.encode("utf-8")).decode("utf-8")
            local_stream_host = self.m3u_account.custom_properties.get("local_stream_host", "http://127.0.0.1:5656")
            return f"{local_stream_host}/stalker/play/{portal_key}/?cmd={encoded_cmd}"
    return _original_movie_get_stream_url(self)

def stalker_episode_get_stream_url(self):
    if self.m3u_account and self.m3u_account.name.startswith("Stalker:"):
        portal_key = self.m3u_account.custom_properties.get("portal_key", "")
        cmd = self.custom_properties.get("cmd", "")
        if portal_key and cmd:
            encoded_cmd = base64.b64encode(cmd.encode("utf-8")).decode("utf-8")
            local_stream_host = self.m3u_account.custom_properties.get("local_stream_host", "http://127.0.0.1:5656")
            return f"{local_stream_host}/stalker/play/{portal_key}/?cmd={encoded_cmd}"
    return _original_episode_get_stream_url(self)

M3UMovieRelation.get_stream_url = stalker_movie_get_stream_url
M3UEpisodeRelation.get_stream_url = stalker_episode_get_stream_url
logger.info("Stalker Portals: Dynamically patched VOD stream URL resolution methods.")


# ----------------------------------------------------------------------
# 2. STALKER API CLIENT
# ----------------------------------------------------------------------
class StalkerClient:
    def __init__(self, portal_url, mac, user_agent=None, logger=None):
        self.portal_url = portal_url.strip()
        self.base_url = self._normalize_stalker_url(self.portal_url)
        self.mac = mac.strip()
        self.logger = logger or logging.getLogger(__name__)
        
        # MAG250 STB default User-Agent
        self.user_agent = user_agent.strip() if user_agent else (
            "Mozilla/5.0 (QtEmbedded; U; Linux; C) "
            "AppleWebKit/533.3 (KHTML, like Gecko) "
            "MAG200 stbapp vtuner RTKD DLNADOC/1.50 compatible "
            "Env/Linux/2.6.32-27-ext/0.2.18-r7-pub-250 HST="
        )
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "*/*",
            "Cookie": f"mac={self.mac}"
        })
        self.token = ""

    def _normalize_stalker_url(self, url):
        if not url:
            return ""
        if "portal.php" in url:
            return url
        if url.endswith("/"):
            return url + "portal.php"
        return url + "/portal.php"

    def _get_request(self, url, timeout=15):
        # Ensure JsHttpRequest=1-xml is present in the query parameters
        if "JsHttpRequest=" not in url:
            connector = "&" if "?" in url else "?"
            url = f"{url}{connector}JsHttpRequest=1-xml"
            
        self.logger.debug(f"Stalker: Sending request to: {url}")
        res = self.session.get(url, timeout=timeout)
        res.raise_for_status()
        
        text = res.text.strip()
        if not text:
            raise ValueError("Empty response received from Stalker portal")
            
        # Strip legacy JsHttpRequest comment wrappers (e.g. /* ... */)
        if text.startswith("/*"):
            end_comment = text.find("*/")
            if end_comment != -1:
                text = text[end_comment + 2:].strip()
                
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Stalker: Failed to parse JSON response. Status code: {res.status_code}. Response snippet: {text[:300]}")
            if text.startswith("<") or "html" in text.lower():
                raise ValueError(
                    f"Portal returned HTML page instead of JSON API response. "
                    f"This might mean the portal URL is incorrect, your MAC is blocked/unauthorized, or the portal is protected. "
                    f"Snippet: {text[:150]}"
                )
            raise ValueError(f"Invalid JSON response: {str(e)}. Snippet: {text[:150]}")

    def handshake(self):
        cache_key = f"stalker_token_{self.portal_url}_{self.mac}"
        cached_data = cache.get(cache_key)
        if cached_data and isinstance(cached_data, dict):
            self.base_url = cached_data.get("base_url", self.base_url)
            self.token = cached_data.get("token", "")
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
            })
            self.logger.info(f"Stalker: Using cached session token and base URL {self.base_url}")
            return self.token

        url_clean = self.portal_url.rstrip("/")
        if "portal.php" in url_clean or "server/load.php" in url_clean:
            paths_to_try = [url_clean]
        else:
            paths_to_try = [
                f"{url_clean}/server/load.php",
                f"{url_clean}/portal.php",
                url_clean if url_clean.endswith(".php") else f"{url_clean}/",
            ]

        last_error = None
        for path in paths_to_try:
            self.logger.info(f"Stalker: Attempting handshake on {path}")
            url = f"{path}?type=stb&action=handshake&mac={self.mac}&key=&token="
            try:
                data = self._get_request(url, timeout=15)
                js_data = data.get("js", {})
                
                token = ""
                if isinstance(js_data, dict):
                    token = js_data.get("token", "")
                elif isinstance(js_data, str):
                    token = js_data
                
                if token:
                    self.token = token
                    self.base_url = path
                    self.logger.info(f"Stalker: Handshake successful on {path}, token acquired: {self.token}")
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.token}",
                    })
                    
                    # Cache token and base_url for 50 minutes
                    cache.set(cache_key, {"token": self.token, "base_url": self.base_url}, timeout=3000)
                    
                    # Warm up session with profile registration
                    try:
                        profile_url = f"{self.base_url}?type=stb&action=get_profile&mac={self.mac}&token={self.token}"
                        self._get_request(profile_url, timeout=15)
                    except Exception as e:
                        self.logger.warning(f"Stalker: Profile registration failed: {e}")
                        
                    return self.token
                else:
                    self.logger.warning(f"Stalker: Handshake response from {path} did not return a token: {data}")
            except Exception as e:
                self.logger.warning(f"Stalker: Handshake failed on {path}: {e}")
                last_error = e

        raise ValueError(
            f"Handshake failed for all endpoints. "
            f"Please verify the URL ({self.portal_url}) and MAC address ({self.mac}). "
            f"Last error: {last_error}"
        )

    def execute_with_retry(self, func, *args, **kwargs):
        """Helper to run a client function, refreshing token on authentication errors"""
        try:
            if not self.token:
                self.handshake()
            return func(*args, **kwargs)
        except Exception as e:
            self.logger.warning(f"Stalker API error ({e}), retrying handshake...")
            cache_key = f"stalker_token_{self.portal_url}_{self.mac}"
            cache.delete(cache_key)
            self.token = ""
            self.handshake()
            return func(*args, **kwargs)

    def _get_genres(self):
        url = f"{self.base_url}?type=itv&action=get_genres&token={self.token}"
        data = self._get_request(url, timeout=15)
        genres = {}
        js_list = data.get("js", [])
        if isinstance(js_list, list):
            for g in js_list:
                genres[str(g.get("id"))] = g.get("title", "Unknown")
        return genres

    def get_genres(self):
        return self.execute_with_retry(self._get_genres)

    def _get_channels(self):
        url = f"{self.base_url}?type=itv&action=get_all_channels&token={self.token}"
        data = self._get_request(url, timeout=30)
        js_data = data.get("js", {})
        channels = []
        if isinstance(js_data, dict):
            channels = js_data.get("data", [])
        elif isinstance(js_data, list):
            channels = js_data

        if not channels:
            # Fallback to get_ordered_list paging if all_channels is blank
            page = 1
            while True:
                p_url = f"{self.base_url}?type=itv&action=get_ordered_list&page={page}&token={self.token}"
                p_data = self._get_request(p_url, timeout=15)
                p_js = p_data.get("js", {})
                p_channels = p_js.get("data", []) if isinstance(p_js, dict) else (p_js if isinstance(p_js, list) else [])
                if not p_channels:
                    break
                channels.extend(p_channels)
                page += 1
                if page > 50:
                    break
        return channels

    def get_channels(self):
        return self.execute_with_retry(self._get_channels)

    def _get_movies(self):
        # Fetch categories/genres for VOD
        url_cats = f"{self.base_url}?type=vod&action=get_categories&token={self.token}"
        categories = {}
        try:
            cats_data = self._get_request(url_cats, timeout=15)
            js_cats = cats_data.get("js", [])
            if isinstance(js_cats, list):
                for c in js_cats:
                    categories[str(c.get("id"))] = c.get("name", "VOD Category")
        except Exception as e:
            self.logger.warning(f"Stalker: Failed to load VOD categories: {e}")

        # Fetch movies via paged get_ordered_list
        movies = []
        page = 1
        while True:
            p_url = f"{self.base_url}?type=vod&action=get_ordered_list&page={page}&token={self.token}"
            p_data = self._get_request(p_url, timeout=15)
            p_js = p_data.get("js", {})
            p_movies = p_js.get("data", []) if isinstance(p_js, dict) else (p_js if isinstance(p_js, list) else [])
            if not p_movies:
                break
            for m in p_movies:
                cat_id = str(m.get("category_id"))
                m["category_name"] = categories.get(cat_id, "Movies")
                movies.append(m)
            page += 1
            if page > 20:  # Cap to prevent excessive memory/time usage on massive portals
                break
        return movies

    def get_movies(self):
        return self.execute_with_retry(self._get_movies)

    def _get_series(self):
        url_cats = f"{self.base_url}?type=series&action=get_categories&token={self.token}"
        categories = {}
        try:
            cats_data = self._get_request(url_cats, timeout=15)
            js_cats = cats_data.get("js", [])
            if isinstance(js_cats, list):
                for c in js_cats:
                    categories[str(c.get("id"))] = c.get("name", "Series Category")
        except Exception as e:
            self.logger.warning(f"Stalker: Failed to load series categories: {e}")

        series = []
        page = 1
        while True:
            p_url = f"{self.base_url}?type=series&action=get_ordered_list&page={page}&token={self.token}"
            p_data = self._get_request(p_url, timeout=15)
            p_js = p_data.get("js", {})
            p_series = p_js.get("data", []) if isinstance(p_js, dict) else (p_js if isinstance(p_js, list) else [])
            if not p_series:
                break
            for s in p_series:
                cat_id = str(s.get("category_id"))
                s["category_name"] = categories.get(cat_id, "TV Series")
                series.append(s)
            page += 1
            if page > 20:
                break
        return series

    def get_series(self):
        return self.execute_with_retry(self._get_series)

    def _get_episodes(self, series_id):
        url = f"{self.base_url}?type=series&action=get_episodes&series_id={series_id}&token={self.token}"
        data = self._get_request(url, timeout=20)
        js_data = data.get("js", [])
        if isinstance(js_data, list):
            return js_data
        elif isinstance(js_data, dict):
            return js_data.get("data", [])
        return []

    def get_episodes(self, series_id):
        return self.execute_with_retry(self._get_episodes, series_id)

    def _create_link(self, cmd):
        # Series is always empty for default live and vod, forced checks 0
        url = f"{self.base_url}?type=itv&action=create_link&cmd={requests.utils.quote(cmd)}&token={self.token}&series=&forced_ch_link_check=0&download=0"
        self.logger.debug(f"Stalker: Requesting playback link for cmd: {cmd}")
        data = self._get_request(url, timeout=15)

        js_data = data.get("js", {})
        link = ""
        if isinstance(js_data, dict):
            link = js_data.get("cmd", "")
        elif isinstance(js_data, str):
            link = js_data

        if not link:
            raise ValueError(f"Failed to generate playback URL. Response: {data}")

        # Clean stream link: strip command prefixes like ffmpeg or ffrt
        cleaned_link = link
        if " " in cleaned_link:
            parts = cleaned_link.split()
            for p in parts:
                if any(p.startswith(proto) for proto in ("http://", "https://", "rtmp://", "rtsp://", "udp://", "rtp://")):
                    cleaned_link = p
                    break
        return cleaned_link

    def create_link(self, cmd):
        return self.execute_with_retry(self._create_link, cmd)


# ----------------------------------------------------------------------
# 3. UTILITIES & DYNAMIC PLAYBACK VIEW
# ----------------------------------------------------------------------
def parse_portals_from_settings(settings_dict):
    portals = []
    
    # 1. Parse portals_list (bulk list format)
    portals_list_str = settings_dict.get("portals_list", "").strip()
    if portals_list_str:
        from urllib.parse import urlparse
        for line in portals_list_str.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Split by pipe '|' or comma ','
            if "|" in line:
                parts = [p.strip() for p in line.split("|")]
            else:
                parts = [p.strip() for p in line.split(",")]
                
            if len(parts) >= 2:
                name = ""
                url = ""
                mac = ""
                ua = ""
                
                mac_pattern = r"^([0-9A-Fa-f:]{17})$"
                url_pattern = r"^https?://"
                
                remaining_parts = []
                for p in parts:
                    if re.match(mac_pattern, p.strip()):
                        mac = p.strip()
                    elif re.match(url_pattern, p.strip()):
                        url = p.strip()
                    else:
                        remaining_parts.append(p.strip())
                        
                if url and mac:
                    if len(remaining_parts) >= 1:
                        name = remaining_parts[0]
                    if len(remaining_parts) >= 2:
                        ua = remaining_parts[1]
                        
                    if not name:
                        name = f"Portal {urlparse(url).netloc}"
                        
                    portals.append({
                        "name": name,
                        "url": url,
                        "mac": mac,
                        "user_agent": ua
                    })

    # 2. Parse portals_json (JSON fallback)
    if not portals:
        portals_json_str = settings_dict.get("portals_json", "[]")
        try:
            portals = json.loads(portals_json_str)
        except Exception:
            pass

    # 3. Fall back to single portal settings
    if not isinstance(portals, list) or not portals:
        single_url = settings_dict.get("portal_url", "")
        single_mac = settings_dict.get("mac_address", "")
        single_name = settings_dict.get("portal_name", "Stalker Portal")
        single_ua = settings_dict.get("user_agent", "")
        if single_url and single_mac:
            portals = [{
                "name": single_name,
                "url": single_url,
                "mac": single_mac,
                "user_agent": single_ua
            }]
            
    return portals


def stalker_play_view(request, portal_key):
    """
    Dynamically handshakes and resolves the real stream URL on-the-fly,
    then redirects the caller to it. Uses base64 encoded 'cmd' parameter.
    """
    encoded_cmd = request.GET.get("cmd", "")
    if not encoded_cmd:
        return HttpResponse("Missing play command", status=400)

    try:
        cmd = base64.b64decode(encoded_cmd.encode("utf-8")).decode("utf-8")
    except Exception:
        return HttpResponse("Invalid encoded command", status=400)

    # Resolve portal settings from the plugin database
    try:
        from apps.plugins.models import PluginConfig
        cfg = PluginConfig.objects.get(key="stalker_portals_integrator")
        settings_dict = cfg.settings or {}
    except Exception:
        return HttpResponse("Plugin configuration unavailable", status=500)

    # Look up portal config matching portal_key
    portals = parse_portals_from_settings(settings_dict)

    target_portal = None
    from django.utils.text import slugify
    for p in portals:
        if slugify(p.get("name", "")) == portal_key:
            target_portal = p
            break

    if not target_portal:
        return HttpResponse("Portal configuration not found", status=404)

    try:
        client = StalkerClient(
            portal_url=target_portal.get("url"),
            mac=target_portal.get("mac"),
            user_agent=target_portal.get("user_agent")
        )
        real_url = client.create_link(cmd)
        return HttpResponseRedirect(real_url)
    except Exception as e:
        logger.exception(f"Stalker play view failed for cmd {cmd}")
        return HttpResponse(f"Playback resolution failed: {e}", status=500)


_route_lock = threading.Lock()
_route_registered = False

def register_stalker_route():
    global _route_registered
    with _route_lock:
        if _route_registered:
            return
        resolver = get_resolver()
        # Verify route isn't already in patterns
        for pattern in resolver.url_patterns:
            if hasattr(pattern, "pattern") and "stalker/play/" in str(pattern.pattern):
                _route_registered = True
                return
        
        route = path("stalker/play/<str:portal_key>/", stalker_play_view, name="stalker-play")
        resolver.url_patterns.append(route)
        _route_registered = True
        logger.info("Stalker Portals: Dynamically registered playback route '/stalker/play/<portal_key>/'.")


# ----------------------------------------------------------------------
# 4. LIGHTWEIGHT STREAM TESTING (HTTP CHECKER)
# ----------------------------------------------------------------------
def test_stream_url(url, user_agent, logger_inst=None):
    """
    Test if a stream URL functions by performing a short range GET request
    and validating that it yields binary chunks of data.
    """
    if not url:
        return False
    if url.startswith(('udp://', 'rtp://', 'rtsp://')):
        # Automatically pass non-HTTP streams
        return True
    try:
        headers = {"User-Agent": user_agent}
        # Short range check
        res = requests.get(url, headers=headers, stream=True, timeout=8)
        if 200 <= res.status_code < 300:
            # Try reading first block
            for chunk in res.iter_content(chunk_size=1024):
                if chunk and len(chunk) > 0:
                    res.close()
                    if logger_inst:
                        logger_inst.info(f"Stream validation passed: resolved {len(chunk)} bytes.")
                    return True
        res.close()
    except Exception as e:
        if logger_inst:
            logger_inst.warning(f"Stream validation failed: {e}")
    return False


# ----------------------------------------------------------------------
# 5. DYNAMIC PERIODIC TASK SCHEDULER
# ----------------------------------------------------------------------
def update_periodic_task(settings_dict, logger_inst):
    try:
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        cron_schedule_str = settings_dict.get("cron_schedule", "0 3 * * *").strip()
        parts = cron_schedule_str.split()
        if len(parts) == 5:
            minute, hour, day_of_month, month_of_year, day_of_week = parts
            
            # Get or create CrontabSchedule
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=minute,
                hour=hour,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                month_of_year=month_of_year,
                timezone=settings.TIME_ZONE
            )
            
            # Create or update PeriodicTask
            task_obj, task_created = PeriodicTask.objects.update_or_create(
                name="Stalker Portal Sync Schedule",
                defaults={
                    "crontab": schedule,
                    "task": "argusflix_manager_stalker_portal.sync_task",
                    "args": "[]",
                    "kwargs": "{}",
                    "enabled": True,
                }
            )
            logger_inst.info(f"Stalker Portals: Registered periodic background sync task (cron: '{cron_schedule_str}').")
        else:
            logger_inst.warning(f"Stalker Portals: Invalid cron expression '{cron_schedule_str}', skipped scheduling periodic task.")
    except Exception as e:
        logger_inst.warning(f"Stalker Portals: Could not update background scheduler task: {e}")


# ----------------------------------------------------------------------
# 6. CELERY BACKGROUND SYNC TASK
# ----------------------------------------------------------------------
@shared_task(name="argusflix_manager_stalker_portal.sync_task")
def stalker_sync_task():
    from apps.plugins.models import PluginConfig
    from apps.plugins.loader import PluginManager
    
    logger.info("Stalker Portals: Starting automated background sync Celery task.")
    try:
        cfg = PluginConfig.objects.get(key="stalker_portals_integrator")
        if not cfg.enabled:
            logger.info("Stalker Portals: Plugin is disabled. Skipping scheduled sync task.")
            return "Plugin is disabled, skipping sync."
            
        lp = PluginManager.get().get_plugin("stalker_portals_integrator")
        if not lp or not lp.instance:
            logger.error("Stalker Portals: Plugin instance not loaded. Cannot run scheduled sync.")
            return "Plugin code not loaded."
            
        context = PluginManager.get()._build_context(lp, cfg)
        res = lp.instance.run("sync", {}, context)
        logger.info(f"Stalker Portals: Scheduled background sync complete. Status: {res}")
        return res
    except Exception as e:
        logger.exception("Stalker Portals: Scheduled background sync task failed")
        return f"Failed: {e}"


# ----------------------------------------------------------------------
# 8. PRE-IMPORT DYNAMIC FILTER HELPER
# ----------------------------------------------------------------------
def is_filtered(name, category, whitelist_cats, blacklist_cats, blacklist_keywords):
    name_lower = name.lower()
    cat_lower = category.lower() if category else ""
    
    # 1. Whitelist Category Filter
    if whitelist_cats:
        match = False
        for c in whitelist_cats:
            if c in cat_lower:
                match = True
                break
        if not match:
            return True # Not in whitelist, skip
            
    # 2. Blacklist Category Filter
    if blacklist_cats:
        for c in blacklist_cats:
            if c in cat_lower:
                return True # In blacklist, skip
                
    # 3. Title Keyword Blacklist Filter
    if blacklist_keywords:
        for kw in blacklist_keywords:
            if kw in name_lower:
                return True # Contains blacklisted keyword, skip
                
    return False


# ----------------------------------------------------------------------
# 9. CORE DISPATCHARR PLUGIN IMPLEMENTATION
# ----------------------------------------------------------------------
class Plugin:
    name = "Stalker Portals Integrator"
    version = "1.2.0"
    description = "Integrate Stalker IPTV portals using URL and MAC address. Translates portals into standard M3U accounts and VOD libraries with selective sync, pre-import category/keyword filters, random testing, scheduling, and new entry markers."
    author = "Antigravity"
    
    def __init__(self):
        # Register playback route on initialization
        register_stalker_route()

    def stop(self, context: dict):
        logger_inst = context.get("logger", logger)
        logger_inst.info("Stalker Portals: Stopping plugin, disabling background scheduler task...")
        try:
            from django_celery_beat.models import PeriodicTask
            PeriodicTask.objects.filter(name="Stalker Portal Sync Schedule").update(enabled=False)
            logger_inst.info("Stalker Portals: Background periodic task 'Stalker Portal Sync Schedule' disabled successfully.")
        except Exception as e:
            logger_inst.warning(f"Stalker Portals: Failed to disable background task on stop: {e}")

    def run(self, action: str, params: dict, context: dict):
        settings_dict = context.get("settings", {})
        logger_inst = context.get("logger", logger)

        # Synchronize background Celery Beat schedule on every settings load/save
        update_periodic_task(settings_dict, logger_inst)

        if action == "sync":
            # Extract configuration settings
            sync_live_tv = bool(settings_dict.get("sync_live_tv", True))
            sync_movies = bool(settings_dict.get("sync_movies", True))
            sync_series = bool(settings_dict.get("sync_series", True))
            mark_new_entries = bool(settings_dict.get("mark_new_entries", True))
            test_sample_size = int(settings_dict.get("test_sample_size", 5))
            local_stream_host = settings_dict.get("local_stream_host", "http://127.0.0.1:5656").rstrip("/")
            
            # Parse whitelist, blacklist and keyword filters
            whitelist_cats = [c.strip().lower() for c in settings_dict.get("category_whitelist", "").split(",") if c.strip()]
            blacklist_cats = [c.strip().lower() for c in settings_dict.get("category_blacklist", "").split(",") if c.strip()]
            blacklist_keywords = [k.strip().lower() for k in settings_dict.get("title_blacklist", "").split(",") if k.strip()]
            
            # Load configured portals
            portals = parse_portals_from_settings(settings_dict)

            if not portals:
                return {"status": "error", "message": "No Stalker portals configured. Please configure at least one portal."}

            results = {
                "portals_processed": 0,
                "channels": {"found": 0, "tested": 0, "working": 0, "imported": 0},
                "movies": {"found": 0, "tested": 0, "working": 0, "imported": 0},
                "series": {"found": 0, "tested": 0, "working": 0, "imported": 0},
                "episodes": {"found": 0, "tested": 0, "working": 0, "imported": 0}
            }

            for portal in portals:
                p_name = portal.get("name", "Stalker Portal")
                p_url = portal.get("url", "")
                p_mac = portal.get("mac", "")
                p_ua = portal.get("user_agent", "")
                
                from django.utils.text import slugify
                portal_key = slugify(p_name)
                
                logger_inst.info(f"Stalker: Processing portal '{p_name}' ({p_url})")

                try:
                    client = StalkerClient(portal_url=p_url, mac=p_mac, user_agent=p_ua, logger=logger_inst)
                    client.handshake()
                    
                    # Register standard M3UAccount representing this portal
                    from apps.m3u.models import M3UAccount
                    from apps.m3u.tasks import refresh_single_m3u_account
                    
                    m3u_account_name = f"Stalker: {p_name}"
                    
                    # Create directories and paths
                    data_dir = os.path.join(os.path.dirname(__file__), "data")
                    os.makedirs(data_dir, exist_ok=True)
                    m3u_file_path = os.path.join(data_dir, f"{portal_key}.m3u")
                    
                    account, created = M3UAccount.objects.update_or_create(
                        name=m3u_account_name,
                        defaults={
                            "file_path": m3u_file_path,
                            "account_type": M3UAccount.Types.STADNARD,
                            "is_active": True,
                            "status": M3UAccount.Status.IDLE,
                            "last_message": "Syncing tested channels from Stalker portal plugin...",
                            "custom_properties": {
                                "portal_key": portal_key,
                                "local_stream_host": local_stream_host,
                            }
                        }
                    )

                    # --- PART 1: SELECTIVE SYNC - LIVE CHANNELS ---
                    if sync_live_tv:
                        genres = {}
                        channels = []
                        try:
                            genres = client.get_genres()
                            channels = client.get_channels()
                        except Exception as e:
                            logger_inst.warning(f"Stalker '{p_name}': Failed to fetch Live TV genres or channels: {e}")
                        results["channels"]["found"] += len(channels)

                        filtered_channels = []
                        for ch in channels:
                            genre_id = ch.get("tv_genre_id", "")
                            genre_name = genres.get(str(genre_id), "Stalker TV")
                            ch_name = ch.get("name", "Unknown Channel")
                            if is_filtered(ch_name, genre_name, whitelist_cats, blacklist_cats, blacklist_keywords):
                                continue
                            filtered_channels.append(ch)

                        logger_inst.info(f"Stalker '{p_name}': Selective sync - Loaded {len(channels)} channels, {len(filtered_channels)} passed pre-import filters.")

                        working_channels = []
                        if filtered_channels:
                            sample_channels = random.sample(filtered_channels, min(len(filtered_channels), test_sample_size))
                            results["channels"]["tested"] += len(sample_channels)
                            for ch in sample_channels:
                                cmd = ch.get("cmd", "")
                                ch_name = ch.get("name", "Unknown Channel")
                                if not cmd:
                                    continue
                                try:
                                    stream_url = client.create_link(cmd)
                                    if test_stream_url(stream_url, client.user_agent, logger_inst):
                                        working_channels.append(ch)
                                        results["channels"]["working"] += 1
                                except Exception as e:
                                    logger_inst.warning(f"Playback check failed for live channel '{ch_name}': {e}")
                        
                        # Generate M3U content for working channels
                        from apps.channels.models import Stream
                        m3u_lines = ["#EXTM3U\n"]
                        for ch in working_channels:
                            ch_id = ch.get("id", "")
                            ch_name = ch.get("name", "Unknown Channel")
                            ch_logo = ch.get("logo", "")
                            genre_id = ch.get("tv_genre_id", "")
                            genre_name = genres.get(str(genre_id), "Stalker TV")
                            cmd = ch.get("cmd", "")
                            
                            # Build dynamic proxy URL
                            encoded_cmd = base64.b64encode(cmd.encode("utf-8")).decode("utf-8")
                            play_url = f"{local_stream_host}/stalker/play/{portal_key}/?cmd={encoded_cmd}"
                            
                            # Resolve relative logos
                            resolved_logo = ""
                            if ch_logo:
                                if ch_logo.startswith("http://") or ch_logo.startswith("https://"):
                                    resolved_logo = ch_logo
                                else:
                                    from urllib.parse import urljoin
                                    resolved_logo = urljoin(p_url, ch_logo)

                            # Determine stream identity hash to check if it already exists
                            stream_hash = Stream.generate_hash_key(
                                name=ch_name,
                                url=play_url,
                                tvg_id=ch_id,
                                m3u_id=account.id,
                                group=genre_name,
                                account_type="STD"
                            )
                            
                            # Prefix name if new
                            is_new_stream = not Stream.objects.filter(m3u_account=account, stream_hash=stream_hash).exists()
                            display_name = f"🆕 {ch_name}" if (is_new_stream and mark_new_entries) else ch_name

                            m3u_lines.append(f'#EXTINF:-1 tvg-id="{ch_id}" tvg-name="{display_name}" tvg-logo="{resolved_logo}" group-title="{genre_name}",{display_name}\n')
                            m3u_lines.append(f"{play_url}\n")

                        # Write M3U file
                        with open(m3u_file_path, "w", encoding="utf-8") as f:
                            f.writelines(m3u_lines)

                        # Trigger ArgusFlix Standard M3U parsing
                        refresh_single_m3u_account.delay(account.id)
                        results["channels"]["imported"] += len(working_channels)
                    else:
                        # Write empty M3U if Live TV sync is disabled
                        if not os.path.exists(m3u_file_path):
                            with open(m3u_file_path, "w", encoding="utf-8") as f:
                                f.write("#EXTM3U\n")
                        logger_inst.info(f"Stalker '{p_name}': Selective sync - Live TV disabled, skipped.")


                    # --- PART 2: SELECTIVE SYNC - VOD MOVIES ---
                    if sync_movies:
                        movies = []
                        try:
                            movies = client.get_movies()
                        except Exception as e:
                            logger_inst.warning(f"Stalker '{p_name}': Failed to fetch VOD movies (might be unsupported or empty): {e}")
                        results["movies"]["found"] += len(movies)

                        filtered_movies = []
                        for mv in movies:
                            mv_name = mv.get("name", "Unknown Movie")
                            mv_cat = mv.get("category_name", "Movies")
                            if is_filtered(mv_name, mv_cat, whitelist_cats, blacklist_cats, blacklist_keywords):
                                continue
                            filtered_movies.append(mv)

                        logger_inst.info(f"Stalker '{p_name}': Selective sync - Loaded {len(movies)} movies, {len(filtered_movies)} passed pre-import filters.")

                        from apps.vod.models import Movie, M3UMovieRelation, VODCategory, VODLogo
                        
                        working_movies = []
                        if filtered_movies:
                            sample_movies = random.sample(filtered_movies, min(len(filtered_movies), test_sample_size))
                            results["movies"]["tested"] += len(sample_movies)
                            for mv in sample_movies:
                                cmd = mv.get("cmd", "")
                                mv_name = mv.get("name", "Unknown Movie")
                                if not cmd:
                                    continue
                                try:
                                    stream_url = client.create_link(cmd)
                                    if test_stream_url(stream_url, client.user_agent, logger_inst):
                                        working_movies.append(mv)
                                        results["movies"]["working"] += 1
                                except Exception as e:
                                    logger_inst.warning(f"Playback check failed for movie '{mv_name}': {e}")

                        # Import tested movies
                        for mv in working_movies:
                            mv_id = str(mv.get("id"))
                            mv_name = mv.get("name", "Unknown Movie")
                            mv_cat = mv.get("category_name", "Movies")
                            mv_logo = mv.get("logo", "")
                            mv_cmd = mv.get("cmd", "")
                            
                            year = None
                            year_match = re.search(r"\((\d{4})\)", mv_name)
                            if year_match:
                                year = int(year_match.group(1))

                            cat_obj, _ = VODCategory.objects.get_or_create(
                                name=mv_cat,
                                category_type='movie'
                            )

                            logo_obj = None
                            if mv_logo:
                                resolved_logo = mv_logo if (mv_logo.startswith("http://") or mv_logo.startswith("https://")) else requests.compat.urljoin(p_url, mv_logo)
                                logo_obj, _ = VODLogo.objects.get_or_create(
                                    name=mv_name,
                                    defaults={"url": resolved_logo}
                                )

                            # Highlight new entries with 🆕
                            is_new_movie = not Movie.objects.filter(name=mv_name, year=year).exists()
                            display_name = f"🆕 {mv_name}" if (is_new_movie and mark_new_entries) else mv_name

                            movie_obj, _ = Movie.objects.update_or_create(
                                name=display_name,
                                defaults={
                                    "description": mv.get("description") or "",
                                    "year": year,
                                    "genre": mv_cat,
                                    "logo": logo_obj,
                                }
                            )

                            M3UMovieRelation.objects.update_or_create(
                                m3u_account=account,
                                stream_id=mv_id,
                                defaults={
                                    "movie": movie_obj,
                                    "category": cat_obj,
                                    "container_extension": "mp4",
                                    "custom_properties": {
                                        "cmd": mv_cmd,
                                        "stalker_id": mv_id,
                                    }
                                }
                            )
                            results["movies"]["imported"] += 1
                    else:
                        logger_inst.info(f"Stalker '{p_name}': Selective sync - VOD Movies disabled, skipped.")


                    # --- PART 3: SELECTIVE SYNC - TV SERIES & EPISODES ---
                    if sync_series:
                        series_list = []
                        try:
                            series_list = client.get_series()
                        except Exception as e:
                            logger_inst.warning(f"Stalker '{p_name}': Failed to fetch TV series (might be unsupported or empty): {e}")
                        results["series"]["found"] += len(series_list)

                        filtered_series = []
                        for sr in series_list:
                            sr_name = sr.get("name", "Unknown Series")
                            sr_cat = sr.get("category_name", "TV Series")
                            if is_filtered(sr_name, sr_cat, whitelist_cats, blacklist_cats, blacklist_keywords):
                                continue
                            filtered_series.append(sr)

                        logger_inst.info(f"Stalker '{p_name}': Selective sync - Loaded {len(series_list)} TV Series, {len(filtered_series)} passed pre-import filters.")

                        from apps.vod.models import Series, Episode, M3USeriesRelation, M3UEpisodeRelation, VODCategory, VODLogo
                        
                        working_series_episodes = []
                        if filtered_series:
                            sample_series = random.sample(filtered_series, min(len(filtered_series), test_sample_size))
                            for sr in sample_series:
                                sr_id = str(sr.get("id"))
                                sr_name = sr.get("name", "Unknown Series")
                                
                                episodes = client.get_episodes(sr_id)
                                results["episodes"]["found"] += len(episodes)
                                
                                if episodes:
                                    # Validate playability of a random episode in series
                                    ep = random.choice(episodes)
                                    cmd = ep.get("cmd", "")
                                    ep_name = ep.get("name", "Unknown Episode")
                                    
                                    results["episodes"]["tested"] += 1
                                    try:
                                        stream_url = client.create_link(cmd)
                                        if test_stream_url(stream_url, client.user_agent, logger_inst):
                                            working_series_episodes.append((sr, episodes))
                                            results["series"]["working"] += 1
                                            results["episodes"]["working"] += 1
                                    except Exception as e:
                                        logger_inst.warning(f"Playback check failed for episode '{ep_name}' in series '{sr_name}': {e}")

                        # Import verified series and their episodes
                        for sr, episodes in working_series_episodes:
                            sr_id = str(sr.get("id"))
                            sr_name = sr.get("name", "Unknown Series")
                            sr_cat = sr.get("category_name", "TV Series")
                            sr_logo = sr.get("logo", "")

                            cat_obj, _ = VODCategory.objects.get_or_create(
                                name=sr_cat,
                                category_type='series'
                            )

                            logo_obj = None
                            if sr_logo:
                                resolved_logo = sr_logo if (sr_logo.startswith("http://") or sr_logo.startswith("https://")) else requests.compat.urljoin(p_url, sr_logo)
                                logo_obj, _ = VODLogo.objects.get_or_create(
                                    name=sr_name,
                                    defaults={"url": resolved_logo}
                                )

                            # Highlight new Series with 🆕
                            is_new_series = not Series.objects.filter(name=sr_name).exists()
                            series_display_name = f"🆕 {sr_name}" if (is_new_series and mark_new_entries) else sr_name

                            series_obj, _ = Series.objects.update_or_create(
                                name=series_display_name,
                                defaults={
                                    "genre": sr_cat,
                                    "logo": logo_obj,
                                }
                            )

                            series_rel, _ = M3USeriesRelation.objects.update_or_create(
                                m3u_account=account,
                                external_series_id=sr_id,
                                defaults={
                                    "series": series_obj,
                                    "category": cat_obj,
                                }
                            )
                            results["series"]["imported"] += 1

                            # Populate all episodes
                            for ep in episodes:
                                ep_id = str(ep.get("id"))
                                ep_name = ep.get("name", f"Episode {ep.get('number', '0')}")
                                ep_cmd = ep.get("cmd", "")
                                
                                season_no = int(ep.get("season_number", 1) or 1)
                                episode_no = int(ep.get("number", 1) or (ep.get("episode_number", 1) or 1))

                                # Highlight new Episode with 🆕
                                is_new_episode = not Episode.objects.filter(series=series_obj, season_number=season_no, episode_number=episode_no).exists()
                                episode_display_name = f"🆕 {ep_name}" if (is_new_episode and mark_new_entries) else ep_name

                                episode_obj, _ = Episode.objects.update_or_create(
                                    series=series_obj,
                                    season_number=season_no,
                                    episode_number=episode_no,
                                    defaults={
                                        "name": episode_display_name,
                                    }
                                )

                                M3UEpisodeRelation.objects.update_or_create(
                                    m3u_account=account,
                                    stream_id=ep_id,
                                    defaults={
                                        "episode": episode_obj,
                                        "series_relation": series_rel,
                                        "container_extension": "mp4",
                                        "custom_properties": {
                                            "cmd": ep_cmd,
                                            "stalker_id": ep_id,
                                        }
                                    }
                                )
                                results["episodes"]["imported"] += 1
                    else:
                        logger_inst.info(f"Stalker '{p_name}': Selective sync - TV Series disabled, skipped.")

                    results["portals_processed"] += 1

                except Exception as e:
                    logger_inst.exception(f"Stalker: Failed to complete sync for portal '{p_name}': {e}")
                    return {"status": "error", "message": f"Sync failed for portal '{p_name}': {str(e)}"}

            return {
                "status": "ok",
                "message": f"Successfully completed sync for {results['portals_processed']} portal(s).",
                "details": results
            }

        return {"status": "error", "message": f"Unknown action: {action}"}
