from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPainter
import math


class ZPlane(QGraphicsView):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

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

        self.graphical_items = {}

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

    def add_graphical_item(self, position):
        x, y = position.x(), -position.y()
        complex_value = complex(x / 100, y / 100)

        graphical_item_shape = ''
        if self.main_window.complex_type == "Pole" or self.main_window.complex_type == "Conj Poles":
            graphical_item_shape = 'X'
        else:
            graphical_item_shape = 'O'

        graphical_item = QGraphicsTextItem(graphical_item_shape)
        graphical_item.setDefaultTextColor(Qt.GlobalColor.black)

        font = graphical_item.font()
        font.setPointSize(7)
        graphical_item.setFont(font)

        bounding_rect = graphical_item.boundingRect()
        x_offset = bounding_rect.width() / 2
        y_offset = bounding_rect.height() / 2
        graphical_item.setPos(x - x_offset, position.y() - y_offset)

        self.scene.addItem(graphical_item)

        self.graphical_items[graphical_item] = {"complex value": complex_value, "type": self.main_window.complex_type}

    def add_graphical_conjugate_items(self, position):
        self.add_graphical_item(position)
        
        x, y = position.x(), -position.y()
        conjugate_position = QPointF(x, y)
        self.add_graphical_item(conjugate_position)

        original_item = self.get_graphical_item_at_position(position)
        conjugate_item = self.get_graphical_item_at_position(conjugate_position)
        
        if original_item and conjugate_item:
            self.graphical_items[original_item]['conjugate'] = conjugate_item
            self.graphical_items[conjugate_item]['conjugate'] = original_item

    def remove_graphical_item(self, pole_graphical_item):
        if pole_graphical_item:
            conjugate_item = self.graphical_items.get(pole_graphical_item, {}).get('conjugate')
            if conjugate_item:
                self.scene.removeItem(conjugate_item)
                del self.graphical_items[conjugate_item]

            self.scene.removeItem(pole_graphical_item)
            del self.graphical_items[pole_graphical_item]

    def get_graphical_item_at_position(self, position):
        for pole in self.graphical_items.keys():
            if pole.sceneBoundingRect().contains(position):
                return pole
        return None
    
    def clear_poles_graphical_items(self):
        items_to_remove = [item for item, data in self.graphical_items.items() if data["type"] == "Pole" or data["type"] == "Conj Poles"]
        
        for item in items_to_remove:
            self.scene.removeItem(item)
            del self.graphical_items[item]

    def clear_zeroes_graphical_items(self):
        items_to_remove = [item for item, data in self.graphical_items.items() if data["type"] == "Zero" or data["type"] == "Conj Zeroes"]
        
        for item in items_to_remove:
            self.scene.removeItem(item)
            del self.graphical_items[item]

    def clear_all_graphical_items(self):
        items_to_remove = list(self.graphical_items.keys())
        
        for item in items_to_remove:
            self.scene.removeItem(item)
            del self.graphical_items[item]
