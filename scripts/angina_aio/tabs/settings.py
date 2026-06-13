from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QGroupBox, QMessageBox
from PyQt5.QtCore import Qt

class SettingsTab(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.app = parent_app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        group = QGroupBox("Global Settings")
        glayout = QVBoxLayout(group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Timeout (seconds):"))
        self.set_timeout = QSpinBox()
        self.set_timeout.setValue(self.app.config["timeout"])
        row1.addWidget(self.set_timeout)
        row1.addStretch()
        glayout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Max Threads:"))
        self.set_threads = QSpinBox()
        self.set_threads.setRange(1, 500)
        self.set_threads.setValue(self.app.config["max_threads"])
        row2.addWidget(self.set_threads)
        row2.addStretch()
        glayout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("User Agent:"))
        self.set_ua = QLineEdit()
        self.set_ua.setText(self.app.config["user_agent"])
        row3.addWidget(self.set_ua)
        glayout.addLayout(row3)

        btn = QPushButton("Save Settings")
        btn.setFixedWidth(150)
        btn.clicked.connect(self.save_settings)
        glayout.addWidget(btn)

        layout.addWidget(group)

    def save_settings(self):
        self.app.config["timeout"] = self.set_timeout.value()
        self.app.config["max_threads"] = self.set_threads.value()
        self.app.config["user_agent"] = self.set_ua.text()
        QMessageBox.information(self, "Success", "Settings saved successfully.")
