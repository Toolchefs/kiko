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

import os

KIKO_FILE_VERSION = 1
KIKO_FILE_EXTENSION = '.kiko'
KB_FILE_EXTENSION = '.kb'

KIKO_PREVIEW_MAXIMUM_SIZE = int(os.environ.get('KIKO_PREVIEW_MAXIMUM_SIZE',
                                               300))
KIKO_PREVIEW_PLAY = int(os.environ.get('KIKO_PREVIEW_PLAY', False))
KIKO_PREVIEW_FPS = int(os.environ.get('KIKO_PREVIEW_FPS', 5))


class APPS:
    MAYA = 'maya'
    NUKE = 'nuke'
    HOUDINI = 'houdini'

    @classmethod
    def all(cls):
        return (cls.MAYA, cls.NUKE, cls.HOUDINI)


class IMPORT_METHODS:
    class OBJECT:
        HIERARCHY = 'hierarchy'
        NAME = 'name'

        @classmethod
        def all(cls):
            return (cls.HIERARCHY, cls.NAME)

    class ANIMATION:
        #delete any animation before loading kiko animation
        APPLY = 'apply'
        #shifts the current animation from the first frame of the kiko animation
        INSERT = 'insert'
        #replace the animation in the frame range of the kiko animation
        REPLACE = 'replace'

        @classmethod
        def all(cls):
            return (cls.APPLY, cls.INSERT, cls.REPLACE)


class SERIALIZATION:
    KIKO_VERSION = 'kikoVersion'
    KIKO_DATA = 'data'
    KIKO_OPERATORS = 'usedOperators'
    KIKO_FPS = 'fps'
    KIKO_FRAME_RANGE = 'frameRange'

    ITEM_ID = 'itemId'
    NAME = 'name'
    TYPE = 'type'
    CHILDREN = 'children'
    PARENT = 'parentItemId'
    CHUNKS = 'chunks'
    CHANNELS = 'channels'

    OPERATOR_DATA = 'opData'
    OPERATOR_VERSION = 'opVer'
    OPERATOR_NAME = 'opName'


class SERIALIZATION_TYPES:
    ROOT_ITEM = 'RootItem'
    ITEM = 'Item'
    CHANNEL = 'Channel'
    CHUNK = 'Chunk'


class KIKO_FILE:
    METADATA = 'metadata'
    SEQUENCE_FOLDER = 'sequence'
    SEQUENCE_FILE_NAME = 'frame'
    DATA = 'data.kb'
    NUM_IMAGES = 'numImages'
    IMAGES_EXT = 'imagesExt'


class KIKO_STD_CHANNEL_NAMES:
    TX = 'translateX'
    TY = 'translateY'
    TZ = 'translateZ'
    RX = 'rotateX'
    RY = 'rotateY'
    RZ = 'rotateZ'
    SX = 'scaleX'
    SY = 'scaleY'
    SZ = 'scaleZ'
    RO = 'rotateOrder'
    VIS = 'visibility'


class KIKO_INFINITY_BEHAVIOR:
    CONSTANT = 'constant'
    LINEAR = 'linear'
    CYCLE = 'cycle'
    CYCLE_RELATIVE = 'cycleRelative'
    OSCILLATE = 'oscillate'


class KIKO_TANGENT_TYPES:
    AUTO = 'auto'
    CLAMPED = 'clamped'
    FLAT = 'flat'
    LINEAR = 'linear'
    PLATEAU = 'plateau'
    STEPNEXT = 'stepNext'
    FIXED = 'fixed'
    SPLINE = 'spline'
    STEP = 'step'
    USER_DEFINED = 'userDefined'

    @classmethod
    def stepped_types(cls):
        return (cls.STEP, cls.STEPNEXT,)


