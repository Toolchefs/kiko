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

from types import NoneType
from collections import OrderedDict

from kiko.exceptions import InvalidChunkException

class ChunkHandler(object):
    _chunk_type = NoneType

    def __init__(self):
        self._chunks = OrderedDict()

    @property
    def num_chunks(self):
        return len(self._chunks)

    def has_chunk(self, name):
        return name in self._chunks

    def get_chunk_names(self):
        return self._chunks.keys()

    def iter_chunks(self):
        for c in self._chunks.itervalues():
            yield c

    def remove_chunk(self, chunk):
        self.remove_chunk_by_name(chunk.operator_name)

    def remove_chunk_by_name(self, name):
        if name in self._chunks:
            chunk = self._chunks[name]
            chunk._parent = None
            del self._chunks[name]

    def add_chunk(self, chunk):
        if not isinstance(chunk, self._chunk_type):
            raise InvalidChunkException('Given chunk is not of type %s' %
                                        str(self._chunk_type))

        if chunk._parent:
            chunk._parent.remove_chunk_by_name(chunk.operator_name)

        chunk._parent = self
        self._chunks[chunk.operator_name] = chunk

    def chunk(self, name):
        return self._chunks.get(name)

    def clear_chunks(self):
        self._chunks.clear()

    def chunk_by_index(self, index):
        return self._chunks.values()[index]

    def chunk_index(self, chunk):
        return self._chunks.keys().index(chunk.name)
