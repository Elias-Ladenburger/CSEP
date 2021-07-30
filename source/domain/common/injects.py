from __future__ import annotations
from typing import List, Dict, Optional
from pydantic import BaseModel

from domain.common.auxiliary import BaseScenarioVariable, LegalOperator, BaseVariableChange
from domain.scenario_design.graphs import GraphNode


class BaseInject(GraphNode):
    """An inject in a story."""
    text: str
    slug: str
    media_path: str = ""

    def __init__(self, label: str, **keyword_args):
        slug = keyword_args.pop("slug", label.replace(" ", "-").lower())
        super().__init__(label=label, slug=slug, **keyword_args)

    @property
    def title(self):
        return self.label

    def __str__(self):
        return_str = str(self.slug) + "\n" + str(self.label) + "\n"
        return_str += self.text
        return return_str


class BaseInjectCondition(BaseModel):
    """
    Base object for inject choices.
    A choice may have a condition which, if met, leads to another inject or a different outcome.
    """
    variable: BaseScenarioVariable
    comparison_operator: str
    variable_threshold: str
    alternative_inject: BaseInject

    def __init__(self, variable: BaseScenarioVariable, comparison_operator, variable_threshold,
                 alternative_inject: BaseInject, **keyword_args):
        super().__init__(variable=variable, comparison_operator=comparison_operator,
                         variable_threshold=variable_threshold, alternative_inject=alternative_inject, **keyword_args)
        if variable.is_value_legal(variable_threshold):
            self.variable_threshold = variable_threshold
        else:
            raise ValueError("The threshold is not a valid value for the data type of this variable!")


class InjectResult(BaseModel):
    """The outcome of solving an inject.
    Provides the next inject as well as a list of effects that may change the scenario."""
    next_inject: BaseInject = None
    variable_changes: List[BaseVariableChange] = []


class BaseInjectChoice(BaseModel):
    """A choice is a decision made in a scenario,
    that may change the course of the story or change the variables of the scenario."""
    label: str
    outcome: Optional[InjectResult] = None

    def __init__(self, label: str, outcome: InjectResult = None, **keyword_args):
        self.update_forward_refs()
        super().__init__(label=label, outcome=outcome, **keyword_args)
        if not outcome:
            self.outcome = InjectResult(next_inject=None, variable_changes=[])

    def dict(self, **kwargs):
        update_args = kwargs.get("exclude") or {}
        update_args.update({"exclude": {"source_node": ..., "target_node": ...}})
        kwargs.update(update_args)
        return_dict = super().dict(**kwargs)
        return return_dict


class BaseChoiceInject(BaseInject):
    choices: List[BaseInjectChoice] = []
    condition: BaseInjectCondition = None

    next_inject: Optional[BaseInject] = None

    def __init__(self, label: str, text: str,  **kwargs):
        super().__init__(label=label, text=text, **kwargs)
        self.update_forward_refs()

    @property
    def has_choices(self):
        return len(self.choices) > 0
