class PadController():
    def __init__(self,main_window):
        self.main_window = main_window
        self.main_window.padding_area.pad_controller = self