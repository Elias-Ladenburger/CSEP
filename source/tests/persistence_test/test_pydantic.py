from unittest import TestCase

from pydantic import BaseModel, PrivateAttr

from infrastructure.database import CustomDB


class TestModel(BaseModel):
    test: str
    _test2: str = PrivateAttr("test2")

    def __init__(self, test: str, test2: str, **kwargs):
        super().__init__(test=test, **kwargs)
        self._test2 = test2

    def dict(self, **kwargs):
        return_dict = super().dict(**kwargs)
        return_dict.update({"_test2": self._test2})
        return return_dict


class DictConversionTest(TestCase):
    def setUp(self) -> None:
        self.model = TestModel(test="hello", test2="world")

    def tearDown(self) -> None:
        CustomDB._purge_database("scenarios")

    def test_model(self):
        print(self.model.dict())
        print(self.model._test2)
        self.assertEqual(True, True)
