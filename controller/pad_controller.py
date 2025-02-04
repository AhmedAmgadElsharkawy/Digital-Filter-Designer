class PadController():
    def __init__(self,main_window):
        self.main_window = main_window
        self.main_window.padding_area.pad_controller = self
        self.pointer = 0

    def add_point(self, last, curr):
        signal_x = self.main_window.signal_controller.x
        signal_y = self.main_window.signal_controller.y
        if last != None:
            self.main_window.signal_controller.x.append(signal_x[-1] + 0.05)
            self.main_window.signal_controller.y.append(signal_y[-1] + (0.1 if last.y() > curr.y() else 0.01) * (-1 if last.x() > curr.x() else 1) )
        else :
            self.main_window.signal_controller.x.append(0)
            self.main_window.signal_controller.y.append(0.5)

        self.main_window.signal_controller.plot_file()