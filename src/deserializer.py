import struct

from constants import *


class MsgPackDeserializer:
    @staticmethod
    def _deserialize_unsigned_int(data):
        type = data[0]
        if type == UINT8:
            return struct.unpack(">B", data[1:2])[0], data[2:]
        elif type == UINT16:
            return struct.unpack(">H", data[1:3])[0], data[3:]
        elif type == UINT32:
            return struct.unpack(">I", data[1:5])[0], data[5:]

        return struct.unpack(">Q", data[1:9])[0], data[9:]

    @staticmethod
    def _deserialize_signed_int(data):
        type = data[0]
        if type == INT8:
            return struct.unpack(">b", data[1:2])[0], data[2:]
        elif type == INT16:
            return struct.unpack(">h", data[1:3])[0], data[3:]
        elif type == INT32:
            return struct.unpack(">i", data[1:5])[0], data[5:]

        return struct.unpack(">q", data[1:9])[0], data[9:]

    @staticmethod
    def _deserialize_boolean(data):
        if data[0] == TRUE:
            return True, data[1:]

        return False, data[1:]

    @staticmethod
    def _deserialize_float(data):
        if data[0] == FLOAT32:
            return struct.unpack(">f", data[1:5])[0], data[5:]

        return struct.unpack(">d", data[1:9])[0], data[9:]

    @staticmethod
    def _deserialize_str(data):
        type = data[0]
        if type == STR8:
            length = struct.unpack(">B", data[1:2])[0]
            return data[2 : 2 + length].decode("utf-8"), data[2 + length :]
        elif type == STR16:
            length = struct.unpack(">H", data[1:3])[0]
            return data[3 : 3 + length].decode("utf-8"), data[3 + length :]

        length = struct.unpack(">I", data[1:5])[0]
        return data[5 : 5 + length].decode("utf-8"), data[5 + length :]

    @staticmethod
    def _deserialize_array(data):
        elements = []
        length = 0
        pointer = 0
        if data[0] == ARRAY16:
            length = struct.unpack(">H", data[1:3])[0]
            pointer = 3
        else:
            length = struct.unpack(">I", data[1:5])[0]
            pointer = 5
        for _ in range(length):
            element, remaining = MsgPackDeserializer._deserializer(data[pointer:])
            elements.append(element)
            pointer = len(data) - len(remaining)
        return elements, data[pointer:]

    @staticmethod
    def _deserialize_map(data):
        map = {}
        length = 0
        pointer = 0
        if data[0] == MAP16:
            length = struct.unpack(">H", data[1:3])[0]
            pointer = 3
        else:
            length = struct.unpack(">I", data[1:5])[0]
            pointer = 5
        for _ in range(length):
            key, remaining = MsgPackDeserializer._deserializer(data[pointer:])
            pointer = len(data) - len(remaining)
            value, remaining = MsgPackDeserializer._deserializer(data[pointer:])
            pointer = len(data) - len(remaining)
            map[key] = value
        return map, data[pointer:]

    @staticmethod
    def _deserializer(data):
        type = data[0]
        if type in [UINT8, UINT16, UINT32, UINT64]:
            return MsgPackDeserializer._deserialize_unsigned_int(data)
        elif type in [INT8, INT16, INT32, INT64]:
            return MsgPackDeserializer._deserialize_signed_int(data)
        elif type in [FALSE, TRUE]:
            return MsgPackDeserializer._deserialize_boolean(data)
        elif type in [STR8, STR16, STR32]:
            return MsgPackDeserializer._deserialize_str(data)
        elif type in [ARRAY16, ARRAY32]:
            return MsgPackDeserializer._deserialize_array(data)
        elif type in [MAP16, MAP32]:
            return MsgPackDeserializer._deserialize_map(data)
        elif type == NIL:
            return None, data[1:]
        else:
            raise TypeError(f"unsupported type: {type(data[0])}")

    @staticmethod
    def deserializer(data):
        return MsgPackDeserializer._deserializer(data)[0]


if __name__ == "__main__":
    print("----------------------")
    print(
        MsgPackDeserializer.deserializer(
            b"\xde\x00\x04\xd9\x03key\xd9\x05value\xd9\x06number\xcc{\xd9\x05array\xdc\x00\x03\xcc\x01\xcc\x02\xcc\x03\xd9\x06nested\xde\x00\x02\xd9\x01a\xcc\x01\xd9\x01b\xc0"
        )
    )
    print("-----------------------------")
