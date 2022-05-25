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

from kiko.exceptions import InvalidItemException, InvalidChunkException
from kiko.core.entity.handlers import chunkhandler, maptohandler

NoneType = type(None)

class Channel(chunkhandler.ChunkHandler, maptohandler.MapToHandler):
    _parent_type = NoneType
    _chunk_type = NoneType

    def __init__(self, parent, name):
        chunkhandler.ChunkHandler.__init__(self)
        maptohandler.MapToHandler.__init__(self)

        self._name = str(name)

        self._parent = None
        self.parent = parent

    def get_name(self):
        return self._name

    def set_name(self, name):
        p = self._parent
        p._channel = OrderedDict([(name, v) if k == self._name else (k, v)
                                       for k, v in p._channel.items()])
        self._name = str(name)

    name = property(get_name, set_name)

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        if not isinstance(parent, self._parent_type):
            raise InvalidItemException('Given parent is not of type %s' %
                                       str(self._parent_type))

        parent.add_channel(self)

    parent = property(get_parent, set_parent)



from kiko.core.entity.item import Item
from kiko.core.entity.chunk import ChannelChunk
Channel._parent_type = Item
Channel._chunk_type = ChannelChunk
