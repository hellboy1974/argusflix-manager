import json
import logging
import os
import re
import socket
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from django.utils import timezone
from apps.m3u.models import M3UAccount
from apps.m3u.tasks import refresh_single_m3u_account
from apps.plugins.models import PluginConfig
import concurrent.futures
import ssl
from urllib.parse import urlparse
import random
import hashlib
try:
    import socks
except ImportError:
    try:
        import subprocess
        import sys
        logger.info("PySocks not found. Attempting to install PySocks automatically...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySocks", "--quiet"])
        import socks
        logger.info("PySocks installed successfully.")
    except Exception as e:
        logger.warning(f"Failed to auto-install PySocks: {e}. Stubbing socks module.")
        class socks_stub:
            SOCKS5 = 1
            SOCKS4 = 2
            HTTP = 3
            class socksocket(socket.socket):
                def set_proxy(self, *args, **kwargs):
                    raise RuntimeError("SOCKS proxy support requires the 'PySocks' package. Please install it manually or check internet connection.")
        socks = socks_stub()

# Set up logging
logger = logging.getLogger("stalker_toolbox")

# Disable warning for SSL
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Common constants from scripts
COMMON_PORTS = [80, 443, 8080, 8880, 25461, 2052, 2082, 2086, 2095, 8443, 8844, 8888, 9000, 9600]
ADMIN_PAYLOADS = ['/c/', '/portal.php', '/server/load.php', '/portalstb/', '/stalker_portal/server/load.php', '/portal.php/c/', '/stalker_portal', '/admin/', '/panel/', '/login/', '/manager/', '/web/', '/xc/', '/xtream/']
ADMIN_USER_AGENTS = [
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/537.36',
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/537.36',
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +https://www.cloudflare.com/always-online) AppleWebKit/534.34'
]
COMMON_SUBDOMAINS = ['www', 'api', 'portal', 'stream', 'tv', 'iptv', 'live', 'm', 'mobile', 'secure', 'admin', 'login', 'panel', 'cdn', 'video', 'play']

STB_MODELS_LIST = ['MAG250', 'MAG254', 'MAG322', 'MAG324', 'MAG420', 'MAG520', 'FormulerZ8', 'DreamBoxOne', 'Enigma2']

COUNTRY_EMOJIS = {
    'US': '🇺🇸', 'GB': '🇬🇧', 'CA': '🇨🇦', 'AU': '🇦🇺', 'DE': '🇩🇪', 'FR': '🇫🇷', 'IT': '🇮🇹', 'ES': '🇪🇸',
    'NL': '🇳🇱', 'BE': '🇧🇪', 'CH': '🇨🇭', 'AT': '🇦🇹', 'SE': '🇸🇪', 'NO': '🇳🇴', 'DK': '🇩🇰', 'FI': '🇫🇮',
    'IE': '🇮🇪', 'PT': '🇵🇹', 'PL': '🇵🇱', 'CZ': '🇨🇿', 'HU': '🇭🇺', 'GR': '🇬🇷', 'RO': '🇷🇴', 'BG': '🇧🇬',
    'HR': '🇭🇷', 'RS': '🇷🇸', 'TR': '🇹🇷', 'RU': '🇷🇺', 'UA': '🇺🇦', 'BR': '🇧🇷', 'MX': '🇲🇽', 'IN': '🇮🇳'
}

# ==============================================================================
# Helper functions from scripts
# ==============================================================================
def parse_bulk_input(text):
    pairs = []
    url_pattern = r"(?:PORTAL|Panel|Server|Server_URL)\s*[:➤\-=\s]\s*(https?://\S+)"
    mac_pattern = r"(?:MAC|Mac)\s*[:➤\-=\s]\s*([0-9A-Fa-f:]{17})"

    blocks = re.split(r"\n\s*\n|╭─•|├─•|╰─•|🛰|📍|🌍|✅|📆|📡|▬|#", text)
    for block in blocks:
        u_match = re.search(url_pattern, block, re.IGNORECASE)
        m_match = re.search(mac_pattern, block, re.IGNORECASE)
        if u_match and m_match:
            u = u_match.group(1).rstrip("/")
            m = m_match.group(1).upper().replace("-", ":")
            pairs.append((u, m))

    if not pairs:
        urls = re.findall(url_pattern, text, re.IGNORECASE)
        macs = re.findall(mac_pattern, text, re.IGNORECASE)
        urls = [u.rstrip("/") for u in urls]
        macs = [m.upper().replace("-", ":") for m in macs]
        pairs = list(zip(urls, macs))

    # Fallback to unlabelled parsing
    if not pairs:
        raw_urls = re.findall(r"(https?://[^\s|;,\"\']+)", text)
        raw_macs = re.findall(r"\b([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})\b", text)
        if len(raw_urls) == len(raw_macs) and raw_urls:
            pairs = [(u.rstrip("/"), m.upper().replace("-", ":")) for u, m in zip(raw_urls, raw_macs)]
        else:
            for line in text.splitlines():
                u_m = re.search(r"(https?://[^\s|;,\"\']+)", line)
                m_m = re.search(r"\b([0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2})\b", line)
                if u_m and m_m:
                    pairs.append((u_m.group(1).rstrip("/"), m_m.group(1).upper().replace("-", ":")))

    return pairs

def detect_expiry(data, depth=0):
    if not isinstance(data, dict) or depth > 4:
        return None

    primary_keys = [
        "expire_date", "end_date", "max_view_date", "expire_billing_date",
        "tariff_expired_date", "date_end", "exp_date", "expDate", "expired",
        "expires", "expiry_date", "access_end", "end_date_time", "valid_until",
        "end", "to", "active_until"
    ]

    unlimited_values = [
        "unlimited", "lifetime", "never", "infinity", "infinite", "permanent",
        "forever", "no expiry", "no limit", "no expiration"
    ]

    for key in primary_keys:
        val = data.get(key)
        if val is not None:
            val_str = str(val).strip().lower()
            if val_str in unlimited_values:
                return str(val)
            if val_str not in ["", "0", "0000-00-00", "0000-00-00 00:00:00", "null", "none", "false"]:
                return str(val)

    for k, v in data.items():
        if v is None:
            continue
        k_low = str(k).lower()
        v_str = str(v).strip()
        if not v_str:
            continue

        if any(x in k_low for x in ["expire", "end_date", "valid_until", "exp_date", "access_end"]):
            if v_str.lower() not in ["0", "0000-00-00", "0000-00-00 00:00:00", "null", "none", "false"]:
                if "-" in v_str or (v_str.isdigit() and len(v_str) >= 10):
                    return v_str

    sub_keys = ["account_info", "stb_account", "active_sub", "billing", "profile", "payment", "tariff", "subscription", "services"]
    for sub in sub_keys:
        sub_data = data.get(sub)
        if isinstance(sub_data, dict):
            res = detect_expiry(sub_data, depth + 1)
            if res:
                return res
        elif isinstance(sub_data, list):
            for item in sub_data:
                if isinstance(item, dict):
                    res = detect_expiry(item, depth + 1)
                    if res:
                        return res

    return None

# ==============================================================================
# Helper functions for Security Signatures and Path cleaning
# ==============================================================================
def clean_base_url(url):
    parsed = urlparse(url)
    path = parsed.path
    if path.endswith("/c/"):
        path = path[:-3]
    elif path.endswith("/c"):
        path = path[:-2]
    elif path.endswith("/"):
        path = path[:-1]
    
    port_str = f":{parsed.port}" if parsed.port and parsed.port not in [80, 443] else ""
    return f"{parsed.scheme}://{parsed.hostname}{port_str}{path}"

def get_security_params(mac):
    mac_clean = mac.strip().upper().replace("-", ":")
    serialnumber = hashlib.md5(mac_clean.encode()).hexdigest().upper()
    sn = serialnumber[0:13]
    device_id = hashlib.sha256(sn.encode()).hexdigest().upper()
    device_id2 = hashlib.sha256(mac_clean.encode()).hexdigest().upper()
    hw_version_2 = hashlib.sha1(mac_clean.encode()).hexdigest()
    snmac = f"{sn}{mac_clean}"
    sig = hashlib.sha256(snmac.encode()).hexdigest().upper()
    return {
        "sn": sn,
        "device_id": device_id,
        "device_id2": device_id2,
        "hw_version_2": hw_version_2,
        "sig": sig
    }

