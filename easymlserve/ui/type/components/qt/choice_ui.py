from random import choices
from tabnanny import check
from typing import Iterable, Union, List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from . import BaseQtUI


class QtMultipleChoiceUI(BaseQtUI):
    """Multiple choice Qt UI element."""

    def __init__(self,
                 choices: List[str],
                 **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        group_box_layout = QGridLayout()
        self.checkboxes = []
        for choice in choices:
            checkbox = QCheckBox(choice)
            self.checkboxes.append(checkbox)
            group_box_layout.addWidget(checkbox)
        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def get_value(self):
        choices = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                choices.append(checkbox.text())
        return choices

    def set_value(self, value: Union[str, List[str]]):
        if isinstance(value, Iterable):
            choices = value
        else:
            choices = [value]

        for checkbox in self.checkboxes:
            if checkbox.text() in choices:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)


class QtSingleChoiceUI(BaseQtUI):
    """Single choice Qt UI element."""

    def __init__(self,
                 choices: List[str],
                 **kwargs):
        super().__init__(**kwargs)
        self.choices = choices
        group_box_layout = QGridLayout()
        self.radios = []
        for choice in choices:
            radio = QRadioButton(choice)
            self.radios.append(radio)
            group_box_layout.addWidget(radio)
        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def get_value(self):
        for radio in self.radios:
            if radio.isChecked():
                return radio.text()

    def set_value(self, value: str):
        for radio in self.radios:
            if radio.text() == value:
                radio.setChecked(True)
            else:
                radio.setChecked(False)
