import requests
import logging
import traceback
import json
import uuid
import time
from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse, urlencode

logger = logging.getLogger(__name__)

STB_USER_AGENT = "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2116 Mobile Safari/533.3"

class Client:
    """Stalker/Ministra Portal API Client"""

    def __init__(self, server_url, mac_address, sn="0000000000000", device_id=None, device_id2=None, model="MAG254", timezone="UTC", username="", password=""):
        self.server_url = self._normalize_url(server_url)
        self.mac_address = mac_address.upper() if mac_address else ""
        self.sn = sn
        
        # Default device IDs to 64 'f's if not provided
        default_dev_id = "f" * 64
        self.device_id = device_id if device_id else default_dev_id
        self.device_id2 = device_id2 if device_id2 else default_dev_id
        
        self.model = model
        self.timezone = timezone
        self.username = username
        self.password = password

        self.token = ""
        self.session = requests.Session()
        self.endpoint = self._get_portal_endpoint()
        
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=15,
            max_retries=3,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def _normalize_url(self, url):
        """Strip trailing slashes"""
        if not url:
            raise ValueError("Server URL cannot be empty")
        return url.strip().rstrip('/')

    def _get_portal_endpoint(self):
        """Determine if it's portal.php or load.php based on URL structure"""
        if '/stalker_portal/' in self.server_url or self.server_url.endswith('/stalker_portal'):
            idx = self.server_url.find('/stalker_portal')
            base = self.server_url[:idx] if idx > 0 else self.server_url
            return f"{base}/stalker_portal/server/load.php"
            
        if '/portal.php' in self.server_url:
            return self.server_url
            
        if self.server_url.endswith('/c'):
            return f"{self.server_url}/portal.php"
            
        return f"{self.server_url}/portal.php"

    def _get_cookie(self):
        return f"mac={self.mac_address}; stb_lang=en; timezone={self.timezone};"

    def _get_headers(self, is_handshake=False):
        headers = {
            'User-Agent': STB_USER_AGENT,
            'X-User-Agent': f"Model: {self.model}; Link: Ethernet",
            'Accept': '*/*',
            'Accept-Language': 'en',
            'Cookie': self._get_cookie()
        }
        if not is_handshake and self.token:
            headers['Authorization'] = f"Bearer {self.token}"
        return headers

    def _make_request(self, req_type, action, params=None, is_handshake=False):
        """Make an API request to the stalker portal"""
        url = self.endpoint
        
        query = {
            'type': req_type,
            'action': action,
            'JsHttpRequest': '1-xml'
        }
        if params:
            query.update(params)
            
        full_url = f"{url}?{urlencode(query)}"
        headers = self._get_headers(is_handshake=is_handshake)
        
        logger.debug(f"Stalker API Request: {full_url}")

        try:
            response = self.session.get(full_url, headers=headers, timeout=30)
            response.raise_for_status()

            if not response.content:
                raise ValueError("Empty response from Stalker portal")

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                raise ValueError(f"Invalid JSON from Stalker portal: {response.text[:200]}")

            return data.get('js', data)
            
        except requests.RequestException as e:
            logger.error(f"Stalker API Request failed: {e}")
            raise
        except ValueError as e:
            logger.error(f"Stalker API Invalid response: {e}")
            raise

    def authenticate(self):
        """Perform handshake and authenticate"""
        # Handshake
        logger.debug(f"Stalker Handshake for MAC {self.mac_address}")
        hs_params = {
            'token': '',
            'prehash': '0'
        }
        hs_data = self._make_request('stb', 'handshake', params=hs_params, is_handshake=True)
        if isinstance(hs_data, dict) and hs_data.get('token'):
            self.token = hs_data['token']
            logger.debug(f"Stalker Token obtained: {self.token}")

        # Authenticate
        if self.username and self.password:
            logger.debug("Stalker Auth with Credentials")
            auth_params = {
                'login': self.username,
                'password': self.password,
                'device_id': self.device_id,
                'device_id2': self.device_id2
            }
            res = self._make_request('stb', 'do_auth', params=auth_params)
            if not res:
                raise ValueError("Authentication failed: invalid credentials")
        else:
            logger.debug("Stalker Auth with Device IDs")
            auth_params = {
                'hd': '1',
                'sn': self.sn,
                'stb_type': self.model,
                'device_id': self.device_id,
                'device_id2': self.device_id2,
                'auth_second_step': '1'
            }
            res = self._make_request('stb', 'get_profile', params=auth_params)
            if not res or (isinstance(res, dict) and not res.get('id')):
                raise ValueError("Authentication failed: device ID auth rejected")
        
        logger.info(f"Stalker Authentication successful for MAC {self.mac_address}")
        return True

    def handshake(self):
        """Perform handshake and return the token"""
        logger.debug(f"Stalker Handshake for MAC {self.mac_address}")
        hs_params = {
            'token': '',
            'prehash': '0'
        }
        hs_data = self._make_request('stb', 'handshake', params=hs_params, is_handshake=True)
        if isinstance(hs_data, dict) and hs_data.get('token'):
            self.token = hs_data['token']
            logger.debug(f"Stalker Token obtained: {self.token}")
            return self.token
        elif isinstance(hs_data, str):
            self.token = hs_data
            logger.debug(f"Stalker Token obtained: {self.token}")
            return self.token
        return None

    def get_profile(self):
        """Fetch user profile using current authentication state"""
        params = {
            'hd': '1',
            'sn': self.sn,
            'stb_type': self.model,
            'device_id': self.device_id,
            'device_id2': self.device_id2,
            'auth_second_step': '1'
        }
        return self._make_request('stb', 'get_profile', params=params)

    def get_live_categories(self):
        """Fetch TV Genres"""
        res = self._make_request('itv', 'get_genres')
        if isinstance(res, list):
            return res
        return []

    def get_live_streams(self):
        """Fetch TV Channels"""
        res = self._make_request('itv', 'get_all_channels')
        if isinstance(res, dict) and 'data' in res:
            return res['data']
        if isinstance(res, list):
            return res
        return []

    def get_vod_categories(self):
        """Fetch Movie Categories (excluding series)"""
        res = self._make_request('vod', 'get_categories')
        
        categories = []
        raw_cats = []
        if isinstance(res, dict) and 'data' in res:
            raw_cats = res['data']
        elif isinstance(res, list):
            raw_cats = res
            
        for c in raw_cats:
            title = str(c.get('title') or c.get('alias') or '').lower()
            # Filter out series-like categories
            if any(kw in title for kw in ['series', 'tv show', 'tv shows', 'season']):
                continue
            if title.startswith('tv ') or title.endswith(' tv'):
                continue
            
            # Map to XC-style fields for seamless integration
            c['category_id'] = c.get('id')
            c['category_name'] = c.get('title') or c.get('alias') or 'Unknown'
            
            categories.append(c)
            
        return categories

    def get_series_categories(self):
        """Fetch Series Categories"""
        try:
            res = self._make_request('series', 'get_categories')
            if res and (isinstance(res, list) or (isinstance(res, dict) and 'data' in res)):
                raw_cats = res.get('data') if isinstance(res, dict) else res
                if len(raw_cats) > 0:
                    for c in raw_cats:
                        c['category_id'] = c.get('id')
                        c['category_name'] = c.get('title') or c.get('alias') or 'Unknown'
                    return raw_cats
        except Exception:
            pass
            
        # Fallback: fetch vod categories and filter for series
        res = self._make_request('vod', 'get_categories')
        categories = []
        raw_cats = []
        if isinstance(res, dict) and 'data' in res:
            raw_cats = res['data']
        elif isinstance(res, list):
            raw_cats = res
            
        for c in raw_cats:
            title = str(c.get('title') or c.get('alias') or '').lower()
            if any(kw in title for kw in ['series', 'tv show', 'tv shows', 'season']) or title.startswith('tv ') or title.endswith(' tv'):
                c['category_id'] = c.get('id')
                c['category_name'] = c.get('title') or c.get('alias') or 'Unknown'
                categories.append(c)
                
        return categories

    def _get_ordered_list_all_pages(self, req_type, params):
        """Helper to fetch paginated lists"""
        all_items = []
        params['p'] = 1
        
        while True:
            res = self._make_request(req_type, 'get_ordered_list', params=params)
            
            data = []
            if isinstance(res, dict) and 'data' in res:
                data = res['data']
            elif isinstance(res, list):
                data = res
                
            if not data:
                break
                
            for item in data:
                item['stream_id'] = item.get('id') or item.get('cmd')
                item['series_id'] = item.get('id') # for series
                if 'name' not in item:
                    item['name'] = item.get('title') or item.get('alias') or 'Unknown'
                
            all_items.extend(data)
            
            if len(data) < 14:
                break
                
            params['p'] += 1
            
        return all_items

    def get_vod_streams(self, category_id=None):
        """Fetch VOD items"""
        params = {}
        if category_id:
            params['category'] = category_id
        return self._get_ordered_list_all_pages('vod', params)

    def get_series(self, category_id=None):
        """Fetch Series items"""
        params = {}
        if category_id:
            params['category'] = category_id
        
        try:
            series = self._get_ordered_list_all_pages('series', params)
            if series:
                return series
        except Exception:
            pass
            
        return self._get_ordered_list_all_pages('vod', params)

    def get_seasons_and_episodes(self, series_id):
        """Fetch seasons and episodes for a series"""
        params = {
            'movie_id': series_id
        }
        try:
            return self._get_ordered_list_all_pages('series', params)
        except Exception:
            return self._get_ordered_list_all_pages('vod', params)

    def create_link(self, cmd, is_vod=False):
        """Create a playback link"""
        req_type = 'vod' if is_vod else 'itv'
        params = {'cmd': cmd}
        res = self._make_request(req_type, 'create_link', params=params)
        
        if isinstance(res, dict):
            if 'cmd' in res:
                return res['cmd']
            if 'url' in res:
                return res['url']
        elif isinstance(res, str):
            return res
            
        raise ValueError(f"Could not parse create_link response: {res}")


