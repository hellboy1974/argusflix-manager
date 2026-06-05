# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ANGINA_Portal_Detective_Final_PyQt7.py
# Bytecode version: 3.8.0rc1+ (3413)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import time
import socket
import random
import json
import csv
import logging
import argparse
import threading
import re
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import pycountry
import ssl
import urllib3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QProgressBar, QComboBox, QLineEdit, QSpinBox, QCheckBox, QGroupBox, QTabWidget, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QListWidget, QListWidgetItem, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QTextCursor, QColor, QPalette
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Errno111Filter(logging.Filter):
    def filter(self, record):
        return 'Errno 111' not in record.getMessage() and 'Connection refused' not in record.getMessage()
logging.getLogger().addFilter(Errno111Filter())

def get_app_directory():
    """Get the directory where the application is running from"""  # inserted
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def create_folders():
    app_dir = get_app_directory()
    script_name = 'Portal_Detective_Pro'
    main_folder = os.path.join(app_dir, f'{script_name}_Data')
    if not os.path.exists(main_folder):
        try:
            os.makedirs(main_folder)
            print(f'Created main folder: {main_folder}')
        except Exception as e:
            print(f'Error creating main folder: {e}')
            main_folder = app_dir
    input_folder = os.path.join(main_folder, 'URL_Lists')
    output_folder = os.path.join(main_folder, 'Analysis_Results')
    history_folder = os.path.join(main_folder, 'Analysis_History')
    for folder in [input_folder, output_folder, history_folder]:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print(f'Created folder: {folder}')
            except Exception as e:
                print(f'Error creating folder {folder}: {e}')
    sample_file = os.path.join(input_folder, 'portals.txt')
    if not os.path.exists(sample_file):
        try:
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write('# Sample IPTV portals file\n')
                f.write('# Add your portal URLs here, one per line or separated by commas\n')
                f.write('# Examples:\n')
                f.write('http://example.com:8080\n')
                f.write('https://iptv-provider.com:8000\n')
                f.write('http://live-tv.com:1234\n')
                f.write('http://192.168.1.100:8080\n')
                f.write('https://portal.iptvservice.com:8000\n')
            print(f'Created sample portals file: {sample_file}')
        except Exception as e:
            print(f'Error creating sample file: {e}')
    return (input_folder, output_folder, history_folder, main_folder)
INPUT_FOLDER, OUTPUT_FOLDER, HISTORY_FOLDER, MAIN_FOLDER = create_folders()

def load_config():
    app_dir = get_app_directory()
    config_path = os.path.join(app_dir, 'config_portal_detective.json')
    default_config = {'max_workers': 15, 'timeout': 10, 'retries': 2, 'check_interval': 300, 'output_formats': ['txt'], 'enable_history': True, 'quick_mode': False}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return {**default_config, **json.load(f)}
        except:
            return default_config
    try:
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
    except:
        pass
    return default_config
CONFIG = load_config()

def get_country_info(country_code):
    """Get country name and flag emoji without external libraries"""  # inserted
    country_code = country_code.strip().upper()
    Croatia = {'US': 'United States', 'United Kingdom': 'United Kingdom', 'CA': 'Canada', 'AU': 'Australia', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy', 'ES': 'Spain', 'NL': 'Netherlands', 'BE': 'Belgium', 'CH': 'Switzerland', 'AT': 'Austria', 'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark', 'FI': 'Finland', 'IE': 'Ireland', 'PT': 'Portugal', 'PL': 'Poland', 'CZ': 'Czech Republic', 'HU': 'Hungary', 'GR': 'Greece', 'RO': 'Romania', 'BG': 'Bulgaria', 'HR': 'Croatia', 'RS': '
    🇭🇷 = {'US': '🇺🇸', '🇬🇧': '🇬🇧', 'CA': '🇨🇦', 'AU': '🇦🇺', 'DE': '🇩🇪', 'FR': '🇫🇷', 'IT': '🇮🇹', 'ES': '🇪🇸', 'NL': '🇳🇱', 'BE': '🇧🇪', 'CH': '🇨🇭', 'AT': '🇦🇹', 'SE': '🇸🇪', 'NO': '🇳🇴', 'DK': '🇩🇰', 'FI': '🇫🇮', 'IE': '🇮🇪', 'PT': '🇵🇹', 'PL': '🇵🇱', 'CZ': '🇨🇿', 'HU': '🇭🇺', 'GR': '🇬🇷', 'RO': '🇷🇴', 'BG': '🇧🇬', 'HR': '🇭🇷', 'RS': '
    country_name = country_names.get(country_code, 'Unknown')
    flag_emoji = flag_emojis.get(country_code, '🌍')
    return (country_name, flag_emoji)
URLSCAN_API_KEY = '01990b54-2cad-730c-8107-fa36271e7a4c'
URLSCAN_HEADERS = {'API-Key': URLSCAN_API_KEY, 'Content-Type': 'application/json'}
URLSCAN_SCAN_ENDPOINT = 'https://urlscan.io/api/v1/scan/'
URLSCAN_RESULT_ENDPOINT = 'https://urlscan.io/api/v1/result/'
URLSCAN_SEARCH_ENDPOINT = 'https://urlscan.io/api/v1/search/'

def urlscan_normalize_url(url):
    """Normalize URL for urlscan.io - add /c/ if not present"""  # inserted
    url = url.strip()
    if not url.startswith('http://') and (not url.startswith('https://')):
        url = 'http://' + url
    if '/c/' not in url:
        if not url.endswith('/'):
            url += '/'
        url += 'c/'
    return url

def normalize_url_for_scans(url):
    """Normalize URL for all scans except admin payloads - FIXED to handle ports properly"""  # inserted
    url = url.strip()
    parsed = urlparse(url)
    if '/c/' not in url and (not parsed.path) and (not url.endswith('/c/')):
        if parsed.port and parsed.port not in [80, 443]:
            return url.rstrip('/') + '/'
        return url.rstrip('/') + '/c/'
    return url.rstrip('/') + '/'

def urlscan_scan_url(url):
    """Submit URL to urlscan.io for scanning"""  # inserted
    try:
        resp = requests.post(URLSCAN_SCAN_ENDPOINT, json={'url': url, 'visibility': 'public'}, headers=URLSCAN_HEADERS, timeout=30, verify=False)
        if resp.status_code not in [200, 201]:
            logging.error(f'URLScan submission failed ({resp.status_code}) → {resp.text}')
            return
        return resp.json().get('uuid')
    except requests.exceptions.RequestException as e:
        logging.error(f'URLScan request error: {e}')
        return None

def urlscan_get_scan_result(uuid):
    """Get scan results from urlscan.io"""  # inserted
    url = URLSCAN_RESULT_ENDPOINT + uuid + '/'
    try:
        for _ in range(30):
            resp = requests.get(url, headers=URLSCAN_HEADERS, timeout=10, verify=False)
            if resp.status_code == 200:
                return resp.json()
            time.sleep(2)
    except requests.exceptions.RequestException:
        pass
    return None

def urlscan_search_by_ip(ip):
    """Search for similar portals by IP using urlscan.io"""  # inserted
    try:
        params = {'q': f'page.ip:{ip}', 'size': 50}
        resp = requests.get(URLSCAN_SEARCH_ENDPOINT, headers=URLSCAN_HEADERS, params=params, timeout=10, verify=False)
        if resp.status_code!= 200:
            logging.error(f'URLScan search failed ({resp.status_code}) → {resp.text}')
            return []
        return [item.get('page', {}).get('url') for item in resp.json().get('results', []) if item.get('page')]
    except requests.exceptions.RequestException:
        return []

def urlscan_analyze_portal(url, proxy=None):
    """Main function to analyze portal using urlscan.io and find similar portals"""  # inserted
    normalized_url = normalize_url_for_scans(url)
    try:
        parsed = urlparse(normalized_url)
        hostname = parsed.hostname
        ip = socket.gethostbyname(hostname)
    except Exception as e:
        return []
    uuid = urlscan_scan_url(normalized_url)
    if not uuid:
        return []
    result = urlscan_get_scan_result(uuid)
    if not result:
        return []
    similar_portals = urlscan_search_by_ip(ip)
    unique_portals = []
    seen_urls = set()
    for portal in similar_portals:
        if portal:
            normalized = portal.lower().replace('https://', '').replace('http://', '').replace('www.', '')
            if normalized not in seen_urls:
                seen_urls.add(normalized)
                unique_portals.append(portal)
    return unique_portals
COMMON_PORTS = [80, 443, 8080, 8880, 25461, 2052, 2082, 2086, 2095, 8443, 8844, 8888, 9000, 9600]
MAC_PREFIXES = ['00:01:5F', '00:02:F2', '00:03:93', '00:03:FF', '00:04:4F', '00:05:69', '00:05:9A', '00:07:AB', '00:09:18', '00:09:C7', '00:09:DF', '00:0A:27', '00:0C:29', '00:0E:50', '00:0E:8F', '00:0F:4B', '00:11:D8', '00:13:E8', '00:14:22', '00:15:AD', '00:16:3E', '00:18:82', '00:18:BD', '00:19:66', '00:19:E0', '00:1A:70', '00:1A:78', '00:1A:79', '00:1A:E9', '00:1B:79', '00:1B:EA', '00:1C:14', '00:1C:19', '00:1C:42', '00:1C:79', '00:1D:20', '00:1D:79', '00:1D:D5', '00:1E:79', '00:1E:8A', '00:1E:B8', '00:1F:16', '00:1F:33', '00:1F:3A', '00:1F:79', '00:20:91', '00:21:5C', '00:22:93', '00:23:45', '00:24:D4', '00:25:90', '00:26:75', '00:2A:01', '00:2A:79', '00:30:18', '00:40:96', '00:50:56', '00:60:2F', '00:90:0B', '00:A0:C9', '00:A1:79', '00:D0:D0', '00:E0:4C', '04:D6:AA', '08:00:27', '08:05:81', '08:9E:08', '0C:47:C9', '10:27:BE', '11:33:01', '18:C8:E7', '1A:00:6A', '1A:00:FB', '30:87:30', '33:44:CF', '55:93:EA', '68:FF:7B', '74:1A:79', 'A0:BB:3E', 'BC:2F:D0', 'D4:CF:F9', 'E0:37:17']
USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3']
COMMON_SUBDOMAINS = ['www', 'api', 'portal', 'stream', 'tv', 'iptv', 'live', 'm', 'mobile', 'secure', 'admin', 'login', 'panel', 'cdn', 'video', 'play']
ADMIN_PAYLOADS = ['/c/', '/portal.php', '/server/load.php', '/portalstb/', '/stalker_portal/server/load.php', '/portal.php/c/', '/stalker_portal', '/admin/', '/panel/', '/login/', '/manager/', '/web/', '/xc/', '/xtream/']
ADMIN_USER_AGENTS = ['Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/537.36', 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/537.36', 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/537.36', 'Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +https://www.cloudflare.com/always-online) AppleWebKit/534.34', 'Mozilla/5.0 (X11; Linux i686; U;rv: 1.7.13) Gecko/20070322 Kazehakase/0.4.4.1', 'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586; en-US; m18) Gecko/20010131 Netscape6/6.01', 'Mozilla/5.0 (X11; U; Linux i686; de-AT; rv:1.8.0.2) Gecko/20060309 SeaMonkey/1.0']

def format_status_code(status_code, error_message=''):
    """Format status codes with colors and custom handling"""  # inserted
    if status_code == 200:
        return ('[ 200 ]', 200, 'green')
    if status_code in [444, 403] or '104' in str(error_message):
        return ('[ 200 ]', 200, 'green')
    if status_code == 'Error':
        if '104' in error_message or 'Connection reset by peer' in error_message:
            return ('[ 200 ]', 200, 'green')
        return ('[ Error ]', 'Error', 'red')
    if status_code == 401:
        return ('[ 401 ]', 401, 'magenta')
    if status_code == 404:
        return ('[ 404 ]', 404, 'yellow')
    if status_code == 500:
        return ('[ 500 ]', 500, 'red')
    if status_code == 302:
        return ('[ 302 ]', 302, 'blue')
    return (f'[ {status_code} ]', status_code, 'white')

def get_admin_panel_status(status_code, error_message=''):
    """Convert status code to colored status message with enhanced formatting"""  # inserted
    status_display, display_code, color = format_status_code(status_code, error_message)
    return status_display

def discover_admin_panels(url, proxy=None):
    """Discover admin panels and portal endpoints using original URL (not normalized)"""  # inserted
    results = []
    best_results = []
    original_url = url
    for payload in ADMIN_PAYLOADS:
        try:
            target_url = original_url.rstrip('/') + payload
            headers = {'User-Agent': random.choice(ADMIN_USER_AGENTS)}
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            response = requests.get(target_url, headers=headers, timeout=5, verify=False, proxies=proxies, allow_redirects=True)
            display_status = 200 if response.status_code in [200, 444, 403] else response.status_code
            status_display = get_admin_panel_status(display_status)
            result = {'url': target_url, 'status_code': response.status_code, 'display_status': display_status, 'status_display': status_display, 'length': len(response.text), 'redirect': response.url if response.history else None}
            results.append(result)
            if display_status == 200:
                best_results.append(result)
            time.sleep(0.1)
        except requests.exceptions.RequestException as e:
            error_message = str(e)
            display_status = 200 if '104' in error_message or 'Connection reset by peer' in error_message else 'Error'
            status_display = get_admin_panel_status(display_status, error_message)
            error_result = {'url': target_url, 'status_code': 'Error', 'display_status': display_status, 'status_display': status_display, 'error': error_message, 'length': 'N/A'}
            results.append(error_result)
            if display_status == 200:
                best_results.append(error_result)
    best_results.sort(key=lambda x: len(x['url']))
    return (results, best_results)

def check_ssl(url):
    try:
        normalized_url = normalize_url_for_scans(url)
        parsed = urlparse(normalized_url)
        hostname = parsed.hostname
        port = parsed.port or 443
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, port))
        return True
    except Exception as e:
        if 'Errno 111' not in str(e) and 'Connection refused' not in str(e):
            logging.error(f'SSL check failed for {url}: {e}')
        return False

