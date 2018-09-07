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
        raise NotImplementedError()

    @staticmethod
    def get_selection():
        raise NotImplementedError()

    @staticmethod
    def supports_image_generation():
        raise NotImplementedError()

    @staticmethod
    def get_image_sources():
        raise NotImplementedError()

    @staticmethod
    def generate_image_sequence(source, start_frame, end_frame, sample_every=1):
        raise NotImplementedError()

    @staticmethod
    def get_node_by_name(node_name):
        raise NotImplementedError()

    @staticmethod
    def map_kiko_channel_to_app_channel(app_object, channel_name):
        raise NotImplementedError()

    @staticmethod
    def map_app_channel_to_kiko_channel(app_object, channel_name):
        raise NotImplementedError()

    @staticmethod
    def get_name(node_obj):
        raise NotImplementedError()

    @staticmethod
    def get_selected_channel_names():
        raise NotImplementedError()

    @staticmethod
    def list_channels(node_obj):
        raise NotImplementedError()

    @staticmethod
    def is_channel_animated(node_obj, channel_obj):
        raise NotImplementedError()

    @staticmethod
    def is_channel_connected(node_obj, channel_obj):
        raise NotImplementedError()

    @staticmethod
    def get_children(node_obj):
        raise NotImplementedError()

    @staticmethod
    def get_channel_name(node_obj, channel_obj):
        raise NotImplementedError()

    @staticmethod
    def get_channel_value(node_obj, channel_obj):
        raise NotImplementedError()

    @staticmethod
    def set_channel_value(node_obj, channel_obj, value):
        raise NotImplementedError()

    @staticmethod
    def support_hierarchy():
        raise NotImplementedError()

    @staticmethod
    def move_to_frame(frame):
        raise NotImplementedError()

    @staticmethod
    def get_active_frame_range():
        raise NotImplementedError()

    @staticmethod
    def get_current_time():
        raise NotImplementedError()

    @staticmethod
    def get_channel_object(node_obj, channel_name):
        raise NotImplementedError()

    @staticmethod
    def get_keyframable_channel_object(node_obj, channel_obj,
                                       force_create=True):
        raise NotImplementedError()

    @staticmethod
    def get_frame_range_from_channel(k_channel_obj):
        raise NotImplementedError()

    @staticmethod
    def set_channel_key_frame(k_channel_obj, time, value):
        raise NotImplementedError()

    @staticmethod
    def set_channel_key_frames_in_bulk(k_channel_obj, times, values):
        raise NotImplementedError()

    @staticmethod
    def get_fps():
        raise NotImplementedError()

    @staticmethod
    def pre_import():
        raise NotImplementedError()

    @staticmethod
    def post_import():
        raise NotImplementedError()

    @staticmethod
    def get_channel_num_keys(k_channel_obj):
        raise NotImplementedError()

    @staticmethod
    def get_channel_is_weighted(k_channel_obj):
        raise NotImplementedError()

    @staticmethod
    def set_channel_is_weighted(k_channel_obj, value):
        raise NotImplementedError()

    @staticmethod
    def get_channel_pre_infinity(k_channel_obj):
        raise NotImplementedError()

    @staticmethod
    def set_channel_pre_infinity(k_channel_obj, pre_infinity):
        raise NotImplementedError()

    @staticmethod
    def get_channel_post_infinity(k_channel_obj):
        raise NotImplementedError()

    @staticmethod
    def set_channel_post_infinity(k_channel_obj, post_inifinity):
        raise NotImplementedError()

    @staticmethod
    def get_channel_in_tangent_type_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def set_channel_in_tangent_type_at_index(k_channel_obj, index, in_type):
        raise NotImplementedError()

    @staticmethod
    def get_channel_out_tangent_type_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def set_channel_out_tangent_type_at_index(k_channel_obj, index, out_type):
        raise NotImplementedError()

    @staticmethod
    def get_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def set_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
       raise NotImplementedError()

    @staticmethod
    def get_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def set_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        raise NotImplementedError()

    @staticmethod
    def get_channel_tangents_locked_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def set_channel_tangents_locked_at_index(k_channel_obj, index, value):
        raise NotImplementedError()

    @staticmethod
    def get_channel_weights_locked_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def set_channel_weights_locked_at_index(k_channel_obj, index, value):
        raise NotImplementedError()

    @staticmethod
    def get_channel_value_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def get_channel_time_at_index(k_channel_obj, index):
        raise NotImplementedError()

    @staticmethod
    def get_channel_value_at_time(k_channel_obj, time):
        raise NotImplementedError()

    @staticmethod
    def has_world_space_matrix(node):
        raise NotImplementedError()

    @staticmethod
    def get_world_space_rotation_and_translation(node):
        raise NotImplementedError()

    @staticmethod
    def set_world_space_rotation_and_translation_at_time(node, time, rotation,
                                                         translation):
        raise NotImplementedError()

    @staticmethod
    def remove_animation_from_channel(node, channel_obj):
        raise NotImplementedError()

    @staticmethod
    def shift_animation_in_frame_range(node, channel_obj, start, end):
        raise NotImplementedError()

    @staticmethod
    def remove_animation_from_frame_range(node, channel_obj, start, end):
        raise NotImplementedError()

    @staticmethod
    def pre_import_keyframable_channel_object(k_channel_obj):
        pass

    @staticmethod
    def post_import_keyframable_channel_object(k_channel_obj):
        pass

    @staticmethod
    def pre_export_keyframable_channel_object(k_channel_obj):
        pass

    @staticmethod
    def post_export_keyframable_channel_object(k_channel_obj):
        pass

