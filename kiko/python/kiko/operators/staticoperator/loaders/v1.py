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

from kiko.operators.baseoperator import BaseOperatorLoader
from kiko.operators.staticoperator.constants import VALUE

from kiko.constants import KIKO_TANGENT_TYPES

class StaticOperatorLoaderV1(BaseOperatorLoader):

    @staticmethod
    def version():
        return 1

    @staticmethod
    def load(data, facade, node, import_anim_method, start_frame, end_frame,
             frame_value, channel=None, time_multiplier=1):

        if data[VALUE] is None:
            return

        if not facade.is_channel_animated(node, channel):
            facade.set_channel_value(node, channel, data[VALUE])
            return

        #we delete all keyframes in the frame range first
        facade.remove_animation_from_frame_range(node, channel, start_frame,
                                                 end_frame)

        #if the channel was already animated we set a key at the beginning and
        #end of the animation range
        kco = facade.get_keyframable_channel_object(node, channel)

        index1 = facade.set_channel_key_frame(kco,
                                frame_value + start_frame * time_multiplier,
                                data[VALUE])
        facade.set_channel_tangents_locked_at_index(kco, index1, False)
        facade.set_channel_out_tangent_type_at_index(kco, index1,
                                                     KIKO_TANGENT_TYPES.LINEAR)
        facade.set_channel_out_tangent_angle_and_weight_at_index(kco, index1, 0,
                                                                 1)

        index2 = facade.set_channel_key_frame(kco,
                                frame_value + end_frame * time_multiplier,
                                data[VALUE])
        facade.set_channel_tangents_locked_at_index(kco, index2, False)
        facade.set_channel_in_tangent_type_at_index(kco, index2,
                                                     KIKO_TANGENT_TYPES.LINEAR)
        facade.set_channel_in_tangent_angle_and_weight_at_index(kco, index2, 0,
                                                                1)


