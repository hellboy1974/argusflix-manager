from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from datetime import datetime
from ..threads import PortalDetectiveThread

class DetectiveTab(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.app = parent_app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        lbl = QLabel("Target Portal URL to Analyze:")
        layout.addWidget(lbl)

        self.detective_input = QLineEdit()
        self.detective_input.setPlaceholderText("http://portal.com:8080")
        layout.addWidget(self.detective_input)

        btn = QPushButton("Run Deep Forensic Analysis")
        btn.clicked.connect(self.run_detective)
        layout.addWidget(btn)

        self.detective_log = QTextEdit()
        self.detective_log.setReadOnly(True)
        layout.addWidget(self.detective_log)

    def run_detective(self):
        url = self.detective_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Warning", "Please enter a URL.")
            return

        self.detective_log.clear()
        self.detective_thread = PortalDetectiveThread(url, self.app.config["user_agent"], self.app.config["timeout"])
        self.detective_thread.signals.log.connect(self.log_detective)
        self.detective_thread.start()

    def log_detective(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.detective_log.append(f"[{timestamp}] {msg}")
