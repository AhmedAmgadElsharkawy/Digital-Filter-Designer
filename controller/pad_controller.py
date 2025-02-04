class PadController():
    def __init__(self,main_window):
        self.main_window = main_window
        self.main_window.padding_area.pad_controller = self
        self.pointer = 0
        self.drawing = False
        self.yMin = 0
        self.yMax = 0

    def add_point(self, last, curr):
        self.drawing = True
        signal_x = self.main_window.signal_controller.x
        signal_y = self.main_window.signal_controller.y
        new_x, new_y = 0, 0
        if last != None:
            new_x = signal_x[-1] + 0.05
            new_y = signal_y[-1] + (0.1 if last.y() > curr.y() else 0.01) * (-1 if last.x() > curr.x() else 1)
        else :
            self.main_window.signal_controller.clear_plots_data()
        self.main_window.signal_controller.x.append(new_x)
        self.main_window.signal_controller.y.append(new_y)
        self.yMax = max(self.yMax, new_y)
        self.yMin = min(self.yMin, new_y)
        self.set_ranges(new_x, self.yMin, self.yMax)

        self.main_window.signal_controller.plot_file()

    def reset_variables(self):
        self.drawing = False
        self.main_window.padding_area.last_pos = None

    def set_ranges(self, x_max, y_min, y_max):
        self.main_window.signal_plot.setLimits(xMin = 0, xMax = x_max, yMin = y_min, yMax = y_max)
        self.main_window.filtered_signal_plot.setLimits(xMin = 0, xMax = x_max)
        self.main_window.signal_plot.setXRange(x_max - 10, x_max)
        self.main_window.filtered_signal_plot.setXRange(x_max - 10, x_max)
        self.main_window.signal_plot.setYRange(y_min, y_max)