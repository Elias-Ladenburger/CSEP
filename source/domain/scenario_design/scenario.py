from typing import Optional, Dict, List

from pydantic import BaseModel, PrivateAttr

from domain.scenario_design.auxiliary import ScenarioVariable
from domain.scenario_design.injects import Inject, Transition


class Story(BaseModel):
    """A _Story_ is a collection of injects within a scenario_design"""
    title: str
    entry_node: Inject
    _injects: Optional[Dict[str, Inject]] = PrivateAttr({})
    _transitions: Optional[Dict[str, List[Transition]]] = PrivateAttr({})

    def __init__(self, title: str, entry_node: Inject, injects: List[Inject],
                 transitions: List[Transition], **keyword_args):
        super().__init__(title=title, entry_node=entry_node, **keyword_args)
        self._initialize_injects(injects)
        self._initialize_transitions(transitions)

    def _initialize_injects(self, injects):
        self._injects[self.entry_node.slug] = self.entry_node
        for inject in injects:
            self._injects[inject.slug] = inject
            self._transitions[inject.slug] = []

    def _initialize_transitions(self, transitions):
        for transition in transitions:
            if transition.from_inject.slug in self.injects and transition.to_inject.slug in self._injects:
                self._transitions[transition.from_inject.slug].append(transition)

    @property
    def injects(self):
        return self._injects

    @property
    def transitions(self):
        return self._transitions

    def add_inject(self, inject: Inject):
        self._injects[str(inject.slug)] = inject

    def remove_inject(self, inject: Inject):
        self._injects.pop(str(inject.slug))

    def remove_inject_by_slug(self, inject_slug: str):
        self._injects.pop(inject_slug)

    def get_inject_by_slug(self, inject_slug: str):
        if inject_slug in self._injects:
            inject = self._injects[inject_slug]
            return inject
        return None

    def add_transition(self, new_transition: Transition):
        source = new_transition.from_inject
        if source.slug in self._injects:
            self._injects[source.slug].transitions.append(new_transition)

    def remove_transition(self, transition: Transition):
        source = transition.from_inject
        if source in self._injects:
            self._injects[source.slug].transitions.remove(transition)

    def solve_inject(self, inject_slug, solution):
        """
        :param solution: The solution to this inject. Can be either a string or a Transition or a number.
        :param inject_slug: The slug of the inject that has been solved.
        :return: A transition that points to the next inject. Returns None if there is no next inject.
        """
        if isinstance(solution, Transition):
            return solution
        elif not isinstance(solution, int):
            solution = int(solution)
        if -1 < solution < len(self.transitions[inject_slug]):
            return self.transitions[inject_slug][solution]
        else:
            raise IndexError(
                "A transition at index {} was selected, but this inject only has {} transitions"
                .format(solution, len(self.transitions[inject_slug])))


class Scenario(BaseModel):
    _id: str = PrivateAttr()
    title: str
    description: str
    stories: List[Story] = []
    _variables: Dict[str, ScenarioVariable] = PrivateAttr({})
    _variable_values: dict = PrivateAttr({})

    def __init__(self, title: str, description: str, scenario_id: str, **keyword_args):
        super().__init__(title=title, description=description, **keyword_args)
        self._id = scenario_id

    @property
    def scenario_id(self):
        return self._id

    @property
    def variables(self):
        return self._variables

    @property
    def variable_values(self):
        return self._variable_values

    def add_story(self, story: Story):
        self.stories.append(story)

    def remove_story(self, story: Story):
        self.stories.remove(story)
    
    def add_variable(self, var: ScenarioVariable, starting_value=None):
        if var.name in self._variables:
            raise ValueError("Cannot insert two scenario_design variables of the same name!")
        self._variables[var.name] = var
        self.set_variable_starting_value(var, starting_value)
    
    def remove_variable(self, var: ScenarioVariable):
        self._variables.pop(var.name)
        self._variable_values.pop(var.name)

    def set_variable_starting_value(self, var: ScenarioVariable, starting_value=None):
        if var.is_value_legal(starting_value):
            self._variable_values[var.name] = starting_value
        else:
            raise ValueError("Trying to assign an illegal value to this scenario_design variable!")

    def get_inject_by_slug(self, inject_slug: str):
        for story in self.stories:
            inject = story.get_inject_by_slug(inject_slug=inject_slug)
            if inject:
                return inject
        return None

    def _set_id(self, scenario_id: str):
        if self._id:
            raise ValueError("Cannot reassign id of a scenario object!")
        self._scenario_id = scenario_id

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.scenario_id == self.scenario_id

    class Config:
        underscore_attrs_are_private = True


class EvaluatableScenario(Scenario):
    """A scenario can also be used for evaluation purposes.
    To this end it could sometimes be interesting to refer to previous versions of the scenario."""
    previous_scenario: Scenario
