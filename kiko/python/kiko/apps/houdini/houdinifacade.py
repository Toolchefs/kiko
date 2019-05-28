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
import math
import warnings
import tempfile

import hou

from kiko.constants import APPS, KIKO_PREVIEW_MAXIMUM_SIZE
from kiko.exceptions import FacadeRuntimeError, FacadeWarning
from kiko.apps.basefacade import BaseFacade

from .constants import (HOU_TO_KIKO_CHANNELS, KIKO_TO_HOU_CHANNELS,
                        KIKO_TO_HOU_INFINITY_BEHAVIOR,
                        HOU_TO_KIKO_INFINITY_BEHAVIOR,
                        KIKO_TO_HOU_TANGENT_TYPES, HOU_TO_KIKO_TANGENT_TYPES)

from houdinipreferences import HoudiniPreferences


class HoudiniFacade(BaseFacade):

    @staticmethod
    def get_app_name():
        return APPS.HOUDINI

    @staticmethod
    def get_selection():
        return [s for s in hou.selectedNodes() if isinstance(s, hou.ObjNode)]

    @staticmethod
    def supports_image_generation():
        return False

    @staticmethod
    def get_image_sources():
        pass

    @staticmethod
    def generate_image_sequence(source, start_frame, end_frame, sample_every=1):
        pass

    @staticmethod
    def get_node_by_name(node_name):
        return hou.node(node_name) or hou.node("/obj/" + node_name)

    @staticmethod
    def map_kiko_channel_to_app_channel(node_obj, channel_name):
        return KIKO_TO_HOU_CHANNELS.get(channel_name) or channel_name

    @staticmethod
    def map_app_channel_to_kiko_channel(node_obj, channel_name):
        return HOU_TO_KIKO_CHANNELS.get(channel_name) or channel_name

    @staticmethod
    def get_name(node_obj):
        if HoudiniPreferences.use_full_paths:
            return node_obj.path()
        return node_obj.name()

    @staticmethod
    def get_selected_channel_names():
        raise NotImplementedError()

    @staticmethod
    def list_channels(node_obj):
        parm_objs = []
        
        allowed_types = [hou.parmData.Int, hou.parmData.Float]
        for parm in node_obj.parms():
            if parm.parmTemplate().dataType() not in allowed_types:
                continue
            parm_objs.append(parm)

        return parm_objs

    @staticmethod
    def is_channel_animated(node_obj, channel_obj):
        return len(channel_obj.keyframes()) > 0

    @staticmethod
    def is_channel_connected(node_obj, channel_obj):
        return channel_obj.isTimeDependent() or channel_obj.isConstrained()

    @staticmethod
    def get_children(node_obj):
        return node_obj.outputs()

    @staticmethod
    def get_channel_name(node_obj, channel_obj):
        return channel_obj.name()

    @staticmethod
    def get_channel_value(node_obj, channel_obj):
        return channel_obj.eval()

    @staticmethod
    def set_channel_value(node_obj, channel_obj, value):
        channel_obj.set(value)

    @staticmethod
    def support_hierarchy():
        return True

    @staticmethod
    def move_to_frame(frame):
        hou.hscript("fcur %d" % frame)
        hou.hscript("updateui")

    @staticmethod
    def get_active_frame_range():
        r = hou.playbar.playbackRange()
        return (r[0], r[1])

    @staticmethod
    def get_current_time():
        return hou.intFrame()

    @staticmethod
    def get_channel_object(node_obj, channel_name):
        return node_obj.parm(channel_name)

    @staticmethod
    def get_keyframable_channel_object(node_obj, channel_obj,
                                       force_create=True):
        return channel_obj

    @staticmethod
    def get_frame_range_from_channel(k_channel_obj):
        keys = k_channel_obj.keyframes()
        return keys[0].frame(), keys[-1].frame()

    @staticmethod
    def set_channel_key_frame(k_channel_obj, time, value):
        k = hou.Keyframe()
        k.setFrame(time)
        k.setValue(value)
        k_channel_obj.setKeyframe(k)
        keys = k_channel_obj.keyframes()
        for i in range(len(keys)):
            if keys[i].frame() == time:
                return i

    @staticmethod
    def set_channel_key_frames_in_bulk(k_channel_obj, times, values):
        keys = []
        for i in range(len(times)):
            k = hou.Keyframe()
            k.setFrame(times[i])
            k.setValue(values[i])
            keys.append(k)
        k_channel_obj.setKeyframes(keys)

    @staticmethod
    def get_fps():
        return hou.fps()

    @staticmethod
    def pre_import():
        pass

    @staticmethod
    def post_import():
        pass

    @staticmethod
    def get_channel_num_keys(k_channel_obj):
        return len(k_channel_obj.keyframes())

    @staticmethod
    def get_channel_is_weighted(k_channel_obj):
        for k in k_channel_obj.keyframes():
            if k.isAccelSet():
                return True
        return False

    @staticmethod
    def set_channel_is_weighted(k_channel_obj, value):
        pass

    @staticmethod
    def get_channel_pre_infinity(k_channel_obj):
        if hou.applicationVersion()[0] <= 14:
            return
        
        return HOU_TO_KIKO_INFINITY_BEHAVIOR[k_channel_obj.keyframeExtrapolation(True)]

    @staticmethod
    def set_channel_pre_infinity(k_channel_obj, pre_infinity):
        if hou.applicationVersion()[0] <= 14:
            return
        
        k_channel_obj.setKeyframeExtrapolation(True,
                            KIKO_TO_HOU_INFINITY_BEHAVIOR[pre_infinity])

    @staticmethod
    def get_channel_post_infinity(k_channel_obj):
        if hou.applicationVersion()[0] <= 14:
            return
        
        return HOU_TO_KIKO_INFINITY_BEHAVIOR[k_channel_obj.keyframeExtrapolation(False)]

    @staticmethod
    def set_channel_post_infinity(k_channel_obj, post_inifinity):
        if hou.applicationVersion()[0] <= 14:
            return

        k_channel_obj.setKeyframeExtrapolation(False,
                            KIKO_TO_HOU_INFINITY_BEHAVIOR[post_inifinity])

    @staticmethod
    def get_channel_in_tangent_type_at_index(k_channel_obj, index):
        k = k_channel_obj.keyframes()[index]
        return HOU_TO_KIKO_TANGENT_TYPES[k.expression()]

    @staticmethod
    def set_channel_in_tangent_type_at_index(k_channel_obj, index, in_type):
        k = k_channel_obj.keyframes()[index]
        k.setExpression(KIKO_TO_HOU_TANGENT_TYPES[in_type])
        k_channel_obj.setKeyframe(k)

    @staticmethod
    def get_channel_out_tangent_type_at_index(k_channel_obj, index):
        k = k_channel_obj.keyframes()[index]
        return HOU_TO_KIKO_TANGENT_TYPES[k.expression()]

    @staticmethod
    def set_channel_out_tangent_type_at_index(k_channel_obj, index, out_type):
        k = k_channel_obj.keyframes()[index]
        k.setExpression(KIKO_TO_HOU_TANGENT_TYPES[out_type])
        k_channel_obj.setKeyframe(k)

    @staticmethod
    def get_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index):
        k = k_channel_obj.keyframes()[index]
        s = k.slope()
        angle = math.atan2(s, hou.fps())
        a = k.accel()
        
        w = math.sqrt((a * a * (hou.fps() * hou.fps() + s * s)) / (s * s + 1))
        
        return math.degrees(a), w

    @staticmethod
    def set_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        k = k_channel_obj.keyframes()[index]
        s = hou.fps() * math.tan(math.radians(angle))
        k.setSlope(s)
        
        if weight != 1.0:
            k_channel_obj.setKeyframe(k)
            k.setExpression("bezier()")
            a = math.sqrt((weight * weight * (s * s + 1)) / (
                    hou.fps() * hou.fps() + s * s))
            k.setAccel(a)

        k_channel_obj.setKeyframe(k)

        k = k_channel_obj.keyframes()[index]

    @staticmethod
    def get_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index):
        k = k_channel_obj.keyframes()[index]
        s = k.inSlope()
        angle = math.atan2(s, hou.fps())
        a = k.inAccel()
    
        w = math.sqrt((a * a * (hou.fps() * hou.fps() + s * s)) / (s * s + 1))
    
        return math.degrees(a), w

    @staticmethod
    def set_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        k = k_channel_obj.keyframes()[index]
        s = hou.fps() * math.tan(math.radians(angle))
        k.setInSlope(s)

        if weight != 1.0:
            k_channel_obj.setKeyframe(k)
            k.setExpression("bezier()")
            a = math.sqrt((weight * weight * (s * s + 1)) / (
                    hou.fps() * hou.fps() + s * s))
            k.setInAccel(a)
            
        k_channel_obj.setKeyframe(k)

        k = k_channel_obj.keyframes()[index]

    @staticmethod
    def get_channel_tangents_locked_at_index(k_channel_obj, index):
        k = k_channel_obj.keyframes()[index]
        return k.isSlopeSet() and k.slope() != k.inSlope()

    @staticmethod
    def set_channel_tangents_locked_at_index(k_channel_obj, index, value):
        pass

    @staticmethod
    def get_channel_weights_locked_at_index(k_channel_obj, index):
        k = k_channel_obj.keyframes()[index]
        return k.slope() == k.inSlope()

    @staticmethod
    def set_channel_weights_locked_at_index(k_channel_obj, index, value):
        pass

    @staticmethod
    def get_channel_value_at_index(k_channel_obj, index):
       return k_channel_obj.keyframes()[index].value()

    @staticmethod
    def get_channel_time_at_index(k_channel_obj, index):
        return k_channel_obj.keyframes()[index].frame()

    @staticmethod
    def get_channel_value_at_time(k_channel_obj, time):
        if k_channel_obj.parmTemplate().dataType() == hou.parmData.Float:
            return k_channel_obj.evalAsFloatAtFrame(time)
        elif k_channel_obj.parmTemplate().dataType() == hou.parmData.Int:
            return k_channel_obj.evalAsIntAtFrame(time)

    @staticmethod
    def has_world_space_matrix(node_obj):
        return isinstance(node_obj, hou.ObjNode)

    @staticmethod
    def get_world_space_rotation_and_translation(node_obj):
        wm = node_obj.worldTransform()

        q = hou.Quaternion()
        q.setToRotationMatrix(wm)

        return (q[0], q[1], q[2], q[3]), (wm.at(3, 0), wm.at(3, 1), wm.at(3, 2))

    @staticmethod
    def set_world_space_rotation_and_translation_at_time(node_obj, time,
                                                         rotation, translation):
        q = hou.Quaternion()
        q[0] = rotation[0]
        q[1] = rotation[1]
        q[2] = rotation[2]
        q[3] = rotation[3]
        
        m3 = q.extractRotationMatrix3()
        m4 = hou.Matrix4()
        
        for r in range(3):
            for c in range(3):
                m4.setAt(r, c, m3.at(r, c))
                
        m4.setAt(3, 0, translation[0])
        m4.setAt(3, 1, translation[1])
        m4.setAt(3, 2, translation[2])
        
        node_obj.setWorldTransform(m4)
        
        parms = ["tx", "ty", "tz", "rx", "ry", "rz"]
        for p in parms:
            parm = node_obj.parm(p)
            v = parm.eval()

            k = hou.Keyframe()
            k.setFrame(time)
            k.setValue(v)
            parm.setKeyframe(k)
        
    @staticmethod
    def remove_animation_from_channel(node_obj, channel_obj):
        channel_obj.deleteAllKeyframes()

    @staticmethod
    def shift_animation_in_frame_range(node_obj, channel_obj, start, end):
        if not channel_obj.keyframes():
            return

        delta = end - start
        keys = channel_obj.keyframes()
        c_key = len(keys) - 1
        while c_key > 0 and keys[c_key].x >= start:
            keys[c_key].setFrame(delta + keys[c_key].frame())
            c_key -= 1

    @staticmethod
    def remove_animation_from_frame_range(node_obj, channel_obj, start, end):
        if not channel_obj.keyframes():
            return

        keys_to_remove = channel_obj.keyframesInRange(start, end)
        frames = [k.frame() for k in keys_to_remove]

        for f in frames:
            channel_obj.deleteKeyframeAtFrame(f)


