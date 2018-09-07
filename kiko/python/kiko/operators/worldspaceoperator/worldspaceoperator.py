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
from kiko.operators.worldspaceoperator.loaders.v1 import \
                                                    WorldSpaceOperatorLoaderV1
from kiko.operators.worldspaceoperator.constants import (TIME, ROTATION,
                                                         TRANSLATION)

class WorldSpaceOperator(BaseOperator):
    #IMPORTANT: need to have these two class static members declared in each
    #operator class

    _loaders = {}
    _max_loader_version = None

    @staticmethod
    def name():
        return "WorldSpaceOperator"

    @staticmethod
    def validate(facade, node, channel=None, force=False):
        #check if node has world matrix
        return facade.has_world_space_matrix(node)

    @staticmethod
    def ignore_following_operators():
        return True

    @staticmethod
    def is_app_supported(app_name):
        return app_name in APPS.all()

    @staticmethod
    def is_channel_operator():
        return False

    @staticmethod
    def bakeable():
        return True

    @staticmethod
    def get_frame_range(facade, node, channel=None):
        return facade.get_active_frame_range()

    @staticmethod
    def run(facade, node, channel=None, start_frame=None, end_frame=None):
        rot, trans = facade.get_world_space_rotation_and_translation(node)
        return {TIME: facade.get_current_time(), ROTATION: rot,
                TRANSLATION: trans}


WorldSpaceOperator.register_loader(WorldSpaceOperatorLoaderV1)
