from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPainter
import math


class ZPlane(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.scene.setSceneRect(-120, -120, 240, 240)
        self.unit_circle = QGraphicsEllipseItem(-100, -100, 200, 200)
        self.unit_circle.setPen(QPen(Qt.GlobalColor.gray, 2))
        self.scene.addItem(self.unit_circle)

        self.draw_circular_sections()
        self.draw_radial_lines()
        self.add_labels()

        self.pole_graphical_items = {}

        self.fit_to_view()

    def fit_to_view(self):
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        self.fit_to_view()
        super().resizeEvent(event)

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)

    def draw_circular_sections(self):
        pen = QPen(Qt.GlobalColor.lightGray, 1, Qt.DashLine)

        for radius in range(20, 100, 20):
            circle = QGraphicsEllipseItem(-radius, -radius, 2 * radius, 2 * radius)
            circle.setPen(pen)
            self.scene.addItem(circle)

    def draw_radial_lines(self):
        pen = QPen(Qt.GlobalColor.lightGray, 1, Qt.DashLine)

        center = QPointF(0, 0)
        radius = 100

        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = math.cos(rad) * radius
            y = math.sin(rad) * radius
            self.scene.addLine(center.x(), center.y(), x, y, pen)

    def add_labels(self):
        font = self.font()
        font.setPointSize(5)

        radius = 110
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x = math.cos(rad) * radius
            y = -math.sin(rad) * radius

            label = QGraphicsTextItem(f"{angle}°")
            label.setFont(font)
            label.setDefaultTextColor(Qt.GlobalColor.black)

            label_width = label.boundingRect().width()
            label_height = label.boundingRect().height()
            label.setPos(x - label_width / 2, y - label_height / 2)
            self.scene.addItem(label)

    def add_pole_graphically(self, position):
        x, y = position.x(), -position.y()
        pole_complex = complex(x / 100, y / 100)

        pole_graphical_item = QGraphicsTextItem("X")
        pole_graphical_item.setDefaultTextColor(Qt.GlobalColor.black)

        font = pole_graphical_item.font()
        font.setPointSize(7)
        pole_graphical_item.setFont(font)

        bounding_rect = pole_graphical_item.boundingRect()
        x_offset = bounding_rect.width() / 2
        y_offset = bounding_rect.height() / 2
        pole_graphical_item.setPos(x - x_offset, position.y() - y_offset)

        self.scene.addItem(pole_graphical_item)

        self.pole_graphical_items[pole_graphical_item] = pole_complex


    def remove_pole_graphically(self, pole_graphical_item):
        if pole_graphical_item:
            self.scene.removeItem(pole_graphical_item)
            del self.pole_graphical_items[pole_graphical_item]


    def get_pole_graphical_item_at_position(self, position):
        for pole in self.pole_graphical_items.keys():
            if pole.sceneBoundingRect().contains(position):
                return pole
        return None

