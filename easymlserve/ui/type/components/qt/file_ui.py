import shutil

from PyQt6.QtWidgets import *

from . import BaseQtUI


class QtFileUI(BaseQtUI):
    """File Input or Output Qt UI element."""

    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)
        self.file_path = None

        group_box_layout = QVBoxLayout()
        self.setLayout(group_box_layout)

        self.file_path_display = QLineEdit()
        self.file_path_display.setReadOnly(True)
        group_box_layout.addWidget(self.file_path_display)

        if self.kind == 'input':
            self.btn_file_dialog = QPushButton('Load File')
            self.btn_file_dialog.clicked.connect(self.load_file_dialog)
        else:
            self.btn_file_dialog = QPushButton('Save File')
            self.btn_file_dialog.clicked.connect(self.save_file_dialog)
        group_box_layout.addWidget(self.btn_file_dialog)

        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def update_file_path(self):
        self.file_path_display.setText(self.file_path)

    def load_file_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Load File', '.', 'Files (*)')
        if fname[0]:
            self.file_path = fname[0]
        self.update_file_path()

    def save_file_dialog(self):
        if self.file_path is not None:
            fname = QFileDialog.getSaveFileName(
                self, 'Save File', '.', 'Files (*)')
            if fname[0]:
                shutil.copy(self.file_path, fname[0])

    def get_value(self):
        if self.file_path is None:
            return None
        else:
            with open(self.file_path, 'rb') as file:
                return file.read()

    def set_value(self, value: str):
        self.file_path = value
        self.update_file_path()