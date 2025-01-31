from utils.z_plane_utils import calculate_response
from PyQt5.QtCore import QPointF
class AllPassFilterController():
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.filters = []
        self.checked_filters = []

    def add_filter(self, complex):
        self.filters.append(complex)
        return len(self.filters) - 1

    def checkbox_state_changed(self, idx, state):
        if state == 2:
            self.checked_filters.append(self.filters[idx])
        else:
            self.checked_filters.remove(self.filters[idx])
        self.data_pre_processing()

    def data_pre_processing(self):
        poles, zeroes = [], []
        for idx, value in enumerate(self.checked_filters):
            poles.append(value)
            if value.imag != 0:
                zeroes.append(value.real - value.imag * 1j)
            else:
                zeroes.append(1 / value.real)
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