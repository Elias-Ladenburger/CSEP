from typing import Optional, List, Dict

from domain_layer.common.auxiliary import BaseScenarioVariable
from domain_layer.common.injects import BaseInject
from domain_layer.common.scenarios import BaseStory, BaseScenario, DetailedScenario
from domain_layer.scenariodesign.injects import EditableInject


class EditableStory(BaseStory):
    """A Story is a collection of injects within a scenario design"""
    injects: Dict[str, EditableInject] = {}

    class Config:
        allow_mutation = True

    def __init__(self, title: str, entry_node: str, **kwargs):
        super().__init__(title=title, entry_node=entry_node, **kwargs)

    def set_entry_node(self, new_entry_node_slug):
        if new_entry_node_slug in self.injects:
            self._entry_node = new_entry_node_slug

    def add_injects(self, new_injects: List[EditableInject]):
        """
        Adds a list of injects to the story.
        This will overwrite existing injects within the story if they have the same slug as one of the new injects.
        """
        for inject in new_injects:
            self.injects[inject.slug] = inject

    def add_inject(self, inject: EditableInject, preceded_by_inject: str = "", make_entry_node=False):
        """Adds a single inject to the story.
           :param inject: the inject to be added.
           :param preceded_by_inject: the slug of an existing inject that will now point to this inject.
           :param make_entry_node: a boolean to indicate whether to set this inject to be the new entry node.
           """
        i = 1
        slug = inject.slug
        if slug == "new-inject":
            slug = inject.label.replace(" ", "-").lower()
        while slug in self.injects:
            slug = inject.slug + str(i)
            i += 1
        inject.slug = slug
        self.update_inject(inject, make_entry_node)
        if preceded_by_inject and preceded_by_inject in self.injects:
            self.injects[preceded_by_inject].next_inject = inject.slug

    def update_inject(self, inject: EditableInject, make_entry_node=False):
        """Updates a single inject in the story."""
        self.injects[inject.slug] = inject
        if make_entry_node:
            self.set_entry_node(inject.slug)

    def remove_inject(self, inject):
        """Removes an inject from the story.

        :param inject: the inject to be removed. Can be the inject slug of the inject object.
        :returns: the inject that has been removed."""
        if isinstance(inject, str):
            return self._remove_inject_by_slug(inject)
        elif isinstance(inject, BaseInject):
            return self._remove_inject_by_slug(str(inject.slug))
        else:
            raise TypeError("Argument for removing inject must be of type 'str' or 'Inject'!")

    def _remove_inject_by_slug(self, inject_slug: str):
        """Deletes an inject from this story.
        Updates all references to this inject so that they point to the inject that comes after."""
        inject = self.get_inject_by_slug(inject_slug)
        self._update_inject_references(inject_slug, inject.next_inject)
        return self.injects.pop(inject_slug)

    def _update_inject_references(self, old_reference: str, new_reference: str):
        """Updates all references to this inject so that they point to the inject that comes after."""
        if old_reference == self.entry_node.slug:
            self._entry_node = new_reference
        for slug in self.injects:
            if self.injects[slug].next_inject == old_reference:
                self.injects[slug].next_inject = new_reference
            if self.injects[slug].condition:
                if self.injects[slug].condition.alternative_inject == old_reference:
                    self.injects[slug].condition.alternative_inject = new_reference


class EditableScenario(DetailedScenario):
    stories: List[EditableStory] = []

    def add_story(self, story: EditableStory):
        """Adds a new story to this scenario."""
        self.stories.append(story)

    def remove_story(self, story: EditableStory):
        """
        Removes an entire story from this scenario.
        """
        self.stories.remove(story)

    def add_inject(self, inject: EditableInject, story_index: int = 0,
                   preceded_by_inject: str = "", make_entry_node=False):
        """
        Adds an inject to this scenario.
        :param inject: the inject to be added.
        :param make_entry_node: A boolean, whether to make this inject the new entry node of the story.
        :param story_index: the story to which to add this inject. Will append a new story if index is -1.
        """
        self.stories[story_index].add_inject(inject, preceded_by_inject=preceded_by_inject,
                                             make_entry_node=make_entry_node)

    def update_inject(self, inject: EditableInject, story_index: int = 0, make_entry_node=False):
        """
        Adds an inject to this scenario.
        :param inject: the inject to be added.
        :param make_entry_node: A boolean, whether to make this inject the new entry node of the story.
        :param story_index: the story to which to add this inject. Will append a new story if index is -1.
        """
        self.stories[story_index].update_inject(inject, make_entry_node=make_entry_node)

    def remove_inject(self, inject: EditableInject, story_index: int = 0):
        """Removes an inject from this story."""
        self.stories[story_index].remove_inject(inject)

    def get_all_injects(self):
        injects = []
        for story in self.stories:
            injects += [*story.injects.values()]
        return injects

    def add_variable(self, var: BaseScenarioVariable):
        """
        Adds a new variable to this scenario.
        """
        if var.name in self._variables:
            raise ValueError("Cannot insert two scenariodesign variables of the same name!")
        self._variables[var.name] = var

    def remove_variable(self, scenario_var):
        """
        Removes a variable from this scenario.
        :param scenario_var: either the name or the entire scenario variable to be removed
        """

        if isinstance(scenario_var, BaseScenarioVariable):
            var_name = scenario_var.name
        else:
            var_name = scenario_var
        self._variables.pop(scenario_var)
        for inject in self.get_all_injects():
            if inject.condition:
                if inject.condition.variable_name == var_name:
                    inject.condition = None

    def conditions_with_var(self, scenario_var):
        """
        Counts how often a given scenario variable is used in any inject conditions.
        :param scenario_var: the name of the scenario variable to look for.
        :returns: the number of occurrences of this scenario variable.
        """
        if isinstance(scenario_var, BaseScenarioVariable):
            var_name = scenario_var.name
        else:
            var_name = scenario_var
        counter = 0
        for inject in self.get_all_injects():
            if inject.condition:
                if inject.condition.var_name == var_name:
                    counter += 1
        return counter

    def set_id(self, scenario_id: str):
        if self._id and self._id != "new":
            raise ValueError("Cannot reassign id of a scenario object!")
        self._id = scenario_id
