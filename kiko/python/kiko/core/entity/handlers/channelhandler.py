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

class ChannelHandler(object):
    _channel_type = NoneType

    def __init__(self):
        self._channels = OrderedDict()

    @property
    def num_channels(self):
        return len(self._channels)

    def has_channel(self, name):
        return name in self._channels

    def get_channel_names(self):
        return self._channels.keys()

    def iter_channels(self):
        for c in self._channels.itervalues():
            yield c

    def remove_channel(self, channel):
        self.remove_channel_by_name(channel.name)

    def remove_channel_by_name(self, name):
        if name in self._channels:
            channel = self._channels[name]
            channel._parent = None
            del self._channels[name]

    def add_channel(self, channel):
        if not isinstance(channel, self._channel_type):
            raise InvalidChannelException('Given channel is not of type %s'
                                          % str(self._channel_type))

        if channel._parent:
            channel._parent.remove_channel_by_name(channel.name)

        channel._parent = self
        self._channels[channel.name] = channel

    def channel(self, name):
        return self._channels.get(name)

    def clear_channels(self):
        self._channels.clear()

    def channel_by_index(self, index):
        return self._channels.values()[index]

    def channel_index(self, channel):
        return self._channels.keys().index(channel.name)

