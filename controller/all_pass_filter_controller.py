from utils.z_plane_utils import calculate_response
from PyQt5.QtCore import QPointF
import numpy as np
class AllPassFilterController():
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.filters = []
        self.checked_filters = []

        self.main_window.apply_all_pass_filter_button.clicked.connect(self.apply_all_pass_filter)

    def add_filter(self, complex_value):
        self.filters.append(complex(round(complex_value.real,5),round(complex_value.imag,5)))
        return len(self.filters) - 1

    def checkbox_state_changed(self, idx, state):
        if state == 2:
            self.checked_filters.append(self.filters[idx])
        else:
            self.checked_filters.remove(self.filters[idx])
        zeroes, poles = self.data_pre_processing()
        self.plot_processed_data(zeroes, poles)

    def data_pre_processing(self):
        poles, zeroes = [], []
        for idx, value in enumerate(self.checked_filters):
            poles.append(value)
            conj = complex(value.real,-value.imag)
            zero = 1/conj
            zero = complex(round(zero.real,5),round(zero.imag,5))
            zeroes.append(zero)
        return zeroes, poles

    def plot_processed_data(self, zeroes, poles):
        self.plot_phase_response(zeroes, poles)
        self.plot_z_plane(zeroes, poles)

    def plot_phase_response(self, zeroes, poles):
        omega, magnitude, phase = calculate_response(poles, zeroes)
        self.main_window.all_pass_filter_phase_response.plot_response(omega,phase)

    def plot_z_plane(self, zeroes, poles):
        self.main_window.all_pass_filter_z_plane.clear_all_graphical_items()
        for pole in poles:
            point = QPointF(pole.real * 100, pole.imag * -100)
            self.main_window.all_pass_filter_z_plane.add_graphical_item(point, "Pole")

        for zero in zeroes:
            point = QPointF(zero.real * 100, zero.imag * -100)
            self.main_window.all_pass_filter_z_plane.add_graphical_item(point, "Zero")

    def apply_all_pass_filter(self):
        zeroes, poles = self.data_pre_processing()
        for pole in poles:
            point = QPointF(pole.real * 100, pole.imag * -100)
            self.main_window.filter_model.add_pole(pole)
            self.main_window.filter_z_plane.add_graphical_item(point, "Pole")

        for zero in zeroes:
            point = QPointF(zero.real * 100, zero.imag * -100)
            self.main_window.filter_model.add_zero(zero)
            self.main_window.filter_z_plane.add_graphical_item(point, "Zero")

        self.main_window.signal_controller.plot_file()
        self.main_window.save_load_controller.save_current_state()
        