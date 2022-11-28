from itertools import groupby
import numpy as np
import PIL
from PIL.ImageQt import ImageQt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *

from . import BaseQtUI


class QtImageUI(BaseQtUI):
    """Image Qt UI element."""

    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)
        self.image = None
        group_box_layout = QVBoxLayout()
        self.image_plane = QLabel()
        self.image_plane.setMinimumHeight(300)
        self.image_plane.setAlignment(Qt.AlignmentFlag.AlignHCenter |
                                      Qt.AlignmentFlag.AlignVCenter)
        group_box_layout.addWidget(self.image_plane, stretch=3)
        self.btn_file_dialog = QPushButton('Load Image')
        self.btn_file_dialog.clicked.connect(self.file_dialog)
        group_box_layout.addWidget(self.btn_file_dialog)

        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def resizeEvent(self, event):
        self.update_image()

    def update_image(self):
        if self.image is None:
            return
        else:
            pil_image = PIL.Image.fromarray(
                self.image.astype('uint8'), 'RGB')
            qimage = ImageQt(pil_image)
            qimage.bits()
            pix = QPixmap.fromImage(qimage)
            pix = pix.scaled(0.95 * self.image_plane.width(),
                             0.95 * self.image_plane.height(),
                             Qt.AspectRatioMode.KeepAspectRatio)
            self.image_plane.setPixmap(pix)

    def file_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Load Image', '.', 'Image Files (*.png, *.jpg)')
        if fname[0]:
            image = PIL.Image.open(fname[0])
            image = np.asarray(image)
            self.image = image
        self.update_image()

    def get_value(self):
        return self.image

    def set_value(self, value: np.ndarray):
        self.image = value
        self.update_image()