from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QPushButton

from view.custom_z_plane import CustomZPlane


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fingerprint')
        self.setGeometry(300,300,1300, 500)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setSpacing(10)


        self.controls_widget = QWidget()
        self.controls_widget_layout = QHBoxLayout(self.controls_widget)
        self.main_widget_layout.addWidget(self.controls_widget)

        self.poles_zeroes_widget = QWidget()
        self.poles_zeroes_widget_layout = QHBoxLayout(self.poles_zeroes_widget)
        self.controls_widget_layout.addWidget(self.poles_zeroes_widget)
        self.pole_button = QPushButton("pole")
        self.zero_button = QPushButton("zero")
        self.conjugate_poles_button = QPushButton("conj poles")
        self.conjugate_zeroes_button = QPushButton("conj zeroes")
        self.poles_zeroes_widget_layout.addWidget(self.pole_button)
        self.poles_zeroes_widget_layout.addWidget(self.zero_button)
        self.poles_zeroes_widget_layout.addWidget(self.conjugate_poles_button)
        self.poles_zeroes_widget_layout.addWidget(self.conjugate_zeroes_button)
        self.pole_button.setDisabled(True)

        self.swap_controls_widget = QWidget()
        self.swap_controls_widget_layout = QHBoxLayout(self.swap_controls_widget)
        self.controls_widget_layout.addWidget(self.swap_controls_widget)
        self.swap_poles_button = QPushButton("Swap poles")
        self.swap_zeroes_button = QPushButton("Swap Zeroes")
        self.swap_controls_widget_layout.addWidget(self.swap_poles_button)
        self.swap_controls_widget_layout.addWidget(self.swap_zeroes_button)

        self.clear_controls_widget = QWidget()
        self.clear_controls_widget_layout = QHBoxLayout(self.clear_controls_widget)
        self.controls_widget_layout.addWidget(self.clear_controls_widget)
        self.clear_poles_button = QPushButton("Clear Poles")
        self.clear_zeroes_button = QPushButton("Clear Zeroes")
        self.clear_all_poles_and_zeroes_button = QPushButton("Clear All")
        self.clear_controls_widget_layout.addWidget(self.clear_poles_button)
        self.clear_controls_widget_layout.addWidget(self.clear_zeroes_button)
        self.clear_controls_widget_layout.addWidget(self.clear_all_poles_and_zeroes_button)
        

        self.filter_row = QWidget()
        self.filter_row_layout = QHBoxLayout(self.filter_row) 
        self.main_widget_layout.addWidget(self.filter_row)
        
        self.custom_z_plane = CustomZPlane()
        self.filter_row_layout.addWidget(self.custom_z_plane)



        self.setStyleSheet("""
            
        """)
