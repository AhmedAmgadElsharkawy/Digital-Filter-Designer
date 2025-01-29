from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ResponsePlot(QWidget):
    def __init__(self, parent=None, title="", xlabel="", ylabel=""):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.ax = self.figure.add_subplot(111)

        self.ax.set_title(title, fontsize=10)
        self.ax.set_xlabel(xlabel, fontsize=8) 
        self.ax.set_ylabel(ylabel, fontsize=8) 

        self.ax.tick_params(axis='both', which='major', labelsize=6)
        self.ax.tick_params(axis='both', which='minor', labelsize=4) 
        
        self.ax.grid()
        
        # self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove extra margins
        # self.figure.tight_layout(pad=0)  # Reduce padding

        self.canvas.draw()
