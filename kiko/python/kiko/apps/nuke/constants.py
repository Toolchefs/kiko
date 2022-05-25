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

import nuke

from kiko.constants import (KIKO_STD_CHANNEL_NAMES, KIKO_INFINITY_BEHAVIOR,
                            KIKO_TANGENT_TYPES)

################################################################################
#CHANNEL NAMES
################################################################################
KIKO_TO_NUKE_CHANNELS = {KIKO_STD_CHANNEL_NAMES.TX: 'translate[0]',
                         KIKO_STD_CHANNEL_NAMES.TY: 'translate[1]',
                         KIKO_STD_CHANNEL_NAMES.TZ: 'translate[2]',
                         KIKO_STD_CHANNEL_NAMES.RX: 'rotate[0]',
                         KIKO_STD_CHANNEL_NAMES.RY: 'rotate[1]',
                         KIKO_STD_CHANNEL_NAMES.RZ: 'rotate[2]',
                         KIKO_STD_CHANNEL_NAMES.SX: 'scale[0]',
                         KIKO_STD_CHANNEL_NAMES.SY: 'scale[1]',
                         KIKO_STD_CHANNEL_NAMES.SZ: 'scale[2]',
                         KIKO_STD_CHANNEL_NAMES.RO: 'rot_order'}

NUKE_TO_KIKO_CHANNELS = {}
for k, v in KIKO_TO_NUKE_CHANNELS.items():
    NUKE_TO_KIKO_CHANNELS[v] = k


NUKE_NODE_TO_KIKO_CHANNELS = {'Camera': {"uniform_scale": "cameraScale",
                                         "focal": "focalLength",
                                         "haperture": "hAperture",
                                         "vaperture": "vAperture",
                                         "near": "nearClipPlane",
                                         "far": "farClipPlane",
                                         "win_translate[0]": "hFilmOffset",
                                         "win_translate[1]": "vFilmOffset"}}
NUKE_NODE_TO_KIKO_CHANNELS['Camera2'] = NUKE_NODE_TO_KIKO_CHANNELS['Camera']

KIKO_TO_NUKE_NODE_CHANNELS = {}
for k, v in NUKE_NODE_TO_KIKO_CHANNELS.items():
    KIKO_TO_NUKE_NODE_CHANNELS[k] = {}
    for ck, cv in v.items():
        KIKO_TO_NUKE_NODE_CHANNELS[k][cv] = ck


################################################################################
#TANGENTS TYPES
################################################################################
KIKO_TO_NUKE_TANGENT_TYPES = {
            KIKO_TANGENT_TYPES.AUTO         : nuke.SMOOTH,
            KIKO_TANGENT_TYPES.CLAMPED      : nuke.SMOOTH,
            KIKO_TANGENT_TYPES.FIXED        : nuke.SMOOTH,
            KIKO_TANGENT_TYPES.FLAT         : nuke.SMOOTH,
            KIKO_TANGENT_TYPES.LINEAR       : nuke.LINEAR,
            KIKO_TANGENT_TYPES.PLATEAU      : nuke.SMOOTH,
            KIKO_TANGENT_TYPES.SPLINE       : nuke.SMOOTH,
            KIKO_TANGENT_TYPES.STEP         : nuke.CONSTANT,
            #although this is not correct we need to map STEPNEXT to something
            KIKO_TANGENT_TYPES.STEPNEXT     : nuke.CONSTANT,
            KIKO_TANGENT_TYPES.USER_DEFINED : nuke.USER_SET_SLOPE}

NUKE_TO_KIKO_TANGENT_TYPES = {}
for k, v in KIKO_TO_NUKE_TANGENT_TYPES.items():
   NUKE_TO_KIKO_TANGENT_TYPES[v] = k

NUKE_TO_KIKO_TANGENT_TYPES[nuke.SMOOTH] = KIKO_TANGENT_TYPES.SPLINE
NUKE_TO_KIKO_TANGENT_TYPES[nuke.CUBIC] = KIKO_TANGENT_TYPES.SPLINE
NUKE_TO_KIKO_TANGENT_TYPES[nuke.USER_SET_SLOPE] = KIKO_TANGENT_TYPES.SPLINE
NUKE_TO_KIKO_TANGENT_TYPES[nuke.BREAK] = KIKO_TANGENT_TYPES.LINEAR

for t in [nuke.CATMULL_ROM, nuke.BEFORE_LINEAR, nuke.BEFORE_CONST,
          nuke.AFTER_LINEAR, nuke.AFTER_CONST]:
    NUKE_TO_KIKO_TANGENT_TYPES[t] = KIKO_TANGENT_TYPES.SPLINE
