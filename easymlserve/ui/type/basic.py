from typing import List, Union, Literal

import gradio

from easymlserve.ui.type.components.qt import *
from easymlserve.ui.type.components.qt.choice_ui import QtMultipleChoiceUI, QtSingleChoiceUI


class BaseType:
    """Basic UI type class used for all UIs (e.g. Gradio or Qt)."""

    def __init__(self,
                 name: str = '',
                 description: str = '') -> None:
        self.name = name
        self.description = description

    def to_gradio(self):
        """Return gradio UI element.

        Raises:
            NotImplementedError: If Gradio UI class does not implement UI type.
        """
        raise NotImplementedError(
            f'{self.__class__.__name__} has no UI elements for Gradio.'
        )

    def to_qt(self, kind: Literal['input', 'output']):
        """_summary_

        Args:
            kind (Literal[&#39;input&#39;, &#39;output&#39;]): Kind of Qt UI element.

        Raises:
            NotImplementedError: If Qt UI type is not implemented for Qt.
        """
        raise NotImplementedError(
            f'{self.__class__.__name__} has no UI elements for Qt.'
        )


class Text(BaseType):
    """Short text UI type."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_gradio(self):
        if self.name == '':
            return gradio.Textbox(lines=1, show_label=False)
        else:
            return gradio.Textbox(label=self.name, lines=5)

    def to_qt(self, kind: Literal['input', 'output']):
        return QtTextUI(name=self.name, kind=kind)


class TextLong(BaseType):
    """Long text UI type."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_gradio(self):
        if self.name == '':
            return gradio.Textbox(lines=5, show_label=False)
        else:
            return gradio.Textbox(label=self.name, lines=5)

    def to_qt(self, kind: Literal['input', 'output']):
        return QtTextLongUI(name=self.name, kind=kind)


class Number(BaseType):
    """Number UI type."""

    def __init__(self, dtype=int, precision=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dtype = dtype
        if self.dtype == int:
            self.precision = 1
        elif precision is None:
            self.precision = 2
        else:
            self.precision = precision

    def to_gradio(self):
        if self.name == '':
            return gradio.Number(show_label=False, precision=self.precision)
        else:
            return gradio.Number(label=self.name, precision=self.precision)

    def to_qt(self, kind: Literal['input', 'output']):
        return QtNumberUI(dtype=self.dtype, name=self.name,
                          precision=self.precision, kind=kind)


class Range(BaseType):
    """Range slider UI type."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def __init__(self,
                 minimum: Union[int, float],
                 maximum: Union[int, float],
                 dtype=float,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.minimum = minimum
        self.maximum = maximum
        self.dtype = dtype
        if isinstance(dtype, float):
            self.step = 0.01
        else:
            self.step = 1

    def to_gradio(self):
        if self.name == '':
            return gradio.Slider(self.minimum, self.maximum,
                                 step=self.step, show_label=False)
        else:
            return gradio.Slider(self.minimum, self.maximum,
                                 step=self.step, label=self.name)

    def to_qt(self, kind: Literal['input', 'output']):
        return QtSliderUI(self.minimum, self.maximum, self.step,
                          name=self.name, kind=kind)


class SingleChoice(BaseType):
    """Single choice UI type."""

    def __init__(self,
                 choices: List[str],
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices

    def to_gradio(self):
        if self.name == '':
            return gradio.Radio(self.choices, show_label=False)
        else:
            return gradio.Radio(self.choices, label=self.name)

    def to_qt(self, kind: Literal['input', 'output']):
        return QtSingleChoiceUI(self.choices, name=self.name, kind=kind)


class MultipleChoice(BaseType):
    """Multiple choice UI type."""

    def __init__(self, choices: List[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.choices = choices

    def to_gradio(self):
        if self.name == '':
            return gradio.CheckboxGroup(self.choices, show_label=False)
        else:
            return gradio.CheckboxGroup(self.choices, label=self.name)

    def to_qt(self, kind: Literal['input', 'output']):
        return QtMultipleChoiceUI(self.choices, name=self.name, kind=kind)
