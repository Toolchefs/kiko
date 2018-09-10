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

from kiko.constants import IMPORT_METHODS

from kiko.operators.baseoperator import BaseOperatorLoader
from kiko.operators.bakeoperator.constants import TIME, VALUE

class BakeOperatorLoaderV1(BaseOperatorLoader):

    @staticmethod
    def version():
        return 1

    @staticmethod
    def load(data, facade, node, import_anim_method, start_frame, end_frame,
             frame_value, channel=None, time_multiplier=1):

        kco = facade.get_keyframable_channel_object(node, channel)
        if kco is None:
            return

        times = []
        values = []
        for d in data:
            t = d[TIME]
            if t < start_frame or t > end_frame:
                continue

            if import_anim_method == IMPORT_METHODS.ANIMATION.INSERT:
                t -= start_frame
            times.append(frame_value + t * time_multiplier)
            values.append(d[VALUE])

        if not values:
            return

        facade.set_channel_key_frames_in_bulk(kco, times, values)
