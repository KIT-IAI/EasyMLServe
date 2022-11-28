from PyQt6.QtWidgets import *

from . import BaseQtUI


class QtTextUI(BaseQtUI):
    """Long text Qt UI element."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        group_box_layout = QVBoxLayout()
        self.line_edit = QLineEdit()
        group_box_layout.addWidget(self.line_edit)
        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def get_value(self):
        return self.line_edit.text()

    def set_value(self, value: str):
        self.line_edit.setText(value)


class QtTextLongUI(BaseQtUI):
    """Short text Qt UI element."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = QVBoxLayout()
        if self.name != '':
            label = QLabel(self.name)
            layout.addWidget(label)
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def get_value(self):
        return self.text_edit.toPlainText()

    def set_value(self, value: str):
        self.text_edit.setPlainText(value)
