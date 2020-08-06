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

import os
import sys
import time
import tarfile
import json
import pprint

try:
    # Python 2
    from StringIO import StringIO
    BytesIO = StringIO

except ImportError:
    # Python 3
    from io import StringIO, BytesIO

from kiko.exceptions import FileManagerError, KikoWarning
from kiko.constants import (KIKO_FILE_VERSION, KIKO_FILE_EXTENSION, KIKO_FILE,
                            SERIALIZATION, KB_FILE_EXTENSION)


class KikoFile(object):
    COMPRESSION = 'gz'

    def __init__(self, file_path):
        if file_path is None:
            raise FileManagerError("File path is None")

        f, ext = os.path.splitext(file_path)
        if not ext:
            ext = KIKO_FILE_EXTENSION
            file_path = f + KIKO_FILE_EXTENSION
        elif ext not in [KIKO_FILE_EXTENSION, KB_FILE_EXTENSION]:
            raise FileManagerError("File extension must be %s " %
                                   " or ".join([KIKO_FILE_EXTENSION,
                                                KB_FILE_EXTENSION]))

        self._data_only = ext == KB_FILE_EXTENSION
        self._file_path = file_path
        self._metadata = {SERIALIZATION.KIKO_VERSION: None,
                          KIKO_FILE.NUM_IMAGES: 0,
                          KIKO_FILE.IMAGES_EXT: None}
        self._data = {}
        self._images_ext = None
        self._image_sequence = []

    @staticmethod
    def _add_to_tar(tar_file, name, f_obj):

        # Figure out how large the file is
        pos = f_obj.tell()
        f_obj.seek(0, os.SEEK_END)
        size = f_obj.tell()
        f_obj.seek(pos)  # Restore seek position

        info = tarfile.TarInfo(name=name)
        info.size = size
        info.mtime = time.time()  # Update modified time

        # Translate Unicode to bytes, it's what tar would want
        if sys.version_info >= (3, 0):
            f_obj = BytesIO(f_obj.read().encode("utf-8"))

        tar_file.addfile(tarinfo=info, fileobj=f_obj)

    @classmethod
    def _add_to_tar_from_dict(cls, tar_file, name, data):
        io = StringIO()
        json.dump(data, io)
        io.seek(0)
        cls._add_to_tar(tar_file, name, io)

    def _add_images(self, tar_file):
        for i in range(len(self._image_sequence)):
            file_name = KIKO_FILE.SEQUENCE_FILE_NAME + "%04d" % i
            if self._images_ext is not None:
                file_name += self._images_ext

            file_name = os.path.join(KIKO_FILE.SEQUENCE_FOLDER, file_name)

            io = BytesIO()
            io.write(self._image_sequence[i])
            io.seek(0)

            self._add_to_tar(tar_file, file_name, io)

    def save(self):
        if not self._data:
            raise FileManagerError("Can not save. No data was found.")

        if self._data_only:
            self._save_data_only()
            return

        tar_file = tarfile.open(self._file_path, 'w:' + self.COMPRESSION)

        self._metadata[SERIALIZATION.KIKO_VERSION] = KIKO_FILE_VERSION

        self._add_to_tar_from_dict(tar_file, KIKO_FILE.METADATA, self._metadata)
        self._add_to_tar_from_dict(tar_file, KIKO_FILE.DATA, self._data)
        self._add_images(tar_file)

        tar_file.close()

    def _save_data_only(self):
        with open(self._file_path, 'w') as f:
            json.dump(self._data, f)

    @property
    def version(self):
        if self._data_only:
            return self._data[SERIALIZATION.KIKO_VERSION]
        return self._metadata[SERIALIZATION.KIKO_VERSION]

    def get_data(self):
        return self._data

    def set_data(self, value):
        if not isinstance(value, dict):
            raise FileManagerError("The given data is not a dict.")
        self._data = value

    data = property(get_data, set_data)

    def _parse_data_only(self):
        f = open(self._file_path, 'rb')
        self._data = json.load(f)
        f.close()

    def parse(self):
        if not os.path.exists(self._file_path):
            raise FileManagerError('%s does not exist.' % self._file_path)

        if self._data_only:
            self._parse_data_only()
            return

        tar_file = tarfile.open(self._file_path, 'r:' + self.COMPRESSION)

        metadata_member = tar_file.getmember(KIKO_FILE.METADATA)
        if metadata_member:
            self._metadata = json.load(tar_file.extractfile(metadata_member))

        data_member = tar_file.getmember(KIKO_FILE.DATA)
        if data_member:
            self._data = json.load(tar_file.extractfile(data_member))

        # Extracting images
        self._image_sequence = []
        for i in range(self._metadata[KIKO_FILE.NUM_IMAGES]):
            file_name = os.path.join(KIKO_FILE.SEQUENCE_FOLDER,
                                     KIKO_FILE.SEQUENCE_FILE_NAME + "%04d" % i)

            if self._metadata[KIKO_FILE.IMAGES_EXT] is not None:
                file_name += self._metadata[KIKO_FILE.IMAGES_EXT]

            f = tar_file.extractfile(tar_file.getmember(file_name))
            self._image_sequence.append(f.read())

    def set_images(self, images):
        if not isinstance(images, list):
            raise FileManagerError("Please provide a list of files as images.")

        self._metadata[KIKO_FILE.NUM_IMAGES] = len(images)
        self._image_sequence = []
        for f in images:
            f = open(f, 'rb')
            self._image_sequence.append(f.read())
            f.close()

        if self._image_sequence:
            _, self._images_ext = os.path.splitext(images[0])
            self._metadata[KIKO_FILE.IMAGES_EXT] = self._images_ext

    def get_image(self, index):
        if index < len(self._image_sequence):
            return self._image_sequence[index]

    @property
    def num_images(self):
        return len(self._image_sequence)

    # TODO: make this so that dict and lists are printed on the same line
    def print_data(self):
        pprint.PrettyPrinter(indent=4).pprint(self._data)
