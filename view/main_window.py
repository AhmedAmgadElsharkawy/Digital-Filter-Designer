from PyQt5.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QLabel

from view.custom_z_plane import CustomZPlane


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fingerprint')
        self.setGeometry(300,300,1300, 500)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget_layout = QHBoxLayout(self.main_widget)
        self.main_widget_layout.setSpacing(10)
        
        self.custom_z_plane = CustomZPlane()
        self.main_widget_layout.addWidget(self.custom_z_plane)



        self.setStyleSheet("""
            
        """)
