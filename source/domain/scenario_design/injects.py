from enum import Enum
from typing import List

from domain.scenario_design.auxiliary import Image, TransitionCondition, StateChange
from domain.scenario_design.graphs import GraphNode, GraphEdge


class InjectType(Enum):
    SIMPLE = 0
    SEQUENTIAL = 1
    BRANCHING = 2


class SimpleInject(GraphNode):
    """An inject in a story."""
    def __init__(self, title: str, text: str, image: Image = None, inject_id=None):
        super().__init__(label=title, node_id=inject_id)
        self.text = text
        self.image = image or Image()
        self.inject_id = self.id  # alias
        self._type = InjectType.SIMPLE

    @property
    def type(self):
        return self._type

    @property
    def transitions(self):
        return None

    @property
    def title(self):
        return self.label

    @title.setter
    def set_title(self, new_title: str):
        self.label = new_title

    def solve(self, solution):
        """Solving an inject means to provide a solution ot the inject and
        receiving a transition that points to the next inject in return.

        :param solution: The solution to this inject. Can be either a string or a Transition or a number.
        :return: A transition that points to the next inject. Returns None if there is no next inject."""
        return None

    def __str__(self):
        return_str = str(self.type) + "\n"
        return_str += str(self.id) + "\n" + str(self.label) + "\n"
        return_str += self.text
        return return_str


class Transition(GraphEdge):
    """A transition can be understood as a weighted, directed Edge pointing from one Inject to another."""

    def __init__(self, from_inject: SimpleInject, to_inject: SimpleInject, label: str = ""):
        """
        :param from_inject: The inject which this transition is attached to.
        :param to_inject: The inject which this transition will lead to.
        :param label: A brief description that will be shown to a scenario_design player.
        Behavior for empty values is undefined at the moment.
        """
        super().__init__(label=label, source_node=from_inject, target_node=to_inject)
        self.condition = None
        self.state_changes = None

    @property
    def from_inject(self):
        return self.source

    @property
    def to_inject(self):
        return self.target


class ConditionalTransition(Transition):
    def __init__(self, from_inject: SimpleInject, to_inject: SimpleInject, label: str,
                 condition: TransitionCondition, alternative_inject: SimpleInject):
        super().__init__(from_inject=from_inject, to_inject=to_inject, label=label)
        self.condition = condition
        self.alternative_inject = alternative_inject


class ChangingTransition(Transition):
    def __init__(self, from_inject: SimpleInject, to_inject: SimpleInject,
                 label: str, state_changes: List[StateChange]):
        super().__init__(from_inject=from_inject, to_inject=to_inject, label=label)
        self.changes = state_changes


class Inject(SimpleInject):
    """An inject that refers to more than one other inject and
        therefore requires the player to make a choice."""

    def __init__(self, title: str, text: str, image: Image = None, inject_id=None,
                 transitions: List[Transition] = None):
        super().__init__(title=title, text=text, image=image, inject_id=inject_id)
        self._type = InjectType.BRANCHING
        self._transitions = transitions

    @property
    def transitions(self):
        return self._transitions

    @transitions.setter
    def transitions(self, new_transitions: List[Transition]):
        self._transitions = new_transitions

    @transitions.deleter
    def transitions(self):
        self._transitions = []

    def add_transition(self, transition: Transition):
        self._transitions.append(transition)

    def solve(self, solution):
        """
        :param solution: The solution to this inject. Can be either a string or a Transition or a number.
        :return: A transition that points to the next inject. Returns None if there is no next inject.
        """
        solution = self._parse_solution(solution)
        if not self.transitions:
            return None
        elif len(self.transitions) == 1:
            return self._solve_single_transition()
        elif isinstance(solution, int):
            return self._solve_transition_index(solution)
        elif isinstance(solution, Transition):
            return self._solve_transitions_object(solution)
        else:
            raise ValueError("The provided solution has an invalid format. Must be of type 'int' or 'Transition'!")

    @staticmethod
    def _parse_solution(solution):
        if isinstance(solution, int):
            return solution
        elif isinstance(solution, str):
            if solution.isnumeric():
                return int(solution)
        else:
            raise TypeError("Solution for choice injects must be of type int!")

    def _solve_single_transition(self):
        return self.transitions[0]

    def _solve_transition_index(self, choice):
        if -1 < choice < len(self.transitions):
            return self.transitions[choice]
        else:
            raise IndexError("Inject " + self.label + " does not have a transition at index " + str(choice) + "!")

    def _solve_transitions_object(self, choice):
        if choice in self.transitions:
            return choice
        else:
            raise ReferenceError("The inject " + self.label + " does not have a transition " + repr(choice) + "!")

    def __str__(self):
        return_str = super().__str__()
        for transition in self.transitions:
            return_str += "\nOption " + transition.label + " points to " + transition.to_inject.label
        return return_str


class InjectFactory:

    @staticmethod
    def create_inject(self):
        return Inject(title="", text="")

    @staticmethod
    def create_transition(self):
        return Transition

