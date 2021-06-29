from typing import Optional, Dict, List

from pydantic import BaseModel, PrivateAttr

from domain.scenario_design.auxiliary import ScenarioVariable
from domain.scenario_design.injects import Inject, Transition


class Story(BaseModel):
    """A Story is a collection of injects within a scenario design"""
    title: str
    entry_node: Inject
    injects: Optional[Dict[str, Inject]] = {}
    transitions: Optional[Dict[str, List[Transition]]] = {}

    def __init__(self, title: str, entry_node: Inject, **keyword_args):
        super().__init__(title=title, entry_node=entry_node, **keyword_args)

    def add_injects(self, injects):
        self.injects[self.entry_node.slug] = self.entry_node
        for inject in injects:
            self.injects[inject.slug] = inject
            self.transitions[inject.slug] = []

    def initialize_transitions(self, transitions):
        for transition in transitions:
            if transition.from_inject.slug in self.injects and transition.to_inject.slug in self.injects:
                self.transitions[transition.from_inject.slug].append(transition)

    def add_inject(self, inject: Inject):
        self.injects[str(inject.slug)] = inject

    def remove_inject(self, inject: Inject):
        self.injects.pop(str(inject.slug))

    def remove_inject_by_slug(self, inject_slug: str):
        self.injects.pop(inject_slug)

    def get_inject_by_slug(self, inject_slug: str):
        if inject_slug in self.injects:
            inject = self.injects[inject_slug]
            return inject
        return None

    def add_transition(self, new_transition: Transition):
        source = new_transition.from_inject
        if source.slug in self.injects:
            self.transitions[source.slug].append(new_transition)

    def remove_transition(self, transition: Transition):
        source = transition.from_inject
        if source in self.injects:
            self.injects[source.slug].transitions.remove(transition)

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

    def dict(self, **kwargs):
        story_dict = super().dict(**kwargs)
        return story_dict


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

    @property
    def variable_dict(self):
        var_dict = {}
        for var in self._variables:
            var_dict[var] = self._variables[var].dict()
        return var_dict

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

    def dict(self, **kwargs):
        scenario_dict = super().dict(**kwargs)
        scenario_dict.update({"variables": self.variable_dict, "variable_values": self._variable_values})
        return scenario_dict


class EvaluatableScenario(Scenario):
    """A scenario can also be used for evaluation purposes.
    To this end it could sometimes be interesting to refer to previous versions of the scenario."""
    previous_scenario: Scenario
