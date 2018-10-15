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

import warnings

from kiko.exceptions import KikoDeserializeException

from kiko.constants import (KIKO_FILE_VERSION, SERIALIZATION_TYPES,
                            SERIALIZATION, IMPORT_METHODS)
from kiko.exceptions import (KikoDeserializeException, InvalidOperator,
                             KikoWarning)
from kiko.core.entity import item, chunk, channel
from kiko.operators.factory import OperatorsFactory

from kiko.io.basedeserializer import BaseDeserializer


class _DeserializerV1Helper:

    @classmethod
    def add_children(cls, parent, data, flatten_hierarchy, ignore_item_chunks):
        i = item.Item(parent, data[SERIALIZATION.NAME])

        for cd in data[SERIALIZATION.CHILDREN]:
            cls.add_children(parent if flatten_hierarchy else i, cd,
                             flatten_hierarchy, ignore_item_chunks)

        for cd in data[SERIALIZATION.CHANNELS]:
            cls.add_channel(i, cd)

        if not ignore_item_chunks:
            for cd in data[SERIALIZATION.CHUNKS]:
                cls.add_chunk(i, cd)

    @classmethod
    def add_channel(cls, parent, data):
        c = channel.Channel(parent, data[SERIALIZATION.NAME])

        for cd in data[SERIALIZATION.CHUNKS]:
            cls.add_chunk(c, cd)

    @staticmethod
    def add_chunk(parent, data):
        constructor = (chunk.ItemChunk if isinstance(parent,
                                                     item.Item) else chunk.ChannelChunk)

        c = constructor(parent, operator_name=data[SERIALIZATION.OPERATOR_NAME],
                        operator_ver=data[SERIALIZATION.OPERATOR_VERSION])
        c.operator_data = data[SERIALIZATION.OPERATOR_DATA]

    @staticmethod
    def _load_chunk(facade, chunk_, op_priority, o, start_frame, end_frame,
                    frame_value, time_multiplier, import_anim_method,
                    channel=None):
        op_c = OperatorsFactory().get_operator(chunk_.operator_name,
                                               chunk_.operator_version)
        if not op_c.is_app_supported(facade.get_app_name()):
            return False

        chunk_.operator = op_c
        chunk_.operator.deserialize(facade, o, chunk_.operator_version,
                                    chunk_.operator_data, import_anim_method,
                                    start_frame, end_frame, frame_value,
                                    channel, time_multiplier)
        return chunk_.operator.ignore_following_operators()

    @classmethod
    def _load_chunks(cls, facade, entity_, op_priority, o, start_frame,
                     end_frame, frame_value, time_multiplier,
                     import_anim_method, channel=None):
        if op_priority:
            for op in op_priority:
                chunk_ = entity_.chunk(op)
                if not chunk_:
                    continue

                if cls._load_chunk(facade, chunk_, op_priority, o, start_frame,
                                   end_frame, frame_value, time_multiplier,
                                   import_anim_method, channel):
                    return True
        else:
            for chunk_ in entity_.iter_chunks():
                if cls._load_chunk(facade, chunk_, op_priority, o, start_frame,
                                   end_frame, frame_value, time_multiplier,
                                   import_anim_method, channel):
                    return True

    @classmethod
    def _pre_load_channel_set_up(cls, facade, o, attr, frame_value, start_frame,
                                 end_frame, time_multiplier,
                                 import_anim_method):
        tm = time_multiplier
        if import_anim_method == IMPORT_METHODS.ANIMATION.APPLY:
            facade.remove_animation_from_channel(o, attr)
        elif import_anim_method == IMPORT_METHODS.ANIMATION.INSERT:
            facade.shift_animation_in_frame_range(o, attr, frame_value,
                                                  frame_value + (
                                                              end_frame - start_frame) * tm)
        elif import_anim_method == IMPORT_METHODS.ANIMATION.REPLACE:
            facade.remove_animation_from_frame_range(o, attr,
                                                     frame_value + start_frame * tm,
                                                     frame_value + end_frame * tm)
        else:
            raise KikoDeserializeException("Invalid animation import "
                                           "method")

    @classmethod
    def _load_item(cls, facade, item, item_op_priority, channel_op_priority, o,
                   import_anim_method, start_frame, end_frame, frame_value,
                   time_multiplier):
        # load item chunks
        if cls._load_chunks(facade, item, item_op_priority, o, start_frame,
                            end_frame, frame_value, time_multiplier,
                            import_anim_method):
            return

        # load channels
        for cc in item.iter_channels():
            # mapping channel name from kiko to app
            name = facade.map_kiko_channel_to_app_channel(o, cc.name)

            attr = facade.get_channel_object(o, name)

            if attr is None:
                continue

            cls._pre_load_channel_set_up(facade, o, attr, frame_value,
                                         start_frame, end_frame,
                                         time_multiplier, import_anim_method)

            cls._load_chunks(facade, cc, channel_op_priority, o, start_frame,
                             end_frame, frame_value, time_multiplier,
                             import_anim_method, attr)

    @classmethod
    def _load_specified_channels(cls, facade, item, channel_op_priority, o,
                                 import_anim_method, start_frame, end_frame,
                                 frame_value, time_multiplier, attr_mapping):
        attr_name = attr_mapping[0]

        cc = item.channel(facade.map_app_channel_to_kiko_channel(o, attr_name))
        if cc is None:
            return

        dest_attr_name = attr_mapping[1]
        name = facade.map_app_channel_to_kiko_channel(o, dest_attr_name)
        dest_attr = facade.get_channel_object(o, name)
        if dest_attr is None:
            return

        cls._pre_load_channel_set_up(facade, o, dest_attr, frame_value,
                                     start_frame, end_frame, time_multiplier,
                                     import_anim_method)

        cls._load_chunks(facade, cc, channel_op_priority, o, start_frame,
                         end_frame, frame_value, time_multiplier,
                         import_anim_method, dest_attr)

    @classmethod
    def load_data_on_hierarchy(cls, facade, obj, import_anim_method, item,
                               item_op_priority, channel_op_priority,
                               start_frame, end_frame, frame_value,
                               time_multiplier):
        cls._load_item(facade, item, item_op_priority, channel_op_priority, obj,
                       import_anim_method, start_frame, end_frame, frame_value,
                       time_multiplier)

        children = facade.get_children(obj)
        num_obj_children = len(children)
        num_item_children = item.num_children

        if num_item_children > num_obj_children:
            warnings.warn("Critical hierarchy mismatch - Found a greater "
                          "number of children for item %s (%d > %d) in file." % (
                          item.name, num_item_children, num_obj_children),
                          KikoWarning)
            return

        if num_obj_children != num_item_children:
            warnings.warn("Found a different number of children for item %s "
                          "(%d - %d)." % (
                          item.name, num_obj_children, num_item_children),
                          KikoWarning)

        for i in range(num_item_children):
            child = item.child_by_index(i)
            cls.load_data_on_hierarchy(facade, children[i], import_anim_method,
                                       child, item_op_priority,
                                       channel_op_priority, start_frame,
                                       end_frame, frame_value, time_multiplier)

    @classmethod
    def load_data_by_name(cls, facade, objects, import_anim_method,
                          item_op_priority, channel_op_priority, names_to_item,
                          start_frame, end_frame, frame_value, time_multiplier):
        if objects:
            for o in objects:
                name = facade.get_name(o)

                entry = names_to_item.get(name)
                if entry is None:
                    warnings.warn("Could not find object %s" % name,
                                  KikoWarning)
                    continue

                for e in entry:
                    if isinstance(e, (list, tuple)):
                        cls._load_specified_channels(facade, e[0],
                                                     channel_op_priority, o,
                                                     import_anim_method,
                                                     start_frame, end_frame,
                                                     frame_value,
                                                     time_multiplier,
                                                     (e[1], e[2]))
                    else:
                        cls._load_item(facade, e, item_op_priority,
                                       channel_op_priority, o,
                                       import_anim_method,
                                       start_frame, end_frame, frame_value,
                                       time_multiplier)
        else:
            item_found = False
            for name, entry in names_to_item.iteritems():
                o = facade.get_node_by_name(name)

                if o is None:
                    warnings.warn("Could not find object %s" % name,
                                  KikoWarning)
                    continue

                item_found = True

                for e in entry:
                    if isinstance(e, (list, tuple)):
                        cls._load_specified_channels(facade, e[0],
                                                     channel_op_priority, o,
                                                     import_anim_method,
                                                     start_frame, end_frame,
                                                     frame_value,
                                                     time_multiplier,
                                                     (e[1], e[2]))
                    else:
                        cls._load_item(facade, e, item_op_priority,
                                       channel_op_priority, o,
                                       import_anim_method,
                                       start_frame, end_frame, frame_value,
                                       time_multiplier)

            if not item_found:
                raise KikoDeserializeException("Could not find any object to "
                                               "associate with the given kiko "
                                               "data")


