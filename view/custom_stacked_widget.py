from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QStackedWidget, QHBoxLayout,
    QTextEdit, QGraphicsView, QGraphicsScene, QFileDialog, QRadioButton
)
from PyQt5.QtGui import QFont, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt
from controller.c_code_controller import CCodeController
from controller.structure_controller import StructureController

class CustomStackedWidget(QWidget):
    def __init__(self, filter_model=None):
        super().__init__()
        self.filter_model = filter_model
        self.c_code_controller = CCodeController(self.filter_model)
        self.structure_controller = StructureController(self.filter_model)
        
        # Setup layouts
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.central_layout)
        
        # Main widget setup
        self.main_widget = QWidget()
        self.main_widget.setObjectName("custom_stacked_widget_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setSpacing(15)
        self.central_layout.addWidget(self.main_widget)
        
        # Stack widget setup
        self.stack = QStackedWidget(self)
        self.main_widget_layout.addWidget(self.stack)
        
        # Buttons setup
        self.buttons_widget = QWidget()
        self.buttons_widget_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_widget_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toggle buttons
        self.toggle_buttons_widget = QWidget()
        self.toggle_buttons_widget_layout = QHBoxLayout(self.toggle_buttons_widget)
        self.toggle_buttons_widget_layout.setContentsMargins(0,0,0,0)
        self.buttons_widget_layout.addWidget(self.toggle_buttons_widget)
        
        self.structure_button = QPushButton("Structure", self)
        self.code_button = QPushButton("Code", self)
        self.structure_button.setDisabled(True)
        
        self.toggle_buttons_widget_layout.addWidget(self.structure_button)
        self.toggle_buttons_widget_layout.addWidget(self.code_button)
        
        # Filter form radio buttons
        self.filter_form_widget = QWidget()
        self.filter_form_layout = QHBoxLayout(self.filter_form_widget)
        self.direct_form = QRadioButton("Direct Form II")
        self.cascade_form = QRadioButton("Cascade Form")
        self.direct_form.setChecked(True)
        self.filter_form_layout.addWidget(self.direct_form)
        self.filter_form_layout.addWidget(self.cascade_form)
        self.buttons_widget_layout.addWidget(self.filter_form_widget)

        self.direct_form.toggled.connect(self.update_structure_view)
        self.cascade_form.toggled.connect(self.update_structure_view)

        # Connect filter model's updated signal to update methods
        self.filter_model.updated.connect(self.update_structure_view)
        self.filter_model.updated.connect(self.update_code_view)
        
        # Export button
        self.export_button = QPushButton("Export")
        self.buttons_widget_layout.addStretch()
        self.buttons_widget_layout.addWidget(self.export_button)
        
        self.main_widget_layout.addWidget(self.buttons_widget)
        
        # Structure view setup
        self.structure_widget = QWidget()
        self.structure_layout = QVBoxLayout(self.structure_widget)
        self.structure_layout.setContentsMargins(0, 0, 0, 0)
        
        self.graphics_view = QGraphicsView(self.structure_widget)
        self.graphics_view.setScene(QGraphicsScene(self.graphics_view))
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphics_view.setRenderHint(QPainter.Antialiasing)
        self.graphics_view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphics_view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphics_view.setStyleSheet("border: none;")
        self.graphics_view.wheelEvent = self.zoom_event 
        self.structure_layout.addWidget(self.graphics_view)
        self.stack.addWidget(self.structure_widget)  # Add this line

        
        # Code view setup
        self.code_widget = QTextEdit()
        self.code_widget.setReadOnly(True)
        self.code_widget.setFont(QFont("Courier", 12))
        self.code_widget.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
                border: none;
                padding: 10px;
            }
        """)
        self.stack.addWidget(self.code_widget)
        
        # Connect signals
        self.direct_form.toggled.connect(self.update_code_view)
        self.cascade_form.toggled.connect(self.update_code_view)
        self.structure_button.clicked.connect(lambda: self.switch_view(0))
        self.code_button.clicked.connect(lambda: self.switch_view(1))
        self.code_button.clicked.connect(self.show_code_view)
        self.export_button.clicked.connect(self.export_filter_structure)
        
        # Styling
        self.setStyleSheet("""
            #custom_stacked_widget_main_widget{
                border: 2px solid gray;
                border-radius:15px;
            }
        """)
        
        self.export_button.setFixedWidth(150)
        self.toggle_buttons_widget.setMaximumWidth(310)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        self.structure_button.setDisabled(index == 0)
        self.code_button.setDisabled(index == 1)

    def update_code_view(self):
        temp_filename = "temp_filter.c"
        method = "direct_form_II" if self.direct_form.isChecked() else "cascade_form"
        self.c_code_controller.generate_c_code(temp_filename, method=method)
        
        with open(temp_filename, 'r') as f:
            code = f.read()
        self.code_widget.setPlainText(code)

    def show_code_view(self):
        temp_filename = "temp_filter.c"
        method = "direct_form_II" if self.direct_form.isChecked() else "cascade_form"
        self.c_code_controller.generate_c_code(temp_filename, method=method)
        
        with open(temp_filename, 'r') as f:
            code = f.read()
        self.code_widget.setPlainText(code)
        self.stack.setCurrentIndex(1)

    def export_filter_structure(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Filter Structure", "", "PNG Files (*.png);;JPG Files (*.jpg)"
        )
        if filename:
            scene = self.graphics_view.scene()
            pixmap = scene.items()[0].pixmap()  
            pixmap.save(filename)  

    def update_structure_view(self):
        scene = self.graphics_view.scene()
        scene.clear()
        
        if self.direct_form.isChecked():
            fig = self.structure_controller.draw_direct_form_2()
        else:
            fig, ax = self.structure_controller.draw_cascade_form()
        
        if isinstance(fig, tuple):
            fig = fig[0]
            
        fig.canvas.draw()
        buf = fig.canvas.buffer_rgba()
        w, h = buf.shape[:2]
        qimage = QImage(buf, w, h, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        
        self.graphics_view.setSceneRect(0, 0, w, h)
        scene.addPixmap(pixmap)
        self.structure_controller.cleanup_figure(fig)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        self.structure_button.setDisabled(index == 0)
        self.code_button.setDisabled(index == 1)
        if index == 0:
            self.update_structure_view()

    # Add zoom handler method:
    def zoom_event(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        # Save the scene pos
        old_pos = self.graphics_view.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        self.graphics_view.scale(zoom_factor, zoom_factor)

        # Get the new position
        new_pos = self.graphics_view.mapToScene(event.pos())

        # Move scene to old position
        delta = new_pos - old_pos
        self.graphics_view.translate(delta.x(), delta.y())


