from typing import Optional, Dict, List

from pydantic import BaseModel, PrivateAttr

from domain_layer.common.auxiliary import BaseScenarioVariable
from domain_layer.common.injects import BaseChoiceInject


class BaseStory(BaseModel):
    """An immutable collection of injects. Use this class only for data-transfer."""

    title: str
    _entry_node: Optional[str] = PrivateAttr("")
    injects: Optional[Dict[str, BaseChoiceInject]] = {}

    class Config:
        allow_mutation = False

    def __init__(self, title: str, entry_node: str = "", **keyword_args):
        """
        :param title: The title of this story.
        :param entry_node: A string of the slug of the first inject of this story.
        :param injects: A list of injects.
        If `entry_node` is not specified, the first inject from this list will be selected as the entry_node.
        """
        super().__init__(title=title, **keyword_args)
        self._entry_node = entry_node

    @property
    def entry_node(self):
        """
        Returns the first inject in this story.
        """
        return self.get_inject_by_slug(self._entry_node)

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
        return self.injects[inject_slug]

    def dict(self, **kwargs):
        story_dict = super().dict(**kwargs)
        story_dict["entry_node"] = self._entry_node
        story_dict["injects"] = {inject_slug: inject.dict() for inject_slug, inject in self.injects.items()}
        return story_dict


class BaseScenario(BaseModel):
    """A container for all the data of a scenario."""

    _id: str = PrivateAttr()
    title: str
    scenario_description: str
    stories: List[BaseStory] = []

    _variables: Dict[str, BaseScenarioVariable] = PrivateAttr({})

    def __init__(self, title: str, scenario_description: str, scenario_id: str = "", **keyword_args):
        super().__init__(title=title, scenario_description=scenario_description, **keyword_args)
        self._id = scenario_id
        var_dict = keyword_args.get("variables", {})
        if var_dict:
            for var_name, scenario_var in var_dict.items():
                if not isinstance(scenario_var, BaseScenarioVariable):
                    var_dict[var_name] = BaseScenarioVariable(**scenario_var)
                self._variables = var_dict

    @property
    def scenario_id(self):
        return self._id

    @property
    def description(self):
        return self.scenario_description

    @property
    def variables(self):
        return self._variables

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
            "variables": {var_name: var.dict() for (var_name, var) in self.variables.items()},
        })
        return scenario_dict
