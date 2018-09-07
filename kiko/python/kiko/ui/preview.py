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

from qthandler import QtGui, QtWidgets, QtCore

from kiko.constants import (KIKO_FILE_EXTENSION, KIKO_PREVIEW_PLAY,
                            KIKO_PREVIEW_FPS)

from kiko.io.kikofile import KikoFile

from .mixed import get_image


class PreviewWidget(QtWidgets.QWidget):
    def __init__(self, kiko_file=None, play_by_default=KIKO_PREVIEW_PLAY,
                 parent=None):
        super(PreviewWidget, self).__init__(parent=parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)

        self._play_by_default = play_by_default
        self._current_image = QtGui.QImage()

        self._scrubbing_line_position = 5
        self._mouse_over = False

        self.file = kiko_file

    @property
    def file(self):
        return self._kiko_file

    @file.setter
    def file(self, kiko_file):
        if isinstance(kiko_file, KikoFile):
            self._static_image_only = kiko_file.num_images == 0
            self._kiko_file = kiko_file
        else:
            self._static_image_only = (kiko_file is None or
                                   not kiko_file.endswith(KIKO_FILE_EXTENSION))

            if not self._static_image_only:
                self._kiko_file = KikoFile(kiko_file)
                self._kiko_file.parse()

        self._static_image = QtGui.QImage()
        if self._static_image_only:
            self._static_image.load(get_image('kiko.jpg'))
        else:
            self._scrubbing_line_position = 5

            if self._kiko_file.num_images > 0:
                self._static_image.loadFromData(self._kiko_file.get_image(0))

                self._timer = QtCore.QTimer(self)
                self._timer.setInterval(1000 / KIKO_PREVIEW_FPS)
                self._timer.timeout.connect(self._next_frame)
            else:
                self._static_image.load(get_image('kiko.jpg'))
                self._static_image_only = True

        self.setMouseTracking(not self._static_image_only)

        self._current_image = self._static_image
        self.setMaximumWidth(self._static_image.width())
        self.setMaximumHeight(self._static_image.height())

        if not self._current_image.isNull():
            self.setMinimumHeight(self.width() / self.aspect_ratio)

        if self._play_by_default:
            self.play()
        else:
            self.repaint()

    def resizeEvent(self, event):
        if not self._current_image.isNull():
            self.setMinimumHeight(self.width() / self.aspect_ratio)

        if self._scrubbing_line_position:
            self._scrubbing_line_position *= (float(event.size().width()) /
                                             float(event.oldSize().width()))

        super(PreviewWidget, self).resizeEvent(event)

    def play(self):
        if not self._static_image_only and not self._timer.isActive():
            self._timer.start()

    def pause(self):
        if not self._static_image_only and self._timer.isActive():
            self._timer.stop()

    def _next_frame(self):
        self._frame_number += 1
        if self._frame_number > self._kiko_file.num_images - 1:
            self._frame_number = 0
        self._current_image.loadFromData(self._kiko_file.get_image(
                                                            self._frame_number))
        self.repaint()

    @property
    def aspect_ratio(self):
        if self._current_image.isNull():
            return None

        w = float(self._current_image.width())
        h = float(self._current_image.height())
        return w / h

    def mouseMoveEvent(self, event):
        if not self._static_image_only and not self._play_by_default:
            w = self.width()

            ratio = float(event.pos().x()) / float(w)
            ratio = max(0, min(ratio, 1))

            frame_number = int(round((self._kiko_file.num_images - 1) * ratio))

            self._current_image.loadFromData(self._kiko_file.get_image(
                                                                frame_number))


            self._scrubbing_line_position = max(5, min(event.pos().x(), w - 5))
            self.repaint()

        super(PreviewWidget, self).mouseMoveEvent(event)

    def enterEvent(self, event):
        self._mouse_over = True
        super(PreviewWidget, self).enterEvent(event)

    def leaveEvent(self, event):
        self._mouse_over = False
        self.repaint()

        super(PreviewWidget, self).leaveEvent(event)

    def hideEvent(self, event):
        if self._play_by_default:
            self.pause()
        super(PreviewWidget, self).hideEvent(event)

    def showEvent(self, event):
        if self._play_by_default:
            self.play()
        super(PreviewWidget, self).showEvent(event)

    def paintEvent(self, event):
        if not self._current_image.isNull():
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            w = min(self._current_image.width(), self.width())
            h = w / self.aspect_ratio

            #image
            pen = QtGui.QPen()
            pen.setColor(QtGui.QColor(0, 0, 0, 0))
            pen.setJoinStyle(QtCore.Qt.RoundJoin)
            brush = QtGui.QBrush(self._current_image.scaledToWidth(w,
                                                QtCore.Qt.SmoothTransformation))
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.drawRoundedRect(0, 0, w, h, 10, 10)

            #border
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(0, 0, w, h), 10, 10)
            pen = QtGui.QPen(QtCore.Qt.black, 3)
            painter.setPen(pen)
            painter.drawPath(path)

            if not self._play_by_default and self._scrubbing_line_position:
                x = self._scrubbing_line_position

                sh = h - 8
                sy = 4
                if not self._mouse_over:
                    sh = 4
                    sy = h - 8

                path = QtGui.QPainterPath()
                path.addRoundedRect(QtCore.QRectF(x - 2, sy, 4, sh), 5, 5)
                pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 123), 3)
                painter.setPen(pen)
                painter.drawPath(path)

        super(PreviewWidget, self).paintEvent(event)
