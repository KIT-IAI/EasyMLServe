import sys

from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from .base_ui import BaseEasyMLUI


class QtEasyMLUI(BaseEasyMLUI):
    """Qt UI class to display a Qt UI for REST API calls."""

    def __init__(self,
                 width: int = 1024,
                 height: int = 768,
                 **kwargs):
        """Initialize Qt UI class.

        Args:
            width (int, optional): Qt UI width. Defaults to 1024.
            height (int, optional): Qt UI height. Defaults to 768.
        """
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle(self.name)
        main_layout = QHBoxLayout()
        side_bar_layout = QVBoxLayout()
        result_page_layout = QVBoxLayout()

        side_bar_layout.addStretch()
        self.inputs = {}
        for key, input_type in self.input_schema.items():
            qt_widget = input_type.to_qt(kind='input')
            side_bar_layout.addWidget(qt_widget)
            self.inputs[key] = qt_widget
        btn_send = QPushButton('Send')
        btn_send.clicked.connect(self.clicked)
        side_bar_layout.addWidget(btn_send)
        side_bar_layout.addStretch()

        self.outputs = []
        for output in self.output_schema:
            qt_widget = output.to_qt(kind='output')
            result_page_layout.addWidget(qt_widget)
            self.outputs.append(qt_widget)

        main_layout.addLayout(side_bar_layout, stretch=1)
        main_layout.addLayout(result_page_layout, stretch=2)
        self.window.setLayout(main_layout)
        self.window.resize(width, height)

    def run(self):
        """Start Qt UI."""
        self.window.show()
        sys.exit(self.app.exec())

    def clicked(self):
        """Clicked event of Qt UI class."""
        parent_kwargs = {}
        for key, element in self.inputs.items():
            value = element.get_value()
            parent_kwargs[key] = value
            if value is None:
                return
        results =  super().clicked(**parent_kwargs)
        if not (isinstance(results, list) or isinstance(results, tuple)):
            results = [results]
        for element, result in zip(self.outputs, results):
            element.set_value(result)
