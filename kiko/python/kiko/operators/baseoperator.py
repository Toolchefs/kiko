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

from kiko.exceptions import InvalidOperatorLoaderException

class BaseOperatorLoader(object):

    @staticmethod
    def version(self):
        raise NotImplementedError()

    @staticmethod
    def load(data, facade, node, import_anim_method, start_frame, end_frame,
             frame_value, channel=None, time_multiplier=1):
        raise NotImplementedError()


class BaseOperator(object):
    _loaders = {}
    _max_loader_version = None

    @staticmethod
    def name():
        raise NotImplementedError()

    @staticmethod
    def is_channel_operator():
        raise NotImplementedError()

    @staticmethod
    def ignore_following_operators():
        raise NotImplementedError()

    @classmethod
    def version(cls):
        return cls._max_loader_version

    @staticmethod
    def validate(facade, node, channel=None, force=False):
        return True

    @staticmethod
    def is_app_supported(app_name):
        return False

    @classmethod
    def register_loader(cls, loader):
        if not issubclass(loader, BaseOperatorLoader):
            raise InvalidOperatorLoaderException("Invalid loader")

        cls._loaders[loader.version()] = loader

        if (cls._max_loader_version is None or
                cls._max_loader_version < loader.version()):
            cls._max_loader_version = loader.version()

    @classmethod
    def deserialize(cls, facade, node, loder_version, data, import_anim_method,
                    start_frame, end_frame, frame_value, channel=None,
                    time_multiplier=1):
        cls._loaders[loder_version].load(data, facade, node, import_anim_method,
                            start_frame, end_frame, frame_value,
                            channel=channel, time_multiplier=time_multiplier)

    @staticmethod
    def bakeable():
        return False

    @staticmethod
    def get_frame_range(facade, node, channel=None):
        raise NotImplementedError()

    @staticmethod
    def run(facade, node, channel=None, start_frame=None, end_frame=None):
        raise NotImplementedError()

