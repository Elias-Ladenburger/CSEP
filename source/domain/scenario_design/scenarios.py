from typing import Optional, List, Dict

from domain.common.auxiliary import BaseScenarioVariable
from domain.common.scenarios import BaseStory, BaseScenario
from domain.scenario_design.injects import EditableInject


class Story(BaseStory):
    """A Story is a collection of injects within a scenario design"""
    injects: Dict[str, EditableInject] = {}

    class Config:
        allow_mutation = True

    def __init__(self, title: str, entry_node: EditableInject, **kwargs):
        if isinstance(entry_node, EditableInject):
            entry_node = entry_node.dict()
        super().__init__(title=title, entry_node=entry_node["slug"], **kwargs)
        self.injects[entry_node["slug"]] = EditableInject(**entry_node)

    def add_injects(self, new_injects: List[EditableInject]):
        """
        Adds a list of injects to the story.
        This will overwrite existing injects within the story if they have the same slug as one of the new injects.
        """
        for inject in new_injects:
            self.injects[inject.slug] = inject

    def add_inject(self, inject: EditableInject):
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
        elif isinstance(inject, EditableInject):
            return self.injects.pop(str(inject.slug))
        else:
            raise TypeError("Argument for removing inject must be of type 'str' or 'Inject'!")

    def _remove_inject_by_slug(self, inject_slug: str):
        return self.injects.pop(inject_slug)


class EditableScenario(BaseScenario):
    """
    A scenario is a number of realistic situations that are exposed to a participant.
    """
    stories: List[Story] = []

    learning_objectives: Optional[str] = ""
    required_knowledge: Optional[str] = ""
    target_group: Optional[str]

    def __init__(self, title: str, description: str = "", scenario_id: str = "", **keyword_args):
        scenario_description = keyword_args.pop("scenario_description", description)
        super().__init__(title=title, scenario_description=scenario_description,
                         scenario_id=scenario_id, **keyword_args)

    def add_story(self, story: Story):
        """Adds a new story to this scenario."""
        self.stories.append(story)

    def remove_story(self, story: Story):
        """
        Removes an entire chapter from this scenario.
        """
        self.stories.remove(story)

    def add_variable(self, var: BaseScenarioVariable):
        """
        Adds a new variable to this scenario.
        """
        if var.name in self._variables:
            raise ValueError("Cannot insert two scenario_design variables of the same name!")
        self._variables[var.name] = var

    def remove_variable(self, scenario_var):
        """
        Removes a variable from this scenario.
        :param scenario_var: either the name or the entire scenario variable to be removed
        """
        if isinstance(scenario_var, BaseScenarioVariable):
            self._variables.pop(scenario_var.name)
        else:
            self._variables.pop(scenario_var)

    def set_id(self, scenario_id: str):
        if self._id and self._id != "new":
            raise ValueError("Cannot reassign id of a scenario object!")
        self._id = scenario_id
