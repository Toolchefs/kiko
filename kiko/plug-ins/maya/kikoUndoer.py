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

"""
This plug-in is used in maya for handling the undo
"""

import sys

from maya import OpenMaya, OpenMayaMPx

from kiko.apps.maya.mayaundohelper import MayaUndoHelper

COMMAND_NAME = 'kikoUndoer'

class KikoUndoer(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

        self._anim_curve_change = None
        self._dg_modifier = None

    def doIt(self, argList):
        argData = OpenMaya.MArgDatabase(self.syntax(), argList)

        if argData.isFlagSet('-help'):
            self.displayInfo("kikoUndoer should never be called directly. It's "
                             "used directly from Kiko to manage Maya undos.")
        else:
            if (MayaUndoHelper.anim_curve_change is None or
                                            MayaUndoHelper.dg_modifier is None):
                raise RuntimeError("Kiko critical error: could not set up "
                                   "command.")
            self._anim_curve_change = MayaUndoHelper.anim_curve_change
            self._dg_modifier = MayaUndoHelper.dg_modifier

            MayaUndoHelper.anim_curve_change = None
            MayaUndoHelper.dg_modifier = None

    def isUndoable(self):
        return True

    def undoIt(self):
        self._anim_curve_change.undoIt()
        self._dg_modifier.undoIt()

    def redoIt(self):
       self._dg_modifier.doIt()
       self._anim_curve_change.redoIt()


def cmdCreator():
    return OpenMayaMPx.asMPxPtr(KikoUndoer())

def syntaxCreator():
    syntax = OpenMaya.MSyntax()

    syntax.addFlag('-h', '-help', OpenMaya.MSyntax.kNoArg)

    syntax.enableQuery(False)
    syntax.enableEdit(False)

    return syntax


def initializePlugin(m_obj):
    mplugin = OpenMayaMPx.MFnPlugin(m_obj, 'Toolchefs', '1.0', 'Any')
    try:
        mplugin.registerCommand(COMMAND_NAME, cmdCreator, syntaxCreator)
    except:
        sys.stderr.write('Failed to register command: %s.\n' % COMMAND_NAME)
        raise


def uninitializePlugin(m_obj):
    mplugin = OpenMayaMPx.MFnPlugin(m_obj)
    try:
        mplugin.deregisterCommand(COMMAND_NAME)
    except:
        sys.stderr.write('Failed to unregister command: %s.\n' % COMMAND_NAME)
        raise
