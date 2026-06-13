import os
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QGroupBox, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class MacGenTab(QWidget):
    def __init__(self, parent_app):
        super().__init__()
        self.app = parent_app
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
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
        self.mac_amount.setRange(1, 1000000)
        self.mac_amount.setValue(1000)
        row2.addWidget(self.mac_amount)
        row2.addStretch()
        glayout.addLayout(row2)

        btn = QPushButton("Generate & Save to TXT")
        btn.setFixedWidth(200)
        btn.clicked.connect(self.generate_macs)
        glayout.addWidget(btn)

        layout.addWidget(group)

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
