
from kiko.constants import SERIALIZATION

from kiko.exceptions import (KikoDeserializeException,
                             InvalidDeserializerException)
from kiko.io.basedeserializer import BaseDeserializer
from . import v1

class DeserializerManager:
    _deserializers = {}

    @classmethod
    def get_deserializer(cls, version, facade):
        d = cls._deserializers.get(version)
        if d is None:
            raise InvalidDeserializerException('Can not find kiko deserializer '
                                               'version %d' % version)

        return d(facade)

    @classmethod
    def register_deserializer(cls, deserializer):
        if not issubclass(deserializer, BaseDeserializer):
            raise InvalidDeserializerException("Invalid deserializer")

        cls._deserializers[deserializer.version()] = deserializer

DeserializerManager.register_deserializer(v1.DeserializerV1)
