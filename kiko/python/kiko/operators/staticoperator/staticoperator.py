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
from kiko.operators.staticoperator.loaders.v1 import StaticOperatorLoaderV1
from kiko.operators.staticoperator.constants import VALUE

class StaticOperator(BaseOperator):
    #IMPORTANT: need to have these two class static members declared in each
    #operator class
    _loaders = {}
    _max_loader_version = None

    @staticmethod
    def name():
        return "StaticOperator"

    @staticmethod
    def validate(facade, node, channel=None, force=False):
        return force or not facade.is_channel_connected(node, channel)

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
        return None

    @staticmethod
    def run(facade, node, channel=None, start_frame=None, end_frame=None):
        return {VALUE: facade.get_channel_value(node, channel)}


StaticOperator.register_loader(StaticOperatorLoaderV1)
