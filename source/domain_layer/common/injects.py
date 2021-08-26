from __future__ import annotations

import string
from typing import List, Optional
from pydantic import BaseModel

from domain_layer.common.auxiliary import BaseVariableChange
from domain_layer.scenariodesign.graphs import GraphNode


"""This scenario contains the inject class hierarchy, as well as Value-object classes that are inject-specific."""


class BaseInjectCondition(BaseModel):
    """
    Base object for inject conditions.
    A condition may belong to an inject and is evaluated before the inject is show.
    If the condition evaluates to true, it may lead to another inject instead.
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


class BaseInject(GraphNode):
    """An inject in a story."""
    text: str
    slug: str
    condition: Optional[BaseInjectCondition] = None
    media_path: Optional[str] = ""

    def __init__(self, label: str, **keyword_args):
        slug = keyword_args.pop("slug", False)
        if not slug:
            slug = label.replace(" ", "-").lower()
            slug = slug.translate(str.maketrans('', '', string.punctuation))
        self.update_forward_refs()
        super().__init__(label=label, slug=slug, **keyword_args)

    @property
    def title(self) -> str:
        return self.label

    def __str__(self) -> str:
        return_str = str(self.slug) + "\n" + str(self.label) + "\n"
        return_str += self.text
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

    def __str__(self):
        return self.label


class BaseChoiceInject(BaseInject):
    """A specific inject that must be solved by selecting one of a number of choices."""
    choices: Optional[List[BaseInjectChoice]] = []
    next_inject: Optional[str] = ""

    def __init__(self, label: str, text: str,  **kwargs):
        super().__init__(label=label, text=text, **kwargs)

    @property
    def has_choices(self):
        return len(self.choices) > 0