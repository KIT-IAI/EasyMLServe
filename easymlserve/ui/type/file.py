from typing import Union, List, Literal

import gradio

from easymlserve.ui.type.components.qt import *

from . import BaseType


class File(BaseType):
    """File UI type."""

    def __init__(self, is_output=False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.is_output = is_output

    def to_gradio(self):
        if self.name == '':
            return gradio.File(show_label=False, type='bytes')
        else:
            return gradio.File(label=self.name, type='bytes')

    def to_qt(self, kind: Literal['input', 'output']):
        return QtFileUI(name=self.name, kind=kind)


class ImageFile(File):
    """Image file UI type."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_gradio(self):
        if self.name == '':
            return gradio.Image(show_label=False, type='numpy')
        else:
            return gradio.Image(label=self.name, type='numpy')

    def to_qt(self, kind: Literal['input', 'output']):
        return QtImageUI(name=self.name, kind=kind)


class CSVFile(File):
    """CSV file UI Type."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class TimeSeriesCSVFile(CSVFile):
    """Time Series CSV file UI type."""

    def __init__(self, time: str, values: Union[str, List[str]], **kwargs) -> None:
        super().__init__(**kwargs)
        self.time = time
        self.values = values

    def to_gradio(self):
        if self.name == '':
            return gradio.TimeSeries(x=self.time, y=self.values,
                                     show_label=False)
        else:
            return gradio.TimeSeries(x=self.time, y=self.values,
                                     label=self.name)

    def to_qt(self, kind: Literal['input', 'output']):
        raise NotImplementedError(
            'A qt UI is not implemented for TimeSeriesCSVFile class. '
            'Please use CSVFile or File as input or output Type.'
        )
