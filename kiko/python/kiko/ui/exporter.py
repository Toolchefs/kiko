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

from qthandler import QtWidgets, QtGui, QtCore

from kiko.constants import KIKO_FILE_EXTENSION, KB_FILE_EXTENSION
from kiko.operators.factory import OperatorsFactory
from kiko.exceptions import InvalidOperation
from kiko.io.kikofile import KikoFile

from .mixed import (create_box_layout, create_label, ORIENTATION, FrameRange,
                    create_separator, create_radio_buttons)


class KikoExporterDialog(QtWidgets.QDialog):
    def __init__(self, manager, app_preference_widget=None):
        super(KikoExporterDialog, self).__init__()

        self._manager = manager
        facade = self._manager.facade
        self._image_generation = facade.supports_image_generation()

        app_name = facade.get_app_name().capitalize()
        self.setWindowTitle(app_name + ' Kiko Exporter')
        self._layout = create_box_layout(ORIENTATION.VERTICAL)
        self.setLayout(self._layout)

        self._app_preference_widget = app_preference_widget
        if app_preference_widget:
            tab_widget = QtWidgets.QTabWidget(self)
            self._layout.addWidget(tab_widget)
            self._layout.setContentsMargins(0, 0, 0, 0)

            widget = QtWidgets.QWidget(self)
            self._layout = create_box_layout(ORIENTATION.VERTICAL)
            widget.setLayout(self._layout)
            tab_widget.addTab(widget, "Export")

            tab_widget.addTab(app_preference_widget, app_name + " Preferences")

        self.resize(500, 400)

        self._build_widgets()
        self._initialize_widgets()
        self._connect_signals()

    def _build_file(self):
        h_layout = create_box_layout(ORIENTATION.HORIZONTAL, margin=2)
        h_layout.addWidget(create_label("File: "))
        self._file_path = QtWidgets.QLineEdit()
        h_layout.addWidget(self._file_path)
        self._search_file_button = QtWidgets.QPushButton("Search")
        h_layout.addWidget(self._search_file_button)
        self._layout.addLayout(h_layout)

        self._options_group = QtWidgets.QGroupBox("Options")
        v_layout = create_box_layout(ORIENTATION.VERTICAL, margin=2)
        self._options_group.setLayout(v_layout)

        self._data_export, self._tar_export = create_radio_buttons("Data: ",
                    ['Data Only', "Data And Images"], self, v_layout)

        self._selection, self._hierarchy = create_radio_buttons("Hierarchy: ",
                    ["Selection", "Below"], self, v_layout)
        self._hierarchy.setEnabled(self._manager.facade.support_hierarchy())

        self._all_frames, self._gui_range, self._start_end = \
                    create_radio_buttons("Frames:", ["All", "GUI Frame Range",
                                         "Start/End"], self, v_layout)

        self._frame_range = FrameRange(self)
        v_layout.addWidget(self._frame_range)

        self._layout.addWidget(self._options_group)

    def _build_image(self):
        self._images_group = QtWidgets.QGroupBox("Images")
        v_layout = create_box_layout(ORIENTATION.VERTICAL, margin=2)
        self._images_group.setLayout(v_layout)

        h_layout = create_box_layout(ORIENTATION.HORIZONTAL, margin=2)
        h_layout.addWidget(create_label("Source: ", width=80))
        self._image_source = QtWidgets.QComboBox()
        h_layout.addWidget(self._image_source)

        v_layout.addLayout(h_layout)

        h_layout = create_box_layout(ORIENTATION.HORIZONTAL, margin=2)
        self._image_frame_range = FrameRange(self)
        h_layout.addWidget(self._image_frame_range)
        h_layout.addWidget(create_separator(ORIENTATION.VERTICAL))
        h_layout.addWidget(create_label("Sample every (frames): ", width=120))
        self._image_sampling = QtWidgets.QLineEdit()
        self._image_sampling.setValidator(QtGui.QDoubleValidator())
        h_layout.addWidget(self._image_sampling)

        v_layout.addLayout(h_layout)

        self._layout.addWidget(self._images_group)

    def _build_operators(self):
        self._operators_group = QtWidgets.QGroupBox("Operators")
        h_layout = create_box_layout(ORIENTATION.HORIZONTAL, margin=2)
        self._operators_group.setLayout(h_layout)

        self._operator_list = QtWidgets.QListWidget()
        self._operator_list.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        h_layout.addWidget(self._operator_list)

        self._force_all = QtWidgets.QCheckBox("Force Evaluation")
        h_layout.addWidget(self._force_all, 0, QtCore.Qt.AlignTop)

        self._layout.addWidget(self._operators_group)

    def _build_buttons(self):
        self._export_button = QtWidgets.QPushButton("Export")
        self._export_button.setFixedHeight(25)
        self._layout.addWidget(self._export_button)

    def _build_widgets(self):
        self._build_file()
        if self._image_generation:
            self._build_image()
        self._build_operators()
        self._build_buttons()

    def _initialize_widgets(self):
        self._data_export.setChecked(True)
        self._selection.setChecked(True)
        self._all_frames.setChecked(True)
        self._frame_range.setVisible(False)

        facade = self._manager.facade
        f_range = facade.get_active_frame_range()
        self._frame_range.set_range(*f_range)

        if self._image_generation:
            self._images_group.setVisible(self._tar_export.isChecked())
            self._image_source.addItems(facade.get_image_sources())
            self._image_sampling.setText('3')
            self._image_frame_range.set_range(*f_range)

        operator_names = OperatorsFactory().get_all_operator_names(
                                                        facade.get_app_name())
        self._operator_list.addItems(operator_names)

        self.enable_groups(False)

    def enable_groups(self, value):
        self._options_group.setEnabled(value)
        self._operators_group.setEnabled(value)
        self._export_button.setEnabled(value)
        if self._app_preference_widget:
            self._app_preference_widget.setEnabled(value)

    def _connect_signals(self):
        self._search_file_button.clicked.connect(self._search_file)

        self._file_path.returnPressed.connect(self._editing_finished)
        self._file_path.editingFinished.connect(self._editing_finished)
        self._tar_export.toggled.connect(self._images_group.setVisible)
        self._tar_export.toggled.connect(self._change_file_ext)
        self._start_end.toggled.connect(self._frame_range.setVisible)

        self._export_button.clicked.connect(self._export_button_clicked)

    def _change_file_ext(self):
        path = self._file_path.text()
        if not path:
            return

        ext = (KIKO_FILE_EXTENSION if self._tar_export.isChecked() else
               KB_FILE_EXTENSION)

        p, _ = os.path.splitext(path)

        self._file_path.blockSignals(True)
        self._file_path.setText(p + ext)
        self._file_path.blockSignals(False)

    def _editing_finished(self):
        path = self._file_path.text()
        if not path:
            self.enable_groups(False)
            return

        p, ext = os.path.splitext(path)
        if ext == KIKO_FILE_EXTENSION:
            self._tar_export.setChecked(True)
        elif ext == KB_FILE_EXTENSION:
            self._data_export.setChecked(True)
        else:
            if self._data_export.isChecked():
                path = p + KIKO_FILE_EXTENSION
            else:
                path = p + KB_FILE_EXTENSION

            self._file_path.blockSignals(True)
            self._file_path.setText(path)
            self._file_path.blockSignals(False)

        self.enable_groups(True)

    def _search_file(self):
        path, filter = QtWidgets.QFileDialog.getSaveFileName(self,
                                              "Select a kiko file",
                                              filter="Kiko Files (*.kiko *.kb)")
        if path:
            self._file_path.setText(path)
            self._editing_finished()

    def _sanitise_file_name(self, f_name):
        ext = (KIKO_FILE_EXTENSION if self._tar_export.isChecked() else
               KB_FILE_EXTENSION)

        p, _ = os.path.splitext(f_name)
        return p + ext

    def _get_start_end_frame(self):
        if self._all_frames.isChecked():
            return None, None

        if self._gui_range.isChecked():
            return self._manager.facade.get_active_frame_range()

        if self._start_end.isChecked():
            return self._frame_range.get_range()

    def _get_selected_operators(self):
        sel = self._operator_list.selectedItems()
        if not sel:
            return None
        return [s.text() for s in sel]

    def _export_button_clicked(self):
        path = self._file_path.text()
        if not os.path.exists(os.path.dirname(path)):
            QtWidgets.QMessageBox.critical(self, "Error", "Invalid file path.")
            return

        facade = self._manager.facade
        if not facade.get_selection():
            QtWidgets.QMessageBox.critical(self, "Error", "Please selected "
                                           "something and retry.")
            return

        f_name = self._sanitise_file_name(path)

        start_frame, end_frame = self._get_start_end_frame()
        selected_operators = self._get_selected_operators()

        self._manager.export_to_file(f_name, operators=selected_operators,
                                keep_previous_images=False,
                                hierarchy=self._hierarchy.isChecked(),
                                start_frame=start_frame, end_frame=end_frame,
                                force_op_evaluation=self._force_all.isChecked())

        if self._data_export.isChecked():
            QtWidgets.QMessageBox.information(self, "Success!", "KB file "
                                                                "exported "
                                                                "successfully!")
            return

        sample = int(self._image_sampling.text())
        start, end = self._image_frame_range.get_range()
        images = facade.generate_image_sequence(
                        self._image_source.currentText(), start, end, sample)
        if not images:
            raise InvalidOperation("Could not generate images")

        if self._app_preference_widget:
            self._app_preference_widget.set_preferences()

        k_file = KikoFile(f_name)
        k_file.parse()
        start, end = self._image_frame_range.get_range()
        k_file.set_images(images)

        k_file.save()

        QtWidgets.QMessageBox.information(self, "Success!", "KIKO file exported "
                                          "successfully!")

    def keyPressEvent(self, event):
        return