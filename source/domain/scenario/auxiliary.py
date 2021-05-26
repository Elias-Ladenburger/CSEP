import operator
from enum import Enum


class Image:
    def __init__(self, image_path="", image_position=""):
        self.path = image_path
        self.position = image_position

    def show_image(self):
        pass


class DataType(Enum):
    TEXT = 1
    NUMBER = 2
    BOOL = 3


class ScenarioVariable:
    """A variable that simulates the environment of a scenario."""

    def __init__(self, name: str, datatype: DataType, private: bool = False):
        self.name = name
        self.datatype = datatype
        self.private = private

    def is_value_legal(self, value):
        if self.datatype == DataType.TEXT:
            if isinstance(value, str):
                return True
        elif self.datatype == DataType.NUMBER:
            if isinstance(value, float) or isinstance(value, int):
                return True
        elif self.datatype == DataType.BOOL:
            if isinstance(value, bool):
                return True
        return False

    def __eq__(self, other):
        if isinstance(other, ScenarioVariable):
            return self.name == other.name


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
    def get_comparison_operator(cls, operator_string: str):
        return cls._get_operator(operator_string, cls._comparison_operators)

    @classmethod
    def get_manipulation_operator(cls, operator_string: str):
        return cls._get_operator(operator_string, cls._manipulation_operators)

    @classmethod
    def _get_operator(cls, operator_string: str, legal_operators):
        if operator_string in legal_operators:
            return legal_operators[operator_string]
        else:
            raise ValueError("Invalid string for this type of operator. "
                             "Expected one of " + ",".join(legal_operators.keys()) + "!")


class StateChange:
    """Represents a change of the value of a game's variables."""

    def __init__(self, var: ScenarioVariable, new_value, value_operator: str):
        """
        :param var: the ScenarioVariable that will be changed.
        :param new_value: the new value of the ScenarioVariable.
        :param value_operator: the operation to change the value. Can be one of '+', '-', '/', '*' and 'set'.
        """
        self.var = var
        self.new_var = self._set_new_value(var, new_value)
        self.operator = LegalOperator.get_manipulation_operator(value_operator)

    def get_new_value(self, old_value):
        """
        :param old_value: The current value of the variable.
        :return: The new value of the variable.
        """
        if self.operator == "set":
            return self.new_var
        else:
            return self.operator(old_value, self.new_var)

    @staticmethod
    def _set_new_value(var, new_value):
        if var.is_value_legal(new_value):
            return new_value
        else:
            raise ValueError("This variable cannot have a value of this type!")


class TransitionCondition:
    """
    A transition may have a condition which, if met, leads to another inject or a different outcome.
    """

    def __init__(self, variable: ScenarioVariable, comparison_operator, variable_threshold):
        if variable.is_value_legal(variable_threshold):
            self.variable = variable
            self.threshold = variable_threshold
            self.operator = LegalOperator.get_comparison_operator(comparison_operator)
        else:
            raise ValueError("The threshold is not a valid value for the data type of this variable!")

    def evaluate_condition(self, game_variables, variable_values):
        if self.variable not in game_variables:
            raise ValueError("This variable is not in the game's variables. Cannot evaluate condition!")
        else:
            current_value = variable_values[self.variable.name]
            return self.operator(current_value, self.threshold)
