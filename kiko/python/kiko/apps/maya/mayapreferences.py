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


class MayaPreferences:
    ignore_shapes_in_hierarchy = True
    break_all_connections_in_apply_mode = False
    use_referenced_anim_curves = False
    use_full_paths = False

    @classmethod
    def reset(cls):
        cls.ignore_shapes_in_hierarchy = True
        cls.break_all_connections_in_apply_mode = False
        cls.use_referenced_anim_curves = False
        cls.use_full_paths = False
