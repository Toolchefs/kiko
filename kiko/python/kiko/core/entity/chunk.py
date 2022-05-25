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

from abc import ABCMeta, abstractmethod

from kiko.exceptions import (InvalidParentChunkExpception, InvalidOperation,
                             InvalidOperatorName)

NoneType = type(None)


class Chunk(object):
    __metaclass__ = ABCMeta
    _parent_type = NoneType

    def __init__(self, parent, operator=None, operator_name=None,
                 operator_ver=None):
        if not isinstance(parent, self._parent_type):
            raise InvalidParentChunkExpception('Invalid parent for Chunk')

        if operator is None and (operator_name is None or operator_ver is None):
            raise InvalidOperation("You have to provide an operator or an "
                                   "operator name and version")

        self._operator = operator
        self._operator_name = (operator_name if operator is None
                               else operator.name())
        self._operator_version = (operator_ver if operator is None
                                  else operator.version())

        self._parent = None
        self.parent = parent

        self._operator_data = None

    # this method is just to trick python and make this class abstract
    @abstractmethod
    def is_base(self):
        return True

    @property
    def name(self):
        return self._operator_name

    def get_operator_name(self):
        return self._operator_name

    operator_name = property(get_operator_name)

    def get_operator_version(self):
        return self._operator_version

    operator_version = property(get_operator_version)

    def get_operator_data(self):
        return self._operator_data

    def set_operator_data(self, value):
        self._operator_data = value

    operator_data = property(get_operator_data, set_operator_data)

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        if not isinstance(parent, self._parent_type):
            raise InvalidItemException('Given parent is not of type %s' %
                                       str(self._parent_type))

        parent.add_chunk(self)

    parent = property(get_parent, set_parent)

    def get_operator(self):
        return self._operator

    def set_operator(self, operator):
        self._operator = operator

    operator = property(get_operator, set_operator)


class ItemChunk(Chunk):
    def __init__(self, parent, operator=None, operator_name=None,
                 operator_ver=None):
        super(ItemChunk, self).__init__(parent, operator=operator,
                        operator_name=operator_name, operator_ver=operator_ver)

    def is_base(self):
        return False


class ChannelChunk(Chunk):
    def __init__(self, parent, operator=None, operator_name=None,
                 operator_ver=None):
        super(ChannelChunk, self).__init__(parent, operator=operator,
                        operator_name=operator_name, operator_ver=operator_ver)

    def is_base(self):
        return False


from kiko.core.entity.item import BaseItem
ItemChunk._parent_type = BaseItem

from kiko.core.entity.channel import Channel
ChannelChunk._parent_type = Channel
