from PyQt5.QtCore import Qt
from view.z_plane import ZPlane


class InteractiveZPlane(ZPlane):
    def __init__(self):
        super().__init__()

        self.dragging_pole = None
        self.setMouseTracking(True)

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



