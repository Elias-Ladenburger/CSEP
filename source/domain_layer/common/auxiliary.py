from __future__ import annotations

import operator
from enum import Enum

from pydantic import BaseModel, PrivateAttr


"""This module contains classes that are used by both injects and scenarios."""


def convert_to_number(value_candidate):
    if isinstance(value_candidate, str):
        if value_candidate.isdigit():
            return int(value_candidate)
        elif value_candidate.isnumeric():
            return float(value_candidate)
    elif isinstance(value_candidate, int) or isinstance(value_candidate, float):
        return value_candidate
    raise ValueError("{} should be either an integer or a float!".format(value_candidate))


def convert_to_boolean(value_candidate):
    if isinstance(value_candidate, str):
        if value_candidate.lower() in ["true", "yes"]:
            return True
        elif value_candidate.lower() in ["false", "no"]:
            return False
    elif isinstance(value_candidate, bool):
        return value_candidate
    raise ValueError("{} should be a boolean!".format(value_candidate))


class DataType(str, Enum):
    def __new__(cls, value, parse_function):
        datatype = str.__new__(cls, value)
        datatype._value_ = value
        datatype.parse_value = parse_function
        return datatype

    TEXT = ("textual", lambda x: x)
    NUMBER = ("numeric", convert_to_number)
    BOOL = ("boolean", convert_to_boolean)


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
        self._value = self.datatype.parse_value(new_value)

    def is_value_legal(self, value):
        """
        Validate whether this variable can hold a given value.
        """
        try:
            self.datatype.parse_value(value)
            return True
        except ValueError as ve:
            return False

    def legal_value(self, value_candidate):
        return self.datatype.parse_value(value_candidate)

    def __eq__(self, other):
        if isinstance(other, BaseScenarioVariable):
            return self.name == other.name and self.datatype == other.datatype

    def dict(self, **kwargs):
        var_dict = super().dict(**kwargs)
        var_dict["datatype"] = self.datatype.value
        var_dict["value"] = self.value
        return var_dict


class LegalOperator:
    """A collection class for easy access to legal operators."""
    _manipulation_operators = {"/": operator.truediv,
                               "*": operator.mul,
                               "+": operator.add,
                               "-": operator.sub,
                               "=": "set",
                               "set": "set"}

    _comparison_operators = {"<": operator.lt,
                             ">": operator.gt,
                             ">=": operator.ge,
                             "<=": operator.le,
                             "==": operator.eq}

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
        legal_operators = cls._comparison_operators
        legal_operators.update(cls._manipulation_operators)
        return cls._get_operator_from_dict(operator_string=operator_string, legal_operators=legal_operators)

    @classmethod
    def _get_operator_from_dict(cls, operator_string: str, legal_operators: dict):
        if operator_string in legal_operators:
            return_operator = legal_operators[operator_string]
            return return_operator
        else:
            raise ValueError("Invalid string for this type of operator. "
                             "Expected one of " + ",".join(legal_operators.keys()) + "!")


class BaseVariableChange(BaseModel):
    """Represents a change of the value of a game's variables."""
    var: BaseScenarioVariable
    _new_value: str = PrivateAttr("")
    operator: str

    def __init__(self, var: BaseScenarioVariable, new_value, operator: str, **keyword_args):
        """
        :param var: the ScenarioVariable that will be changed.
        :param new_value: the new value of the ScenarioVariable.
        :param value_operator: the operation to change the value. Can be one of '+', '-', '/', '*' and 'set'.
        """
        if isinstance(var, dict):
            var = BaseScenarioVariable(**var)
        super().__init__(var=var, new_value=new_value, operator=operator, **keyword_args)
        self._new_value = self._parse_new_value(var, new_value)

    @property
    def new_value(self):
        return self._new_value

    @staticmethod
    def _parse_new_value(var, new_value):
        if var.is_value_legal(new_value):
            return var.legal_value(new_value)
        else:
            raise ValueError("The variable {} must have a value of type {}!".format(var.name, var.datatype.value))

    @classmethod
    def get_operator(cls, operator_string: str):
        return LegalOperator.get_manipulation_operator(operator_string)

    def dict(self, **kwargs):
        return_dict = super().dict(**kwargs)
        return_dict["new_value"] = self.new_value
        return return_dict

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
