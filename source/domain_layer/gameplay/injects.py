from __future__ import annotations

from typing import Dict, Optional, List

from domain_layer.common.auxiliary import BaseScenarioVariable, LegalOperator, BaseVariableChange
from domain_layer.common.injects import BaseChoiceInject, InjectResult, BaseInjectCondition


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
                outcome = solution.outcome
                if not outcome.next_inject:
                    variable_changes = [GameVariableChange(**var_change.dict()) for var_change in outcome.variable_changes]
                    outcome = GameInjectResult(next_inject=self.next_inject, variable_changes=variable_changes)
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
            current_value = game_variables[self.variable_name].value
            operator_method = LegalOperator.get_comparison_operator(self.comparison_operator)
            return operator_method(current_value, self.variable_threshold)


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
            old_value = self.var.legal_value(old_value)
            new_value = self.var.legal_value(self._new_value)
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
        if self.is_value_legal(new_value):
            self._value = new_value
        else:
            raise ValueError("The value '{}' is not legal for the variable {}!".format(new_value, self.name))


class GameInjectResult(InjectResult):
    """The outcome of solving an inject.
    Provides the next inject as well as a list of effects that may change the scenario."""
    next_inject: Optional[str] = ""
    variable_changes: List[GameVariableChange] = []
