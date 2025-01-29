class FilterModel:
    def __init__(self):
        self.poles = []
        self.zeroes = []
        self.conj_poles = []
        self.conj_zeroes = []
        
    def add_pole(self,pole):
        self.poles.append(pole)

    def remove_pole(self,pole):
        if pole in self.poles:
            self.poles.remove(pole)

    def add_zero(self,zero):
        self.zeroes.append(zero)

    def remove_zero(self,zero):
        if zero in self.zeroes:
            self.zeroes.remove(zero)

    def add_conj_poles(self,pole):
        self.conj_poles.append(pole)

    def remove_conj_poles(self,pole):
        conjugate_pole = complex(pole.real, -pole.imag)
        if pole in self.conj_poles:
            self.conj_poles.remove(pole)
            return
        if conjugate_pole in self.conj_poles:
            self.conj_poles.remove(conjugate_pole)
            return
    
    def add_conj_zeroes(self,zero):
        self.conj_zeroes.append(zero)

    def remove_conj_zeroes(self,zero):
        conjugate_zero = complex(zero.real, -zero.imag)
        if zero in self.conj_zeroes:
            self.conj_zeroes.remove(zero)
            return
        if conjugate_zero in self.conj_zeroes:
            self.conj_zeroes.remove(conjugate_zero)
            return 
        

    def clear_poles(self):
        self.poles = []
        self.conj_poles = []

    def clear_zeroes(self):
        self.zeroes = []
        self.conj_zeroes = []

    def clear_all_poles_and_zeores(self):
        self.clear_poles()
        self.clear_zeroes()
        

    

    
        