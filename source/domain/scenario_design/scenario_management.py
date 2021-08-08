from __future__ import annotations

from typing import List

from domain.common.auxiliary import BaseScenarioVariable
from domain.common.scenario_management import ScenarioRepository, ScenarioFactory
from domain.game_play.injects import Inject
from domain.scenario_design.injects import EditableInject
from domain.scenario_design.scenarios import EditableScenario, Story


class EditableScenarioFactory(ScenarioFactory):
    @classmethod
    def create_scenario(cls, title="new scenario", description="This is a new scenario", **kwargs):
        return EditableScenario(title=title,
                                description=description, **kwargs)

    @classmethod
    def build_from_dict(cls, **scenario_data):
        """
        Takes any number of keywords as argument and tries to build a valid scenario object from the key-value pairs.
        :returns: a Scenario which can be edited.
        """
        scenario_id = scenario_data.pop("scenario_id", None) or scenario_data.pop("_id", None)
        title = scenario_data.pop("title")
        description = scenario_data.pop("scenario_description", None) or scenario_data.pop("description")

        stories = scenario_data.pop("stories", [])
        scenario_vars = scenario_data.pop("variables", {})

        stories = cls._build_stories_from_dict(
            stories_data=stories)

        variables = cls._build_vars_from_dict(scenario_vars=scenario_vars)

        scenario = EditableScenario(title=title, scenario_description=description, scenario_id=scenario_id,
                                    stories=stories, variables=variables, **scenario_data)

        return scenario

    @classmethod
    def _build_stories_from_dict(cls, stories_data):
        stories = []
        for story_data in stories_data:
            story = cls._build_story_from_dict(story_data)
            stories.append(story)
        return stories

    @classmethod
    def _build_story_from_dict(cls, story_data):
        injects_data = story_data.pop("injects", {})
        entry_data = story_data.pop("entry_node", {})
        entry_node = cls._build_inject_from_dict(entry_data)
        injects = {}

        for inject_data in injects_data:
            inject = cls._build_inject_from_dict(inject_data=injects_data[inject_data])
            injects[inject.slug] = inject

        story = Story(**story_data, entry_node=entry_node, injects=injects)
        return story

    @classmethod
    def _build_inject_from_dict(cls, inject_data):
        inject_data.pop("slug")
        inject = EditableInject(**inject_data)
        return inject

    @classmethod
    def _build_vars_from_dict(cls, scenario_vars):
        new_vars = {}
        for var_name in scenario_vars:
            new_vars[var_name] = BaseScenarioVariable(**scenario_vars[var_name])
        return new_vars


class EditableScenarioRepository(ScenarioRepository):
    @classmethod
    def add_story(cls, scenario_id: str, story: Story):
        scenario = cls.get_scenario_by_id(scenario_id)
        scenario.stories.append(story)
        return cls.save_scenario(scenario)

    @classmethod
    def get_factory(cls):
        return EditableScenarioFactory

    @classmethod
    def save_variable(cls, scenario_id, variable: BaseScenarioVariable):
        scenario = cls.get_scenario_by_id(scenario_id)
        scenario.variables[variable.name] = variable
        return cls.save_scenario(scenario)

    @classmethod
    def save_variables(cls, scenario_id, variables: List[BaseScenarioVariable]):
        scenario = cls.get_scenario_by_id(scenario_id)
        scenario.variables = variables
        return cls.save_scenario(scenario)
