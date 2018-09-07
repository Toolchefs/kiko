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

############################################
# CORE
############################################

class InvalidItemException(Exception):
    pass

class InvalidChannelException(Exception):
    pass

class InvalidChunkException(Exception):
    pass

class InvalidParentChunkExpception(Exception):
    pass

############################################
# APPS
############################################

class InvalidFacadeException(Exception):
    pass

class FacadeRuntimeError(Exception):
    pass

############################################
# FACTORY
############################################

class InvalidFactoryException(Exception):
    pass

class InvalidClassException(Exception):
    pass

class InvalidOperatorName(Exception):
    pass

############################################
# MANAGER
############################################

class KikoManagerException(Exception):
    pass

############################################
# OPERATORS
############################################

class InvalidOperator(Exception):
    pass

class InvalidOperatorLoaderException(Exception):
    pass

############################################
# IO
############################################

class KikoDeserializeException(Exception):
    pass

class InvalidDeserializerException(Exception):
    pass

class FileManagerError(Exception):
    pass

############################################
# OTHERS
############################################

class InvalidHostException(Exception):
    pass

class InvalidOperation(Exception):
    pass

class InvalidFrameRangeException(Exception):
    pass

############################################
# WARNINGS
############################################
class KikoWarning(Warning):
    pass

class FacadeWarning(Warning):
    pass
