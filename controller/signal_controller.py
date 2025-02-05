from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import csv
import numpy as np
from scipy import signal
class SignalController():
    def __init__(self,main_window):
        self.main_window = main_window
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.step = 0
        self.pointer = 0
        self.x = []
        self.y = []
        self.speed = 20
        self.moving = False

        self.main_window.import_signal_button.clicked.connect(self.import_signal)
        self.main_window.filter_speed_slider.valueChanged.connect(self.change_filter_speed)

    def import_signal(self):
        self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls)" )
        if self.fileName[0]:  
            self.main_window.pad_controller.reset_variables()
            self.open_file(self.fileName[0])

    def open_file(self, path:str):
        with open(path, 'r') as file:
            csv_data = csv.reader(file, delimiter=',')
            data = list(csv_data)
            x_values = np.array([float(row[0]) for row in data[1:] if row[0]])  # Extract first column as X
            y_values = np.array([float(row[1]) for row in data[1:] if row[1]])  # Extract second column as Y       

            self.x = x_values
            self.y = y_values

            self.plot_file()

    def plot_file(self):
        self.main_window.signal_plot.clear()
        self.main_window.filtered_signal_plot.clear()
        filtered_signal= self.apply_filter()
        if (len(filtered_signal)) == 0 or np.isnan(np.real(filtered_signal[0])):
            filtered_signal = self.y

        if len(self.x) == 0:
            return
        
        y_min = np.min(self.y)
        y_max = np.max(self.y)
        y_min_f = np.real(np.min(filtered_signal))
        y_max_f = np.real(np.max(filtered_signal))

        self.set_ranges(self.x[-1], y_min, y_max, y_min_f, y_max_f)

        self.main_window.signal_plot.plot(self.x, self.y, pen=pg.mkPen('b', width=2))
        self.main_window.filtered_signal_plot.plot(self.x, np.real(filtered_signal), pen=pg.mkPen('r', width=2))

        self.run_signal(self.x[-1] / 10)

    def run_signal(self, step):
        if self.main_window.pad_controller.drawing:
            return
        self.timer.stop()
        self.step = step
        self.pointer = self.step
        self.timer.start(self.speed)
        self.moving = True

    def update(self):
        self.main_window.signal_plot.setXRange(self.pointer - self.step, self.pointer)
        self.main_window.filtered_signal_plot.setXRange(self.pointer - self.step, self.pointer)
        self.pointer += self.step * 0.01
        if self.pointer >= self.step *10:
              self.pointer = self.step

    def reset_signal(self):
        self.pointer = self.step

    def apply_filter(self):
        self.reset_signal()
        poles = self.main_window.filter_model.poles.copy()
        zeros = self.main_window.filter_model.zeroes.copy()
        gain = 1

        if len(self.y) < 7:
            return []

        if poles == [] and zeros == []:
            b, a = [1, 1], [1, 1]
        else :
            b, a = signal.zpk2tf(zeros, poles, gain)

        if len(self.y) <= 3 * (len(b) + 1) * (len(a) + 1):
            return []
        
        filtered_signal = signal.filtfilt(b, a, self.y)
        
        return filtered_signal
    
    def set_ranges(self, x_max, y_min, y_max, y_min_f, y_max_f):
        self.main_window.signal_plot.setLimits(xMin = 0, xMax = x_max, yMin = y_min, yMax = y_max)
        self.main_window.filtered_signal_plot.setLimits(xMin = 0, xMax = x_max, yMin = y_min_f, yMax = y_max_f)
        self.main_window.signal_plot.setXRange(x_max - 0.5, x_max)
        self.main_window.filtered_signal_plot.setXRange(x_max - 0.5, x_max)
        self.main_window.signal_plot.setYRange(y_min, y_max)
        self.main_window.filtered_signal_plot.setYRange(y_min_f, y_max_f)
    
    def change_filter_speed(self, value):
        self.speed = 10 + 100 - value
        if self.moving:
            self.timer.stop()
            self.timer.start(self.speed)

    def clear_plots_data(self):
        self.x = []
        self.y = []
        self.timer.stop()
        self.moving = False