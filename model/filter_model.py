from PyQt5.QtCore import pyqtSignal, QObject

class FilterModel(QObject):
    updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.poles = []
        self.zeroes = []
        self.conj_poles = []
        self.conj_zeroes = []

    def add_pole(self, pole):
        self.poles.append(pole)
        self.updated.emit()  

    def remove_pole(self, pole):
        if pole in self.poles:
            self.poles.remove(pole)
            self.updated.emit()

    def add_zero(self, zero):
        self.zeroes.append(zero)
        self.updated.emit()

    def remove_zero(self, zero):
        if zero in self.zeroes:
            self.zeroes.remove(zero)
            self.updated.emit()

    def add_conj_poles(self, pole):
        self.conj_poles.append(pole)
        self.updated.emit()

    def remove_conj_poles(self, pole):
        conjugate_pole = complex(pole.real, -pole.imag)
        if pole in self.conj_poles:
            self.conj_poles.remove(pole)
            self.updated.emit()
            return
        if conjugate_pole in self.conj_poles:
            self.conj_poles.remove(conjugate_pole)
            self.updated.emit()
            return

    def add_conj_zeroes(self, zero):
        self.conj_zeroes.append(zero)
        self.updated.emit()

    def remove_conj_zeroes(self, zero):
        conjugate_zero = complex(zero.real, -zero.imag)
        if zero in self.conj_zeroes:
            self.conj_zeroes.remove(zero)
            self.updated.emit()
            return
        if conjugate_zero in self.conj_zeroes:
            self.conj_zeroes.remove(conjugate_zero)
            self.updated.emit()

    def clear_poles(self):
        self.poles = []
        self.conj_poles = []
        self.updated.emit()

    def clear_zeroes(self):
        self.zeroes = []
        self.conj_zeroes = []
        self.updated.emit()

    def clear_all_poles_and_zeroes(self):
        self.clear_poles()
        self.clear_zeroes()

    def swap_zeroes(self):
        self.poles.extend(self.zeroes)
        self.conj_poles.extend(self.conj_zeroes)
        self.clear_zeroes()
        self.updated.emit()

    def swap_poles(self):
        self.zeroes.extend(self.poles)
        self.conj_zeroes.extend(self.conj_poles)
        self.clear_poles()
        self.updated.emit()

    def add_complex_value(self,complex_value,complex_value_type):
        if complex_value_type == "Pole":
            self.add_pole(complex_value)
        if complex_value_type == "Zero":
            self.add_zero(complex_value)
        if complex_value_type == "Conj Poles":
            self.add_conj_poles(complex_value)
        if complex_value_type == "Conj Zeroes":
            self.add_conj_zeroes(complex_value)

    def remove_complex_value(self,complex_value,complex_value_type):
        if complex_value_type == "Pole":
            self.remove_pole(complex_value)
        if complex_value_type == "Zero":
            self.remove_zero(complex_value)
        if complex_value_type == "Conj Poles":
            self.remove_conj_poles(complex_value)
        if complex_value_type == "Conj Zeroes":
            self.remove_conj_zeroes(complex_value)

    # In the FilterModel class
    def get_cascade_form(self):
        """Returns filter coefficients in cascade form sections"""
        # Each section should have format [b0, b1, b2, 1, a1, a2]
        # where b's are numerator coeffs and a's are denominator coeffs
        sections = []
        
        # Get zeros and poles
        zeros = self.get_zeros()
        poles = self.get_poles()
        
        # Group into second-order sections
        for i in range(0, len(zeros), 2):
            section = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]  # Default coefficients
            # Add zeros coefficients
            if i < len(zeros):
                section[1] = -zeros[i].real
                if i+1 < len(zeros):
                    section[2] = abs(zeros[i])**2
            # Add poles coefficients  
            if i < len(poles):
                section[4] = -poles[i].real
                if i+1 < len(poles):
                    section[5] = abs(poles[i])**2
            sections.append(section)
        
        return sections
    
    def get_zeros(self):
        """Returns all zeros including conjugates"""
        all_zeros = []
        all_zeros.extend(self.zeroes)
        all_zeros.extend(self.conj_zeroes)
        return all_zeros

    def get_poles(self):
        """Returns all poles including conjugates"""
        all_poles = []
        all_poles.extend(self.poles)
        all_poles.extend(self.conj_poles)
        return all_poles

    def get_transfer_function(self, controller):
        """Returns transfer function coefficients as (numerator, denominator)"""
        zeros = self.get_zeros()
        poles = self.get_poles()
        
        # Create transfer function coefficients
        numerator = [1.0]  # Start with highest order term
        denominator = [1.0]
        
        # Add zero contributions
        for zero in zeros:
            numerator = [numerator[i] - zero.real * numerator[i-1] if i > 0 else numerator[i] 
                        for i in range(len(numerator))]
            numerator.append(abs(zero)**2)
            
        # Add pole contributions  
        for pole in poles:
            denominator = [denominator[i] - pole.real * denominator[i-1] if i > 0 else denominator[i]
                        for i in range(len(denominator))]
            denominator.append(abs(pole)**2)
            
        return numerator, denominator