class DeserializerV1(BaseDeserializer):

    @staticmethod
    def version():
        return KIKO_FILE_VERSION

    def load_data(self, root, objects, item_op_priority=None,
                  channel_op_priority=None,
                  import_obj_method=IMPORT_METHODS.OBJECT.NAME,
                  import_anim_method=IMPORT_METHODS.ANIMATION.APPLY,
                  str_replacements=None, obj_mapping=None, prefix_to_add=None,
                  suffix_to_add=None, frame_value=0, time_multiplier=1,
                  start_frame=None, end_frame=None):

        start_frame = root.start_frame if start_frame is None else start_frame
        end_frame = root.end_frame if end_frame is None else end_frame

        if import_obj_method == IMPORT_METHODS.OBJECT.NAME:
            names_to_item = {}

            for child in root.iter_children():
                name = child.name

                if obj_mapping and name in obj_mapping:
                    value = obj_mapping[name]
                    if isinstance(value, list):
                        for v in value:
                            if not v[1] in names_to_item:
                                names_to_item[v[1]] = []
                            # this might happen if the user is trying to map
                            # both channels, but not all channels for one item
                            elif not isinstance(names_to_item[v[1]], list):
                                continue
                            names_to_item[v[1]].append((child, v[0], v[2]))
                    else:
                        if value in names_to_item:
                            names_to_item[value].append(child)
                        else:
                            names_to_item[value] = [child]
                else:
                    if str_replacements:
                        for key, value in str_replacements.iteritems():
                            name = name.replace(key, value)

                    if suffix_to_add:
                        name += suffix_to_add

                    if prefix_to_add:
                        name = prefix_to_add + name

                    names_to_item[name] = [child]

            if not names_to_item:
                raise KikoDeserializeException("Could not find any object to "
                                               "associate with the given kiko data")

            _DeserializerV1Helper.load_data_by_name(self._facade, objects,
                                                    import_anim_method,
                                                    item_op_priority,
                                                    channel_op_priority,
                                                    names_to_item, start_frame,
                                                    end_frame, frame_value,
                                                    time_multiplier)
        else:
            for i in range(len(objects)):
                item = root.child_by_index(i)
                _DeserializerV1Helper.load_data_on_hierarchy(self._facade,
                                                             objects[i],
                                                             import_anim_method,
                                                             item,
                                                             item_op_priority,
                                                             channel_op_priority,
                                                             start_frame,
                                                             end_frame,
                                                             frame_value,
                                                             time_multiplier)

    def get_root_from_data(self, data, flatten_hierarchy=False,
                           ignore_item_chunks=False):
        for op in data[SERIALIZATION.KIKO_OPERATORS]:
            if not OperatorsFactory().has_operator(op[0], op[1]):
                raise InvalidOperator("Operator %s (version %d) is not "
                                      "available. Cannot deserialize file." % (
                                      op[0], op[1]))

        s_data = data[SERIALIZATION.KIKO_DATA]
        if (s_data[SERIALIZATION.TYPE] != SERIALIZATION_TYPES.ROOT_ITEM):
            raise KikoDeserializeException('Root not found. Cannot deserialize '
                                           'file')

        frame_range = data[SERIALIZATION.KIKO_FRAME_RANGE]
        root = item.RootItem(fps=data[SERIALIZATION.KIKO_FPS],
                             start_frame=frame_range[0],
                             end_frame=frame_range[1])

        for kd in s_data[SERIALIZATION.CHILDREN]:
            _DeserializerV1Helper.add_children(root, kd, flatten_hierarchy,
                                               ignore_item_chunks)

        return root

