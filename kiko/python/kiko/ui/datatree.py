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

from kiko.core.entity.item import BaseItem
from kiko.core.entity.channel import Channel

from .mixed import create_box_layout, ORIENTATION, get_image


class DataTreeModel(QtCore.QAbstractItemModel):

    def __init__(self, root=None, show_channels=True, show_chunks=False,
                 parent=None):
        super(DataTreeModel, self).__init__()

        self._show_channels = show_channels
        self._show_chunks = show_chunks

        self._root = root

        self._item_icon = QtGui.QIcon(get_image("item.png"))
        self._chunk_icon = QtGui.QIcon(get_image("chunk.png"))
        self._channel_icon = QtGui.QIcon(get_image("channel.png"))

    def columnCount(self, index):
        return 2

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation != QtCore.Qt.Horizontal or role != QtCore.Qt.DisplayRole:
            return None

        return "Entity" if section == 0 else "Map To"

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        entity = index.internalPointer()
        column = index.column()

        if column == 0:
            if role == QtCore.Qt.DisplayRole:
                return entity.name
            elif role == QtCore.Qt.DecorationRole:
                if isinstance(entity, BaseItem):
                    return self._item_icon
                elif isinstance(entity, Channel):
                    return self._channel_icon
                else:
                    return self._chunk_icon
        elif column == 1:
            if role == QtCore.Qt.DisplayRole:
                if hasattr(entity, "mapped") and entity.mapped:
                    return entity.mapped

        return None

    def _get_child_entity(self, entity, row):
        if isinstance(entity, BaseItem):
            num_chunks = entity.num_chunks
            num_channels = entity.num_channels
            num_children = entity.num_children

            if row < num_children:
                return entity.child_by_index(row)
            if self._show_channels:
                if row < num_children + num_channels:
                    return entity.channel_by_index(row - num_children)
            if self._show_chunks:
                if row < num_children + num_channels + num_chunks:
                    return entity.chunk_by_index(row - num_children -
                                                 num_channels)
        elif isinstance(entity, Channel):
            if self._show_chunks and row < entity.num_chunks:
                return entity.chunk_by_index(row)

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        parent_entity = None
        if not parent or not parent.isValid():
            parent_entity = self._root
        else:
            parent_entity = parent.internalPointer()

        child_entity = self._get_child_entity(parent_entity, row)
        if child_entity:
            return self.createIndex(row, column, child_entity)

        return QtCore.QModelIndex()

    def _get_entity_index(self, entity):
        parent = entity.parent
        if isinstance(entity, BaseItem):
            return parent.child_index(entity)
        elif isinstance(entity, Channel):
            return parent.num_children + parent.channel_index(entity)
        else:
            if isinstance(entity, BaseItem):
                offset = parent.num_children + parent.num_channels
            else:
                offset = 0

            return offset + parent.chunk_index(entity)

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        entity = index.internalPointer()
        if not entity:
            return QtCore.QModelIndex()
        parent = entity.parent

        if parent == self._root:
            return QtCore.QModelIndex()

        return self.createIndex(self._get_entity_index(entity), 0, parent)

    def _get_num_children(self, entity):
        count = 0
        if isinstance(entity, BaseItem):
            count = entity.num_children
            if self._show_channels:
                count += entity.num_channels
            if self._show_chunks:
                count += entity.num_chunks
        elif isinstance(entity, Channel):
            return entity.num_chunks if self._show_chunks else 0
        return count

    def rowCount(self, index):
        if not index or index.column() > 0:
            return 0

        entity = index.internalPointer() if index.isValid() else self._root
        return self._get_num_children(entity)

    def set_root(self, root):
        self._root = root

    def set_mapping_object(self, index, name):
        index.internalPointer().mapped = name

    def set_mapping_channel(self, index, channel):
        index.internalPointer().mapped = channel

    def _populate_mapping(self, mapping, item):
        for child in item.iter_children():
            if child.mapped:
                mapping[child.name] = child.mapped
            self._populate_mapping(mapping, child)

        for channel in item.iter_channels():
            if channel.mapped:
                mapping[item.name + "." + channel.name] = channel.mapped

    def get_mapping(self):
        mapping = {}
        self._populate_mapping(mapping, self._root)
        return mapping


class DataTreeSortProxyFilterModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super(DataTreeSortProxyFilterModel, self).__init__()

    def filterAcceptsRow(self, source_row, source_parent):
        if super(DataTreeSortProxyFilterModel, self).filterAcceptsRow(
                                                    source_row, source_parent):
            return True

        return self.hasAcceptedChildren(source_row, source_parent)

    def hasAcceptedChildren(self, source_row, source_parent):
        item = self.sourceModel().index(source_row, 0, source_parent)
        if not item.isValid():
            return False

        child_count = self.sourceModel().rowCount(item)
        if child_count == 0:
            return False

        for i in range(child_count):
            if super(DataTreeSortProxyFilterModel, self).filterAcceptsRow(i,
                                                                          item):
                return True
            if self.hasAcceptedChildren(i, item):
                return True

        return False


