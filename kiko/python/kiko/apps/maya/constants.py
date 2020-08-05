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

from maya.OpenMaya import MTime, MFn
from maya.OpenMayaAnim import MFnAnimCurve
from kiko.constants import (KIKO_STD_CHANNEL_NAMES, KIKO_INFINITY_BEHAVIOR,
                            KIKO_TANGENT_TYPES)

################################################################################
# FPS
################################################################################
FPS = {MTime.k100FPS: 100, MTime.k10FPS: 10, MTime.k1200FPS: 1200,
       MTime.k120FPS: 26, MTime.k125FPS: 125, MTime.k12FPS: 12,
       MTime.k1500FPS: 1500, MTime.k150FPS: 150, MTime.k16FPS: 16,
       MTime.k2000FPS: 2000, MTime.k200FPS: 200, MTime.k20FPS: 20,
       MTime.k240FPS: 240, MTime.k250FPS: 250, MTime.k2FPS: 2,
       MTime.k3000FPS: 3000, MTime.k300FPS: 300, MTime.k375FPS: 375,
       MTime.k3FPS: 3, MTime.k400FPS: 400, MTime.k40FPS: 40, MTime.k4FPS: 4,
       MTime.k500FPS: 500, MTime.k5FPS: 5, MTime.k6000FPS: 6000,
       MTime.k600FPS: 600, MTime.k6FPS: 6, MTime.k750FPS: 750, MTime.k75FPS: 75,
       MTime.k80FPS: 80, MTime.k8FPS: 8, MTime.kFilm: 24, MTime.kGames: 15,
       MTime.kNTSCField: 60, MTime.kNTSCFrame: 30, MTime.kPALField: 50,
       MTime.kPALFrame: 25, MTime.kShowScan:48, MTime.kHours: 0.00277,
       MTime.kMilliseconds: 1000, MTime.kMinutes: 0.0166, MTime.kSeconds: 1,
       MTime.k23_976FPS: 23.976, MTime.k29_97FPS: 29.97,
       MTime.k29_97DF: 29.97, MTime.k47_952FPS: 47.952,
       MTime.k59_94FPS: 59.94, MTime.kInvalid: None}

################################################################################
# CHANNEL NAMES
################################################################################
KIKO_TO_MAYA_CHANNELS = {KIKO_STD_CHANNEL_NAMES.TX: 'tx',
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

MAYA_TO_KIKO_CHANNELS = {}
for k, v in KIKO_TO_MAYA_CHANNELS.items():
    MAYA_TO_KIKO_CHANNELS[v] = k

MAYA_NODE_TO_KIKO_CHANNELS = {MFn.kCamera: {"cs": "cameraScale",
                                            "fl": "focalLength",
                                            "hfa": "hAperture",
                                            "vfa": "vAperture",
                                            "ncp": "nearClipPlane",
                                            "fcp": "farClipPlane",
                                            "hfo": "hFilmOffset",
                                            "vfo": "vFilmOffset"}}
KIKO_TO_MAYA_NODE_CHANNELS = {}
for k, v in MAYA_NODE_TO_KIKO_CHANNELS.items():
    KIKO_TO_MAYA_NODE_CHANNELS[k] = {}
    for ck, cv in v.items():
        KIKO_TO_MAYA_NODE_CHANNELS[k][cv] = ck


################################################################################
# INFINITY BEHAVIOR
################################################################################
KIKO_TO_MAYA_INFINITY_BEHAVIOR = {
            KIKO_INFINITY_BEHAVIOR.CONSTANT     : MFnAnimCurve.kConstant,
            KIKO_INFINITY_BEHAVIOR.LINEAR       : MFnAnimCurve.kLinear,
            KIKO_INFINITY_BEHAVIOR.CYCLE        : MFnAnimCurve.kCycle,
            KIKO_INFINITY_BEHAVIOR.OSCILLATE    : MFnAnimCurve.kOscillate,
            KIKO_INFINITY_BEHAVIOR.CYCLE_RELATIVE: MFnAnimCurve.kCycleRelative}

MAYA_TO_KIKO_INFINITY_BEHAVIOR = {}
for k, v in KIKO_TO_MAYA_INFINITY_BEHAVIOR.items():
    MAYA_TO_KIKO_INFINITY_BEHAVIOR[v] = k

################################################################################
# TANGENTS TYPES
################################################################################
KIKO_TO_MAYA_TANGENT_TYPES = {
            KIKO_TANGENT_TYPES.AUTO     : MFnAnimCurve.kTangentAuto,
            KIKO_TANGENT_TYPES.CLAMPED  : MFnAnimCurve.kTangentClamped,
            KIKO_TANGENT_TYPES.FIXED    : MFnAnimCurve.kTangentFixed,
            KIKO_TANGENT_TYPES.FLAT     : MFnAnimCurve.kTangentFlat,
            KIKO_TANGENT_TYPES.LINEAR   : MFnAnimCurve.kTangentLinear,
            KIKO_TANGENT_TYPES.PLATEAU  : MFnAnimCurve.kTangentPlateau,
            KIKO_TANGENT_TYPES.SPLINE   : MFnAnimCurve.kTangentSmooth,
            KIKO_TANGENT_TYPES.STEP     : MFnAnimCurve.kTangentStep,
            KIKO_TANGENT_TYPES.STEPNEXT : MFnAnimCurve.kTangentStepNext,
            KIKO_TANGENT_TYPES.USER_DEFINED: MFnAnimCurve.kTangentAuto}

MAYA_TO_KIKO_TANGENT_TYPES = {}
for k, v in KIKO_TO_MAYA_TANGENT_TYPES.items():
    MAYA_TO_KIKO_TANGENT_TYPES[v] = k
    
MAYA_TO_KIKO_TANGENT_TYPES[MFnAnimCurve.kTangentAuto] = KIKO_TANGENT_TYPES.AUTO
