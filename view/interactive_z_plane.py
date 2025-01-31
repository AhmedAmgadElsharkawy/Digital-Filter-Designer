from view.z_plane import ZPlane
from PyQt5.QtCore import Qt, QPointF


class InteractiveZPlane(ZPlane):
    def __init__(self, main_window):
        super().__init__(main_window)

        self.selected_item = None
        self.dragging_item = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        position = self.mapToScene(event.pos())

        graphical_item = self.get_graphical_item_at_position(position)

        if event.button() == Qt.MouseButton.LeftButton:
            if graphical_item:
                
                self.change_item_position_graphically(graphical_item,position)
                position = graphical_item.pos()
                x, y = round(position.x() / 100, 5), round(-position.y() / 100, 5)
                new_complex_value = complex(x, y)

                old_complex_value = self.graphical_items[graphical_item]["complex value"]
                graphical_item_type = self.graphical_items[graphical_item]["type"]

                self.main_window.filter_model.remove_complex_value(old_complex_value, graphical_item_type)
                self.main_window.filter_model.add_complex_value(new_complex_value, graphical_item_type)

                self.graphical_items[graphical_item]["complex value"] = new_complex_value


                self.dragging_item = graphical_item
                self.selected_item = self.dragging_item

                self.update_input_fields()
                self.setCursor(Qt.ClosedHandCursor)

                complex_value = self.graphical_items[graphical_item]["complex value"]

            else:
                graphical_item_type = self.main_window.complex_type
                x, y = position.x(), -position.y()
                complex_value = complex(round(x / 100, 5), round(y / 100, 5))

                if graphical_item_type == "Pole" or graphical_item_type == "Zero" or complex_value.imag == 0:
                    self.add_graphical_item(position)
                else:
                    self.add_graphical_conjugate_items(position)

                self.main_window.filter_model.add_complex_value(complex_value, graphical_item_type)
                self.selected_item = self.get_graphical_item_at_position(position)
                self.update_input_fields()


        if event.button() == Qt.MouseButton.RightButton and graphical_item:
            if graphical_item == self.selected_item:
                self.disable_input_fields()
            graphical_item_type = self.graphical_items[graphical_item]["type"]
            complex_value = self.graphical_items[graphical_item]["complex value"]
            self.main_window.filter_model.remove_complex_value(complex_value, graphical_item_type)
            self.remove_graphical_item(position)

    def mouseMoveEvent(self, event):
        position = self.mapToScene(event.pos())
        if self.dragging_item:
            self.change_item_position_graphically(self.dragging_item,position)
            self.selected_item = self.dragging_item
            self.update_input_fields()
            
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

    def change_item_position_graphically(self,item,new_pos):
        bounding_rect = item.boundingRect()
        x_offset = bounding_rect.width() / 2
        y_offset = bounding_rect.height() / 2
        item.setPos(new_pos.x() - x_offset, new_pos.y() - y_offset)
        conjugate_item = self.graphical_items.get(item, {}).get('conjugate')
        if conjugate_item:
            conjugate_position = QPointF(new_pos.x() - x_offset, -new_pos.y() - y_offset)
            conjugate_item.setPos(conjugate_position)

    def update_input_fields(self):
        self.main_window.filter_raal_value_input_field.double_spin_box.blockSignals(True)
        self.main_window.filter_imag_value_input_field.double_spin_box.blockSignals(True)
        
        self.main_window.filter_raal_value_input_field.setEnabled(True)
        self.main_window.filter_imag_value_input_field.setEnabled(True)
        x, y = self.selected_item.pos().x(), self.selected_item.pos().y()
        complex_value = complex(x/100,-y/100)
        self.main_window.filter_raal_value_input_field.setValue(complex_value.real)
        self.main_window.filter_imag_value_input_field.setValue(complex_value.imag)
        

        self.main_window.filter_raal_value_input_field.double_spin_box.blockSignals(False)
        self.main_window.filter_imag_value_input_field.double_spin_box.blockSignals(False)

    def disable_input_fields(self):
        self.main_window.filter_raal_value_input_field.double_spin_box.blockSignals(True)
        self.main_window.filter_imag_value_input_field.double_spin_box.blockSignals(True)
        self.main_window.filter_raal_value_input_field.setValue(0)
        self.main_window.filter_imag_value_input_field.setValue(0)
        self.main_window.filter_raal_value_input_field.setEnabled(False)
        self.main_window.filter_imag_value_input_field.setEnabled(False)
        self.main_window.filter_raal_value_input_field.double_spin_box.blockSignals(False)
        self.main_window.filter_imag_value_input_field.double_spin_box.blockSignals(False)

        

