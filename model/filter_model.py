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
            self.poles.remove(zero)

    def add_conj_poles(self,conj_poles):
        self.conj_poles.append(conj_poles)

    def remove_conj_poles(self,conj_poles):
        pass
    
    def add_conj_zeroes(self,conj_zeroes):
        self.conj_zeroes.append(conj_zeroes)

    def remove_conj_zeroes(self,conj_zeroes):
        pass

    def clear_all_polses(self):
        self.poles = []
        self.conj_poles = []
    
    def clear_all_zeroes(self):
        self.zeroes = []
        self.conj_zeroes = []

    def clear_all_poles_and_zeores(self):
        self.clear_all_polses()
        self.clear_all_zeroes()

    

    
        