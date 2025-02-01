from PyQt5.QtWidgets import QWidget,QHBoxLayout,QLabel,QDoubleSpinBox


class CustomDoubleSpinBox(QWidget):
    def __init__(self,label = "label",range_start = 0.00010,range_end = 0.49999,initial_value = 0.1,decimals = 5,step_value = 0.1):
        super().__init__()
        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_widget = QWidget()
        self.main_widget_layout = QHBoxLayout(self.main_widget)
        self.main_widget_layout.setContentsMargins(0,0,0,0)
        self.central_layout.addWidget(self.main_widget)
        
        self.label = QLabel(label)
        self.main_widget_layout.addWidget(self.label)
        self.double_spin_box = QDoubleSpinBox()
        self.double_spin_box.setRange(range_start, range_end)
        self.double_spin_box.setValue(initial_value)
        self.double_spin_box.setDecimals(decimals)
        self.double_spin_box.setSingleStep(step_value)
        self.main_widget_layout.addWidget(self.double_spin_box)

        self.double_spin_box.setButtonSymbols(QDoubleSpinBox.NoButtons)

    def value(self):
        return self.double_spin_box.value()
    
    def setValue(self,value):
        self.double_spin_box.setValue(value)

    def disable(self):
        self.double_spin_box.setDisabled(True)

    def enable(self):
        self.double_spin_box.setDisabled(False)

        

