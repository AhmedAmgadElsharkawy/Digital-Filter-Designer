from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QPushButton

from view.custom_z_plane import CustomZPlane
from view.response_plot import ResponsePlot


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

        self.undo_redo_widget = QWidget()
        self.undo_redo_widget_layout = QHBoxLayout(self.undo_redo_widget)
        self.controls_widget_layout.addWidget(self.undo_redo_widget)
        self.undo_button = QPushButton("Undo")
        self.redo_button = QPushButton("Redo")
        self.undo_redo_widget_layout.addWidget(self.undo_button)
        self.undo_redo_widget_layout.addWidget(self.redo_button)

        

        self.filter_row = QWidget()
        self.filter_row_layout = QHBoxLayout(self.filter_row) 
        self.main_widget_layout.addWidget(self.filter_row)
        
        self.custom_z_plane = CustomZPlane()
        self.filter_row_layout.addWidget(self.custom_z_plane)

        self.filter_response_plots_widget = QWidget()
        self.filter_response_plots_widget_layout = QVBoxLayout(self.filter_response_plots_widget)
        self.filter_row_layout.addWidget(self.filter_response_plots_widget)
        self.filter_magnitude_response = ResponsePlot(title="Magnitude Response",xlabel='Normalized Frequency (xπ rad/sample)',ylabel='Magnitude')
        self.filter_phase_response = ResponsePlot(title="Phase Response", xlabel='Normalized Frequency (xπ rad/sample)',ylabel='Phase (radians)')
        self.filter_response_plots_widget_layout.addWidget(self.filter_magnitude_response)
        self.filter_response_plots_widget_layout.addWidget(self.filter_phase_response)
        



        self.setStyleSheet("""
            
        """)
