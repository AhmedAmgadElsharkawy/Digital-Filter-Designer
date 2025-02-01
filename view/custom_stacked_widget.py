from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
    QHBoxLayout,
    QTextEdit,
    QGraphicsView,
    QGraphicsScene,
)
from PyQt5.QtGui import QFont


class CustomStackedWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.central_layout)

        self.main_widget = QWidget()
        self.main_widget.setObjectName("custom_stacked_widget_main_widget")
        self.main_widget_layout = QVBoxLayout(self.main_widget)
        self.main_widget_layout.setSpacing(15)
        # self.main_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.addWidget(self.main_widget)

        self.buttons_widget = QWidget()
        self.buttons_widget_layout = QHBoxLayout(self.buttons_widget)
        self.buttons_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_buttons_widget = QWidget()
        self.toggle_buttons_widget_layout = QHBoxLayout(self.toggle_buttons_widget)
        self.toggle_buttons_widget_layout.setContentsMargins(0,0,0,0)
        self.buttons_widget_layout.addWidget(self.toggle_buttons_widget)

        self.structure_button = QPushButton("Structure", self)
        self.structure_button.setDisabled(True)
        self.code_button = QPushButton("Code", self)

        self.toggle_buttons_widget_layout.addWidget(self.structure_button)
        self.toggle_buttons_widget_layout.addWidget(self.code_button)

        self.export_button = QPushButton("Export")
        self.buttons_widget_layout.addStretch()
        self.buttons_widget_layout.addWidget(self.export_button)

        self.main_widget_layout.addWidget(self.buttons_widget)

        self.stack = QStackedWidget(self)
        self.main_widget_layout.addWidget(self.stack)

        self.structure_widget = QWidget()
        self.structure_layout = QVBoxLayout(self.structure_widget)
        self.structure_layout.setContentsMargins(0, 0, 0, 0)

        self.graphics_view = QGraphicsView(self.structure_widget)
        self.graphics_view.setScene(QGraphicsScene(self.graphics_view))
        self.graphics_view.scene().setSceneRect(0, 0, 0, 0)
        self.graphics_view.setStyleSheet("border: none;")
        self.structure_layout.addWidget(self.graphics_view)
        self.structure_widget.setLayout(self.structure_layout)
        self.stack.addWidget(self.structure_widget)

        self.code_widget = QTextEdit()
        self.code_widget.setReadOnly(True)
        self.code_widget.setFont(QFont("Courier", 12))
        self.code_widget.setStyleSheet(
            """
            QTextEdit {
                background-color: white;
                color: black;
                border: none;
                padding: 10px;
            }
        """
        )

        sample_code = """from PyQt5.QtWidgets import QApplication, QTextEdit
                        app = QApplication([])
                        editor = QTextEdit()
                        editor.setPlainText("Hello, this is a code block!")
                        editor.show()
                        app.exec_()"""

        self.code_widget.setPlainText(sample_code)
        self.stack.addWidget(self.code_widget)

        self.structure_button.clicked.connect(lambda: self.switch_view(0))
        self.code_button.clicked.connect(lambda: self.switch_view(1))

        self.setStyleSheet(
            """
            #custom_stacked_widget_main_widget{
                           border: 2px solid gray;
                           border-radius:15px;
                           }
        """
        )

        self.export_button.setFixedWidth(150)
        self.toggle_buttons_widget.setMaximumWidth(310)

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)
        self.structure_button.setDisabled(index == 0)
        self.code_button.setDisabled(index == 1)

