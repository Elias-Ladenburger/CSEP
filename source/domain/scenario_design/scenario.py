from typing import Optional, Dict, List

from pydantic import BaseModel, PrivateAttr

from domain.scenario_design.auxiliary import ScenarioVariable
from domain.scenario_design.injects import Inject, InjectChoice


class Story(BaseModel):
    """A Story is a collection of injects within a scenario design"""
    title: str
    entry_node: Inject
    injects: Optional[Dict[str, Inject]] = {}
    story_id: Optional[str]

    def __init__(self, title: str, entry_node: Inject, **keyword_args):
        super().__init__(title=title, entry_node=entry_node, **keyword_args)

    def add_injects(self, injects: List[Inject]):
        """
        Adds a list of injects to the story.
        This will overwrite existing injects within the story, if they have the same slug as one of the new injects.
        """
        self.injects[self.entry_node.slug] = self.entry_node
        for inject in injects:
            self.injects[inject.slug] = inject

    def add_inject(self, inject: Inject):
        """Adds a single inject to the story.
           If the story already contains an inject with this slug, the new inject will overwrite the existing inject.

           :param inject: the inject to be added.
           """
        self.injects[str(inject.slug)] = inject

    def remove_inject(self, inject):
        """Removes an inject from the story.

        :param inject: the inject to be removed. Can be the inject slug of the inject object.
        :returns: the inject that has been removed."""
        if isinstance(inject, str):
            return self._remove_inject_by_slug(inject)
        elif isinstance(inject, Inject):
            return self.injects.pop(str(inject.slug))
        else:
            raise TypeError("Argument for removing inject must be of type 'str' or 'Inject'!")

    def _remove_inject_by_slug(self, inject_slug: str):
        return self.injects.pop(inject_slug)

    def has_inject_with_slug(self, inject_slug: str):
        """
        Checks whether this story has an inject with the given slug.

        :param inject_slug: A string with the slug to look for.
        :returns: True if an inject with this slug exists, False otherwise.
        """
        return inject_slug in self.injects

    def get_inject_by_slug(self, inject_slug: str):
        """Provides an inject with the given slug in this story.

        :param inject_slug: A string with the inject-slug.
        :returns: an inject with this slug, if one exists in this story. False if no inject is found.
        """
        inject = self.injects[inject_slug]
        return inject

    def solve_inject(self, inject_slug: str, solution):
        """
        Solves an inject with the given solution.
        Returns the next inject, if one exists.

        :param solution: The solution to this inject. Can be either a string or a Transition or a number.
        :param inject_slug: The slug of the inject that has been solved.
        :return: A transition that points to the next inject. Returns None if there is no next inject.
        """
        inject = self.get_inject_by_slug(inject_slug=inject_slug)
        return inject.solve(solution)

    def dict(self, **kwargs):
        story_dict = super().dict(**kwargs)
        return story_dict


class ScenarioData(BaseModel):
    """A container for all the data of a scenario."""

    _id: str = PrivateAttr()
    title: str
    scenario_description: str
    stories: List[Story] = []

    _variables: Dict[str, ScenarioVariable] = PrivateAttr({})
    _variable_values: dict = PrivateAttr({})

    def __init__(self, title: str, scenario_description: str, scenario_id: str = "", **keyword_args):
        super().__init__(title=title, scenario_description=scenario_description, **keyword_args)
        self._id = scenario_id

    @property
    def scenario_id(self):
        return self._id


class Scenario(ScenarioData):
    """
    A scenario is a number of realistic situations that are exposed to a participant.
    """
    learning_objectives: Optional[str] = ""
    required_knowledge: Optional[str] = ""
    target_group: Optional[str]

    def __init__(self, title: str, scenario_description: str, scenario_id: str = "", **keyword_args):
        super().__init__(title=title, scenario_description=scenario_description,
                         scenario_id=scenario_id, **keyword_args)

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
        scenario_dict.update({
            "scenario_id": self.scenario_id,
            "variables": self.variable_dict,
            "variable_values": self._variable_values
        })
        return scenario_dict


class EvaluatableScenario(Scenario):
    """A scenario can also be used for evaluation purposes.
    To this end it could sometimes be interesting to refer to previous versions of the scenario."""
    previous_scenario: Scenario
