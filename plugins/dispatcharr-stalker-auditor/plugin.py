import os
import sys
import time
import socket
import random
import json
import csv
import logging
import re
import ssl
import urllib3
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

# Constants
COMMON_PORTS = [80, 443, 8080, 8880, 25461, 2052, 2082, 2086, 2095, 8443, 8844, 8888, 9000, 9600]
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3'
]
ADMIN_USER_AGENTS = [
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Safari/537.36',
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/537.36',
    'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/537.36 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 2721 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; CloudFlare-AlwaysOnline/1.0; +https://www.cloudflare.com/always-online) AppleWebKit/534.34'
]
COMMON_SUBDOMAINS = ['www', 'api', 'portal', 'stream', 'tv', 'iptv', 'live', 'm', 'secure', 'admin', 'login', 'panel', 'cdn', 'video', 'play']
ADMIN_PAYLOADS = ['/c/', '/portal.php', '/server/load.php', '/portalstb/', '/stalker_portal/server/load.php', '/portal.php/c/', '/stalker_portal', '/admin/', '/panel/', '/login/', '/manager/', '/web/', '/xc/', '/xtream/']
STB_MODELS_LIST = ['MAG250', 'MAG254', 'MAG256', 'MAG322', 'MAG324', 'MAG349', 'MAG351', 'MAG420', 'MAG520', 'Formuler Z8', 'DreamBox']

# Geolocation Service with Multi-Fallback
class IPGeolocationService:
    def __init__(self):
        self.services = [self._ipapi_service, self._ipwhois_service, self._ipapi_com_service]

    def get_ip_info(self, host_with_port, proxies=None):
        """Get IP address and geolocation information with multiple fallbacks"""
        host = host_with_port.split(':')[0]
        ip = self._resolve_ip(host, proxies)
        if ip == 'Unknown':
            return 'Unknown', 'Unknown', 'Unknown', 'Unknown'
        
        for service in self.services:
            try:
                country, isp, org = service(ip, proxies)
                if country != 'Unknown':
                    flag = self._get_country_flag(country)
                    return ip, f"{country} {flag}".strip(), isp, org
            except Exception:
                continue
        return ip, 'Unknown', 'Unknown', 'Unknown'

    def _resolve_ip(self, host, proxies=None):
        """Resolve hostname to IP address, optionally using DoH over proxy"""
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            pass
        
        # Fallback using DNS-over-HTTPS via dns.google over proxy
        try:
            url = f"https://dns.google/resolve?name={host}&type=A"
            resp = requests.get(url, proxies=proxies, timeout=5, verify=False)
            data = resp.json()
            if 'Answer' in data:
                return data['Answer'][0]['data']
        except Exception:
            pass
        return 'Unknown'

    def _ipapi_service(self, ip, proxies=None):
        try:
            resp = requests.get(f'http://ip-api.com/json/{ip}?fields=country,countryCode,isp,org', proxies=proxies, timeout=3)
            data = resp.json()
            if data.get('status') == 'success':
                return data.get('country', 'Unknown'), data.get('isp', 'Unknown'), data.get('org', 'Unknown')
        except Exception:
            pass
        return 'Unknown', 'Unknown', 'Unknown'

    def _ipwhois_service(self, ip, proxies=None):
        try:
            resp = requests.get(f'http://ipwhois.app/json/{ip}', proxies=proxies, timeout=3)
            data = resp.json()
            if data.get('success', False):
                return data.get('country', 'Unknown'), data.get('isp', 'Unknown'), data.get('org', 'Unknown')
        except Exception:
            pass
        return 'Unknown', 'Unknown', 'Unknown'

    def _ipapi_com_service(self, ip, proxies=None):
        try:
            # Fallback free tier endpoint
            resp = requests.get(f'http://ip-api.com/json/{ip}', proxies=proxies, timeout=3)
            data = resp.json()
            if data.get('status') == 'success':
                return data.get('country', 'Unknown'), data.get('isp', 'Unknown'), data.get('org', 'Unknown')
        except Exception:
            pass
        return 'Unknown', 'Unknown', 'Unknown'

    def _get_country_flag(self, country_name):
        country_codes = {
            'United States': 'US', 'United Kingdom': 'GB', 'Canada': 'CA', 'Australia': 'AU', 
            'Germany': 'DE', 'France': 'FR', 'Italy': 'IT', 'Spain': 'ES', 'Netherlands': 'NL', 
            'Belgium': 'BE', 'Switzerland': 'CH', 'Austria': 'AT', 'Sweden': 'SE', 'Norway': 'NO', 
            'Denmark': 'DK', 'Finland': 'FI', 'Ireland': 'IE', 'Portugal': 'PT', 'Poland': 'PL', 
            'Czech Republic': 'CZ', 'Hungary': 'HU', 'Greece': 'GR', 'Romania': 'RO', 'Bulgaria': 'BG', 
            'Croatia': 'HR', 'Serbia': 'RS', 'Slovakia': 'SK', 'Slovenia': 'SI', 'Ukraine': 'UA', 
            'Russia': 'RU', 'Turkey': 'TR', 'Brazil': 'BR', 'Argentina': 'AR', 'Mexico': 'MX', 
            'India': 'IN', 'China': 'CN', 'Japan': 'JP', 'South Korea': 'KR', 'South Africa': 'ZA'
        }
        code = country_codes.get(country_name, country_name)
        if len(code) == 2:
            return ''.join((chr(ord(c) + 127397) for c in code.upper()))
        return ''

