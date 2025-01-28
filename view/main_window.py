from PyQt5.QtWidgets import QMainWindow,QTableWidget,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QPushButton,QComboBox,QSpinBox,QDoubleSpinBox
import pyqtgraph as pg

from view.custom_z_plane import CustomZPlane
from view.response_plot import ResponsePlot
from view.custom_double_spin_box import CustomDoubleSpinBox
from view.custom_table import CustomTable
from view.padding_area import PaddingArea


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
        self.controls_widget_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.addWidget(self.controls_widget)

        self.save_load_widget = QWidget()
        self.save_load_widget_layout = QHBoxLayout(self.save_load_widget)
        self.save_load_widget_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.addWidget(self.save_load_widget)
        self.save_filter_button = QPushButton("Save")
        self.load_filter_button = QPushButton("Load")
        self.save_load_widget_layout.addWidget(self.save_filter_button)
        self.save_load_widget_layout.addWidget(self.load_filter_button)
        

        self.poles_zeroes_widget = QWidget()
        self.poles_zeroes_widget_layout = QHBoxLayout(self.poles_zeroes_widget)
        self.poles_zeroes_widget_layout.setContentsMargins(0,0,0,0)
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
        self.swap_controls_widget_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.addWidget(self.swap_controls_widget)
        self.swap_poles_button = QPushButton("Swap poles")
        self.swap_zeroes_button = QPushButton("Swap Zeroes")
        self.swap_controls_widget_layout.addWidget(self.swap_poles_button)
        self.swap_controls_widget_layout.addWidget(self.swap_zeroes_button)

        self.clear_controls_widget = QWidget()
        self.clear_controls_widget_layout = QHBoxLayout(self.clear_controls_widget)
        self.clear_controls_widget_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.addWidget(self.clear_controls_widget)
        self.clear_poles_button = QPushButton("Clear Poles")
        self.clear_zeroes_button = QPushButton("Clear Zeroes")
        self.clear_all_poles_and_zeroes_button = QPushButton("Clear All")
        self.clear_controls_widget_layout.addWidget(self.clear_poles_button)
        self.clear_controls_widget_layout.addWidget(self.clear_zeroes_button)
        self.clear_controls_widget_layout.addWidget(self.clear_all_poles_and_zeroes_button)

        self.undo_redo_widget = QWidget()
        self.undo_redo_widget_layout = QHBoxLayout(self.undo_redo_widget)
        self.undo_redo_widget_layout.setContentsMargins(0,0,0,0)
        self.controls_widget_layout.addWidget(self.undo_redo_widget)
        self.undo_button = QPushButton("Undo")
        self.redo_button = QPushButton("Redo")
        self.undo_redo_widget_layout.addWidget(self.undo_button)
        self.undo_redo_widget_layout.addWidget(self.redo_button)

        
        self.bottom_container = QWidget()
        self.bottom_container_layout = QHBoxLayout(self.bottom_container)
        self.bottom_container_layout.setContentsMargins(0,0,0,0)
        self.main_widget_layout.addWidget(self.bottom_container)

        self.left_container = QWidget()
        self.left_container_layout = QVBoxLayout(self.left_container)
        self.left_container_layout.setContentsMargins(0,0,0,0)
        self.bottom_container_layout.addWidget(self.left_container)

        self.filter_row = QWidget()
        self.filter_row_layout = QHBoxLayout(self.filter_row) 
        self.filter_row_layout.setContentsMargins(0,0,0,0)
        self.left_container_layout.addWidget(self.filter_row)
        
        self.custom_z_plane = CustomZPlane()
        self.filter_row_layout.addWidget(self.custom_z_plane)

        self.filter_response_plots_widget = QWidget()
        self.filter_response_plots_widget_layout = QVBoxLayout(self.filter_response_plots_widget)
        self.filter_response_plots_widget_layout.setContentsMargins(0,0,0,0)
        self.filter_row_layout.addWidget(self.filter_response_plots_widget)
        self.filter_magnitude_response = ResponsePlot(title="Magnitude Response",xlabel='Normalized Frequency (xπ rad/sample)',ylabel='Magnitude')
        self.filter_phase_response = ResponsePlot(title="Phase Response", xlabel='Normalized Frequency (xπ rad/sample)',ylabel='Phase (radians)')
        self.filter_response_plots_widget_layout.addWidget(self.filter_magnitude_response)
        self.filter_response_plots_widget_layout.addWidget(self.filter_phase_response)
        
        self.right_widget = QWidget()
        self.right_widget_layout = QVBoxLayout(self.right_widget)
        self.right_widget.setFixedWidth(400)
        self.right_widget_layout.setContentsMargins(0,0,0,0)
        self.bottom_container_layout.addWidget(self.right_widget)

        self.filters_widget = QWidget()
        self.filters_widget_layout = QVBoxLayout(self.filters_widget)
        self.filters_widget_layout.setContentsMargins(0,0,0,0)
        self.filters_widget_layout.setSpacing(0)
        self.right_widget_layout.addWidget(self.filters_widget)
        
        self.filters_widget_header = QWidget()
        self.filters_widget_header_layout = QHBoxLayout(self.filters_widget_header)
        self.filters_widget_header_layout.setContentsMargins(0,0,0,0)
        self.filters_widget_layout.addWidget(self.filters_widget_header)
        filter_items = ['Butterworth Filter', 'Chebyshev Filter', 'inv Chebyshev Filter', 'Bessel Filter',"Elliptic Filter"]
        self.filters_combobox = QComboBox()
        self.filters_combobox.addItems(filter_items)
        self.apply_filter_button = QPushButton("Apply Filter")
        self.filters_widget_header_layout.addWidget(self.filters_combobox)
        self.filters_widget_header_layout.addWidget(self.apply_filter_button)

        

        self.filter_controls_widget = QWidget()
        self.filter_controls_widget_layout = QVBoxLayout(self.filter_controls_widget)
        self.filter_controls_widget_layout.setContentsMargins(0,0,0,0)
        self.filters_widget_layout.addWidget(self.filter_controls_widget)

        self.filter_type_container = QWidget()
        self.filter_type_container_layout = QHBoxLayout(self.filter_type_container)
        self.filter_type_container_layout.setContentsMargins(0,0,0,0)
        self.filter_controls_widget_layout.addWidget(self.filter_type_container)
        self.filter_type_label = QLabel("type")
        self.filter_types = ['Low-pass', 'High-pass', 'Band-pass', 'Band-stop']
        self.filter_type_combobox = QComboBox()
        self.filter_type_combobox.addItems(self.filter_types)
        self.filter_type_container_layout.addWidget(self.filter_type_label)
        self.filter_type_container_layout.addWidget(self.filter_type_combobox)

        self.filter_order_container = QWidget()
        self.filter_order_container_layout = QHBoxLayout(self.filter_order_container)
        self.filter_order_container_layout.setContentsMargins(0,0,0,0)
        self.filter_controls_widget_layout.addWidget(self.filter_order_container)
        self.filter_order_label = QLabel("Order")
        self.filter_order_container_layout.addWidget(self.filter_order_label)
        self.filter_order_spin_box = QSpinBox()
        self.filter_order_spin_box.setRange(1, 4)
        self.filter_order_spin_box.setValue(1)
        self.filter_order_container_layout.addWidget(self.filter_order_spin_box)
        self.filter_order_spin_box.setButtonSymbols(QSpinBox.NoButtons)


        self.filter_start_frequency_container = CustomDoubleSpinBox(label="Start Frequency")
        self.filter_controls_widget_layout.addWidget(self.filter_start_frequency_container)

        self.filter_end_frequency_container = CustomDoubleSpinBox(label="End Frequency")
        self.filter_controls_widget_layout.addWidget(self.filter_end_frequency_container)

        self.transition_band_container = CustomDoubleSpinBox(label="Transition Band")
        self.filter_controls_widget_layout.addWidget(self.filter_end_frequency_container)

        self.passband_ripple_container = CustomDoubleSpinBox(label="Passband Ripple")
        self.filter_controls_widget_layout.addWidget(self.passband_ripple_container)

        self.stopband_ripple_contnainer = CustomDoubleSpinBox(label="Stopband Ripple")
        self.filter_controls_widget_layout.addWidget(self.filter_end_frequency_container)
        
        self.all_pass_filters_widget = QWidget()
        self.all_pass_filters_widget_layout = QVBoxLayout(self.all_pass_filters_widget)
        self.all_pass_filters_widget_layout.setContentsMargins(0,0,0,0)
        self.right_widget_layout.addWidget(self.all_pass_filters_widget)



        self.all_pass_filters_table = CustomTable()
        self.all_pass_filters_table.setFixedHeight(300)
        self.all_pass_filter_phase_response = ResponsePlot()
        self.all_pass_filter_z_plane = CustomZPlane()
        self.apply_all_pass_filter_button = QPushButton("Apply The Filter")
        self.all_pass_filters_widget_layout.addWidget(self.all_pass_filter_z_plane)
        self.all_pass_filters_widget_layout.addWidget(self.all_pass_filter_phase_response)
        self.all_pass_filters_widget_layout.addWidget(self.all_pass_filters_table)
        self.all_pass_filters_widget_layout.addWidget(self.apply_all_pass_filter_button)
        
        
        self.signal_row = QWidget()
        self.signal_row_layout = QHBoxLayout(self.signal_row)
        self.left_container_layout.addWidget(self.signal_row)
        self.signal_row_layout.setContentsMargins(0,0,0,0)
        
        self.signal_plots_container = QWidget()
        self.signal_plots_container_layout = QVBoxLayout(self.signal_plots_container)
        self.signal_plots_container_layout.setContentsMargins(0,0,0,0)
        self.signal_row_layout.addWidget(self.signal_plots_container)

        self.signal_plot = pg.PlotWidget()
        self.signal_plot.setTitle("Signal Plot", color="k", size="8pt")
        self.signal_plot.setBackground("w")
        self.signal_plot.showGrid(x=True, y=True)
        self.signal_plot.getAxis('bottom').setPen(pg.mkPen('k'))  
        self.signal_plot.getAxis('left').setPen(pg.mkPen('k'))
        self.signal_plot.getAxis('bottom').setTextPen(pg.mkPen('k')) 
        self.signal_plot.getAxis('left').setTextPen(pg.mkPen('k')) 

        self.filtered_signal_plot = pg.PlotWidget()
        self.filtered_signal_plot.setTitle("Filtered Signal Plot", color="k", size="8pt")
        self.filtered_signal_plot.setBackground("w")
        self.filtered_signal_plot.showGrid(x=True, y=True)
        self.filtered_signal_plot.getAxis('bottom').setPen(pg.mkPen('k'))  
        self.filtered_signal_plot.getAxis('left').setPen(pg.mkPen('k'))
        self.filtered_signal_plot.getAxis('bottom').setTextPen(pg.mkPen('k')) 
        self.filtered_signal_plot.getAxis('left').setTextPen(pg.mkPen('k')) 

        self.signal_plots_container_layout.addWidget(self.signal_plot)
        self.signal_plots_container_layout.addWidget(self.filtered_signal_plot)
        
        
        self.padding_area = PaddingArea()
        self.signal_plots_container_layout.addWidget(self.padding_area)
        self.padding_area.setFixedSize(300,300)



        self.setStyleSheet("""
            
        """)
