from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class ResponsePlot(QWidget):
    def __init__(self, parent=None, title="", xlabel="", ylabel="",plot_type = "mag"):
        super().__init__(parent)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.plot_type = plot_type
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.ax = self.figure.add_subplot(111)

        self.reset_plot()
    
    def plot_response(self, x, y):
        self.ax.clear()
        self.ax.set_title(self.title, fontsize=10)
        self.ax.set_xlabel(self.xlabel, fontsize=8)
        self.ax.set_ylabel(self.ylabel, fontsize=8)
        self.ax.tick_params(axis='both', which='major', labelsize=6)
        self.ax.tick_params(axis='both', which='minor', labelsize=4)
        self.ax.set_xlim(-np.pi, np.pi)
        self.ax.grid()
        self.ax.plot(x, y, linewidth=1.2)
        self.canvas.draw()

    def reset_plot(self):
        x = np.linspace(-np.pi, np.pi, 1000)
        if self.plot_type == "magnitude":
            y = np.ones(1000)
        else:
            y = np.zeros(1000)
        self.plot_response(x,y)

        
