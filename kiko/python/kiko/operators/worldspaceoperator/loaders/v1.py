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

from kiko.constants import KIKO_STD_CHANNEL_NAMES as KSCN
from kiko.constants import IMPORT_METHODS

from kiko.operators.baseoperator import BaseOperatorLoader
from kiko.operators.worldspaceoperator.constants import (TIME, ROTATION,
                                                         TRANSLATION)

class WorldSpaceOperatorLoaderV1(BaseOperatorLoader):

    @staticmethod
    def version():
        return 1

    @staticmethod
    def load(data, facade, node, import_anim_method, start_frame, end_frame,
             frame_value, channel=None, time_multiplier=1):

        tm = time_multiplier
        #cleaning the transform value
        for ch_name in [KSCN.TX, KSCN.TY, KSCN.TZ, KSCN.RX, KSCN.RY, KSCN.RZ]:
            ch_name = facade.map_kiko_channel_to_app_channel(node, ch_name)
            ch = facade.get_channel_object(node, ch_name)
            if import_anim_method == IMPORT_METHODS.ANIMATION.APPLY:
                facade.remove_animation_from_channel(node, ch)
            elif import_anim_method == IMPORT_METHODS.ANIMATION.INSERT:
                facade.shift_animation_in_frame_range(node, ch, frame_value,
                                  frame_value + (end_frame - start_frame) * tm)
            elif import_anim_method == IMPORT_METHODS.ANIMATION.REPLACE:
                facade.remove_animation_from_frame_range(node, ch,
                                                frame_value + start_frame * tm,
                                                frame_value + end_frame * tm)

        for d in data:
            t = d[TIME]
            if t < start_frame or t > end_frame:
                continue

            if import_anim_method == IMPORT_METHODS.ANIMATION.INSERT:
                t -= start_frame
            facade.set_world_space_rotation_and_translation_at_time(node,
                                    frame_value + t * time_multiplier,
                                    d[ROTATION], d[TRANSLATION])

