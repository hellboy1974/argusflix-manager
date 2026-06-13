from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from datetime import datetime
from ..threads import PortalCheckerThread

class CheckerTab(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.app = parent_app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        lbl = QLabel("Portal URLs (one per line):")
        layout.addWidget(lbl)

        self.checker_input = QTextEdit()
        self.checker_input.setMaximumHeight(150)
        self.checker_input.setPlaceholderText("http://portal.com:8080/c/")
        layout.addWidget(self.checker_input)

        btn = QPushButton("Run Portal Checker")
        btn.clicked.connect(self.run_checker)
        layout.addWidget(btn)

        self.checker_log = QTextEdit()
        self.checker_log.setReadOnly(True)
        layout.addWidget(self.checker_log)

    def run_checker(self):
        text = self.checker_input.toPlainText()
        urls = [u.strip() for u in text.split('\n') if u.strip()]
        if not urls:
            QMessageBox.warning(self, "Warning", "Please enter at least one URL.")
            return

        self.checker_log.clear()
        self.checker_thread = PortalCheckerThread(urls, self.app.config["user_agent"], self.app.config["timeout"])
        self.checker_thread.signals.log.connect(self.log_checker)
        self.checker_thread.start()

    def log_checker(self, msg):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.checker_log.append(f"[{timestamp}] {msg}")
