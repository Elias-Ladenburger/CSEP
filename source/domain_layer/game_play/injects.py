from __future__ import annotations

from typing import Dict

from domain_layer.common.auxiliary import BaseScenarioVariable, LegalOperator, BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject, InjectResult, BaseInjectCondition


class GameInject(BaseChoiceInject):
    condition: InjectCondition = None

    def __init__(self, **kwargs):
        self.update_forward_refs()
        super().__init__(**kwargs)

    def solve(self, solution: str):
        """
        Resolves user input (or lack thereof).

        :returns: an InjectResult object that contains a reference to the next inject and a list of effects.
        """
        if solution.isnumeric() and self.has_choices:
            solution = self._parse_solution(solution)
            outcome = self.choices[solution].outcome
            if not outcome.next_inject:
                outcome.next_inject = self.next_inject
        else:
            outcome = InjectResult(next_inject=self.next_inject, variable_changes=[])
        return outcome

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


class InjectCondition(BaseInjectCondition):
    def evaluate_condition(self, game_variables: Dict[str, BaseScenarioVariable]):
        if self.variable_name.name not in game_variables:
            raise ValueError("This variable is not in the game's variables. Cannot evaluate condition!")
        else:
            current_value = game_variables[self.variable_name.name].value
            operator_method = LegalOperator.get_comparison_operator(self.comparison_operator)
            return operator_method(current_value, self.variable_threshold)


class GameVariable(BaseScenarioVariable):
    def update_value(self, change: VariableChange):
        if self.is_value_legal(change.value):
            self._value = change.get_new_value(self._value)
        else:
            raise TypeError("The new value is not legal for this variable!")


class VariableChange(BaseVariableChange):
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