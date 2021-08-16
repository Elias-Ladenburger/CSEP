from enum import Enum
from unittest import TestCase


class TestEnum(Enum):
    HELLO = "hello"
    GOODBYE = "bye"

class EnumTest(TestCase):

    def test_enum_serialization(self):
        test_value = TestEnum.GOODBYE
        print(test_value)
        print(test_value.value)
        new_enum = TestEnum("hello")
        print(new_enum)
