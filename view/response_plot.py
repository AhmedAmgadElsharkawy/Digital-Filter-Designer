import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ResponsePlot(QWidget):
    def __init__(self, parent=None,title = "response",xlabel = "xlabel",ylabel = "ylabel"):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(8, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.grid()
        self.canvas.draw()