geo_service = IPGeolocationService()

# Plugin Implementation
class Plugin:
    name = "Stalker Portal Auditor & Checker"
    version = "1.0.0"
    description = "Sicherheits-Audits & Bulk-Online-Statusprüfungen für Stalker IPTV Portale. Unterstützt SOCKS4/5 & VPN Proxy-Routing."
    author = "Antigravity"

    fields = []
    actions = []

    def __init__(self):
        self.reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def run(self, action: str, params: dict, context: dict):
        settings = context.get("settings", {})
        plugin_logger = context.get("logger", logger)

        if action == "import_and_test_proxies":
            return self._execute_import_and_test_proxies(settings, plugin_logger)

        # Parse Proxy
        proxy_use_rotation = bool(settings.get("proxy_use_rotation", False))
        active_proxies = self._load_active_proxies() if proxy_use_rotation else []
        
        proxies = None
        if active_proxies:
            chosen = random.choice(active_proxies)
            proxies = {
                "http": chosen,
                "https": chosen
            }
            plugin_logger.info(f"Proxy Rotation active. Loaded {len(active_proxies)} active proxies. Chosen for init: {chosen}")
        else:
            proxy_url = settings.get("proxy", "").strip()
            if proxy_url:
                proxies = {
                    "http": proxy_url,
                    "https": proxy_url
                }
                plugin_logger.info(f"Using manual proxy routing: {proxy_url}")

        if action == "run_status_check":
            return self._execute_bulk_status_check(settings, proxies, plugin_logger)
        elif action == "run_audit":
            return self._execute_deep_portal_audit(settings, proxies, plugin_logger)

        return {"status": "error", "message": f"Unknown action: {action}"}

    # ----------------------------------------------------------------------
    # ACTION: Bulk Status Checker
    # ----------------------------------------------------------------------
    def _execute_bulk_status_check(self, settings, proxies, plugin_logger):
        raw_urls = settings.get("bulk_urls", "").strip()
        if not raw_urls:
            return {"status": "error", "message": "Keine URLs im Bulk-Check Feld angegeben."}

        # Clean URLs
        urls = re.split(r'[\s,;\n\r]+', raw_urls)
        urls = list(dict.fromkeys([u.strip() for u in urls if u.strip()]))
        if not urls:
            return {"status": "error", "message": "Keine gültigen URLs gefunden."}

        max_workers = min(int(settings.get("max_workers", 15)), 50)
        plugin_logger.info(f"Starting bulk status check on {len(urls)} portals with {max_workers} workers.")

        results = []
        online_count = 0
        offline_count = 0
        
        active_proxies = self._load_active_proxies() if bool(settings.get("proxy_use_rotation", False)) else []

        def check_single_url(url):
            clean_url = url if url.startswith(('http://', 'https://')) else 'http://' + url
            parsed = urlparse(clean_url)
            host = parsed.netloc
            
            # Select proxy for this thread/URL
            local_proxies = proxies
            if active_proxies:
                chosen = random.choice(active_proxies)
                local_proxies = {"http": chosen, "https": chosen}
            
            status = "Offline"
            status_code = None
            response_time = None
            
            start_time = time.time()
            try:
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                resp = requests.get(clean_url, headers=headers, proxies=local_proxies, timeout=8, verify=False, allow_redirects=True)
                response_time = round((time.time() - start_time) * 1000, 2)
                status_code = resp.status_code
                if resp.status_code == 200:
                    status = "Online"
                else:
                    status = f"HTTP {resp.status_code}"
            except requests.exceptions.Timeout:
                status = "Timeout"
            except requests.exceptions.ConnectionError:
                status = "Connection Error"
            except Exception as e:
                status = f"Error: {str(e)[:40]}"

            ip, country, isp, org = geo_service.get_ip_info(host, proxies=local_proxies)
            is_online = (status == "Online")
            
            return {
                "url": url,
                "status": status,
                "status_code": status_code,
                "response_time": response_time,
                "ip": ip,
                "country": country,
                "isp": isp,
                "org": org,
                "is_online": is_online,
                "timestamp": datetime.now().isoformat()
            }

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(check_single_url, url): url for url in urls}
            for future in as_completed(future_to_url):
                try:
                    res = future.result()
                    results.append(res)
                    if res["is_online"]:
                        online_count += 1
                    else:
                        offline_count += 1
                except Exception as e:
                    plugin_logger.error(f"Error checking portal: {e}")

        # Sort results
        results.sort(key=lambda x: x["url"])

        # Save Report Files
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file_txt = os.path.join(self.reports_dir, f"Bulk_Check_{timestamp}.txt")
        report_file_json = os.path.join(self.reports_dir, f"Bulk_Check_{timestamp}.json")

        # Save TXT Report
        with open(report_file_txt, 'w', encoding='utf-8') as f:
            f.write(f"Stalker Bulk Status Check Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n")
            f.write(f"Gesamt: {len(urls)} | Online: {online_count} | Offline: {offline_count}\n")
            f.write("="*80 + "\n\n")
            for r in results:
                time_str = f"{r['response_time']} ms" if r['response_time'] else "N/A"
                f.write(f"[{'ONLINE' if r['is_online'] else 'OFFLINE'}] {r['url']}\n")
                f.write(f"  ├─ Status: {r['status']}\n")
                f.write(f"  ├─ IP: {r['ip']} | ISP: {r['isp']}\n")
                f.write(f"  ├─ Land: {r['country']}\n")
                f.write(f"  └─ Latenz: {time_str}\n\n")

        # Save JSON Report
        with open(report_file_json, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": {"total": len(urls), "online": online_count, "offline": offline_count},
                "results": results
            }, f, indent=2)

        return {
            "status": "ok",
            "message": f"Scan abgeschlossen. {online_count} von {len(urls)} Portalen sind online.",
            "report_file": report_file_txt,
            "summary": {
                "total": len(urls),
                "online": online_count,
                "offline": offline_count,
                "success_rate": f"{round((online_count/len(urls))*100, 2) if urls else 0}%"
            },
            "results": results[:50] # Send first 50 results to the frontend
        }

    # ----------------------------------------------------------------------
    # ACTION: Deep Portal Audit
    # ----------------------------------------------------------------------
    def _execute_deep_portal_audit(self, settings, proxies, plugin_logger):
        url = settings.get("single_url", "").strip()
        if not url:
            return {"status": "error", "message": "Keine URL im Tiefen-Audit Feld angegeben."}

        clean_url = url if url.startswith(('http://', 'https://')) else 'http://' + url
        parsed = urlparse(clean_url)
        hostname = parsed.hostname
        if not hostname:
            return {"status": "error", "message": "Geklonte URL hat keinen gültigen Hostnamen."}

        plugin_logger.info(f"Starting deep portal audit on: {clean_url}")

        audit_data = {
            "Portal": clean_url,
            "IP Address": "N/A",
            "Country": "N/A",
            "ISP": "N/A",
            "Org": "N/A",
            "Reverse DNS": "Not available",
            "SSL Valid": "N/A",
            "Status": "🔴 Down",
            "Status Code": "N/A",
            "Response Time (ms)": "N/A",
            "HTTP Headers": {},
            "Protections Detected": [],
            "Open Ports": {},
            "Subdomains Found": [],
            "Similar Portals": [],
            "Admin Panel Results": [],
            "Best Admin Panel Candidates": [],
            "MAC Login Tests": {},
            "STB Fingerprinting": [],
            "Extracted Accounts": {}
        }

        max_workers = min(int(settings.get("max_workers", 15)), 50)

        # 1. Resolve IP and Geolocation
        ip, country, isp, org = geo_service.get_ip_info(hostname, proxies=proxies)
        audit_data["IP Address"] = ip
        audit_data["Country"] = country
        audit_data["ISP"] = isp
        audit_data["Org"] = org
        
        if ip != "Unknown":
            try:
                hostname_lookup, _, _ = socket.gethostbyaddr(ip)
                audit_data["Reverse DNS"] = hostname_lookup
            except Exception:
                pass

        # 2. Portal Status & SSL
        try:
            start_time = time.time()
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            resp = requests.get(clean_url, headers=headers, proxies=proxies, timeout=10, verify=False)
            response_time = round((time.time() - start_time) * 1000, 2)
            audit_data["Response Time (ms)"] = response_time
            audit_data["Status Code"] = resp.status_code
            if resp.status_code < 400:
                audit_data["Status"] = "✅ Up"
            else:
                audit_data["Status"] = f"🔴 HTTP {resp.status_code}"
        except Exception as e:
            audit_data["Status"] = f"🔴 Down (Error: {str(e)[:40]})"

        # SSL Check
        if clean_url.startswith("https://"):
            try:
                ctx = ssl.create_default_context()
                port = parsed.port or 443
                with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
                    s.settimeout(5)
                    s.connect((hostname, port))
                audit_data["SSL Valid"] = "✅ Valid"
            except Exception:
                audit_data["SSL Valid"] = "❌ Invalid/Error"
        else:
            audit_data["SSL Valid"] = "⚠️ HTTP (Kein SSL)"

        # 3. HTTP Header Analysis & Protection Detection
        try:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            resp = requests.get(clean_url, headers=headers, proxies=proxies, timeout=10, verify=False)
            audit_data["HTTP Headers"] = {
                "Server": resp.headers.get("Server", "Unknown"),
                "X-Powered-By": resp.headers.get("X-Powered-By", "Unknown"),
                "All": dict(resp.headers)
            }
            
            # Detect Cloudflare / DDoS protections
            protections = {
                'Cloudflare': ['cf-ray', 'cloudflare', '__cfduid', '__cf_bm'],
                'DDoS-Guard': ['ddos-guard'],
                'Sucuri': ['sucuri'],
                'Akamai': ['akamai', 'akamaiedge'],
                'Incapsula': ['incapsula', 'visid_incap']
            }
            headers_lower = {k.lower(): str(v).lower() for k, v in resp.headers.items()}
            cookies_lower = [c.lower() for c in resp.cookies.keys()] if resp.cookies else []
            body_lower = resp.text.lower()
            
            for prot, signs in protections.items():
                for sign in signs:
                    if any(sign in h for h in headers_lower.values()) or sign in str(cookies_lower) or sign in body_lower:
                        audit_data["Protections Detected"].append(prot)
                        break
        except Exception:
            pass

        # 4. Open Ports Scan
        if settings.get("enable_ports", True) and ip != "Unknown":
            def scan_port(port):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(2)
                        result = s.connect_ex((ip, port))
                        if result == 0:
                            # Try to read banner
                            try:
                                req = f"HEAD / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
                                s.send(req.encode())
                                banner = s.recv(256).decode(errors='ignore').split('\n')[0].strip()
                                return port, banner if banner else "open"
                            except Exception:
                                return port, "open"
                except Exception:
                    pass
                return port, None

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(scan_port, p): p for p in COMMON_PORTS}
                for future in as_completed(futures):
                    p, status = future.result()
                    if status:
                        audit_data["Open Ports"][p] = status

        # 5. Subdomain Enumeration
        if settings.get("enable_subdomains", True):
            domain_parts = hostname.split('.')
            domain = '.'.join(domain_parts[-2:]) if len(domain_parts) >= 2 else hostname
            
            def check_subdomain(sub):
                try:
                    sub_host = f"{sub}.{domain}"
                    sub_ip = socket.gethostbyname(sub_host)
                    return sub_host, sub_ip
                except Exception:
                    return None

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(check_subdomain, sub): sub for sub in COMMON_SUBDOMAINS}
                for future in as_completed(futures):
                    res = future.result()
                    if res:
                        audit_data["Subdomains Found"].append(res)

        # 6. Admin Panel Discovery
        if settings.get("enable_admin_discovery", True):
            def check_admin_payload(payload):
                target_path = clean_url.rstrip('/') + payload
                try:
                    headers = {"User-Agent": random.choice(ADMIN_USER_AGENTS)}
                    r = requests.get(target_path, headers=headers, proxies=proxies, timeout=5, verify=False, allow_redirects=True)
                    # Safe check for portal status code
                    status_display = f"HTTP {r.status_code}"
                    if r.status_code in [200, 403, 444]:
                        status_display = "[ 200 ] OK / Accessible"
                    
                    return {
                        "url": target_path,
                        "status_code": r.status_code,
                        "length": len(r.text),
                        "status_display": status_display
                    }
                except Exception as e:
                    return {
                        "url": target_path,
                        "status_code": "Error",
                        "length": 0,
                        "status_display": f"[ Error ] {str(e)[:30]}"
                    }

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(check_admin_payload, pl): pl for pl in ADMIN_PAYLOADS}
                for future in as_completed(futures):
                    res = future.result()
                    audit_data["Admin Panel Results"].append(res)
                    if "[ 200 ]" in res["status_display"]:
                        audit_data["Best Admin Panel Candidates"].append(res)

        # 7. STB Fingerprinting & MAC authentication test
        macs_str = settings.get("custom_macs", "").strip()
        custom_macs = [m.strip() for m in macs_str.split(',') if m.strip()]
        if not custom_macs:
            custom_macs = ["00:1A:79:33:44:CF"] # Default fallback test MAC

        if settings.get("enable_stb_fingerprinting", True):
            # Test how different models react with a custom MAC
            def test_mac_stb(model, mac):
                headers = {
                    'User-Agent': f'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) {model} stbapp ver: 2 rev: 250 Safari/533.3',
                    'X-User-Agent': f'Model: {model}; Link: WiFi',
                    'Authorization': f'MAC {mac}'
                }
                
                # Normalize stalker portal authentication path
                auth_url = clean_url.rstrip('/') + '/c/'
                try:
                    r = requests.get(auth_url, headers=headers, proxies=proxies, timeout=6, verify=False)
                    resp_text = r.text.lower()
                    
                    status = f"HTTP {r.status_code}"
                    is_authorized = False
                    
                    if r.status_code == 200:
                        if 'not authorized' in resp_text:
                            status = "❌ Denied (Unauthorized)"
                        elif 'ok' in resp_text or 'true' in resp_text or 'js' in resp_text:
                            status = "✅ OK (Authorized)"
                            is_authorized = True
                        else:
                            status = "⚠️  200 OK (Unknown Response)"
                    elif r.status_code == 403:
                        status = "🚫 403 Forbidden"
                    
                    return {
                        "model": model,
                        "mac": mac,
                        "status": status,
                        "is_authorized": is_authorized
                    }
                except Exception as e:
                    return {
                        "model": model,
                        "mac": mac,
                        "status": f"💥 Error: {str(e)[:30]}",
                        "is_authorized": False
                    }

            for mac in custom_macs:
                audit_data["MAC Login Tests"][mac] = []
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = {executor.submit(test_mac_stb, model, mac): model for model in STB_MODELS_LIST}
                    for future in as_completed(futures):
                        res = future.result()
                        audit_data["STB Fingerprinting"].append(res)
                        audit_data["MAC Login Tests"][mac].append(f"{res['model']}: {res['status']}")
                
                # Perform deep account/channel extraction for this MAC if authorized
                is_authorized_any = any(r["mac"] == mac and r["is_authorized"] for r in audit_data["STB Fingerprinting"])
                if is_authorized_any:
                    plugin_logger.info(f"Extracting deep account details for MAC: {mac}")
                    details = self._deep_stalker_account_audit(clean_url, mac, proxies, plugin_logger)
                    if details:
                        audit_data["Extracted Accounts"][mac] = details

        # 8. urlscan.io Integration
        urlscan_api_key = settings.get("urlscan_api_key", "").strip()
        # Fallback to integrated key if empty
        if not urlscan_api_key:
            urlscan_api_key = "01990b54-2cad-730c-8107-fa36271e7a4c"

        if settings.get("enable_similar_portals", True) and ip != "Unknown":
            # Search by IP
            try:
                headers = {'API-Key': urlscan_api_key, 'Content-Type': 'application/json'}
                search_url = f"https://urlscan.io/api/v1/search/?q=page.ip:{ip}&size=50"
                resp = requests.get(search_url, headers=headers, proxies=proxies, timeout=10, verify=False)
                if resp.status_code == 200:
                    results = resp.json().get('results', [])
                    seen_urls = set()
                    for item in results:
                        p_url = item.get('page', {}).get('url')
                        if p_url:
                            norm = p_url.lower().replace('https://', '').replace('http://', '').replace('www.', '').rstrip('/')
                            if norm not in seen_urls:
                                seen_urls.add(norm)
                                audit_data["Similar Portals"].append(p_url)
            except Exception as e:
                plugin_logger.warning(f"urlscan.io scan failed: {e}")

        # Save Beautiful Audit Report (TXT & JSON)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_host = "".join(c for c in hostname if c.isalnum() or c in ['-', '_'])
        report_file_txt = os.path.join(self.reports_dir, f"Portal_Audit_{safe_host}_{timestamp}.txt")
        report_file_json = os.path.join(self.reports_dir, f"Portal_Audit_{safe_host}_{timestamp}.json")

        # Write TXT Report (ASCII Layout)
        with open(report_file_txt, 'w', encoding='utf-8') as f:
            f.write("╔" + "═"*78 + "╗\n")
            f.write("║" + " "*20 + "🕵  PORTAL DETECTIVE & AUDITOR REPORT  🕵" + " "*19 + "║\n")
            f.write("║" + " "*23 + "🌐 Advanced Stalker Intelligence 🌐" + " "*20 + "║\n")
            f.write("╚" + "═"*78 + "╝\n\n")
            f.write(f"📅 Audit-Zeitpunkt: {datetime.now().strftime('%B %d, %Y - %I:%M %p')}\n")
            f.write("─"*80 + "\n\n")
            
            f.write("🔰 BASICS:\n")
            f.write(f"   📍 Portal URL: {audit_data['Portal']}\n")
            f.write(f"   📊 Status:     {audit_data['Status']}\n")
            f.write(f"   📟 Status-Code: {audit_data['Status Code']}\n")
            f.write(f"   ⏱️  Latenz:      {audit_data['Response Time (ms)']} ms\n")
            f.write(f"   🔒 SSL-Valid:   {audit_data['SSL Valid']}\n")
            f.write(f"   🌐 IP-Adresse:  {audit_data['IP Address']}\n")
            f.write(f"   🔁 Reverse DNS: {audit_data['Reverse DNS']}\n\n")

            f.write("🌍 GEOLOKALISIERUNG:\n")
            f.write(f"   Country: {audit_data['Country']}\n")
            f.write(f"   ISP:     {audit_data['ISP']}\n")
            f.write(f"   Org:     {audit_data['Org']}\n\n")

            if audit_data["Protections Detected"]:
                f.write("🛡️  SICHERHEITSSCHILD / CDN DETEKTIERT:\n")
                for prot in audit_data["Protections Detected"]:
                    f.write(f"   • {prot}\n")
                f.write("\n")

            f.write("📋 SERVER HEADERS:\n")
            f.write(f"   Server:       {audit_data['HTTP Headers'].get('Server', 'Unknown')}\n")
            f.write(f"   X-Powered-By: {audit_data['HTTP Headers'].get('X-Powered-By', 'Unknown')}\n\n")

            if audit_data["Open Ports"]:
                f.write("🚪 OFFENE PORTS:\n")
                for port, status in audit_data["Open Ports"].items():
                    f.write(f"   Port {port:5d} ─ {status}\n")
                f.write("\n")

            if audit_data["Subdomains Found"]:
                f.write(f"🌐 ENTDECKTE SUBDOMAINS ({len(audit_data['Subdomains Found'])}):\n")
                for sub, sub_ip in audit_data["Subdomains Found"]:
                    f.write(f"   • {sub} ─ {sub_ip}\n")
                f.write("\n")

            if audit_data["Best Admin Panel Candidates"]:
                f.write("🔐 ADMIN PANELS & PFADE:\n")
                for admin in audit_data["Best Admin Panel Candidates"]:
                    f.write(f"   • {admin['status_display']} ─ {admin['url']} (Länge: {admin['length']} Bytes)\n")
                f.write("\n")

            if audit_data.get("Extracted Accounts"):
                f.write("🔑 EXTRAHIERTE ACCOUNT-DETAILS (DEEP AUDIT):\n")
                for mac, details in audit_data["Extracted Accounts"].items():
                    f.write(f"   MAC: {mac}\n")
                    f.write(f"     ├─ Status:         {details.get('Status', 'N/A')}\n")
                    f.write(f"     ├─ Ablaufdatum:    {details.get('Expiry', 'N/A')}\n")
                    f.write(f"     ├─ Live-TV-Kanäle: {details.get('Live TV Channels', 0)}\n")
                    f.write(f"     └─ VOD-Kategorien: {details.get('VOD Categories', 0)}\n")
                f.write("\n")

            if audit_data["STB Fingerprinting"]:
                f.write("🔬 STB KOMPATIBILITÄTS-TESTS (FINGERPRINTING):\n")
                for mac, results in audit_data["MAC Login Tests"].items():
                    f.write(f"   MAC: {mac}:\n")
                    for r in results:
                        f.write(f"     ├─ {r}\n")
                    f.write("\n")

            if audit_data["Similar Portals"]:
                f.write(f"🔗 ÄHNLICHE PORTALE AUF DERSELBEN IP ({len(audit_data['Similar Portals'])}):\n")
                for sim in audit_data["Similar Portals"]:
                    f.write(f"   • {sim}\n")
                f.write("\n")
                
            f.write("─"*80 + "\n")
            f.write("📋 Ende des Berichts\n")

        # Write JSON Report
        with open(report_file_json, 'w', encoding='utf-8') as f:
            json.dump(audit_data, f, indent=2)

        # Condense results summary
        safe_headers = {k: str(v) for k, v in audit_data["HTTP Headers"].items() if k != "All"}
        summary_msg = f"Audit für {hostname} abgeschlossen. "
        if audit_data["Best Admin Panel Candidates"]:
            summary_msg += f"{len(audit_data['Best Admin Panel Candidates'])} Admin-Pfade gefunden! "
        if any("Authorized" in str(r) for r in audit_data["STB Fingerprinting"]):
            summary_msg += "Kompatible MAC-Anmeldung erkannt!"

        return {
            "status": "ok",
            "message": summary_msg,
            "report_file": report_file_txt,
            "basics": {
                "url": audit_data["Portal"],
                "status": audit_data["Status"],
                "ip": audit_data["IP Address"],
                "country": audit_data["Country"],
                "isp": audit_data["ISP"],
                "ssl": audit_data["SSL Valid"]
            },
            "open_ports": audit_data["Open Ports"],
            "subdomains": len(audit_data["Subdomains Found"]),
            "admin_panels": len(audit_data["Best Admin Panel Candidates"]),
            "fingerprints": [r for r in audit_data["STB Fingerprinting"] if "OK" in r["status"] or "Authorized" in r["status"]],
            "extracted_accounts": audit_data.get("Extracted Accounts", {})
        }

    # ----------------------------------------------------------------------
    # Helper: Expiry Date Detector for Stalker JSON responses
    # ----------------------------------------------------------------------
    def _detect_expiry(self, data, depth=0):
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
        for sub in ["account_info", "stb_account", "active_sub", "billing", "profile", "payment", "tariff", "subscription", "services"]:
            sub_data = data.get(sub)
            if isinstance(sub_data, dict):
                res = self._detect_expiry(sub_data, depth + 1)
                if res:
                    return res
            elif isinstance(sub_data, list) and len(sub_data) > 0:
                for item in sub_data:
                    if isinstance(item, dict):
                        res = self._detect_expiry(item, depth + 1)
                        if res:
                            return res
        return None

    # ----------------------------------------------------------------------
    # Helper: Deep Handshake & Account / Channels Metadata Audit
    # ----------------------------------------------------------------------
    def _deep_stalker_account_audit(self, clean_url, mac, proxies, plugin_logger):
        base_url = clean_url.rstrip("/")
        headers = {
            "User-Agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 2 rev: 250 Safari/533.3",
            "X-User-Agent": "model=MAG250;version=218;sig=6fb2447331356ecca928394477c0500e2630cc3c",
            "Cookie": f"mac={mac.upper()}",
            "Accept": "*/*",
        }
        token = None
        active_path = None
        paths_to_try = [
            f"{base_url}/server/load.php",
            f"{base_url}/portal.php",
            base_url if base_url.endswith(".php") else f"{base_url}/",
        ]
        
        def do_request(params, path):
            try:
                full_params = {"JsHttpRequest": "1-xml", **params}
                req_headers = headers.copy()
                if token:
                    req_headers["Authorization"] = f"Bearer {token}"
                r = requests.get(path, params=full_params, headers=req_headers, proxies=proxies, timeout=10, verify=False)
                if r.status_code == 404:
                    return 404
                data = r.json()
                if isinstance(data, dict):
                    if "js" in data:
                        data = data["js"]
                    if isinstance(data, dict) and "result" in data:
                        if isinstance(data["result"], (dict, list)):
                            data = data["result"]
                return data
            except Exception:
                return None

        # 1. Handshake
        for path in paths_to_try:
            res = do_request({"type": "stb", "action": "handshake"}, path)
            if res == 404:
                continue
            if res and isinstance(res, (dict, str)):
                if isinstance(res, dict):
                    token = res.get("token")
                else:
                    token = res
                if token:
                    active_path = path
                    break
        
        if not token or not active_path:
            return None
            
        # 2. Get Profile & Account Info
        profile = do_request({
            "type": "stb",
            "action": "get_profile",
            "stb_type": "MAG250",
            "sn": "1234567890123"
        }, active_path)
        
        acc_info = do_request({
            "type": "stb",
            "action": "get_account_info"
        }, active_path)
        
        # 3. Get Expiry Date
        expiry = self._detect_expiry(profile) or self._detect_expiry(acc_info) or "Unlimited"
        
        status = "Unknown"
        if profile and isinstance(profile, dict):
            status = str(profile.get("status", "Active"))
            if status == "1" or status == "0":
                status = "Active"
                
        # 4. Get Live Channels
        channels_data = do_request({
            "type": "itv",
            "action": "get_all_channels"
        }, active_path)
        
        channel_count = 0
        if channels_data:
            if isinstance(channels_data, dict) and "data" in channels_data:
                channel_count = len(channels_data["data"])
            elif isinstance(channels_data, list):
                channel_count = len(channels_data)
                
        # 5. Get VOD Movie Categories Count
        vod_data = do_request({
            "type": "vod",
            "action": "get_categories"
        }, active_path)
        
        vod_count = 0
        if vod_data:
            if isinstance(vod_data, list):
                vod_count = len(vod_data)
                
        return {
            "Status": status,
            "Expiry": expiry,
            "Live TV Channels": channel_count,
            "VOD Categories": vod_count
        }

    # ----------------------------------------------------------------------
    # Helper: Load Active Proxies
    # ----------------------------------------------------------------------
    def _load_active_proxies(self):
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        active_file = os.path.join(data_dir, "active_proxies.json")
        if os.path.exists(active_file):
            try:
                with open(active_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    # ----------------------------------------------------------------------
    # ACTION: Import and Test Proxies
    # ----------------------------------------------------------------------
    def _execute_import_and_test_proxies(self, settings, plugin_logger):
        from django.conf import settings as django_settings
        from pathlib import Path
        
        import_url = settings.get("proxy_import_url", "").strip()
        import_file = settings.get("proxy_import_file", "").strip()
        
        if not import_url and not import_file:
            return {
                "status": "error",
                "message": "Bitte geben Sie unter 'Proxy GitHub/Web-URL' oder 'Proxy Lokale Datei' eine Quelle an."
            }
            
        timeout = float(settings.get("proxy_test_timeout", 4))
        max_workers = min(int(settings.get("max_workers", 15)), 50)
        
        raw_proxies = set()
        
        # 1. Import from URL
        if import_url:
            plugin_logger.info(f"Proxies: Importiere von URL '{import_url}'...")
            try:
                r = requests.get(import_url, timeout=12, verify=False)
                if r.status_code == 200:
                    for line in r.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith('#'):
                            raw_proxies.add(line)
                else:
                    plugin_logger.warning(f"Proxies: URL-Import fehlgeschlagen mit HTTP {r.status_code}")
            except Exception as e:
                plugin_logger.error(f"Proxies: URL-Import fehlgeschlagen: {e}")
                
        # 2. Import from File
        if import_file:
            base_dir = Path(django_settings.BASE_DIR)
            filepath = base_dir / import_file
            plugin_logger.info(f"Proxies: Importiere von lokaler Datei '{filepath}'...")
            if filepath.exists():
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                raw_proxies.add(line)
                except Exception as e:
                    plugin_logger.error(f"Proxies: Datei-Import fehlgeschlagen: {e}")
            else:
                plugin_logger.warning(f"Proxies: Lokale Datei '{filepath}' nicht gefunden.")
                
        if not raw_proxies:
            return {
                "status": "error",
                "message": "Keine Proxys in der URL oder lokalen Datei gefunden."
            }
            
        plugin_logger.info(f"Proxies: {len(raw_proxies)} Proxys gefunden. Normalisiere und teste...")
        
        # 3. Normalize Proxies
        normalized_proxies = []
        for proxy in raw_proxies:
            proxy = proxy.strip()
            if not proxy:
                continue
            if not proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://', 'socks5h://')):
                # Auto-prefix pure ip:port with socks5h://
                proxy = 'socks5h://' + proxy
            normalized_proxies.append(proxy)
            
        # Ensure uniqueness after normalization
        normalized_proxies = list(dict.fromkeys(normalized_proxies))
        
        # 4. Test Proxies in Parallel
        active_proxies = []
        
        def test_single_proxy(proxy_addr):
            test_proxies = {
                "http": proxy_addr,
                "https": proxy_addr
            }
            try:
                start = time.time()
                r = requests.get("https://api.ipify.org", proxies=test_proxies, timeout=timeout, verify=False)
                latency = round((time.time() - start) * 1000, 2)
                if r.status_code == 200:
                    return proxy_addr, True, latency
            except Exception:
                pass
            return proxy_addr, False, None
            
        plugin_logger.info(f"Proxies: Starte parallele Validierung von {len(normalized_proxies)} Proxys mit {max_workers} Threads...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(test_single_proxy, p): p for p in normalized_proxies}
            for future in as_completed(futures):
                try:
                    p_addr, is_alive, latency = future.result()
                    if is_alive:
                        active_proxies.append(p_addr)
                        plugin_logger.info(f"Proxies: [ALIVE] {p_addr} (Latenz: {latency}ms)")
                except Exception as e:
                    plugin_logger.error(f"Proxies: Fehler beim Testen von Proxy: {e}")
                    
        # 5. Persist Active Proxies
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)
        active_file = os.path.join(data_dir, "active_proxies.json")
        
        with open(active_file, "w", encoding="utf-8") as f:
            json.dump(active_proxies, f, indent=2)
            
        total_discovered = len(normalized_proxies)
        total_active = len(active_proxies)
        total_deleted = total_discovered - total_active
        
        plugin_logger.info(f"Proxies: Synchronisation beendet. Aktiv: {total_active} | Inaktiv gelöscht: {total_deleted}")
        
        return {
            "status": "ok",
            "message": f"Proxy-Synchronisation erfolgreich. Online: {total_active} | Inaktive gelöscht: {total_deleted}",
            "summary": {
                "total_imported": total_discovered,
                "active": total_active,
                "deleted": total_deleted,
                "active_proxies": active_proxies
            }
        }
