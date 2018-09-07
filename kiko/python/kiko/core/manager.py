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

from kiko.apps.basefacade import BaseFacade
from kiko.exceptions import (InvalidFacadeException, KikoManagerException,
                             KikoWarning)
from kiko.operators.factory import OperatorsFactory
from kiko.constants import IMPORT_METHODS

from kiko.io import serializer, deserializers
from kiko.io.kikofile import KikoFile

class KikoManager(object):

    def __init__(self, facade=None):
        if facade is None or not issubclass(facade, BaseFacade):
            raise InvalidFacadeException('Invalid facade was provided.')
        self._facade = facade

    @property
    def facade(self):
        return self._facade

    def export_to_file(self, file_name, objects=None, operators=None,
                       hierarchy=False, keep_previous_images=False,
                       start_frame=None, end_frame=None,
                       force_op_evaluation=False, channel_filter=None,
                       image_fps=None):
        if self._facade is None:
            raise InvalidFacadeException('Cannot export file without a facade. '
                                'Please create a new kikoManager with a facade')

        ops = []
        operators = operators or OperatorsFactory().get_all_operator_names(
                                                    self._facade.get_app_name())
        for o in operators:
            op_c = None
            if isinstance(o, tuple):
                if OperatorsFactory.has_operator(o[0], version=o[1]):
                    op_c = OperatorsFactory().get_operator(o[0], o[1])
            else:
                op_ver = OperatorsFactory().get_latest_version(o)
                if not op_ver is None:
                    op_c = OperatorsFactory().get_operator(o, op_ver)

            if op_c is None:
                raise KikoManagerException('Could not find operator %s' % o)

            if not op_c.is_app_supported(self._facade.get_app_name()):
                continue

            ops.append(op_c)

        if not ops:
            raise KikoManagerException("No valid operator found.")

        if objects:
            objs = [self._facade.get_node_by_name(o) for o in objects]
        else:
            objs = self._facade.get_selection()

        if not objs:
            raise KikoManagerException("No obj was selected or passed as arg.")

        k_file = KikoFile(file_name)
        if keep_previous_images:
            k_file.parse()
        s = serializer.Serializer(facade=self._facade)
        k_file.data = s.serialize(file_name, objs, hierarchy=hierarchy,
                                  operators=ops, start_frame=start_frame,
                                  end_frame=end_frame,
                                  force_op_evaluation=force_op_evaluation,
                                  channel_filter=channel_filter)
        k_file.save()

    def import_from_file(self, file_name, objects=None, item_op_priority=None,
                         channel_op_priority=None, import_obj_method=None,
                         import_anim_method=None, str_replacements=None,
                         obj_mapping=None, prefix_to_add=None,
                         suffix_to_add=None, scale_using_fps=False,
                         frame_value=0, ignore_item_chunks=False,
                         start_frame=None, end_frame=None):
        if self._facade is None:
            raise InvalidFacadeException('Cannot import file without a facade. '
                                'Please create a new kikoManager with a facade')

        k_file = KikoFile(file_name)
        k_file.parse()

        if import_obj_method is None:
            import_obj_method = IMPORT_METHODS.OBJECT.NAME
        elif not import_obj_method in IMPORT_METHODS.OBJECT.all():
            raise KikoManagerException('Invalid object import method given')
        flatten_hierarchy = import_obj_method != IMPORT_METHODS.OBJECT.HIERARCHY

        if import_anim_method is None:
            import_anim_method = IMPORT_METHODS.ANIMATION.APPLY
        elif not import_anim_method in IMPORT_METHODS.ANIMATION.all():
            raise KikoManagerException('Invalid animation import method given')

        if item_op_priority or channel_op_priority:
            all_op = (item_op_priority or []) + (channel_op_priority or [])
            for o in all_op:
                op_ver = OperatorsFactory().get_latest_version(o)
                if op_ver is None:
                    raise KikoManagerException("Operators %s not found" % o)

                op_c = OperatorsFactory().get_operator(o, op_ver)
                if not op_c.is_app_supported(self._facade.get_app_name()):
                    raise KikoManagerException("Operator %s does not support %s"
                                            % (o, self._facade.get_app_name()))

        if obj_mapping:
            #building a new map in case there is some channel remapping
            temp_mapping = {}
            for key, value in obj_mapping.iteritems():
                tokens = key.split('.')
                if (len(tokens) == 2) != ('.' in value):
                    raise KikoManagerException("Cannot map channel to object "
                                               "or viceversa: %s -> %s" %
                                               (key, value))

                if len(tokens) == 2:
                    if (not tokens[0] in temp_mapping or
                            not isinstance(temp_mapping[tokens[0]], list)):
                        temp_mapping[tokens[0]] = []

                    vts = value.split('.')
                    temp_mapping[tokens[0]].append((tokens[1], vts[0], vts[1]))
                else:
                    temp_mapping[key] = value
            obj_mapping = temp_mapping

        if objects:
            objs = [self._facade.get_node_by_name(o) for o in objects]
        else:
            objs = self._facade.get_selection()

        if not objs:
            msg = "No obj was selected or passed as arg."
            if import_obj_method == IMPORT_METHODS.OBJECT.NAME:
                warnings.warn(msg + " Trying to match items by name.")
            else:
                raise KikoManagerException(msg)

        d = deserializers.DeserializerManager.get_deserializer(k_file.version,
                                                               self._facade)
        root = d.get_root_from_data(k_file.data,
                                    flatten_hierarchy=flatten_hierarchy,
                                    ignore_item_chunks=ignore_item_chunks)

        t_mult = ((float(self._facade.get_fps()) / root.fps)
                  if scale_using_fps else 1)

        self._facade.pre_import()

        d.load_data(root, objs, item_op_priority=item_op_priority,
                    channel_op_priority=channel_op_priority,
                    import_obj_method=import_obj_method,
                    import_anim_method=import_anim_method,
                    str_replacements=str_replacements, obj_mapping=obj_mapping,
                    prefix_to_add=prefix_to_add, suffix_to_add=suffix_to_add,
                    frame_value=frame_value, time_multiplier=t_mult,
                    start_frame=start_frame, end_frame=end_frame)

        self._facade.post_import()


    def get_root_from_file(self, file_name, flatten_hierarchy=False):
        k_file = KikoFile(file_name)
        k_file.parse()

        d = deserializers.DeserializerManager.get_deserializer(k_file.version,
                                                               self._facade)
        return d.get_root_from_data(k_file.data,
                                    flatten_hierarchy=flatten_hierarchy)