def detect_expiry(data, depth=0):
    """
    Recursively inspects dict keys to find an expiration date.
    Returns the raw string, integer, or float expiration value if found, or None.
    """
    if not isinstance(data, dict) or depth > 4:
        return None

    primary_keys = [
        "expire_date",
        "end_date",
        "max_view_date",
        "expire_billing_date",
        "tariff_expired_date",
        "date_end",
        "exp_date",
        "expDate",
        "expired",
        "expires",
        "expiry_date",
        "access_end",
        "end_date_time",
        "valid_until",
        "end",
        "to",
        "active_until",
    ]

    unlimited_values = [
        "unlimited",
        "lifetime",
        "never",
        "infinity",
        "infinite",
        "permanent",
        "forever",
        "no expiry",
        "no limit",
        "no expiration",
    ]

    # 1. Check primary keys
    for key in primary_keys:
        val = data.get(key)
        if val is not None:
            val_str = str(val).strip().lower()
            if val_str in unlimited_values:
                return "Unlimited"
            if val_str not in [
                "",
                "0",
                "0000-00-00",
                "0000-00-00 00:00:00",
                "null",
                "none",
                "false",
            ]:
                return str(val)

    # 2. Aggressive search: Check ANY key that contains date/expire/end keywords
    for k, v in data.items():
        if v is None:
            continue
        k_low = str(k).lower()
        v_str = str(v).strip()
        if not v_str:
            continue

        if any(
            x in k_low
            for x in ["expire", "end_date", "valid_until", "exp_date", "access_end"]
        ):
            if v_str.lower() not in [
                "0",
                "0000-00-00",
                "0000-00-00 00:00:00",
                "null",
                "none",
                "false",
            ]:
                if "-" in v_str or (v_str.isdigit() and len(v_str) >= 10):
                    return v_str

    # 3. Check common sub-objects (recursive)
    for sub in [
        "account_info",
        "stb_account",
        "active_sub",
        "billing",
        "profile",
        "payment",
        "tariff",
        "subscription",
        "services",
    ]:
        sub_data = data.get(sub)
        if isinstance(sub_data, dict):
            res = detect_expiry(sub_data, depth + 1)
            if res:
                return res
        elif isinstance(sub_data, list) and len(sub_data) > 0:
            for item in sub_data:
                if isinstance(item, dict):
                    res = detect_expiry(item, depth + 1)
                    if res:
                        return res

    return None


def clean_expiry_value(val):
    """
    Parses a raw expiration value string/timestamp into ISO-8601 string or numeric timestamp.
    """
    if val is None:
        return None
    val_str = str(val).strip()
    
    if val_str.isdigit() and len(val_str) >= 10:
        try:
            return float(val_str)
        except ValueError:
            pass

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d-%m-%Y %H:%M:%S", "%d-%m-%Y"):
        try:
            dt = datetime.strptime(val_str, fmt)
            dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except ValueError:
            continue

    if "-" in val_str:
        return val_str.replace(" ", "T")

    return val_str


# Export alias to fix ImportError in tasks
StalkerClient = Client
