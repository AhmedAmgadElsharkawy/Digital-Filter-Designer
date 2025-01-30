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
