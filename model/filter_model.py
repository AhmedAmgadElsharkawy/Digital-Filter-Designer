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
