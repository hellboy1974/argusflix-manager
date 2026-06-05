# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'ANGINA_Portal_Status_Checker_08.py'
# Bytecode version: 3.8.0rc1+ (3413)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import subprocess
import importlib.util
import requests
import socket
import time
import re
import concurrent.futures
import json
import csv
import base64
from datetime import datetime
import urllib3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QProgressBar, QComboBox, QLineEdit, QSpinBox, QCheckBox, QGroupBox, QTabWidget, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QListWidget, QListWidgetItem, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QTextCursor, QColor, QPalette
from PyQt5.QtGui import QIcon
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def check_requirements():
    # ***<module>.check_requirements: Failure: Compilation Error
    required_packages = ['requests', 'urllib3', 'PyQt5']
    missing_packages = []
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
    if missing_packages:
        print(f'Installing missing packages: {', '.join(missing_packages)}')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print('Packages installed successfully!')
            os.execl(sys.executable, sys.executable, *sys.argv)
        except subprocess.CalledProcessError:
            print('Failed to install required packages. Please install them manually.')
            sys.exit(1)
check_requirements()
def get_app_directory():
    """Get the directory where the application is running from"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))
def create_folders():
    app_dir = get_app_directory()
    script_name = 'ANGINA_Portal_Checker'
    main_folder = os.path.join(app_dir, f'{script_name}_Data')
    if not os.path.exists(main_folder):
        try:
            os.makedirs(main_folder)
            print(f'Created main folder: {main_folder}')
        except Exception as e:
            print(f'Error creating main folder: {e}')
            main_folder = app_dir
    input_folder = os.path.join(main_folder, 'URL_Lists')
    output_folder = os.path.join(main_folder, 'Check_Results')
    history_folder = os.path.join(main_folder, 'Check_History')
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
    # irreducible cflow, using cdg fallback
    # ***<module>.load_config: Failure: Compilation Error
    app_dir = get_app_directory()
    config_path = os.path.join(app_dir, 'config.json')
    default_config = {'max_workers': 15, 'timeout': 5, 'retries': 2, 'check_interval': 300, 'output_formats': ['txt', 'json', 'csv'], 'enable_history': True, 'quick_mode': False}
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return {**default_config, **json.load(f)}
                    return default_config
                    try:
                        with open(config_path, 'w') as f:
                            json.dump(default_config, f, indent=2)
                    except:
                        pass
                    return default_config
CONFIG = load_config()
class IPGeolocationService:
    def __init__(self):
        self.services = [self._ipapi_service, self._ipapi_com_service, self._ipwhois_service, self._ipgeolocation_service]
    def get_ip_info(self, host_with_port):
        """Get IP address and geolocation information with multiple fallbacks"""
        host = host_with_port.split(':')[0]
        ip = self._resolve_ip(host)
        if ip == 'Unknown':
            return ('Unknown', 'Unknown', 'Unknown', 'Unknown')
        else:
            for service in self.services:
                try:
                    country, isp, org = service(ip)
                    if country!= 'Unknown':
                        flag = self._get_country_flag(country)
                        return (ip, f'{country} {flag}'.strip(), isp, org)
                except:
                    continue
            return (ip, 'Unknown', 'Unknown', 'Unknown')
    def _resolve_ip(self, host):
        """Resolve hostname to IP address with multiple methods"""
        # ***<module>.IPGeolocationService._resolve_ip: Failure: Different control flow
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            import dns.resolver
            answers = dns.resolver.resolve(host, 'A')
            return answers[0].to_text()
        try:
            resp = requests.get(f'https://dns.google/resolve?name={host}&type=A', timeout=3)
            data = resp.json()
            if 'Answer' in data:
                return data['Answer'][0]['data']
        except:
            pass
        return 'Unknown'
    def _ipapi_service(self, ip):
        """ip-api.com service (free, no API key needed)"""
        try:
            resp = requests.get(f'http://ip-api.com/json/{ip}?fields=country,countryCode,isp,org', timeout=3)
            data = resp.json()
            if data.get('status') == 'success':
                country = data.get('country', 'Unknown')
                isp = data.get('isp', 'Unknown')
                org = data.get('org', 'Unknown')
                return (country, isp, org)
        except:
            pass
        return ('Unknown', 'Unknown', 'Unknown')
    def _ipapi_com_service(self, ip):
        """api.ipapi.com service (free tier available)"""
        try:
            resp = requests.get(f'http://api.ipapi.com/{ip}?access_key=free', timeout=3)
            data = resp.json()
            country = data.get('country_name', 'Unknown')
            isp = data.get('connection', {}).get('isp', 'Unknown')
            org = data.get('connection', {}).get('organization', 'Unknown')
            return (country, isp, org)
        except:
            pass
        return ('Unknown', 'Unknown', 'Unknown')
    def _ipwhois_service(self, ip):
        """ipwhois.io service (free)"""
        try:
            resp = requests.get(f'http://ipwhois.app/json/{ip}', timeout=3)
            data = resp.json()
            country = data.get('country', 'Unknown')
            isp = data.get('isp', 'Unknown')
            org = data.get('org', 'Unknown')
            return (country, isp, org)
        except:
            pass
        return ('Unknown', 'Unknown', 'Unknown')
    def _ipgeolocation_service(self, ip):
        """ipgeolocation.io service (free tier)"""
        try:
            resp = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey=free&ip={ip}', timeout=3)
            data = resp.json()
            country = data.get('country_name', 'Unknown')
            isp = data.get('isp', 'Unknown')
            org = data.get('organization', 'Unknown')
            return (country, isp, org)
        except:
            pass
        return ('Unknown', 'Unknown', 'Unknown')
    def _get_country_flag(self, country_name):
        """Convert country name to flag emoji"""
        # ***<module>.IPGeolocationService._get_country_flag: Failure: Compilation Error
        San Marino = {'US': 'United States', 'United Kingdom': 'United Kingdom', 'CA': 'Canada', 'AU': 'Australia', 'DE': 'Germany', 'FR': 'France', 'IT': 'Italy', 'ES': 'Spain', 'NL': 'Netherlands', 'BE': 'Belgium', 'CH': 'Switzerland', 'AT': 'Austria', 'SE': 'Sweden', 'NO': 'Norway', 'DK': 'Denmark', 'FI': 'Finland', 'IE': 'Ireland', 'PT': 'Portugal', 'PL': 'Poland', 'CZ': 'Czech Republic', 'HU': 'Hungary', 'GR': 'Greece', 'RO': 'Romania', 'BG': 'Bulgaria', 'HR': 'Croatia', 'RS': '
        country_code = country_codes.get(country_name, '')
        if len(country_code) == 2:
            return ''.join((chr(ord(c) + 127397) for c in country_code.upper()))
        else:
            return ''
geo_service = IPGeolocationService()
class PortalCheckerThread(QThread):
    progress_update = pyqtSignal(dict)
    finished_checking = pyqtSignal(list, int, int, int)
    error_occurred = pyqtSignal(str)
    def __init__(self, portals, config):
        super().__init__()
        self.portals = portals
        self.config = config
        self.is_running = True
    def stop(self):
        self.is_running = False
    def check_single_portal(self, url, index):
        # irreducible cflow, using cdg fallback
        # ***<module>.PortalCheckerThread.check_single_portal: Failure: Compilation Error
        if not self.is_running:
            return None
        else:
            full_url = url if url.startswith('http') else 'http://' + url
            host = full_url.split('//')[(-1)].split('/')[0]
            status = 'Offline'
            response_time = None
            status_code = None
            for attempt in range(self.config['retries']):
                pass
        if not self.is_running:
            return
        start_time = time.time()
        resp = requests.get(full_url, timeout=self.config['timeout'], verify=False)
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
        status_code = resp.status_code
        if resp.status_code == 200:
            pass
        status = 'Online'
        status = f'HTTP Error {resp.status_code}'
        except requests.exceptions.Timeout:
            pass
        status = 'Timeout'
        except requests.exceptions.ConnectionError:
            pass
        status = 'Connection Error'
        except requests.exceptions.RequestException as e:
            pass
        status = f'Error: {str(e)}'
        if attempt < self.config['retries'] - 1:
            time.sleep(1 * (attempt + 1))
        is_online = status == 'Online'
        ip, country, isp, org = geo_service.get_ip_info(host)
        result = {'url': url, 'status': status, 'status_code': status_code, 'response_time': response_time, 'ip': ip, 'country': country, 'isp': isp, 'org': org, 'is_online': is_online, 'index': index, 'timestamp': datetime.now().isoformat()}
        self.progress_update.emit(result)
        return result
    def run(self):
        try:
            results = []
            online_count = 0
            offline_count = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['max_workers']) as executor:
                future_to_url = {executor.submit(self.check_single_portal, url, i + 1): (url, i + 1) for i, url in enumerate(self.portals)}
                for future in concurrent.futures.as_completed(future_to_url):
                    if not self.is_running:
                        break
                    else:
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                                if result['is_online']:
                                    online_count += 1
                                else:
                                    offline_count += 1
                        except Exception as e:
                            self.error_occurred.emit(f'Error checking portal: {e}')
            unknown_count = len(self.portals) - (online_count + offline_count)
            results.sort(key=lambda x: x['index'])
            self.finished_checking.emit(results, online_count, offline_count, unknown_count)
        except Exception as e:
            self.error_occurred.emit(str(e))
DARK_THEME = '\nQMainWindow, QWidget {\n    background-color: #1e1e1e;\n    color: #ffffff;\n    font-family: Segoe UI, Arial;\n}\n\nQTabWidget::pane {\n    border: 1px solid #444;\n    background-color: #2d2d2d;\n}\n\nQTabBar::tab {\n    background-color: #333;\n    color: #ccc;\n    padding: 8px 16px;\n    margin-right: 2px;\n    border: 1px solid #444;\n    border-bottom: none;\n    border-top-left-radius: 4px;\n    border-top-right-radius: 4px;\n}\n\nQTabBar::tab:selected {\n    background-color: #0078d4;\n    color: white;\n    border-color: #005a9e;\n}\n\nQTabBar::tab:hover {\n    background-color: #555;\n}\n\nQGroupBox {\n    font-weight: bold;\n    border: 1px solid #444;\n    border-radius: 5px;\n    margin-top: 10px;\n    padding-top: 10px;\n    color: #0078d4;\n    background-color: #252525;\n}\n\nQGroupBox::title {\n    subcontrol-origin: margin;\n    left: 10px;\n    padding: 0 5px 0 5px;\n    color: #0078d4;\n}\n\nQPushButton {\n    background-color: #0078d4;\n    color: white;\n    border: none;\n    padding: 8px 16px;\n    border-radius: 4px;\n    font-weight: bold;\n    min-width: 80px;\n}\n\nQPushButton:hover {\n    background-color: #106ebe;\n}\n\nQPushButton:pressed {\n    background-color: #005a9e;\n}\n\nQPushButton:disabled {\n    background-color: #555;\n    color: #888;\n}\n\nQPushButton#scanButton {\n    background-color: #107c10;\n    font-size: 12px;\n}\n\nQPushButton#scanButton:hover {\n    background-color: #0e6b0e;\n}\n\nQPushButton#stopButton {\n    background-color: #d83b01;\n    font-size: 12px;\n}\n\nQPushButton#stopButton:hover {\n    background-color: #b32d00;\n}\n\nQPushButton#saveButton {\n    background-color: #ffb900;\n    color: #000;\n    font-size: 12px;\n}\n\nQPushButton#saveButton:hover {\n    background-color: #d19d00;\n}\n\nQPushButton#exportOnlineButton {\n    background-color: #107c10;\n    font-size: 12px;\n}\n\nQPushButton#exportOnlineButton:hover {\n    background-color: #0e6b0e;\n}\n\nQPushButton#historyButton {\n    background-color: #9C27B0;\n    font-size: 12px;\n}\n\nQPushButton#historyButton:hover {\n    background-color: #7B1FA2;\n}\n\nQLabel {\n    color: #cccccc;\n    padding: 2px;\n}\n\nQProgressBar {\n    border: 1px solid #444;\n    border-radius: 3px;\n    text-align: center;\n    color: white;\n    background-color: #333;\n}\n\nQProgressBar::chunk {\n    background-color: #0078d4;\n    border-radius: 2px;\n}\n\nQTextEdit, QListWidget, QTableWidget {\n    background-color: #252525;\n    color: #cccccc;\n    border: 1px solid #444;\n    border-radius: 3px;\n    font-family: Consolas, monospace;\n    font-size: 11px;\n}\n\nQComboBox, QSpinBox, QLineEdit {\n    background-color: #333;\n    color: white;\n    border: 1px solid #555;\n    border-radius: 3px;\n    padding: 4px;\n    min-height: 20px;\n}\n\nQComboBox:editable, QSpinBox:editable, QLineEdit:editable {\n    background-color: #2a2a2a;\n}\n\nQComboBox::drop-down {\n    border: none;\n}\n\nQComboBox QAbstractItemView {\n    background-color: #333;\n    color: white;\n    border: 1px solid #555;\n    selection-background-color: #0078d4;\n}\n\nQCheckBox {\n    color: #cccccc;\n    spacing: 5px;\n}\n\nQCheckBox::indicator {\n    width: 16px;\n    height: 16px;\n}\n\nQCheckBox::indicator:unchecked {\n    border: 1px solid #666;\n    background-color: #333;\n}\n\nQCheckBox::indicator:checked {\n    border: 1px solid #0078d4;\n    background-color: #0078d4;\n}\n\nQHeaderView::section {\n    background-color: #333;\n    color: #cccccc;\n    padding: 4px;\n    border: 1px solid #444;\n    font-weight: bold;\n}\n\nQTableWidget {\n    gridline-color: #444;\n    alternate-background-color: #2a2a2a;\n}\n\nQTableWidget::item {\n    padding: 4px;\n    border-bottom: 1px solid #333;\n}\n\nQTableWidget::item:selected {\n    background-color: #0078d4;\n    color: white;\n}\n\nQSplitter::handle {\n    background-color: #444;\n    border: 1px solid #555;\n}\n\nQSplitter::handle:hover {\n    background-color: #555;\n}\n\nQStatusBar {\n    background-color: #0078d4;\n    color: white;\n    border-top: 1px solid #005a9e;\n}\n'
class AnginaPortalChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.portals = []
        self.current_results = []
        self.checker_thread = None
        self.continuous_timer = QTimer()
        self.continuous_timer.timeout.connect(self.start_continuous_check)
        self.continuous_mode = False
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('🖤 ANGINA™ 🖤 Portal Status Checker 🚥')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(DARK_THEME)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        header_layout = QHBoxLayout()
        title_label = QLabel('🖤 ANGINA™ 🖤 Portal Status Checker 🚥')
        title_label.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title_label.setStyleSheet('color: #e91e63; padding: 5px;')
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.scan_btn = QPushButton('🔍 START SCAN')
        self.scan_btn.setObjectName('scanButton')
        self.scan_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.scan_btn.clicked.connect(self.start_checking)
        self.scan_btn.setMinimumHeight(35)
        header_layout.addWidget(self.scan_btn)
        self.stop_btn = QPushButton('🛑 STOP SCAN')
        self.stop_btn.setObjectName('stopButton')
        self.stop_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.stop_btn.clicked.connect(self.stop_checking)
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
        self.export_online_btn = QPushButton('💚 EXPORT ONLINE PORTALS')
        self.export_online_btn.setObjectName('exportOnlineButton')
        self.export_online_btn.setFont(QFont('Segoe UI', 10, QFont.Bold))
        self.export_online_btn.clicked.connect(self.export_online_urls)
        self.export_online_btn.setMinimumHeight(35)
        self.export_online_btn.setEnabled(False)
        header_layout.addWidget(self.export_online_btn)
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
        progress_layout.addWidget(self.progress_bar)
        self.progress_label = QLabel('Ready to scan')
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
        url_group = QGroupBox('📥 Portal URLs Input')
        url_layout = QVBoxLayout(url_group)
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel('⌨ Input Method:'))
        self.input_method = QComboBox()
        self.input_method.addItems(['Import from file', 'Manual entry', 'Load from history', 'Continuous monitoring'])
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
        self.url_text.setPlaceholderText('Enter URLs here (one per line or separated by commas/semicolons)...')
        self.url_text.setMinimumHeight(120)
        url_layout.addWidget(self.url_text)
        self.load_urls_btn = QPushButton('🔰 Load URLs')
        self.load_urls_btn.clicked.connect(self.load_urls)
        url_layout.addWidget(self.load_urls_btn)
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
        formats_layout = QVBoxLayout()
        formats_layout.addWidget(QLabel('📒 Output Formats:'))
        self.output_txt = QCheckBox('📄 TXT Format')
        self.output_txt.setChecked('txt' in CONFIG['output_formats'])
        formats_layout.addWidget(self.output_txt)
        self.output_json = QCheckBox('📊 JSON Format')
        self.output_json.setChecked('json' in CONFIG['output_formats'])
        formats_layout.addWidget(self.output_json)
        self.output_csv = QCheckBox('📋 CSV Format')
        self.output_csv.setChecked('csv' in CONFIG['output_formats'])
        formats_layout.addWidget(self.output_csv)
        config_layout.addLayout(formats_layout)
        input_layout.addWidget(config_group)
        tabs.addTab(input_tab, '📥 Input & Configuration')
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        results_layout.setSpacing(10)
        splitter = QSplitter(Qt.Vertical)
        online_group = QGroupBox('✅ Online Portals')
        online_layout = QVBoxLayout(online_group)
        self.online_list = QListWidget()
        self.online_list.setFont(QFont('Consolas', 9))
        online_layout.addWidget(self.online_list)
        splitter.addWidget(online_group)
        results_group = QGroupBox('📊 Detailed Results')
        results_detail_layout = QVBoxLayout(results_group)
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(7)
        self.results_table.setHorizontalHeaderLabels(['URL', 'Status', 'Response Time', 'IP', 'Country', 'ISP', 'Timestamp'])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.results_table.setFont(QFont('Consolas', 8))
        results_detail_layout.addWidget(self.results_table)
        splitter.addWidget(results_group)
        splitter.setSizes([300, 500])
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
        self.statusBar().showMessage(f'🖤 ANGINA™ 🖤 Portal Checker - Ready{folder_info}')
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
        else:
            if method == 'Load from history':
                folder = HISTORY_FOLDER
            else:
                return None
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and (not f.startswith('.'))]
            self.file_combo.addItems(sorted(files))
        except Exception as e:
            self.log_message(f'Error reading folder: {e}', 'error')
    def load_urls(self):
        # ***<module>.AnginaPortalChecker.load_urls: Failure: Compilation Error
        method = self.input_method.currentText()
        self.portals = []
        if method == 'Import from file':
            filename = self.file_combo.currentText()
            if not filename:
                QMessageBox.warning(self, 'Warning', 'Please select a file')
                return None
            else:
                filepath = os.path.join(INPUT_FOLDER, filename)
                self.portals = self.read_urls_from_file(filepath)
        else:
            if method == 'Manual entry':
                text = self.url_text.toPlainText().strip()
                if not text:
                    QMessageBox.warning(self, 'Warning', 'Please enter some URLs')
                    return None
                else:
                    urls = re.split('[\\s,;]+', text)
                    self.portals = list(dict.fromkeys([u.strip() for u in urls if u.strip()]))
            else:
                if method == 'Load from history':
                    filename = self.file_combo.currentText()
                    if not filename:
                        QMessageBox.warning(self, 'Warning', 'Please select a history file')
                        return None
                    else:
                        filepath = os.path.join(HISTORY_FOLDER, filename)
                        self.portals = self.read_urls_from_history(filepath)
                else:
                    if method == 'Continuous monitoring':
                        filename = self.file_combo.currentText()
                        if not filename:
                            QMessageBox.warning(self, 'Warning', 'Please select a file for continuous monitoring')
                            return None
                        else:
                            filepath = os.path.join(INPUT_FOLDER, filename)
                            self.portals = self.read_urls_from_file(filepath)
                            if self.portals:
                                self.log_message(f'🔄 Continuous monitoring configured with {len(self.portals)} URLs')
                                self.log_message(f'⏰ Will check every {CONFIG['check_interval']} seconds')
                                folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
                                self.statusBar().showMessage(f'🔄 Monitoring {len(self.portals)} URLs every {CONFIG['check_interval']}s{folder_info}')
                            else:
                                QMessageBox.warning(self, 'Warning', 'No valid URLs loaded for monitoring')
                                return None
        if self.portals:
            self.log_message(f'✅ Loaded {len(self.portals)} URLs')
            self.scan_btn.setEnabled(True)
            folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
            self.statusBar().showMessage(f'🖤 Ready - {len(self.portals)} URLs loaded{folder_info}')
        else:
            QMessageBox.warning(self, 'Warning', 'No valid URLs loaded')
            self.scan_btn.setEnabled(False)
    def read_urls_from_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if not content.strip():
                self.log_message('File is empty', 'warning')
                return []
            else:
                urls = re.split('[\\s,;]+', content)
                valid_urls = list(dict.fromkeys([u.strip() for u in urls if u.strip()]))
                if not valid_urls:
                    self.log_message('No valid URLs found in file', 'warning')
                    return []
                else:
                    return valid_urls
        except Exception as e:
            self.log_message(f'Error reading file: {e}', 'error')
            return []
    def read_urls_from_history(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            urls = set()
            for entry in data:
                for portal in entry.get('portals', []):
                    urls.add(portal.get('url'))
            valid_urls = list(urls)
            return valid_urls
        except Exception as e:
            self.log_message(f'Error reading history file: {e}', 'error')
            return []
    def start_checking(self):
        if not self.portals:
            QMessageBox.warning(self, 'Warning', 'No URLs to check')
            return None
        else:
            method = self.input_method.currentText()
            if method == 'Continuous monitoring':
                self.start_continuous_monitoring()
            else:
                self.start_single_check()
    def start_single_check(self):
        self.prepare_for_checking()
        config = {'max_workers': self.max_workers.value(), 'timeout': self.timeout.value(), 'retries': self.retries.value(), 'enable_history': self.enable_history.isChecked()}
        self.checker_thread = PortalCheckerThread(self.portals, config)
        self.checker_thread.progress_update.connect(self.on_progress_update)
        self.checker_thread.finished_checking.connect(self.on_checking_finished)
        self.checker_thread.error_occurred.connect(self.on_error_occurred)
        self.checker_thread.start()
    def start_continuous_monitoring(self):
        """Start continuous monitoring mode"""
        # ***<module>.AnginaPortalChecker.start_continuous_monitoring: Failure: Compilation Error
        if not self.portals:
            QMessageBox.warning(self, 'Warning', 'No URLs loaded for monitoring')
            return None
        else:
            self.prepare_for_checking()
            self.continuous_mode = True
            self.start_single_check()
            self.continuous_timer.start(CONFIG['check_interval'] * 1000)
            self.log_message(f'🔄 Continuous monitoring started - checking every {CONFIG['check_interval']} seconds')
    def prepare_for_checking(self):
        self.current_results = []
        self.online_list.clear()
        self.results_table.setRowCount(0)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.portals))
        self.progress_bar.setValue(0)
        self.scan_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.save_btn.setEnabled(False)
        self.export_online_btn.setEnabled(False)
        self.progress_label.setText('🔄 Starting scan...')
        method = self.input_method.currentText()
        folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
        if method == 'Continuous monitoring':
            self.statusBar().showMessage(f'🔄 Continuous monitoring - Starting scan...{folder_info}')
        else:
            self.statusBar().showMessage(f'🔄 Scanning portals...{folder_info}')
        self.log_message('🚀 Started scanning portals')
    def stop_checking(self):
        method = self.input_method.currentText()
        if method == 'Continuous monitoring':
            self.continuous_timer.stop()
            self.continuous_mode = False
            self.log_message('⏹️ Continuous monitoring stopped')
            folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
            self.statusBar().showMessage(f'🛑 Continuous monitoring stopped{folder_info}')
        if self.checker_thread and self.checker_thread.isRunning():
                self.checker_thread.stop()
                self.checker_thread.wait()
                if method!= 'Continuous monitoring':
                    self.log_message('⏹️ Scan stopped by user')
        self.scan_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if method!= 'Continuous monitoring':
            self.progress_label.setText('🛑 Scan stopped')
    def start_continuous_check(self):
        if self.portals and self.continuous_mode:
                self.log_message('🔄 Continuous monitoring check started')
                self.start_single_check()
    def on_progress_update(self, result):
        # ***<module>.AnginaPortalChecker.on_progress_update: Failure: Compilation Error
        self.current_results.append(result)
        current_progress = len(self.current_results)
        self.progress_bar.setValue(current_progress)
        method = self.input_method.currentText()
        if method == 'Continuous monitoring':
            self.progress_label.setText(f'🔄 Monitoring... {current_progress}/{len(self.portals)}')
        else:
            self.progress_label.setText(f'🔍 Scanning... {current_progress}/{len(self.portals)}')
        if result['is_online']:
            country_display = result['country'] if result['country']!= 'Unknown' else '🌐 Location'
            item_text = f'✅ {result['url']} - {result['response_time']}ms - {country_display}'
            item = QListWidgetItem(item_text)
            item.setForeground(QColor('#90EE90'))
            self.online_list.addItem(item)
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        url_item = QTableWidgetItem(result['url'])
        self.results_table.setItem(row, 0, url_item)
        status_item = QTableWidgetItem(result['status'])
        if result['is_online']:
            status_item.setBackground(QColor(25, 100, 25))
            status_item.setForeground(QColor('#90EE90'))
        else:
            status_item.setBackground(QColor(100, 25, 25))
            status_item.setForeground(QColor('#FF6B6B'))
        self.results_table.setItem(row, 1, status_item)
        response_time = str(result['response_time']) + ' ms' if result['response_time'] else 'N/A'
        response_item = QTableWidgetItem(response_time)
        self.results_table.setItem(row, 2, response_item)
        self.results_table.setItem(row, 3, QTableWidgetItem(result['ip']))
        country_item = QTableWidgetItem(result['country'])
        if result['country']!= 'Unknown':
            country_item.setForeground(QColor('#4FC3F7'))
        self.results_table.setItem(row, 4, country_item)
        isp_item = QTableWidgetItem(result['isp'])
        if result['isp']!= 'Unknown':
            isp_item.setForeground(QColor('#FFA726'))
        self.results_table.setItem(row, 5, isp_item)
        self.results_table.setItem(row, 6, QTableWidgetItem(result['timestamp'][11:19]))
    def on_checking_finished(self, results, online_count, offline_count, unknown_count):
        self.current_results = results
        self.progress_bar.setVisible(False)
        self.scan_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.save_btn.setEnabled(True)
        self.export_online_btn.setEnabled(True)
        total = len(results)
        success_rate = online_count / total * 100 if total > 0 else 0
        successful_geo = len([r for r in results if r['country']!= 'Unknown'])
        geo_success_rate = successful_geo / total * 100 if total > 0 else 0
        summary = f'✅ Scan completed! Total: {total} | ✅ Online: {online_count} | ❌ Offline: {offline_count} | ❓ Unknown: {unknown_count} | 📊 Success rate: {success_rate:.2f}% | 🌍 Geolocation: {geo_success_rate:.1f}%'
        self.progress_label.setText(summary)
        method = self.input_method.currentText()
        folder_info = f' | Data Folder: {MAIN_FOLDER}' if len(MAIN_FOLDER) < 50 else f' | Data Folder: ...{MAIN_FOLDER[(-40):]}'
        if method == 'Continuous monitoring':
            next_check = datetime.now().timestamp() + CONFIG['check_interval']
            next_time = datetime.fromtimestamp(next_check).strftime('%H:%M:%S')
            self.statusBar().showMessage(f'🔄 Monitoring - Next check at {next_time} | {summary}{folder_info}')
        else:
            self.statusBar().showMessage(f'{summary}{folder_info}')
        self.log_message(summary)
        self.auto_save_results()
        if method!= 'Continuous monitoring':
            QMessageBox.information(self, 'Scan Completed', summary)
    def on_error_occurred(self, error_msg):
        self.log_message(f'❌ Error: {error_msg}', 'error')
    def auto_save_results(self):
        if not self.current_results:
            return None
        else:
            online_count = len([r for r in self.current_results if r['is_online']])
            offline_count = len([r for r in self.current_results if not r['is_online']])
            unknown_count = len(self.current_results) - (online_count + offline_count)
            timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
            base_filename = f'ANGINA_portal_results_{timestamp}'
            output_formats = []
            if self.output_txt.isChecked():
                output_formats.append('txt')
            if self.output_json.isChecked():
                output_formats.append('json')
            if self.output_csv.isChecked():
                output_formats.append('csv')
            for fmt in output_formats:
                filename = os.path.join(OUTPUT_FOLDER, f'{base_filename}.{fmt}')
                self.save_to_file(filename, fmt, online_count, offline_count, unknown_count)
            if self.enable_history.isChecked():
                self.save_to_history(online_count, offline_count, unknown_count)
            self.log_message(f'💾 Results auto-saved as: {base_filename}.*')
    def save_to_history(self, online_count, offline_count, unknown_count):
        """Save current scan results to history"""
        # ***<module>.AnginaPortalChecker.save_to_history: Failure: Compilation Error
        try:
            history_file = os.path.join(HISTORY_FOLDER, f'history_{datetime.now().strftime('%d-%m-%Y')}.json')
            history_data = []
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history_data = json.load(f)
                except Exception as e:
                    self.log_message(f'⚠️ Error reading history file: {e}', 'warning')
                    history_data = []
            history_entry = {'timestamp': datetime.now().isoformat(), 'total_scanned': len(self.current_results), 'online_count': online_count, 'offline_count': offline_count, 'unknown_count': unknown_count, 'success_rate': round(online_count / len(self.current_results) * 100, 2) if self.current_results else 0, 'portals': self.current_results}
            history_data.append(history_entry)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2)
            self.log_message(f'📚 Scan results saved to history: {os.path.basename(history_file)}')
        except Exception as e:
            self.log_message(f'❌ Error saving to history: {e}', 'error')
    def save_results(self):
        if not self.current_results:
            QMessageBox.warning(self, 'Warning', 'No results to save')
            return None
        else:
            filename, selected_filter = QFileDialog.getSaveFileName(self, 'Save Results', OUTPUT_FOLDER, 'Text Files (*.txt);;JSON Files (*.json);;CSV Files (*.csv)')
            if filename:
                online_count = len([r for r in self.current_results if r['is_online']])
                offline_count = len([r for r in self.current_results if not r['is_online']])
                unknown_count = len(self.current_results) - (online_count + offline_count)
                if selected_filter == 'Text Files (*.txt)':
                    fmt = 'txt'
                else:
                    if selected_filter == 'JSON Files (*.json)':
                        fmt = 'json'
                    else:
                        fmt = 'csv'
                self.save_to_file(filename, fmt, online_count, offline_count, unknown_count)
                self.log_message(f'💾 Results saved to: {filename}')
    def export_online_urls(self):
        """Export only online URLs to a clean text file"""
        # ***<module>.AnginaPortalChecker.export_online_urls: Failure: Compilation Error
        if not self.current_results:
            QMessageBox.warning(self, 'Warning', 'No results to export')
            return None
        else:
            online_portals = [r for r in self.current_results if r['is_online']]
            if not online_portals:
                QMessageBox.information(self, 'No Online Portals', 'No online portals found to export')
                return None
            else:
                filename, _ = QFileDialog.getSaveFileName(self, 'Export Online URLs', OUTPUT_FOLDER, 'Text Files (*.txt)')
                if filename:
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write('🖤 ANGINA™ 🖤 Online Portals Only\n')
                            f.write('========================================\n')
                            f.write(f'Generated: {datetime.now().strftime('%B %d,%Y - %I:%M %p')}\n')
                            f.write(f'Total Online: {len(online_portals)}\n')
                            f.write('========================================\n\n')
                            for i, portal in enumerate(online_portals, 1):
                                f.write(f'{portal['url']}\n')
                            f.write('\n========================================\n')
                            f.write('DETAILED ONLINE PORTALS INFO:\n')
                            f.write('========================================\n\n')
                            for i, portal in enumerate(online_portals, 1):
                                f.write(f'{i}. {portal['url']}\n')
                                if portal['response_time']:
                                    f.write(f'   Response: {portal['response_time']} ms\n')
                                f.write(f'   IP: {portal['ip']}\n')
                                f.write(f'   Country: {portal['country']}\n')
                                f.write(f'   ISP: {portal['isp']}\n\n')
                        self.log_message(f'💚 Online URLs exported to: {filename}')
                        QMessageBox.information(self, 'Export Successful', f'Exported {len(online_portals)} online portals to:\n{filename}')
                    except Exception as e:
                        self.log_message(f'❌ Error exporting online URLs: {e}', 'error')
                        QMessageBox.critical(self, 'Export Error', f'Failed to export online URLs:\n{e}')
    def show_history_statistics(self):
        """Show statistics from history files"""
        # ***<module>.AnginaPortalChecker.show_history_statistics: Failure: Compilation Error
        try:
            files = [f for f in os.listdir(HISTORY_FOLDER) if f.startswith('history_') and f.endswith('.json')]
            if not files:
                QMessageBox.information(self, 'No History', 'No history files found.')
                return
            else:
                filename, _ = QFileDialog.getOpenFileName(self, 'Select History File', HISTORY_FOLDER, 'History Files (*.json)')
                if not filename:
                    return
                else:
                    with open(filename, 'r', encoding='utf-8') as f:
                        history_data = json.load(f)
                    total_checks = len(history_data)
                    total_portals = sum((entry['total_scanned'] for entry in history_data))
                    total_online = sum((entry['online_count'] for entry in history_data))
                    avg_online = total_online / total_checks if total_checks > 0 else 0
                    avg_success_rate = total_online / total_portals * 100 if total_portals > 0 else 0
                    portal_reliability = {}
                    for entry in history_data:
                        for portal in entry.get('portals', []):
                            url = portal['url']
                            if url not in portal_reliability:
                                portal_reliability[url] = {'checks': 0, 'online': 0}
                            portal_reliability[url]['checks'] += 1
                            if portal['is_online']:
                                portal_reliability[url]['online'] += 1
                    reliable_portals = []
                    for url, stats in portal_reliability.items():
                        reliability = stats['online'] / stats['checks'] * 100 if stats['checks'] > 0 else 0
                        reliable_portals.append((url, reliability, stats['checks'], stats['online']))
                    reliable_portals.sort(key=lambda x: x[1], reverse=True)
                    stats_dialog = QDialog(self)
                    stats_dialog.setWindowTitle('📊 History Statistics')
                    stats_dialog.setGeometry(200, 200, 800, 600)
                    stats_dialog.setStyleSheet(DARK_THEME)
                    layout = QVBoxLayout(stats_dialog)
                    file_info = QLabel(f'History File: {os.path.basename(filename)}')
                    file_info.setStyleSheet('font-weight: bold; color: #4FC3F7;')
                    layout.addWidget(file_info)
                    stats_group = QGroupBox('📈 Scan Statistics')
                    stats_layout = QVBoxLayout(stats_group)
                    stats_text = QTextEdit()
                    stats_text.setReadOnly(True)
                    stats_text.append(f'Total scans: {total_checks}')
                    stats_text.append(f'Total portals scanned: {total_portals}')
                    stats_text.append(f'Average online per scan: {avg_online:.1f}')
                    stats_text.append(f'Average success rate: {avg_success_rate:.2f}%')
                    stats_text.append(f'History period: {history_data[0]['timestamp'][:10]} to {history_data[(-1)]['timestamp'][:10]}')
                    stats_layout.addWidget(stats_text)
                    layout.addWidget(stats_group)
                    if reliable_portals:
                        reliable_group = QGroupBox('🏆 Most Reliable Portals')
                        reliable_layout = QVBoxLayout(reliable_group)
                        reliable_text = QTextEdit()
                        reliable_text.setReadOnly(True)
                        for i, (url, reliability, checks, online) in enumerate(reliable_portals[:10], 1):
                            reliable_text.append(f'{i}. {url}')
                            reliable_text.append(f'   Reliability: {reliability:.1f}% ({online}/{checks} successful)')
                            reliable_text.append('')
                        reliable_layout.addWidget(reliable_text)
                        layout.addWidget(reliable_group)
                    close_btn = QPushButton('Close')
                    close_btn.clicked.connect(stats_dialog.close)
                    layout.addWidget(close_btn)
                    stats_dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load history statistics:\n{e}')
    def save_to_file(self, filename, fmt, online_count, offline_count, unknown_count):
        # ***<module>.AnginaPortalChecker.save_to_file: Failure: Compilation Error
        try:
            if fmt == 'txt':
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('🖤 ANGINA™ 🖤 Portal Status Checker Results\n')
                    f.write('==================================================\n\n')
                    f.write(f'Scan Date: {datetime.now().strftime('%B %d,%Y - %I:%M %p')}\n\n')
                    for result in self.current_results:
                        f.write(f'{result['index']}. {result['url']}\n')
                        f.write(f'   Status: {result['status']}\n')
                        if result['response_time']:
                            f.write(f'   Response: {result['response_time']} ms\n')
                        f.write(f'   IP: {result['ip']}\n')
                        f.write(f'   Country: {result['country']}\n')
                        f.write(f'   ISP: {result['isp']}\n\n')
                    f.write('============================================================\n')
                    f.write('✅ ONLINE PORTALS SUMMARY\n')
                    f.write('============================================================\n\n')
                    online_portals = [r for r in self.current_results if r['is_online']]
                    if online_portals:
                        for i, portal in enumerate(online_portals, 1):
                            f.write(f'{i}. {portal['url']}\n')
                            f.write('   Status: ✅ ONLINE\n')
                            if portal['response_time']:
                                f.write(f'   Response Time: {portal['response_time']} ms\n')
                            f.write(f'   IP: {portal['ip']}\n')
                            f.write(f'   Country: {portal['country']}\n')
                            f.write(f'   ISP: {portal['isp']}\n')
                            f.write(f'   Timestamp: {portal['timestamp'][11:19]}\n\n')
                    else:
                        f.write('No online portals found.\n\n')
                    f.write('==================================================\n')
                    f.write(f'SUMMARY: Total: {len(self.current_results)} | Online: {online_count} | Offline: {offline_count} | Unknown: {unknown_count}\n')
            else:
                if fmt == 'json':
                    online_portals = [r for r in self.current_results if r['is_online']]
                    output_data = {'metadata': {'timestamp': datetime.now().isoformat(), 'total_scanned': len(self.current_results), 'online_count': online_count, 'offline_count': offline_count, 'unknown_count': unknown_count, 'success_rate': round(online_count / len(self.current_results) * 100, 2) if self.current_results else 0}, 'portals': self.current_results, 'online_portals_summary': {'count': len(online_portals), 'urls_only': [portal['url'] for portal in online_portals], 'detailed': online_portals, 'fastest': sorted(online_portals, key=lambda x: x['response_time'] or float('inf'))[:5], 'by_country': {}, 'by_isp': {}}}
                    for portal in online_portals:
                        country = portal['country']
                        isp = portal['isp']
                        if country not in output_data['online_portals_summary']['by_country']:
                            output_data['online_portals_summary']['by_country'][country] = 0
                        output_data['online_portals_summary']['by_country'][country] += 1
                        if isp not in output_data['online_portals_summary']['by_isp']:
                            output_data['online_portals_summary']['by_isp'][isp] = 0
                        output_data['online_portals_summary']['by_isp'][isp] += 1
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(output_data, f, indent=2)
                else:
                    if fmt == 'csv':
                        with open(filename, 'w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow(['Index', 'URL', 'Status', 'Response Time (ms)', 'IP', 'Country', 'ISP', 'Timestamp'])
                            for result in self.current_results:
                                writer.writerow([result['index'], result['url'], result['status'], result['response_time'] or '', result['ip'], result['country'], result['isp'], result['timestamp']])
                            writer.writerow([])
                            writer.writerow(['ONLINE PORTALS SUMMARY'])
                            writer.writerow(['Number', 'URL', 'Response Time (ms)', 'IP', 'Country', 'ISP'])
                            online_portals = [r for r in self.current_results if r['is_online']]
                            for i, portal in enumerate(online_portals, 1):
                                writer.writerow([i, portal['url'], portal['response_time'] or '', portal['ip'], portal['country'], portal['isp']])
        except Exception as e:
            self.log_message(f'❌ Error saving file: {e}', 'error')
    def log_message(self, message, level='info'):
        timestamp = datetime.now().strftime('%H:%M:%S')
        if level == 'error':
            formatted_message = f'[{timestamp}] ❌ {message}'
            color = '#FF6B6B'
        else:
            if level == 'warning':
                formatted_message = f'[{timestamp}] ⚠️ {message}'
                color = '#FFA726'
            else:
                formatted_message = f'[{timestamp}] ℹ️ {message}'
                color = '#4FC3F7'
        self.log_text.append(f'<span style=\"color: {color}\">{formatted_message}</span>')
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text.setTextCursor(cursor)
    def closeEvent(self, event):
        if self.checker_thread and self.checker_thread.isRunning():
                self.checker_thread.stop()
                self.checker_thread.wait()
        if self.continuous_timer.isActive():
            self.continuous_timer.stop()
        event.accept()
    def set_window_icon(self):
        """Set application icon from external file"""
        try:
            app_dir = get_app_directory()
            icon_path = os.path.join(app_dir, 'Portal_Checker.ico')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
                self.log_message('✅ Application icon loaded')
            else:
                self.log_message('⚠️ Icon file \'Portal_Checker.ico\' not found in application directory', 'warning')
        except Exception as e:
            self.log_message(f'❌ Error loading icon: {e}', 'error')
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = AnginaPortalChecker()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()