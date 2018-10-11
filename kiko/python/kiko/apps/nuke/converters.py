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

import nuke


def convert_camera_aperture(node, knob, index, value, t=None):
    # inch to mm conversion
    return value * 25.4


def convert_camera_win_translates(node, knob, index, value, t=None):
    if index == 0:
        if t is None:
            ha = node.knob("haperture").value()
        else:
            ha = node.knob("haperture").valueAt(t)
        return (2 / ha) * (value * 25.4)
    else:
        if t is None:
            va = node.knob("vaperture").value()
        else:
            va = node.knob("vaperture").valueAt(t)

        h = float(nuke.root().format().height())
        w = float(nuke.root().format().width())
        return (h / w) * 2 / va * (value * 25.4)
    

def convert_camera_aperture_to_kiko(node, knob, index, value, t=None):
    # mm to inch conversion
    return value / 25.4


def convert_camera_win_translates_to_kiko(node, knob, index, value, t=None):
    if index == 0:
        if t is None:
            ha = node.knob("haperture").value()
        else:
            ha = node.knob("haperture").valueAt(t)
        
        return value * ha / (2 * 25.4)
    else:
        if t is None:
            va = node.knob("vaperture").value()
        else:
            va = node.knob("vaperture").valueAt(t)

        h = float(nuke.root().format().height())
        w = float(nuke.root().format().width())
        return (w * value * va) / (2 * h * 25.4)


KIKO_TO_NUKE_CONVERTERS = {
    'Camera': {'haperture': convert_camera_aperture,
               'vaperture': convert_camera_aperture,
               'win_translate': convert_camera_win_translates}
}
KIKO_TO_NUKE_CONVERTERS['Camera2'] = KIKO_TO_NUKE_CONVERTERS['Camera']

NUKE_TO_KIKO_CONVERTERS = {
    'Camera2': {'haperture': convert_camera_aperture_to_kiko,
                'vaperture': convert_camera_aperture_to_kiko,
                'win_translate': convert_camera_win_translates_to_kiko}
}


def get_kiko_to_nuke_converter(node, knob):
    nd = KIKO_TO_NUKE_CONVERTERS.get(node.Class())
    if nd is None:
        return
    return nd.get(knob.name())


def get_nuke_to_kiko_converter(node, knob):
    nd = NUKE_TO_KIKO_CONVERTERS.get(node.Class())
    if nd is None:
        return
    return nd.get(knob.name())
