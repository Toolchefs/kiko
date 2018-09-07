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

from kiko.constants import APPS, KIKO_INFINITY_BEHAVIOR
from kiko.operators.baseoperator import BaseOperator
from kiko.operators.bakeoperator.loaders.v1 import BakeOperatorLoaderV1
from kiko.operators.bakeoperator.constants import TIME, VALUE

class BakeOperator(BaseOperator):
    #IMPORTANT: need to have these two class static members declared in each
    #operator class
    _loaders = {}
    _max_loader_version = None

    @staticmethod
    def name():
        return "BakeOperator"

    @staticmethod
    def validate(facade, node, channel=None, force=False):
        return force or facade.is_channel_connected(node, channel)

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
        return True

    @staticmethod
    def get_frame_range(facade, node, channel=None):
        gui_range = facade.get_active_frame_range()

        key_obj = facade.get_keyframable_channel_object(node, channel,
                                                        force_create=False)
        if key_obj is None:
            return gui_range

        anim_range = facade.get_frame_range_from_channel(key_obj)
        if not anim_range:
            return gui_range

        anim_range = list(anim_range)

        #in case pre infinity is not constants then the baking initial frame
        #should be the GUI start frame (if GUI start frame is smaller)
        if (anim_range[0] > gui_range[0] and
                facade.get_channel_pre_infinity(key_obj) !=
                KIKO_INFINITY_BEHAVIOR.CONSTANT):
            anim_range[0] = gui_range[0]

        #in case post infinity is not constants then the baking final frame
        #should be the GUI end frame (if GUI end frame is greater)
        if (anim_range[1] < gui_range[1] and
                facade.get_channel_post_infinity(key_obj) !=
                KIKO_INFINITY_BEHAVIOR.CONSTANT):
            anim_range[1] = gui_range[1]

        return tuple(anim_range)

    @staticmethod
    def run(facade, node, channel=None, start_frame=None, end_frame=None):
        return {TIME: facade.get_current_time(),
                VALUE: facade.get_channel_value(node, channel)}


BakeOperator.register_loader(BakeOperatorLoaderV1)
