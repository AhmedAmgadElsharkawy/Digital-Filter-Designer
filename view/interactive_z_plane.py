from view.z_plane import ZPlane
from PyQt5.QtCore import Qt, QPointF


class InteractiveZPlane(ZPlane):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.dragging_item = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        position = self.mapToScene(event.pos())

        graphical_item = self.get_graphical_item_at_position(position)

        if event.button() == Qt.MouseButton.LeftButton:
            if graphical_item:
                self.dragging_item = graphical_item
                self.setCursor(Qt.ClosedHandCursor)

                complex_value = self.graphical_items[graphical_item]["complex value"]
                complex_value = complex(round(complex_value.real, 5), round(complex_value.imag, 5))
                print(f"Complex value of the clicked item: {complex_value}")

            else:
                graphical_item_type = self.main_window.complex_type
                x, y = position.x(), -position.y()
                complex_value = complex(round(x / 100, 5), round(y / 100, 5))
                print(f"Complex value of the clicked item: {complex_value}")

                if graphical_item_type == "Pole" or graphical_item_type == "Zero" or complex_value.imag == 0:
                    self.add_graphical_item(position)
                else:
                    self.add_graphical_conjugate_items(position)

                self.main_window.filter_model.add_complex_value(complex_value, graphical_item_type)
                print(self.main_window.filter_model.poles)

        if event.button() == Qt.MouseButton.RightButton and graphical_item:
            graphical_item_type = self.graphical_items[graphical_item]["type"]
            complex_value = self.graphical_items[graphical_item]["complex value"]
            self.main_window.filter_model.remove_complex_value(complex_value, graphical_item_type)
            self.remove_graphical_item(position)

    def mouseMoveEvent(self, event):
        position = self.mapToScene(event.pos())

        if self.dragging_item:
            bounding_rect = self.dragging_item.boundingRect()
            x_offset = bounding_rect.width() / 2
            y_offset = bounding_rect.height() / 2
            self.dragging_item.setPos(position.x() - x_offset, position.y() - y_offset)

            conjugate_item = self.graphical_items.get(self.dragging_item, {}).get('conjugate')
            if conjugate_item:
                conjugate_position = QPointF(position.x() - x_offset, -position.y() - y_offset)
                conjugate_item.setPos(conjugate_position)

        else:
            hovered_pole = self.get_graphical_item_at_position(position)
            if hovered_pole:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.dragging_item:
            position = self.dragging_item.pos()
            x, y = round(position.x() / 100, 5), round(-position.y() / 100, 5)
            new_complex_value = complex(x, y)

            old_complex_value = self.graphical_items[self.dragging_item]["complex value"]
            graphical_item_type = self.graphical_items[self.dragging_item]["type"]

            self.main_window.filter_model.remove_complex_value(old_complex_value, graphical_item_type)
            self.main_window.filter_model.add_complex_value(new_complex_value, graphical_item_type)

            self.graphical_items[self.dragging_item]["complex value"] = new_complex_value

            conjugate_item = self.graphical_items.get(self.dragging_item, {}).get('conjugate')
            if conjugate_item:
                conjugate_position = conjugate_item.pos()
                conj_x, conj_y = round(conjugate_position.x() / 100, 5), round(-conjugate_position.y() / 100, 5)
                new_conjugate_value = complex(conj_x, conj_y)

                if graphical_item_type == "Conj Poles":
                    self.main_window.filter_model.remove_conj_poles(old_complex_value)
                    self.main_window.filter_model.add_conj_poles(new_conjugate_value)
                elif graphical_item_type == "Conj Zeroes":
                    self.main_window.filter_model.remove_conj_zeroes(old_complex_value)
                    self.main_window.filter_model.add_conj_zeroes(new_conjugate_value)

                self.graphical_items[conjugate_item]["complex value"] = new_conjugate_value

            self.dragging_item = None
            self.setCursor(Qt.ArrowCursor)
