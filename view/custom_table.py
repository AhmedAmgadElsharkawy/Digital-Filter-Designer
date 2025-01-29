from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QDoubleSpinBox, QPushButton, QLabel, QCheckBox, QTableWidget
)
from PyQt5.QtCore import Qt


class CustomTable(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        self.real_part_spin = QDoubleSpinBox()
        self.real_part_spin.setMinimum(-1000.0)
        self.real_part_spin.setMaximum(1000.0)
        self.real_part_spin.setValue(0)
        self.real_part_spin.setDecimals(2)
        self.real_part_spin.setSingleStep(0.1)
        self.real_part_spin.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.real_part_spin.setMaximumWidth(100)
        self.input_layout.addWidget(QLabel("Real:"))
        self.input_layout.addWidget(self.real_part_spin)

        self.imaginary_part_spin = QDoubleSpinBox()
        self.imaginary_part_spin.setMinimum(-1000.0)
        self.imaginary_part_spin.setMaximum(1000.0)
        self.imaginary_part_spin.setValue(0)
        self.imaginary_part_spin.setDecimals(2)
        self.imaginary_part_spin.setSingleStep(0.1)
        self.imaginary_part_spin.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.imaginary_part_spin.setMaximumWidth(100)
        self.input_layout.addWidget(QLabel("Imag:"))
        self.input_layout.addWidget(self.imaginary_part_spin)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_to_table)
        self.input_layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Complex", "Select"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, 1)
        self.table.horizontalHeader().setSectionResizeMode(1, 1)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.main_layout.addWidget(self.table)
        self.main_layout.addLayout(self.input_layout)

        self.setLayout(self.main_layout)

    def add_to_table(self):
        real = self.real_part_spin.value()
        imag = self.imaginary_part_spin.value()

        complex_number = complex(real, imag)

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(str(complex_number)))

        checkbox = QCheckBox()
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        self.table.setCellWidget(row_position, 1, checkbox_widget)

        self.real_part_spin.setValue(0)
        self.imaginary_part_spin.setValue(0)