COMMON_PORTAL_PATHS = [
    "/server/load.php",
    "/portal.php",
    "/c/server/load.php",
    "/c/portal.php",
    "/stalker_portal/server/load.php",
    "/magaccess/portal.php",
    "/portalcc.php",
    "/bs.mag.portal.php",
    "/magportal/portal.php",
    "/maglove/portal.php",
    "/tek/server/load.php",
    "/emu/server/load.php",
    "/emu2/server/load.php",
    "/ghandi_portal/server/load.php",
    "/magLoad.php",
    "/ministra/portal.php",
    "/portalstb/portal.php",
    "/portalmega.php",
    "/rmxportal/portal.php",
    "/powerfull/portal.php",
    "/korisnici/server/load.php",
    "/nettvmag/portal.php",
    "/cmdforex/portal.php",
    "/k/portal.php",
    "/p/portal.php",
    "/cp/server/load.php",
    "/extraportal.php",
    "/Link_Ok/portal.php",
    "/delko/portal.php",
    "/client/portal.php",
    "/magportal",
    "/magaccess",
    "/powerfull",
    "/client",
    "/ministra",
    "/portalstb",
    "/cmdforex",
    "/maglove",
    "/xui"
]

def parse_proxies_text(text):
    if not text or not text.strip():
        return []
    proxies = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(('#', '//')):
            continue
        if re.match(r'^[a-zA-Z0-9]+://', line):
            proxies.append(line)
        else:
            proxies.append(f"socks5h://{line}")
    return proxies

def fetch_and_parse_proxies(proxies_paste, proxy_urls_text):
    proxies = parse_proxies_text(proxies_paste)
    if not proxy_urls_text or not proxy_urls_text.strip():
        return proxies
        
    for line in proxy_urls_text.splitlines():
        url = line.strip()
        if not url or url.startswith(('#', '//')):
            continue
        if not url.startswith(('http://', 'https://')):
            continue
            
        try:
            logger.info(f"Fetching proxy list from: {url}")
            resp = requests.get(url, timeout=5, verify=False)
            if resp.status_code == 200:
                fetched = parse_proxies_text(resp.text)
                logger.info(f"Fetched {len(fetched)} proxies from {url}")
                proxies.extend(fetched)
            else:
                logger.warning(f"Failed to fetch proxy list from {url} (status: {resp.status_code})")
        except Exception as e:
            logger.warning(f"Error fetching proxies from {url}: {e}")
            
    # Deduplicate while preserving order
    seen = set()
    unique_proxies = []
    for p in proxies:
        if p not in seen:
            seen.add(p)
            unique_proxies.append(p)
    return unique_proxies

_PROXY_CACHE = {
    "proxies": [],
    "last_updated": 0
}

def get_proxies_list(settings, force_refresh=False):
    global _PROXY_CACHE
    now = time.time()
    # Cache external URL fetches for 5 minutes (300 seconds) to avoid slowing play redirects
    if force_refresh or now - _PROXY_CACHE["last_updated"] > 300 or not _PROXY_CACHE["proxies"]:
        proxies_paste = settings.get("proxies_paste", "")
        proxy_urls_text = settings.get("proxy_urls", "")
        _PROXY_CACHE["proxies"] = fetch_and_parse_proxies(proxies_paste, proxy_urls_text)
        _PROXY_CACHE["last_updated"] = now
    return _PROXY_CACHE["proxies"]

def create_proxied_socket(proxy=None):
    if not proxy:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        parsed = urlparse(proxy)
        scheme = parsed.scheme.lower() if parsed.scheme else "socks5h"
        
        if "socks5" in scheme:
            proxy_type = socks.SOCKS5
        elif "socks4" in scheme:
            proxy_type = socks.SOCKS4
        elif "http" in scheme or "https" in scheme:
            proxy_type = socks.HTTP
        else:
            proxy_type = socks.SOCKS5
            
        s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
        s.set_proxy(
            proxy_type=proxy_type,
            addr=parsed.hostname,
            port=parsed.port,
            username=parsed.username,
            password=parsed.password
        )
        return s
    except Exception as e:
        logger.warning(f"Failed to create proxied socket: {e}. Falling back to default socket.")
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ==============================================================================
# Stalker Portal API Client
# ==============================================================================
class StalkerClient:
    def __init__(self, url, mac, user_agent=None, proxy=None):
        self.url = url.rstrip("/")
        self.mac = mac.strip().upper().replace("-", ":")
        self.user_agent = user_agent or "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3"
        self.session = requests.Session()
        if proxy:
            self.session.proxies = {
                "http": proxy,
                "https": proxy
            }
        
        self.sec = get_security_params(self.mac)
        
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "*/*",
            "Accept-Encoding": "identity",
            "Connection": "keep-alive"
        })
        self.session.cookies.update({
            "mac": self.mac,
            "sn": self.sec["sn"],
            "device_id": self.sec["device_id"],
            "device_id2": self.sec["device_id2"],
            "adid": self.sec["hw_version_2"],
            "hw_version": "1.7-BD-00",
            "stb_lang": "en",
            "timezone": "America/Los_Angeles"
        })
        self.token = None
        self.token_random = None
        self.active_path = None

    def handshake(self):
        base_url = clean_base_url(self.url)
        paths_to_try = [p for p in COMMON_PORTAL_PATHS]
        
        parsed_orig = urlparse(self.url)
        if parsed_orig.path.endswith(".php"):
            paths_to_try.insert(0, parsed_orig.path)
            
        for path in paths_to_try:
            ep_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
            
            queries = [
                "?type=stb&action=handshake&js=true",
                "?action=handshake&type=stb&token=&JsHttpRequest=1-xml"
            ]
            
            for q in queries:
                try:
                    hs_url = f"{ep_url}{q}"
                    resp = self.session.get(hs_url, timeout=5, verify=False)
                    if resp.status_code == 404:
                        continue
                        
                    resp.raise_for_status()
                    txt = resp.text
                    
                    data = None
                    try:
                        data = resp.json()
                    except Exception:
                        m = re.search(r'"token"\s*:\s*"([^"]+)"', txt)
                        if m:
                            data = {"token": m.group(1)}
                        else:
                            m_js = re.search(r'"js"\s*:\s*({[^}]+})', txt)
                            if m_js:
                                try:
                                    data = {"js": json.loads(m_js.group(1))}
                                except Exception:
                                    pass

                    if isinstance(data, dict):
                        token = data.get("token")
                        token_random = data.get("random")
                        if "js" in data and isinstance(data["js"], dict):
                            token = token or data["js"].get("token")
                            token_random = token_random or data["js"].get("random")
                        
                        if token:
                            self.token = token
                            self.token_random = token_random
                            self.active_path = ep_url
                            
                            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                            self.session.cookies.update({"token": self.token})
                            
                            if self.token_random:
                                self.session.headers.update({"X-Random": str(self.token_random)})
                            return True
                except Exception:
                    continue
        return False

    def get_profile(self):
        if not self.token and not self.handshake():
            return None
        try:
            if self.token_random:
                sig_rand = hashlib.sha256(str(self.token_random).encode()).hexdigest().upper()
                metrics = {
                    "mac": self.mac,
                    "sn": self.sec["sn"],
                    "type": "STB",
                    "model": "MAG250",
                    "uid": self.sec["device_id"],
                    "random": self.token_random
                }
                metrics_json = json.dumps(metrics)
                metrics_encoded = urllib.parse.quote(metrics_json)
                
                profile_url = (
                    f"{self.active_path}?type=stb&action=get_profile&hd=1"
                    f"&ver=ImageDescription: 0.2.18-r23-250; ImageDate: Wed Aug 29 10:49:53 EEST 2018; PORTAL version: 5.3.1; API Version: JS API version: 343; STB API version: 146; Player Engine version: 0x58c"
                    f"&num_banks=2&sn={self.sec['sn']}&stb_type=MAG250&client_type=STB&image_version=218&video_out=hdmi"
                    f"&device_id={self.sec['device_id2']}&device_id2={self.sec['device_id2']}&sig={sig_rand}&auth_second_step=1"
                    f"&hw_version=1.7-BD-00&not_valid_token=0&metrics={metrics_encoded}&hw_version_2={self.sec['hw_version_2']}"
                    f"&timestamp={round(time.time())}&api_sig=262&prehash=0"
                )
            else:
                profile_url = f"{self.active_path}?type=stb&action=get_profile"
                
            resp = self.session.get(profile_url, timeout=10, verify=False)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "js" in data:
                return data["js"]
            return data
        except Exception:
            try:
                simple_url = f"{self.active_path}?type=stb&action=get_profile"
                resp = self.session.get(simple_url, timeout=10, verify=False)
                data = resp.json()
                if isinstance(data, dict) and "js" in data:
                    return data["js"]
                return data
            except Exception:
                return None

    def get_account_info(self):
        if not self.token and not self.handshake():
            return None
        try:
            acc_url = f"{self.active_path}?type=stb&action=get_account_info"
            resp = self.session.get(acc_url, timeout=10, verify=False)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "js" in data:
                return data["js"]
            return data
        except Exception:
            return None

    def get_all_channels(self):
        if not self.token and not self.handshake():
            return []
        try:
            channels_url = f"{self.active_path}?type=itv&action=get_all_channels"
            resp = self.session.get(channels_url, timeout=15, verify=False)
            resp.raise_for_status()
            data = resp.json()
            
            channels = []
            if isinstance(data, dict):
                if "js" in data:
                    js_data = data["js"]
                    if isinstance(js_data, list):
                        channels = js_data
                    elif isinstance(js_data, dict) and "data" in js_data:
                        channels = js_data["data"]
                elif "data" in data:
                    channels = data["data"]
            return channels if isinstance(channels, list) else []
        except Exception:
            return []

    def get_genres(self):
        if not self.token and not self.handshake():
            return []
        try:
            url = f"{self.active_path}?type=itv&action=get_genres&JsHttpRequest=1-xml"
            resp = self.session.get(url, timeout=10, verify=False)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "js" in data:
                return data["js"]
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def get_vod_categories(self):
        if not self.token and not self.handshake():
            return []
        try:
            url = f"{self.active_path}?type=vod&action=get_categories&JsHttpRequest=1-xml"
            resp = self.session.get(url, timeout=10, verify=False)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "js" in data:
                return data["js"]
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def get_series_categories(self):
        if not self.token and not self.handshake():
            return []
        try:
            url = f"{self.active_path}?type=series&action=get_categories&JsHttpRequest=1-xml"
            resp = self.session.get(url, timeout=10, verify=False)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "js" in data:
                return data["js"]
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def get_ordered_list(self, type_str, category_id, limit=100):
        if not self.token and not self.handshake():
            return []
        try:
            items = []
            page = 0
            total_items = 0
            
            # Fetch first page to get total items
            url = f"{self.active_path}?type={type_str}&action=get_ordered_list&category={category_id}&p={page}&JsHttpRequest=1-xml"
            resp = self.session.get(url, timeout=10, verify=False)
            resp.raise_for_status()
            res_json = resp.json()
            
            js_data = res_json.get("js", {})
            if isinstance(js_data, dict):
                total_items = int(js_data.get("total_items", 0))
                first_page_items = js_data.get("data", [])
                items.extend(first_page_items)
                
                items_per_page = len(first_page_items)
                if items_per_page > 0:
                    total_pages = (total_items + items_per_page - 1) // items_per_page
                else:
                    total_pages = 0
            else:
                total_pages = 0

            max_items = total_items
            if limit > 0:
                max_items = min(limit, total_items)
            
            if len(items) >= max_items or total_pages <= 1:
                return items[:max_items]

            pages_to_fetch = []
            current_count = len(items)
            for p in range(1, total_pages):
                if current_count >= max_items:
                    break
                pages_to_fetch.append(p)
                current_count += items_per_page

            def fetch_page_worker(p_num):
                try:
                    p_url = f"{self.active_path}?type={type_str}&action=get_ordered_list&category={category_id}&p={p_num}&JsHttpRequest=1-xml"
                    p_resp = self.session.get(p_url, timeout=10, verify=False)
                    p_json = p_resp.json()
                    p_data = p_json.get("js", {}).get("data", [])
                    return p_data if isinstance(p_data, list) else []
                except Exception:
                    return []

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                results = executor.map(fetch_page_worker, pages_to_fetch)
                for res in results:
                    items.extend(res)
                    if limit > 0 and len(items) >= limit:
                        return items[:limit]

            if limit > 0:
                return items[:limit]
            return items
        except Exception:
            return []

    def get_series_episodes(self, series_id):
        if not self.token and not self.handshake():
            return []
        try:
            episodes = []
            page = 0
            url = f"{self.active_path}?type=series&action=get_ordered_list&movie_id={series_id}&season_id=0&episode_id=0&p={page}&JsHttpRequest=1-xml"
            resp = self.session.get(url, timeout=10, verify=False)
            resp.raise_for_status()
            res_json = resp.json()
            
            js_data = res_json.get("js", {})
            if isinstance(js_data, dict):
                total_items = int(js_data.get("total_items", 0))
                first_page_episodes = js_data.get("data", [])
                episodes.extend(first_page_episodes)
                
                items_per_page = len(first_page_episodes)
                if items_per_page > 0:
                    total_pages = (total_items + items_per_page - 1) // items_per_page
                else:
                    total_pages = 0
            else:
                total_pages = 0
                
            if len(episodes) >= total_items or total_pages <= 1:
                return episodes
                
            for p in range(1, total_pages):
                try:
                    p_url = f"{self.active_path}?type=series&action=get_ordered_list&movie_id={series_id}&season_id=0&episode_id=0&p={p}&JsHttpRequest=1-xml"
                    p_resp = self.session.get(p_url, timeout=10, verify=False)
                    p_json = p_resp.json()
                    p_data = p_json.get("js", {}).get("data", [])
                    if isinstance(p_data, list):
                        episodes.extend(p_data)
                except Exception:
                    pass
            return episodes
        except Exception:
            return []

    def create_link(self, cmd, is_vod=False):
        if not self.token and not self.handshake():
            return None
        try:
            encoded_cmd = urllib.parse.quote(cmd)
            type_val = "vod" if is_vod else "itv"
            link_url = f"{self.active_path}?type={type_val}&action=create_link&cmd={encoded_cmd}&js=true"
            resp = self.session.get(link_url, timeout=10, verify=False)
            resp.raise_for_status()
            data = resp.json()
            
            link = None
            if isinstance(data, dict):
                if "js" in data:
                    js_data = data["js"]
                    if isinstance(js_data, str):
                        link = js_data
                    elif isinstance(js_data, dict) and "cmd" in js_data:
                        link = js_data["cmd"]
                elif "cmd" in data:
                    link = data["cmd"]
            return link
        except Exception:
            return None

