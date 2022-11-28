from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

import PIL
from PIL.ImageQt import ImageQt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QResizeEvent
from PyQt6.QtWidgets import *

from . import BaseQtUI


class QtPlotUI(BaseQtUI):
    """Plot Qt UI element."""

    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)
        self.figure = None

        group_box_layout = QVBoxLayout()
        self.figure_plane = QLabel()
        self.figure_plane.setMinimumHeight(300)
        self.figure_plane.setAlignment(Qt.AlignmentFlag.AlignHCenter |
                                       Qt.AlignmentFlag.AlignVCenter)
        group_box_layout.addWidget(self.figure_plane, stretch=3)

        groupbox = QGroupBox(self.name)
        groupbox.setLayout(group_box_layout)
        layout = QVBoxLayout()
        layout.addWidget(groupbox)
        self.setLayout(layout)

    def resizeEvent(self, event: QResizeEvent):
        self.update_figure()

    def update_figure(self):
        if self.figure is None:
            return
        else:
            canvas = FigureCanvas(self.figure)
            ax = self.figure.gca()
            canvas.draw()
            pil_image = PIL.Image.frombytes(
                'RGB',
                canvas.get_width_height(),
                canvas.tostring_rgb()
            )
            qimage = ImageQt(pil_image)
            qimage.bits()
            pix = QPixmap.fromImage(qimage)
            pix = pix.scaled(0.95 * self.figure_plane.width(),
                             0.95 * self.figure_plane.height(),
                             Qt.AspectRatioMode.KeepAspectRatio)
            self.figure_plane.setPixmap(pix)

    def set_value(self, value: plt.Figure):
        self.figure = value
        self.update_figure()