def portal_status(url, proxy=None):
    """Enhanced portal status check that handles URLs with ports properly"""  # inserted
    try:
        parsed = urlparse(url)
        if parsed.port and parsed.port not in [80, 443]:
            test_url = url
        else:  # inserted
            test_url = normalize_url_for_scans(url)
        start_time = time.time()
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        try:
            resp = requests.head(test_url, headers=headers, timeout=10, allow_redirects=True, verify=False, proxies=proxies)
        except requests.exceptions.RequestException:
            resp = requests.get(test_url, headers=headers, timeout=10, allow_redirects=True, verify=False, proxies=proxies)
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)
    if resp.status_code < 200:
        status_category = 'Informational (<200)'
        status_icon = 'ℹ️'
    else:  # inserted
        if resp.status_code < 300:
            status_category = 'Success (<300)'
            status_icon = '✅'
        else:  # inserted
            if resp.status_code < 400:
                status_category = 'Redirection (<400)'
                status_icon = '↪️'
            else:  # inserted
                if resp.status_code < 500:
                    status_category = 'Client Error (<500)'
                    status_icon = '❌'
                else:  # inserted
                    status_category = 'Server Error (>=500)'
                    status_icon = '🔥'
    if resp.status_code < 400:
        return ('✅ Up ', resp.status_code, status_category, response_time, status_icon)
    return ('🔴 Down', resp.status_code, status_category, response_time, status_icon)
    except Exception as e:
        if 'Errno 111' not in str(e) and 'Connection refused' not in str(e):
            logging.error(f'Portal status check failed for {url}: {e}')
        return ('🔴 Down', 'N/A', 'No response', 'N/A', '💀')

