# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'ANGINA_MAC_Generator_PyQt4.py'
# Bytecode version: 3.8.0rc1+ (3413)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import os
import sys
import random
import time
import threading
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar, QCheckBox, QRadioButton, QButtonGroup, QScrollArea, QMessageBox, QFrame, QGroupBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
try:
    from tqdm import tqdm
except ImportError:
    print('Installing required package: tqdm')
    os.system(f'{sys.executable} -m pip install tqdm')
    from tqdm import tqdm
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, 'frozen', False):
    SCRIPT_NAME = os.path.splitext(os.path.basename(sys.executable))[0]
else:
    SCRIPT_NAME = os.path.splitext(os.path.basename(__file__))[0]
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, 'ANGINA_MAC_Generator_Plus')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
def get_icon_path():
    icon_name = 'MAC_Generator.ico'
    script_dir_icon = os.path.join(SCRIPT_DIR, icon_name)
    if os.path.exists(script_dir_icon):
        return script_dir_icon
    else:
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else SCRIPT_DIR
            bundled_icon = os.path.join(base_dir, icon_name)
            if os.path.exists(bundled_icon):
                return bundled_icon
        return None
PREFIXES = ['00:1A:79:', '74:1A:79:', '00:1A:70:', 'E0:37:17:', 'D4:CF:F9:', '33:44:CF:', '10:27:BE:', 'A0:BB:3E:', '55:93:EA:', '1A:00:FB:', '00:A1:79:', '00:1B:79:', '00:2A:79:', '00:2A:01:', '04:D6:AA:', '00:0C:29:', '00:50:56:', '00:05:69:', '00:1C:14:', '08:00:27:', '00:03:FF:', '00:25:90:', '00:26:75:', '00:E0:4C:', '00:90:0B:', '00:05:9A:', '00:1B:EA:', '00:1C:42:', '00:16:3E:', '00:14:22:', '00:30:18:', '00:21:5C:', '00:0F:4B:', '00:24:D4:', '00:11:D8:', '00:19:66:', '00:1F:16:', '00:20:91:', '00:40:96:', '00:60:2F:', '00:0A:27:', '00:1E:8A:', '00:1E:B8:', '18:C8:E7:', '1A:00:6A:', '30:87:30:', '00:09:DF:', '00:03:93:', '00:04:4F:', '0C:47:C9:', '68:FF:7B:', '00:1F:3A:', '08:9E:08:', '00:1D:20:', '00:09:18:', '00:1D:D5:', '00:01:5F:', '00:0E:8F:', '00:09:C7:', '00:1F:33:', '08:05:81:']
class SuffixLineEdit(QLineEdit):
    """Custom QLineEdit that automatically inserts colons for MAC suffix format"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_text = ''
        self.textChanged.connect(self.format_text)
    def format_text(self):
        current_text = self.text()
        if current_text == self.last_text:
            return None
        else:
            cursor_pos = self.cursorPosition()
            clean_text = current_text.replace(':', '').upper()
            clean_text = ''.join((c for c in clean_text if c in '0123456789ABCDEF'))
            clean_text = clean_text[:6]
            formatted_text = ''
            for i in range(0, len(clean_text), 2):
                if i > 0:
                    formatted_text += ':'
                formatted_text += clean_text[i:i + 2]
            self.last_text = formatted_text
            self.blockSignals(True)
            self.setText(formatted_text)
            self.blockSignals(False)
            if cursor_pos > 0:
                chars_before_cursor = 0
                for i in range(min(cursor_pos, len(current_text))):
                    if current_text[i]!= ':':
                        chars_before_cursor += 1
                new_pos = 0
                chars_counted = 0
                for i, char in enumerate(formatted_text):
                    if chars_counted >= chars_before_cursor:
                        break
                    else:
                        if char!= ':':
                            chars_counted += 1
                        new_pos = i + 1
                self.setCursorPosition(min(new_pos, len(formatted_text)))
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Backspace, Qt.Key_Delete]:
            cursor_pos = self.cursorPosition()
            text = self.text()
            if event.key() == Qt.Key_Backspace and cursor_pos > 0:
                if cursor_pos > 0 and text[cursor_pos - 1] == ':':
                        self.setCursorPosition(cursor_pos - 1)
            else:
                if event.key() == Qt.Key_Delete and cursor_pos < len(text) and (cursor_pos < len(text)) and (text[cursor_pos] == ':'):
                                self.setCursorPosition(cursor_pos + 1)
        super().keyPressEvent(event)
class CustomPrefixLineEdit(QLineEdit):
    """Custom QLineEdit that automatically inserts colons for MAC prefix format"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_text = ''
        self.textChanged.connect(self.format_text)
    def format_text(self):
        current_text = self.text()
        if current_text == self.last_text:
            return None
        else:
            cursor_pos = self.cursorPosition()
            clean_text = current_text.replace(':', '').upper()
            clean_text = ''.join((c for c in clean_text if c in '0123456789ABCDEF'))
            clean_text = clean_text[:6]
            formatted_text = ''
            for i in range(0, len(clean_text), 2):
                if i > 0:
                    formatted_text += ':'
                formatted_text += clean_text[i:i + 2]
            self.last_text = formatted_text
            self.blockSignals(True)
            self.setText(formatted_text)
            self.blockSignals(False)
            if cursor_pos > 0:
                chars_before_cursor = 0
                for i in range(min(cursor_pos, len(current_text))):
                    if current_text[i]!= ':':
                        chars_before_cursor += 1
                new_pos = 0
                chars_counted = 0
                for i, char in enumerate(formatted_text):
                    if chars_counted >= chars_before_cursor:
                        break
                    else:
                        if char!= ':':
                            chars_counted += 1
                        new_pos = i + 1
                self.setCursorPosition(min(new_pos, len(formatted_text)))
    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Backspace, Qt.Key_Delete]:
            cursor_pos = self.cursorPosition()
            text = self.text()
            if event.key() == Qt.Key_Backspace and cursor_pos > 0:
                if cursor_pos > 0 and text[cursor_pos - 1] == ':':
                        self.setCursorPosition(cursor_pos - 1)
            else:
                if event.key() == Qt.Key_Delete and cursor_pos < len(text) and (cursor_pos < len(text)) and (text[cursor_pos] == ':'):
                                self.setCursorPosition(cursor_pos + 1)
        super().keyPressEvent(event)
