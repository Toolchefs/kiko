# ==============================================================================
#
# KIKO is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version. This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
# for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
#
# ==============================================================================

import os

from qthandler import QtGui, QtWidgets


class ORIENTATION:
    VERTICAL = 0
    HORIZONTAL = 1


def create_box_layout(orientation, margin=None, spacing=None):

    if orientation == ORIENTATION.VERTICAL:
        layout = QtWidgets.QVBoxLayout()
    elif orientation == ORIENTATION.HORIZONTAL:
        layout = QtWidgets.QHBoxLayout()

    if not spacing is None:
        layout.setSpacing(spacing)
    if not margin is None:
        layout.setContentsMargins(margin, margin, margin, margin)

    return layout


def create_label(text, width=30):
    l = QtWidgets.QLabel(text)
    l.setFixedWidth(width)
    return l

def create_separator(orientation, size=None):
    line = QtWidgets.QFrame()
    line.setFrameShape(QtWidgets.QFrame.VLine
                       if orientation == ORIENTATION.VERTICAL
                       else QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    if size is not None:
        if orientation == ORIENTATION.VERTICAL:
            line.setFixedHeight(size)
        else:
            line.setFixedWidth(size)
    return line


def create_radio_buttons(text, labels, parent, parent_layout, width=120,
                         add_stretch=True):
    rbs = []
    layout = create_box_layout(ORIENTATION.HORIZONTAL, margin=0)

    if text is not None:
        layout.addWidget(create_label(text, width=80))

    button_grp = QtWidgets.QButtonGroup(parent)

    for l in labels:
        rb = QtWidgets.QRadioButton(l)
        rb.setFixedWidth(width)
        rbs.append(rb)
        button_grp.addButton(rb)
        layout.addWidget(rb)

    if add_stretch:
        layout.addStretch(1)

    parent_layout.addLayout(layout)
    return tuple(rbs)


class FrameRange(QtWidgets.QWidget):
    def __init__(self, parent=None, width=80):
        super(FrameRange, self).__init__(parent)
        self._layout = create_box_layout(ORIENTATION.HORIZONTAL, margin=0)
        self.setLayout(self._layout)

        self._build_widgets(width)

    def _build_widgets(self, width):
        self._layout.addWidget(create_label("Frame Range: ", width=width))
        self._start_frame = QtWidgets.QSpinBox()
        self._start_frame.setRange(-10000000, 1000000)
        self._layout.addWidget(self._start_frame)
        self._end_frame = QtWidgets.QSpinBox()
        self._end_frame.setRange(-10000000, 1000000)
        self._layout.addWidget(self._end_frame)

    def get_range(self):
        return self._start_frame.value(), self._end_frame.value()

    def set_range(self, start, end):
        if start:
            self._start_frame.setValue(start)
        if end:
            self._end_frame.setValue(end)

    def setEnabled(self, value):
        self._start_frame.setEnabled(value)
        self._end_frame.setEnabled(value)


def get_image(name):
    return "/".join([os.path.dirname(__file__), "images", name])