def get_ip_info(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {'IP': data.get('ip', 'Unknown'), 'Hostname': data.get('hostname', 'Unknown'), 'City': data.get('city', 'Unknown'), 'Region': data.get('region', 'Unknown'), 'Country': data.get('country', 'Unknown'), 'Org': data.get('org', 'Unknown'), 'Postal': data.get('postal', 'Unknown'), 'Timezone': data.get('timezone', 'Unknown'), 'ASN': data.get('org', 'Unknown').split()[0] if data.get('org') else 'Unknown'}
        return {'Error': 'Failed to fetch IP information'}
    except Exception as e:
        logging.error(f'IP info lookup failed for {ip}: {e}')
        return {'Error': str(e)}

def detect_stb_model(headers_info, url='', html_content=''):
    """\n    Detect precise STB model from HTTP headers, URL patterns, HTML content, and other signatures\n    """  # inserted
    stb_models = []
    server = headers_info.get('Server', '').lower()
    x_powered_by = headers_info.get('X-Powered-By', '').lower()
    url_lower = url.lower()
    mag_models = {'MAG254': ['mag254', '254', 'stb_mag254'], 'MAG256': ['mag256', '256', 'stb_mag256'], 'MAG257': ['mag257', '257', 'stb_mag257'], 'MAG260': ['mag260', '260', 'stb_mag260'], 'MAG270': ['mag270', '270', 'stb_mag270'], 'MAG275': ['mag275', '275', 'stb_mag275'], 'MAG322': ['mag322', '322', 'stb_mag322'], 'MAG324': ['mag324', '324', 'stb_mag324'], 'MAG325': ['mag325', '325', 'stb_mag325'], 'MAG349': ['mag349', '349', 'stb_mag349'], 'MAG350': ['mag350', '350', 'stb_mag350'], 'MAG351': ['mag351', '351'
    stb_signatures = {'Formuler Z': ['formuler z', 'formuler-z', 'fz'], 'Formuler Z+': ['formuler z+', 'formuler-z+', 'fz+'], 'Formuler Z8': ['formuler z8', 'formuler-z8', 'fz8'], 'Formuler Z10': ['formuler z10', 'formuler-z10', 'fz10'], 'DreamBox One': ['dreambox one', 'dm one', 'dm-one'], 'DreamBox Two': ['dreambox two', 'dm two', 'dm-two'], 'DreamBox UHD': ['dreambox uhd', 'dm uhd', 'dm-uhd'], 'Enigma2': ['enigma2', 'e2', 'openatv', 'openpli'], 'Android TV Box': ['android tv', 'android-box', 'tv-box'], 'Xtream Codes': ['xtream', 'xc', 'xtream-codes'], 'Stalker Middleware': ['stalker', 'middleware', 'minimiddleware'], 'Kodi': ['kodi',
    for model, signatures in mag_models.items():
        for sig in signatures:
            if (sig in server or sig in x_powered_by or sig in url_lower or (sig in html_content)) and model not in stb_models:
                stb_models.append(model)
    for model, signatures in stb_signatures.items():
        for sig in signatures:
            if (sig in server or sig in x_powered_by or sig in url_lower or (sig in html_content)) and model not in stb_models:
                stb_models.append(model)
    user_agent = headers_info.get('User-Agent', '').lower()
    x_user_agent = headers_info.get('X-User-Agent', '').lower()
    ua_models = {'MAG254': 'mag254', 'MAG256': 'mag256', 'MAG257': 'mag257', 'MAG260': 'mag260', 'MAG322': 'mag322', 'MAG324': 'mag324', 'MAG349': 'mag349', 'MAG350': 'mag350', 'MAG351': 'mag351', 'MAG420': 'mag420', 'MAG424': 'mag424', 'MAG424w3': 'mag424w3', 'MAG520': 'mag520', 'MAG524': 'mag524', 'Formuler': 'formuler', 'DreamBox': 'dreambox'}
    for model, pattern in ua_models.items():
        if (pattern in user_agent or pattern in x_user_agent) and model not in stb_models:
            stb_models.append(model)
    portal_patterns = {'MAG-Compatible': ['/c/', 'stalker_portal', 'mac=', 'serial_number='], 'Xtream-Codes-Compatible': ['player_api.php', 'panel_api.php', 'xtream'], 'Enigma2-Compatible': ['get.php', 'xmltv.php', 'enigma2']}
    for portal_type, patterns in portal_patterns.items():
        for pattern in patterns:
            if (pattern in url_lower or pattern in html_content) and portal_type not in stb_models:
                stb_models.append(portal_type)
    if not stb_models and ('xtream' in server or 'iptv' in server or 'stalker' in server or ('portal' in url_lower) or ('/c/' in url) or ('mac=' in url_lower)):
        stb_models.append('Generic IPTV STB')
    return stb_models if stb_models else ['Unknown/Web Browser']

def get_stb_details(stb_models, headers_info):
    """\n    Get detailed information about detected STB models\n    """  # inserted
    details = {}
    for model in stb_models:
        if 'MAG' in model:
            details[model] = {'Manufacturer': 'Infomir', 'Type': 'Set-top Box', 'Common Usage': 'IPTV services'}
        else:  # inserted
            if 'Formuler' in model:
                details[model] = {'Manufacturer': 'Formuler', 'Type': 'Android TV Box', 'Common Usage': 'IPTV with MYTVOnline'}
            else:  # inserted
                if 'DreamBox' in model:
                    details[model] = {'Manufacturer': 'Dream Multimedia', 'Type': 'Linux Set-top Box', 'Common Usage': 'Satellite TV with Enigma2'}
                else:  # inserted
                    if model == 'Enigma2':
                        details[model] = {'Manufacturer': 'Various', 'Type': 'Software platform', 'Common Usage': 'Satellite receivers'}
                    else:  # inserted
                        details[model] = {'Type': 'Unknown/Generic', 'Common Usage': 'Various media streaming'}
    return details

def reverse_dns_lookup(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except:
        return 'Not available'

def enumerate_subdomains(domain, subdomains_list=COMMON_SUBDOMAINS, max_workers=20):
    found_subdomains = []

    def check_subdomain(subdomain):
        try:
            full_domain = f'{subdomain}.{domain}'
            ip = socket.gethostbyname(full_domain)
            return (full_domain, ip)
        except:
            return None
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_subdomain, subdomain): subdomain for subdomain in subdomains_list}
        for future in as_completed(futures):
            result = future.result()
            if result:
                found_subdomains.append(result)
    return found_subdomains

def analyze_headers(url, proxy=None):
    try:
        normalized_url = normalize_url_for_scans(url)
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        resp = requests.get(normalized_url, headers=headers, timeout=10, verify=False, proxies=proxies)
        security_headers = {'Strict-Transport-Security': 'HSTS', 'Content-Security-Policy': 'CSP', 'X-Frame-Options': 'X-Frame-Options', 'X-Content-Type-Options': 'X-Content-Type-Options', 'X-XSS-Protection': 'X-XSS-Protection', 'Referrer-Policy': 'Referrer-Policy'}
        detected_headers = {}
        for header, value in resp.headers.items():
            if header in security_headers:
                detected_headers[security_headers[header]] = value
        return {'Server': resp.headers.get('Server', 'Unknown'), 'X-Powered-By': resp.headers.get('X-Powered-By', 'Unknown'), 'Security Headers': detected_headers, 'All Headers': dict(resp.headers)}
    except Exception as e:
        logging.error(f'Header analysis failed for {url}: {e}')
        return {'Error': str(e)}

def detect_protection(url, proxy=None):
    protections = {'Cloudflare': ['cf-ray', 'cloudflare', '__cfduid', '__cf_bm'], 'DDoS-Guard': ['ddos-guard'], 'Sucuri': ['sucuri'], 'Akamai': ['akamai', 'akamaiedge'], 'Incapsula': ['incapsula', 'visid_incap'], 'Nginx': ['nginx'], 'Apache': ['apache'], 'LiteSpeed': ['litespeed'], 'IIS': ['microsoft-iis', 'iis'], 'OpenResty': ['openresty']}
    detected = []
    try:
        normalized_url = normalize_url_for_scans(url)
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        resp = requests.get(normalized_url, headers=headers, timeout=10, verify=False, proxies=proxies)
        headers_lower = {k.lower(): v.lower() for k, v in resp.headers.items()}
        cookies_lower = [c.lower() for c in resp.cookies.keys()] if resp.cookies else []
        for prot, signs in protections.items():
            for sign in signs:
                if any((sign in h for h in headers_lower.values())) or sign in str(cookies_lower) or sign in resp.text.lower():
                    detected.append(prot)
                    break
        return list(set(detected))
    except Exception as e:
        logging.error(f'Protection detection failed for {url}: {e}')
        return []

def generate_mac(prefix):
    return prefix + ':' + ':'.join(['%02X' % random.randint(0, 255) for _ in range(3)])

def test_mac_login(url: str, mac: str, stb_model: str='MAG322', proxy: str=None) -> dict:
    """\n    Test MAC address authentication against a portal endpoint, impersonating a specific STB model.\n    """  # inserted
    headers = {'User-Agent': f'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) {stb_model} stbapp ver: 2 rev: 250 Safari/533.3', 'X-User-Agent': f'Model: {stb_model}; Link: WiFi', 'Authorization': f'MAC {mac}'}
    result = {'model': stb_model, 'mac': mac, 'status': '💥 Not Tested', 'http_status': 'N/A', 'response_length': 0, 'response_text_snippet': '', 'is_authorized': False}
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        normalized_url = normalize_url_for_scans(url)
        if not normalized_url.endswith('/c/') and (not normalized_url.endswith('/stalker_portal/server/load.php')):
            normalized_url = normalized_url.rstrip('/') + '/c/'
        response = requests.get(normalized_url, headers=headers, timeout=8, verify=False, proxies=proxies)
        response_text = response.text.lower()
        result['http_status'] = response.status_code
        result['response_length'] = len(response.text)
        result['response_text_snippet'] = response.text[:100] + '...' if response.text else 'Empty Response'
        if response.status_code == 200:
            if 'not authorized' in response_text:
                result['status'] = '❌ Denied (200 but not auth)'
            else:  # inserted
                if 'ok' in response_text or 'true' in response_text:
                    result['status'] = '✅ OK (Authorized)'
                    result['is_authorized'] = True
                else:  # inserted
                    result['status'] = '⚠️  200 OK (Unknown Response)'
        else:  # inserted
            if response.status_code == 403:
                result['status'] = '🚫 403 Forbidden'
            else:  # inserted
                if response.status_code == 404:
                    result['status'] = '🔍 404 Not Found'
                else:  # inserted
                    result['status'] = f'❓ HTTP {response.status_code}'
    except requests.exceptions.Timeout:
        result['status'] = '⏰ Timeout'
    except requests.exceptions.RequestException as e:
        result['status'] = f'🌐 Network Error: {e}'
    except Exception as e:
        result['status'] = f'💥 Unexpected Error: {e}'
    return result

def fingerprint_stb_models(url, mac, models_to_test, proxy=None):
    """\n    Tests a portal against a list of STB models to see which ones are accepted.\n    """  # inserted
    results = []
    for model in models_to_test:
        result = test_mac_login(url, mac, model, proxy)
        results.append(result)
        time.sleep(0.3)
    return results

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((host, port))
            if result!= 0:
                return (port, 'closed')
            req = f'HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Scanner\r\nConnection: close\r\n\r\n'.encode()
            try:
                s.send(req)
                banner = s.recv(1024).decode(errors='ignore')
                status_line = banner.split('\n')[0].strip()
                if status_line.startswith('HTTP/'):
                    return (port, status_line)
                return (port, 'open')
            except:
                return (port, 'open')
    except:
        return (port, 'error')

def scan_ports(host, ports=COMMON_PORTS, max_workers=50):
    open_ports = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, host, port): port for port in ports}
        for future in as_completed(future_to_port):
            try:
                result = future.result()
                if result:
                    port, status = result
                    open_ports[port] = status
            except:
                pass
    return open_ports

def save_summary(data, portal_name):
    safe_name = ''.join((c for c in portal_name if c.isalnum() or c in ['-', '_'])).rstrip()
    timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
    filename = os.path.join(OUTPUT_FOLDER, f'Portal_Detective_{safe_name}_{timestamp}.txt')
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('╔══════════════════════════════════════════════════════════════════╗\n')
            f.write('║                               🕵    PORTAL DETECTIVE PRO FINAL    🕵‍                    ║\n')
            f.write('║                               🌐 Advanced Portal Analysis Toolkit 🌐                    ║\n')
            f.write('║                                          🖤 𝗔𝗡𝗚𝗜𝗡𝗔™ 🖤                                 ║\n')
            f.write('╚══════════════════════════════════════════════════════════════════╝\n\n')
            f.write(f"📅 Report Generated: {datetime.now().strftime('%B %d,%Y - %I:%M %p')}\n")
            f.write('────────────────────────────────────────────────────────────────────────────────\n\n')
            f.write('🔰 BASIC INFORMATION:\n')
            f.write(f"   📍 Portal: {data.get('Portal', 'N/A')}\n")
            f.write(f"   📊 Status: {data.get('Status', 'N/A')}\n")
            f.write(f"   🌐 IP Address: {data.get('IP Address', 'N/A')}\n")
            f.write(f"   🔁 Reverse DNS: {data.get('Reverse DNS', 'N/A')}\n")
            f.write(f"   🔒 SSL Valid: {data.get('SSL Valid', 'N/A')}\n")
            f.write(f"   📟 Status Code: {data.get('Status Code', 'N/A')}\n")
            f.write(f"   ⏱️  Response Time: {data.get('Response Time (ms)', 'N/A')} ms\n\n")
            f.write('🌍 IP INFORMATION:\n')
            ip_info_keys = ['Hostname', 'City', 'Region', 'Country', 'Org', 'Postal', 'Timezone', 'ASN']
            for key in ip_info_keys:
                if key in data:
                    if key == 'Country':
                        country_code = data[key]
                        country_name, flag_emoji = get_country_info(country_code)
                        f.write(f'   {key}: {flag_emoji} {country_code} ({country_name})\n')
                    else:  # inserted
                        f.write(f'   {key}: {data[key]}\n')
            f.write('\n')
            f.write('📺 STB INFORMATION:\n')
            if 'STB Models' in data and data['STB Models']:
                f.write(f"   Detected Models: {', '.join(data['STB Models'])}\n")
            if 'STB Details' in data and data['STB Details']:
                for model, details in data['STB Details'].items():
                    f.write(f'   {model}:\n')
                    for key, value in details.items():
                        f.write(f'     • {key}: {value}\n')
            f.write('\n')
            if 'Open Ports' in data and data['Open Ports']:
                f.write('🚪 OPEN PORTS:\n')
                for port, banner in data['Open Ports'].items():
                    f.write(f'   Port {port}: {banner}\n')
                f.write('\n')
            if 'Subdomains Found' in data and data['Subdomains Found']:
                f.write(f"🌐 FOUND SUBDOMAINS ({len(data['Subdomains Found'])}):\n")
                for i, (subdomain, sub_ip) in enumerate(data['Subdomains Found'], 1):
                    f.write(f'   {i:2d}. {subdomain} → {sub_ip}\n')
                f.write('\n')
            if 'Similar Portals' in data and data['Similar Portals']:
                f.write(f"🔗 SIMILAR PORTALS FOUND ({len(data['Similar Portals'])}):\n")
                for i, portal in enumerate(data['Similar Portals'], 1):
                    f.write(f'   {i:2d}. {portal}\n')
                f.write('\n')
            if 'Admin Panel Results' in data and data['Admin Panel Results']:
                f.write('🔐 ADMIN PANEL DISCOVERY RESULTS:\n')
                if 'Best Admin Panel Candidates' in data and data['Best Admin Panel Candidates']:
                    f.write(f"   Best Candidates ({len(data['Best Admin Panel Candidates'])}):\n")
                    for i, result in enumerate(data['Best Admin Panel Candidates'], 1):
                        ansi_escape = re.compile('\\x1B(?:[@-Z\\\\-_]|\\[[0-?]*[ -/]*[@-~])')
                        clean_status = ansi_escape.sub('', result['status_display'])
                        f.write(f"     {i:2d}. {clean_status} {result['url']}\n")
                    f.write('\n')
                f.write(f"   All Tested Paths ({len(data['Admin Panel Results'])}):\n")
                for i, result in enumerate(data['Admin Panel Results'], 1):
                    ansi_escape = re.compile('\\x1B(?:[@-Z\\\\-_]|\\[[0-?]*[ -/]*[@-~])')
                    clean_status = ansi_escape.sub('', result['status_display'])
                    f.write(f"   {i:2d}. {result['url']} - {clean_status}")
                    if result.get('redirect'):
                        f.write(f" → Redirects to: {result['redirect']}")
                    f.write(f" (Length: {result.get('length', 'N/A')} bytes)\n")
                f.write('\n')
            if 'Protections Detected' in data and data['Protections Detected']:
                f.write(f"🛡️  PROTECTIONS DETECTED ({len(data['Protections Detected'])}):\n")
                for protection in data['Protections Detected']:
                    f.write(f'   • {protection}\n')
                f.write('\n')
            if 'HTTP Headers' in data and 'Error' not in data['HTTP Headers']:
                f.write('📋 HTTP HEADERS:\n')
                headers = data['HTTP Headers']
                f.write(f"   Server: {headers.get('Server', 'Unknown')}\n")
                f.write(f"   X-Powered-By: {headers.get('X-Powered-By', 'Unknown')}\n")
                if headers.get('Security Headers'):
                    f.write('   Security Headers:\n')
                    for header, value in headers['Security Headers'].items():
                        f.write(f'     • {header}: {value}\n')
                f.write('\n')
            if 'MAC Login Tests' in data and data['MAC Login Tests']:
                successful_tests = sum((1 for status in data['MAC Login Tests'].values() if 'OK' in status or 'Authorized' in status))
                total_tests = len(data['MAC Login Tests'])
                f.write(f'🔌 MAC LOGIN TESTS: {successful_tests}/{total_tests} successful\n')
                f.write('   Detailed Results:\n')
                for mac, status in data['MAC Login Tests'].items():
                    status_icon = '✅' if 'OK' in status or 'Authorized' in status else '❌'
                    f.write(f'     {status_icon} {mac}: {status}\n')
                f.write('\n')
            if 'STB Fingerprinting' in data and data['STB Fingerprinting']:
                successful_models = [r for r in data['STB Fingerprinting'] if 'OK' in r['status'] or 'Authorized' in r['status']]
                f.write(f"🔬 STB FINGERPRINTING RESULTS: {len(successful_models)}/{len(data['STB Fingerprinting'])} models accepted\n")
                f.write('   Detailed Results:\n')
                for result in data['STB Fingerprinting']:
                    status_icon = '✅' if 'OK' in result['status'] or 'Authorized' in result['status'] else '❌'
                    f.write(f"     {status_icon} {result['model']}: {result['status']}\n")
                f.write('\n')
            f.write('────────────────────────────────────────────────────────────────────────────────\n')
            f.write('📋 End of Report\n')
        return filename
    except Exception as e:
        logging.error(f'Failed to save summary: {e}')
        return None
DARK_THEME = '\nQMainWindow, QWidget {\n    background-color: #1e1e1e;\n    color: #ffffff;\n    font-family: Segoe UI, Arial;\n}\n\nQTabWidget::pane {\n    border: 1px solid #444;\n    background-color: #2d2d2d;\n}\n\nQTabBar::tab {\n    background-color: #333;\n    color: #ccc;\n    padding: 8px 16px;\n    margin-right: 2px;\n    border: 1px solid #444;\n    border-bottom: none;\n    border-top-left-radius: 4px;\n    border-top-right-radius: 4px;\n}\n\nQTabBar::tab:selected {\n    background-color: #0078d4;\n    color: white;\n    border-color: #005a9e;\n}\n\nQTabBar::tab:hover {\n    background-color: #555;\n}\n\nQGroupBox {\n    font-weight: bold;\n    border: 1px solid #444;\n    border-radius: 5px;\n    margin-top: 10px;\n    padding-top: 10px;\n    color: #0078d4;\n    background-color: #252525;\n}\n\nQGroupBox::title {\n    subcontrol-origin: margin;\n    left: 10px;\n    padding: 0 5px 0 5px;\n    color: #0078d4;\n}\n\nQPushButton {\n    background-color: #0078d4;\n    color: white;\n    border: none;\n    padding: 8px 16px;\n    border-radius: 4px;\n    font-weight: bold;\n    min-width: 80px;\n}\n\nQPushButton:hover {\n    background-color: #106ebe;\n}\n\nQPushButton:pressed {\n    background-color: #005a9e;\n}\n\nQPushButton:disabled {\n    background-color: #555;\n    color: #888;\n}\n\nQPushButton#scanButton {\n    background-color: #107c10;\n    font-size: 12px;\n}\n\nQPushButton#scanButton:hover {\n    background-color: #0e6b0e;\n}\n\nQPushButton#stopButton {\n    background-color: #d83b01;\n    font-size: 12px;\n}\n\nQPushButton#stopButton:hover {\n    background-color: #b32d00;\n}\n\nQPushButton#saveButton {\n    background-color: #ffb900;\n    color: #000;\n    font-size: 12px;\n}\n\nQPushButton#saveButton:hover {\n    background-color: #d19d00;\n}\n\nQPushButton#historyButton {\n    background-color: #9C27B0;\n    font-size: 12px;\n}\n\nQPushButton#historyButton:hover {\n    background-color: #7B1FA2;\n}\n\nQLabel {\n    color: #cccccc;\n    padding: 2px;\n}\n\nQProgressBar {\n    border: 1px solid #444;\n    border-radius: 3px;\n    text-align: center;\n    color: white;\n    background-color: #333;\n}\n\nQProgressBar::chunk {\n    background-color: #0078d4;\n    border-radius: 2px;\n}\n\nQTextEdit, QListWidget, QTableWidget {\n    background-color: #252525;\n    color: #cccccc;\n    border: 1px solid #444;\n    border-radius: 3px;\n    font-family: Consolas, monospace;\n    font-size: 11px;\n}\n\nQComboBox, QSpinBox, QLineEdit {\n    background-color: #333;\n    color: white;\n    border: 1px solid #555;\n    border-radius: 3px;\n    padding: 4px;\n    min-height: 20px;\n}\n\nQComboBox:editable, QSpinBox:editable, QLineEdit:editable {\n    background-color: #2a2a2a;\n}\n\nQComboBox::drop-down {\n    border: none;\n}\n\nQComboBox QAbstractItemView {\n    background-color: #333;\n    color: white;\n    border: 1px solid #555;\n    selection-background-color: #0078d4;\n}\n\nQCheckBox {\n    color: #cccccc;\n    spacing: 5px;\n}\n\nQCheckBox::indicator {\n    width: 16px;\n    height: 16px;\n}\n\nQCheckBox::indicator:unchecked {\n    border: 1px solid #666;\n    background-color: #333;\n}\n\nQCheckBox::indicator:checked {\n    border: 1px solid #0078d4;\n    background-color: #0078d4;\n}\n\nQHeaderView::section {\n    background-color: #333;\n    color: #cccccc;\n    padding: 4px;\n    border: 1px solid #444;\n    font-weight: bold;\n}\n\nQTableWidget {\n    gridline-color: #444;\n    alternate-background-color: #2a2a2a;\n}\n\nQTableWidget::item {\n    padding: 4px;\n    border-bottom: 1px solid #333;\n}\n\nQTableWidget::item:selected {\n    background-color: #0078d4;\n    color: white;\n}\n\nQSplitter::handle {\n    background-color: #444;\n    border: 1px solid #555;\n}\n\nQSplitter::handle:hover {\n    background-color: #555;\n}\n\nQStatusBar {\n    background-color: #0078d4;\n    color: white;\n    border-top: 1px solid #005a9e;\n}\n'

class PortalAnalysisThread(QThread):
    progress_update = pyqtSignal(dict)
    finished_analysis = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, urls, config, proxy=None):
        super().__init__()
        self.urls = urls
        self.config = config
        self.proxy = proxy
        self.is_running = True
        self.results = []
        self.current_progress = 0

    def stop(self):
        self.is_running = False

    def analyze_single_url(self, url):
        """Analyze a single URL and return results"""  # inserted
        try:
            if not self.is_running:
                return
            url = url.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            original_url = url
            normalized_url = normalize_url_for_scans(url)
            parsed = urlparse(normalized_url)
            hostname = parsed.hostname
            domain = '.'.join(hostname.split('.')[(-2):]) if hostname.count('.') >= 2 else hostname
            try:
                ip = socket.gethostbyname(hostname)
                ip_info = get_ip_info(ip)
                reverse_dns = reverse_dns_lookup(ip)
            except Exception as e:
                return {'Portal': url, 'Error': f'Unable to resolve IP: {e}'}
            with ThreadPoolExecutor(max_workers=6) as executor:
                status_future = executor.submit(portal_status, url, self.proxy)
                ssl_future = executor.submit(check_ssl, url)
                ports_future = executor.submit(scan_ports, hostname)
                headers_future = executor.submit(analyze_headers, url, self.proxy)
                protections_future = executor.submit(detect_protection, url, self.proxy)
                subdomains_future = executor.submit(enumerate_subdomains, domain)
                urlscan_future = executor.submit(urlscan_analyze_portal, url, self.proxy)
                status, status_code, status_category, response_time, status_icon = status_future.result()
                ssl_valid = ssl_future.result()
                open_ports = ports_future.result()
                headers_info = headers_future.result()
                protections_detected = protections_future.result()
                found_subdomains = subdomains_future.result()
                similar_portals = urlscan_future.result()
            html_content = ''
            try:
                headers = {'User-Agent': random.choice(USER_AGENTS)}
                proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
                resp = requests.get(normalized_url, headers=headers, timeout=10, verify=False, proxies=proxies)
                html_content = resp.text.lower()
            except:
                pass
            stb_models = detect_stb_model(headers_info, normalized_url, html_content)
            stb_details = get_stb_details(stb_models, headers_info)
            admin_results, best_results = discover_admin_panels(original_url, self.proxy)
            mac_results = {}
            for prefix in MAC_PREFIXES:
                if not self.is_running:
                    break
                mac = generate_mac(prefix)
                result = test_mac_login(url, mac, 'MAG322', self.proxy)
                mac_results[mac] = result['status']
                time.sleep(0.1)
            stb_fingerprinting = []
            working_mac = None
            for mac, status in mac_results.items():
                if 'OK' in status or 'Authorized' in status:
                    working_mac = mac
                    break
            if working_mac and self.is_running:
                target_models = ['MAG254', 'MAG256', 'MAG257', 'MAG260', 'MAG270', 'MAG275', 'MAG322', 'MAG324', 'MAG325', 'MAG349', 'MAG350', 'MAG351', 'MAG352', 'MAG420', 'MAG424', 'MAG424w3', 'MAG425', 'MAG520', 'MAG524', 'Formuler Z', 'Formuler Z+', 'Formuler Z8', 'Formuler Z10']
                stb_fingerprinting = fingerprint_stb_models(url, working_mac, target_models, self.proxy)
            analysis_data = {'Portal': url, 'Normalized Portal': normalized_url, 'Status': status, 'IP Address': ip, 'Reverse DNS': reverse_dns, 'STB Models': stb_models, 'STB Details': stb_details, 'Open Ports': open_ports, 'SSL Valid': 'Yes' if ssl_valid else 'No', 'Status Code': status_code, 'Status Category': status_category, 'Response Time (ms)': response_time, **{'Subdomains Found': ip_info, 'Similar Portals': found_subdomains, 'Protections Detected': similar_portals, 'HTTP Headers': protections_detected, 'Admin Panel Results': headers_info, 'Best Admin Panel Candidates': admin_results, 'MAC Login Tests': best_results, 'STB Fingerprinting': stb_fingerprinting}}
            return analysis_data
        except Exception as e:
            return {'Portal': url, 'Error': str(e)}

    def run(self):
        try:
            total_urls = len(self.urls)
            self.current_progress = 0
            if total_urls == 1:
                url = self.urls[0]
                self.progress_update.emit({'message': '🔄 Starting analysis...', 'type': 'info', 'progress': 5})
                time.sleep(0.5)
                progress_steps = [(15, '🔍 Resolving DNS and IP information...'), (25, '🌐 Checking portal status...'), (35, '🔒 Testing SSL certificate...'), (45, '🚪 Scanning common ports...'), (55, '📋 Analyzing HTTP headers...'), (65, '🛡️ Detecting security protections...'), (75, '🌐 Enumerating subdomains...'), (80, '🔗 Searching for similar portals...'), (85, '📺 Detecting STB models...'), (90, '🔐 Testing admin panel access...'), (95, '🔌 Testing MAC authentication...')]
                for progress, message in progress_steps:
                    if not self.is_running:
                        break
                    self.current_progress = progress
                    self.progress_update.emit({'message': f'{message}', 'type': 'info', 'progress': self.current_progress})
                    time.sleep(1.5)
                if self.is_running:
                    result = self.analyze_single_url(url)
                    if result:
                        self.results.append(result)
                    self.progress_update.emit({'message': '✅ Analysis completed! Processing results...', 'type': 'info', 'progress': 100})
            else:  # inserted
                for i, url in enumerate(self.urls):
                    if not self.is_running:
                        break
                    self.current_progress = int(i / total_urls * 100)
                    self.progress_update.emit({'message': f'🔍 Analyzing {i + 1}/{total_urls}: {url}', 'type': 'info', 'progress': self.current_progress})
                    result = self.analyze_single_url(url)
                    if result:
                        self.results.append(result)
                    self.current_progress = int((i + 1) / total_urls * 100)
                    self.progress_update.emit({'message': f'✅ Completed {i + 1}/{total_urls}: {url}', 'type': 'info', 'progress': self.current_progress})
            self.progress_update.emit({'message': '🎉 All analyses completed!', 'type': 'info', 'progress': 100})
            self.finished_analysis.emit(self.results)
        except Exception as e:
            self.error_occurred.emit(str(e))

class PortalDetectivePro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_urls = []
        self.analysis_thread = None
        self.analysis_results = []
        self.expanded_sections = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('🖤 ANGINA™ 🖤 Portal Detective Pro 🕵️')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(DARK_THEME)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        header_layout = QHBoxLayout()
        title_label = QLabel('🖤 ANGINA™ 🖤 Portal Detective Pro 🕵️')
        title_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title_label.setStyleSheet('color: #e91e63; padding: 5px;')
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.analyze_btn = QPushButton('🔍 START ANALYSIS')
        self.analyze_btn.setObjectName('scanButton')
        self.analyze_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.analyze_btn.setMinimumHeight(35)
        header_layout.addWidget(self.analyze_btn)
        self.stop_btn = QPushButton('🛑 STOP ANALYSIS')
        self.stop_btn.setObjectName('stopButton')
        self.stop_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.stop_btn.clicked.connect(self.stop_analysis)
        self.stop_btn.setMinimumHeight(35)
        self.stop_btn.setEnabled(False)
        header_layout.addWidget(self.stop_btn)
        self.save_btn = QPushButton('💾 SAVE RESULTS')
        self.save_btn.setObjectName('saveButton')
        self.save_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setMinimumHeight(35)
        self.save_btn.setEnabled(False)
        header_layout.addWidget(self.save_btn)
        self.history_btn = QPushButton('📚 HISTORY STATS')
        self.history_btn.setObjectName('historyButton')
        self.history_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.history_btn.clicked.connect(self.show_history_statistics)
        self.history_btn.setMinimumHeight(35)
        header_layout.addWidget(self.history_btn)
        main_layout.addLayout(header_layout)
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel('Progress:'))
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        self.progress_label = QLabel('Ready to analyze')
        self.progress_label.setStyleSheet('color: #4FC3F7; font-weight: bold;')
        progress_layout.addWidget(self.progress_label)
        progress_layout.addStretch()
        main_layout.addLayout(progress_layout)
        tabs = QTabWidget()
        tabs.setFont(QFont('Segoe UI', 9))
        main_layout.addWidget(tabs)
        input_tab = QWidget()
        input_layout = QVBoxLayout(input_tab)
        input_layout.setSpacing(10)
        url_group = QGroupBox('📥 Portal URL Input')
        url_layout = QVBoxLayout(url_group)
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel('⌨ Input Method:'))
        self.input_method = QComboBox()
        self.input_method.addItems(['Import from file', 'Manual entry', 'Load from history'])
        self.input_method.setFont(QFont('Segoe UI', 9))
        method_layout.addWidget(self.input_method)
        method_layout.addStretch()
        url_layout.addLayout(method_layout)
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel('🔻 Input:'))
        self.file_combo = QComboBox()
        self.file_combo.setFont(QFont('Segoe UI', 9))
        self.refresh_file_list()
        file_layout.addWidget(self.file_combo)
        self.refresh_files_btn = QPushButton('🔄 Refresh')
        self.refresh_files_btn.clicked.connect(self.refresh_file_list)
        file_layout.addWidget(self.refresh_files_btn)
        url_layout.addLayout(file_layout)
        self.url_text = QTextEdit()
        self.url_text.setPlaceholderText('🌐 ENTER URL(s) (Line by line or separated by commas/semicolons): \nExamples:\nhttp://example1.com\nhttp://example2.com:port\nhttp://example3.com\nOR \nhttp://example1.com, http://example2.com:port; http://example3.com\n\n⚠️ Note: Donot include /c/ \n\n👇 Press \'🔰 Load URL(s)')
        self.url_text.setMinimumHeight(120)
        url_layout.addWidget(self.url_text)
        self.load_url_btn = QPushButton('🔰 Load URL(s)')
        self.load_url_btn.clicked.connect(self.load_url)
        url_layout.addWidget(self.load_url_btn)
        input_layout.addWidget(url_group)
        config_group = QGroupBox('⚙️ Configuration')
        config_layout = QHBoxLayout(config_group)
        left_config = QVBoxLayout()
        left_config.addWidget(QLabel('🎲 Workers: (MAX 50)'))
        self.max_workers = QSpinBox()
        self.max_workers.setRange(1, 50)
        self.max_workers.setValue(CONFIG['max_workers'])
        left_config.addWidget(self.max_workers)
        left_config.addWidget(QLabel('⏱️ Timeout/seconds: (MAX 30)'))
        self.timeout = QSpinBox()
        self.timeout.setRange(1, 30)
        self.timeout.setValue(CONFIG['timeout'])
        left_config.addWidget(self.timeout)
        config_layout.addLayout(left_config)
        middle_config = QVBoxLayout()
        middle_config.addWidget(QLabel('♾️ Retries: (MAX 5)'))
        self.retries = QSpinBox()
        self.retries.setRange(1, 5)
        self.retries.setValue(CONFIG['retries'])
        middle_config.addWidget(self.retries)
        self.enable_history = QCheckBox('🕕 Enable History')
        self.enable_history.setChecked(CONFIG['enable_history'])
        middle_config.addWidget(self.enable_history)
        config_layout.addLayout(middle_config)
        proxy_layout = QHBoxLayout()
        proxy_layout.addWidget(QLabel('🔌 Proxy (optional):'))
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText('http://proxy:port')
        proxy_layout.addWidget(self.proxy_input)
        config_layout.addLayout(proxy_layout)
        input_layout.addWidget(config_group)
        tabs.addTab(input_tab, '📥 Input & Configuration')
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        results_layout.setSpacing(10)
        splitter = QSplitter(Qt.Vertical)
        results_list_group = QGroupBox('📋 Analysis Results')
        results_list_layout = QVBoxLayout(results_list_group)
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_result_selected)
        results_list_layout.addWidget(self.results_list)
        splitter.addWidget(results_list_group)
        details_group = QGroupBox('🔍 Detailed Results')
        details_layout = QVBoxLayout(details_group)
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(3)
        self.details_table.setHorizontalHeaderLabels(['Category', 'Result', 'Detaills'])
        header = self.details_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.details_table.setColumnWidth(0, 250)
        self.details_table.setColumnWidth(1, 250)
        self.details_table.setFont(QFont('Consolas', 8))
        self.details_table.cellClicked.connect(self.on_details_clicked)
        details_layout.addWidget(self.details_table)
        splitter.addWidget(details_group)
        splitter.setSizes([200, 400])
        results_layout.addWidget(splitter)
        tabs.addTab(results_tab, '📊 Results')
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        log_group = QGroupBox('📝 Activity Log')
        log_group_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont('Consolas', 9))
        log_group_layout.addWidget(self.log_text)
        log_layout.addWidget(log_group)
        tabs.addTab(log_tab, '📝 Log')
        folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
        self.statusBar().showMessage(f'🖤 ANGINA™ 🖤 Portal Detective Pro - Ready{folder_info}')
        self.input_method.currentIndexChanged.connect(self.on_input_method_changed)
        self.on_input_method_changed()

    def on_input_method_changed(self):
        method = self.input_method.currentText()
        self.file_combo.setVisible(method in ['Import from file', 'Load from history'])
        self.refresh_files_btn.setVisible(method in ['Import from file', 'Load from history'])
        self.url_text.setVisible(method == 'Manual entry')

    def refresh_file_list(self):
        self.file_combo.clear()
        method = self.input_method.currentText()
        if method == 'Import from file':
            folder = INPUT_FOLDER
            file_pattern = '*.txt'
        else:  # inserted
            if method == 'Load from history':
                folder = HISTORY_FOLDER
                file_pattern = 'portal_history_*.json'
            else:  # inserted
                return None
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and (f.startswith('.') or method == 'Import from file' or f.startswith('portal_history_'))]
            self.file_combo.addItems(sorted(files, reverse=True))
        except Exception as e:
            self.log_message(f'Error reading folder: {e}', 'error')

    def load_url(self):
        method = self.input_method.currentText()
        urls = []
        if method == 'Import from file':
            filename = self.file_combo.currentText()
            if not filename:
                QMessageBox.warning(self, 'Warning', 'Please select a file')
                return
            filepath = os.path.join(INPUT_FOLDER, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    urls = self.parse_urls_from_text(content)
                    if not urls:
                        QMessageBox.warning(self, 'Warning', 'No valid URLs found in file')
                        return
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error reading file: {e}')
                return
        else:  # inserted
            if method == 'Manual entry':
                url_text = self.url_text.toPlainText().strip()
                if not url_text:
                    QMessageBox.warning(self, 'Warning', 'Please enter URL(s)')
                    return
                urls = self.parse_urls_from_text(url_text)
                if not urls:
                    QMessageBox.warning(self, 'Warning', 'No valid URLs found. URLs must start with http:// or https://')
                    return
            else:  # inserted
                if method == 'Load from history':
                    filename = self.file_combo.currentText()
                    if not filename:
                        QMessageBox.warning(self, 'Warning', 'Please select a history file')
                        return
                    filepath = os.path.join(HISTORY_FOLDER, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            history_data = json.load(f)
                        urls = []
                        if isinstance(history_data, list):
                            for entry in history_data:
                                if isinstance(entry, dict) and 'portal' in entry:
                                    urls.append(entry['portal'])
                                else:  # inserted
                                    if isinstance(entry, str):
                                        urls.append(entry)
                        if not urls:
                            QMessageBox.warning(self, 'Warning', 'No URLs found in history file')
                            return
                        self.log_message(f'📚 Loaded {len(urls)} URL(s) from history')
                    except Exception as e:
                        QMessageBox.warning(self, 'Error', f'Error reading history file: {e}')
                        return
        if urls:
            self.current_urls = urls
            self.log_message(f'✅ Loaded {len(urls)} URL(s)')
            self.analyze_btn.setEnabled(True)
            if method == 'Load from history':
                self.url_text.setPlainText('\n'.join(urls))
            folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
            self.statusBar().showMessage(f'🖤 Ready - {len(urls)} URL(s) loaded{folder_info}')
        else:  # inserted
            QMessageBox.warning(self, 'Warning', 'No valid URL(s) loaded')
            self.analyze_btn.setEnabled(False)

    def parse_urls_from_text(self, text):
        """Parse URLs from text with multiple separators"""  # inserted
        urls = []
        lines = text.split('\n')
        for line in lines:
            line_urls = re.split('[,\\s;]+', line.strip())
            for u in line_urls:
                u_clean = u.strip()
                if u_clean:
                    if not u_clean.startswith(('http://', 'https://')):
                        u_clean = 'http://' + u_clean
                    urls.append(u_clean)
        return list(set(urls))

    def start_analysis(self):
        if not hasattr(self, 'current_urls') or not self.current_urls:
            QMessageBox.warning(self, 'Warning', 'No URLs to analyze')
            return
        reply = QMessageBox.question(self, 'Start Analysis', f'Start analysis of {len(self.current_urls)} URL(s)?\nThis may take a while.', QMessageBox.Yes | QMessageBox.No)
        if reply!= QMessageBox.Yes:
            return
        self.prepare_for_analysis()
        config = {'max_workers': self.max_workers.value(), 'timeout': self.timeout.value(), 'retries': self.retries.value(), 'enable_history': self.enable_history.isChecked()}
        proxy = self.proxy_input.text().strip() or None
        self.analysis_thread = PortalAnalysisThread(self.current_urls, config, proxy)
        self.analysis_thread.progress_update.connect(self.on_progress_update)
        self.analysis_thread.finished_analysis.connect(self.on_analysis_finished)
        self.analysis_thread.error_occurred.connect(self.on_error_occurred)
        self.analysis_thread.start()

    def prepare_for_analysis(self):
        self.analysis_results = []
        self.results_list.clear()
        self.details_table.setRowCount(0)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.analyze_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.save_btn.setEnabled(False)
        self.progress_label.setText('🔄 Starting analysis...')
        folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
        self.statusBar().showMessage(f'🔄 Analyzing {len(self.current_urls)} URL(s)...{folder_info}')
        self.log_message(f'🚀 Started analysis of {len(self.current_urls)} URL(s)')

    def stop_analysis(self):
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.stop()
            self.analysis_thread.wait()
        self.analyze_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_label.setText('🛑 Analysis stopped')
        self.log_message('⏹️ Analysis stopped by user')

    def on_progress_update(self, progress_data):
        message = progress_data.get('message', '')
        msg_type = progress_data.get('type', 'info')
        progress = progress_data.get('progress', 0)
        self.log_message(message, msg_type)
        self.progress_label.setText(message)
        self.progress_bar.setValue(progress)

    def on_analysis_finished(self, results):
        self.analysis_results = results
        self.progress_bar.setValue(100)
        self.analyze_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.save_btn.setEnabled(True)
        self.display_results_list(results)
        if results:
            self.display_detailed_results(results[0])
            self.results_list.setCurrentRow(0)
        summary = f'✅ Analysis completed! Processed {len(results)} URL(s)'
        self.progress_label.setText(summary)
        folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
        self.statusBar().showMessage(f'{summary}{folder_info}')
        self.log_message(summary)
        self.auto_save_results()
        QMessageBox.information(self, 'Analysis Completed', summary)

    def on_error_occurred(self, error_message):
        """Handle errors from the analysis thread"""  # inserted
        self.log_message(f'❌ Analysis error: {error_message}', 'error')
        self.progress_label.setText(f'❌ Error: {error_message}')
        self.analyze_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        QMessageBox.critical(self, 'Analysis Error', f'An error occurred during analysis:\n{error_message}')

    def on_result_selected(self, item):
        """When a result is selected from the list"""  # inserted
        index = self.results_list.row(item)
        if 0 <= index < len(self.analysis_results):
            self.display_detailed_results(self.analysis_results[index])

    def on_details_clicked(self, row, column):
        """Handle clicks on expandable headers in the details table"""  # inserted
        if column!= 0:
            return
        item = self.details_table.item(row, 0)
        if not item:
            return
        text = item.text().strip()
        if text.startswith(('+', '-')) and len(text) > 2:
            display_name = text[2:].strip()
            section_mapping = {'Basic Info': 'basic_info', 'IP Information': 'ip_info', 'STB Information': 'stb_info', 'Open Ports': 'open_ports', 'Subdomains': 'subdomains', 'URLScan Results': 'urlscan', 'Security': 'security', 'HTTP Headers': 'http_headers', 'Admin Panels': 'admin_panels', 'MAC Authentication': 'mac_auth', 'STB Fingerprinting': 'stb_fingerprinting'}
            section_key = section_mapping.get(display_name)
            if section_key and section_key in self.expanded_sections:
                self.expanded_sections[section_key] = not self.expanded_sections[section_key]
                current_index = self.results_list.currentRow()
                if 0 <= current_index < len(self.analysis_results):
                    self.display_detailed_results(self.analysis_results[current_index])

    def display_results_list(self, results):
        """Display all results in the list widget"""  # inserted
        self.results_list.clear()
        for i, result in enumerate(results):
            portal = result.get('Portal', 'Unknown')
            status = result.get('Status', 'Unknown')
            status_code = result.get('Status Code', 'N/A')
            if 'Error' in result:
                item_text = f"❌ {portal} - Error: {result['Error']}"
                item = QListWidgetItem(item_text)
                item.setForeground(QColor('#FF6B6B'))
            else:  # inserted
                if status == '✅ Up ':
                    item_text = f'✅ {portal} - {status_code}'
                    item = QListWidgetItem(item_text)
                    item.setForeground(QColor('#90EE90'))
                else:  # inserted
                    item_text = f'🔴 {portal} - {status_code}'
                    item = QListWidgetItem(item_text)
                    item.setForeground(QColor('#FF6B6B'))
            self.results_list.addItem(item)

    def display_detailed_results(self, results):
        """Display detailed results for a single analysis with expandable sections"""  # inserted
        self.details_table.setRowCount(0)
        row = 0

        def add_row(category, key, value, is_header=False, expanded=False):
            nonlocal row  # inserted
            self.details_table.insertRow(row)
            if is_header:
                sign = '-' if expanded else '+'
                header_text = f'{sign} {category}'
                self.details_table.setItem(row, 0, QTableWidgetItem(header_text))
                self.details_table.setItem(row, 1, QTableWidgetItem(''))
                self.details_table.setItem(row, 2, QTableWidgetItem(''))
                for col in range(3):
                    item = self.details_table.item(row, col)
                    if item:
                        font = QFont()
                        font.setBold(True)
                        item.setFont(font)
                        item.setBackground(QColor('#2d2d2d'))
            else:  # inserted
                self.details_table.setItem(row, 0, QTableWidgetItem(''))
                self.details_table.setItem(row, 1, QTableWidgetItem(f'  {key}'))
                self.details_table.setItem(row, 2, QTableWidgetItem(str(value)))
            row += 1
        if not self.expanded_sections and {'basic_info': True, 'ip_info': False, 'stb_info': False, 'open_ports': False, 'subdomains': False, 'urlscan': False, 'security': False, 'http_headers': False, 'admin_panels': False, 'mac_auth': False, 'stb_fingerprinting': False} as https://urlscan.io/api/v1/scan/:
            pass  # postinserted
        if 'Error' in results:
            add_row('Error', 'Message', results['Error'])
            return
        add_row('Basic Info', '', '', is_header=True, expanded=self.expanded_sections['basic_info'])
        if self.expanded_sections['basic_info']:
            add_row('', 'Portal', results.get('Portal', 'N/A'))
            add_row('', 'Status', results.get('Status', 'N/A'))
            add_row('', 'IP Address', results.get('IP Address', 'N/A'))
            add_row('', 'Reverse DNS', results.get('Reverse DNS', 'N/A'))
            add_row('', 'SSL Valid', results.get('SSL Valid', 'N/A'))
            add_row('', 'Status Code', results.get('Status Code', 'N/A'))
            add_row('', 'Response Time', f"{results.get('Response Time (ms)', 'N/A')} ms")
        has_ip_info = any((key in results for key in ['Hostname', 'City', 'Region', 'Country', 'Org', 'Postal', 'Timezone', 'ASN']))
        if has_ip_info:
            add_row('IP Information', '', '', is_header=True, expanded=self.expanded_sections['ip_info'])
            if self.expanded_sections['ip_info']:
                for key in ['Hostname', 'City', 'Region', 'Country', 'Org', 'Postal', 'Timezone', 'ASN']:
                    if key in results and results[key] not in ['Unknown', 'N/A', '']:
                        if key == 'Country':
                            country_code = results[key]
                            country_name, flag_emoji = get_country_info(country_code)
                            add_row('', key, f'{flag_emoji} {country_code} ({country_name})')
                        else:  # inserted
                            add_row('', key, results[key])
        has_stb_info = 'STB Models' in results and results['STB Models'] and (results['STB Models']!= ['Unknown/Web Browser'])
        if has_stb_info:
            add_row('STB Information', '', '', is_header=True, expanded=self.expanded_sections['stb_info'])
            if self.expanded_sections['stb_info']:
                add_row('', 'Detected Models', ', '.join(results['STB Models']))
                if 'STB Details' in results and results['STB Details']:
                    for model, details in results['STB Details'].items():
                        add_row('', f'{model} Details', '')
                        for detail_key, detail_value in details.items():
                            add_row('', f'  {detail_key}', detail_value)
        has_open_ports = 'Open Ports' in results and results['Open Ports']
        if has_open_ports:
            add_row('Open Ports', '', '', is_header=True, expanded=self.expanded_sections['open_ports'])
            if self.expanded_sections['open_ports']:
                for port, banner in results['Open Ports'].items():
                    add_row('', f'Port {port}', banner)
        has_subdomains = 'Subdomains Found' in results and results['Subdomains Found']
        if has_subdomains:
            add_row('Subdomains', '', '', is_header=True, expanded=self.expanded_sections['subdomains'])
            if self.expanded_sections['subdomains']:
                for subdomain, ip in results['Subdomains Found']:
                    add_row('', subdomain, ip)
        has_similar_portals = 'Similar Portals' in results and results['Similar Portals']
        if has_similar_portals:
            add_row('URLScan Results', '', '', is_header=True, expanded=self.expanded_sections['urlscan'])
            if self.expanded_sections['urlscan']:
                add_row('', 'Similar Portals Found', len(results['Similar Portals']))
                for i, portal in enumerate(results['Similar Portals'], 1):
                    add_row('', f'Similar Portal {i}', portal)
        has_protections = 'Protections Detected' in results and results['Protections Detected']
        if has_protections:
            add_row('Security', '', '', is_header=True, expanded=self.expanded_sections['security'])
            if self.expanded_sections['security']:
                add_row('', 'Protections', ', '.join(results['Protections Detected']))
        has_headers = 'HTTP Headers' in results and 'Error' not in results['HTTP Headers']
        if has_headers:
            add_row('HTTP Headers', '', '', is_header=True, expanded=self.expanded_sections['http_headers'])
            if self.expanded_sections['http_headers']:
                headers = results['HTTP Headers']
                if headers.get('Server') not in ['Unknown', 'N/A', '']:
                    add_row('', 'Server', headers.get('Server', 'Unknown'))
                if headers.get('X-Powered-By') not in ['Unknown', 'N/A', '']:
                    add_row('', 'X-Powered-By', headers.get('X-Powered-By', 'Unknown'))
                if headers.get('Security Headers'):
                    add_row('', 'Security Headers', '')
                    for header, value in headers['Security Headers'].items():
                        add_row('', f'  {header}', value)
        has_admin_panels = 'Best Admin Panel Candidates' in results and results['Best Admin Panel Candidates']
        if has_admin_panels:
            add_row('Admin Panels', '', '', is_header=True, expanded=self.expanded_sections['admin_panels'])
            if self.expanded_sections['admin_panels']:
                add_row('', 'Candidates Found', len(results['Best Admin Panel Candidates']))
                for i, result in enumerate(results['Best Admin Panel Candidates'][:5], 1):
                    import re
                    ansi_escape = re.compile('\\x1B(?:[@-Z\\\\-_]|\\[[0-?]*[ -/]*[@-~])')
                    clean_status = ansi_escape.sub('', result['status_display'])
                    add_row('', f'Candidate {i}', f"{clean_status} - {result['url']}")
        has_mac_tests = 'MAC Login Tests' in results and results['MAC Login Tests']
        if has_mac_tests:
            add_row('MAC Authentication', '', '', is_header=True, expanded=self.expanded_sections['mac_auth'])
            if self.expanded_sections['mac_auth']:
                successful = sum((1 for status in results['MAC Login Tests'].values() if 'OK' in status or 'Authorized' in status))
                add_row('', 'Total Tests', len(results['MAC Login Tests']))
                add_row('', 'Successful Tests', successful)
                if len(results['MAC Login Tests']) > 0:
                    add_row('', 'Detailed Results', '')
                    for mac, status in list(results['MAC Login Tests'].items())[:10]:
                        status_icon = '✅' if 'OK' in status or 'Authorized' in status else '❌'
                        add_row('', f'  {status_icon} {mac}', status)
        has_fingerprinting = 'STB Fingerprinting' in results and results['STB Fingerprinting']
        if has_fingerprinting:
            add_row('STB Fingerprinting', '', '', is_header=True, expanded=self.expanded_sections['stb_fingerprinting'])
            if self.expanded_sections['stb_fingerprinting']:
                successful = len([r for r in results['STB Fingerprinting'] if 'OK' in r['status'] or 'Authorized' in r['status']])
                add_row('', 'Total Models Tested', len(results['STB Fingerprinting']))
                add_row('', 'Accepted Models', successful)
                if len(results['STB Fingerprinting']) > 0:
                    add_row('', 'Detailed Results', '')
                    for result in results['STB Fingerprinting'][:10]:
                        status_icon = '✅' if 'OK' in result['status'] or 'Authorized' in result['status'] else '❌'
                        add_row('', f"  {status_icon} {result['model']}", result['status'])

    def auto_save_results(self):
        """Auto-save all results to output folder with daily summary"""  # inserted
        if not self.analysis_results:
            return
        timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
        today_date = datetime.now().strftime('%d%m%Y')
        for result in self.analysis_results:
            if 'Error' not in result:
                portal_name = result.get('Portal', 'unknown_portal')
                safe_name = ''.join((c for c in portal_name if c.isalnum() or c in ['-', '_'])).rstrip()
                filename = save_summary(result, f'{safe_name}_{timestamp}')
                if filename:
                    self.log_message(f'💾 Results saved: {os.path.basename(filename)}')
        daily_summary_filename = os.path.join(OUTPUT_FOLDER, f'Daily_Analysis_Summary_{today_date}.txt')
        try:
            file_exists = os.path.exists(daily_summary_filename)
            with open(daily_summary_filename, 'a', encoding='utf-8') as f:
                if not file_exists:
                    f.write('🖤 ANGINA™ 🖤 Portal Detective Pro - DAILY ANALYSIS SUMMARY\n')
                    f.write('══════════════════════════════════════════════════════════\n')
                    f.write(f"📅 Date: {datetime.now().strftime('%d-%m-%Y')}\n")
                    f.write('────────────────────────────────────────────────────────────────────────────────\n\n')
                f.write(f"🕒 Analysis Session: {datetime.now().strftime('%H:%M:%S')}\n")
                f.write('──────────────────────────────────────────────────\n')
                f.write(f'📊 URLs Processed in this session: {len(self.analysis_results)}\n')
                online_count = sum((1 for r in self.analysis_results if r.get('Status') == '✅ Up '))
                error_count = sum((1 for r in self.analysis_results if 'Error' in r))
                offline_count = len(self.analysis_results) - online_count - error_count
                f.write(f'✅ Online: {online_count}\n')
                f.write(f'🔴 Offline: {offline_count}\n')
                f.write(f'❌ Errors: {error_count}\n\n')
                f.write('Session Results:\n')
                for i, result in enumerate(self.analysis_results, 1):
                    portal = result.get('Portal', 'Unknown')
                    status = result.get('Status', 'Unknown')
                    if 'Error' in result:
                        f.write(f"  {i}. ❌ {portal} - Error: {result['Error']}\n")
                    else:  # inserted
                        ip = result.get('IP Address', 'N/A')
                        stb_models = ', '.join(result.get('STB Models', [])) if result.get('STB Models') else 'Unknown'
                        f.write(f'  {i}. {status} {portal} | IP: {ip} | STB: {stb_models}\n')
                f.write('\n')
                f.write('────────────────────────────────────────────────────────────────────────────────\n\n')
            if file_exists:
                self.log_message(f'📊 Appended to daily summary: {os.path.basename(daily_summary_filename)}')
            else:  # inserted
                self.log_message(f'📊 Created daily summary: {os.path.basename(daily_summary_filename)}')
        except Exception as e:
            self.log_message(f'❌ Error saving daily summary: {e}', 'error')
        batch_filename = os.path.join(OUTPUT_FOLDER, f'Session_Summary_{timestamp}.txt')
        try:
            with open(batch_filename, 'w', encoding='utf-8') as f:
                f.write('🖤 ANGINA™ 🖤 Portal Detective Pro - Session Analysis Summary\n')
                f.write('══════════════════════════════════════════════════════════\n\n')
                f.write(f"📅 Session Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
                f.write(f'📊 Total URLs Processed: {len(self.analysis_results)}\n\n')
                online_count = sum((1 for r in self.analysis_results if r.get('Status') == '✅ Up '))
                error_count = sum((1 for r in self.analysis_results if 'Error' in r))
                offline_count = len(self.analysis_results) - online_count - error_count
                f.write(f'✅ Online: {online_count}\n')
                f.write(f'🔴 Offline: {offline_count}\n')
                f.write(f'❌ Errors: {error_count}\n\n')
                f.write('Detailed Results:\n')
                f.write('────────────────────────────────────────────────────────────────────────────────\n')
                for i, result in enumerate(self.analysis_results, 1):
                    portal = result.get('Portal', 'Unknown')
                    status = result.get('Status', 'Unknown')
                    if 'Error' in result:
                        f.write(f"{i}. ❌ {portal} - Error: {result['Error']}\n")
                    else:  # inserted
                        f.write(f'{i}. {status} {portal}\n')
            self.log_message(f'💾 Session summary saved: {os.path.basename(batch_filename)}')
        except Exception as e:
            self.log_message(f'❌ Error saving session summary: {e}', 'error')
        if self.enable_history.isChecked():
            self.save_to_history()

    def save_to_history(self):
        """Save current analysis results to history - FIXED to create proper portal history"""  # inserted
        try:
            history_file = os.path.join(HISTORY_FOLDER, f"portal_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            portal_history = []
            for result in self.analysis_results:
                if 'Error' not in result:
                    portal_entry = {'portal': result.get('Portal', 'Unknown'), 'timestamp': datetime.now().isoformat(), 'status': result.get('Status', 'Unknown'), 'ip': result.get('IP Address', 'Unknown'), 'stb_models': result.get('STB Models', [])}
                    portal_history.append(portal_entry)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(portal_history, f, indent=2)
            self.log_message(f'📚 Portal URLs saved to history: {os.path.basename(history_file)}')
            detailed_history_file = os.path.join(HISTORY_FOLDER, f"detailed_history_{datetime.now().strftime('%d-%m-%Y')}.json")
            detailed_history_data = []
            if os.path.exists(detailed_history_file):
                try:
                    with open(detailed_history_file, 'r', encoding='utf-8') as f:
                        detailed_history_data = json.load(f)
                except Exception as e:
                    self.log_message(f'⚠️ Error reading detailed history file: {e}', 'warning')
                    detailed_history_data = []
        for result in self.analysis_results:
            if 'Error' not in result:
                history_entry = {'timestamp': datetime.now().isoformat(), 'portal': result.get('Portal', 'Unknown'), 'ip': result.get('IP Address', 'Unknown'), 'status': result.get('Status', 'Unknown'), 'stb_models': result.get('STB Models', []), 'admin_panels_found': len(result.get('Best Admin Panel Candidates', [])), 'similar_portals_found': len(result.get('Similar Portals', [])), 'analysis_data': result}
                detailed_history_data.append(history_entry)
        with open(detailed_history_file, 'w', encoding='utf-8') as f:
            json.dump(detailed_history_data, f, indent=2)
        self.log_message(f'📊 Detailed analysis saved to history: {os.path.basename(detailed_history_file)}')
        except Exception as e:
            self.log_message(f'❌ Error saving to history: {e}', 'error')

    def save_results(self):
        """Manual save results"""  # inserted
        if not self.analysis_results:
            QMessageBox.warning(self, 'Warning', 'No analysis results to save')
            return
        self.auto_save_results()
        QMessageBox.information(self, 'Save Successful', f'Results saved to:\n{OUTPUT_FOLDER}')

    def show_history_statistics(self):
        """Show statistics from history files"""  # inserted
        try:
            files = [f for f in os.listdir(HISTORY_FOLDER) if f.startswith('detailed_history_') and f.endswith('.json')]
            if not files:
                QMessageBox.information(self, 'No History', 'No history files found.')
                return
            filename, _ = QFileDialog.getOpenFileName(self, 'Select History File', HISTORY_FOLDER, 'History Files (*.json)')
            if not filename:
                return
            with open(filename, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            total_analyses = len(history_data)
            total_portals = len(set((entry.get('portal') for entry in history_data)))
            stats_dialog = QDialog(self)
            stats_dialog.setWindowTitle('📊 History Statistics')
            stats_dialog.setGeometry(200, 200, 600, 400)
            stats_dialog.setStyleSheet(DARK_THEME)
            layout = QVBoxLayout(stats_dialog)
            file_info = QLabel(f'History File: {os.path.basename(filename)}')
            file_info.setStyleSheet('font-weight: bold; color: #4FC3F7;')
            layout.addWidget(file_info)
            stats_group = QGroupBox('📈 Analysis Statistics')
            stats_layout = QVBoxLayout(stats_group)
            stats_text = QTextEdit()
            stats_text.setReadOnly(True)
            stats_text.append(f'Total analyses: {total_analyses}')
            stats_text.append(f'Unique portals analyzed: {total_portals}')
            if history_data:
                stats_text.append(f"History period: {history_data[0]['timestamp'][:10]} to {history_data[(-1)]['timestamp'][:10]}")
            stats_layout.addWidget(stats_text)
            layout.addWidget(stats_group)
            close_btn = QPushButton('Close')
            close_btn.clicked.connect(stats_dialog.close)
            layout.addWidget(close_btn)
            stats_dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load history statistics:\n{e}')

    def log_message(self, message, level='info'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        if level == 'error':
            formatted_message = f'[{timestamp}] ❌ {message}'
            color = '#FF6B6B'
        else:  # inserted
            if level == 'warning':
                formatted_message = f'[{timestamp}] ⚠️ {message}'
                color = '#FFA726'
            else:  # inserted
                formatted_message = f'[{timestamp}] ℹ️ {message}'
                color = '#4FC3F7'
        self.log_text.append(f'<span style=\"color: {color}\">{formatted_message}</span>')
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)

    def closeEvent(self, event):
        if self.analysis_thread and self.analysis_thread.isRunning():
            self.analysis_thread.stop()
            self.analysis_thread.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = PortalDetectivePro()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()