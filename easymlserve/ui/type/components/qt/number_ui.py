from typing import Union

from PyQt6.QtWidgets import *

from . import BaseQtUI


class QtNumberUI(BaseQtUI):
    """Number Qt UI element."""

    def __init__(self, dtype=int, precision=0, **kwargs):
        super().__init__(**kwargs)
        self.dtype = dtype
        self.precision = precision
        group_box_layout = QVBoxLayout()
        if self.dtype == int:
            self.spin_box = QSpinBox()
            self.spin_box.setMinimum(-2147483648)
            self.spin_box.setMaximum(2147483647)
        else:
            self.spin_box = QDoubleSpinBox()
            self.spin_box.setMinimum(2.2250738585072014e-308)
            self.spin_box.setMaximum(1.7976931348623157e+308)
            self.spin_box.setSingleStep(0.1)
        if self.kind == 'output':
            self.spin_box.setReadOnly(True)
        group_box_layout.addWidget(self.spin_box)
        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def get_value(self):
        return self.spin_box.value()

    def set_value(self, value: Union[int, float]):
        self.spin_box.setValue(value)