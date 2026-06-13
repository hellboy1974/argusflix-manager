from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QFileDialog
from datetime import datetime
from ..threads import ScannerThread

class ScannerTab(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.app = parent_app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

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

    def load_macs(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select MACs File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.app.macs_list = [line.strip() for line in f if line.strip()]
            self.update_scan_labels()

    def load_proxies(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Proxies File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.app.proxies_list = [line.strip() for line in f if line.strip()]
            self.update_scan_labels()

    def update_scan_labels(self):
        self.scan_status_lbl.setText(f"Loaded: {len(self.app.macs_list)} MACs | {len(self.app.proxies_list)} Proxies")

    def start_scan(self):
        url = self.scan_url.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a target Portal URL.")
            return
        if not self.app.macs_list:
            QMessageBox.warning(self, "Warning", "Please load a MAC list first.")
            return

        self.btn_start_scan.setEnabled(False)
        self.btn_stop_scan.setEnabled(True)
        self.scan_log.clear()

        self.scanner_thread = ScannerThread(
            url, self.app.macs_list, self.app.proxies_list, 
            self.app.config["user_agent"], self.app.config["timeout"], self.app.config["max_threads"]
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
        import os
        hits_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hits.txt")
        try:
            with open(hits_file, "a", encoding="utf-8") as f:
                f.write(f"{url} | {mac}\n")
        except:
            pass
