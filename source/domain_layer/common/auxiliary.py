from __future__ import annotations

import operator
from enum import Enum
from typing import Any

from pydantic import BaseModel, PrivateAttr


class DataType(Enum):
    TEXT = "textual"
    NUMBER = "numeric"
    BOOL = "boolean"


class BaseScenarioVariable(BaseModel):
    """A variable that simulates the environment of a scenario."""
    name: str
    datatype: DataType
    is_private: bool = False
    _value: str = PrivateAttr("None")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._value = kwargs.pop("value")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.is_value_legal(new_value):
            self._value = new_value

    def is_value_legal(self, value):
        if self.datatype == DataType.TEXT:
            return isinstance(value, str)
        elif self.datatype == DataType.NUMBER:
            if isinstance(value, str):
                return value.isnumeric()
            return isinstance(value, float) or isinstance(value, int)
        elif self.datatype == DataType.BOOL:
            if isinstance(value, str):
                return value == "True" or value == "true"
            return isinstance(value, bool)
        return False

    def __eq__(self, other):
        if isinstance(other, BaseScenarioVariable):
            return self.name == other.name and self.datatype == other.datatype

    def dict(self, **kwargs):
        var_dict = super().dict(**kwargs)
        var_dict["datatype"] = self.datatype.value
        var_dict["value"] = self.value
        return var_dict


class LegalOperator:
    _manipulation_operators = {'/': operator.truediv,
                               '*': operator.mul,
                               '+': operator.add,
                               '-': operator.sub,
                               '=': operator.eq,
                               'set': operator}

    _comparison_operators = {'<': operator.lt,
                             '>': operator.gt,
                             '>=': operator.ge,
                             '<=': operator.le,
                             '==': operator.eq,
                             '=': operator.eq,
                             'set': operator}

    @classmethod
    def comparison_operators(cls):
        return cls._comparison_operators

    @classmethod
    def manipulation_operators(cls):
        return cls._manipulation_operators

    @classmethod
    def get_comparison_operator(cls, operator_string: str):
        return cls._get_operator_from_dict(operator_string, cls._comparison_operators)

    @classmethod
    def get_manipulation_operator(cls, operator_string: str):
        return cls._get_operator_from_dict(operator_string, cls._manipulation_operators)

    @classmethod
    def get_operator(cls, operator_string: str):
        legal_operators = cls._comparison_operators.update(cls._manipulation_operators)
        return cls._get_operator_from_dict(operator_string=operator_string, legal_operators=legal_operators)

    @classmethod
    def _get_operator_from_dict(cls, operator_string: str, legal_operators: dict):
        if operator_string in legal_operators:
            return legal_operators[operator_string]
        else:
            raise ValueError("Invalid string for this type of operator. "
                             "Expected one of " + ",".join(legal_operators.keys()) + "!")


class BaseVariableChange(BaseModel):
    """Represents a change of the value of a game's variables."""
    var: BaseScenarioVariable
    _new_value: Any
    operator: str

    def __init__(self, var: BaseScenarioVariable, new_value, value_operator: str, **keyword_args):
        """
        :param var: the ScenarioVariable that will be changed.
        :param new_value: the new value of the ScenarioVariable.
        :param value_operator: the operation to change the value. Can be one of '+', '-', '/', '*' and 'set'.
        """
        super().__init__(var=var, new_value=new_value, value_operator=value_operator, **keyword_args)
        self._new_value = self._parse_new_value(var, new_value)

    @staticmethod
    def _parse_new_value(var, new_value):
        if var.is_value_legal(new_value):
            return new_value
        else:
            raise ValueError("This variable cannot have a value of this type!")

    @classmethod
    def get_operator(cls, operator_string: str):
        LegalOperator.get_manipulation_operator(operator_string)

    def __str__(self):
        return_str = str(self.var)
        return_str += self.operator + str(self._new_value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            is_equal_by_value = other.var.name == self.var.name \
                                and other.operator == self.operator \
                                and other._new_value == self._new_value
            return is_equal_by_value
        return False