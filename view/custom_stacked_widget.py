from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QStackedWidget, QLabel, QHBoxLayout

class CustomStackedWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.central_layout)

        self.buttons_widget = QWidget()
        self.buttons_widget_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_structure = QPushButton('Structure', self)
        self.btn_code = QPushButton('Code', self)

        self.buttons_widget_layout.addWidget(self.btn_structure)
        self.buttons_widget_layout.addWidget(self.btn_code)

        self.central_layout.addWidget(self.buttons_widget)

        self.stack = QStackedWidget(self)
        self.central_layout.addWidget(self.stack)

        self.structure_widget = QLabel("Structure View")
        self.code_widget = QLabel("Code View")

        self.stack.addWidget(self.structure_widget)
        self.stack.addWidget(self.code_widget)

        self.btn_structure.clicked.connect(lambda: self.switch_view(0))
        self.btn_code.clicked.connect(lambda: self.switch_view(1))


    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        self.btn_structure.setDisabled(index == 0)
        self.btn_code.setDisabled(index == 1)
