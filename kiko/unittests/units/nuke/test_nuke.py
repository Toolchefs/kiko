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
import math

#suppressing the warnings here in the unit tests
warnings.simplefilter("ignore")

from nose.tools import (assert_false, assert_true, assert_equal, assert_raises,
                        assert_greater)

import nuke

from kiko.apps.nuke import manager
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

TRANSFORM_ATTR = {"translate": 3, "rotate": 3, "scaling": 3}

class TestNuke(object):

    def setUp(self):
        self._manager = manager.NukeKikoManager()
        self._facade = self._manager.facade

        _, self._kiko_file = tempfile.mkstemp(suffix=KIKO_FILE_EXTENSION)
        _, self._kb_file = tempfile.mkstemp(suffix=KB_FILE_EXTENSION)


    def tearDown(self):
        nuke.scriptClose()

        #os.unlink(self._kiko_file)
        #os.unlink(self._kb_file)

    def _create_and_animate_axis_node(self, frame_range=None, factor=3):
        if frame_range is None:
            frame_range = self._facade.get_active_frame_range()
    
        node = nuke.createNode('Axis')
        channels = [("translate", 0), ("translate", 1), ("translate", 2)]
        channels += [("rotate", 0), ("rotate", 1), ("rotate", 2)]
        channels += [("scaling", 0), ("scaling", 1), ("scaling", 2)]
    
        for channel in channels:
            knob = node.knobs()[channel[0]]
            if isinstance(knob, nuke.Enumeration_Knob):
                value = random.randint(0, len(channel[0].values()) - 1)
                self._facade.set_channel_value(node, channel, value)
                continue
            if isinstance(knob, nuke.Boolean_Knob):
                value = random.randint(0, 1)
                self._facade.set_channel_value(node, channel, value)
                continue
        
            if factor == 1:
                num_keys = frame_range[1] - frame_range[0]
            else:
                num_keys = random.randint(3, (
                            frame_range[1] - frame_range[0]) / factor)
        
            knob.setAnimated(channel[1])
            ko = knob.animation(channel[1])
        
            for i in range(num_keys):
                frame = random.randint(frame_range[0], frame_range[1])
                value = random.randint(-100, 100)
                self._facade.set_channel_key_frame(ko, frame, value)
        
            value = random.randint(-100, 100)
            # making sure there's a keyframe at the begining and end of animation
            self._facade.set_channel_key_frame(ko, frame_range[0], value)
            self._facade.set_channel_key_frame(ko, frame_range[1], value)
    
        return node

    def _export_import_simple_file_test_shared(self, file_):
        node1 = self._create_and_animate_axis_node()
        node1.setSelected(True)
        self._manager.export_to_file(file_)

        node2 = nuke.createNode('Axis')
        obj_mapping = {node1.name(): node2.name()}

        self._manager.import_from_file(file_, objects=[node2.name()],
                                       obj_mapping=obj_mapping,
                                       ignore_item_chunks=True)
        
        fmin, fmax = self._facade.get_active_frame_range()

        for i in range(int(fmin), int(fmax)):
            self._facade.move_to_frame(i)
            for channel in self._facade.list_channels(node1):
                k1 = channel[0]

                #ignoring matrix as when setting all transform attributes, its
                #values can be pretty messed up
                if k1.name() == 'matrix':
                    continue

                k2 = node2.knob(k1.name())
                
                assert_true(floats_equal(k1.valueAt(i, channel[1]),
                                         k2.valueAt(i, channel[1])))

    def export_import_simple_kiko_file_test(self):
        self._export_import_simple_file_test_shared(self._kiko_file)

    def export_import_simple_kb_file_test(self):
        self._export_import_simple_file_test_shared(self._kb_file)

    def export_import_static_values_test(self):
        node1 = nuke.createNode('Axis')
        for channel in self._facade.list_channels(node1):
            if isinstance(channel[0], nuke.Enumeration_Knob):
                value = random.randint(0, len(channel[0].values()) - 1)
            else:
                value = random.randint(-100, 100)
            self._facade.set_channel_value(node1, channel, value)

        self._manager.export_to_file(self._kb_file)

        node2 = nuke.createNode('Axis')
        obj_mapping = {node1.name(): node2.name()}

        self._manager.import_from_file(self._kb_file, objects=[node2.name()],
                                       obj_mapping=obj_mapping,
                                       ignore_item_chunks=True)

        for channel in self._facade.list_channels(node1):
            k1 = channel[0]
            k2 = node2.knob(k1.name())

            if channel[1] == 0:
                try:
                    assert_true(floats_equal(k1.getValue(channel[1]),
                                             k2.getValue(channel[1])))
                except:
                    assert_true(k1.getValue(channel[1]),
                                k2.getValue(channel[1]))

            else:
                assert_true(floats_equal(k1.getValue(channel[1]),
                                         k2.getValue(channel[1])))

    def export_import_baked_values_test(self):
        node1 = self._create_and_animate_axis_node()
        node1.setSelected(True)

        bkn = bakeoperator.BakeOperator.name()
        stn = staticoperator.StaticOperator.name()
        self._manager.export_to_file(self._kb_file, operators=[bkn, stn])

        node2 = nuke.createNode('Axis')
        obj_mapping = {node1.name(): node2.name()}

        self._manager.import_from_file(self._kb_file, objects=[node2.name()],
                                       obj_mapping=obj_mapping,
                                       ignore_item_chunks=True)

        min, max = self._facade.get_active_frame_range()

        for i in  range(int(min), int(max)):
            self._facade.move_to_frame(i)
            for channel in self._facade.list_channels(node1):
                k1 = channel[0]

                #ignoring matrix as when setting all transform attributes, its
                #values can be pretty messed up
                if k1.name() == 'matrix':
                    continue

                k2 = node2.knob(k1.name())

                assert_true(floats_equal(k1.valueAt(i, channel[1]),
                                         k2.valueAt(i, channel[1])))


    def export_import_simple_test(self):
        nuke.scriptOpen(get_app_file(KIKO_APP_NAME, 'simple_axis.nk'))
        node1 = nuke.toNode("Axis1")
        node1.setSelected(True)

        self._manager.export_to_file(self._kb_file)

        node2 = nuke.createNode('Axis')
        obj_mapping = {node1.name(): node2.name()}
        self._manager.import_from_file(self._kb_file, objects=[node2.name()],
                                       obj_mapping=obj_mapping,
                                       ignore_item_chunks=True)

        min, max = self._facade.get_active_frame_range()

        channels = ['translate', 'rotate']

        for i in range(int(min), int(max)):
            self._facade.move_to_frame(i)

            for c in channels:
                k1 = node1.knob(c)
                k2 = node2.knob(c)
                for ci in range(3):
                    assert_true(floats_equal(k1.valueAt(i, ci),
                                             k2.valueAt(i, ci)))
