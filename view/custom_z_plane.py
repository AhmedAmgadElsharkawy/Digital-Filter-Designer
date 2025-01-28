from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPainter
import math


class CustomZPlane(QGraphicsView):
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

        self.poles = []
        self.dragging_pole = None

        self.setMouseTracking(True)
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

    def mousePressEvent(self, event):
        position = self.mapToScene(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            clicked_pole = self.get_pole_at_position(position)
            if clicked_pole:
                self.dragging_pole = clicked_pole
                self.setCursor(Qt.ClosedHandCursor)  # Change cursor to closed hand
            else:
                self.add_pole(position)
        elif event.button() == Qt.MouseButton.RightButton:
            self.remove_pole(position)

    def mouseMoveEvent(self, event):
        position = self.mapToScene(event.pos())

        if self.dragging_pole:
            bounding_rect = self.dragging_pole.boundingRect()
            x_offset = bounding_rect.width() / 2
            y_offset = bounding_rect.height() / 2
            self.dragging_pole.setPos(position.x() - x_offset, position.y() - y_offset)
        else:
            hovered_pole = self.get_pole_at_position(position)
            if hovered_pole:
                self.setCursor(Qt.OpenHandCursor)  # Change cursor to open hand when hovering
            else:
                self.setCursor(Qt.ArrowCursor)  # Default cursor

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_pole = None
            self.setCursor(Qt.ArrowCursor)  # Revert to default cursor


    def add_pole(self, position):
        pole = QGraphicsTextItem("X")
        pole.setDefaultTextColor(Qt.GlobalColor.black)
        
        font = pole.font()
        font.setPointSize(7)  # Adjust this value to control the size of the pole
        pole.setFont(font)

        bounding_rect = pole.boundingRect()
        x_offset = bounding_rect.width() / 2
        y_offset = bounding_rect.height() / 2

        pole.setPos(position.x() - x_offset, position.y() - y_offset)

        self.scene.addItem(pole)
        self.poles.append(pole)


    def remove_pole(self, position):
        clicked_pole = self.get_pole_at_position(position)
        if clicked_pole:
            self.scene.removeItem(clicked_pole)
            self.poles.remove(clicked_pole)

    def get_pole_at_position(self, position):
        for pole in self.poles:
            bounding_rect = pole.sceneBoundingRect()
            if bounding_rect.contains(position):
                return pole
        return None

