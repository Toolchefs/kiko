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

import sys

from collections import OrderedDict

from kiko.exceptions import InvalidClassException, InvalidFacadeException
from kiko.operators.baseoperator import BaseOperator
from kiko.apps.basefacade import BaseFacade
from kiko.utils.patterns import Singleton

class OperatorsFactory(Singleton):

    def __init__(self):
        self._entries = OrderedDict()

    @property
    def name(self):
        return self._name

    def register(self, operator_class):
        if not issubclass(operator_class, BaseOperator):
            raise InvalidClassException("The given class is not a BaseOperator "
                                        "subclass.")

        name = operator_class.name()
        ver = operator_class.version()
        entry = self._entries.get(name)
        if entry:
            entry[int(ver)] = operator_class
        else:
            self._entries[name] = {int(ver): operator_class}

    def has_operator(self, name, version=None):
        if version is None:
            return name in self._entries
        return name in self._entries and int(version) in self._entries[name]

    def get_all_operator_names(self, app=None):
        if app is None:
            return self._entries.keys()

        res = set()
        for versions in self._entries.values():
            for c in versions.values():
                if c.is_app_supported(app):
                    res.add(c.name())
                break
        return list(res)

    def get_channel_operator_names(self, app=None):
        res = set()
        for versions in self._entries.values():
            for c in versions.values():
                if c.is_channel_operator() and (app is None or
                                                c.is_app_supported(app)):
                    res.add(c.name())
                break
        return list(res)

    def get_item_operator_names(self, app=None):
        res = set()
        for versions in self._entries.values():
            for c in versions.values():
                import os
                if not c.is_channel_operator() and (app is None or
                                                    c.is_app_supported(app)):
                    res.add(c.name())
                break
        return list(res)

    def get_operator(self, name, version):
        if name in self._entries and int(version) in self._entries[name]:
            return self._entries[name][int(version)]

    def create(self, name, version, facade, node, channel=None):
        if not isinstance(facade, BaseFacade):
            raise InvalidFacadeException('You need to provide a valid facade '
                                         'to create an operator')

        if name in self._entries and int(version) in self._entries[name]:
            return self._entries[name][int(version)](facade, node,
                                                     channel=channel)

    def get_latest_version(self, name):
        if name not in self._entries:
            return None

        versions = list(self._entries[name].keys())
        versions.sort()
        return versions[-1]

    def remove_operator(self, name):
        del self._entries[name]

    def clear_operators(self):
        self._entries.clear()

    def reload_operators(self):
        for name, versions in self._entries.items():
            for ver, constructor in versions.items():
                module_name = constructor.__module__
                class_name = constructor.__name__

                del sys.modules[module_name]
                self._entries[name][ver] = __import__(module_name, globals(),
                                                      locals(), [class_name])
