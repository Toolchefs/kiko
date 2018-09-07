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

from kiko.constants import IMPORT_METHODS, APPS, KIKO_TANGENT_TYPES

from kiko.operators.baseoperator import BaseOperatorLoader
from kiko.operators.curveoperator.constants import (VALUE, TIME, IS_WEIGHTED,
                PRE_INFINITY, POST_INFINITY, IN_TANGENT_TYPE, OUT_TANGENT_TYPE,
                IN_ANGLE, OUT_ANGLE, IN_WEIGHT, OUT_WEIGHT, TANGENTS_LOCKED,
                WEIGHT_LOCKED, KEYS)

class CurveOperatorLoaderV1(BaseOperatorLoader):

    @staticmethod
    def version():
        return 1

    @staticmethod
    def set_tangents_on_key(facade, kco, index, key_data):
        # breaking the tangents before setting the values
        facade.set_channel_weights_locked_at_index(kco, index, False)
        facade.set_channel_tangents_locked_at_index(kco, index, False)

        facade.set_channel_in_tangent_type_at_index(kco, index,
                                                key_data[IN_TANGENT_TYPE])
        facade.set_channel_out_tangent_type_at_index(kco, index,
                                                key_data[OUT_TANGENT_TYPE])

        if key_data[IN_TANGENT_TYPE] not in KIKO_TANGENT_TYPES.stepped_types():
            facade.set_channel_in_tangent_angle_and_weight_at_index(kco, index,
                                        key_data[IN_ANGLE], key_data[IN_WEIGHT])
        if key_data[OUT_TANGENT_TYPE] not in KIKO_TANGENT_TYPES.stepped_types():
            facade.set_channel_out_tangent_angle_and_weight_at_index(kco, index,
                                key_data[OUT_ANGLE], key_data[OUT_WEIGHT])

        # setting the right values for the tangents
        facade.set_channel_weights_locked_at_index(kco, index,
                                                key_data[WEIGHT_LOCKED])
        facade.set_channel_tangents_locked_at_index(kco, index,
                                                key_data[TANGENTS_LOCKED])

    @staticmethod
    def load(data, facade, node, import_anim_method, start_frame, end_frame,
             frame_value, channel=None, time_multiplier=1):

        kco = facade.get_keyframable_channel_object(node, channel)
        if kco is None:
            return

        facade.pre_import_keyframable_channel_object(kco)

        facade.set_channel_is_weighted(kco, data[IS_WEIGHTED])

        indices = []

        temp_data = []
        for key_data in data[KEYS]:
            t = key_data[TIME]
            if t < start_frame or t > end_frame:
                continue

            if import_anim_method == IMPORT_METHODS.ANIMATION.INSERT:
                t -= start_frame

            indices.append(facade.set_channel_key_frame(kco,
                                frame_value + t * time_multiplier,
                                key_data[VALUE]))
            temp_data.append(key_data)

        for i in range(len(indices)):
            key_data = temp_data[i]
            # this may be the case if any baking happened on serializing the data
            if len(key_data) == 2:
                continue
            index = indices[i]
            CurveOperatorLoaderV1.set_tangents_on_key(facade, kco, index,
                                                      key_data)

        if import_anim_method == IMPORT_METHODS.ANIMATION.APPLY:
            facade.set_channel_pre_infinity(kco, data[PRE_INFINITY])
            facade.set_channel_post_infinity(kco, data[POST_INFINITY])

        facade.post_import_keyframable_channel_object(kco)

