from typing import Optional, List

from domain.common.auxiliary import BaseScenarioVariable
from domain.common.scenarios import BaseStory, BaseScenario
from domain.scenario_design.injects import Inject


class Story(BaseStory):
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


class Scenario(BaseScenario):
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
        self.stories.append(story)

    def remove_story(self, story: Story):
        self.stories.remove(story)

    def add_variable(self, var: BaseScenarioVariable, starting_value=None):
        if var.name in self._variables:
            raise ValueError("Cannot insert two scenario_design variables of the same name!")
        self._variables[var.name] = var
        self.set_variable_starting_value(var, starting_value)

    def remove_variable(self, var: BaseScenarioVariable):
        self._variables.pop(var.name)
        self._variable_values.pop(var.name)

    def set_variable_starting_value(self, var: BaseScenarioVariable, starting_value=None):
        if var.is_value_legal(starting_value):
            self._variable_values[var.name] = starting_value
        else:
            raise ValueError("Trying to assign an illegal value to this scenario_design variable!")

    def _set_id(self, scenario_id: str):
        if self._id:
            raise ValueError("Cannot reassign id of a scenario object!")
        self._scenario_id = scenario_id
