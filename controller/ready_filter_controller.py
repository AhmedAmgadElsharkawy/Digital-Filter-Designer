import scipy.signal as signal
class FilterTypeController():
    def __init__(self,main_window):
        self.main_window = main_window

        self.main_window.apply_filter_button.clicked.connect(self.apply_filter)
        self.main_window.filter_type_combobox.currentTextChanged.connect(self.changing_filter_btype)
        self.main_window.filters_combobox.currentTextChanged.connect(self.changing_filter_type)

        self.main_window.filter_start_frequency_container.disable()
        self.main_window.filter_end_frequency_container.disable()
        
        self.filter_types_array_preventions = {}
        self.enable_and_disable_initialization()
        self.changing_filter_type("Butterworth Filter")

    def apply_filter(self):
        filter_name = self.main_window.filters_combobox.currentText()
        filter_btype = self.main_window.filter_type_combobox.currentText().lower()
        filter_order = self.main_window.filter_order_spin_box.value()
        filter_cutoff_frequency = self.main_window.filter_cutoff_frequency_container.value()
        filter_passband_ripple = self.main_window.passband_ripple_container.value()
        filter_stopband_ripple = self.main_window.stopband_ripple_container.value()

        if filter_name == "Butterworth Filter":
            zeroes, poles = self.butterworth_filter(filter_order, filter_cutoff_frequency, filter_btype)
        elif filter_name == "Chebyshev Filter":
            zeroes, poles = self.chebyshev_filter(filter_order, filter_cutoff_frequency, filter_passband_ripple, filter_btype)
        elif filter_name == "inv Chebyshev Filter":
            zeroes, poles = self.chebyshev_type_2_filter(filter_order, filter_cutoff_frequency, filter_stopband_ripple, filter_btype)
        elif filter_name == "Bessel Filter":
            zeroes, poles = self.bessel_filter(filter_order, filter_cutoff_frequency, filter_btype)
        elif filter_name == "Elliptic Filter":
            zeroes, poles = self.elliptic_filter(filter_order, filter_cutoff_frequency, filter_passband_ripple, filter_stopband_ripple, filter_btype)

    def butterworth_filter(self, order, cutoff_frequency, type):
        b, a = signal.butter(order, cutoff_frequency, btype=type, analog=False)

        zeros, poles, gain = signal.tf2zpk(b, a)
        return zeros, poles
    
    def chebyshev_filter(self, order, cutoff_frequency, passband_ripple, type):
        b, a = signal.cheby1(order, passband_ripple, cutoff_frequency, btype=type, analog=False)

        zeros, poles, gain = signal.tf2zpk(b, a)
        return zeros, poles
    
    def chebyshev_type_2_filter(self, order, cutoff_frequency, stopband_ripple, type):
        b, a = signal.cheby2(order, stopband_ripple, cutoff_frequency, btype=type, analog=False)

        zeros, poles, gain = signal.tf2zpk(b, a)
        return zeros, poles
    
    def bessel_filter(self, order, cutoff_frequency, type):
        b, a = signal.bessel(order, cutoff_frequency, btype=type, analog=False)

        zeros, poles, gain = signal.tf2zpk(b, a)
        return zeros, poles
    
    def elliptic_filter(self, order, cutoff_frequency, passband_ripple, stopband_ripple, type):
        b, a = signal.ellip(order, passband_ripple, stopband_ripple, cutoff_frequency, btype=type, analog=False)

        zeros, poles, gain = signal.tf2zpk(b, a)
        return zeros, poles
    
    def changing_filter_btype(self, text):
        if text == 'Low' or text == 'High':
            self.main_window.filter_start_frequency_container.disable()
            self.main_window.filter_end_frequency_container.disable()
            self.main_window.filter_cutoff_frequency_container.enable()
        else :
            self.main_window.filter_start_frequency_container.enable()
            self.main_window.filter_end_frequency_container.enable()
            self.main_window.filter_cutoff_frequency_container.disable()

    def changing_filter_type(self, text):
        for widget in self.filter_types_array_preventions[text][0]:
            widget.disable()
        
        for widget in self.filter_types_array_preventions[text][1]:
            widget.enable()


    def enable_and_disable_initialization(self):
        self.filter_types_array_preventions["Butterworth Filter"] = [[self.main_window.passband_ripple_container, self.main_window.stopband_ripple_container], []]
        self.filter_types_array_preventions["Chebyshev Filter"] = [[self.main_window.stopband_ripple_container], [self.main_window.passband_ripple_container]]
        self.filter_types_array_preventions["inv Chebyshev Filter"] = [[self.main_window.passband_ripple_container], [self.main_window.stopband_ripple_container]]
        self.filter_types_array_preventions["Bessel Filter"] = [[self.main_window.passband_ripple_container, self.main_window.stopband_ripple_container], []]
        self.filter_types_array_preventions["Elliptic Filter"] = [[], [self.main_window.passband_ripple_container, self.main_window.stopband_ripple_container]]