# ==============================================================================
# Local Redirect Proxy Server Thread
# ==============================================================================
class StalkerProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.debug(f"Proxy connection: {format % args}")

    def do_GET(self):
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) >= 3 and path_parts[0] == "play":
            portal_name = path_parts[1]
            channel_id = path_parts[2]
            
            plugin_settings = getattr(self.server, "plugin_settings", {})
            portals = plugin_settings.get("portals_json", "[]")
            try:
                portals_list = json.loads(portals)
            except Exception:
                portals_list = []
                
            portal_config = next((p for p in portals_list if p.get("name") == portal_name), None)
            if not portal_config:
                self.send_error(404, f"Portal '{portal_name}' not configured")
                return
                
            mapping_file = f"/data/stalker_channels_{portal_name}.json"
            if not os.path.exists(mapping_file):
                self.send_error(404, f"Channel mapping file missing. Perform 'Sync Playlists' action.")
                return
                
            try:
                with open(mapping_file, "r", encoding="utf-8") as f:
                    mapping = json.load(f)
            except Exception as e:
                self.send_error(500, f"Failed to read channel map: {e}")
                return
                
            mapping_data = mapping.get(str(channel_id))
            if not mapping_data:
                self.send_error(404, f"Channel ID '{channel_id}' not found in map")
                return
                
            if isinstance(mapping_data, dict):
                cmd = mapping_data.get("cmd")
                is_vod = mapping_data.get("is_vod", False)
            else:
                cmd = mapping_data
                is_vod = False
                
            proxies_list = get_proxies_list(plugin_settings, force_refresh=False)
            proxy = random.choice(proxies_list) if proxies_list else None
            
            client = StalkerClient(
                url=portal_config.get("url"),
                mac=portal_config.get("mac"),
                user_agent=portal_config.get("user_agent"),
                proxy=proxy
            )
            
            real_url = client.create_link(cmd, is_vod=is_vod)
            if not real_url:
                self.send_error(502, "Stalker portal rejected stream generation")
                return
                
            clean_url = real_url.strip()
            if clean_url.startswith("ffmpeg "):
                clean_url = clean_url[7:].strip()
            elif clean_url.startswith("rtmp "):
                clean_url = clean_url[5:].strip()
                
            logger.info(f"Redirecting play request to Stalker stream URL: {clean_url}")
            
            self.send_response(302)
            self.send_header("Location", clean_url)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Stalker Portal Proxy running. format: /play/<portal_name>/<channel_id>")

class StalkerProxyServer:
    def __init__(self, port, plugin_settings):
        self.port = int(port)
        self.plugin_settings = plugin_settings
        self.server = None
        self.thread = None
        self.is_running = False

    def start(self):
        if self.is_running:
            return
        try:
            self.server = HTTPServer(("0.0.0.0", self.port), StalkerProxyHandler)
            self.server.plugin_settings = self.plugin_settings
            
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            self.is_running = True
            logger.info(f"Stalker redirect proxy server started on port {self.port}")
        except Exception as e:
            logger.error(f"Failed to start proxy server on port {self.port}: {e}")

    def stop(self):
        if not self.is_running or not self.server:
            return
        try:
            self.server.shutdown()
            self.server.server_close()
            self.is_running = False
            logger.info("Stalker redirect proxy server stopped")
        except Exception as e:
            logger.error(f"Error stopping proxy server: {e}")

