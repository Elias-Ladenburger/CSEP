from unittest import TestCase

from pydantic import BaseModel, PrivateAttr, Field

from infrastructure_layer.database import CustomDB


class TestModel(BaseModel):
    test: str
    _test2: str = PrivateAttr("test2")
    _test3: str = Field("test3", alias="test3")
    _test4: str = PrivateAttr(Field(default="default text", alias="test4"))

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
        self.assertTrue("_test2" in self.model.dict())

    def test_access_by_alias(self):
        print(self.model._test3)

    def test_set_protected_attribute(self):
        self.model._test3 = "another test"
        print(self.model._test3)

    def test_access_via_alias(self):
        print(self.model._test3)

    def test_pydantic_dict(self):
        print(self.model.dict())

    def test_pydantic_dict_include_private(self):
        dict = self.model.dict(include={"_test2", "_test3", "_test4"})
        print(dict)
