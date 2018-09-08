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
        """
        :return: the loader version
        """
        raise NotImplementedError()

    @staticmethod
    def load(data, facade, node, import_anim_method, start_frame, end_frame,
             frame_value, channel=None, time_multiplier=1):
        """
        :param data: the data to load
        :param facade: the app facade.
        :param node: The app node
        :param import_anim_method: the import animation method
        :param start_frame: the animation should only be imported from this
                            frame
        :param end_frame: the animation should only be imported until this frame
        :param frame_value: the offset frame value
        :param channel: the channel object, this is None if this is an item
                        operator
        :param time_multiplier: time_multiplier in case this scene has a
                                different frame rate compared to the original
                                scene
        """
        raise NotImplementedError()


class BaseOperator(object):
    # IMPORTANT: need to have these two class static members declared in each
    # operator class
    _loaders = {}
    _max_loader_version = None

    @staticmethod
    def name():
        """
        :return: the operator name
        """
        raise NotImplementedError()

    @staticmethod
    def is_channel_operator():
        """
        :return: True if this is a channel operator, False if this an item
                 operator.
        """
        raise NotImplementedError()

    @staticmethod
    def ignore_following_operators():
        """
        :return: if True subsequent operators will be ignored
        """
        raise NotImplementedError()

    @classmethod
    def version(cls):
        """
        DO NOT OVERRIDE THIS METHOD UNLESS YOU KNOW WHAT YOU ARE DOING

        :return: returns the latest loader version
        """
        return cls._max_loader_version

    @staticmethod
    def validate(facade, node, channel=None, force=False):
        """
        :param facade: the app facade.
        :param node: The app node
        :param channel: the channel object, this is None if this is an item
                        operator
        :param force: if this is True, the users explicitly asked to run all the
                      registered operators and this method should return True

        :return: validates if the operator should be run or not, channel is None
                 if this is an item operator
        """
        return True

    @staticmethod
    def is_app_supported(app_name):
        """
        :param app_name: The app name

        :return: validates if the given DCC name is supported
        """
        return False

    @classmethod
    def register_loader(cls, loader):
        """
        DO NOT OVERRIDE THIS METHOD UNLESS YOU KNOW WHAT YOU ARE DOING

        :param loader: a BaseOperatorLoader class

        Registers a new loader for this operator
        """
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
        """
        DO NOT OVERRIDE THIS METHOD UNLESS YOU KNOW WHAT YOU ARE DOING

        :param facade: the app facade.
        :param node: The app node
        :param loder_version: The loader version
        :param data: The data to be loaded
        :param import_anim_method: the import animation method
        :param start_frame: the start frame for the animation, operators should
                            not return data about animation before this frame
        :param end_frame: the end frame for the animation, operators should
                          not return data about animation after this frame
        :param frame_value: the frame offset value
        :param channel: the channel object, this is None if this is an item
                        operator
        :param time_multiplier: the time multiplier, users should time scale the
                                animation using this value

        :return: the data for this operator
        """

        cls._loaders[loder_version].load(data, facade, node, import_anim_method,
                            start_frame, end_frame, frame_value,
                            channel=channel, time_multiplier=time_multiplier)

    @staticmethod
    def bakeable():
        """
        :return: True if this is a bakeable operator
        """
        return False

    @staticmethod
    def get_frame_range(facade, node, channel=None):
        """
        :param facade: the app facade.
        :param node: The app node
        :param channel: the channel object, this is None if this is an item
                        operator

        :return: the export frame range of this operator
        """
        raise NotImplementedError()

    @staticmethod
    def run(facade, node, channel=None, start_frame=None, end_frame=None):
        """
        :param facade: the app facade.
        :param node: The app node
        :param channel: the channel object, this is None if this is an item
                        operator
        :param start_frame: the start frame for the animation, operators should
                            not return data for animation before this frame
        :param end_frame: the end frame for the animation, operators should
                          not return data for animation after this frame

        :return: the data for this operator
        """
        raise NotImplementedError()

