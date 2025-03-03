import sys
from PyQt5.QtCore import Qt, QTimer, QTime, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QWidget
import math

class PaddingArea(QWidget):
    def __init__(self):
        super().__init__()

        self.pad_controller = None
        self.paths = []
        self.opacity = 255

        self.last_pos = None
        self.last_time = QTime.currentTime()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fade_lines)
        self.timer.start(10)

        self.setGeometry(100, 100, 600, 400)

    def fade_lines(self):
        for path in self.paths:
            if path['opacity'] > 0:
                path['opacity'] -= 5
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        grid_spacing = 20
        grid_color = QColor(220, 220, 220)

        painter.setPen(grid_color)
        
        for x in range(0, self.width(), grid_spacing):
            painter.drawLine(x, 0, x, self.height())

        for y in range(0, self.height(), grid_spacing):
            painter.drawLine(0, y, self.width(), y)

        for path in self.paths:
            painter.setBrush(QColor(0, 0, 0, path['opacity']))
            for point in path['points']:
                painter.drawEllipse(point, 3, 3)

        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont('Arial', 12))

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:  
            return 

        path = {'points': [], 'opacity': self.opacity}
        self.paths.append(path)

        path['points'].append(event.pos())

        self.pad_controller.add_point(self.last_pos, event.pos(), self.last_time, QTime.currentTime())
        self.last_pos = event.pos()
        self.last_time = QTime.currentTime()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.paths.clear()



