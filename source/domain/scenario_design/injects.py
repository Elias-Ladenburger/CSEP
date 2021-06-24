from enum import Enum
from typing import List, Optional

from pydantic import PrivateAttr

from domain.scenario_design.auxiliary import TransitionCondition, StateChange
from domain.scenario_design.graphs import GraphNode, GraphEdge


class InjectType(Enum):
    SIMPLE = 0
    SEQUENTIAL = 1
    BRANCHING = 2


class Inject(GraphNode):
    text: str
    slug: str
    transitions = []
    _type = PrivateAttr(InjectType.SIMPLE)

    """An inject in a story."""
    def __init__(self, title: str, text: str, **keyword_args):
        super().__init__(label=title, text=text, slug=title.replace(" ", "-"), **keyword_args)

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


class Transition(GraphEdge):
    """A transition can be understood as a weighted, directed Edge pointing from one Inject to another."""
    _condition: TransitionCondition = PrivateAttr(None)
    effects: StateChange = None

    def __init__(self, from_inject: Inject, to_inject: Inject, label: str = "", **keyword_args):
        super().__init__(source_node=from_inject, target_node=to_inject, label=label, **keyword_args)

    @property
    def from_inject(self):
        return self.source_node

    @property
    def to_inject(self):
        return self.target_node

    @property
    def condition(self):
        if self._condition:
            return self._condition

    @property
    def alternative_inject(self):
        if self._condition:
            return self._condition.alternative_inject

    @condition.setter
    def condition(self, condition: TransitionCondition):
        self._condition = condition


class InjectFactory:

    @staticmethod
    def create_inject():
        return Inject(title="", text="")

    @staticmethod
    def create_transition(from_inject: Inject, to_inject: Inject):
        return Transition(from_inject=from_inject, to_inject=to_inject)
