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
import sys
import traceback

from qthandler import QtGui, QtCore, QtWidgets

from kiko.constants import (KIKO_FILE_EXTENSION, KB_FILE_EXTENSION,
                            IMPORT_METHODS)
from kiko.operators.factory import OperatorsFactory
from kiko.io.kikofile import KikoFile
from kiko.io import deserializers

from .mixed import (create_box_layout, create_label, ORIENTATION, FrameRange,
                    create_separator, create_radio_buttons)
from datatree import DataTreeAndSearchWidget

from preview import PreviewWidget


class KikoImporterDialog(QtWidgets.QDialog):
    def __init__(self, manager, app_preference_widget=None):
        super(KikoImporterDialog, self).__init__()

        self._manager = manager
        facade = self._manager.facade

        self._kiko_file_path = None

        app_name = facade.get_app_name().capitalize()
        self.setWindowTitle(app_name + ' Kiko Importer')
        self._layout = create_box_layout(ORIENTATION.VERTICAL)
        self.setLayout(self._layout)

        self._app_preference_widget = app_preference_widget

        self.resize(730, 400)

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

    def _build_tab_import(self):
        widget = QtWidgets.QWidget()
        v_layout = create_box_layout(ORIENTATION.VERTICAL, margin=5,
                                     spacing=10)
        widget.setLayout(v_layout)
        self._tab_widget.addTab(widget, "Import")

        v_layout.addSpacing(10)

        self._apply, self._insert, self._replace = create_radio_buttons(
                None, ['Apply', 'Insert', 'Replace'], self, v_layout,
                width=60, add_stretch=False)

        v_layout.addWidget(create_separator(ORIENTATION.HORIZONTAL))

        h_layout1 = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                      spacing=0)
        h_layout1.addSpacing(18)
        h_layout1.addWidget(create_label("Frame value: ", width=116))
        self._frame_value = QtWidgets.QSpinBox(self)
        h_layout1.addWidget(self._frame_value)
        v_layout.addLayout(h_layout1)

        h_layout2 = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                      spacing=5)
        self._enable_frame_range = QtWidgets.QCheckBox("")
        self._enable_frame_range.setFixedWidth(13)
        h_layout2.addWidget(self._enable_frame_range)
        self._frame_range = FrameRange(self, width=111)
        h_layout2.addWidget(self._frame_range)
        v_layout.addLayout(h_layout2)

        self._hierarchy = QtWidgets.QCheckBox("Hierarchy")
        self._hierarchy.setVisible(self._manager.facade.support_hierarchy())
        v_layout.addWidget(self._hierarchy)

        v_layout.addWidget(create_separator(ORIENTATION.HORIZONTAL))

        h_layout3 = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                      spacing=5)
        self._enable_channel_op_priority = QtWidgets.QCheckBox("Channel Op "
                                                               "Priority")
        self._enable_channel_op_priority.setFixedWidth(130)
        h_layout3.addWidget(self._enable_channel_op_priority)
        self._channel_op_priority = QtWidgets.QListWidget(self)
        self._channel_op_priority.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove)
        h_layout3.addWidget(self._channel_op_priority)

        v_layout.addLayout(h_layout3)

        h_layout4 = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                      spacing=5)
        self._enable_item_op_priority = QtWidgets.QCheckBox("Item Op Priority")
        self._enable_item_op_priority.setFixedWidth(130)
        h_layout4.addWidget(self._enable_item_op_priority)
        self._item_op_priority = QtWidgets.QListWidget(self)
        self._item_op_priority.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove)
        h_layout4.addWidget(self._item_op_priority)

        v_layout.addLayout(h_layout4)

        self._scale_fps = QtWidgets.QCheckBox("Scale FPS")
        v_layout.addWidget(self._scale_fps)
        self._ignore_item_chunks = QtWidgets.QCheckBox("Ignore Item Chunks")
        v_layout.addWidget(self._ignore_item_chunks)

        v_layout.addStretch(1)

    def _build_string(self):
        widget = QtWidgets.QWidget()
        v_layout = create_box_layout(ORIENTATION.VERTICAL, margin=5,
                                     spacing=10)
        widget.setLayout(v_layout)
        self._tab_widget.addTab(widget, "Names")

        h_layout1 = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                      spacing=0)
        h_layout1.addWidget(create_label("String Replacement: ", width=115))
        self._str_repl_table = QtWidgets.QTableWidget(self)
        self._str_repl_table.setRowCount(1)
        self._str_repl_table.setColumnCount(2)
        self._str_repl_table.setHorizontalHeaderLabels(["From", "To"])
        self._str_repl_table.setColumnWidth(0, 125)
        self._str_repl_table.horizontalHeader().setStretchLastSection(True)
        self._str_repl_table.horizontalHeader().setSectionsClickable(False)
        self._str_repl_table.verticalHeader().setVisible(False)
        self._str_repl_table.setAlternatingRowColors(True)
        self._str_repl_table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self._str_repl_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        h_layout1.addWidget(self._str_repl_table)
        v_layout.addLayout(h_layout1)

        self._str_repl_menu = QtWidgets.QMenu(self)
        self._str_repl_add_row = self._str_repl_menu.addAction("Add Row")
        self._str_repl_del_row = self._str_repl_menu.addAction("Delete Row")
        self._str_repl_del_all = self._str_repl_menu.addAction("Delete All")

        h_layout2 = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                      spacing=0)
        h_layout2.addWidget(create_label("Prefix To Add: ", width=115))
        self._prefix = QtWidgets.QLineEdit()
        h_layout2.addWidget(self._prefix)
        v_layout.addLayout(h_layout2)

        h_layout3 = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                      spacing=0)
        h_layout3.addWidget(create_label("Suffix To Add: ", width=115))
        self._suffix = QtWidgets.QLineEdit()
        h_layout3.addWidget(self._suffix)
        v_layout.addLayout(h_layout3)

    def _build_preview_and_buttons(self):
        v_layout = create_box_layout(ORIENTATION.VERTICAL, margin=0,
                                      spacing=5)

        v_layout.addSpacing(20)

        self._preview = PreviewWidget(parent=self)
        v_layout.addWidget(self._preview, 0, QtCore.Qt.AlignTop)

        self._import_button = QtWidgets.QPushButton("Import")
        self._import_button.setFixedHeight(75)
        v_layout.addWidget(self._import_button, 1, QtCore.Qt.AlignBottom)

        self._secondary_layout.addLayout(v_layout)

    def _build_mapping(self):
        widget = QtWidgets.QWidget()
        v_layout = create_box_layout(ORIENTATION.VERTICAL, margin=5,
                                     spacing=10)
        widget.setLayout(v_layout)
        self._tab_widget.addTab(widget, "Mapping")

        v_layout.addWidget(QtWidgets.QLabel('Channel and Item mapping takes '
                                            'precedence over name management.'))

        v_layout.addWidget(create_separator(ORIENTATION.HORIZONTAL))

        self._mapping = DataTreeAndSearchWidget(parent=self,
                                                facade=self._manager.facade)

        v_layout.addWidget(self._mapping)

    def _build_app_preference_widget(self):
        if self._app_preference_widget:
            self._tab_widget.addTab(self._app_preference_widget, "Preferences")

    def _build_widgets(self):
        self._build_file()

        self._secondary_layout = create_box_layout(ORIENTATION.HORIZONTAL,
                                                   margin=0, spacing=8)
        self._layout.addLayout(self._secondary_layout)
        self._tab_widget = QtWidgets.QTabWidget(self)
        self._secondary_layout.addWidget(self._tab_widget)

        self._build_tab_import()
        self._build_string()
        self._build_preview_and_buttons()
        self._build_mapping()
        self._build_app_preference_widget()

    def _initialize_widgets(self):
        self._import_button.setEnabled(False)
        self._tab_widget.setEnabled(False)

        #disabling controls
        self._frame_range.setEnabled(False)
        self._channel_op_priority.setEnabled(False)
        self._item_op_priority.setEnabled(False)

        #turning on apply mode
        self._apply.setChecked(True)

        #ignoring item chunks by default
        self._ignore_item_chunks.setChecked(True)

        #frame value
        self._frame_value.setValue(0)

        #priority lists
        facade = self._manager.facade
        chan_operator_names = OperatorsFactory().get_channel_operator_names(
                                                        facade.get_app_name())
        self._channel_op_priority.addItems(chan_operator_names)

        item_operator_names = OperatorsFactory().get_item_operator_names(
                                                        facade.get_app_name())
        self._item_op_priority.addItems(item_operator_names)

    def _editing_finished(self):
        path = self._file_path.text()
        if (not os.path.exists(path) or
                not path.endswith((KIKO_FILE_EXTENSION, KB_FILE_EXTENSION))):
            self._disable_all()
            self._kiko_file_path = None
            return

        self._load_kiko_file(path)

    def _disable_all(self):
        self._import_button.setEnabled(False)
        self._tab_widget.setEnabled(False)
        self._preview.file = None

    def _connect_signals(self):
        self._str_repl_table.customContextMenuRequested.connect(
                                                    self._show_str_context_menu)
        self._str_repl_menu.triggered.connect(self._str_repl_action_triggered)

        self._hierarchy.toggled.connect(self._hierachy_toggled)

        self._search_file_button.clicked.connect(self._search_file)
        self._file_path.returnPressed.connect(self._editing_finished)

        self._enable_frame_range.toggled.connect(self._frame_range.setEnabled)
        self._enable_channel_op_priority.toggled.connect(
                                        self._channel_op_priority.setEnabled)
        self._enable_item_op_priority.toggled.connect(
                                        self._item_op_priority.setEnabled)

        self._import_button.clicked.connect(self._import_button_clicked)

    def _search_file(self):
        path, filter = QtWidgets.QFileDialog.getOpenFileName(self,
                                              "Select a kiko file",
                                              filter="Kiko Files (*.kiko *.kb)")
        if path:
            self._file_path.setText(path)
            self._load_kiko_file(path)

    def _load_kiko_file(self, path):
        if path != self._kiko_file_path:
            self._kiko_file_path = path

            k_file = KikoFile(self._kiko_file_path)
            k_file.parse()

            d = deserializers.DeserializerManager.get_deserializer(
                                        k_file.version, self._manager.facade)
            root = d.get_root_from_data(k_file.data)

            self._import_button.setEnabled(True)
            self._tab_widget.setEnabled(True)

            self._preview.file = k_file

            self._frame_range.set_range(root.start_frame, root.end_frame)
            self._mapping.set_root(root)

    def _show_str_context_menu(self, point):
        selection = self._str_repl_table.selectedIndexes()
        valid_sel = bool(selection)

        self._str_repl_del_row.setEnabled(valid_sel)
        if valid_sel:
            self._str_repl_del_row.setProperty("row", selection[0].row())

        point.setY(point.y() + self._str_repl_table.horizontalHeader().height())
        self._str_repl_menu.popup(self._str_repl_table.mapToGlobal(point))

    def _str_repl_action_triggered(self, action):
        if action.text() == "Add Row":
            self._str_repl_table.setRowCount(self._str_repl_table.rowCount() +
                                             1)
        elif action.text() == "Delete Row":
            self._str_repl_table.removeRow(self._str_repl_del_row.property(
                                                                        'row'))
        elif action.text() == "Delete All":
            self._str_repl_table.clearContents()
            self._str_repl_table.setRowCount(1)

    def _hierachy_toggled(self, value):
        self._mapping.setEnabled(not value)
        tooltip = ""
        if value:
            tooltip = "Mapping is disabled when hierarchy mode is activated."
        self._mapping.setToolTip(tooltip)

    def _get_op_priority_list(self, cb, list_widget):
        if not cb.isChecked():
            return None
        return [list_widget.item(i).text() for i in range(list_widget.count())]

    def _get_import_obj_method(self):
        if self._hierarchy.isChecked():
            return IMPORT_METHODS.OBJECT.HIERARCHY
        return IMPORT_METHODS.OBJECT.NAME

    def _get_import_anim_method(self):
        if self._apply.isChecked():
            return IMPORT_METHODS.ANIMATION.APPLY
        if self._insert.isChecked():
            return IMPORT_METHODS.ANIMATION.INSERT
        return IMPORT_METHODS.ANIMATION.REPLACE

    def _get_string_replacements(self):
        str_repl_dict = {}
        for row in range(self._str_repl_table.rowCount()):
            from_ = self._str_repl_table.item(row, 0)
            if from_ is None or from_.text() in str_repl_dict:
                continue
            to = self._str_repl_table.item(row, 1)
            str_repl_dict[from_.text()] = to.text() if to else ""
        return str_repl_dict or None

    def _import_button_clicked(self):
        if self._app_preference_widget:
            self._app_preference_widget.set_preferences()

        frame_range = (self._frame_range.get_range()
                    if self._enable_frame_range.isChecked() else (None, None))
        chan_op_list = self._get_op_priority_list(
                                            self._enable_channel_op_priority,
                                            self._channel_op_priority)
        item_op_list = self._get_op_priority_list(
                                            self._enable_item_op_priority,
                                            self._item_op_priority)

        import_obj_method = self._get_import_obj_method()
        import_anim_method = self._get_import_anim_method()

        scale_fps = self._scale_fps.isChecked()
        ignore_item_chunks = self._ignore_item_chunks.isChecked()

        str_repls = self._get_string_replacements()
        prefix = self._prefix.text() or None
        suffix = self._suffix.text() or None
        mapping = self._mapping.get_mapping() or None

        try:
            self._manager.import_from_file(self._kiko_file_path,
                                       item_op_priority=item_op_list,
                                       channel_op_priority=chan_op_list,
                                       import_obj_method=import_obj_method,
                                       import_anim_method=import_anim_method,
                                       str_replacements=str_repls,
                                       obj_mapping=mapping,
                                       prefix_to_add=prefix,
                                       suffix_to_add=suffix,
                                       scale_using_fps=scale_fps,
                                       frame_value=self._frame_value.value(),
                                       ignore_item_chunks=ignore_item_chunks,
                                       start_frame=frame_range[0],
                                       end_frame=frame_range[1])
            QtWidgets.QMessageBox.information(self, "Success!", "KIKO file was "
                                              "successfully imported!")
        except:
            traceback.print_exc(file=sys.stdout)
            QtWidgets.QMessageBox.information(self, "Error!", "Something went "
                                              "wrong while importing the KIKO "
                                              "file. Check the script editor "
                                              "for errros.")

    def keyPressEvent(self, event):
        return
