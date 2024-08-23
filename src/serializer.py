import struct

from constants import *


class MsgPackSerializer:

    @staticmethod
    def _serialize_signed_int(value):
        if -127 <= value <= 127:
            return bytes([INT8, value])
        elif -32768 <= value <= 32767:
            return bytes([INT16]) + struct.pack(">h", value)
        elif -2147483648 <= value <= 2147483647:
            return bytes([INT32]) + struct.pack(">i", value)
        elif -9223372036854775808 <= value <= 9223372036854775808:
            return bytes([INT64]) + struct.pack(">q", value)
        else:
            raise ValueError("number exceeds the maximum value")

    @staticmethod
    def _serialize_unsigned_int(value):
        if 0 <= value <= 255:
            return bytes([UINT8, value])
        elif 256 <= value <= 65535:
            return bytes([UINT32]) + struct.pack(">H", value)
        elif 65536 <= value <= 4294967295:
            return bytes([UINT32]) + struct.pack(">I", value)
        elif 4294967296 <= value <= 18446744073709551615:
            return bytes([UINT64]) + struct.pack(">Q", value)
        else:
            raise ValueError("number exceeds the maximum value")

    @staticmethod
    def _serialize_boolean(value):
        if value:
            return TRUE

        return FALSE

    @staticmethod
    def _serialize_float(value, single_percision=False):
        if single_percision:
            return bytes([FLOAT32]) + struct.pack(">f", value)

        return bytes([FLOAT64]) + struct.pack(">d", value)

    @staticmethod
    def _serialize_str(value):
        size = len(value)
        if size <= 255:
            return bytes([STR8]) + struct.pack(">B", size) + value.encode("utf-8")
        elif 256 <= size <= 65535:
            return bytes([STR16]) + struct.pack(">H", size) + value.encode("utf-8")
        elif 65536 <= size <= 4294967295:
            return bytes([STR32]) + struct.pack(">I", size) + value.encode("utf-8")
        else:
            raise ValueError("length of str exceed the maximum length to serialize")

    @staticmethod
    def _serialize_array(value):
        length = len(value)

        if length <= 65535:
            prefix = ARRAY16
            length_field = struct.pack(">H", length)
        elif length <= 4294967295:
            prefix = ARRAY32
            length_field = struct.pack(">I", length)
        else:
            raise ValueError("length can't be serialized")
        serialized_elements = [
            MsgPackSerializer.serialize(element) for element in value
        ]
        if not all(isinstance(elem, bytes) for elem in serialized_elements):
            raise TypeError("Serialization resulted in non-bytes objects")

        return bytes([prefix]) + length_field + b"".join(serialized_elements)

    @staticmethod
    def _serialize_map(value):
        length = len(value)

        if length <= 65535:
            prefix = MAP16
            length_field = struct.pack(">H", length)
        elif length <= 4294967295:
            prefix = MAP32
            length_field = struct.pack(">I", length)
        else:
            raise ValueError("length can't be serialized")
        serialized_items = b"".join(
            MsgPackSerializer.serialize(key) + MsgPackSerializer.serialize(value)
            for key, value in value.items()
        )
        return bytes([prefix]) + length_field + serialized_items

    @staticmethod
    def serialize(value, single_percision=False):
        if isinstance(value, int):
            if value < 0:
                return MsgPackSerializer._serialize_signed_int(value)
            else:
                return MsgPackSerializer._serialize_unsigned_int(value)
        elif isinstance(value, bool):
            return bytes(MsgPackSerializer._serialize_boolean(value))
        elif isinstance(value, str):
            return MsgPackSerializer._serialize_str(value)
        elif isinstance(value, float):
            return MsgPackSerializer._serialize_float(value, single_percision)
        elif isinstance(value, list):
            return MsgPackSerializer._serialize_array(value)
        elif isinstance(value, dict):
            return MsgPackSerializer._serialize_map(value)
        elif value is None:
            return bytes([NIL])
        else:
            raise TypeError(f"unsupported type: {type(value)}")


if __name__ == "__main__":
    print("----------------------")
    print(
        MsgPackSerializer.serialize(
            {
                "key": "value",
                "number": 123,
                "array": [1, 2, 3],
                "nested": {"a": True, "b": None},
            }
        )
    )
    print("-----------------------------")
