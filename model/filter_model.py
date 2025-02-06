from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np

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

    def get_cascade_form(self):
        """Returns filter coefficients in cascade form sections"""
        sections = []
        zeros = self.get_zeros()
        poles = self.get_poles()
        
        n_sections = max(len(zeros) // 2 + len(zeros) % 2,
                        len(poles) // 2 + len(poles) % 2)
        
        for i in range(n_sections):
            # Initialize section polynomials
            numerator = [1.0]
            denominator = [1.0]
            
            # Process zeros for this section
            if 2*i < len(zeros):
                z = zeros[2*i]
                numerator = [numerator[j] - z.real * numerator[j-1] if j > 0 else numerator[j] 
                            for j in range(len(numerator))]
                numerator.append(abs(z)**2)
                
                if 2*i+1 < len(zeros):
                    z2 = zeros[2*i+1]
                    numerator = [numerator[j] - z2.real * numerator[j-1] if j > 0 else numerator[j] 
                            for j in range(len(numerator))]
                    numerator.append(abs(z2)**2)
            
            # Process poles for this section
            if 2*i < len(poles):
                p = poles[2*i]
                denominator = [denominator[j] - p.real * denominator[j-1] if j > 0 else denominator[j] 
                            for j in range(len(denominator))]
                denominator.append(abs(p)**2)
                
                if 2*i+1 < len(poles):
                    p2 = poles[2*i+1]
                    denominator = [denominator[j] - p2.real * denominator[j-1] if j > 0 else denominator[j] 
                                for j in range(len(denominator))]
                    denominator.append(abs(p2)**2)
            
            # Create section with [b0, b1, b2, a1, a2]
            section = [1.0, 0.0, 0.0, 0.0, 0.0]
            if len(numerator) > 1:
                section[1] = numerator[1]
            if len(numerator) > 2:
                section[2] = numerator[2]
            if len(denominator) > 1:
                section[3] = denominator[1]
            if len(denominator) > 2:
                section[4] = denominator[2]
                
            sections.append(section)

        return sections
            
    def get_zeros(self):
        """Returns all zeros including conjugates"""
        all_zeros = []
        all_zeros.extend(self.zeroes)
        # Add both parts of conjugate pairs
        for z in self.conj_zeroes:
            all_zeros.append(z)
            all_zeros.append(complex(z.real, -z.imag))  
        return all_zeros

    def get_poles(self):
        """Returns all poles including conjugates"""
        all_poles = []
        all_poles.extend(self.poles)
        # Add both parts of conjugate pairs
        for p in self.conj_poles:
            all_poles.append(p)
            all_poles.append(complex(p.real, -p.imag))  
        return all_poles

    def get_transfer_function(self):
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


