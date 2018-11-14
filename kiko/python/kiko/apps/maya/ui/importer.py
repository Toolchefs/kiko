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


from kiko.ui.qthandler import QtWidgets, QtCore

from kiko.apps.maya import manager
from kiko.apps.maya.mayafacade import MayaFacadeHelper
from kiko.apps.maya.mayapreferences import MayaPreferences
from kiko.ui.importer import KikoImporterDialog
from kiko.ui.mixed import create_box_layout, ORIENTATION


class MayaImporterPreferences(QtWidgets.QWidget):
    def __init__(self):
        super(MayaImporterPreferences, self).__init__()
        self._layout = create_box_layout(ORIENTATION.VERTICAL)
        self.setLayout(self._layout)

        self._build_widgets()
        self._initialize_widgets()

    def _build_widgets(self):
        self._break_all = QtWidgets.QCheckBox("Break all connections in apply "
                                              "mode")
        self._layout.addWidget(self._break_all)

        self._layout.addStretch(1)

    def _initialize_widgets(self):
        self._break_all.setChecked(
                            MayaPreferences.break_all_connections_in_apply_mode)

    def set_preferences(self):
        break_all = self._break_all.isChecked()
        MayaPreferences.break_all_connections_in_apply_mode = break_all


class MayaImporterDialog(KikoImporterDialog):
    def __init__(self):
        super(MayaImporterDialog, self).__init__(manager.MayaKikoManager(),
                            app_preference_widget=MayaImporterPreferences())

        self.setParent(MayaFacadeHelper.get_main_window())
        self.setWindowFlags(QtCore.Qt.Window)
