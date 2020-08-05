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

import math
import warnings
import tempfile

import nuke

from kiko.constants import (APPS, KIKO_PREVIEW_MAXIMUM_SIZE,
                            KIKO_INFINITY_BEHAVIOR)
from kiko.apps.basefacade import BaseFacade
from kiko.utils.value import floats_equal

from .constants import (KIKO_TO_NUKE_CHANNELS, NUKE_TO_KIKO_CHANNELS,
                        KIKO_TO_NUKE_TANGENT_TYPES, NUKE_TO_KIKO_TANGENT_TYPES,
                        NUKE_NODE_TO_KIKO_CHANNELS, KIKO_TO_NUKE_NODE_CHANNELS)
from .converters import get_kiko_to_nuke_converter, get_nuke_to_kiko_converter


class NukeFacadeHelper(object):

    @staticmethod
    def tangent_length(x_1, y_1, slope, b_val, x_2):
        x = x_1 + (x_2 - x_1) * b_val / 3
        y = slope * x_1 - slope * x + y_1
        return math.sqrt((x_1 - x) * (x_1 - x) + (y_1 - y) * (y_1 - y))

    @staticmethod
    def angle_from_slope(slope):
        return math.degrees(math.atan(slope))

    @staticmethod
    def tangent_length_from_angle_and_weight(w, a, key_x_1, key_x_2):
        value = (3 * math.fabs(math.cos(a)) * w / math.fabs(key_x_2 - key_x_1))
        #nuke accepts only tangents length from 0.0 and 3.0
        return max(min(value, 3.0), 0.0)

    @staticmethod
    def get_matrix_from_knob(knob):
        m_value = knob.valueAt(nuke.frame())
        m = nuke.math.Matrix4()
        for i in range(16):
            m[i] = m_value[i]
        m.transpose()
        return m

    @staticmethod
    def convert_to_euler(node, quaternion):
        rot_matrix = quaternion.matrix()
        ro = node['rot_order'].value()

        ro_method = {'XYZ': rot_matrix.rotationsXYZ,
                     'XZY': rot_matrix.rotationsXZY,
                     'YXZ': rot_matrix.rotationsYXZ,
                     'YZX': rot_matrix.rotationsYZX,
                     'ZXY': rot_matrix.rotationsZXY,
                     'ZYX': rot_matrix.rotationsZYX}
        rad_rot = ro_method[ro]()

        return [math.degrees(rad_rot[i]) for i in range(3)]


