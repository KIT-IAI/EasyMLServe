from PyQt6.QtWidgets import QWidget


class BaseQtUI(QWidget):
    """Basic QT UI element for QtEasyMLUI."""

    def __init__(self,
                 name: str = '',
                 kind: str = 'input',
                 **kwargs):
        """Initialize basic Qt UI elements.

        Args:
            name (str, optional): Name of UI element. Defaults to ''.
            kind (str, optional): Kind of UI element (input or output).
                                  Defaults to 'input'.
        """
        super().__init__(**kwargs)
        self.name = name
        self.kind = kind

    def get_value(self):
        """Get actual UI value (e.g. text or image).

        Raises:
            NotImplemented: If child class not implements.
        """
        raise NotImplemented(
            'This QtUI has no get_value method. '
            'Please use a different input type.'
        )

    def set_value(self, value):
        """Set UI value (e.g. text or image).

        Args:
            value: Set value of UI element.

        Raises:
            NotImplemented: If not implemented by child class.
        """
        raise NotImplemented(
            'This QtUI has no set_value method. '
            'Please use a different output type.'
        )