class DataTreeWidget(QtWidgets.QTreeView):
    def __init__(self, root=None, show_channels=True, show_chunks=False,
                 parent=None, facade=None):
        super(DataTreeWidget, self).__init__(parent)

        self._show_channels = show_channels
        self._show_chunks = show_chunks

        self._facade = facade

        self._model = DataTreeModel(root=root, show_channels=show_channels,
                                    show_chunks=show_chunks)
        self._sorting_model = DataTreeSortProxyFilterModel()
        self._sorting_model.setSourceModel(self._model)
        self._sorting_model.setDynamicSortFilter(False)
        self.setModel(self._sorting_model)

        self.header().setSectionsClickable(False)

        self.setColumnWidth(0, 250)

        if self._facade:
            self._menu = QtWidgets.QMenu(self)
            self._sel_item_a = self._menu.addAction("Map To Selected Item")
            self._sel_chan_a = self._menu.addAction("Map To Selected Channel")
            self._unmap_a = self._menu.addAction("Remove Mapping")
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self._show_menu)
            self._menu.triggered.connect(self._action_triggered)

        if root is not None:
            self.set_root(root)

    def set_root(self, root):
        self._model.beginResetModel()
        self._model.set_root(root)
        self._model.endResetModel()

    def set_filter(self, filter):
        self._sorting_model.setFilterFixedString(filter)

    def _action_triggered(self, action):
        selection = self.selectedIndexes()
        if not selection:
            return

        index = self._sorting_model.mapToSource(selection[0])

        if action.text() == "Map To Selected Item":
            f_sel = self._facade.get_selection()
            if f_sel:
                self._model.set_mapping_object(index,
                                               self._facade.get_name(f_sel[0]))
                #self.update()
            else:
                QtWidgets.QMessageBox.critical(self, "Error",
                                               "No item is selected")
        elif action.text() == "Map To Selected Channel":
            f_chan = self._facade.get_selected_channel_names()
            if f_chan:
                name = self._facade.get_name(self._facade.get_selection()[0])
                self._model.set_mapping_channel(index, name + "." + f_chan[0])
                #self.update()
            else:
                QtWidgets.QMessageBox.critical(self, "Error",
                                               "No channel is selected")
        else:
            self._model.set_mapping_object(index, None)

    def _show_menu(self, point):
        selection = self.selectedIndexes()
        if not selection:
            return

        index = self._sorting_model.mapToSource(selection[0])
        entity = index.internalPointer()

        is_item = isinstance(entity, BaseItem)
        is_channel = not is_item and isinstance(entity, Channel)

        self._sel_item_a.setEnabled(is_item)
        self._sel_chan_a.setEnabled(is_channel)
        self._unmap_a.setEnabled(entity.mapped is not None)

        point.setY(point.y() + self.header().height())
        self._menu.popup(self.mapToGlobal(point))

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.clearSelection()

        super(DataTreeWidget, self).mouseReleaseEvent(event)

    def get_mapping(self):
        return self._model.get_mapping()


class DataTreeAndSearchWidget(QtWidgets.QWidget):
    def __init__(self, root=None, show_channels=True, show_chunks=False,
                 parent=None, facade=None):
        super(DataTreeAndSearchWidget, self).__init__(parent)

        self._layout = create_box_layout(ORIENTATION.VERTICAL, margin=0)
        self.setLayout(self._layout)

        self._buid_widgets(root, show_channels, show_chunks, facade)
        self._connect_signals()

    def _buid_widgets(self, root, show_channels, show_chunks, facade):
        h_layout = create_box_layout(ORIENTATION.HORIZONTAL, margin=0,
                                     spacing=10)
        self._layout.addLayout(h_layout)

        self._search_field = QtWidgets.QLineEdit(self)
        h_layout.addWidget(self._search_field)

        self._search_button = QtWidgets.QPushButton(self)
        self._search_button.setIcon(QtGui.QIcon(get_image("search.png")))
        h_layout.addWidget(self._search_button)

        self._data_tree = DataTreeWidget(root=root, show_channels=show_channels,
                                         show_chunks=show_chunks, parent=self,
                                         facade=facade)
        self._layout.addWidget(self._data_tree)

    def _connect_signals(self):
        self._search_button.clicked.connect(self._search)
        self._search_field.returnPressed.connect(self._search)

    def _search(self):
        self._data_tree.set_filter(self._search_field.text())

    def set_root(self, root):
        self._data_tree.set_root(root)

    def get_mapping(self):
        return self._data_tree.get_mapping()

