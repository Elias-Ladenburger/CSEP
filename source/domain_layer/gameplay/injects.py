from __future__ import annotations

from typing import Dict, Optional, List

from domain_layer.common.auxiliary import BaseScenarioVariable, LegalOperator, BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject, BaseInjectResult, BaseInjectCondition


class GameInject(BaseChoiceInject):
    """An inject that must be solved during a game."""
    condition: GameInjectCondition = None

    def __init__(self, **kwargs):
        self.update_forward_refs()
        super().__init__(**kwargs)

    def solve(self, solution: str = ""):
        """
        Resolves user input (or lack thereof).

        :returns: an InjectResult object that contains a reference to the next inject and a list of effects.
        """
        outcome = GameInjectResult(next_inject=self.next_inject, variable_changes=[])
        if self.has_choices:
            solution = self._parse_solution(solution)
            if solution:
                next_inject = solution.outcome.next_inject or self.next_inject
                variable_changes = self._parse_var_changes(solution.outcome.variable_changes)
                outcome = GameInjectResult(next_inject=next_inject, variable_changes=variable_changes)
        return outcome

    def _parse_var_changes(self, var_changes):
        parsed_changes = []
        for var_change in var_changes:
            raw_dict = var_change.dict()
            parsed_changes.append(GameVariableChange(**raw_dict))
        return parsed_changes

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
                # raise ValueError("Solution {} not found for inject {}".format(solution, self.label))
                return False
        else:
            raise TypeError("Solution for choice injects must be of type int or str!")


class GameInjectCondition(BaseInjectCondition):
    """
    A condition may belong to an inject and is evaluated before the inject is shown.
    If the condition evaluates to true, it may lead to another inject instead.
    """
    def evaluate(self, game_variables: Dict[str, BaseScenarioVariable]) -> bool:
        """Check whether this condition is met with the current variables.

        :return: True if this condition is met.
        """
        if self.variable_name not in game_variables:
            raise ValueError("This variable is not in the gameplay's variables. Cannot evaluate condition!")
        else:
            var_to_evaluate = game_variables[self.variable_name]
            current_value = var_to_evaluate.value
            threshold = var_to_evaluate.legalize_value(self.variable_threshold)
            operator_method = LegalOperator.get_comparison_operator(self.comparison_operator)
            return operator_method(current_value, threshold)


class GameVariableChange(BaseVariableChange):
    """Represents a change of a GameVariable"""

    def _calculate_new_value(self, old_value):
        """
        Apply the operator and new value to the old value in the form of
        `{old_value} {operator} {new_value}`.

        :return: the result of this operation.
        """
        operator = self.get_operator(self.operator)
        try:
            old_value = self.var.legalize_value(old_value)
            new_value = self.var.legalize_value(self._new_value)
            result = operator(old_value, new_value)
            return result
        except TypeError as te:
            print(te)


    def get_new_value(self, old_value):
        """
        :param old_value: The current value of the variable.
        :return: The new value of the variable.
        """
        if self.operator == "set" or self.operator == "=":
            return self._new_value
        else:
            return self._calculate_new_value(old_value)


class GameVariable(BaseScenarioVariable):
    """A variable that simulates the environment of a scenario."""
    def update_value(self, change: GameVariableChange):
        """Apply a change operation to alter the value of this GameVariable."""
        new_value = change.get_new_value(self._value)
        self.set_value(new_value)

    def set_value(self, new_value: str):
        """Set the value of this variable to the new value.

        :raise ValueError: If a value is not legal for this type of variable."""
        self._value = new_value


class GameInjectResult(BaseInjectResult):
    """The outcome of solving an inject.
    Provides the next inject as well as a list of effects that may change the scenario."""
    next_inject: Optional[str] = ""
    variable_changes: List[GameVariableChange] = []
