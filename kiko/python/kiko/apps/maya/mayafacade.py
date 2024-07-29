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


import re
import sys
import math
import warnings
import tempfile

from maya import OpenMayaUI as omui
from maya import OpenMaya, OpenMayaAnim
from maya import cmds

from kiko.constants import APPS, KIKO_PREVIEW_MAXIMUM_SIZE
from kiko.exceptions import FacadeRuntimeError, FacadeWarning
from kiko.apps.basefacade import BaseFacade
from kiko.ui.qthandler import QtWidgets, shiboken

from .constants import (MAYA_TO_KIKO_CHANNELS, KIKO_TO_MAYA_CHANNELS, FPS,
                        KIKO_TO_MAYA_INFINITY_BEHAVIOR,
                        MAYA_TO_KIKO_INFINITY_BEHAVIOR,
                        KIKO_TO_MAYA_TANGENT_TYPES, MAYA_TO_KIKO_TANGENT_TYPES,
                        MAYA_NODE_TO_KIKO_CHANNELS, KIKO_TO_MAYA_NODE_CHANNELS)
from .mayaundohelper import MayaUndoHelper
from .mayapreferences import MayaPreferences


class MayaFacadeHelper(object):
    ATTR_REGEX = re.compile("(?P<name>[0-9a-zA-Z_]+)\[(?P<index>\d{0,4})\]")

    AC_NODE_TYPES = [OpenMaya.MFn.kAnimCurveTimeToAngular,
                     OpenMaya.MFn.kAnimCurveTimeToUnitless,
                     OpenMaya.MFn.kAnimCurveTimeToTime,
                     OpenMaya.MFn.kAnimCurveTimeToDistance]

    INVALID_ATTR_TYPES = [OpenMaya.MFn.kMessageAttribute]

    @staticmethod
    def is_angular_curve(curve):
        return curve.animCurveType() == OpenMayaAnim.MFnAnimCurve.kAnimCurveTA

    @staticmethod
    def get_connected_animation_curve(plug):
        connections = OpenMaya.MPlugArray()
        plug.connectedTo(connections, True, False)
        if connections.length():
            for ci in range(connections.length()):
                node = connections[ci].node()
                if node.apiType() in MayaFacadeHelper.AC_NODE_TYPES:
                    return node
        return None

    @staticmethod
    def get_fps():
        return FPS[OpenMaya.MTime.uiUnit()]

    @classmethod
    def get_channels(cls, plug, attrs_objs):
        attr_fn = OpenMaya.MFnAttribute(plug.attribute())
        if plug.isNull() or attr_fn.isHidden():
            return

        t = plug.attribute().apiType()

        if plug.isArray():
            plug.evaluateNumElements()
            indices = OpenMaya.MIntArray()
            plug.getExistingArrayAttributeIndices(indices)
            for index in indices:
                c_plug = plug.elementByLogicalIndex(index)
                cls.get_channels(c_plug, attrs_objs)
        elif plug.isCompound():
            for index in range(plug.numChildren()):
                c_plug = plug.child(index)
                cls.get_channels(c_plug, attrs_objs)
        elif plug.isKeyable() and t not in cls.INVALID_ATTR_TYPES:
            attrs_objs.append(plug)

    @staticmethod
    def get_numeric_attribute_value(plug):
        nData = OpenMaya.MFnNumericData
        fn = OpenMaya.MFnNumericAttribute(plug.attribute())

        t = fn.unitType()
        if t == nData.kBoolean:
            return plug.asBool()

        elif t == nData.kShort:
            return plug.asShort()
        elif t == nData.k2Short:
            return [plug.child(0).asShort(), plug.child(1).asShort()]
        elif t == nData.k3Short:
            return [plug.child(0).asShort(), plug.child(1).asShort(),
                    plug.child(2).asShort()]

        elif t in [nData.kInt, nData.kLong]:
            return plug.asInt()
        elif t in [nData.k2Int, nData.k2Long]:
            return [plug.child(0).asInt(), plug.child(1).asInt()]
        elif t in [nData.k3Int, nData.k3Long]:
            return [plug.child(0).asInt(), plug.child(1).asInt(),
                    plug.child(2).asInt()]

        elif t == nData.kDouble:
            return plug.asDouble()
        elif t == nData.k2Double:
            return [plug.child(0).asDouble(), plug.child(1).asDouble()]
        elif t == nData.k3Double:
            return [plug.child(0).asDouble(), plug.child(1).asDouble(),
                    plug.child(2).asDouble()]
        elif t == nData.k4Double:
            return [plug.child(0).asDouble(), plug.child(1).asDouble(),
                    plug.child(2).asDouble(), plug.child(3).asDouble()]

        elif t == nData.kFloat:
            return plug.asFloat()
        elif t == nData.k2Float:
            return [plug.child(0).asFloat(), plug.child(1).asFloat()]
        elif t == nData.k3Float:
            return [plug.child(0).asFloat(), plug.child(1).asFloat(),
                    plug.child(2).asFloat()]

        raise FacadeRuntimeError("Could not find numeric type for plug %s" %
                                 plug.partialName(True))

    @staticmethod
    def set_numeric_attribute_value(plug, value):
        nData = OpenMaya.MFnNumericData
        fn = OpenMaya.MFnNumericAttribute(plug.attribute())

        t = fn.unitType()
        if t == nData.kBoolean:
            MayaUndoHelper.dg_modifier.newPlugValueBool(plug, value)
            return

        if t in [nData.kShort, nData.kInt, nData.kLong, nData.kByte,
                  nData.kChar]:
            MayaUndoHelper.dg_modifier.newPlugValueInt(plug, value)
            return

        if t in [nData.kDouble, nData.kFloat]:
            MayaUndoHelper.dg_modifier.newPlugValueDouble(plug, value)
            return

        if t in [nData.k2Short, nData.k2Int, nData.k2Long]:
            for i in range(2):
                MayaUndoHelper.dg_modifier.newPlugValueInt(plug.child(i),
                                                           value[i])
            return

        if t in [nData.k2Double, nData.k2Float]:
            for i in range(2):
                MayaUndoHelper.dg_modifier.newPlugValueDouble(plug.child(i),
                                                              value[i])
            return

        if t in [nData.k3Short, nData.k3Int, nData.k3Long]:
            for i in range(3):
                MayaUndoHelper.dg_modifier.newPlugValueInt(plug.child(i),
                                                           value[i])
            return

        if t in [nData.k3Double, nData.k3Float]:
            for i in range(3):
                MayaUndoHelper.dg_modifier.newPlugValueDouble(plug.child(i),
                                                              value[i])
            return

        if t == nData.k4Double:
            for i in range(4):
                MayaUndoHelper.dg_modifier.newPlugValueDouble(plug.child(i),
                                                              value[i])
            return

        raise FacadeRuntimeError("Could not set numeric type for plug %s" %
                                 plug.partialName(True))

    @staticmethod
    def can_get_mobject(plug):
        try:
            data = plug.asMObject()
            return True
        except:
            return False

    @staticmethod
    def get_unit_attribute_value(plug):
        fn = OpenMaya.MFnUnitAttribute(plug.attribute())

        if fn.unitType() == OpenMaya.MFnUnitAttribute.kAngle:
            return math.degrees(plug.asFloat())
        elif fn.unitType() == OpenMaya.MFnUnitAttribute.kTime:
            return plug.asMTime().value()
        elif fn.unitType() == OpenMaya.MFnUnitAttribute.kDistance:
            return plug.asMDistance().value()

    @staticmethod
    def set_unit_attribute_value(plug, value):
        fn = OpenMaya.MFnUnitAttribute(plug.attribute())
        if fn.unitType() == OpenMaya.MFnUnitAttribute.kAngle:
            MayaUndoHelper.dg_modifier.newPlugValueMAngle(plug,
                                        OpenMaya.MAngle(math.radians(value)))
        elif fn.unitType() == OpenMaya.MFnUnitAttribute.kDistance:
            MayaUndoHelper.dg_modifier.newPlugValueMDistance(plug,
                                                    OpenMaya.MDistance(value))
        elif fn.unitType() == OpenMaya.MFnUnitAttribute.kTime:
            MayaUndoHelper.dg_modifier.newPlugValueMTime(plug,
                                OpenMaya.MTime(value, OpenMaya.MTime.uiUnit()))

    @staticmethod
    def find_plug(node_obj, channel_name):
        mfn = OpenMaya.MFnDependencyNode(node_obj)

        tokens = channel_name.split('.')
        match = MayaFacadeHelper.ATTR_REGEX.match(tokens[0])
        if match:
            name = match.group(1)
            index = int(match.group(2))
            plug = mfn.findPlug(name)
            plug.evaluateNumElements()
            plug = plug.elementByLogicalIndex(index)
        else:
            try:
                plug = mfn.findPlug(tokens[0])
            except:
                warnings.warn("Cannot find plug %s.%s" %
                              (mfn.name(), tokens[0]), FacadeWarning)
                return

        for t in tokens[1:]:
            name = t
            index = None

            match = MayaFacadeHelper.ATTR_REGEX.match(t[0])
            if match:
                name = match.group(1)
                index = int(match.group(2))

            child_plug = mfn.findPlug(name)
            plug = plug.child(child_plug.attribute())
            if not index is None:
                plug.evaluateNumElements()
                plug = plug.elementByLogicalIndex(index)

        return plug

    @staticmethod
    def sanitize_matrix(matrix):
        # apparently the matrix translation values are always in centimeters.
        # so we use this little hack to have the right translation values
        if OpenMaya.MDistance.uiUnit() == OpenMaya.MDistance.kCentimeters:
            final_index = 4
        else:
            final_index = 3

        matrix_list = []
        for i in range(final_index):
            for j in range(4):
                matrix_list.append(matrix(i, j))

        if final_index == 3:
            for i in range(3):
                matrix_list.append(OpenMaya.MDistance(matrix(3, i)).asUnits(
                                                   OpenMaya.MDistance.uiUnit()))
            matrix_list.append(1.0)

        return matrix_list

    @staticmethod
    def sanitize_translation_vector(vector):
        if OpenMaya.MDistance.uiUnit() != OpenMaya.MDistance.kCentimeters:
            for i in range(3):
                vector[i] = OpenMaya.MDistance(vector[i]).asUnits(
                                               OpenMaya.MDistance.uiUnit())
        return vector

    @staticmethod
    def get_main_window():
        main_window_ptr = omui.MQtUtil.mainWindow()

        # Support for Python 2
        if sys.version_info.major < 3:
            main_window_ptr = long(main_window_ptr)
        else:
            main_window_ptr = int(main_window_ptr)

        main_window = shiboken.wrapInstance(main_window_ptr,
                                            QtWidgets.QMainWindow)

        return main_window

