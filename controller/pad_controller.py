import math
import numpy as np
class PadController():
    def __init__(self,main_window):
        self.main_window = main_window
        self.main_window.padding_area.pad_controller = self
        self.pointer = 0
        self.drawing = False
        self.yMin = 0
        self.yMax = 0

    def add_point(self, last_pos, curr_pos, last_time, curr_time):
        self.drawing = True
        signal_x = self.main_window.signal_controller.x
        signal_y = self.main_window.signal_controller.y
        new_x, new_y = 0, 0
        if last_pos != None:
            new_x = signal_x[-1] + 0.001
            new_y = self.calculate_new_y(last_pos.x(), last_pos.y(), curr_pos.x(), curr_pos.y(), last_time, curr_time, new_x)
        else :
            self.main_window.signal_controller.clear_plots_data()
        self.main_window.signal_controller.x.append(new_x)
        self.main_window.signal_controller.y.append(new_y)

        self.main_window.signal_controller.plot_file()

    def reset_variables(self):
        self.drawing = False
        self.main_window.padding_area.last_pos = None

    def calculate_new_y(self, x1, y1, x2, y2, last_time, curr_time, x_axis):
        speed = self.calculate_speed(x1, y1, x2, y2, last_time, curr_time)
        return np.cos(speed * x_axis) * x2

    def calculate_speed(self, x1, y1, x2, y2, last_time, curr_time):
        d = self.distance(x1, y1, x2, y2)
        time_diff = last_time.msecsTo(curr_time) * 2
        if time_diff == 0:
            return 0.001
        else:
            return d / time_diff

    def distance(self, x1, y1, x2, y2):
        return math.sqrt ((x2 - x1) ** 2 + (y2 - y1) ** 2)