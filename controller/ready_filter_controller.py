class FilterTypeController():
    def __init__(self,main_window):
        self.main_window = main_window

        self.main_window.apply_filter_button.clicked.connect(self.apply_filter)

    def apply_filter(self):
        filter_name = self.main_window.filters_combobox.currentText()
        filter_type = self.main_window.filter_type_combobox.currentText()
        filter_order = self.main_window.filter_order_spin_box.value()
        filter_start_frequency = self.main_window.filter_start_frequency_container.value()
        filter_passband_ripple = self.main_window.filter_end_frequency_container.value()
        filter_end_frequency = self.main_window.filter_end_frequency_container.value()
        print(filter_start_frequency, filter_end_frequency, filter_passband_ripple)