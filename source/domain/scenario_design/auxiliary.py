import operator
from enum import Enum
from typing import Any

from pydantic import BaseModel


class DataType(Enum):
    TEXT = 1
    NUMBER = 2
    BOOL = 3


class ScenarioVariable(BaseModel):
    """A variable that simulates the environment of a scenario_design."""
    name: str
    datatype: DataType
    is_private: bool = False

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


class TransitionEffect(BaseModel):
    var: ScenarioVariable
    new_value: Any
    operator: str

    """Represents a change of the value of a game's variables."""

    def __init__(self, var: ScenarioVariable, new_value, value_operator: str, **keyword_args):
        """
        :param var: the ScenarioVariable that will be changed.
        :param new_value: the new value of the ScenarioVariable.
        :param value_operator: the operation to change the value. Can be one of '+', '-', '/', '*' and 'set'.
        """
        super().__init__(var=var, new_value=new_value, value_operator=value_operator, **keyword_args)
        self.new_var = self._parse_new_value(var, new_value)

    def get_new_value(self, old_value):
        """
        :param old_value: The current value of the variable.
        :return: The new value of the variable.
        """
        if self.operator == "set":
            return self.new_var
        else:
            operator_method = LegalOperator.get_manipulation_operator(self.operator)
            return operator_method(old_value, self.new_var)

    @staticmethod
    def _parse_new_value(var, new_value):
        if var.is_value_legal(new_value):
            return new_value
        else:
            raise ValueError("This variable cannot have a value of this type!")


class TransitionCondition(BaseModel):
    """
    A transition may have a condition which, if met, leads to another inject or a different outcome.
    """
    variable: ScenarioVariable
    comparison_operator: str
    variable_threshold: str
    alternative_inject: Any

    def __init__(self, variable: ScenarioVariable, comparison_operator, variable_threshold,
                 alternative_inject: Any, **keyword_args):
        super().__init__(variable=variable, comparison_operator=comparison_operator,
                         variable_threshold=variable_threshold, alternative_inject=alternative_inject, **keyword_args)
        if variable.is_value_legal(variable_threshold):
            self.variable_threshold = variable_threshold
        else:
            raise ValueError("The threshold is not a valid value for the data type of this variable!")

    def evaluate_condition(self, game_variables, variable_values):
        if self.variable not in game_variables:
            raise ValueError("This variable is not in the game's variables. Cannot evaluate condition!")
        else:
            current_value = variable_values[self.variable.name]
            operator_method = LegalOperator.get_comparison_operator(self.comparison_operator)
            return operator_method(current_value, self.variable_threshold)


class SolutionHandler:
    @staticmethod
    def solve_inject(solution, transitions):
        solution = SolutionHandler._parse_solution(solution)
        if not transitions:
            return None
        elif len(transitions) == 1:
            return transitions[0]
        elif isinstance(solution, int):
            return SolutionHandler._solve_transition_index(solution, transitions)
        elif isinstance(solution, str):
            return SolutionHandler._solve_transition_str(solution, transitions)
        else:
            raise ValueError("The provided solution has an invalid format. Must be of type 'int' or 'Transition'!")

    @staticmethod
    def _parse_solution(solution):
        """
        Takes the solution that a user has provided for an inject.
        :param solution: the solution provided by the user.

        :return: an index for a transition
        """
        if isinstance(solution, int):
            return solution
        elif isinstance(solution, str):
            if solution.isnumeric():
                return int(solution)
        else:
            raise TypeError("Solution for choice injects must be of type int!")

    @staticmethod
    def _solve_transition_index(solution):
        """
        Takes the solution that a user has provided for an inject.
        :param solution: the solution provided by the user.

        :return: an index for a transition
        """
        if isinstance(solution, int):
            return solution
        elif isinstance(solution, str):
            if solution.isnumeric():
                return int(solution)
        else:
            raise TypeError("Solution for choice injects must be of type int!")
