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


class BaseFacade(object):

    @staticmethod
    def get_app_name():
        """
        :return: the app name for this facade
        """
        raise NotImplementedError()

    @staticmethod
    def get_selection():
        """
        :return: the app selection in a list of internal app objects
        """
        raise NotImplementedError()

    @staticmethod
    def supports_image_generation():
        """
        :return: True is this facade can generate preview images
        """
        raise NotImplementedError()

    @staticmethod
    def get_image_sources():
        """
        :return: the source that could be used for generating preview images
                (i.e. a camera)
        """
        raise NotImplementedError()

    @staticmethod
    def generate_image_sequence(source, start_frame, end_frame, sample_every=1):
        """
        :param source: the source used for generating the images
        :param start_frame: The start frame
        :param end_frame: the end frame
        :param sample_every: sample every frame

        :return: generate an image sequence and returns sorted list of frames
        """
        raise NotImplementedError()

    @staticmethod
    def get_node_by_name(node_name):
        """
        :param node_name: the node name

        :return: returns the internal app object with the given name
        """
        raise NotImplementedError()

    @staticmethod
    def map_kiko_channel_to_app_channel(node_obj, channel_name):
        """
        :param node_obj: the app internal node
        :param channel_name: the kiko channel name

        :return: returns a mapped app channel name
        """
        raise NotImplementedError()

    @staticmethod
    def map_app_channel_to_kiko_channel(node_obj, channel_name):
        """
        :param node_obj: the app internal node
        :param channel_name: the app channel name

        :return: returns a mapped kiko channel name
        """
        raise NotImplementedError()

    @staticmethod
    def get_name(node_obj):
        """
        :param node_obj: the app internal node

        :return: returns the app internal nodeect name
        """
        raise NotImplementedError()

    @staticmethod
    def get_selected_channel_names():
        """
        :return: returns the list of selected channels in the app UI
        """
        raise NotImplementedError()

    @staticmethod
    def list_channels(node_obj):
        """
        :param node_obj: the app internal node

        :return: list all exportable channels for this node
        """
        raise NotImplementedError()

    @staticmethod
    def is_channel_animated(node_obj, channel_obj):
        """
        :param node_obj: the app internal node
        :param channel_obj: the app internal channel

        :return: returns True if this channel is animated
        """
        raise NotImplementedError()

    @staticmethod
    def is_channel_connected(node_obj, channel_obj):
        """
        :param node_obj: the app internal node
        :param channel_obj: the app internal channel

        :return: True if this channel has a connection
        """
        raise NotImplementedError()

    @staticmethod
    def get_children(node_obj):
        """
        :param node_obj: the app internal node

        :return: a list of app internal nodes being children of the given node
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_name(node_obj, channel_obj):
        """
        :param node_obj: the app internal node
        :param channel_obj: the app internal channel

        :return: the channel name
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_value(node_obj, channel_obj):
        """
        :param node_obj: the app internal node
        :param channel_obj: the app internal channel

        :return: the channel static value
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_value(node_obj, channel_obj, value):
        """
        :param node_obj: the app internal node
        :param channel_obj: the app internal channel
        :param value: the value to set on this channel
        """
        raise NotImplementedError()

    @staticmethod
    def support_hierarchy():
        """
        :return: True if this app supports hierarchies
        """
        raise NotImplementedError()

    @staticmethod
    def move_to_frame(frame):
        """
        :param frame: the frame to move to
        """
        raise NotImplementedError()

    @staticmethod
    def get_active_frame_range():
        """
        :return: a tuple representing the app UI frame range
        """
        raise NotImplementedError()

    @staticmethod
    def get_current_time():
        """
        :return: the current time
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_object(node_obj, channel_name):
        """
        :param node_obj: the app internal node
        :param channel_name: the channel name

        :return: the app internal channel
        """
        raise NotImplementedError()

    @staticmethod
    def get_keyframable_channel_object(node_obj, channel_obj,
                                       force_create=True):
        """
        :param node_obj: the app internal node
        :param channel_obj: the app internal channel
        :param force_create: forces the creation of an animation curve object

        :return: the app internal animation curve
        """
        raise NotImplementedError()

    @staticmethod
    def get_frame_range_from_channel(k_channel_obj):
        """
        :param k_channel_obj: the app internal animation curve

        :return: a tuple representing the frame range for this curve
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_key_frame(k_channel_obj, time, value):
        """
        :param k_channel_obj: the app internal animation curve
        :param time: the keyframe time
        :param value: the keyframe value
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_key_frames_in_bulk(k_channel_obj, times, values):
        """
        :param k_channel_obj: the app internal animation curve
        :param time: the keyframe times
        :param value: the keyframe values
        """
        raise NotImplementedError()

    @staticmethod
    def get_fps():
        """
        :return: the app frame rate
        """
        raise NotImplementedError()

    @staticmethod
    def pre_import():
        """
        method called before the import process begins
        """
        raise NotImplementedError()

    @staticmethod
    def post_import():
        """
        method called after the import process ends
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_num_keys(k_channel_obj):
        """
        :param k_channel_obj: the app internal animation curve

        :return: the number of keys frames for this curve
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_is_weighted(k_channel_obj):
        """
        :param k_channel_obj: the app internal animation curve

        :return: True if the channel curve is weighted
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_is_weighted(k_channel_obj, value):
        """
        :param k_channel_obj: the app internal animation curve
        :param value: True to make this channel weighted
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_pre_infinity(k_channel_obj):
        """
        :param k_channel_obj: the app internal animation curve

        :return: channel pre infinity value
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_pre_infinity(k_channel_obj, pre_infinity):
        """
        :param k_channel_obj: the app internal animation curve
        :param pre_infinity: channel pre infinity value
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_post_infinity(k_channel_obj):
        """
        :param k_channel_obj: the app internal animation curve

        :return: channel post infinity value
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_post_infinity(k_channel_obj, post_inifinity):
        """
        :param k_channel_obj: the app internal animation curve
        :param post_inifinity: channel post infinity value
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_in_tangent_type_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: the in tangent type
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_in_tangent_type_at_index(k_channel_obj, index, in_type):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index
        :param in_type: the in tangent type
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_out_tangent_type_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: the out tangent type
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_out_tangent_type_at_index(k_channel_obj, index, out_type):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index
        :param out_type: the out tangent type
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: the angle and weight for the out tangent
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index
        :param angle: the angle value
        :param weight: the weight value
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: the angle and weight for the in tangent
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index
        :param angle: the angle value
        :param weight: the weight value
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_tangents_locked_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: True if the tangents are locked
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_tangents_locked_at_index(k_channel_obj, index, value):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index
        :param value: the tangent lock state
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_weights_locked_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: True if the tangent weights are locked
        """
        raise NotImplementedError()

    @staticmethod
    def set_channel_weights_locked_at_index(k_channel_obj, index, value):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index
        :param value: the weight lock state
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_value_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: the value at the key with the given index
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_time_at_index(k_channel_obj, index):
        """
        :param k_channel_obj: the app internal animation curve
        :param index: the key index

        :return: the time at the key with the given index
        """
        raise NotImplementedError()

    @staticmethod
    def get_channel_value_at_time(k_channel_obj, time):
        """
        :param k_channel_obj: the app internal animation curve
        :param time: time

        :return: the value at the given time
        """
        raise NotImplementedError()

    @staticmethod
    def has_world_space_matrix(node_obj):
        """
        :param node_obj: the app internal node

        :return: True if a world matrix can be extracted from the given node
        """
        raise NotImplementedError()

    @staticmethod
    def get_world_space_rotation_and_translation(node_obj):
        """
        :param node_obj: the app internal node

        :return: the world matrix for the given node at the current time
        """
        raise NotImplementedError()

    @staticmethod
    def set_world_space_rotation_and_translation_at_time(node_obj, time,
                                                         rotation, translation):
        """
        :param node_obj: the app internal node
        :param time: time
        :param rotation: rotation
        :param translation: translation
        """
        raise NotImplementedError()

    @staticmethod
    def remove_animation_from_channel(node_obj, channel_obj):
        """
        :param node_obj: the app internal node
        :param k_channel_obj: the app internal animation curve
        """
        raise NotImplementedError()

    @staticmethod
    def shift_animation_in_frame_range(node_obj, channel_obj, start, end):
        """
        :param node_obj: the app internal node
        :param k_channel_obj: the app internal animation curve
        :param start: start frame
        :param end: end frame
        """
        raise NotImplementedError()

    @staticmethod
    def remove_animation_from_frame_range(node_obj, channel_obj, start, end):
        """
        :param node_obj: the app internal node
        :param k_channel_obj: the app internal animation curve
        :param start: start frame
        :param end: end frame
        """
        raise NotImplementedError()

    @staticmethod
    def pre_import_keyframable_channel_object(k_channel_obj):
        """
        this methods is run before an animation is imported on a channel

        :param k_channel_obj: the app internal animation curve
        """
        pass

    @staticmethod
    def post_import_keyframable_channel_object(k_channel_obj):
        """
        this methods is run after an animation is imported on a channel

        :param k_channel_obj: the app internal animation curve
        """
        pass

    @staticmethod
    def pre_export_keyframable_channel_object(k_channel_obj):
        """
        this methods is run before an animation is exported from a channel

        :param k_channel_obj: the app internal animation curve
        """
        pass

    @staticmethod
    def post_export_keyframable_channel_object(k_channel_obj):
        """
        this methods is run after an animation is exported from a channel

        :param k_channel_obj: the app internal animation curve
        """
        pass