_PROXY_SERVER = None

def ensure_proxy_running(settings):
    global _PROXY_SERVER
    port = int(settings.get("proxy_port", 8282))
    
    if _PROXY_SERVER:
        if _PROXY_SERVER.port == port and _PROXY_SERVER.is_running:
            _PROXY_SERVER.plugin_settings = settings
            _PROXY_SERVER.server.plugin_settings = settings
            return
        else:
            _PROXY_SERVER.stop()
            
    _PROXY_SERVER = StalkerProxyServer(port, settings)
    _PROXY_SERVER.start()

# ==============================================================================
# Multi-threaded MAC Range Scanner Background Loop
# ==============================================================================
_SCAN_STATUS = {
    "running": False,
    "portal": None,
    "current_mac": None,
    "checked": 0,
    "total": 0,
    "active_found": 0,
    "results": []
}

def mac_to_int(mac):
    clean = mac.replace(":", "").replace("-", "").strip()
    return int(clean, 16)

def int_to_mac(val):
    h = f"{val:012X}"
    return ":".join(h[i:i+2] for i in range(0, 12, 2))

def run_mac_scan_threaded(portal_config, start_mac, end_mac, cooldown, thread_count, proxies_list=None):
    global _SCAN_STATUS
    
    _SCAN_STATUS["running"] = True
    _SCAN_STATUS["portal"] = portal_config["name"]
    _SCAN_STATUS["checked"] = 0
    _SCAN_STATUS["active_found"] = 0
    _SCAN_STATUS["results"] = []
    
    try:
        start_val = mac_to_int(start_mac)
        end_val = mac_to_int(end_mac)
    except Exception as e:
        logger.error(f"Invalid MAC format: {e}")
        _SCAN_STATUS["running"] = False
        return
        
    if start_val > end_val:
        start_val, end_val = end_val, start_val
        
    total_macs = end_val - start_val + 1
    _SCAN_STATUS["total"] = total_macs
    
    logger.info(f"MAC range scan started (threads={thread_count}): {start_mac} to {end_mac} ({total_macs} MACs) on portal '{portal_config['name']}'")
    
    results_file = "/data/stalker_scan_results.txt"
    try:
        with open(results_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- SCAN STARTED: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            f.write(f"Portal: {portal_config['url']}\n")
            f.write(f"Range: {start_mac} to {end_mac}\n")
            f.write("MAC Address | Expiration | Status | Connections\n")
            f.write("--------------------------------------------------\n")
    except Exception as e:
        logger.error(f"Failed to initialize scan results file: {e}")
        
    mac_values = list(range(start_val, end_val + 1))
    
    def check_mac_worker(val):
        global _SCAN_STATUS
        if not _SCAN_STATUS["running"]:
            return None
            
        current_mac = int_to_mac(val)
        _SCAN_STATUS["current_mac"] = current_mac
        
        proxy = None
        if proxies_list:
            proxy = proxies_list[val % len(proxies_list)]
            
        client = StalkerClient(portal_config["url"], current_mac, portal_config.get("user_agent"), proxy=proxy)
        if client.handshake():
            profile = client.get_profile()
            acc_info = client.get_account_info()
            if profile:
                exp_date = detect_expiry(profile) or detect_expiry(acc_info) or "Unlimited"
                status = profile.get("status") or "Active"
                connections = f"{profile.get('active_cons', 0)}/{profile.get('max_connections', 1)}"
                
                logger.info(f"[FOUND VALID MAC] {current_mac} | Exp: {exp_date} | Status: {status} | Cons: {connections}")
                result_str = f"{current_mac} | {exp_date} | {status} | {connections}"
                
                try:
                    with open(results_file, "a", encoding="utf-8") as f:
                        f.write(result_str + "\n")
                except Exception:
                    pass
                return result_str
        
        if cooldown > 0:
            time.sleep(cooldown)
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=int(thread_count)) as executor:
        futures = {executor.submit(check_mac_worker, val): val for val in mac_values}
        for future in concurrent.futures.as_completed(futures):
            if not _SCAN_STATUS["running"]:
                break
            _SCAN_STATUS["checked"] += 1
            res = future.result()
            if res:
                _SCAN_STATUS["active_found"] += 1
                _SCAN_STATUS["results"].append(res)

    _SCAN_STATUS["running"] = False

