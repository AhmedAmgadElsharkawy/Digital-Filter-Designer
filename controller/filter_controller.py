from utils.z_plane_utils import calculate_response
class FilterController():
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window

        self.main_window.clear_poles_button.clicked.connect(self.clear_poles)
        self.main_window.clear_zeroes_button.clicked.connect(self.clear_zeores)
        self.main_window.clear_all_poles_and_zeroes_button.clicked.connect(self.clear_all_poles_and_zeroes)

        self.main_window.swap_poles_button.clicked.connect(self.swap_poles)
        self.main_window.swap_zeroes_button.clicked.connect(self.swap_zeroes)

        self.main_window.filter_model.updated.connect(self.plot_filter_response)

    def clear_poles(self):
        self.main_window.filter_z_plane.clear_poles_graphical_items()
        self.main_window.filter_model.clear_poles()

    def clear_zeores(self):
        self.main_window.filter_z_plane.clear_zeroes_graphical_items()
        self.main_window.filter_model.clear_zeroes()

    def clear_all_poles_and_zeroes(self):
        self.main_window.filter_z_plane.clear_all_graphical_items()
        self.main_window.filter_model.clear_all_poles_and_zeroes()

    def swap_poles(self):
        self.main_window.filter_model.swap_poles()
        self.main_window.filter_z_plane.swap_poles_graphically()

    def swap_zeroes(self):
        self.main_window.filter_model.swap_zeroes()
        self.main_window.filter_z_plane.swap_zeroes_graphically()

    

    def plot_filter_response(self):
        poles = self.main_window.filter_model.poles.copy()
        for pole in self.main_window.filter_model.conj_poles:
            poles.append(pole)
            conj_pole = complex(pole.real,-pole.imag)
            if conj_pole != pole:
                poles.append(complex(pole.real,-pole.imag))

        zeroes = self.main_window.filter_model.zeroes.copy()
        for zero in self.main_window.filter_model.conj_zeroes:
            zeroes.append(zero)
            conj_zero = complex(zero.real,-zero.imag)
            if conj_zero != zero:
                zeroes.append(complex(zero.real,-zero.imag))

        omega, magnitude, phase = calculate_response(poles, zeroes)

        self.main_window.filter_magnitude_response.plot_response(omega,magnitude)
        self.main_window.filter_phase_response.plot_response(omega,phase)