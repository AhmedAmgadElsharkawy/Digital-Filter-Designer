from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QDoubleSpinBox, QPushButton, QLabel, QCheckBox, QTableWidget
)
from PyQt5.QtCore import Qt

from view.custom_double_spin_box import CustomDoubleSpinBox


class CustomTable(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.input_layout = QHBoxLayout()
        self.input_layout.setContentsMargins(0, 0, 0, 0)

        

        self.real_part_spin = CustomDoubleSpinBox(label = "Real:",range_start=-1000,range_end=1000,step_value=0.1,initial_value=0,decimals=2)
        self.input_layout.addWidget(self.real_part_spin)

        self.imaginary_part_spin = CustomDoubleSpinBox(label = "Imag:",range_start=-1000,range_end=1000,step_value=0.1,initial_value=0,decimals=2)
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

        if real == 0 and imag == 0:
            return

        complex_number = complex(real, imag)
        idx = self.all_pass_filter_controller.add_filter(complex_number)

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        self.table.setItem(row_position, 0, QTableWidgetItem(str(complex_number)))

        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda state: self.all_pass_filter_controller.checkbox_state_changed(idx, state))
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.setAlignment(Qt.AlignCenter)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        self.table.setCellWidget(row_position, 1, checkbox_widget)

        self.real_part_spin.setValue(0)
        self.imaginary_part_spin.setValue(0)