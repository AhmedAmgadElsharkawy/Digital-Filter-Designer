from view.z_plane import ZPlane
from PyQt5.QtCore import Qt, QPointF


class InteractiveZPlane(ZPlane):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.dragging_pole = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        position = self.mapToScene(event.pos())

        graphical_item = self.get_graphical_item_at_position(position)

        if event.button() == Qt.MouseButton.LeftButton:
            if graphical_item:
                self.dragging_pole = graphical_item
                self.setCursor(Qt.ClosedHandCursor)
            else:
                graphical_item_type = self.main_window.complex_type

                if graphical_item_type == "Pole" or graphical_item_type == "Zero":
                    self.add_graphical_item(position)
                else:
                    self.add_graphical_conjugate_items(position)
                x, y = position.x(), -position.y()
                complex_value = complex(x / 100, y / 100)

                if graphical_item_type == "Pole":
                    self.main_window.filter_model.add_pole(complex_value)
                if graphical_item_type == "Zero":
                    self.main_window.filter_model.add_zero(complex_value)
                if graphical_item_type == "Conj Poles":
                    self.main_window.filter_model.add_conj_poles(complex_value)
                if graphical_item_type == "Conj Zeroes":
                    self.main_window.filter_model.add_conj_zeroes(complex_value)

        if event.button() == Qt.MouseButton.RightButton and graphical_item:
            graphical_item_type = self.graphical_items[graphical_item]["type"]
            if graphical_item_type == "Pole":
                self.main_window.filter_model.remove_pole(self.graphical_items[graphical_item]["complex value"])
            if graphical_item_type == "Zero":
                self.main_window.filter_model.remove_zero(self.graphical_items[graphical_item]["complex value"])
            if graphical_item_type == "Conj Poles":
                self.main_window.filter_model.remove_conj_poles(self.graphical_items[graphical_item]["complex value"])
            if graphical_item_type == "Conj Zeroes":
                self.main_window.filter_model.remove_conj_zeroes(self.graphical_items[graphical_item]["complex value"])
            self.remove_graphical_item(graphical_item)

    def mouseMoveEvent(self, event):
        position = self.mapToScene(event.pos())

        if self.dragging_pole:
            bounding_rect = self.dragging_pole.boundingRect()
            x_offset = bounding_rect.width() / 2
            y_offset = bounding_rect.height() / 2
            self.dragging_pole.setPos(position.x() - x_offset, position.y() - y_offset)

            conjugate_item = self.graphical_items.get(self.dragging_pole, {}).get('conjugate')
            if conjugate_item:
                conjugate_position = QPointF(position.x() - x_offset, -position.y() + y_offset)
                conjugate_item.setPos(conjugate_position)

        else:
            hovered_pole = self.get_graphical_item_at_position(position)
            if hovered_pole:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_pole = None
            self.setCursor(Qt.ArrowCursor)
