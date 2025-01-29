from PyQt5.QtCore import Qt
from view.z_plane import ZPlane


class InteractiveZPlane(ZPlane):
    def __init__(self,filter_model):
        super().__init__()

        self.filter_model = filter_model

        self.dragging_pole = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        position = self.mapToScene(event.pos())
        pole_graphical_item = self.get_pole_graphical_item_at_position(position)

        if event.button() == Qt.MouseButton.LeftButton:
            if pole_graphical_item:
                self.dragging_pole = pole_graphical_item
                self.setCursor(Qt.ClosedHandCursor)  # Change cursor to closed hand
            else:
                self.add_pole_graphically(position)
                x, y = position.x(), -position.y()
                pole_complex = complex(x / 100, y / 100)
                self.filter_model.add_pole(pole_complex)
                
        elif event.button() == Qt.MouseButton.RightButton:
            self.filter_model.remove_pole(self.pole_graphical_items[pole_graphical_item])
            self.remove_pole_graphically(pole_graphical_item)

    def mouseMoveEvent(self, event):
        position = self.mapToScene(event.pos())

        if self.dragging_pole:
            bounding_rect = self.dragging_pole.boundingRect()
            x_offset = bounding_rect.width() / 2
            y_offset = bounding_rect.height() / 2
            self.dragging_pole.setPos(position.x() - x_offset, position.y() - y_offset)
        else:
            hovered_pole = self.get_pole_graphical_item_at_position(position)
            if hovered_pole:
                self.setCursor(Qt.OpenHandCursor) 
            else:
                self.setCursor(Qt.ArrowCursor)  

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_pole = None
            self.setCursor(Qt.ArrowCursor)  