class NukeFacade(BaseFacade):
    INDEX_ATTR_MAP = ['X', 'Y', 'Z']
    TRANSFORM_CHANNELS = set(['translate', 'rotate', 'scale'])

    @staticmethod
    def get_app_name():
        return APPS.NUKE

    @staticmethod
    def get_selection():
        return nuke.selectedNodes()

    @staticmethod
    def supports_image_generation():
        return True

    @staticmethod
    def get_image_sources():
        return nuke.allNodes("Write")

    @staticmethod
    def generate_image_sequence(source, start_frame, end_frame, sample_every=1):
        #get the write node and find the original image size
        source_node = nuke.toNode(source)
        w = source_node.width()
        h = source_node.height()
        aspect_ratio = float(w) / float(h)

        if aspect_ratio < 1:
            h = KIKO_PREVIEW_MAXIMUM_SIZE
            w = int(KIKO_PREVIEW_MAXIMUM_SIZE * aspect_ratio)
        else:
            w = KIKO_PREVIEW_MAXIMUM_SIZE
            h = int(KIKO_PREVIEW_MAXIMUM_SIZE / aspect_ratio)

        #caching write node inputs and values
        previous_input = source_node.input(0)
        previous_path = source_node['file'].value()
        previous_ext = source_node['file_type'].value()

        #create a reformat node and connect the input of the write node
        reformat_node = nuke.createNode("Reformat")
        f = reformat_node['format'].value()
        f.setWidth(w)
        f.setHeight(h)

        if previous_input:
            reformat_node.setInput(0, previous_input)
        source_node.setInput(0, reformat_node)

        #setting up write node
        f_range = "%d-%d/%d" % ()
        _, path = tempfile.mkstemp()
        source_node['file'].setValue(path)
        source_node['file_type'].setValue('jpeg')

        #render
        nuke.execute(source_node, start_frame, end_frame, sample_every)

        #delete format node and reconnect everything
        nuke.delete(reformat_node)

        if previous_input:
            source_node.setInput(0, previous_input)
        source_node['file'].setValue(previous_path)
        source_node['file_type'].setValue(previous_ext)

    @staticmethod
    def get_node_by_name(node_name):
        return nuke.toNode(node_name)

    @staticmethod
    def map_kiko_channel_to_app_channel(node_obj, channel_name):
        node_map = KIKO_TO_NUKE_NODE_CHANNELS.get(node_obj.Class())
        if node_map and channel_name in node_map:
            return node_map.get(channel_name)
        return KIKO_TO_NUKE_CHANNELS.get(channel_name) or channel_name

    @staticmethod
    def map_app_channel_to_kiko_channel(node_obj, channel_name):
        node_map = NUKE_NODE_TO_KIKO_CHANNELS.get(node_obj.Class())
        if node_map and channel_name in node_map:
            return node_map.get(channel_name)
        return NUKE_TO_KIKO_CHANNELS.get(channel_name) or channel_name

    @staticmethod
    def get_name(node_obj):
        return node_obj.name()

    @staticmethod
    def get_selected_channel_names():
        raise NotImplementedError()

    @staticmethod
    def list_channels(node_obj, factor=3):
        invalid_knob_types = (nuke.ColorChip_Knob,)

        #world matrix is in this list as for some reason nuke thinks it is
        #always enabled while it's not. We never want to edit it
        invalid_knob_names = ['xpos', 'ypos', 'selected', 'postage_stamp',
                              'bookmark', 'note_font_size', 'dope_sheet',
                              'hide_input', 'note_font_color', 'world_matrix',
                              'cached', 'postage_stamp_frame']

        channels = []
        for k in node_obj.allKnobs():
            if (not k.enabled() or not k.visible()
                    or not isinstance(k, nuke.Array_Knob)
                    or isinstance(k, invalid_knob_types)
                    or k.name() in invalid_knob_names):
                continue

            for i in range(k.arraySize()):
                channels.append((k, i))

        return channels

    @staticmethod
    def is_channel_animated(node_obj, channel_obj):
        knob = channel_obj[0]
        index = channel_obj[1]

        return knob.isAnimated(index) or knob.getNumKeys(index) > 0

    @staticmethod
    def is_channel_connected(node_obj, channel_obj):
        if NukeFacade.is_channel_animated(node_obj, channel_obj):
            return True

        knob = channel_obj[0]
        index = channel_obj[1]
        return knob.hasExpression(index)

    @staticmethod
    def get_channel_name(node_obj, channel_obj):
        knob = channel_obj[0]
        index = channel_obj[1]
        return knob.name() + '[' + str(index) + ']'

    @staticmethod
    def get_channel_value(node_obj, channel_obj):
        knob = channel_obj[0]
        index = channel_obj[1]

        val = knob.getValue(index, nuke.thisView(), nuke.frame())

        if isinstance(knob, nuke.Enumeration_Knob):
            return int(val)
        if isinstance(knob, nuke.Boolean_Knob):
            return bool(val)

        converter = get_nuke_to_kiko_converter(node_obj, knob)
        if converter:
            val = converter(node_obj, knob, index, val)

        return val

    @staticmethod
    def set_channel_value(node_obj, channel_obj, value):
        knob = channel_obj[0]
        index = channel_obj[1]
        
        converter = get_kiko_to_nuke_converter(node_obj, knob)
        if converter:
            value = converter(node_obj, knob, index, value)

        if index == 0:
            knob.setValue(value)
        else:
            knob.setValue(value, index)

    @staticmethod
    def support_hierarchy():
        return False

    @staticmethod
    def move_to_frame(frame):
        nuke.frame(frame)

    @staticmethod
    def get_active_frame_range():
        r = nuke.Root()
        return (r.knob('first_frame').value(), r.knob('last_frame').value())

    @staticmethod
    def get_current_time():
        return nuke.frame()

    @staticmethod
    def get_channel_object(node_obj, channel_name):
        try:
            i = channel_name.index('[')
            index = int(channel_name[i + 1:-1])
        except ValueError:
            i = len(channel_name)
            index = 0

        knob = node_obj.knob(channel_name[:i])
        if knob:
            return knob, index

    @staticmethod
    def get_keyframable_channel_object(node_obj, channel_obj,
                                       force_create=True):
        knob = channel_obj[0]
        index = channel_obj[1]

        if NukeFacade.is_channel_animated(node_obj, channel_obj):
            return knob.animation(index)
        elif force_create:
            knob.clearAnimated(index)
            knob.setAnimated(index)
            return knob.animation(index)

        return None

    @staticmethod
    def get_frame_range_from_channel(k_channel_obj):
        keys = k_channel_obj.keys()
        return keys[0].x, keys[-1].x

    @staticmethod
    def set_channel_key_frame(k_channel_obj, time, value):
        keys = k_channel_obj.keys()

        knob = k_channel_obj.knob()
        node_obj = knob.node()
        converter = get_kiko_to_nuke_converter(node_obj, knob)
        if converter:
            index = k_channel_obj.knobIndex()
            value = converter(node_obj, knob, index, value, t=time)

        k_channel_obj.setKey(time, value)

        #This is ugly, but there is no way to find a key index with nuke python
        #TODO: use getKeyIndex from Array_Knob instead
        if len(keys) == 0:
            return 0

        for i in range(len(keys)):
            if time <= keys[i].x:
                return i

        return len(keys)

    @staticmethod
    def set_channel_key_frames_in_bulk(k_channel_obj, times, values):
        knob = k_channel_obj.knob()
        node_obj = knob.node()
        converter = get_kiko_to_nuke_converter(node_obj, knob)
        if converter:
            index = k_channel_obj.knobIndex()
            keys = [nuke.AnimationKey(times[i],
                                      converter(node_obj, knob, index,
                                                values[i], t=times[i]))
                    for i in range(times)]
        else:
            keys = [nuke.AnimationKey(times[i], values[i])
                    for i in range(len(times))]

        k_channel_obj.addKey(keys)

    @staticmethod
    def get_fps():
        return nuke.Root()['fps'].value()

    @staticmethod
    def pre_import():
        pass

    @staticmethod
    def post_import():
        pass

    @staticmethod
    def get_channel_num_keys(k_channel_obj):
        return k_channel_obj.size()

    @staticmethod
    def get_channel_is_weighted(k_channel_obj):
        for k in k_channel_obj.keys():
            if k.ra != 1.0 or k.la != 1.0:
                return True
        return False

    @staticmethod
    def set_channel_is_weighted(k_channel_obj, value):
        pass

    @staticmethod
    def get_channel_pre_infinity(k_channel_obj):
        key = k_channel_obj.keys()[0]
        if key.extrapolation == nuke.CONSTANT:
            return KIKO_INFINITY_BEHAVIOR.CONSTANT
        else:
            return KIKO_INFINITY_BEHAVIOR.LINEAR

    @staticmethod
    def set_channel_pre_infinity(k_channel_obj, pre_infinity):
        key = k_channel_obj.keys()[0]
        if pre_infinity == KIKO_INFINITY_BEHAVIOR.CONSTANT:
            key.extrapolation = nuke.CONSTANT
        else:
            key.extrapolation = nuke.LINEAR

    @staticmethod
    def get_channel_post_infinity(k_channel_obj):
        # check the last key and find the after
        key = k_channel_obj.keys()[-1]
        if key.extrapolation == nuke.CONSTANT:
            return KIKO_INFINITY_BEHAVIOR.CONSTANT
        else:
            return KIKO_INFINITY_BEHAVIOR.LINEAR

    @staticmethod
    def set_channel_post_infinity(k_channel_obj, post_inifinity):
        key = k_channel_obj.keys()[-1]
        if post_inifinity == KIKO_INFINITY_BEHAVIOR.CONSTANT:
            key.extrapolation = nuke.CONSTANT
        else:
            key.extrapolation = nuke.LINEAR

    @staticmethod
    def get_channel_in_tangent_type_at_index(k_channel_obj, index):
        key = k_channel_obj.keys()[index]
        return NUKE_TO_KIKO_TANGENT_TYPES[key.interpolation]

    @staticmethod
    def set_channel_in_tangent_type_at_index(k_channel_obj, index, in_type):
        # interpolation is just one value, there's no in and out in nuke.
        # This is why, we just set the out tangent type.
        pass

    @staticmethod
    def get_channel_out_tangent_type_at_index(k_channel_obj, index):
        key = k_channel_obj.keys()[index]
        return NUKE_TO_KIKO_TANGENT_TYPES[key.interpolation]

    @staticmethod
    def set_channel_out_tangent_type_at_index(k_channel_obj, index, out_type):
        key = k_channel_obj.keys()[index]
        interpolation = KIKO_TO_NUKE_TANGENT_TYPES.get(out_type) or nuke.SMOOTH
        key.interpolation = interpolation

    @staticmethod
    def get_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index):
        keys = k_channel_obj.keys()
        k = keys[index]
        if index == len(keys) - 1:
            return 0, 1

        weight = NukeFacadeHelper.tangent_length(k.x, k.y, k.rslope, k.ra,
                                                 keys[index + 1].x)
        return NukeFacadeHelper.angle_from_slope(k.rslope), weight

    @staticmethod
    def set_channel_out_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        keys = k_channel_obj.keys()
        k = keys[index]
        a = math.radians(angle)

        k.rslope = math.tan(a)

        if index < len(keys) - 1:
            k.ra = NukeFacadeHelper.tangent_length_from_angle_and_weight(weight,
                                                a, k.x, keys[index + 1].x)

    @staticmethod
    def get_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index):
        keys = k_channel_obj.keys()
        k = keys[index]
        if index == 0:
            return 0, 1

        weight = NukeFacadeHelper.tangent_length(k.x, k.y, k.lslope, k.la,
                                                 keys[index - 1].x)
        return NukeFacadeHelper.angle_from_slope(k.lslope), weight

    @staticmethod
    def set_channel_in_tangent_angle_and_weight_at_index(k_channel_obj, index,
                                                          angle, weight):
        keys = k_channel_obj.keys()
        k = keys[index]
        a = math.radians(angle)

        k.lslope = math.tan(a)

        if index > 0:
            k.la = NukeFacadeHelper.tangent_length_from_angle_and_weight(weight,
                                                a, k.x, keys[index - 1].x)

    @staticmethod
    def get_channel_tangents_locked_at_index(k_channel_obj, index):
        k = k_channel_obj.keys()[index]
        return floats_equal(NukeFacadeHelper.angle_from_slope(k.lslope),
                             NukeFacadeHelper.angle_from_slope(k.rslope),
                             places=5)

    @staticmethod
    def set_channel_tangents_locked_at_index(k_channel_obj, index, value):
        pass

    @staticmethod
    def get_channel_weights_locked_at_index(k_channel_obj, index):
        k = k_channel_obj.keys()[index]
        return floats_equal(NukeFacadeHelper.angle_from_slope(k.la),
                             NukeFacadeHelper.angle_from_slope(k.ra),
                             places=5)

    @staticmethod
    def set_channel_weights_locked_at_index(k_channel_obj, index, value):
        pass

    @staticmethod
    def get_channel_value_at_index(k_channel_obj, index):
        knob = k_channel_obj.knob()
        node_obj = knob.node()
        
        converter = get_nuke_to_kiko_converter(node_obj, knob)
        value = k_channel_obj.keys()[index].y
        if converter:
            value = converter(node_obj, knob, index, value)
        return value

    @staticmethod
    def get_channel_time_at_index(k_channel_obj, index):
        return k_channel_obj.keys()[index].x

    @staticmethod
    def get_channel_value_at_time(k_channel_obj, time):
        knob = k_channel_obj.knob()
        index = k_channel_obj.knobIndex()
        node_obj = knob.node()
    
        converter = get_nuke_to_kiko_converter(node_obj, knob)
        value = k_channel_obj.evaluate(time)
        if converter:
            value = converter(node_obj, knob, index, value)
        return value

    @staticmethod
    def has_world_space_matrix(node_obj):
        return "matrix" in node_obj.knobs()

    @staticmethod
    def get_world_space_rotation_and_translation(node_obj):
        knob = node_obj.knob('matrix')

        rm = NukeFacadeHelper.get_matrix_from_knob(knob)
        tm = nuke.math.Matrix4(rm)

        tm.translationOnly()
        t = tm.translation()

        rm.rotationOnly()
        r = nuke.math.Quaternion(rm)

        return (r.vx, r.vy, r.vz, r.s), t

    @staticmethod
    def set_world_space_rotation_and_translation_at_time(node_obj, time,
                                                         rotation, translation):
        q = nuke.math.Quaternion(rotation[3], *rotation[:3])
        rot = NukeFacadeHelper.convert_to_euler(node_obj, q)

        k = node_obj.knobs('useMatrix')
        if k:
            k.setValue(False)

        knob_values = {'translate': translation, 'rotate': rot}
        for kn, kv in knob_values.items():
            knob = node_obj[kn]

            if not knob.isAnimated():
                knob.setAnimated(True)

            for i in range(knob.arraySize()):
                knob.setValueAt(kv[i], time, i)

    @staticmethod
    def remove_animation_from_channel(node_obj, channel_obj):
        knob = channel_obj[0]
        index = channel_obj[1]

        knob.clearAnimated(index)


    @staticmethod
    def shift_animation_in_frame_range(node_obj, channel_obj, start, end):
        animation = NukeFacade.get_keyframable_channel_object(node_obj,
                                                              channel_obj,
                                                              force_create=False)
        if animation is None:
            return

        delta = end - start
        keys = animation.keys()
        c_key = len(keys) - 1
        while c_key > 0 and keys[c_key].x >= start:
            keys[c_key].x += delta
            c_key -= 1

    @staticmethod
    def remove_animation_from_frame_range(node_obj, channel_obj, start, end):
        animation = NukeFacade.get_keyframable_channel_object(node_obj,
                                                              channel_obj,
                                                              force_create=False)
        if animation is None:
            return

        keys = animation.keys()
        c_key = len(keys) - 1

        keys_to_remove = []
        while c_key > 0 and keys[c_key].x >= start:
            if keys[c_key].x > end:
                c_key -= 1
                continue
            keys_to_remove.append(keys[c_key])
            c_key -= 1

        if keys_to_remove:
            animation.removeKey(keys_to_remove)

    @staticmethod
    def post_import_keyframable_channel_object(k_channel_obj):
        # in this function we set the animation knob with TCL as nuke will
        # forget everything about the curve tangents unless we do this.
        # Nuke python API provides now the the changeInterpolation method, but
        # it's tricky to get the desired result by post-setting the tangent
        # types

        knob = k_channel_obj.knob()
        index = k_channel_obj.knobIndex()

        itc = {nuke.CONSTANT: 'K', nuke.LINEAR: 'L', nuke.SMOOTH: 'S',
               nuke.HORIZONTAL: 'C k', nuke.CUBIC: 'C', nuke.BREAK: 'L',
               nuke.CATMULL_ROM: 'R', nuke.USER_SET_SLOPE: 'S'}

        keys = k_channel_obj.keys()

        index_script = 'curve'

        for i in range(len(keys)):
            k = keys[i]
            k.la = 1.0 if k.la == 0.0 else k.la
            k.ra = 1.0 if k.ra == 0.0 else k.ra

            index_script += (" " + itc[k.interpolation]
                             if k.interpolation in itc else " S")

            if i in [0, len(keys) - 1] and k.extrapolation == nuke.LINEAR:
                index_script += ' l'

            index_script += ' x' + ' '.join([str(k.x), str(k.y)])

            if k.interpolation != nuke.CONSTANT:
                if i == 0:
                    if 0 < k.ra < 3:
                        if (not floats_equal(k.lslope, k.rslope, places=5) and
                                k.extrapolation == nuke.CONSTANT):
                            index_script += ' ' + ' '.join(['s' + str(k.lslope),
                                                            't' + str(k.rslope),
                                                            'u' + str(k.la),
                                                            'v' + str(k.ra)])
                        else:
                            index_script += ' ' + ' '.join(['s' + str(k.rslope),
                                                        'u' + str(k.ra)])
                elif i == len(keys) - 1:
                    if 0 < k.la < 3:
                        index_script += ' ' + ' '.join(['s' + str(k.lslope),
                                                        'u' + str(k.la)])
                        if (not floats_equal(k.lslope, k.rslope, places=5) and
                                k.extrapolation == nuke.CONSTANT):
                            index_script += ' ' + ' '.join(['t' + str(k.rslope),
                                                            'v' + str(k.ra)])
                else:
                    if 0 < k.la < 3 and 0 < k.ra < 3:
                        if floats_equal(k.lslope, k.rslope, places=5):
                            index_script += ' s' + str(k.lslope)
                            index_script += ' ' + ' '.join(['u' + str(k.la),
                                                            'v' + str(k.ra)])
                        else:
                            index_script += ' ' + ' '.join(['s' + str(k.lslope),
                                                            't' + str(k.rslope),
                                                            'u' + str(k.la),
                                                            'v' + str(k.ra)])
        scripts = []
        for t in knob.toScript().split('{'):
            if t == '':
                continue

            tts = t.split('}') if '}' in t else t.split(' ')
            for i in tts:
                if i == '' or i.isspace():
                    continue
                scripts.append(i)

        scripts[index] = index_script
        for i in range(len(scripts)):
            if not unicode(scripts[i].replace(" ", "")).isnumeric():
                scripts[i] = '{' + scripts[i] + '}'

        knob.fromScript(" ".join(scripts))

    @staticmethod
    def pre_export_keyframable_channel_object(k_channel_obj):
        # fixing broken tangents before exporting the knob animation, this is
        # necessary in batch mode
        if not nuke.GUI:
            k_channel_obj.fixSlopes()


