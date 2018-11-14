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
from kiko.ui.exporter import KikoExporterDialog
from kiko.ui.mixed import create_box_layout, ORIENTATION


class MayaExporterPreferences(QtWidgets.QWidget):
    def __init__(self):
        super(MayaExporterPreferences, self).__init__()
        self._layout = create_box_layout(ORIENTATION.VERTICAL)
        self.setLayout(self._layout)

        self._build_widgets()
        self._initialize_widgets()

    def _build_widgets(self):
        self._ignore_shapes_in_hierarchy = QtWidgets.QCheckBox("Ignore shapes")
        self._layout.addWidget(self._ignore_shapes_in_hierarchy)

        self._use_referenced_anim_curves = QtWidgets.QCheckBox("Use referenced "
                                                               "anim curves")
        self._layout.addWidget(self._use_referenced_anim_curves)

        self._layout.addStretch(1)

    def _initialize_widgets(self):
        use_references = MayaPreferences.use_referenced_anim_curves
        self._use_referenced_anim_curves.setChecked(use_references)

        ignore_shapes = MayaPreferences.ignore_shapes_in_hierarchy
        self._ignore_shapes_in_hierarchy.setChecked(ignore_shapes)

    def set_preferences(self):
        ignore_shapes = self._ignore_shapes_in_hierarchy.isChecked()
        MayaPreferences.ignore_shapes_in_hierarchy = ignore_shapes

        use_references = self._use_referenced_anim_curves.isChecked()
        MayaPreferences.use_referenced_anim_curves = use_references


class MayaExporterDialog(KikoExporterDialog):
    def __init__(self):
        super(MayaExporterDialog, self).__init__(manager.MayaKikoManager(),
                            app_preference_widget=MayaExporterPreferences())

        self.setParent(MayaFacadeHelper.get_main_window())
        self.setWindowFlags(QtCore.Qt.Window)
