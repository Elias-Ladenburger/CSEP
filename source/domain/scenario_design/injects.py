from enum import Enum
from typing import Optional

from pydantic import PrivateAttr

from domain.scenario_design.auxiliary import TransitionCondition, TransitionEffect
from domain.scenario_design.graphs import GraphNode, GraphEdge


class InjectType(Enum):
    SIMPLE = 0
    SEQUENTIAL = 1
    BRANCHING = 2


class Inject(GraphNode):
    """An inject in a story."""
    text: str
    slug: str
    transitions = []
    _type = PrivateAttr(InjectType.SIMPLE)

    def __init__(self, label: str, **keyword_args):
        super().__init__(label=label, slug=label.replace(" ", "-").lower(), **keyword_args)

    @property
    def type(self):
        return self._type

    @property
    def title(self):
        return self.label

    @title.setter
    def title(self, new_title: str):
        self.label = new_title

    def __str__(self):
        return_str = str(self.type) + "\n"
        return_str += str(self.slug) + "\n" + str(self.label) + "\n"
        return_str += self.text
        return return_str


class Choice(GraphEdge):
    """A choice is a decision made in a scenario,
    that may change the course of the story or change the variables of the scenario."""
    condition: Optional[TransitionCondition] = None
    effects: Optional[TransitionEffect] = None

    def __init__(self, from_inject: Inject, to_inject: Inject, label: str = "", **keyword_args):
        super().__init__(source_node=from_inject, target_node=to_inject, label=label, **keyword_args)

    @property
    def from_inject(self):
        return self.source_node

    @property
    def to_inject(self):
        return self.target_node

    def dict(self, **kwargs):
        update_args = kwargs.get("exclude") or {}
        update_args.update({"exclude": {"source_node": ..., "target_node": ...}})
        kwargs.update(update_args)
        return_dict = super().dict(**kwargs)
        return_dict["from_inject"] = self.from_inject.slug
        return_dict["to_inject"] = self.to_inject.slug
        return return_dict

