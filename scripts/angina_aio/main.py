import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

# Import tabs
from tabs.checker import CheckerTab
from tabs.detective import DetectiveTab
from tabs.macgen import MacGenTab
from tabs.scanner import ScannerTab
from tabs.settings import SettingsTab

class AnginaAIO(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🖤 ANGINA™ 🖤 AIO Reloaded")
        self.resize(1100, 750)
        
        # Internal Global State
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

        # Add individual tabs
        self.tab_checker = CheckerTab(self)
        self.tab_detective = DetectiveTab(self)
        self.tab_macgen = MacGenTab(self)
        self.tab_scanner = ScannerTab(self)
        self.tab_settings = SettingsTab(self)

        self.tabs.addTab(self.tab_checker, "1. Portal Checker")
        self.tabs.addTab(self.tab_detective, "2. Portal Detective")
        self.tabs.addTab(self.tab_macgen, "3. MAC Generator")
        self.tabs.addTab(self.tab_scanner, "4. Mac Attack")
        self.tabs.addTab(self.tab_settings, "5. Settings")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = AnginaAIO()
    window.show()
    sys.exit(app.exec_())
