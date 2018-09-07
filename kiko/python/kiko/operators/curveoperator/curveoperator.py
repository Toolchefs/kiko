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

from kiko.constants import APPS
from kiko.operators.baseoperator import BaseOperator
from kiko.operators.curveoperator.loaders.v1 import CurveOperatorLoaderV1
from .constants import (VALUE, TIME, IS_WEIGHTED, PRE_INFINITY, POST_INFINITY,
                        IN_TANGENT_TYPE, OUT_TANGENT_TYPE, IN_ANGLE, OUT_ANGLE,
                        IN_WEIGHT, OUT_WEIGHT, TANGENTS_LOCKED, WEIGHT_LOCKED,
                        KEYS)

class CurveOperator(BaseOperator):
    # IMPORTANT: need to have these two class static members declared in each
    # operator class
    _loaders = {}
    _max_loader_version = None

    @staticmethod
    def name():
        return "CurveOperator"

    @staticmethod
    def validate(facade, node, channel=None, force=False):
        return facade.is_channel_animated(node, channel)

    @staticmethod
    def ignore_following_operators():
        return True

    @staticmethod
    def is_app_supported(app_name):
        return app_name in APPS.all()

    @staticmethod
    def is_channel_operator():
        return True

    @staticmethod
    def bakeable():
        return False

    @staticmethod
    def get_frame_range(facade, node, channel=None):
        kco = facade.get_keyframable_channel_object(node, channel,
                                                    force_create=False)
        if kco is None:
            return None

        return facade.get_frame_range_from_channel(kco)

    @staticmethod
    def run(facade, node, channel=None, start_frame=None, end_frame=None):
        kco = facade.get_keyframable_channel_object(node, channel)
        if kco is None:
            return

        facade.pre_export_keyframable_channel_object(kco)

        num_keys = facade.get_channel_num_keys(kco)
        is_weighted = facade.get_channel_is_weighted(kco)

        pre_infinity = facade.get_channel_pre_infinity(kco)
        post_infinity = facade.get_channel_post_infinity(kco)

        keys = []
        for ki in range(num_keys):
            t = facade.get_channel_time_at_index(kco, ki)
            if ((start_frame is not None and t < start_frame) or
                (end_frame is not None and t > end_frame)):
                continue

            in_type = facade.get_channel_in_tangent_type_at_index(kco, ki)
            out_type = facade.get_channel_out_tangent_type_at_index(kco, ki)
            in_a, in_w = facade.\
                    get_channel_in_tangent_angle_and_weight_at_index(kco, ki)
            out_a, out_w = facade.\
                    get_channel_out_tangent_angle_and_weight_at_index(kco, ki)

            t_locked = facade.get_channel_tangents_locked_at_index(kco, ki)
            w_locked = facade.get_channel_weights_locked_at_index(kco, ki)

            key = {TIME: t,
                   VALUE: facade.get_channel_value_at_index(kco, ki),
                   IN_TANGENT_TYPE: in_type, OUT_TANGENT_TYPE: out_type,
                   IN_ANGLE: in_a, OUT_ANGLE: out_a,
                   IN_WEIGHT: in_w, OUT_WEIGHT: out_w,
                   TANGENTS_LOCKED: t_locked, WEIGHT_LOCKED: w_locked}
            keys.append(key)

        # in case frames are missing we bake the missing range: this could happen
        # when a start and end frame were specified
        if not keys:
            if start_frame is not None and end_frame is not None:
                for t in range(int(start_frame), int(end_frame) + 1):
                    keys.append({TIME: t,
                               VALUE: facade.get_channel_value_at_time(kco, t)})
        else:
            if start_frame is not None and keys[0][TIME] > int(start_frame):
                for i in range(int(keys[0][TIME]) - 1, int(start_frame) - 1, -1):
                    keys.insert(0, {TIME: i,
                               VALUE: facade.get_channel_value_at_time(kco, i)})
            if end_frame is not None and keys[-1][TIME] < int(end_frame):
                for i in range(int(keys[-1][TIME]) + 1, int(end_frame) + 1):
                    keys.append({TIME: i,
                               VALUE: facade.get_channel_value_at_time(kco, i)})

        facade.post_export_keyframable_channel_object(kco)

        return {KEYS: keys,
                IS_WEIGHTED: is_weighted,
                PRE_INFINITY: pre_infinity,
                POST_INFINITY: post_infinity}

CurveOperator.register_loader(CurveOperatorLoaderV1)
