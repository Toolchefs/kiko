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

from kiko.exceptions import InvalidChannelException

class MapToHandler(object):

    def __init__(self):
        self._mapped_name = None

    @property
    def mapped(self):
        return self._mapped_name

    @mapped.setter
    def mapped(self, value):
        self._mapped_name = value