def urlscan_analyze_portal(url, api_key, ip_address):
    if not api_key:
        return []
        
    headers = {"API-Key": api_key, "Content-Type": "application/json"}
    normalized_url = url.strip()
    if not normalized_url.startswith(("http://", "https://")):
        normalized_url = "http://" + normalized_url
        
    try:
        scan_data = {"url": normalized_url, "visibility": "public"}
        resp = requests.post("https://urlscan.io/api/v1/scan/", json=scan_data, headers=headers, timeout=15)
        if resp.status_code in [200, 201]:
            uuid = resp.json().get("uuid")
            if uuid:
                for _ in range(20):
                    time.sleep(3)
                    res_resp = requests.get(f"https://urlscan.io/api/v1/result/{uuid}/", headers=headers, timeout=10)
                    if res_resp.status_code == 200:
                        break
        else:
            logger.error(f"urlscan.io submission failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        logger.error(f"urlscan.io error during submission: {e}")
        
    similar_portals = []
    if ip_address and ip_address != "Unknown":
        try:
            params = {"q": f"page.ip:{ip_address}", "size": 50}
            resp = requests.get("https://urlscan.io/api/v1/search/", headers=headers, params=params, timeout=10)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                seen = set()
                for item in results:
                    page_url = item.get("page", {}).get("url")
                    if page_url:
                        clean_p = page_url.strip().lower().replace("https://", "").replace("http://", "").replace("www.", "")
                        if clean_p not in seen:
                            seen.add(clean_p)
                            similar_portals.append(page_url)
        except Exception as e:
            logger.error(f"urlscan.io IP search error: {e}")
            
    return similar_portals

def reverse_dns_lookup(ip):
    try:
        rdns, _, _ = socket.gethostbyaddr(ip)
        return rdns
    except Exception:
        return 'Not available'

def scan_port_banner(host, port, proxy=None):
    try:
        with create_proxied_socket(proxy) as s:
            s.settimeout(2.5)
            if s.connect_ex((host, port)) == 0:
                req = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: MAG250\r\nConnection: close\r\n\r\n".encode()
                try:
                    s.send(req)
                    banner = s.recv(512).decode(errors='ignore')
                    status_line = banner.split('\n')[0].strip()
                    if status_line:
                        server_header = "Unknown"
                        for line in banner.split('\n'):
                            if line.lower().startswith("server:"):
                                server_header = line.split(":", 1)[1].strip()
                                break
                        return f"open ({status_line} | Server: {server_header})"
                except Exception:
                    pass
                return "open"
    except Exception:
        pass
    return None

def detect_protection(url, proxy=None):
    protections = {
        'Cloudflare': ['cf-ray', 'cloudflare', '__cfduid', '__cf_bm'],
        'DDoS-Guard': ['ddos-guard'],
        'Sucuri': ['sucuri'],
        'Akamai': ['akamai', 'akamaiedge'],
        'Incapsula': ['incapsula', 'visid_incap'],
        'Nginx': ['nginx'],
        'Apache': ['apache'],
        'LiteSpeed': ['litespeed'],
        'IIS': ['microsoft-iis', 'iis'],
        'OpenResty': ['openresty']
    }
    detected = []
    try:
        proxies_dict = {"http": proxy, "https": proxy} if proxy else None
        resp = requests.get(url, timeout=5, verify=False, proxies=proxies_dict)
        headers_lower = {k.lower(): v.lower() for k, v in resp.headers.items()}
        cookies_lower = [c.lower() for c in resp.cookies.keys()]
        body_lower = resp.text.lower()
        
        for prot, signs in protections.items():
            for sign in signs:
                if any(sign in h for h in headers_lower.values()) or sign in str(cookies_lower) or sign in body_lower:
                    detected.append(prot)
                    break
    except Exception:
        pass
    return detected if detected else ["None/Direct Connection"]

def test_stb_login_fingerprint(url, mac, model, proxy=None):
    headers = {
        'User-Agent': f'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) {model} stbapp ver: 2 rev: 250 Safari/533.3',
        'X-User-Agent': f'Model: {model}; Link: WiFi',
        'Authorization': f'MAC {mac}'
    }
    try:
        probe_url = url.rstrip("/")
        if not probe_url.endswith("/c/"):
            probe_url += "/c/"
            
        proxies_dict = {"http": proxy, "https": proxy} if proxy else None
        resp = requests.get(probe_url, headers=headers, timeout=5, verify=False, proxies=proxies_dict)
        resp_text = resp.text.lower()
        
        if resp.status_code == 200:
            if 'not authorized' in resp_text:
                return "Denied (HTTP 200, Not Authorized)"
            elif 'ok' in resp_text or 'true' in resp_text or 'js' in resp_text:
                return "✅ OK (Authorized)"
            else:
                return "Accepted (HTTP 200, Unknown Body)"
        else:
            return f"Rejected (HTTP {resp.status_code})"
    except Exception as e:
        return f"Failed Connection ({e})"

# ==============================================================================
# Dispatcharr Plugin Hooks
# ==============================================================================
class Plugin:
    name = "Stalker Portal Toolbox"
    version = "1.0.0"
    description = "All-in-One Stalker (Ministra) portal utility. Includes dynamic redirect proxying, portal testing, scanning, MAC generation, and bulk imports."
    author = "Antigravity"
    
    fields = [
        {"id": "sec_core", "label": "⚙️ [ SEKTION 1: CORE CONFIG & MULTI-PORTALS ] ─────────────────────────", "type": "info", "description": ""},
        {"id": "proxy_port", "label": "Proxy Port", "type": "number", "default": 8282},
        {"id": "portals_json", "label": "Portals JSON Configuration", "type": "text", "default": "[]"},
        {"id": "bulk_import_text", "label": "Bulk Import Text / Paste Bin", "type": "text", "default": ""},
        
        {"id": "sec_detective", "label": "🕵️ [ SEKTION 2: PORTAL DETECTIVE ] ────────────────────────────────────", "type": "info", "description": ""},
        {"id": "detective_url", "label": "Detective Target URL", "type": "string", "default": ""},
        {"id": "detective_urlscan_key", "label": "urlscan.io API Key (Optional)", "type": "string", "default": ""},
        {"id": "detective_scan_subdomains", "label": "Enumerate Subdomains", "type": "boolean", "default": False},
        {"id": "detective_scan_ports", "label": "Port Scan Server", "type": "boolean", "default": False},
        
        {"id": "sec_generator", "label": "🔢 [ SEKTION 3: MAC ADDRESS GENERATOR ] ──────────────────────────────", "type": "info", "description": ""},
        {"id": "gen_prefixes", "label": "MAC Prefixes", "type": "string", "default": "00:1A:79:"},
        {"id": "gen_count", "label": "MAC Count per Prefix", "type": "number", "default": 1000},
        {"id": "gen_mode", "label": "Generation Mode", "type": "select", "default": "random", "options": [
            {"value": "random", "label": "Random Suffix"},
            {"value": "ascending", "label": "Sequential Ascending"},
            {"value": "descending", "label": "Sequential Descending"}
        ]},
        {"id": "gen_suffix_start", "label": "Suffix Start (Optional)", "type": "string", "default": ""},
        {"id": "gen_suffix_end", "label": "Suffix Finish (Optional)", "type": "string", "default": ""},
        {"id": "gen_filename", "label": "Output Filename", "type": "string", "default": "combo.txt"},
        
        {"id": "sec_scanner", "label": "🔍 [ SEKTION 4: MAC ADDRESS RANGE SCANNER ] ───────────────────────────", "type": "info", "description": ""},
        {"id": "scan_portal", "label": "Scan Target Portal Name", "type": "string", "default": ""},
        {"id": "scan_mac_start", "label": "Scan MAC Start", "type": "string", "default": "00:1A:79:00:00:00"},
        {"id": "scan_mac_end", "label": "Scan MAC End", "type": "string", "default": "00:1A:79:00:00:FF"},
        {"id": "scan_threads", "label": "Scan Threads (Concurrency)", "type": "number", "default": 5},
        {"id": "scan_cooldown", "label": "Scan Cooldown (seconds)", "type": "number", "default": 1},
        {"id": "sec_proxies", "label": "🔗 [ SEKTION 5: SOCKS5/HTTP PROXY ROTATOR ] ─────────────────────────", "type": "info", "description": ""},
        {"id": "proxies_paste", "label": "Proxies List (Paste Bin)", "type": "text", "default": ""},
        {"id": "proxy_urls", "label": "Proxy list URLs (e.g. GitHub)", "type": "text", "default": ""}
    ]
    
    actions = [
        {"id": "bulk_import_portals", "label": "Bulk Import Combos"},
        {"id": "test_connections", "label": "Test Connections"},
        {"id": "sync_channels", "label": "Sync Playlists"},
        {"id": "run_detective", "label": "Run Portal Detective"},
        {"id": "run_generator", "label": "Generate MACs"},
        {"id": "scan_macs", "label": "Scan MAC Range"}
    ]

    def __init__(self):
        try:
            cfg = PluginConfig.objects.get(key="stalker_toolbox")
            if cfg.enabled:
                ensure_proxy_running(cfg.settings)
        except Exception:
            pass

    def run(self, action: str, params: dict, context: dict):
        settings = context.get("settings", {})
        ensure_proxy_running(settings)
        
        portals_json = settings.get("portals_json", "[]")
        if isinstance(portals_json, str) and portals_json.strip() == "[] Persisted portals list":
            portals_json = "[]"
            
        try:
            portals_list = json.loads(portals_json) if portals_json.strip() else []
        except Exception as e:
            portals_list = []
            if action != "bulk_import_portals":
                return {"status": "error", "message": f"Invalid Portals JSON syntax in settings: {e}"}

        if action == "bulk_import_portals":
            bulk_text = settings.get("bulk_import_text", "")
            if not bulk_text.strip():
                return {"status": "error", "message": "Bulk Import Text / Paste Bin field is empty."}
                
            combos = parse_bulk_input(bulk_text)
            if not combos:
                return {"status": "error", "message": "No valid Portal URL / MAC address combos found in text."}
                
            imported = 0
            for url, mac in combos:
                exists = any(
                    p.get("url").rstrip("/") == url.rstrip("/") and 
                    p.get("mac").upper().replace("-", ":") == mac.upper().replace("-", ":") 
                    for p in portals_list
                )
                if not exists:
                    name = f"portal_{int(time.time() * 1000) % 1000000}_{imported}"
                    portals_list.append({
                        "name": name,
                        "url": url,
                        "mac": mac,
                        "user_agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3",
                        "active": True
                    })
                    imported += 1
                    
            if imported > 0:
                try:
                    cfg = PluginConfig.objects.get(key="stalker_toolbox")
                    cfg.settings["portals_json"] = json.dumps(portals_list, indent=2)
                    cfg.settings["bulk_import_text"] = ""
                    cfg.save()
                    return {"status": "ok", "message": f"Successfully bulk-imported {imported} new portals! Saved to Portals JSON. Reload Plugins tab to view."}
                except Exception as e:
                    return {"status": "error", "message": f"Parsed {imported} portals, but failed to save: {e}"}
            else:
                return {"status": "ok", "message": "Parsed portals, but all found combos were already present in Portals JSON."}

        elif action == "test_connections":
            if not portals_list:
                return {"status": "error", "message": "No portals configured."}
                
            proxies_list = get_proxies_list(settings, force_refresh=True)
            
            outputs = []
            modified = False
            for idx, p in enumerate(portals_list):
                name = p.get("name")
                url = p.get("url")
                mac = p.get("mac")
                if not name or not url or not mac:
                    outputs.append(f"Portal '{name or 'unnamed'}': Missing credentials.")
                    continue
                    
                proxy = proxies_list[idx % len(proxies_list)] if proxies_list else None
                client = StalkerClient(url, mac, p.get("user_agent"), proxy=proxy)
                if client.handshake():
                    profile = client.get_profile()
                    acc_info = client.get_account_info()
                    if profile:
                        status = profile.get("status") or "Active"
                        exp_date = detect_expiry(profile) or detect_expiry(acc_info) or "Unlimited"
                        cons = f"{profile.get('active_cons', 0)}/{profile.get('max_connections', 1)}"
                        
                        p["expiry"] = exp_date
                        p["status"] = status
                        p["connections"] = cons
                        modified = True
                        
                        outputs.append(f"Portal '{name}': SUCCESS! Status: {status} | Expiry: {exp_date} | Connections: {cons}")
                    else:
                        p["status"] = "Handshake OK, Profile Failed"
                        p["expiry"] = "Unknown"
                        p["connections"] = "-"
                        modified = True
                        outputs.append(f"Portal '{name}': Handshake succeeded, but profile query failed.")
                else:
                    p["status"] = "Handshake Failed"
                    p["expiry"] = "N/A"
                    p["connections"] = "-"
                    modified = True
                    outputs.append(f"Portal '{name}': Handshake failed.")
            
            if modified:
                try:
                    cfg = PluginConfig.objects.get(key="stalker_toolbox")
                    cfg.settings["portals_json"] = json.dumps(portals_list, indent=2)
                    cfg.save()
                except Exception as e:
                    logger.error(f"Failed to save connection test details: {e}")
            
            return {"status": "ok", "message": "\n".join(outputs)}

        elif action == "prune_offline_portals":
            if not portals_list:
                return {"status": "error", "message": "No portals configured."}
            
            initial_count = len(portals_list)
            pruned_list = [p for p in portals_list if p.get("status") not in ["Handshake Failed", "Handshake OK, Profile Failed"]]
            pruned_count = initial_count - len(pruned_list)
            
            if pruned_count > 0:
                try:
                    cfg = PluginConfig.objects.get(key="stalker_toolbox")
                    cfg.settings["portals_json"] = json.dumps(pruned_list, indent=2)
                    cfg.save()
                    return {"status": "ok", "message": f"Successfully pruned {pruned_count} offline/failed portals. {len(pruned_list)} portals remaining."}
                except Exception as e:
                    return {"status": "error", "message": f"Failed to save pruned portals: {e}"}
            else:
                return {"status": "ok", "message": "No offline/failed portals found to prune."}

        elif action == "sync_channels":
            if not portals_list:
                return {"status": "error", "message": "No portals configured."}
                
            active_portals = [p for p in portals_list if p.get("active", True)]
            if not active_portals:
                return {"status": "ok", "message": "No active portals selected for sync (set 'active': true)."}
                
            results = []
            proxy_port = settings.get("proxy_port", 8282)
            
            sync_live = settings.get("sync_live", True)
            sync_vod = settings.get("sync_vod", False)
            sync_series = settings.get("sync_series", False)
            sync_vod_limit = int(settings.get("sync_vod_limit", 100))
            sync_series_limit = int(settings.get("sync_series_limit", 50))
            
            proxies_list = get_proxies_list(settings, force_refresh=True)
            
            for idx, p in enumerate(active_portals):
                name = p.get("name")
                url = p.get("url")
                mac = p.get("mac")
                
                proxy = proxies_list[idx % len(proxies_list)] if proxies_list else None
                client = StalkerClient(url, mac, p.get("user_agent"), proxy=proxy)
                if not client.handshake():
                    results.append(f"Portal '{name}': Handshake failed.")
                    continue
                    
                selected_cats = p.get("selected_categories") or {}
                sel_live = selected_cats.get("live")
                sel_vod = selected_cats.get("vod")
                sel_series = selected_cats.get("series")
                
                mapping = {}
                m3u_lines = ["#EXTM3U\n"]
                total_items = 0
                
                # 1. Sync Live TV
                if sync_live:
                    logger.info(f"Syncing Live TV for portal '{name}'...")
                    channels = client.get_all_channels()
                    for ch in channels:
                        ch_id = ch.get("id")
                        ch_name = ch.get("name") or "Unknown Channel"
                        ch_cmd = ch.get("cmd")
                        
                        if not ch_id or not ch_cmd:
                            continue
                            
                        genre_id = ch.get("tv_genre_id")
                        if sel_live is not None and str(genre_id) not in [str(x) for x in sel_live]:
                            continue
                            
                        mapping[str(ch_id)] = {
                            "cmd": ch_cmd,
                            "is_vod": False
                        }
                        local_stream_url = f"http://127.0.0.1:{proxy_port}/play/{name}/{ch_id}"
                        
                        genre = ch.get("tv_genre_id") or "Live TV"
                        logo = ch.get("logo") or ""
                        
                        logo_attr = f' tvg-logo="{logo}"' if logo else ''
                        group_attr = f' group-title="{genre}"' if genre else ''
                        m3u_lines.append(f'#EXTINF:-1 tvg-id="stalker_{name}_{ch_id}"{logo_attr}{group_attr},{ch_name}\n')
                        m3u_lines.append(f"{local_stream_url}\n")
                        total_items += 1
                        
                # 2. Sync VOD (Movies)
                if sync_vod:
                    logger.info(f"Syncing VOD Movies for portal '{name}' (limit={sync_vod_limit})...")
                    vod_categories = client.get_vod_categories()
                    for cat in vod_categories:
                        cat_id = cat.get("id")
                        cat_name = cat.get("title") or "Movies"
                        if not cat_id:
                            continue
                            
                        if sel_vod is not None and str(cat_id) not in [str(x) for x in sel_vod]:
                            continue
                            
                        movies = client.get_ordered_list("vod", cat_id, limit=sync_vod_limit)
                        for movie in movies:
                            m_id = movie.get("id")
                            m_name = movie.get("name") or "Unknown Movie"
                            m_cmd = movie.get("cmd")
                            
                            if not m_id or not m_cmd:
                                continue
                                
                            unique_id = f"vod_{m_id}"
                            mapping[unique_id] = {
                                "cmd": m_cmd,
                                "is_vod": True
                            }
                            local_stream_url = f"http://127.0.0.1:{proxy_port}/play/{name}/{unique_id}"
                            
                            logo = movie.get("logo") or ""
                            logo_attr = f' tvg-logo="{logo}"' if logo else ''
                            group_attr = f' group-title="Movies - {cat_name}"'
                            m3u_lines.append(f'#EXTINF:-1 tvg-id="stalker_{name}_{unique_id}"{logo_attr}{group_attr},{m_name}\n')
                            m3u_lines.append(f"{local_stream_url}\n")
                            total_items += 1
                            
                # 3. Sync Series
                if sync_series:
                    logger.info(f"Syncing TV Series for portal '{name}' (limit={sync_series_limit})...")
                    series_categories = client.get_series_categories()
                    for cat in series_categories:
                        cat_id = cat.get("id")
                        cat_name = cat.get("title") or "Series"
                        if not cat_id:
                            continue
                            
                        if sel_series is not None and str(cat_id) not in [str(x) for x in sel_series]:
                            continue
                            
                        series_list = client.get_ordered_list("series", cat_id, limit=sync_series_limit)
                        for series in series_list:
                            s_id = series.get("id")
                            s_name = series.get("name") or "Unknown Series"
                            if not s_id:
                                continue
                                
                            episodes = client.get_series_episodes(s_id)
                            for ep in episodes:
                                ep_id = ep.get("id")
                                ep_name = ep.get("name") or f"Episode {ep.get('number', '?')}"
                                ep_cmd = ep.get("cmd")
                                
                                if not ep_id or not ep_cmd:
                                    continue
                                    
                                unique_id = f"series_{ep_id}"
                                mapping[unique_id] = {
                                    "cmd": ep_cmd,
                                    "is_vod": True
                                }
                                local_stream_url = f"http://127.0.0.1:{proxy_port}/play/{name}/{unique_id}"
                                
                                logo = ep.get("logo") or series.get("logo") or ""
                                logo_attr = f' tvg-logo="{logo}"' if logo else ''
                                group_attr = f' group-title="Series - {s_name}"'
                                m3u_lines.append(f'#EXTINF:-1 tvg-id="stalker_{name}_{unique_id}"{logo_attr}{group_attr},{s_name} - {ep_name}\n')
                                m3u_lines.append(f"{local_stream_url}\n")
                                total_items += 1
                                
                if total_items == 0:
                    results.append(f"Portal '{name}': No items fetched or selected for sync.")
                    continue
                    
                mapping_file = f"/data/stalker_channels_{name}.json"
                try:
                    with open(mapping_file, "w", encoding="utf-8") as f:
                        json.dump(mapping, f, indent=2)
                except Exception as e:
                    results.append(f"Portal '{name}': Failed to write map: {e}")
                    continue
                    
                m3u_file = f"/data/stalker_{name}.m3u"
                try:
                    with open(m3u_file, "w", encoding="utf-8") as f:
                        f.writelines(m3u_lines)
                except Exception as e:
                    results.append(f"Portal '{name}': Failed to write M3U file: {e}")
                    continue
                    
                try:
                    m3u_acc, created = M3UAccount.objects.get_or_create(
                        name=f"Stalker_{name}",
                        defaults={
                            "file_path": m3u_file,
                            "is_active": True,
                            "status": M3UAccount.Status.IDLE
                        }
                    )
                    if not created:
                        m3u_acc.file_path = m3u_file
                        m3u_acc.is_active = True
                        m3u_acc.save()
                        
                    refresh_single_m3u_account.delay(m3u_acc.id)
                    results.append(f"Portal '{name}': Sync queued! {total_items} items synced.")
                except Exception as e:
                    results.append(f"Portal '{name}': Failed to save: {e}")
                    
            return {"status": "ok", "message": "\n".join(results)}

        elif action == "run_generator":
            prefixes_str = settings.get("gen_prefixes", "00:1A:79:")
            total_count = int(settings.get("gen_count", 1000))
            mode = settings.get("gen_mode", "random")
            suffix_start = settings.get("gen_suffix_start", "").strip().upper().replace(":", "")
            suffix_end = settings.get("gen_suffix_end", "").strip().upper().replace(":", "")
            filename = settings.get("gen_filename", "combo.txt").strip()
            
            if not filename:
                filename = "combo.txt"
                
            prefixes = [p.strip().upper().replace("-", ":") for p in prefixes_str.split(",") if p.strip()]
            if not prefixes:
                return {"status": "error", "message": "No MAC prefixes specified."}
                
            # Parse suffix range values
            start_val = 0
            end_val = 16777215 # 0xFFFFFF
            if suffix_start:
                try:
                    start_val = int(suffix_start, 16)
                except Exception:
                    return {"status": "error", "message": f"Invalid start suffix hex: {suffix_start}"}
            if suffix_end:
                try:
                    end_val = int(suffix_end, 16)
                except Exception:
                    return {"status": "error", "message": f"Invalid finish suffix hex: {suffix_end}"}
                    
            if start_val > end_val:
                start_val, end_val = end_val, start_val
                
            total_range = end_val - start_val + 1
            
            os.makedirs("/data", exist_ok=True)
            filepath = f"/data/{filename}"
            
            macs_list = []
            num_prefixes = len(prefixes)
            base_count = total_count // num_prefixes
            remainder = total_count % num_prefixes
            
            if mode == "random":
                # Generate random unique suffixes per prefix
                for idx, prefix in enumerate(prefixes):
                    count_for_prefix = base_count + (1 if idx < remainder else 0)
                    actual_count = min(count_for_prefix, total_range)
                    if actual_count <= 0:
                        continue
                    used = set()
                    while len(used) < actual_count:
                        val = random.randint(start_val, end_val)
                        if val not in used:
                            used.add(val)
                            # format as XX:XX:XX
                            h = f"{val:06X}"
                            s = f"{h[0:2]}:{h[2:4]}:{h[4:6]}"
                            macs_list.append(prefix + s)
                # Shuffle the combined list
                random.shuffle(macs_list)
            else:
                # Sequential mode
                for idx, prefix in enumerate(prefixes):
                    count_for_prefix = base_count + (1 if idx < remainder else 0)
                    actual_count = min(count_for_prefix, total_range)
                    if actual_count <= 0:
                        continue
                    
                    if mode == "ascending":
                        step = max(1, total_range // actual_count)
                        suffix_vals = [start_val + i * step for i in range(actual_count)]
                    else:
                        # Descending
                        step = max(1, total_range // actual_count)
                        suffix_vals = [end_val - i * step for i in range(actual_count)]
                        
                    for val in suffix_vals:
                        h = f"{val:06X}"
                        s = f"{h[0:2]}:{h[2:4]}:{h[4:6]}"
                        macs_list.append(prefix + s)
                        
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    for mac in macs_list:
                        f.write(mac + "\n")
                return {"status": "ok", "message": f"Generated {len(macs_list)} MACs. Saved successfully to {filepath}."}
            except Exception as e:
                return {"status": "error", "message": f"Failed to save generated MACs: {e}"}

        elif action == "run_detective":
            url = settings.get("detective_url", "").strip()
            if not url:
                return {"status": "error", "message": "Detective Target URL is empty."}
                
            scan_subdomains = settings.get("detective_scan_subdomains", False)
            scan_ports = settings.get("detective_scan_ports", False)
            urlscan_key = settings.get("detective_urlscan_key", "").strip()
            
            proxies_list = get_proxies_list(settings, force_refresh=True)
            proxy = random.choice(proxies_list) if proxies_list else None
            
            # Start detective investigation in background thread to avoid HTTP timeout
            detective_thread = threading.Thread(
                target=self._run_portal_detective_task,
                args=(url, scan_subdomains, scan_ports, urlscan_key, proxy),
                daemon=True
            )
            detective_thread.start()
            
            return {
                "status": "ok",
                "message": f"Portal Detective investigation started in background for '{url}'!\nResults will be written to /data/stalker_detective_<domain>.txt"
            }

        elif action == "scan_macs":
            if _SCAN_STATUS["running"]:
                return {
                    "status": "ok",
                    "message": f"Scan already in progress. Progress: {_SCAN_STATUS['checked']}/{_SCAN_STATUS['total']} MACs."
                }
                
            scan_portal = settings.get("scan_portal")
            scan_mac_start = settings.get("scan_mac_start")
            scan_mac_end = settings.get("scan_mac_end")
            scan_threads = int(settings.get("scan_threads", 5))
            scan_cooldown = float(settings.get("scan_cooldown", 1))
            
            if not scan_portal or not scan_mac_start or not scan_mac_end:
                return {"status": "error", "message": "Scan parameters (Scan Portal, Start MAC, End MAC) must be filled."}
                
            portal_config = next((p for p in portals_list if p.get("name") == scan_portal), None)
            if not portal_config:
                return {"status": "error", "message": f"Selected scan portal '{scan_portal}' not found in portals list."}
                
            proxies_list = get_proxies_list(settings, force_refresh=True)
            
            scan_thread = threading.Thread(
                target=run_mac_scan_threaded,
                args=(portal_config, scan_mac_start, scan_mac_end, scan_cooldown, scan_threads, proxies_list),
                daemon=True
            )
            scan_thread.start()
            return {
                "status": "ok", 
                "message": f"MAC Address Scan (using {scan_threads} threads) started in background on portal '{scan_portal}'!"
            }

        elif action == "get_scan_status":
            return {
                "status": "ok",
                "running": _SCAN_STATUS["running"],
                "portal": _SCAN_STATUS["portal"],
                "current_mac": _SCAN_STATUS["current_mac"],
                "checked": _SCAN_STATUS["checked"],
                "total": _SCAN_STATUS["total"],
                "active_found": _SCAN_STATUS["active_found"],
                "results": _SCAN_STATUS["results"]
            }
            
        elif action == "fetch_portal_categories":
            portal_name = params.get("portal_name")
            if not portal_name:
                return {"status": "error", "message": "Portal name parameter is required."}
            portal_config = next((p for p in portals_list if p.get("name") == portal_name), None)
            if not portal_config:
                return {"status": "error", "message": f"Portal '{portal_name}' not found."}
                
            proxies_list = get_proxies_list(settings, force_refresh=False)
            idx = next((i for i, p in enumerate(portals_list) if p.get("name") == portal_name), 0)
            proxy = proxies_list[idx % len(proxies_list)] if proxies_list else None
            
            client = StalkerClient(
                url=portal_config.get("url"),
                mac=portal_config.get("mac"),
                user_agent=portal_config.get("user_agent"),
                proxy=proxy
            )
            if not client.handshake():
                return {"status": "error", "message": "Failed to connect to portal (handshake failed)."}
                
            live_genres = client.get_genres()
            vod_categories = client.get_vod_categories()
            series_categories = client.get_series_categories()
            
            return {
                "status": "ok",
                "live": [{"id": str(g.get("id")), "title": g.get("title") or g.get("name")} for g in live_genres if g.get("id")],
                "vod": [{"id": str(c.get("id")), "title": c.get("title") or c.get("name")} for c in vod_categories if c.get("id")],
                "series": [{"id": str(c.get("id")), "title": c.get("title") or c.get("name")} for c in series_categories if c.get("id")]
            }
            
        return {"status": "error", "message": f"Unknown action: {action}"}

    def _run_portal_detective_task(self, target_url, scan_subdomains, scan_ports_flag, urlscan_key, proxy=None):
        logger.info(f"Portal Detective starting investigation on: {target_url}")
        
        url = target_url if target_url.startswith(("http://", "https://")) else "http://" + target_url
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            logger.error("Portal Detective: Invalid URL hostname.")
            return
            
        report_data = {
            "Portal": url,
            "IP Address": "Unknown",
            "Reverse DNS": "Not available",
            "SSL Valid": "No",
            "Response Time (ms)": "N/A",
            "Status Code": "N/A",
            "Server": "Unknown",
            "X-Powered-By": "Unknown",
            "Cloudflare Protection": "No",
            "Open Ports": {},
            "Subdomains Found": [],
            "Accepted STB Models": [],
            "Admin Probes": [],
            "Co-Hosted Portals": []
        }
        
        proxies_dict = {"http": proxy, "https": proxy} if proxy else None
        
        # 1. Geolocation & IP Lookup
        try:
            ip = socket.gethostbyname(hostname)
            report_data["IP Address"] = ip
            
            # DNS lookup
            report_data["Reverse DNS"] = reverse_dns_lookup(ip)
                
            # Geolocation info
            geo_resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5, proxies=proxies_dict)
            if geo_resp.status_code == 200:
                geo_data = geo_resp.json()
                report_data["Country"] = f"{geo_data.get('countryCode', 'Unknown')} ({geo_data.get('country', 'Unknown')})"
                report_data["City"] = geo_data.get("city", "Unknown")
                report_data["Region"] = geo_data.get("regionName", "Unknown")
                report_data["Org"] = geo_data.get("org", "Unknown")
                report_data["ASN"] = geo_data.get("as", "Unknown")
        except Exception as e:
            logger.error(f"Detective IP lookup error: {e}")
            ip = None
            
        # 2. SSL Check
        if url.startswith("https://"):
            try:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                    s.settimeout(3)
                    s.connect((hostname, parsed.port or 443))
                report_data["SSL Valid"] = "Yes"
            except Exception:
                report_data["SSL Valid"] = "No"
                
        # 3. Connection and Header Test
        try:
            start_time = time.time()
            resp = requests.get(url, timeout=8, verify=False, allow_redirects=True, proxies=proxies_dict)
            report_data["Response Time (ms)"] = int((time.time() - start_time) * 1000)
            report_data["Status Code"] = resp.status_code
            report_data["Server"] = resp.headers.get("Server", "Unknown")
            report_data["X-Powered-By"] = resp.headers.get("X-Powered-By", "Unknown")
        except Exception:
            pass
            
        # 4. Detect protections (Cloudflare, DDoS-Guard, etc.)
        protections = detect_protection(url, proxy)
        report_data["Cloudflare Protection"] = ", ".join(protections)
            
        # 5. Enumerate Subdomains
        if scan_subdomains and hostname:
            domain_parts = hostname.split(".")
            if len(domain_parts) >= 2:
                base_domain = ".".join(domain_parts[-2:])
                logger.info(f"Detective enumerating subdomains on: {base_domain}")
                for sub in COMMON_SUBDOMAINS:
                    sub_host = f"{sub}.{base_domain}"
                    try:
                        sub_ip = socket.gethostbyname(sub_host)
                        report_data["Subdomains Found"].append(f"{sub_host} -> {sub_ip}")
                    except Exception:
                        pass
                        
        # 6. Port Banner Scanner
        if scan_ports_flag and hostname:
            logger.info("Detective port scanning server and fetching banners...")
            for port in COMMON_PORTS:
                res_port = scan_port_banner(hostname, port, proxy)
                if res_port:
                    report_data["Open Ports"][port] = res_port
                    
        # 7. Admin Panel Discovery
        logger.info("Detective probing admin endpoints...")
        for payload in ADMIN_PAYLOADS:
            try:
                target = url.rstrip("/") + payload
                headers = {"User-Agent": random.choice(ADMIN_USER_AGENTS)}
                resp = requests.get(target, headers=headers, timeout=5, verify=False, allow_redirects=True, proxies=proxies_dict)
                if resp.status_code in [200, 403, 444]:
                    report_data["Admin Probes"].append(f"[FOUND] {resp.status_code} on {target}")
            except Exception as e:
                if "104" in str(e) or "Connection reset" in str(e):
                    report_data["Admin Probes"].append(f"[RESET/POSSIBLE] on {target}")
                    
        # 8. STB Fingerprinting Login Tests
        logger.info("Detective testing STB model fingerprint logins...")
        test_mac = "00:1A:79:AB:CD:EF"
        for stb in STB_MODELS_LIST:
            res_finger = test_stb_login_fingerprint(url, test_mac, stb, proxy)
            report_data["Accepted STB Models"].append(f"{stb} -> {res_finger}")
                
        # 9. urlscan.io co-hosted portals
        if urlscan_key and ip and ip != "Unknown":
            logger.info("Detective querying urlscan.io for similar server co-hostings...")
            report_data["Co-Hosted Portals"] = urlscan_analyze_portal(url, urlscan_key, ip)

        # Write Report File
        safe_domain = re.sub(r'[^a-zA-Z0-9]', '_', hostname)
        report_file = f"/data/stalker_detective_{safe_domain}.txt"
        
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                f.write("========================================================\n")
                f.write("              🕵️ PORTAL DETECTIVE REPORT 🕵️             \n")
                f.write("========================================================\n\n")
                f.write(f"Target Portal:        {report_data['Portal']}\n")
                f.write(f"Status Code:          {report_data['Status Code']}\n")
                f.write(f"Response Time (ms):   {report_data['Response Time (ms)']}\n")
                f.write(f"SSL Valid:            {report_data['SSL Valid']}\n")
                f.write(f"Server Banner:        {report_data['Server']}\n")
                f.write(f"X-Powered-By:         {report_data['X-Powered-By']}\n")
                f.write(f"WAF/Protections:      {report_data['Cloudflare Protection']}\n\n")
                
                f.write("🌐 IP GEOLOCATION:\n")
                f.write(f"   IP Address:        {report_data.get('IP Address')}\n")
                f.write(f"   Reverse DNS:       {report_data.get('Reverse DNS')}\n")
                f.write(f"   ASN:               {report_data.get('ASN', 'N/A')}\n")
                f.write(f"   Country:           {report_data.get('Country', 'Unknown')}\n")
                f.write(f"   City/Region:       {report_data.get('City', 'Unknown')} / {report_data.get('Region', 'Unknown')}\n")
                f.write(f"   ISP/Org:           {report_data.get('Org', 'Unknown')}\n\n")
                
                f.write("🚪 OPEN PORTS:\n")
                if report_data["Open Ports"]:
                    for port in sorted(report_data["Open Ports"].keys()):
                        f.write(f"   Port {port}: {report_data['Open Ports'][port]}\n")
                else:
                    f.write("   None found / Port scan disabled or closed\n\n")
                    
                f.write("🌐 SUBDOMAINS FOUND:\n")
                if report_data["Subdomains Found"]:
                    for sub in report_data["Subdomains Found"]:
                        f.write(f"   {sub}\n")
                else:
                    f.write("   None found / Subdomains scan disabled\n\n")
                    
                f.write("🔐 ADMIN PORTAL DISCOVERY:\n")
                if report_data["Admin Probes"]:
                    for probe in report_data["Admin Probes"]:
                        f.write(f"   {probe}\n")
                else:
                    f.write("   No admin panels detected.\n\n")
                    
                f.write("🔬 STB MODEL FINGERPRINT TESTING:\n")
                if report_data["Accepted STB Models"]:
                    for res_finger in report_data["Accepted STB Models"]:
                        f.write(f"   {res_finger}\n")
                else:
                    f.write("   No STB models tested.\n\n")
                    
                f.write("🌐 CO-HOSTED PORTALS / ASSOCIATED PANELS (via urlscan.io):\n")
                if urlscan_key:
                    if report_data["Co-Hosted Portals"]:
                        for p in report_data["Co-Hosted Portals"]:
                            f.write(f"   {p}\n")
                    else:
                        f.write("   No co-hosted portals discovered on this IP address.\n\n")
                else:
                    f.write("   urlscan.io search skipped (API Key not provided in settings).\n\n")

                f.write("========================================================\n")
                f.write("Report completed successfully.\n")
                
            logger.info(f"Portal Detective investigation completed! Saved report to {report_file}")
        except Exception as e:
            logger.error(f"Failed to write detective report: {e}")
            
        # 10. Persist Results to SQLite database (Django PluginConfig settings)
        try:
            cfg = PluginConfig.objects.get(key="stalker_toolbox")
            history = cfg.settings.get("detective_history", {})
            history[url] = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": report_data["IP Address"],
                "reverse_dns": report_data["Reverse DNS"],
                "status_code": report_data["Status Code"],
                "ssl_valid": report_data["SSL Valid"],
                "server_banner": report_data["Server"],
                "protections": report_data["Cloudflare Protection"],
                "open_ports": report_data["Open Ports"],
                "subdomains": report_data["Subdomains Found"],
                "admin_probes": report_data["Admin Probes"],
                "stb_fingerprints": report_data["Accepted STB Models"],
                "co_hosted_portals": report_data["Co-Hosted Portals"]
            }
            # Limit history to 50 entries
            if len(history) > 50:
                oldest_key = min(history.keys(), key=lambda k: history[k].get("timestamp", ""))
                del history[oldest_key]
                
            cfg.settings["detective_history"] = history
            cfg.save()
            logger.info("Saved Portal Detective results to Dispatcharr SQLite Database.")
        except Exception as db_err:
            logger.error(f"Failed to save detective report to Django SQLite database: {db_err}")

    def stop(self, context: dict):
        global _PROXY_SERVER, _SCAN_STATUS
        if _SCAN_STATUS["running"]:
            _SCAN_STATUS["running"] = False
            logger.info("Stopping Stalker Portal Toolbox scan thread...")
            
        if _PROXY_SERVER:
            _PROXY_SERVER.stop()
            _PROXY_SERVER = None
