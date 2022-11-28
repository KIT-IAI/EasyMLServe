from typing import Literal

import gradio

from easymlserve.ui.type.components.qt import *
from easymlserve.ui.type.components.qt.plot_ui import QtPlotUI

from . import BaseType


class Plot(BaseType):
    """Plot UI type."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_gradio(self):
        if self.name == '':
            return gradio.Plot(show_label=False)
        else:
            return gradio.Plot(label=self.name)

    def to_qt(self, kind: Literal['input', 'output']):
        return QtPlotUI(name=self.name, kind=kind)


class Webcam(BaseType):
    """Webcam input UI type."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_gradio(self):
        if self.name == '':
            return gradio.Image(source='webcam', type='numpy', show_label=False)
        else:
            return gradio.Image(label=self.name, source='webcam', type='numpy')
