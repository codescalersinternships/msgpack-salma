import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from deserializer import MsgPackDeserializer
from serializer import MsgPackSerializer


class TestMsgPack(unittest.TestCase):
    def test_unsigned_int(self):
        testcases = [126, 65515, 429496729, 1844674407370955161]
        for test in testcases:
            packed = MsgPackSerializer.serialize(test)
            self.assertEqual(test, MsgPackDeserializer.deserializer(packed))

    def test_signed_int(self):
        testcases = [
            -128,
            -1,
            0,
            -32768,
            -2147483648,
            -9223372036854775808,
        ]
        for test in testcases:
            packed = MsgPackSerializer.serialize(test)
            self.assertEqual(test, MsgPackDeserializer.deserializer(packed))

    def test_boolean(self):
        testcases = [True, False]
        for test in testcases:
            packed = MsgPackSerializer.serialize(test)
            self.assertEqual(test, MsgPackDeserializer.deserializer(packed))

    def test_float(self):
        testcases = [
            0.0,
            1.0,
            -1.0,
            3.141592653589793,
            2.718281828459045,
            1.2345678901234567,
            -1.2345678901234567,
        ]
        for test in testcases:
            packed = MsgPackSerializer.serialize(test)
            self.assertEqual(test, MsgPackDeserializer.deserializer(packed))

    def test_string(self):
        testcases = [
            "",
            "hello",
            "Hello, MessagePack!",
            "string with newline\nand tab\tcharacters",
        ]
        for test in testcases:
            packed = MsgPackSerializer.serialize(test)
            self.assertEqual(test, MsgPackDeserializer.deserializer(packed))

if __name__ == "__main__":
    unittest.main()
