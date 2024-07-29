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

from collections import OrderedDict

from abc import ABCMeta, abstractmethod

from kiko.exceptions import InvalidItemException
from kiko.core.entity.handlers import channelhandler, chunkhandler, maptohandler
from kiko.vendor import six

@six.add_metaclass(ABCMeta)
class BaseItem(channelhandler.ChannelHandler, chunkhandler.ChunkHandler,
               maptohandler.MapToHandler):

    _parent_type = type(None)
    _child_type = type(None)
    _channel_type = type(None)
    _chunk_type = type(None)

    def __init__(self, parent, name):
        channelhandler.ChannelHandler.__init__(self)
        chunkhandler.ChunkHandler.__init__(self)
        maptohandler.MapToHandler.__init__(self)

        self._id = id(self)

        self._name = str(name)
        self._children = OrderedDict()

        self._parent = None
        self.set_parent(parent)

    # this method is just to trick python and make this class abstract
    @abstractmethod
    def is_base(self):
        return True

    @property
    def id(self):
        return self._id

    def clear(self):
        self.clear_children()
        self.clear_chunks()
        self.clear_channels()

    def get_name(self):
        return self._name

    def set_name(self, name):
        if self._parent:
            p = self._parent
            p._children = OrderedDict([(name, v) if k == self._name else (k, v)
                                       for k, v in p._children.items()])
        self._name = str(name)

    name = property(get_name, set_name)

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        if not isinstance(parent, self._parent_type):
            raise InvalidItemException('Given parent is not of type %s' %
                                       str(self._parent_type))

        if parent:
            parent.add_child(self)

    parent = property(get_parent, set_parent)

    ####################################
    # CHILDREN
    ####################################

    @property
    def num_children(self):
        return len(self._children)

    def get_children_names(self):
        return self._children.keys()

    def iter_children(self):
        for c in self._children.values():
            yield c

    def remove_child(self, child):
        self.remove_child_by_name(child.name)

    def remove_child_by_name(self, name):
        if name in self._children:
            child = self._children[name]
            child._parent = None
            del self._children[name]

    def add_child(self, child):
        if not isinstance(child, self._child_type):
            raise InvalidItemException('Given child is not of type of %s' %
                                       str(self._child_type))

        if child._parent:
            child._parent.remove_child_by_name(child.name)

        child._parent = self
        self._children[child.name] = child

    def child(self, name):
        return self._children.get(name)

    def child_by_index(self, index):
        return list(self._children.values())[index]

    def clear_children(self):
        self._children.clear()

    def child_index(self, child):
        return self._children.keys().index(child.name)


class RootItem(BaseItem):
    def __init__(self, fps=None, start_frame=None, end_frame=None):
        super(RootItem, self).__init__(parent=None, name="kikoRoot")

        self._fps = fps
        self._start_frame = start_frame
        self._end_frame = end_frame

    def is_base(self):
        return False

    @property
    def fps(self):
        return self._fps

    @property
    def start_frame(self):
        return self._start_frame

    @property
    def end_frame(self):
        return self._end_frame


class Item(BaseItem):
    def __init__(self, parent, name):
        super(Item, self).__init__(parent, name)

    def is_base(self):
        return False


from kiko.core.entity.chunk import ItemChunk
from kiko.core.entity.channel import Channel
Item._chunk_type = ItemChunk
Item._channel_type = Channel
Item._parent_type = BaseItem
Item._child_type = Item

RootItem._chunk_type = ItemChunk
RootItem._channel_type = Channel
RootItem._parent_type = type(None)
RootItem._child_type = Item

