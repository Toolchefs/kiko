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

from kiko.constants import APPS
from kiko.exceptions import InvalidHostException

_HOST = None


def get_host():
    global _HOST
    if not _HOST is None:
        return _HOST

    module_dicts = {APPS.MAYA: 'maya',
                    APPS.NUKE: 'nuke',
                    APPS.HOUDINI: 'hou'}

    for key, value in module_dicts.items():
        try:
            __import__(value)
            _HOST = key
            return _HOST
        except ImportError:
            pass

    raise InvalidHostException("Could not find valid host.")


def set_host(host):
    global _HOST
    _HOST = host


