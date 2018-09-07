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


from abc import ABCMeta, abstractmethod

from kiko.constants import IMPORT_METHODS
from kiko.exceptions import InvalidFacadeException
from kiko.apps.basefacade import BaseFacade

class BaseDeserializer(object):
    __metaclass__ = ABCMeta

    def __init__(self, facade):
        if not issubclass(facade, BaseFacade):
            raise InvalidFacadeException('Invalid facade provided.')
        self._facade = facade

    @abstractmethod
    def version(self):
        pass

    @abstractmethod
    def load_data(self, root, objects, op_priority=None,
                  import_obj_method=IMPORT_METHODS.OBJECT.NAME,
                  import_anim_method=IMPORT_METHODS.ANIMATION.APPLY,
                  str_replacements=None, obj_mapping=None, prefix_to_add=None,
                  suffix_to_add=None, frame_value=0, time_multiplier=1,
                  start_frame=None, end_frame=None):
        pass

    @abstractmethod
    def get_root_from_data(self, data, flatten_hierarchy=False,
                           ignore_item_chunks=False):
        pass
