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

import hou

from kiko.constants import (KIKO_STD_CHANNEL_NAMES, KIKO_INFINITY_BEHAVIOR,
                            KIKO_TANGENT_TYPES)

################################################################################
# CHANNEL NAMES
################################################################################
KIKO_TO_HOU_CHANNELS = {KIKO_STD_CHANNEL_NAMES.TX: 'tx',
                        KIKO_STD_CHANNEL_NAMES.TY: 'ty',
                        KIKO_STD_CHANNEL_NAMES.TZ: 'tz',
                        KIKO_STD_CHANNEL_NAMES.RX: 'rx',
                        KIKO_STD_CHANNEL_NAMES.RY: 'ry',
                        KIKO_STD_CHANNEL_NAMES.RZ: 'rz',
                        KIKO_STD_CHANNEL_NAMES.SX: 'sx',
                        KIKO_STD_CHANNEL_NAMES.SY: 'sy',
                        KIKO_STD_CHANNEL_NAMES.SZ: 'sz',
                        KIKO_STD_CHANNEL_NAMES.VIS: 'v',
                        KIKO_STD_CHANNEL_NAMES.RO: 'ro'}

HOU_TO_KIKO_CHANNELS = {}
for k, v in KIKO_TO_HOU_CHANNELS.items():
    HOU_TO_KIKO_CHANNELS[v] = k


################################################################################
# INFINITY BEHAVIOR
################################################################################
if hou.applicationVersion()[0] > 14:
    KIKO_TO_HOU_INFINITY_BEHAVIOR = {
            KIKO_INFINITY_BEHAVIOR.CONSTANT     : hou.parmExtrapolate.Hold,
            KIKO_INFINITY_BEHAVIOR.LINEAR       : hou.parmExtrapolate.Slope,
            KIKO_INFINITY_BEHAVIOR.CYCLE        : hou.parmExtrapolate.Cycle,
            KIKO_INFINITY_BEHAVIOR.OSCILLATE    : hou.parmExtrapolate.Oscillate,
            KIKO_INFINITY_BEHAVIOR.CYCLE_RELATIVE: hou.parmExtrapolate.CycleOffset}
else:
    KIKO_TO_HOU_INFINITY_BEHAVIOR = {}

HOU_TO_KIKO_INFINITY_BEHAVIOR = {}
for k, v in KIKO_TO_HOU_INFINITY_BEHAVIOR.items():
    HOU_TO_KIKO_INFINITY_BEHAVIOR[v] = k

################################################################################
# TANGENTS TYPES
################################################################################
KIKO_TO_HOU_TANGENT_TYPES = {
            KIKO_TANGENT_TYPES.AUTO     : "cubic()",
            KIKO_TANGENT_TYPES.CLAMPED  : "cubic()",
            KIKO_TANGENT_TYPES.FIXED    : "cubic()",
            KIKO_TANGENT_TYPES.FLAT     : "cubic()",
            # although mapping linear to cubic does not make much sense, with
            # this we get the closest result to maya
            KIKO_TANGENT_TYPES.LINEAR   : "cubic()",
            KIKO_TANGENT_TYPES.PLATEAU  : "cubic()",
            KIKO_TANGENT_TYPES.SPLINE   : "cubic()",
            KIKO_TANGENT_TYPES.STEP     : "constant()",
            KIKO_TANGENT_TYPES.STEPNEXT : "cubic()",
            KIKO_TANGENT_TYPES.USER_DEFINED: "cubic()"}

HOU_TO_KIKO_TANGENT_TYPES = {}
for k, v in KIKO_TO_HOU_TANGENT_TYPES.items():
    HOU_TO_KIKO_TANGENT_TYPES[v] = k
    
HOU_TO_KIKO_TANGENT_TYPES["bezier()"] = KIKO_TANGENT_TYPES.AUTO
