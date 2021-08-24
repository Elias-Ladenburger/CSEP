from __future__ import annotations

from typing import Dict, Optional, List

from domain_layer.common.auxiliary import BaseScenarioVariable, LegalOperator, BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject, InjectResult, BaseInjectCondition


class GameInject(BaseChoiceInject):
    condition: GameInjectCondition = None

    def __init__(self, **kwargs):
        self.update_forward_refs()
        super().__init__(**kwargs)

    def solve(self, solution: str = ""):
        """
        Resolves user input (or lack thereof).

        :returns: an InjectResult object that contains a reference to the next inject and a list of effects.
        """
        if self.has_choices:
            solution = self._parse_solution(solution)
            outcome = solution.outcome
            if not outcome.next_inject:
                outcome = InjectResult(next_inject=self.next_inject, variable_changes=outcome.variable_changes)
        else:
            outcome = InjectResult(next_inject=self.next_inject, variable_changes=[])
        return outcome

    def _parse_solution(self, solution):
        """
        Takes the solution that a user has provided for an inject.
        :param solution: the solution provided by the user.

        :return: an index for a transition
        """
        if isinstance(solution, int):
            return self.choices[solution]
        elif isinstance(solution, str):
            if solution.isnumeric():
                return self.choices[int(solution)]
            else:
                for choice in self.choices:
                    if solution == str(choice):
                        return choice
                raise ValueError("Solution {} not found for inject {}".format(solution, self.label))
        else:
            raise TypeError("Solution for choice injects must be of type int or str!")


class GameInjectCondition(BaseInjectCondition):
    def evaluate(self, game_variables: Dict[str, BaseScenarioVariable]):
        if self.variable_name not in game_variables:
            raise ValueError("This variable is not in the gameplay's variables. Cannot evaluate condition!")
        else:
            current_value = game_variables[self.variable_name].value
            operator_method = LegalOperator.get_comparison_operator(self.comparison_operator)
            return operator_method(current_value, self.variable_threshold)


class GameVariableChange(BaseVariableChange):
    """Represents a change of a GameVariable"""

    def calculate_new_value(self, old_value):
        operator = self.get_operator(self.operator)
        return operator(old_value, self._new_value)

    def get_new_value(self, old_value):
        """
        :param old_value: The current value of the variable.
        :return: The new value of the variable.
        """
        if self.operator == "set":
            return self._new_value
        else:
            operator_method = LegalOperator.get_manipulation_operator(self.operator)
            return operator_method(old_value, self._new_value)


class GameVariable(BaseScenarioVariable):
    def update_value(self, change: GameVariableChange):
        new_value = change.get_new_value(self._value)
        self.set_value(new_value)

    def set_value(self, new_value: str):
        if self.is_value_legal(new_value):
            self._value = new_value
        else:
            raise ValueError("The new value is not legal for this variable!")


class GameInjectResult(InjectResult):
    next_inject: Optional[str] = ""
    variable_changes: List[GameVariableChange] = []
