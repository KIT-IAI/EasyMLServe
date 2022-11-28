from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from . import BaseQtUI


class QtSliderUI(BaseQtUI):
    """Slider Qt UI element."""

    def __init__(self,
                 minimum: Union[int, float],
                 maximum: Union[int, float],
                 step: Union[int, float],
                 **kwargs):
        super().__init__(**kwargs)
        group_box_layout = QVBoxLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setSingleStep(step)
        self.slider.valueChanged.connect(self.slider_changed)
        group_box_layout.addWidget(self.slider)
        self.slider_state = QLabel(str(self.slider.value()))
        self.slider_state.setAlignment(
            Qt.AlignmentFlag.AlignCenter |
            Qt.AlignmentFlag.AlignVCenter
        )
        group_box_layout.addWidget(self.slider_state)

        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def slider_changed(self):
        value = self.slider.value()
        self.slider_state.setText(str(value))

    def get_value(self):
        return self.slider.value()

    def set_value(self, value: str):
        self.slider.setValue(value)
