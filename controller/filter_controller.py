

class FilterController():
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window

        self.main_window.clear_poles_button.clicked.connect(self.clear_poles)
        self.main_window.clear_zeroes_button.clicked.connect(self.clear_zeores)
        self.main_window.clear_all_poles_and_zeroes_button.clicked.connect(self.clear_all_poles_and_zeroes)

        self.main_window.swap_poles_button.clicked.connect(self.swap_poles)
        self.main_window.swap_zeroes_button.clicked.connect(self.swap_zeroes)

    def clear_poles(self):
        self.main_window.filter_z_plane.clear_poles_graphical_items()
        self.main_window.filter_model.clear_poles()

    def clear_zeores(self):
        self.main_window.filter_z_plane.clear_zeroes_graphical_items()
        self.main_window.filter_model.clear_zeroes()

    def clear_all_poles_and_zeroes(self):
        self.main_window.filter_z_plane.clear_all_graphical_items()
        self.main_window.filter_model.clear_all_poles_and_zeores()

    def swap_poles(self):
        self.main_window.filter_model.swap_poles()
        self.main_window.filter_z_plane.swap_poles_graphically()

    def swap_zeroes(self):
        self.main_window.filter_model.swap_zeroes()
        self.main_window.filter_z_plane.swap_zeroes_graphically()