class GenerationThread(QThread):
    update_progress = pyqtSignal(int)
    update_status = pyqtSignal(str, str)
    update_details = pyqtSignal(str)
    log_message = pyqtSignal(str, str)
    generation_finished = pyqtSignal(bool)
    def __init__(self, prefixes, count_per_prefix, mode, custom_filename, start_suffix, finish_suffix):
        super().__init__()
        self.prefixes = prefixes
        self.count_per_prefix = count_per_prefix
        self.mode = mode
        self.custom_filename = custom_filename
        self.start_suffix = start_suffix
        self.finish_suffix = finish_suffix
        self.stop_generation = False
    def run(self):
        try:
            total_prefixes = len(self.prefixes)
            if self.start_suffix and self.finish_suffix:
                start_val = self.suffix_to_int(self.start_suffix)
                finish_val = self.suffix_to_int(self.finish_suffix)
                suffix_range = abs(finish_val - start_val) + 1
                total_macs = total_prefixes * min(self.count_per_prefix, suffix_range)
            else:
                total_macs = total_prefixes * self.count_per_prefix
            save_dir = self.ensure_output_folder()
            if not save_dir:
                return
            else:
                if self.custom_filename.strip():
                    base_name = self.custom_filename.strip()
                    if not base_name.endswith('.txt'):
                        base_name += '.txt'
                else:
                    formatted_count = self.format_number(total_macs)
                    base_name = f'Combo_ {formatted_count}.txt'
                filename = self.get_unique_filename(save_dir, base_name)
                filepath = os.path.join(save_dir, filename)
                start_time = time.time()
                self.log_message.emit(f'Output file: {filename}', 'info')
                if self.custom_filename.strip():
                    self.log_message.emit(f'Using custom filename: {self.custom_filename}', 'info')
                if self.mode == 'random':
                    total_generated, total_duplicates = self.generate_random_macs_optimized(filepath)
                else:
                    total_generated = self.generate_sequential_macs_optimized(filepath)
                    total_duplicates = 0
                if self.stop_generation:
                    self.log_message.emit('Generation stopped by user', 'warning')
                    self.generation_finished.emit(True)
                    return
                else:
                    end_time = time.time()
                    generation_time = end_time - start_time
                    self.log_message.emit(f'Generation completed in {generation_time:.2f} seconds!', 'success')
                    self.log_message.emit(f'Generated {self.format_number(total_generated)} unique MAC addresses', 'success')
                    if total_duplicates > 0:
                        self.log_message.emit(f'Duplicates found and removed: {total_duplicates}', 'warning')
                    self.log_message.emit(f'Saved to: {filepath}', 'success')
                    self.update_status.emit(f'Generated {self.format_number(total_generated)} MACs', 'success')
                    self.update_details.emit(f'Time: {generation_time:.2f}s | File: {filename}')
                    self.generation_finished.emit(False)
        except Exception as e:
            self.log_message.emit(f'Error during generation: {str(e)}', 'error')
            self.update_status.emit('Generation failed', 'error')
            self.generation_finished.emit(False)
    def stop(self):
        self.stop_generation = True
    def suffix_to_int(self, suffix_str):
        """Convert suffix string (XX:XX:XX) to integer"""
        hex_str = suffix_str.replace(':', '')
        return int(hex_str, 16)
    def int_to_suffix(self, value):
        """Convert integer to suffix string (XX:XX:XX)"""
        hex_str = format(value, '06X')
        return f'{hex_str[0:2]}:{hex_str[2:4]}:{hex_str[4:6]}'
    def format_mac_suffix(self, suffix_str):
        """Format a suffix string into MAC format (XX:XX:XX)"""
        return f'{suffix_str[0:2]}:{suffix_str[2:4]}:{suffix_str[4:6]}'
    def generate_random_macs_optimized(self, output_filepath):
        """Generate random MACs with proper uniqueness per prefix and final shuffling"""
        total_generated = 0
        total_duplicates = 0
        suffix_range = None
        if self.start_suffix and self.finish_suffix:
            start_val = self.suffix_to_int(self.start_suffix)
            finish_val = self.suffix_to_int(self.finish_suffix)
            suffix_range = (min(start_val, finish_val), max(start_val, finish_val))
            total_expected = len(self.prefixes) * min(self.count_per_prefix, suffix_range[1] - suffix_range[0] + 1)
            self.log_message.emit(f'Using suffix range: {self.int_to_suffix(suffix_range[0])} to {self.int_to_suffix(suffix_range[1])}', 'info')
        else:
            total_expected = len(self.prefixes) * self.count_per_prefix
        temp_filepath = output_filepath + '.tmp'
        with open(temp_filepath, 'w', encoding='utf-8') as f:
            for prefix_idx, prefix in enumerate(self.prefixes):
                if self.stop_generation:
                    break
                else:
                    used_suffixes = set()
                    prefix_generated = 0
                    prefix_duplicates = 0
                    self.update_status.emit(f'Random - Prefix {prefix_idx + 1}/{len(self.prefixes)}', 'accent')
                    self.update_details.emit(f'Prefix: {prefix} | Progress: {prefix_generated}/{self.count_per_prefix}')
                    while prefix_generated < self.count_per_prefix and (not self.stop_generation):
                        if suffix_range:
                            suffix_val = random.randint(suffix_range[0], suffix_range[1])
                            suffix = format(suffix_val, '06X')
                        else:
                            suffix = ''.join(random.choices('0123456789ABCDEF', k=6))
                        if suffix not in used_suffixes:
                            mac = prefix + self.format_mac_suffix(suffix)
                            f.write(mac + '\n')
                            used_suffixes.add(suffix)
                            prefix_generated += 1
                            total_generated += 1
                        else:
                            prefix_duplicates += 1
                            total_duplicates += 1
                        if total_generated % 1000 == 0:
                            progress = int(total_generated / total_expected * 100)
                            self.update_progress.emit(progress)
                    progress = int(total_generated / total_expected * 100)
                    self.update_progress.emit(progress)
                    if not self.stop_generation:
                        self.log_message.emit(f'Completed prefix {prefix} - {prefix_generated} MACs (duplicates: {prefix_duplicates})', 'success')
        if not self.stop_generation:
            self.log_message.emit('Shuffling MAC addresses for final output...', 'info')
            total_generated = self.shuffle_output_file(temp_filepath, output_filepath)
            try:
                os.remove(temp_filepath)
            except:
                pass
        return (total_generated, total_duplicates)
    def generate_sequential_macs_optimized(self, output_filepath):
        """Generate sequential MACs with exact range coverage"""
        total_generated = 0
        if self.start_suffix and self.finish_suffix:
            start_val = self.suffix_to_int(self.start_suffix)
            finish_val = self.suffix_to_int(self.finish_suffix)
            if self.mode == 'ascending':
                range_start = min(start_val, finish_val)
                range_end = max(start_val, finish_val)
            else:
                range_start = max(start_val, finish_val)
                range_end = min(start_val, finish_val)
            total_range = abs(range_end - range_start) + 1
            actual_count = min(self.count_per_prefix, total_range)
            if actual_count == 1:
                suffix_values = [range_start]
            else:
                if actual_count == total_range:
                    if self.mode == 'ascending':
                        suffix_values = list(range(range_start, range_end + 1))
                    else:
                        suffix_values = list(range(range_start, range_end - 1, (-1)))
                else:
                    step = (total_range - 1) / (actual_count - 1)
                    suffix_values = []
                    for i in range(actual_count):
                        if self.mode == 'ascending':
                            value = int(round(range_start + i * step))
                            if value > range_end:
                                value = range_end
                        else:
                            value = int(round(range_start - i * step))
                            if value < range_end:
                                value = range_end
                        suffix_values.append(value)
            self.log_message.emit(f'Using suffix range: {self.int_to_suffix(range_start)} to {self.int_to_suffix(range_end)}', 'info')
            self.log_message.emit(f'Generating {actual_count} values from range of {total_range}', 'info')
        else:
            actual_count = min(self.count_per_prefix, 16777216)
            if self.mode == 'ascending':
                suffix_values = list(range(actual_count))
            else:
                max_suffix_value = 16777215
                suffix_values = list(range(max_suffix_value, max_suffix_value - actual_count, (-1)))
            self.log_message.emit(f'Generating {actual_count} sequential values', 'info')
            if actual_count < self.count_per_prefix:
                self.log_message.emit(f'Limited to {self.format_number(actual_count)} per prefix (max suffix limit)', 'warning')
        total_expected = len(self.prefixes) * len(suffix_values)
        with open(output_filepath, 'w', encoding='utf-8', buffering=8192) as f:
            batch_lines = []
            current_batch_size = 0
            self.update_status.emit(f'{self.mode.capitalize()} - Generating MACs', 'accent')
            self.update_details.emit(f'{len(self.prefixes)} prefixes | Progress: 0/{len(suffix_values)}')
            for suffix_val in suffix_values:
                if self.stop_generation:
                    break
                else:
                    for prefix in self.prefixes:
                        suffix = format(suffix_val, '06X')
                        mac = prefix + self.format_mac_suffix(suffix) + '\n'
                        batch_lines.append(mac)
                        total_generated += 1
                        current_batch_size += 1
                    if current_batch_size >= 10000:
                        f.writelines(batch_lines)
                        batch_lines = []
                        current_batch_size = 0
                    progress = int(total_generated / total_expected * 100)
                    self.update_progress.emit(progress)
                    self.update_details.emit(f'Generated: {self.format_number(total_generated)} / {self.format_number(total_expected)}')
            if batch_lines and (not self.stop_generation):
                    f.writelines(batch_lines)
            if not self.stop_generation:
                self.log_message.emit(f'Completed sequential generation - {total_generated} MACs', 'success')
                if suffix_values:
                    first_suffix = suffix_values[0]
                    last_suffix = suffix_values[(-1)]
                    self.log_message.emit(f'Actual range used: {self.int_to_suffix(first_suffix)} to {self.int_to_suffix(last_suffix)}', 'info')
        return total_generated
    def shuffle_output_file(self, input_filepath, output_filepath):
        """Shuffle the contents of a file (for random mode final shuffle)"""
        self.log_message.emit('Shuffling MAC addresses...', 'info')
        with open(input_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        random.shuffle(lines)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        self.log_message.emit(f'Shuffled {len(lines)} MAC addresses', 'success')
        return len(lines)
    def ensure_output_folder(self):
        try:
            if not os.path.exists(OUTPUT_FOLDER):
                os.makedirs(OUTPUT_FOLDER)
                self.log_message.emit(f'Created output folder: {OUTPUT_FOLDER}', 'success')
            return OUTPUT_FOLDER
        except Exception as e:
            self.log_message.emit(f'Error creating output folder: {str(e)}', 'error')
            return None
    def get_unique_filename(self, directory, base_name):
        name, ext = os.path.splitext(base_name)
        counter = 1
        new_name = base_name
        while os.path.exists(os.path.join(directory, new_name)):
            new_name = f'{name}-{counter}{ext}'
            counter += 1
        return new_name
    def format_number(self, n):
        if n >= 1000000:
            return f'{n / 1000000:.1f}M'.replace('.0', '')
        else:
            if n >= 1000:
                return f'{n / 1000:.1f}K'.replace('.0', '')
            else:
                return str(n)
class ModernMACGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generation_thread = None
        self.stop_generation = False
        self.bg_color = QColor(30, 30, 30)
        self.card_bg = QColor(45, 45, 45)
        self.accent_color = QColor(187, 134, 252)
        self.text_color = QColor(255, 255, 255)
        self.secondary_text = QColor(176, 176, 176)
        self.success_color = QColor(3, 218, 198)
        self.warning_color = QColor(255, 183, 77)
        self.error_color = QColor(207, 102, 121)
        self.setup_ui()
        self.apply_dark_theme()
        self.update_status_display()
    def setup_ui(self):
        self.setWindowTitle('🖤ANGINA™🖤 MAC GENERATOR PLUS 🔢')
        self.setGeometry(100, 100, 1200, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        header_layout = QVBoxLayout()
        title_label = QLabel('🖤ANGINA™🖤 MAC GENERATOR PLUS 🔢')
        title_label.setStyleSheet(f'font-size: 16pt; font-weight: bold; color: {self.accent_color.name()};')
        header_layout.addWidget(title_label)
        subtitle_label = QLabel('⚙️ MAC Address Generation and Combination Tool ⚙️')
        subtitle_label.setStyleSheet(f'color: {self.secondary_text.name()};')
        header_layout.addWidget(subtitle_label)
        main_layout.addLayout(header_layout)
        config_group = QGroupBox('⚙️ Configuration:')
        config_group.setStyleSheet(self.get_groupbox_style())
        config_layout = QVBoxLayout(config_group)
        top_row_layout = QHBoxLayout()
        count_layout = QVBoxLayout()
        count_label = QLabel('🔵 MACs Count/Prefix:')
        count_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        count_layout.addWidget(count_label)
        self.count_edit = QLineEdit()
        self.count_edit.setStyleSheet(self.get_line_edit_style())
        self.count_edit.setPlaceholderText('10000')
        self.count_edit.setMaximumWidth(130)
        count_layout.addWidget(self.count_edit)
        top_row_layout.addLayout(count_layout)
        mode_layout = QHBoxLayout()
        mode_label = QLabel('                                                        🔵 Generation Mode: ')
        mode_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        mode_layout.addWidget(mode_label)
        mode_buttons_layout = QVBoxLayout()
        self.mode_group = QButtonGroup()
        modes = [('Random', 'random'), ('Ascending', 'ascending'), ('Descending', 'descending')]
        for text, mode in modes:
            radio = QRadioButton(text)
            radio.setStyleSheet(self.get_radio_button_style())
            self.mode_group.addButton(radio)
            mode_buttons_layout.addWidget(radio)
            if mode == 'random':
                radio.setChecked(True)
        mode_layout.addLayout(mode_buttons_layout)
        top_row_layout.addLayout(mode_layout)
        button_layout = QVBoxLayout()
        self.generate_btn = QPushButton('🎲 GENERATE')
        self.generate_btn.setStyleSheet(self.get_generate_button_style())
        self.generate_btn.clicked.connect(self.start_generation)
        self.generate_btn.setMaximumWidth(300)
        self.stop_btn = QPushButton('⏹️ STOP')
        self.stop_btn.setStyleSheet(self.get_stop_button_style())
        self.stop_btn.clicked.connect(self.stop_generation_process)
        self.stop_btn.setMaximumWidth(300)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.stop_btn)
        top_row_layout.addLayout(button_layout)
        config_layout.addLayout(top_row_layout)
        suffix_layout = QHBoxLayout()
        custom_prefix_layout = QHBoxLayout()
        custom_prefix_label = QLabel('🔵 Custom Prefix:')
        custom_prefix_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        custom_prefix_layout.addWidget(custom_prefix_label)
        self.custom_prefix_edit = CustomPrefixLineEdit()
        self.custom_prefix_edit.setStyleSheet(self.get_line_edit_style())
        self.custom_prefix_edit.setPlaceholderText('XX:XX:XX')
        self.custom_prefix_edit.setMaximumWidth(120)
        self.custom_prefix_edit.textChanged.connect(self.update_status_display)
        custom_prefix_layout.addWidget(self.custom_prefix_edit)
        suffix_layout.addLayout(custom_prefix_layout)
        start_suffix_layout = QHBoxLayout()
        start_suffix_label = QLabel('                         🔵 Custom Suffix:               💠 Suffix Start: ')
        start_suffix_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        start_suffix_layout.addWidget(start_suffix_label)
        self.start_suffix_edit = SuffixLineEdit()
        self.start_suffix_edit.setStyleSheet(self.get_line_edit_style())
        self.start_suffix_edit.setPlaceholderText('00:00:00')
        self.start_suffix_edit.setMaximumWidth(120)
        self.start_suffix_edit.textChanged.connect(self.update_status_display)
        start_suffix_layout.addWidget(self.start_suffix_edit)
        suffix_layout.addLayout(start_suffix_layout)
        finish_suffix_layout = QHBoxLayout()
        finish_suffix_label = QLabel('                                    💠 Suffix Finish: ')
        finish_suffix_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        finish_suffix_layout.addWidget(finish_suffix_label)
        self.finish_suffix_edit = SuffixLineEdit()
        self.finish_suffix_edit.setStyleSheet(self.get_line_edit_style())
        self.finish_suffix_edit.setPlaceholderText('FF:FF:FF')
        self.finish_suffix_edit.setMaximumWidth(120)
        self.finish_suffix_edit.textChanged.connect(self.update_status_display)
        finish_suffix_layout.addWidget(self.finish_suffix_edit)
        suffix_layout.addLayout(finish_suffix_layout)
        info_label = QLabel('   🔴 Leave Empty To Use Default!      ')
        info_label.setStyleSheet(f'color: {self.secondary_text.name()}; font-size: 9pt;')
        suffix_layout.addWidget(info_label)
        clear_btn = QPushButton('      ♻️️      CLEAR       ')
        clear_btn.setStyleSheet(self.get_stop_button_style())
        clear_btn.setMaximumWidth(100)
        clear_btn.clicked.connect(self.clear_suffix_fields)
        suffix_layout.addWidget(clear_btn)
        suffix_layout.addStretch()
        config_layout.addLayout(suffix_layout)
        filename_layout = QHBoxLayout()
        filename_label = QLabel('🔵 Custom File Name:    ')
        filename_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        filename_layout.addWidget(filename_label)
        self.filename_edit = QLineEdit()
        self.filename_edit.setStyleSheet(self.get_line_edit_style())
        self.filename_edit.setPlaceholderText('Enter Combo File Name Or Leave Empty To Use Default!')
        filename_layout.addWidget(self.filename_edit)
        config_layout.addLayout(filename_layout)
        main_layout.addWidget(config_group)
        prefix_group = QGroupBox('🔢 Select MAC Prefix(es):')
        prefix_group.setStyleSheet(self.get_groupbox_style())
        prefix_layout = QVBoxLayout(prefix_group)
        header_label = QLabel('🟢 Available (38) MAC Prefixes (Select One, Multiple or All prefixes):')
        header_label.setStyleSheet(f'color: {self.accent_color.name()}; font-weight: bold;')
        prefix_layout.addWidget(header_label)
        select_layout = QHBoxLayout()
        select_all_btn = QPushButton('✔️ Select All')
        select_all_btn.setStyleSheet(self.get_generate_button_style())
        select_all_btn.clicked.connect(self.select_all_prefixes)
        select_layout.addWidget(select_all_btn)
        select_none_btn = QPushButton('✖ Select None')
        select_none_btn.setStyleSheet(self.get_stop_button_style())
        select_none_btn.clicked.connect(self.select_no_prefixes)
        select_layout.addWidget(select_none_btn)
        select_layout.addStretch()
        prefix_layout.addLayout(select_layout)
        self.prefix_checkboxes = []
        prefix_grid_layout = QVBoxLayout()
        prefixes_per_row = [9, 9, 9, 9, 2]
        prefix_index = 0
        for row_num, count_in_row in enumerate(prefixes_per_row):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(5)
            for col in range(count_in_row):
                if prefix_index >= len(PREFIXES):
                    break
                else:
                    prefix = PREFIXES[prefix_index]
                    cb = QCheckBox(prefix)
                    cb.setStyleSheet(self.get_prefix_checkbox_style())
                    cb.toggled.connect(self.update_status_display)
                    self.prefix_checkboxes.append(cb)
                    row_layout.addWidget(cb)
                    prefix_index += 1
            row_layout.addStretch()
            prefix_grid_layout.addLayout(row_layout)
        prefix_layout.addLayout(prefix_grid_layout)
        main_layout.addWidget(prefix_group)
        progress_group = QGroupBox('📚 Progress & Output:')
        progress_group.setStyleSheet(self.get_groupbox_style())
        progress_layout = QVBoxLayout(progress_group)
        progress_label = QLabel('🟠 Generation Progress:')
        progress_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        progress_layout.addWidget(progress_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(self.get_progressbar_style())
        progress_layout.addWidget(self.progress_bar)
        self.status_label = QLabel('Ready to generate - Select prefixes first')
        self.status_label.setStyleSheet(f'color: {self.warning_color.name()}; font-weight: bold;')
        progress_layout.addWidget(self.status_label)
        self.details_label = QLabel('No prefixes selected - please choose prefixes to generate')
        self.details_label.setStyleSheet(f'color: {self.secondary_text.name()};')
        progress_layout.addWidget(self.details_label)
        log_label = QLabel('🟠 Generation Log:')
        log_label.setStyleSheet(f'font-weight: bold; color: {self.accent_color.name()};')
        progress_layout.addWidget(log_label)
        self.log_text = QTextEdit()
        self.log_text.setStyleSheet(self.get_textedit_style())
        self.log_text.setReadOnly(True)
        progress_layout.addWidget(self.log_text)
        main_layout.addWidget(progress_group)
    def clear_suffix_fields(self):
        """Clear both suffix fields and custom prefix"""
        self.start_suffix_edit.clear()
        self.finish_suffix_edit.clear()
        self.custom_prefix_edit.clear()
    def update_status_display(self):
        """Update the status label to show current configuration"""
        selected_count = sum((1 for cb in self.prefix_checkboxes if cb.isChecked()))
        start_suffix = self.start_suffix_edit.text().strip().upper()
        finish_suffix = self.finish_suffix_edit.text().strip().upper()
        custom_prefix = self.custom_prefix_edit.text().strip().upper()
        use_custom_prefix = bool(custom_prefix)
        if selected_count == 0 and (not use_custom_prefix):
            status_text = 'Ready to generate - No prefixes selected'
            color = self.warning_color.name()
            details_text = 'Please select at least one prefix or enter custom prefix'
        else:
            status_parts = []
            if use_custom_prefix:
                status_parts.append('Custom prefix enabled')
            if selected_count > 0:
                status_parts.append(f'{selected_count} prefix(es) selected')
            if start_suffix and finish_suffix:
                status_parts.append(f'Suffix range: {start_suffix} to {finish_suffix}')
            else:
                if start_suffix:
                    status_parts.append(f'Start suffix: {start_suffix}')
                else:
                    if finish_suffix:
                        status_parts.append(f'Finish suffix: {finish_suffix}')
            status_text = ' | '.join(status_parts) if status_parts else 'Ready to generate'
            color = self.success_color.name()
            details_parts = []
            if use_custom_prefix:
                details_parts.append(f'Custom prefix: {custom_prefix}')
            if selected_count > 0:
                if selected_count == len(PREFIXES):
                    details_parts.append('All prefixes selected')
                else:
                    details_parts.append(f'{selected_count} individual prefix(es) selected')
            if start_suffix and finish_suffix:
                details_parts.append(f'Custom suffix range: {start_suffix} to {finish_suffix}')
            else:
                if start_suffix:
                    details_parts.append(f'Custom start suffix: {start_suffix} (finish: FF:FF:FF)')
                else:
                    if finish_suffix:
                        details_parts.append(f'Custom finish suffix: {finish_suffix} (start: 00:00:00)')
                    else:
                        details_parts.append('Full suffix range (00:00:00 to FF:FF:FF)')
            details_text = ' | '.join(details_parts) if details_parts else 'Default configuration'
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(f'color: {color}; font-weight: bold;')
        self.details_label.setText(details_text)
    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, self.bg_color)
        palette.setColor(QPalette.WindowText, self.text_color)
        palette.setColor(QPalette.Base, QColor(45, 45, 45))
        palette.setColor(QPalette.AlternateBase, self.bg_color)
        palette.setColor(QPalette.ToolTipBase, self.text_color)
        palette.setColor(QPalette.ToolTipText, self.text_color)
        palette.setColor(QPalette.Text, self.text_color)
        palette.setColor(QPalette.Button, self.card_bg)
        palette.setColor(QPalette.ButtonText, self.text_color)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, self.accent_color)
        palette.setColor(QPalette.Highlight, self.accent_color)
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
    def get_groupbox_style(self):
        # ***<module>.ModernMACGenerator.get_groupbox_style: Failure: Compilation Error
        return f'\n            QGroupBox {\n                color: {self.text_color.name()};\n                font-weight: bold;\n                border: 1px solid {self.card_bg.lighter(120).name()};\n                border-radius: 5px;\n                margin-top: 1ex;\n                padding-top: 10px;\n            }\n            QGroupBox::title {\n                subcontrol-origin: margin;\n                left: 10px;\n                padding: 0 5px 0 5px;\n            }\n        '
    def get_line_edit_style(self):
        # ***<module>.ModernMACGenerator.get_line_edit_style: Failure: Compilation Error
        return f'\n            QLineEdit {\n                background-color: #3d3d3d;\n                color: {self.text_color.name()};\n                border: 1px solid #555;\n                border-radius: 3px;\n                padding: 5px;\n            }\n        '
    def get_radio_button_style(self):
        # ***<module>.ModernMACGenerator.get_radio_button_style: Failure: Compilation Error
        return f'\n            QRadioButton {\n                color: {self.text_color.name()};\n            }\n            QRadioButton::indicator {\n                width: 13px;\n                height: 13px;\n            }\n            QRadioButton::indicator::unchecked {\n                border: 1px solid #777;\n                border-radius: 7px;\n                background-color: #2d2d2d;\n            }\n            QRadioButton::indicator::checked {\n                border: 1px solid {self.accent_color.name()};\n                border-radius: 7px;\n                background-color: {self.accent_color.name()};\n            }\n        '
    def get_checkbox_style(self):
        # ***<module>.ModernMACGenerator.get_checkbox_style: Failure: Compilation Error
        return f'\n            QCheckBox {\n                color: {self.accent_color.name()};\n                font-weight: bold;\n            }\n            QCheckBox::indicator {\n                width: 13px;\n                height: 13px;\n            }\n            QCheckBox::indicator::unchecked {\n                border: 1px solid #777;\n                border-radius: 2px;\n                background-color: {self.bg_color.name()};\n            }\n            QCheckBox::indicator::checked {\n                border: 1px solid {self.accent_color.name()};\n                border-radius: 2px;\n                background-color: {self.accent_color.name()};\n            }\n        '
    def get_prefix_checkbox_style(self):
        # ***<module>.ModernMACGenerator.get_prefix_checkbox_style: Failure: Compilation Error
        return f'\n            QCheckBox {\n                color: {self.text_color.name()};\n                font-family: \'Courier New\';\n            }\n            QCheckBox::indicator {\n                width: 13px;\n                height: 13px;\n            }\n            QCheckBox::indicator::unchecked {\n                border: 1px solid #777;\n                border-radius: 2px;\n                background-color: {self.card_bg.name()};\n            }\n            QCheckBox::indicator::checked {\n                border: 1px solid {self.accent_color.name()};\n                border-radius: 2px;\n                background-color: {self.accent_color.name()};\n            }\n        '
    def get_generate_button_style(self):
        # ***<module>.ModernMACGenerator.get_generate_button_style: Failure: Compilation Error
        return f'\n            QPushButton {\n                background-color: {self.accent_color.name()};\n                color: black;\n                font-weight: bold;\n                border: none;\n                border-radius: 4px;\n                padding: 8px 15px;\n            }\n            QPushButton:hover {\n                background-color: {self.accent_color.lighter(120).name()};\n            }\n            QPushButton:disabled {\n                background-color: #555;\n                color: #888;\n            }\n        '
    def get_stop_button_style(self):
        # ***<module>.ModernMACGenerator.get_stop_button_style: Failure: Compilation Error
        return f'\n            QPushButton {\n                background-color: {self.error_color.name()};\n                color: black;\n                font-weight: bold;\n                border: none;\n                border-radius: 4px;\n                padding: 8px 15px;\n            }\n            QPushButton:hover {\n                background-color: {self.error_color.lighter(120).name()};\n            }\n            QPushButton:disabled {\n                background-color: #555;\n                color: #888;\n            }\n        '
    def get_small_button_style(self):
        # ***<module>.ModernMACGenerator.get_small_button_style: Failure: Compilation Error
        return f'\n            QPushButton {\n                background-color: #3d3d3d;\n                color: {self.text_color.name()};\n                border: none;\n                border-radius: 3px;\n                padding: 5px 10px;\n            }\n            QPushButton:hover {\n                background-color: #4d4d4d;\n            }\n        '
    def get_progressbar_style(self):
        # ***<module>.ModernMACGenerator.get_progressbar_style: Failure: Compilation Error
        return f'\n            QProgressBar {\n                border: 1px solid #555;\n                border-radius: 3px;\n                text-align: center;\n                background-color: #2d2d2d;\n            }\n            QProgressBar::chunk {\n                background-color: {self.accent_color.name()};\n                width: 1px;\n            }\n        '
    def get_textedit_style(self):
        # ***<module>.ModernMACGenerator.get_textedit_style: Failure: Compilation Error
        return f'\n            QTextEdit {\n                background-color: #3d3d3d;\n                color: {self.text_color.name()};\n                border: 1px solid #555;\n                border-radius: 3px;\n                font-family: \'Calibri\';\n                font-size: 9pt;\n            }\n        '
    def select_all_prefixes(self):
        for cb in self.prefix_checkboxes:
            cb.setChecked(True)
        self.update_status_display()
    def select_no_prefixes(self):
        for cb in self.prefix_checkboxes:
            cb.setChecked(False)
        self.update_status_display()
    def validate_suffix(self, suffix):
        """Validate suffix format (XX:XX:XX)"""
        if not suffix:
            return (True, None)
        else:
            parts = suffix.split(':')
            if len(parts)!= 3:
                return (False, 'Suffix must be in format XX:XX:XX')
            else:
                for part in parts:
                    if len(part)!= 2:
                        return (False, 'Each part must be 2 characters')
                    else:
                        try:
                            int(part, 16)
                        except ValueError:
                            return (False, 'Suffix must contain valid hexadecimal values')
                return (True, None)
    def validate_prefix(self, prefix):
        """Validate prefix format (XX:XX:XX)"""
        if not prefix:
            return (False, 'Custom prefix cannot be empty')
        else:
            parts = prefix.split(':')
            if len(parts)!= 3:
                return (False, 'Prefix must be in format XX:XX:XX')
            else:
                for part in parts:
                    if len(part)!= 2:
                        return (False, 'Each part must be 2 characters')
                    else:
                        try:
                            int(part, 16)
                        except ValueError:
                            return (False, 'Prefix must contain valid hexadecimal values')
                return (True, None)
    def log_message(self, message, color_type=None):
        timestamp = datetime.now().strftime('%I:%M:%S %p')
        if color_type == 'success':
            color = self.success_color.name()
        else:
            if color_type == 'warning':
                color = self.warning_color.name()
            else:
                if color_type == 'error':
                    color = self.error_color.name()
                else:
                    if color_type == 'info':
                        color = self.accent_color.name()
                    else:
                        color = self.text_color.name()
        formatted_message = f'<span style=\"color: {self.secondary_text.name()}\">[{timestamp}]</span> <span style=\"color: {color}\">{message}</span><br>'
        self.log_text.moveCursor(self.log_text.textCursor().End)
        self.log_text.insertHtml(formatted_message)
        self.log_text.ensureCursorVisible()
    def start_generation(self):
        try:
            count = int(self.count_edit.text())
            if count <= 0:
                QMessageBox.critical(self, 'Error', 'Please enter a positive number')
                return
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Please enter a valid number')
            return
        selected_prefixes = [PREFIXES[i] for i, cb in enumerate(self.prefix_checkboxes) if cb.isChecked()]
        custom_prefix = self.custom_prefix_edit.text().strip().upper()
        use_custom_prefix = bool(custom_prefix)
        if not selected_prefixes and (not use_custom_prefix):
            QMessageBox.critical(self, 'Error', 'Please select at least one MAC prefix or enter custom prefix')
            return None
        else:
            if use_custom_prefix:
                valid, error = self.validate_prefix(custom_prefix)
                if not valid:
                    QMessageBox.critical(self, 'Error', f'Invalid custom prefix: {error}')
                    return None
                else:
                    if not custom_prefix.endswith(':'):
                        custom_prefix += ':'
                    selected_prefixes.append(custom_prefix)
            mode = 'random'
            for button in self.mode_group.buttons():
                if button.isChecked():
                    mode = button.text().lower()
                    break
            custom_filename = self.filename_edit.text().strip()
            start_suffix = self.start_suffix_edit.text().strip().upper()
            finish_suffix = self.finish_suffix_edit.text().strip().upper()
            if start_suffix or finish_suffix:
                if start_suffix:
                    valid, error = self.validate_suffix(start_suffix)
                    if not valid:
                        QMessageBox.critical(self, 'Error', f'Invalid start suffix: {error}')
                        return None
                if finish_suffix:
                    valid, error = self.validate_suffix(finish_suffix)
                    if not valid:
                        QMessageBox.critical(self, 'Error', f'Invalid finish suffix: {error}')
                        return None
                if start_suffix and (not finish_suffix):
                    finish_suffix = 'FF:FF:FF'
                else:
                    if finish_suffix and (not start_suffix):
                            start_suffix = '00:00:00'
            self.generate_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status_label.setText('Generation in progress...')
            self.status_label.setStyleSheet(f'color: {self.accent_color.name()}; font-weight: bold;')
            self.progress_bar.setValue(0)
            self.log_message('Starting MAC address generation...', 'info')
            self.log_message(f'Mode: {mode.capitalize()}', 'info')
            if use_custom_prefix:
                self.log_message(f'Using custom prefix: {custom_prefix}', 'info')
            self.log_message(f'Prefixes: {len(selected_prefixes)}', 'info')
            self.log_message(f'Count per prefix: {count}', 'info')
            if start_suffix and finish_suffix:
                    self.log_message(f'Suffix range: {start_suffix} to {finish_suffix}', 'info')
            if custom_filename:
                self.log_message(f'Custom filename: {custom_filename}', 'info')
            self.generation_thread = GenerationThread(selected_prefixes, count, mode, custom_filename, start_suffix, finish_suffix)
            self.generation_thread.update_progress.connect(self.progress_bar.setValue)
            self.generation_thread.update_status.connect(self.update_status)
            self.generation_thread.update_details.connect(self.details_label.setText)
            self.generation_thread.log_message.connect(self.log_message)
            self.generation_thread.generation_finished.connect(self.generation_finished)
            self.generation_thread.start()
    def update_status(self, text, color_type):
        if color_type == 'success':
            color = self.success_color.name()
        else:
            if color_type == 'error':
                color = self.error_color.name()
            else:
                if color_type == 'warning':
                    color = self.warning_color.name()
                else:
                    color = self.accent_color.name()
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f'color: {color}; font-weight: bold;')
    def stop_generation_process(self):
        if self.generation_thread and self.generation_thread.isRunning():
                self.generation_thread.stop()
                self.status_label.setText('Stopping generation...')
                self.status_label.setStyleSheet(f'color: {self.warning_color.name()}; font-weight: bold;')
                self.log_message('Stopping generation...', 'warning')
    def generation_finished(self, stopped=False):
        self.generate_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if stopped:
            self.status_label.setText('Generation stopped')
            self.status_label.setStyleSheet(f'color: {self.warning_color.name()}; font-weight: bold;')
        else:
            self.progress_bar.setValue(100)
        self.update_status_display()
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ModernMACGenerator()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()