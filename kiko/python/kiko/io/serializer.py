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

from kiko.constants import SERIALIZATION_TYPES, SERIALIZATION, KIKO_FILE_VERSION
from kiko.exceptions import InvalidFacadeException, InvalidFrameRangeException
from kiko.core.entity import item, chunk, channel
from kiko.apps.basefacade import BaseFacade


class Serializer(object):
    def __init__(self, facade):
        if not issubclass(facade, BaseFacade):
            raise InvalidFacadeException('Invalid facade provided.')
        self._facade = facade

    def _cache_channels(self, app_object, c_item, channel_operators, bake_tps,
                        std_tps, force_op_evaluation, channel_filter):

        cfs = None
        if channel_filter:
            cfs = channel_filter.get(c_item.name)

        if cfs:
            channels = [self._facade.get_channel_object(app_object, c) for c in
                        cfs]
        else:
            channels = self._facade.list_channels(app_object)

        for a in channels:
            name = self._facade.get_channel_name(app_object, a)

            # mapping channel name from app to kiko - this is needed for
            # software compatibility
            name = self._facade.map_app_channel_to_kiko_channel(app_object,
                                                                name)

            p = channel.Channel(c_item, name)
            self._cache_chunks(app_object, p, channel_operators, bake_tps,
                               std_tps, force_op_evaluation, a)

    def _cache_chunks(self, app_object, parent_item, operators, bake_tps,
                      std_tps, force_op_evaluation, chan_object=None):
        for op in operators:
            if not op.validate(self._facade, app_object, channel=chan_object,
                               force=force_op_evaluation):
                continue

            if chan_object is None:
                c = chunk.ItemChunk(parent_item, operator=op)
            else:
                c = chunk.ChannelChunk(parent_item, operator=op)

            if op.bakeable():
                bake_tps.append((c, app_object, chan_object))
            else:
                std_tps.append((c, app_object, chan_object))

    def _cache_object(self, app_object, parent_item, cached_objects, item_ops,
                      channel_ops, bake_tps, std_tps, force_op_evaluation,
                      channel_filter):

        name = self._facade.get_name(app_object)

        c_item = item.Item(parent_item, name)
        cached_objects[c_item.id] = (app_object, parent_item.id)

        self._cache_chunks(app_object, c_item, item_ops, bake_tps, std_tps,
                           force_op_evaluation)
        self._cache_channels(app_object, c_item, channel_ops, bake_tps, std_tps,
                             force_op_evaluation, channel_filter)

        return c_item

    def _cache_children(self, app_object, parent_item, cached_objects, item_ops,
                        channel_ops, bake_tps, std_tps, force_op_evaluation,
                        channel_filter):
        for c in self._facade.get_children(app_object):
            c_item = self._cache_object(c, parent_item, cached_objects,
                                        item_ops, channel_ops, bake_tps,
                                        std_tps, force_op_evaluation,
                                        channel_filter)
            self._cache_children(c, c_item, cached_objects, item_ops,
                                 channel_ops, bake_tps, std_tps,
                                 force_op_evaluation, channel_filter)

    def _do_bake_operators(self, bake_tps, cached_data, start_frame, end_frame):
        f_min = f_max = None
        ranges = []

        for tps in bake_tps:
            o_range = tps[0].operator.get_frame_range(self._facade, tps[1],
                                                      tps[2])

            cached_data[tps[0]] = []

            if o_range[0] > o_range[1]:
                raise InvalidFrameRangeException('Invalid frame range (%s) '
                                                 'for operator %s.' % (
                                                 str(o_range), str(o)))
            if f_min is None or o_range[0] < f_min:
                f_min = o_range[0]
            if f_max is None or o_range[1] > f_max:
                f_max = o_range[1]
            ranges.append(o_range)

        # clamping the frame range
        if start_frame is not None and start_frame > f_min:
            f_min = start_frame

        if end_frame is not None and end_frame < f_max:
            f_max = end_frame

        frame = f_min
        while frame < f_max + 1:
            self._facade.move_to_frame(frame)
            for i in range(len(bake_tps)):
                if frame > ranges[i][0] - 1 and frame < ranges[i][1] + 1:
                    tps = bake_tps[i]
                    cached_data[tps[0]].append(
                        tps[0].operator.run(self._facade, tps[1], tps[2]))
            frame += 1

        return (f_min, f_max)

    def _do_std_operators(self, std_tps, cached_data, start_frame, end_frame):
        frame_range = None

        for tps in std_tps:
            cached_data[tps[0]] = tps[0].operator.run(self._facade, tps[1],
                                                      tps[2], start_frame,
                                                      end_frame)

            fr = tps[0].operator.get_frame_range(self._facade, tps[1], tps[2])
            if fr is not None:
                if fr[0] > fr[1]:
                    raise InvalidFrameRangeException('Invalid frame range (%s) '
                                                     'for operator %s.' % (
                                                     str(o_range), str(o)))

                if frame_range is None:
                    frame_range = list(fr)
                    continue

                if fr[0] < frame_range[0]:
                    frame_range[0] = fr[0]
                if fr[1] > frame_range[1]:
                    frame_range[1] = fr[1]

        return frame_range

    def _serialize_chunk(self, chunk, cached_data):
        return {SERIALIZATION.TYPE: SERIALIZATION_TYPES.CHUNK,
                SERIALIZATION.OPERATOR_NAME: chunk.operator.name(),
                SERIALIZATION.OPERATOR_VERSION: chunk.operator.version(),
                SERIALIZATION.OPERATOR_DATA: cached_data[chunk]}

    def _serialize_channel(self, channel, cached_data):
        data = {}

        data[SERIALIZATION.NAME] = channel.name
        data[SERIALIZATION.TYPE] = SERIALIZATION_TYPES.CHANNEL
        data[SERIALIZATION.CHUNKS] = [self._serialize_chunk(chunk, cached_data)
                                      for chunk in channel.iter_chunks()]

        return data

    def _serialize_item(self, c_item, cached_objects, cached_data):
        data = {}

        data[SERIALIZATION.NAME] = c_item.name
        data[SERIALIZATION.TYPE] = (
            SERIALIZATION_TYPES.ITEM if isinstance(c_item,
                                                   item.Item) else SERIALIZATION_TYPES.ROOT_ITEM)
        data[SERIALIZATION.ITEM_ID] = c_item.id
        data[SERIALIZATION.CHILDREN] = [
            self._serialize_item(child, cached_objects, cached_data) for child
            in c_item.iter_children()]
        data[SERIALIZATION.CHANNELS] = [
            self._serialize_channel(channel, cached_data) for channel in
            c_item.iter_channels()]
        data[SERIALIZATION.CHUNKS] = [self._serialize_chunk(chunk, cached_data)
                                      for chunk in c_item.iter_chunks()]

        return data

    def _get_used_operators(self, chunks):
        result = set()
        for c in chunks:
            result.add((c[0].operator.name(), c[0].operator.version()))
        return list(result)

    def serialize(self, file_name, objects, operators, hierarchy=False,
                  start_frame=None, end_frame=None, channel_filter=None,
                  force_op_evaluation=False):

        hierarchy = hierarchy and self._facade.support_hierarchy()

        if not operators:
            raise RuntimeError("No valid operator found.")

        item_ops = [o for o in operators if not o.is_channel_operator()]
        channel_ops = [o for o in operators if o.is_channel_operator()]
        bake_tps = []
        std_tps = []

        cached_objects = {}

        root = item.RootItem()
        root.clear()

        for s in objects:
            c_item = self._cache_object(s, root, cached_objects, item_ops,
                                        channel_ops, bake_tps, std_tps,
                                        force_op_evaluation, channel_filter)
            if hierarchy:
                self._cache_children(s, c_item, cached_objects, item_ops,
                                     channel_ops, bake_tps, std_tps,
                                     force_op_evaluation, channel_filter)

        cached_data = {}
        frame_range = self._do_std_operators(std_tps, cached_data, start_frame,
                                             end_frame)
        if bake_tps:
            bake_frame_range = self._do_bake_operators(bake_tps, cached_data,
                                                       start_frame, end_frame)

            if frame_range is None:
                frame_range = list(bake_frame_range)
            else:
                if bake_frame_range[0] < frame_range[0]:
                    frame_range[0] = bake_frame_range[0]
                if bake_frame_range[1] > frame_range[1]:
                    frame_range[1] = bake_frame_range[1]

        # This might happen when serializing data for an operator like the
        # StaticOperator where no frame range is needed
        if frame_range is None:
            frame_range = [0, 0]
        else:
            # clamping the frame range in case the input values were a smaller range
            if start_frame is not None and start_frame > frame_range[0]:
                frame_range[0] = start_frame

            if end_frame is not None and end_frame < frame_range[1]:
                frame_range[1] = end_frame

        used_operators = self._get_used_operators(bake_tps + std_tps)

        return {SERIALIZATION.KIKO_VERSION: KIKO_FILE_VERSION,
            SERIALIZATION.KIKO_OPERATORS: used_operators,
            SERIALIZATION.KIKO_FPS: self._facade.get_fps(),
            SERIALIZATION.KIKO_FRAME_RANGE: frame_range,
            SERIALIZATION.KIKO_DATA: self._serialize_item(root, cached_objects,
                                                          cached_data)}

