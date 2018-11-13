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

PYSIDE_VERSION = None

from kiko.utils.host import get_host
from kiko.constants import APPS

try:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QtWidgets
    #houdini does not have a shiboken module
    try:
        import shiboken
    except:
        try:
            import PySide.shiboken as shiboken
        except:
            pass
    PYSIDE_VERSION = 1
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    if get_host() == APPS.HOUDINI:
        from PySide2 import shiboken2 as shiboken
    else:
        import shiboken2 as shiboken
    PYSIDE_VERSION = 2


if PYSIDE_VERSION == 1:
    setattr(QtCore, "QSortFilterProxyModel", QtWidgets.QSortFilterProxyModel)
    setattr(QtCore, "QStringListModel", QtWidgets.QStringListModel)
    setattr(QtCore, "QItemSelection", QtWidgets.QItemSelection)
    setattr(QtCore, "QItemSelectionModel", QtWidgets.QItemSelectionModel)
    setattr(QtCore, "QAbstractProxyModel", QtWidgets.QAbstractProxyModel)
    setattr(QtCore, "QStringListModel", QtWidgets.QStringListModel)
    setattr(QtWidgets.QHeaderView, "setSectionResizeMode",
            QtGui.QHeaderView.setResizeMode)
    setattr(QtWidgets.QHeaderView, "setSectionsMovable",
            QtGui.QHeaderView.setMovable)
    setattr(QtWidgets.QHeaderView, "setSectionsClickable",
            QtGui.QHeaderView.setClickable)



