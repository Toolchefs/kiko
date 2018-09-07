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
import tempfile
import random
import warnings

#suppressing the warnings here in the unit tests
warnings.simplefilter("ignore")

from nose.tools import (assert_false, assert_true, assert_equal, assert_raises,
                        assert_greater)

from maya import cmds

from kiko.apps.maya import manager
from kiko.apps.maya.mayapreferences import MayaPreferences
from kiko.utils.value import floats_equal
from kiko.constants import (IMPORT_METHODS, KIKO_FILE_EXTENSION,
                            KB_FILE_EXTENSION)
from kiko.exceptions import KikoManagerException
from kiko.operators.worldspaceoperator import worldspaceoperator
from kiko.operators.staticoperator import staticoperator
from kiko.operators.bakeoperator import bakeoperator
from kiko.operators.factory import OperatorsFactory

from fixtures import get_app_file, get_kiko_file

KIKO_APP_NAME = os.environ['KIKO_APP_NAME']
CHANNEL_OPERATOR_NAMES = OperatorsFactory().get_channel_operator_names(
                                                                KIKO_APP_NAME)

TRANSFORM_ATTR = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]


class TestMaya(object):

    def setUp(self):
        self._manager = manager.MayaKikoManager()
        _, self._kiko_file = tempfile.mkstemp(suffix=KIKO_FILE_EXTENSION)
        _, self._kb_file = tempfile.mkstemp(suffix=KB_FILE_EXTENSION)

        cmds.file(f=True, new=True)

    def tearDown(self):
        # this fails on windows, commenting it out for now
        # os.unlink(self._kiko_file)
        # os.unlink(self._kb_file)
        pass

    def _export_and_duplicate_hierarchy(self, file_, rename_children=False):
        cmds.file(get_app_file(KIKO_APP_NAME, 'locators_hierarchy.ma'),
                  force=True, open=True, options='v=0;')
        cmds.select("parent")

        self._manager.export_to_file(file_, objects=['parent'], hierarchy=True)

        if rename_children:
            cmds.duplicate(rr=True, renameChildren=True)
        else:
            cmds.duplicate(rr=True)

    def _compare_children(self, parent1, parent2, repl=None):
        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)

        children = cmds.listRelatives(parent1, ad=True, f=True, typ='transform')

        for i in  range(int(min), int(max)):
            cmds.currentTime(i)
            for c in children:

                #skipping joints
                if cmds.nodeType(c) == 'joint':
                    continue

                other_c = c.replace(parent1, parent2)
                if repl:
                    for r in repl:
                        other_c = other_c.replace(r[0], r[1])
                for a in list(set(cmds.listAttr(c, k=True, m=True) or []) |
                              set(cmds.listAttr(c, cb=True, m=True) or [])):

                    #making sure the attribute exist, some special nodes may
                    #create attributes/children when attrs are listed.
                    if not cmds.objExists(other_c + '.' + a):
                        continue

                    #if the object is connected to something other than an
                    #anim curve then we skip it
                    if bool([j for j in
                              cmds.listConnections(other_c + '.' + a) or []
                              if not "animCurve" in cmds.nodeType(j, i=True)]):
                        continue

                    val1 = cmds.getAttr(c + "." + a)
                    val2 = cmds.getAttr(other_c + '.' + a)

                    if isinstance(val1, float):
                        assert_true(floats_equal(val1, val2))
                    else:
                        assert_equal(val1, val2)

    def _create_and_animate_locator(self, frame_range=None, factor=3):
        if frame_range is None:
            frame_range = [int(cmds.playbackOptions(q=True, minTime=True)),
                           int(cmds.playbackOptions(q=True, maxTime=True))]

        l = cmds.spaceLocator()[0]

        for attr in TRANSFORM_ATTR:
            if factor == 1:
                num_keys = frame_range[1] - frame_range[0]
            else:
                num_keys = random.randint(3, (frame_range[1] - frame_range[0]) /
                                      factor)
            for i in range(num_keys):
                frame = random.randint(frame_range[0], frame_range[1])
                value = random.randint(-100, 100)
                cmds.setKeyframe(l + attr, v=value, time=frame)
            value = random.randint(-100, 100)
            #making sure there's a keyframe at the begining and end of animation
            cmds.setKeyframe(l + attr, v=value, time=frame_range[0])
            cmds.setKeyframe(l + attr, v=value, time=frame_range[1])

        return l


    def _export_import_simple_file_test_shared(self, file_):
        cmds.file(get_app_file(KIKO_APP_NAME, 'simple_locator.ma'),
                  force=True, open=True, options='v=0;')
        cmds.select("locator1")

        self._manager.export_to_file(file_)

        l = cmds.spaceLocator()
        obj_mapping = {'locator1': l[0]}

        self._manager.import_from_file(file_, objects=l,
                                       obj_mapping=obj_mapping,
                                       ignore_item_chunks=True)

        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)

        for i in  range(int(min), int(max)):
            cmds.currentTime(i)
            for attr in TRANSFORM_ATTR:
                assert_true(floats_equal(cmds.getAttr("locator1" + attr),
                                          cmds.getAttr(l[0] + attr)))

    def export_import_simple_kiko_file_test(self):
        self._export_import_simple_file_test_shared(self._kiko_file)

    def export_import_simple_kb_file_test(self):
        self._export_import_simple_file_test_shared(self._kb_file)

    def _export_import_hierarchy_test_shared(self, file_):
        self._export_and_duplicate_hierarchy(file_)

        self._manager.import_from_file(file_, objects=['parent1'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True)

        self._compare_children("parent", "parent1")

        #the curve operator should have just created one single key per attr on
        #childBBB
        child_bbb = "|parent1|childB|childBB|childBBB"
        for a in TRANSFORM_ATTR:
            assert_true(cmds.keyframe(child_bbb + a, q=True, kc=True) == 1)

        #the bake operator should have created a key frame per frame on ChildD
        child_d = "|parent1|childD"
        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)
        n_frames = max - min + 1
        for a in TRANSFORM_ATTR:
            assert_equal(cmds.keyframe(child_d + a, q=True, kc=True), n_frames)

    def export_import_hierarchy_kiko_file_test(self):
        self._export_import_hierarchy_test_shared(self._kiko_file)

    def export_import_hierarchy_kb_file_test(self):
        self._export_import_hierarchy_test_shared(self._kb_file)

    def export_import_hierarchy_kb_file_no_selection_test(self):
        self._export_and_duplicate_hierarchy(self._kb_file,
                                             rename_children=True)

        self._manager.import_from_file(self._kb_file, ignore_item_chunks=True,
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            suffix_to_add='1')

        self._compare_children("parent", "parent1")

        #the curve operator should have just created one single key per attr on
        #childBBB
        child_bbb = "|parent1|childB1|childBB1|childBBB1"
        for a in TRANSFORM_ATTR:
            assert_true(cmds.keyframe(child_bbb + a, q=True, kc=True) == 1)

        #the bake operator should have created a key frame per frame on ChildD
        child_d = "|parent1|childD1"
        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)
        n_frames = max - min + 1
        for a in TRANSFORM_ATTR:
            assert_equal(cmds.keyframe(child_d + a, q=True, kc=True), n_frames)

    def undo_test(self):
        self._export_and_duplicate_hierarchy(self._kiko_file)

        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)
        children = cmds.listRelatives("parent1", ad=True, f=True,
                                      typ='transform')

        cache = {}
        for c in children:
            attrs_values = {}
            for attr in TRANSFORM_ATTR:
                attr_values = []
                for i in  range(int(min), int(max)):
                    cmds.currentTime(i)
                    attr_values.append(cmds.getAttr(c + attr))
                attrs_values[attr] = attr_values
            cache[c] = attrs_values

        self._manager.import_from_file(self._kiko_file, objects=['parent1'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True)

        cmds.undo()

        for c in children:
            attrs_values = cache[c]
            for attr in TRANSFORM_ATTR:
                attr_values = attrs_values[attr]
                counter = 0
                for i in  range(int(min), int(max)):
                    cmds.currentTime(i)
                    assert_true(floats_equal(cmds.getAttr(c + attr),
                                              attr_values[counter]))
                    counter += 1

    def childA_test(self):
        self._export_and_duplicate_hierarchy(self._kiko_file)

        self._manager.import_from_file(self._kiko_file, objects=['parent1'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True)

        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)

        c1 = '|parent1|childA'
        c2 = '|parent1|childB|childA'
        for attr in TRANSFORM_ATTR:
            assert_true(cmds.keyframe(c1 + attr, q=True, kc=True) > 0)
            assert_true(cmds.keyframe(c2 + attr, q=True, kc=True) == 0)


    def double_hierarchy_import_test(self):
        #test clone hierarchy twice with animation, export all, then with two new hierarchy import animation
        self._export_and_duplicate_hierarchy(self._kiko_file)
        cmds.duplicate(rr=True)
        cmds.duplicate(rr=True)

        self._manager.import_from_file(self._kiko_file, objects=['parent1'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True)

        #adding a 20 of random keyframes for parent1 descendants
        children = cmds.listRelatives("parent1", ad=True, f=True,
                                      typ='transform')
        for i in range(20):
            item = random.choice(children)
            frame = random.randint(1, 120)
            value = random.randint(-100, 100)
            attr = random.choice(TRANSFORM_ATTR)
            cmds.setKeyframe(item + attr, v=value, time=frame)

        #Exporting
        cmds.select(["parent", "parent1"], r=True)
        self._manager.export_to_file(self._kiko_file, hierarchy=True)

        #Importing
        cmds.select(["parent2", "parent3"], r=True)
        self._manager.import_from_file(self._kiko_file,
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True)

        self._compare_children("parent", "parent2")
        self._compare_children("parent1", "parent3")


    def animation_rig_by_name_test(self):
        #test with names, remove namespace
        prefix = 'walk_cycle'
        cmds.file(get_app_file(KIKO_APP_NAME, 'walk_cycle.ma'), i=True,
                  typ="mayaAscii", iv=True, ra=True, mnc=False, options="v=0;",
                  rpr=prefix)

        controls = cmds.sets(prefix + "_controls", q=True)
        self._manager.export_to_file(self._kiko_file, objects=controls)

        cmds.file(get_app_file(KIKO_APP_NAME, 'walk_cycle.ma'), i=True,
                  namespace=prefix, typ="mayaAscii", iv=True, mnc=False,
                  ra=True, options="v=0;", rnn=True)

        #deleting the animation from the imported rig
        new_controls = cmds.sets(prefix + ":controls", q=True)
        for c in new_controls:
            attrs = list(set(cmds.listAttr(c, keyable=True) or []) |
                         set(cmds.listAttr(c, channelBox=True) or []))
            for a in attrs:
                all_keys = cmds.keyframe(c, query=True, indexValue=True, at=a)
                if all_keys:
                    all_keys.sort()
                    all_keys.reverse()
                    for k in all_keys:
                        cmds.cutKey(c, attribute=a, index=(k, k), clear=True)

        #import
        cmds.select(new_controls, r=True)
        self._manager.import_from_file(self._kiko_file,
                                       prefix_to_add=prefix + ":",
                                       str_replacements={prefix + '_': ''},
                                       ignore_item_chunks=True)

        #compare
        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)

        for i in  range(int(min), int(max)):
            cmds.currentTime(i)
            for c in controls:
                attrs = list(set(cmds.listAttr(c, keyable=True) or []) |
                             set(cmds.listAttr(c, channelBox=True) or []))
                other_c = prefix + ":" + c.replace(prefix + "_", "")
                for a in attrs:
                    val = cmds.getAttr(c + '.' + a)
                    if isinstance(val, float):
                        assert_true(floats_equal(val,
                                              cmds.getAttr(other_c + '.' + a)))
                    else:
                        assert_equal(val, cmds.getAttr(other_c + '.' + a))


    def animation_rig_hierarchy_test(self):
        #import file and export hierarchy
        prefix = 'walk_cycle'
        cmds.file(get_app_file(KIKO_APP_NAME, 'walk_cycle.ma'), i=True,
                  typ="mayaAscii", iv=True, ra=True, mnc=False, options="v=0;",
                  rpr=prefix)

        cmds.select(prefix + '_rig', r=True)
        self._manager.export_to_file(self._kiko_file, hierarchy=True)

        #import file with namespace
        cmds.file(get_app_file(KIKO_APP_NAME, 'walk_cycle.ma'), i=True,
                  namespace=prefix, typ="mayaAscii", iv=True, mnc=False,
                  ra=True, options="v=0;", rnn=True)

        #delete animation
        new_controls = cmds.sets(prefix + ":controls", q=True)
        for c in new_controls:
            attrs = list(set(cmds.listAttr(c, keyable=True) or []) |
                         set(cmds.listAttr(c, channelBox=True) or []))
            for a in attrs:
                all_keys = cmds.keyframe(c, query=True, indexValue=True, at=a)
                if all_keys:
                    all_keys.sort()
                    all_keys.reverse()
                    for k in all_keys:
                        cmds.cutKey(c, attribute=a, index=(k, k), clear=True)

        cmds.select(prefix + ':rig', r=True)
        self._manager.import_from_file(self._kiko_file,
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True)

        #compare
        self._compare_children(prefix + '_rig', prefix + ':rig',
                               repl=((prefix + "_", prefix + ":"),))

    def export_import_hierarchy_for_world_space_operator_test(self):
        self._export_and_duplicate_hierarchy(self._kiko_file)

        self._manager.import_from_file(self._kiko_file, objects=['parent1'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY)

        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)

        children = cmds.listRelatives('parent', ad=True, f=True,
                                      typ='transform')

        for i in  range(int(min), int(max)):
            cmds.currentTime(i)
            for c in children:
                if cmds.nodeType(c) != 'transform':
                    continue

                other_c = c.replace('parent', 'parent1')

                x1 = cmds.xform(c, ws=True, m=True, q=True)
                x2 = cmds.xform(other_c, ws=True, m=True, q=True)

                for i in range(len(x1)):
                    assert_true(floats_equal(x1[i], x2[i], places=12))


    def export_hierchy_import_single_item_for_world_space_operator_test(self):
        cmds.file(get_app_file(KIKO_APP_NAME, 'locators_hierarchy.ma'),
                  force=True, open=True, options='v=0;')
        cmds.select("parent")

        wo_name = worldspaceoperator.WorldSpaceOperator.name()
        self._manager.export_to_file(self._kiko_file, objects=['parent'],
                                     hierarchy=True, operators=(wo_name,))

        l = cmds.spaceLocator()
        obj_mapping = {'childBB': l[0]}
        self._manager.import_from_file(self._kiko_file, objects=l,
                                       obj_mapping=obj_mapping)

        c1 = 'childBB'
        c2 = l[0]

        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)
        for i in  range(int(min), int(max)):
            cmds.currentTime(i)

            x1 = cmds.xform(c1, ws=True, m=True, q=True)
            x2 = cmds.xform(c2, ws=True, m=True, q=True)

            for i in range(len(x1)):
                assert_true(floats_equal(x1[i], x2[i], places=12))

    def export_hierchy_import_anim_single_item_for_world_space_operator_test(
                                                                        self):
        cmds.file(get_app_file(KIKO_APP_NAME, 'locators_hierarchy.ma'),
                  force=True, open=True, options='v=0;')
        cmds.select("parent")

        wo_name = worldspaceoperator.WorldSpaceOperator.name()
        self._manager.export_to_file(self._kiko_file, objects=['parent'],
                                     hierarchy=True, operators=(wo_name,))

        l = cmds.spaceLocator()
        obj_mapping = {'childBB': l[0]}

        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)

        channels = [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]

        for i in range(10):
            frame = random.randint(min, max)
            value = random.randint(-100, 100)
            attr = random.choice(channels)
            cmds.setKeyframe(l[0] + attr, v=value, time=frame)

        for i in range(10):
            value = random.randint(-100, 100)
            cmds.setKeyframe(l[0] + ".tx", v=value, time=max + i + 1)

        self._manager.import_from_file(self._kiko_file, objects=l,
                                       obj_mapping=obj_mapping)

        c1 = 'childBB'
        c2 = l[0]

        for i in  range(int(min), int(max)):
            cmds.currentTime(i)
            x1 = cmds.xform(c1, ws=True, m=True, q=True)
            x2 = cmds.xform(c2, ws=True, m=True, q=True)

            for i in range(len(x1)):
                assert_true(floats_equal(x1[i], x2[i], places=12))

        for attr in channels:
            assert_equal(cmds.keyframe(l[0] + attr, q=True, kc=True), 120)


    def replace_animation_on_simple_locator_test(self):
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        frame_range = (min + 5, max - 5)

        l1 = self._create_and_animate_locator(frame_range=frame_range)
        self._manager.export_to_file(self._kiko_file, objects=[l1],
                                     operators=CHANNEL_OPERATOR_NAMES)

        l2 = cmds.spaceLocator()[0]
        for attr in TRANSFORM_ATTR:
            for i in range(min, max):
                value = random.randint(-100, 100)
                cmds.setKeyframe(l2 + attr, v=value, time=i)

        obj_mapping = {l1: l2}
        self._manager.import_from_file(self._kiko_file, objects=[l2],
                            import_anim_method=IMPORT_METHODS.ANIMATION.REPLACE,
                            ignore_item_chunks=True, obj_mapping=obj_mapping)

        for attr in TRANSFORM_ATTR:
            n_keys = cmds.keyframe(l1 + attr, q=True, kc=True)
            assert_equal(cmds.keyframe(l2 + attr, q=True, kc=True), n_keys + 9)
            for i in range(*frame_range):
                cmds.currentTime(i)
                assert_true(floats_equal(cmds.getAttr(l2 + attr),
                                          cmds.getAttr(l1 + attr)))

    def replace_animation_on_simple_locator_with_offset_test(self):
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        frame_range = (min, max)

        l1 = self._create_and_animate_locator(frame_range=frame_range)
        self._manager.export_to_file(self._kiko_file, objects=[l1],
                                     operators=CHANNEL_OPERATOR_NAMES)

        l2 = cmds.spaceLocator()[0]
        for attr in TRANSFORM_ATTR:
            for i in range(min, max):
                value = random.randint(-100, 100)
                cmds.setKeyframe(l2 + attr, v=value, time=i)

        offset = 5
        obj_mapping = {l1: l2}
        self._manager.import_from_file(self._kiko_file, objects=[l2],
                            import_anim_method=IMPORT_METHODS.ANIMATION.REPLACE,
                            ignore_item_chunks=True, obj_mapping=obj_mapping,
                            frame_value=offset)

        for attr in TRANSFORM_ATTR:
            n_keys = cmds.keyframe(l1 + attr, q=True, kc=True)
            assert_equal(cmds.keyframe(l2 + attr, q=True, kc=True),
                         n_keys + offset)
            for i in range(*frame_range):
                cmds.currentTime(i)
                assert_true(floats_equal(cmds.getAttr(l2 + attr,
                                                       time=i + offset),
                                          cmds.getAttr(l1 + attr)))


    def insert_animation_on_simple_locator_test(self):
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        frame_range = (min + 5, max - 5)

        l1 = self._create_and_animate_locator(frame_range=frame_range)
        self._manager.export_to_file(self._kiko_file, objects=[l1],
                                     operators=CHANNEL_OPERATOR_NAMES)

        l2 = cmds.spaceLocator()[0]
        for attr in TRANSFORM_ATTR:
            for i in range(min, max):
                value = random.randint(-100, 100)
                cmds.setKeyframe(l2 + attr, v=value, time=i)

        obj_mapping = {l1: l2}
        self._manager.import_from_file(self._kiko_file, objects=[l2],
                            import_anim_method=IMPORT_METHODS.ANIMATION.INSERT,
                            ignore_item_chunks=True, obj_mapping=obj_mapping,
                            frame_value=10)

        values = {}
        for attr in TRANSFORM_ATTR:
            val = []
            for i in range(*frame_range):
                cmds.currentTime(i)
                val.append(cmds.getAttr(l1 + attr))
            values[attr] = val

        for attr in TRANSFORM_ATTR:
            index = 0
            for i in range(10, 10 + (frame_range[1] - frame_range[0])):
                cmds.currentTime(i)
                assert_true(floats_equal(cmds.getAttr(l2 + attr),
                                          values[attr][index]))
                index += 1

    def insert_animation_on_hierarchy_test(self):
        self._export_and_duplicate_hierarchy(self._kiko_file)

        self._manager.import_from_file(self._kiko_file, objects=['parent1'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            import_anim_method=IMPORT_METHODS.ANIMATION.INSERT,
                            ignore_item_chunks=True, frame_value=10)

        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        children = cmds.listRelatives('parent', ad=True, f=True,
                                      typ='transform')

        for c1 in children:
            if 'constraint' in cmds.nodeType(c1, i=True):
                continue

            c2 = c1.replace('parent', 'parent1')
            values = {}
            for attr in TRANSFORM_ATTR:
                val = []
                for i in range(min, max):
                    cmds.currentTime(i)
                    val.append(cmds.getAttr(c1 + attr))
                values[attr] = val

            for attr in TRANSFORM_ATTR:
                index = 0
                for i in range(10, 10 + (max - min)):
                    cmds.currentTime(i)
                    assert_true(floats_equal(cmds.getAttr(c2 + attr),
                                              values[attr][index]))
                    index += 1

    def apply_animation_and_break_all_connections_test(self):
        cmds.file(get_app_file(KIKO_APP_NAME, 'locators_hierarchy.ma'),
                  force=True, open=True, options='v=0;')

        self._manager.export_to_file(self._kiko_file, objects=['parent'],
                                     hierarchy=True)

        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        MayaPreferences.reset()
        MayaPreferences.break_all_connections_in_apply_mode = True

        children = cmds.listRelatives('parent', ad=True, f=True,
                                      typ='transform')

        cache = {}
        for c in children:
            if 'constraint' in cmds.nodeType(c, i=True):
                continue

            values = {}
            for attr in TRANSFORM_ATTR:
                val = []
                for i in range(min, max):
                    cmds.currentTime(i)
                    val.append(cmds.getAttr(c + attr))
                values[attr] = val
            cache[c] = values

        self._manager.import_from_file(self._kiko_file, objects=['parent'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True)

        #constraints should have been deleted
        assert_false(bool([c for c in cmds.listConnections('|parent|childD',
                                                           s=True, d=False)
                           if 'constraint' in cmds.nodeType(c, i=True)]))

        #checking values are the same
        for c in children:
            if 'constraint' in cmds.nodeType(c, i=True):
                continue
            for attr in TRANSFORM_ATTR:
                index = 0
                for i in range(min, max):
                    cmds.currentTime(i)
                    assert_true(floats_equal(cmds.getAttr(c + attr),
                                              cache[c][attr][index]))
                    index += 1

        MayaPreferences.reset()

    def import_static_channel_on_animation_test(self):
        l1 = cmds.spaceLocator()[0]

        default_value = 15
        for attr in TRANSFORM_ATTR:
            cmds.setAttr(l1 + attr, default_value)

        self._manager.export_to_file(self._kiko_file, objects=[l1])

        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))
        frame_range = (min - 5, max + 5)
        l2 = self._create_and_animate_locator(frame_range=frame_range)
        self._manager.import_from_file(self._kiko_file, objects=[l2],
                            import_anim_method=IMPORT_METHODS.ANIMATION.REPLACE,
                            obj_mapping={l1: l2}, ignore_item_chunks=True)

        for i in range(min, max):
            cmds.currentTime(i)
            for attr in TRANSFORM_ATTR:
                assert_true(floats_equal(default_value,
                                         cmds.getAttr(l2 + attr)))

    def static_channels_test(self):
        l1 = cmds.spaceLocator()[0]
        facade = self._manager._facade
        obj = facade.get_node_by_name(l1)
        cmds.select(l1, r=True)

        attr_types = {'bool': bool, 'long': int, 'short': int, 'byte': int,
                      'char': int, 'float': float, 'double': float,
                      'doubleAngle': float, 'doubleLinear': float,
                      'time': float, 'string': str, 'enum': int}
        base_name = "attr"
        channels = {}
        original_values = {}

        #create channels and set default
        for at, ty in attr_types.iteritems():
            an = '_'.join([base_name, at])
            if at == 'enum':
                cmds.addAttr(ln=an, at=at, en='string1:string2:string3')
                original_values[at] = 1
                cmds.setAttr('.'.join([l1, an]), original_values[at])
            elif at == 'string':
                cmds.addAttr(ln=an, dt=at)
                original_values[at] = 'test'
                cmds.setAttr('.'.join([l1, an]), original_values[at], typ=at)
            else:
                cmds.addAttr(ln=an, at=at)
                original_values[at] = ty(random.random() * 100)
                cmds.setAttr('.'.join([l1, an]), original_values[at])

            channels[at] = facade.get_channel_object(obj, an)

        facade.pre_import()
        for at, chan in channels.iteritems():
            if at == 'enum':
                facade.set_channel_value(obj, chan, 2)
            elif at == 'string':
                facade.set_channel_value(obj, chan, "new_test")
            else:
                facade.set_channel_value(obj, chan,
                                     attr_types[at](random.random() * 100))
        facade.post_import()

        cmds.undo()
        for at, chan in channels.iteritems():
            an = '_'.join([base_name, at])
            if at in ['enum', 'string']:
                assert_equal(original_values[at], cmds.getAttr(l1 + "." + an))
            elif at == 'time':
                assert_true(floats_equal(original_values[at],
                                        cmds.getAttr(l1 + "." + an), places=2))
            else:
                assert_true(floats_equal(original_values[at],
                                          cmds.getAttr(l1 + "." + an)))

    def export_force_all_chunks_test(self):
        cmds.file(get_app_file(KIKO_APP_NAME, 'locators_hierarchy.ma'),
                  force=True, open=True, options='v=0;')
        cmds.select("parent")

        self._manager.export_to_file(self._kiko_file, objects=['parent'],
                                     hierarchy=True, force_op_evaluation=True)

        root = self._manager.get_root_from_file(self._kiko_file,
                                                flatten_hierarchy=True)

        item_op_num = len(OperatorsFactory().get_item_operator_names(
                                                                KIKO_APP_NAME))
        for item in root.iter_children():
            assert_equal(item.num_chunks, item_op_num)
            for c in item.iter_channels():
                assert_greater(c.num_chunks, 1)

    def export_one_operator_test(self):
        cmds.file(get_app_file(KIKO_APP_NAME, 'locators_hierarchy.ma'),
                  force=True, open=True, options='v=0;')
        cmds.select("parent")

        wo_name = worldspaceoperator.WorldSpaceOperator.name()
        st_name = staticoperator.StaticOperator.name()
        self._manager.export_to_file(self._kb_file, objects=['parent'],
                                     hierarchy=True, force_op_evaluation=True,
                                     operators=[wo_name, st_name])

        root = self._manager.get_root_from_file(self._kb_file,
                                                flatten_hierarchy=True)

        for item in root.iter_children():
            assert_equal(item.num_chunks, 1)
            for c in item.iter_channels():
                assert_equal(c.num_chunks, 1)

    def scale_fps_test(self):
        cmds.currentUnit(time='film')  # 24 fps
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))
        l1 = self._create_and_animate_locator((min, max))
        self._manager.export_to_file(self._kb_file, objects=[l1])

        num_keys = {}
        for attr in TRANSFORM_ATTR:
            num_keys[attr] = cmds.keyframe(l1 + attr, q=True, timeChange=True)

        cmds.currentUnit(time='pal')  # 25 fps
        #NO SCALE
        l2 = cmds.spaceLocator()[0]
        self._manager.import_from_file(self._kb_file, objects=[l2],
                                       obj_mapping={l1: l2},
                                       ignore_item_chunks=True)
        for attr in TRANSFORM_ATTR:
            assert_equal(num_keys[attr],
                         cmds.keyframe(l2 + attr, q=True, timeChange=True))

        #SCALE
        l3 = cmds.spaceLocator()[0]
        self._manager.import_from_file(self._kb_file, objects=[l3],
                                       obj_mapping={l1: l3},
                                       scale_using_fps=True,
                                       ignore_item_chunks=True)
        for attr in TRANSFORM_ATTR:
            #pal = 25, film = 24
            times1 = [t * (25.0 / 24) for t in num_keys[attr]]
            times2 = cmds.keyframe(l3 + attr, q=True, timeChange=True)
            for i in range(len(times1)):
                assert_true(floats_equal(times1[i], times2[i]))

    def operator_missing_test(self):
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))
        l1 = self._create_and_animate_locator((min, max))
        assert_raises(KikoManagerException, self._manager.export_to_file,
                      self._kb_file, [l1], ['FakeOperator'])
        self._manager.export_to_file(self._kb_file, objects=[l1])

        l2 = cmds.spaceLocator()[0]
        assert_raises(KikoManagerException, self._manager.import_from_file,
                      self._kb_file, [l2], ['FakeOperator'], None, None, None,
                      {l1: l2})

    def frame_range_export_test(self):
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        l1 = self._create_and_animate_locator((min, max), factor=2)
        l2 = cmds.spaceLocator()[0]
        l3 = cmds.spaceLocator()[0]

        cmds.select([l1, l2])
        cmds.parentConstraint(mo=True, weight=1)

        for attr in TRANSFORM_ATTR:
            cmds.setAttr(l3 + attr, 15)

        fd = 8
        self._manager.export_to_file(self._kb_file, objects=[l1, l2, l3],
                                     start_frame=min + fd, end_frame=max - fd)

        l4 = cmds.spaceLocator()[0]
        l5 = cmds.spaceLocator()[0]
        l6 = cmds.spaceLocator()[0]

        obj_mapping = {l1: l4, l2: l5, l3: l6}
        self._manager.import_from_file(self._kb_file, objects=[l4, l5, l6],
                                       obj_mapping=obj_mapping,
                                       ignore_item_chunks=True)

        for i in range(int(min + fd), int(max - fd) + 1):
            cmds.currentTime(i)
            for attr in TRANSFORM_ATTR:
                for obj1, obj2 in obj_mapping.iteritems():
                    assert_true(floats_equal(cmds.getAttr(obj1 + attr),
                                             cmds.getAttr(obj2 + attr)))

    def frame_range_import_test(self):
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        l1 = self._create_and_animate_locator((min, max), factor=1)
        l2 = cmds.spaceLocator()[0]
        l3 = cmds.spaceLocator()[0]

        cmds.select([l1, l2])
        cmds.parentConstraint(mo=True, weight=1)

        for attr in TRANSFORM_ATTR:
            cmds.setAttr(l3 + attr, 15)

        fd = 8
        self._manager.export_to_file(self._kb_file, objects=[l1, l2, l3])

        l4 = cmds.spaceLocator()[0]
        l5 = cmds.spaceLocator()[0]
        l6 = cmds.spaceLocator()[0]

        obj_mapping = {l1: l4, l2: l5, l3: l6}
        self._manager.import_from_file(self._kb_file, objects=[l4, l5, l6],
                            obj_mapping=obj_mapping, ignore_item_chunks=True,
                            start_frame=min + fd, end_frame=max - fd)

        for attr in TRANSFORM_ATTR:
            for obj1, obj2 in obj_mapping.iteritems():
                frames = cmds.keyframe(obj2 + attr, q=True, tc=True)
                if frames is None:
                    assert_true(floats_equal(cmds.getAttr(obj1 + attr),
                                             cmds.getAttr(obj2 + attr)))
                    continue

                for i in range(int(frames[0]), int(frames[-1])):
                    cmds.currentTime(i)
                    assert_true(floats_equal(cmds.getAttr(obj1 + attr),
                                             cmds.getAttr(obj2 + attr)))

    def _attribute_mapping_testing_shared(self, selection=False):
        min = int(cmds.playbackOptions(q=True, minTime=True))
        max = int(cmds.playbackOptions(q=True, maxTime=True))

        l1 = self._create_and_animate_locator((min, max), factor=1)
        l2 = cmds.spaceLocator()[0]

        cmds.select(l1)
        self._manager.export_to_file(self._kb_file)

        obj_mapping = {l1 + ".tx": l2 + ".ty",
                       l1 + ".ty": l2 + ".tz",
                       l1 + ".tz": l2 + ".tx",
                       l1 + ".rx": l2 + ".ry",
                       l1 + ".ry": l2 + ".rz",
                       l1 + ".rz": l2 + ".rx"}

        if selection:
            cmds.select(l2)
        else:
            cmds.select(cl=True)

        self._manager.import_from_file(self._kb_file, obj_mapping=obj_mapping,
                                       ignore_item_chunks=True)

        min = cmds.playbackOptions(q=True, minTime=True)
        max = cmds.playbackOptions(q=True, maxTime=True)

        for i in  range(int(min), int(max)):
            cmds.currentTime(i)
            for attr1, attr2 in obj_mapping.iteritems():
                assert_true(floats_equal(cmds.getAttr(attr1),
                                          cmds.getAttr(attr2)))

    def attribute_mapping_no_input_objects_test(self):
        self._attribute_mapping_testing_shared()

    def attribute_mapping_input_objects_test(self):
        self._attribute_mapping_testing_shared(True)

    def op_priority_test(self):
        cmds.file(get_app_file(KIKO_APP_NAME, 'locators_hierarchy.ma'),
                  force=True, open=True, options='v=0;')
        cmds.select("parent")

        t = cmds.currentTime(q=True)
        self._manager.export_to_file(self._kiko_file, objects=['parent'],
                                     hierarchy=True, force_op_evaluation=True)
        cmds.duplicate(rr=True)

        children = cmds.listRelatives("parent1", ad=True, f=True,
                                      typ='transform')
        for c in children:
            for a in TRANSFORM_ATTR:
                cmds.setAttr(c + a, 0)

        stn = staticoperator.StaticOperator.name()
        bkn = bakeoperator.BakeOperator.name()
        cmds.delete(cmds.listRelatives("parent1", ad=True, f=True,
                                       typ='constraint') or [])
        self._manager.import_from_file(self._kiko_file, objects=['parent1'],
                            import_obj_method=IMPORT_METHODS.OBJECT.HIERARCHY,
                            ignore_item_chunks=True,
                            channel_op_priority=[stn, bkn])

        children = cmds.listRelatives("parent1", ad=True, f=True,
                                      typ='transform')

        cmds.currentTime(t)
        for c in children:
            for a in TRANSFORM_ATTR:
                assert_true(cmds.keyframe(c + a, q=True, kc=True) == 0)

                other_c = c.replace('parent1', 'parent')

                assert_true(floats_equal(cmds.getAttr(c + a),
                                          cmds.getAttr(other_c + a)))
