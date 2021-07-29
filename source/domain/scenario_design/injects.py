from __future__ import annotations

from typing import List, Dict, Optional

from pydantic import BaseModel

from domain.scenario_design.auxiliary import ScenarioVariable, LegalOperator, VariableChange
from domain.scenario_design.graphs import GraphNode


class SimpleInject(GraphNode):
    """An inject in a story."""
    text: str
    slug: str
    media_path: str = ""

    next_inject: Inject = None

    def __init__(self, label: str, **keyword_args):
        super().__init__(label=label, slug=label.replace(" ", "-").lower(), **keyword_args)

    @property
    def title(self):
        return self.label

    @title.setter
    def title(self, new_title: str):
        self.label = new_title

    def __str__(self):
        return_str = str(self.slug) + "\n" + str(self.label) + "\n"
        return_str += self.text
        return return_str


class InjectCondition(BaseModel):
    """
    A transition may have a condition which, if met, leads to another inject or a different outcome.
    """
    variable: ScenarioVariable
    comparison_operator: str
    variable_threshold: str
    alternative_inject: SimpleInject

    def __init__(self, variable: ScenarioVariable, comparison_operator, variable_threshold,
                 alternative_inject: SimpleInject, **keyword_args):
        super().__init__(variable=variable, comparison_operator=comparison_operator,
                         variable_threshold=variable_threshold, alternative_inject=alternative_inject, **keyword_args)
        if variable.is_value_legal(variable_threshold):
            self.variable_threshold = variable_threshold
        else:
            raise ValueError("The threshold is not a valid value for the data type of this variable!")

    def evaluate_condition(self, game_variables: Dict[str, ScenarioVariable]):
        if self.variable.name not in game_variables:
            raise ValueError("This variable is not in the game's variables. Cannot evaluate condition!")
        else:
            current_value = game_variables[self.variable.name].value
            operator_method = LegalOperator.get_comparison_operator(self.comparison_operator)
            return operator_method(current_value, self.variable_threshold)


class Inject(SimpleInject):
    choices: List[InjectChoice] = []
    condition: InjectCondition = None

    @property
    def has_choices(self):
        return len(self.choices) > 0

    def add_choices(self, new_choices: List[InjectChoice]):
        for choice in new_choices:
            self.choices.append(choice)

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


class InjectChoice(BaseModel):
    """A choice is a decision made in a scenario,
    that may change the course of the story or change the variables of the scenario."""
    label: str
    outcome: Optional[InjectResult] = None

    def __init__(self, label: str, outcome: InjectResult = None, **keyword_args):
        self.update_forward_refs()
        super().__init__(label=label, outcome=outcome, **keyword_args)
        if not outcome:
            self.outcome = InjectResult(next_inject=None, variable_changes=[])

    def set_target_inject(self, inject: Inject):
        self.outcome.next_inject = inject

    def add_effect(self, var_change: VariableChange):
        self.outcome.variable_changes.append(var_change)

    def remove_effect(self, var_change: VariableChange):
        self.outcome.variable_changes.remove(var_change)

    def dict(self, **kwargs):
        update_args = kwargs.get("exclude") or {}
        update_args.update({"exclude": {"source_node": ..., "target_node": ...}})
        kwargs.update(update_args)
        return_dict = super().dict(**kwargs)
        return return_dict


class InjectResult(BaseModel):
    """The outcome of solving an inject.
    Provides the next inject as well as a list of effects that may change the scenario."""
    next_inject: Inject = None
    variable_changes: List[VariableChange] = []
