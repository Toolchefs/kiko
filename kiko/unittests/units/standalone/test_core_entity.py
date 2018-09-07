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

from nose.tools import (assert_false, assert_true, assert_equal,
                        assert_not_equal, assert_almost_equal, assert_raises,
                        nottest)

from kiko.core.entity import item
from kiko.core.entity import chunk
from kiko.core.entity import channel

from kiko.exceptions import (InvalidItemException, InvalidParentChunkExpception,
                             InvalidOperation)


class TestItem(object):
    TEST_ITEM_NAME = "test_item"
    TEST_CHANNEL_NAME = "test_channel"

    def setUp(self):
        self._root = item.RootItem()
        self._test_item = item.Item(self._root, self.TEST_ITEM_NAME)

    def tearDown(self):
        return

    def abstract_classes_test(self):
        assert_raises(TypeError, item.BaseItem, None, "")
        assert_raises(TypeError, chunk.Chunk, None, "")

    def item_hierarchy_test(self):
        assert_equal(self._test_item.parent, self._root)
        assert_equal(self._test_item.name, self.TEST_ITEM_NAME)

        item_names = ["a", "b", "c"]

        item2 = item.Item(self._test_item, item_names[0])
        item.Item(self._test_item, item_names[1])
        item.Item(self._test_item, item_names[2])

        assert_equal(self._test_item.get_children_names(), item_names)

        assert_equal(self._test_item.num_children, 3)
        assert_equal(self._test_item.child('a'), item2)
        assert_equal(self._test_item.child_by_index(0), item2)

        self._test_item.remove_child(item2)
        assert_equal(self._test_item.num_children, 2)
        c = self._test_item.child('c')
        assert_equal(self._test_item.child_by_index(1), c)

        self._test_item.remove_child_by_name(c.name)
        assert_equal(self._test_item.num_children, 1)

    def item_channels_test(self):
        p = channel.Channel(self._test_item, self.TEST_CHANNEL_NAME)
        assert_raises(InvalidItemException, channel.Channel, self._root,
                      self.TEST_CHANNEL_NAME)

        assert_equal(p.parent, self._test_item)
        assert_equal(p.name, self.TEST_CHANNEL_NAME)

        chan_names = [self.TEST_CHANNEL_NAME, "testChanne2", "testChanne3"]

        chan = channel.Channel(self._test_item, chan_names[1])
        channel.Channel(self._test_item, chan_names[2])

        assert_equal(self._test_item.get_channel_names(), chan_names)

        assert_equal(self._test_item.num_channels, 3)
        c = self._test_item.channel('testChanne2')
        assert_equal(chan, c)

        self._test_item.remove_channel(c)
        assert_equal(self._test_item.num_channels, 2)

        self._test_item.remove_channel_by_name("testChanne3")
        assert_equal(self._test_item.num_channels, 1)

    def item_chunk_test(self):
        chan = channel.Channel(self._test_item, "testChannel")
        assert_raises(InvalidParentChunkExpception, chunk.ItemChunk, chan)

        chunk_names = ["test1", "test2", "test3"]

        ic = chunk.ItemChunk(self._root, operator_name=chunk_names[0],
                             operator_ver=1)
        assert_equal(ic.parent, self._root)

        chunk.ItemChunk(self._root, operator_name=chunk_names[1],
                        operator_ver=1)
        chunk.ItemChunk(self._root, operator_name=chunk_names[2],
                        operator_ver=1)

        assert_equal(self._root.get_chunk_names(), chunk_names)

        assert_equal(self._root.num_chunks, 3)
        c = self._root.chunk('test1')
        assert_equal(c, ic)

        self._root.remove_chunk(ic)
        assert_equal(self._root.num_chunks, 2)

        self._root.remove_chunk_by_name("test3")
        assert_equal(self._root.num_chunks, 1)

    def channel_chunk_test(self):
        assert_raises(InvalidParentChunkExpception, chunk.ChannelChunk, self._test_item,
                      None, "test", 1)

        chan = channel.Channel(self._test_item, "testChannel")

        chunk_names = ["test1", "test2", "test3"]

        cc = chunk.ChannelChunk(chan, operator_name=chunk_names[0],
                                operator_ver=1)
        assert_equal(cc.parent, chan)

        chunk.ChannelChunk(chan, operator_name=chunk_names[1],
                           operator_ver=1)
        chunk.ChannelChunk(chan, operator_name=chunk_names[2],
                           operator_ver=1)

        assert_equal(chan.get_chunk_names(), chunk_names)

        assert_equal(chan.num_chunks, 3)
        c = chan.chunk(chunk_names[0])
        assert_equal(c, cc)

        chan.remove_chunk(cc)
        assert_equal(chan.num_chunks, 2)

        chan.remove_chunk_by_name(chunk_names[2])
        assert_equal(chan.num_chunks, 1)


    def item_rename_test(self):
        item.Item(self._test_item, "a")
        item_ = item.Item(self._test_item, "b")
        item.Item(self._test_item, "c")

        test_name = "test_name"
        item_.name = test_name

        assert_equal(self._test_item.child(test_name), item_)
        assert_equal(self._test_item.child_by_index(1), item_)

