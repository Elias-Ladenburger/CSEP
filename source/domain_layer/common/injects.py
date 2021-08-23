from __future__ import annotations

import string
from typing import List, Optional
from pydantic import BaseModel, PrivateAttr

from domain_layer.common.auxiliary import BaseScenarioVariable, LegalOperator, BaseVariableChange
from domain_layer.scenariodesign.graphs import GraphNode


class BaseInject(GraphNode):
    """An inject in a story."""
    text: str
    slug: str
    media_path: Optional[str] = ""

    def __init__(self, label: str, **keyword_args):
        slug = keyword_args.pop("slug", False)
        if not "slug":
            slug = label.replace(" ", "-").lower()
            slug = slug.translate(str.maketrans('', '', string.punctuation))
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
    variable_name: str
    comparison_operator: str
    variable_threshold: str
    alternative_inject: str

    def __init__(self, variable_name: str, comparison_operator, variable_threshold,
                 alternative_inject: str, **keyword_args):
        super().__init__(variable_name=variable_name, comparison_operator=comparison_operator,
                         variable_threshold=variable_threshold, alternative_inject=alternative_inject, **keyword_args)

    def __str__(self):
        return_str = "If (" + str(self.variable_name) + " " + str(self.comparison_operator)
        return_str += " " + str(self.variable_threshold) + ") "
        return_str += "then go to inject " + str(self.alternative_inject)
        return return_str


class InjectResult(BaseModel):
    """The outcome of solving an inject.
    Provides the next inject as well as a list of effects that may change the scenario."""
    next_inject: Optional[str] = ""
    variable_changes: List[BaseVariableChange] = []

    class Config:
        allow_mutation = False


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
    choices: Optional[List[BaseInjectChoice]] = []
    condition: Optional[BaseInjectCondition] = None
    next_inject: Optional[str] = ""

    def __init__(self, label: str, text: str,  **kwargs):
        super().__init__(label=label, text=text, **kwargs)
        self.update_forward_refs()

    @property
    def has_choices(self):
        return len(self.choices) > 0