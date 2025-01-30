from PyQt5.QtWidgets import QFileDialog
import pyqtgraph as pg
import csv
import numpy as np
class SignalController():
    def __init__(self,main_window):
        self.main_window = main_window

    def import_signal(self):
        self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls)" )
        if self.fileName[0]:  
                    self.plot_file(self.fileName[0])

    def plot_file(self, path:str):
          self.main_window.signal_plot.clear()
          with open(path, 'r') as file:
                csv_data = csv.reader(file, delimiter=',')
                data = list(csv_data)
                x_values = np.array([float(row[0]) for row in data[1:] if row[0]])  # Extract first column as X
                y_values = np.array([float(row[1]) for row in data[1:] if row[1]])  # Extract second column as Y

                self.main_window.signal_plot.plot(x_values, y_values, pen=pg.mkPen('b', width=2))