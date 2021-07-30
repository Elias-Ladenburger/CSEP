from typing import Optional, Dict, List

from pydantic import BaseModel, PrivateAttr

from domain.common.auxiliary import BaseScenarioVariable
from domain.common.injects import BaseChoiceInject


class BaseStory(BaseModel):
    """A Story is a collection of injects within a scenario design"""
    title: str
    entry_node: BaseChoiceInject
    injects: Optional[Dict[str, BaseChoiceInject]] = {}

    def __init__(self, title: str, entry_node: BaseChoiceInject, **keyword_args):
        super().__init__(title=title, entry_node=entry_node, **keyword_args)

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


class BaseScenario(BaseModel):
    """A container for all the data of a scenario."""

    _id: str = PrivateAttr()
    title: str
    scenario_description: str
    stories: List[BaseStory] = []

    _variables: Dict[str, BaseScenarioVariable] = PrivateAttr({})
    _variable_values: dict = PrivateAttr({})

    def __init__(self, title: str, scenario_description: str, scenario_id: str = "", **keyword_args):
        super().__init__(title=title, scenario_description=scenario_description, **keyword_args)
        self._id = scenario_id

    @property
    def scenario_id(self):
        return self._id

    @property
    def variables(self):
        return self._variables

    @property
    def variable_dict(self):
        var_dict = {}
        for var in self._variables:
            var_dict[var] = self._variables[var].dict()
        return var_dict

    def get_inject_by_slug(self, inject_slug: str):
        for story in self.stories:
            inject = story.get_inject_by_slug(inject_slug=inject_slug)
            if inject:
                return inject
        raise KeyError("An inject with the slug {} has not been found in this scenario!".format(inject_slug))

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