class MayaFacade(BaseFacade):

    @staticmethod
    def get_app_name():
        return APPS.MAYA

    @staticmethod
    def get_selection():
        sel_list = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getActiveSelectionList(sel_list)
        res = []
        for i in range(sel_list.length()):
            o = OpenMaya.MObject()
            sel_list.getDependNode(i, o)
            res.append(o)
        return res

    @staticmethod
    def supports_image_generation():
        return True

    @staticmethod
    def get_image_sources():
        return cmds.ls(type='camera')

    @staticmethod
    def generate_image_sequence(source, start_frame, end_frame, sample_every=1):
        prev_time = cmds.currentTime(q=True)
        prev_camera = cmds.lookThru(q=True)

        _, path = tempfile.mkstemp()

        w = cmds.getAttr('defaultResolution.width')
        h = cmds.getAttr('defaultResolution.height')
        aspect_ratio = float(w) / float(h)

        if aspect_ratio < 1:
            h = KIKO_PREVIEW_MAXIMUM_SIZE
            w = int(KIKO_PREVIEW_MAXIMUM_SIZE * aspect_ratio)
        else:
            w = KIKO_PREVIEW_MAXIMUM_SIZE
            h = int(KIKO_PREVIEW_MAXIMUM_SIZE / aspect_ratio)

        cmds.lookThru(source)
        cmds.refresh()

        frames = [i for i in range(start_frame, end_frame + 1, sample_every)]

        cmds.playblast(viewer=False, quality=90, frame=frames, format='image',
                       compression="jpg", showOrnaments=False, filename=path,
                       os=True, width=w, height=h, forceOverwrite=True,
                       percent=100)

        cmds.currentTime(prev_time)
        cmds.lookThru(prev_camera)
        cmds.refresh()

        return [path + (".%04d.jpg" % i) for i in range(len(frames))]

    @staticmethod
    def get_node_by_name(node_name):
        sel_list = OpenMaya.MSelectionList()
        try:
            sel_list.add(node_name)
        except RuntimeError:
            return None

        if sel_list.length() == 0:
            return None

        o = OpenMaya.MObject()
        sel_list.getDependNode(0, o)
        return o

    @staticmethod
    def map_kiko_channel_to_app_channel(node_obj, channel_name):
        node_map = KIKO_TO_MAYA_NODE_CHANNELS.get(node_obj.apiType())
        if node_map and channel_name in node_map:
            return node_map.get(channel_name)
        return KIKO_TO_MAYA_CHANNELS.get(channel_name) or channel_name

    @staticmethod
    def map_app_channel_to_kiko_channel(node_obj, channel_name):
        node_map = MAYA_NODE_TO_KIKO_CHANNELS.get(node_obj.apiType())
        if node_map and channel_name in node_map:
            return node_map.get(channel_name)
        return MAYA_TO_KIKO_CHANNELS.get(channel_name) or channel_name

    @staticmethod
    def get_name(node_obj):
        if MayaPreferences.use_full_paths:
            try:
                return OpenMaya.MFnDagNode(node_obj).fullPathName()
            except:
                pass
        return OpenMaya.MFnDependencyNode(node_obj).name()

    @staticmethod
    def get_selected_channel_names():
        return cmds.channelBox("mainChannelBox", selectedMainAttributes=True,
                               q=True)

    @staticmethod
    def list_channels(node_obj):
        mfn = OpenMaya.MFnDependencyNode(node_obj)

        attrs_objs = []
        for ai in range(mfn.attributeCount()):
            attr_obj = mfn.attribute(ai)
            plug = mfn.findPlug(attr_obj, True)
            # plug = OpenMaya.MPlug(node_obj, attr_obj)

            # stupid maya will start iterating sometimes through children or
            # element plugs.
            if plug.isChild() or plug.isElement():
                continue

            MayaFacadeHelper.get_channels(plug, attrs_objs)

        return attrs_objs

    @staticmethod
    def is_channel_animated(node_obj, channel_obj):
        return bool(MayaFacadeHelper.get_connected_animation_curve(channel_obj))

    @staticmethod
    def is_channel_connected(node_obj, channel_obj):
        connections = OpenMaya.MPlugArray()
        channel_obj.connectedTo(connections, True, False)
        return bool(connections.length())

    @staticmethod
    def get_children(node_obj):
        ish = MayaPreferences.ignore_shapes_in_hierarchy

        mfn = OpenMaya.MFnDagNode(node_obj)
        return [mfn.child(i) for i in range(mfn.childCount())
                if not ish or (ish and not
                               mfn.child(i).hasFn(OpenMaya.MFn.kShape))]

    @staticmethod
    def get_channel_name(node_obj, channel_obj):
        return channel_obj.partialName(0, 1, 1)

    @staticmethod
    def get_channel_value(node_obj, channel_obj):

        c_mobj = channel_obj.attribute()
        if c_mobj.hasFn(OpenMaya.MFn.kUnitAttribute):
            return MayaFacadeHelper.get_unit_attribute_value(channel_obj)

        if c_mobj.hasFn(OpenMaya.MFn.kNumericAttribute):
            return MayaFacadeHelper.get_numeric_attribute_value(channel_obj)

        if c_mobj.hasFn(OpenMaya.MFn.kEnumAttribute):
            return channel_obj.asShort()

        if (c_mobj.hasFn(OpenMaya.MFn.kMatrixAttribute) or
                    c_mobj.hasFn(OpenMaya.MFn.kFloatMatrixAttribute)):
            if not MayaFacadeHelper.can_get_mobject(channel_obj):
                return

            mobj = channel_obj.asMObject()
            mmatrix = OpenMaya.MFnMatrixData(mobj).matrix()
            return [mmatrix[0][0], mmatrix[0][1], mmatrix[0][2], mmatrix[0][3],
                    mmatrix[1][0], mmatrix[1][1], mmatrix[1][2], mmatrix[1][3],
                    mmatrix[2][0], mmatrix[2][1], mmatrix[2][2], mmatrix[2][3],
                    mmatrix[3][0], mmatrix[3][1], mmatrix[3][2], mmatrix[3][3]]

        if c_mobj.hasFn(OpenMaya.MFn.kFloatAngleAttribute):
            return math.degrees(channel_obj.asFloat())

        if c_mobj.hasFn(OpenMaya.MFn.kDoubleAngleAttribute):
            return math.degrees(channel_obj.asDouble())

        if c_mobj.hasFn(OpenMaya.MFn.kTypedAttribute):
            fn = OpenMaya.MFnTypedAttribute(c_mobj)
            if fn.attrType() == OpenMaya.MFnData.kString:
                try:
                    return channel_obj.asString()
                except:
                    return

        raise FacadeRuntimeError("Could not find value for plug %s" %
                                 channel_obj.partialName(True))

    @staticmethod
    def set_channel_value(node_obj, channel_obj, value):
        if channel_obj.isLocked():
            warnings.warn("Cannot set attribute %s. It is locked." %
                          channel_obj.partialName(True), FacadeWarning)
            return

        connections = OpenMaya.MPlugArray()
        channel_obj.connectedTo(connections, True, False)
        if bool(connections.length()):
            warnings.warn("Cannot set attribute %s. It is connected." %
                          channel_obj.partialName(True), FacadeWarning)
            return

        if channel_obj.isChild():
            parent_plug = channel_obj.parent()
            connections = OpenMaya.MPlugArray()
            parent_plug.connectedTo(connections, True, False)
            if bool(connections.length()):
                warnings.warn("Cannot set attribute %s. It is connected." %
                              parent_plug.partialName(True), FacadeWarning)
                return

        if channel_obj.isCompound():
            warnings.warn("Cannot set attribute %s. It is a compound." %
                          channel_obj.partialName(True), FacadeWarning)
            return

        c_mobj = channel_obj.attribute()

        if c_mobj.hasFn(OpenMaya.MFn.kUnitAttribute):
            MayaFacadeHelper.set_unit_attribute_value(channel_obj, value)
            MayaUndoHelper.dg_modifier.doIt()
            return

        if c_mobj.hasFn(OpenMaya.MFn.kNumericAttribute):
            MayaFacadeHelper.set_numeric_attribute_value(channel_obj, value)
            MayaUndoHelper.dg_modifier.doIt()
            return

        if c_mobj.hasFn(OpenMaya.MFn.kEnumAttribute):
            MayaUndoHelper.dg_modifier.newPlugValueShort(channel_obj, value)
            MayaUndoHelper.dg_modifier.doIt()
            return

        if (c_mobj.hasFn(OpenMaya.MFn.kMatrixAttribute) or
                    c_mobj.hasFn(OpenMaya.MFn.kFloatMatrixAttribute)):
            matrix = OpenMaya.MMatrix(value)
            MayaUndoHelper.dg_modifier.newPlugValue(channel_obj,
                                        OpenMaya.MFnMatrixData().create(matrix))
            MayaUndoHelper.dg_modifier.doIt()
            return

        if (c_mobj.hasFn(OpenMaya.MFn.kFloatAngleAttribute) or
                c_mobj.hasFn(OpenMaya.MFn.kDoubleAngleAttribute)):
            MayaUndoHelper.dg_modifier.newPlugValueDouble(channel_obj, value)
            MayaUndoHelper.dg_modifier.doIt()
            return

        if c_mobj.hasFn(OpenMaya.MFn.kTypedAttribute):
            fn = OpenMaya.MFnTypedAttribute(c_mobj)
            if fn.attrType() == OpenMaya.MFnData.kString:
                MayaUndoHelper.dg_modifier.newPlugValueString(channel_obj,
                                                              value)
                MayaUndoHelper.dg_modifier.doIt()
                return

        raise FacadeRuntimeError("Could not set value on plug %s" %
                                 channel_obj.partialName(True))


    @staticmethod
    def support_hierarchy():
        return True

    @staticmethod
    def move_to_frame(frame):
        anim_control = OpenMayaAnim.MAnimControl()
        anim_control.setCurrentTime(OpenMaya.MTime(frame, OpenMaya.MTime.uiUnit()))

    @staticmethod
    def get_active_frame_range():
        anim_control = OpenMayaAnim.MAnimControl()
        return (anim_control.minTime().value(), anim_control.maxTime().value())

    @staticmethod
    def get_current_time():
        anim_control = OpenMayaAnim.MAnimControl()
        return anim_control.currentTime().value()

    @staticmethod
    def get_channel_object(node_obj, channel_name):
        return MayaFacadeHelper.find_plug(node_obj, channel_name)

    @staticmethod
    def get_keyframable_channel_object(node_obj, channel_obj,
                                       force_create=True):
        connections = OpenMaya.MPlugArray()
        channel_obj.connectedTo(connections, True, False)
        if bool(connections.length()):
            try:
                mfna = OpenMayaAnim.MFnAnimCurve(channel_obj)
                # check if the node is referenced. Support for unitless input
                # animation curves is not available yet
                allow_ref = MayaPreferences.use_referenced_anim_curves
                if ((not allow_ref and mfna.isFromReferencedFile()) or
                        mfna.isUnitlessInput()):
                    return None
                return mfna
            except:
                return None
        elif force_create:
            try:
                curve_node = OpenMayaAnim.MFnAnimCurve().create(channel_obj,
                                                     MayaUndoHelper.dg_modifier)
            except:
                warnings.warn("Cannot create animation curve node for %s ." %
                              channel_obj.partialName(True), FacadeWarning)
                return None

            return OpenMayaAnim.MFnAnimCurve(curve_node)
        return None

    @staticmethod
    def get_frame_range_from_channel(k_channel_obj):
        num_keys = k_channel_obj.numKeys()
        if num_keys < 1:
            return None

        return (k_channel_obj.time(0).value(),
                k_channel_obj.time(num_keys - 1).value())

    @staticmethod
    def set_channel_key_frame(k_channel_obj, time, value):
        t = OpenMaya.MTime(time, OpenMaya.MTime.uiUnit())

        if MayaFacadeHelper.is_angular_curve(k_channel_obj):
            value = math.radians(value)

        t_global = OpenMayaAnim.MFnAnimCurve.kTangentGlobal

        return k_channel_obj.addKey(t, value, t_global, t_global,
                                    MayaUndoHelper.anim_curve_change)

    @staticmethod
    def set_channel_key_frames_in_bulk(k_channel_obj, times, values):
        is_angular = MayaFacadeHelper.is_angular_curve(k_channel_obj)

        times_ = OpenMaya.MTimeArray()
        values_ = OpenMaya.MDoubleArray()
        for i in range(len(times)):
            values_.append(math.radians(values[i]) if is_angular else values[i])
            times_.append(OpenMaya.MTime(times[i], OpenMaya.MTime.uiUnit()))

        t_global = OpenMayaAnim.MFnAnimCurve.kTangentGlobal
        k_channel_obj.addKeys(times_, values_, t_global, t_global, False,
                              MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_fps():
        return MayaFacadeHelper.get_fps()

    @staticmethod
    def pre_import():
        if not cmds.pluginInfo('kikoUndoer', q=1, l=1):
            cmds.loadPlugin('kikoUndoer', quiet=True)

        MayaUndoHelper.anim_curve_change = OpenMayaAnim.MAnimCurveChange()
        MayaUndoHelper.dg_modifier = OpenMaya.MDGModifier()

    @staticmethod
    def post_import():
        cmds.kikoUndoer()


    @staticmethod
    def get_channel_num_keys(k_channel_obj):
        return k_channel_obj.numKeys()

    @staticmethod
    def get_channel_is_weighted(k_channel_obj):
        return k_channel_obj.isWeighted()

    @staticmethod
    def set_channel_is_weighted(k_channel_obj, value):
        return k_channel_obj.setIsWeighted(value,
                                           MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_pre_infinity(k_channel_obj):
        return MAYA_TO_KIKO_INFINITY_BEHAVIOR[k_channel_obj.preInfinityType()]

    @staticmethod
    def set_channel_pre_infinity(k_channel_obj, pre_infinity):
        k_channel_obj.setPreInfinityType(
                            KIKO_TO_MAYA_INFINITY_BEHAVIOR[pre_infinity],
                            MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_post_infinity(k_channel_obj):
        return MAYA_TO_KIKO_INFINITY_BEHAVIOR[k_channel_obj.postInfinityType()]

    @staticmethod
    def set_channel_post_infinity(k_channel_obj, post_inifinity):
        k_channel_obj.setPostInfinityType(
                            KIKO_TO_MAYA_INFINITY_BEHAVIOR[post_inifinity],
                            MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_in_tangent_type_at_index(k_channel_obj, index):
        return MAYA_TO_KIKO_TANGENT_TYPES[k_channel_obj.inTangentType(index)]

    @staticmethod
    def set_channel_in_tangent_type_at_index(k_channel_obj, index, in_type):
        return k_channel_obj.setInTangentType(index,
                                        KIKO_TO_MAYA_TANGENT_TYPES[in_type],
                                        MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_out_tangent_type_at_index(k_channel_obj, index):
        return MAYA_TO_KIKO_TANGENT_TYPES[k_channel_obj.outTangentType(index)]

    @staticmethod
    def set_channel_out_tangent_type_at_index(k_channel_obj, index, out_type):
        return k_channel_obj.setOutTangentType(index,
                                        KIKO_TO_MAYA_TANGENT_TYPES[out_type],
                                        MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index):
        angle = OpenMaya.MAngle()
        weight = OpenMaya.MScriptUtil()
        weight.createFromDouble(0.0)
        weight_ptr = weight.asDoublePtr()
        k_channel_obj.getTangent(index, angle, weight_ptr, False)
        return angle.asDegrees(), weight.getDouble(weight_ptr)

    @staticmethod
    def set_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        k_channel_obj.setWeight(index, weight, False,
                                MayaUndoHelper.anim_curve_change)

        k_channel_obj.setAngle(index, OpenMaya.MAngle(math.radians(angle)),
                               False, MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index):
        angle = OpenMaya.MAngle()
        weight = OpenMaya.MScriptUtil()
        weight.createFromDouble(0.0)
        weight_ptr = weight.asDoublePtr()
        k_channel_obj.getTangent(index, angle, weight_ptr, True)
        return angle.asDegrees(), weight.getDouble(weight_ptr)

    @staticmethod
    def set_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        k_channel_obj.setWeight(index, weight, True,
                                MayaUndoHelper.anim_curve_change)

        k_channel_obj.setAngle(index, OpenMaya.MAngle(math.radians(angle)),
                               True, MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_tangents_locked_at_index(k_channel_obj, index):
        return k_channel_obj.tangentsLocked(index)

    @staticmethod
    def set_channel_tangents_locked_at_index(k_channel_obj, index, value):
        return k_channel_obj.setTangentsLocked(index, value,
                                               MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_weights_locked_at_index(k_channel_obj, index):
        return k_channel_obj.weightsLocked(index)

    @staticmethod
    def set_channel_weights_locked_at_index(k_channel_obj, index, value):
        return k_channel_obj.setWeightsLocked(index, value,
                                              MayaUndoHelper.anim_curve_change)

    @staticmethod
    def get_channel_value_at_index(k_channel_obj, index):
        val = k_channel_obj.value(index)

        if k_channel_obj.animCurveType() in [
                                    OpenMayaAnim.MFnAnimCurve.kAnimCurveTA,
                                    OpenMayaAnim.MFnAnimCurve.kAnimCurveUA]:
            return math.degrees(val)
        return val

    @staticmethod
    def get_channel_time_at_index(k_channel_obj, index):
        return k_channel_obj.time(index).value()

    @staticmethod
    def get_channel_value_at_time(k_channel_obj, time):
        val = k_channel_obj.evaluate(OpenMaya.MTime(time))
        if k_channel_obj.animCurveType() in [
                                    OpenMayaAnim.MFnAnimCurve.kAnimCurveTA,
                                    OpenMayaAnim.MFnAnimCurve.kAnimCurveUA]:
            return math.degrees(val)
        return val

    @staticmethod
    def has_world_space_matrix(node_obj):
        try:
            OpenMaya.MFnTransform(node_obj)
            return True
        except RuntimeError:
            return False

    @staticmethod
    def get_world_space_rotation_and_translation(node_obj):
        # maya requires a MDagPath in order to build successfully a MFnTransform
        dp = OpenMaya.MDagPath()
        OpenMaya.MDagPath.getAPathTo(node_obj, dp)

        m_trans = OpenMaya.MFnTransform(dp)

        r = OpenMaya.MQuaternion()
        m_trans.getRotation(r, OpenMaya.MSpace.kWorld)

        t = m_trans.getTranslation(OpenMaya.MSpace.kWorld)
        t = MayaFacadeHelper.sanitize_translation_vector(t)

        return (r.x, r.y, r.z, r.w), (t.x, t.y, t.z)

    @staticmethod
    def set_world_space_rotation_and_translation_at_time(node_obj, time,
                                                         rotation, translation):
        # get parent matrix at the given time
        mfn = OpenMaya.MFnDependencyNode(node_obj)
        plug = mfn.findPlug("parentMatrix").elementByLogicalIndex(0)
        o = plug.asMObject(OpenMaya.MDGContext(OpenMaya.MTime(time)))
        m = MayaFacadeHelper.sanitize_matrix(OpenMaya.MFnMatrixData(o).matrix())
        parent_matrix = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList(m, parent_matrix)

        inv_parent_matrix = parent_matrix.inverse()

        # fiding rotation
        world_rotation = OpenMaya.MQuaternion(rotation[0], rotation[1],
                                              rotation[2], rotation[3])
        lm = world_rotation.asMatrix() * inv_parent_matrix
        r = OpenMaya.MTransformationMatrix(lm).eulerRotation()
        r.reorderIt(mfn.findPlug("rotateOrder").asInt())

        # finding translation
        world_translation = OpenMaya.MPoint(translation[0], translation[1],
                                             translation[2])
        t = world_translation * inv_parent_matrix

        # Setting values on node
        d = {'tx': t.x, 'ty': t.y, 'tz':t.z,
             'rx': math.degrees(r.x), 'ry': math.degrees(r.y),
             'rz':math.degrees(r.z)}

        for name, value in d.items():
            plug = mfn.findPlug(name)
            kco = MayaFacade.get_keyframable_channel_object(node_obj, plug)
            # this might happen when having incoming connectiosn to this plug
            if kco is None:
                continue
            MayaFacade.set_channel_key_frame(kco, time, value)

    @staticmethod
    def remove_animation_from_channel(node_obj, channel_obj):
        if MayaPreferences.break_all_connections_in_apply_mode:
            plugs = OpenMaya.MPlugArray()
            channel_obj.connectedTo(plugs, True, False)
            if channel_obj.connectedTo(plugs, True, False):
                for index in range(plugs.length()):
                    MayaUndoHelper.dg_modifier.disconnect(plugs[index],
                                                          channel_obj)

                    node_ = plugs[index].node()
                    if node_.apiType() in MayaFacadeHelper.AC_NODE_TYPES:
                        MayaUndoHelper.dg_modifier.deleteNode(node_)

            # it might be that the parent compound attribute is connected
            if channel_obj.isChild():
                p_plug = channel_obj.parent()
                MayaFacade.remove_animation_from_channel(node_obj, p_plug)

            MayaUndoHelper.dg_modifier.doIt()
        else:
            node = MayaFacadeHelper.get_connected_animation_curve(channel_obj)
            if node:
                MayaUndoHelper.dg_modifier.deleteNode(node)
                MayaUndoHelper.dg_modifier.doIt()

    @staticmethod
    def shift_animation_in_frame_range(node_obj, channel_obj, start, end):
        node = MayaFacadeHelper.get_connected_animation_curve(channel_obj)
        if node is None:
            return

        mfna = OpenMayaAnim.MFnAnimCurve(channel_obj)

        delta = end - start
        c_key = mfna.numKeys() - 1
        while c_key > 0 and mfna.time(c_key).value() >= start:
            ct = mfna.time(c_key).value()
            mfna.setTime(c_key, OpenMaya.MTime(ct + delta,
                                               OpenMaya.MTime.uiUnit()),
                         MayaUndoHelper.anim_curve_change)
            c_key -= 1

    @staticmethod
    def remove_animation_from_frame_range(node_obj, channel_obj, start, end):
        node = MayaFacadeHelper.get_connected_animation_curve(channel_obj)
        if node is None:
            return

        mfna = OpenMayaAnim.MFnAnimCurve(channel_obj)
        c_key = mfna.numKeys() - 1

        while c_key > 0 and mfna.time(c_key).value() >= start:
            if mfna.time(c_key).value() > end:
                c_key -= 1
                continue
            mfna.remove(c_key, MayaUndoHelper.anim_curve_change)
            c_key -= 1


