from PyQt5.QtWidgets import QFileDialog
class SignalController():
    def __init__(self,main_window):
        self.main_window = main_window

    def import_signal(self):
        self.fileName = QFileDialog.getOpenFileName(None,"Open a File","./",filter="Raw Data(*.txt *.csv *.xls)" )