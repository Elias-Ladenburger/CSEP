from __future__ import annotations

from typing import List

from domain_layer.common.auxiliary import BaseScenarioVariable
from domain_layer.common.injects import BaseInject
from domain_layer.common.scenario_management import ScenarioRepository, ScenarioFactory
from domain_layer.scenariodesign.injects import EditableInject
from domain_layer.scenariodesign.scenarios import EditableScenario, EditableStory


class EditableScenarioFactory(ScenarioFactory):
    @classmethod
    def create_scenario(cls, title="new scenario", description="This is a new scenario", **kwargs):
        return EditableScenario(title=title, description=description, **kwargs)

    @classmethod
    def _build_scenario(cls, title, scenario_description, scenario_id,
                        stories, variables, **scenario_data):
        return EditableScenario(title=title, scenario_description=scenario_description,
                                scenario_id=scenario_id, stories=stories, variables=variables, **scenario_data)

    @classmethod
    def _build_story(cls, entry_slug, injects, **story_data):
        return EditableStory(**story_data, entry_node=entry_slug, injects=injects)

    @classmethod
    def _build_inject(cls, inject_data):
        return EditableInject(**inject_data)


class EditableScenarioRepository(ScenarioRepository):
    @classmethod
    def get_factory(cls):
        return EditableScenarioFactory

    @classmethod
    def add_story(cls, scenario_id: str, story: EditableStory):
        scenario = cls.get_scenario_by_id(scenario_id)
        scenario.stories.append(story)
        return cls.save_scenario(scenario)

    @classmethod
    def delete_story(cls, scenario_id: str, story_index: int):
        scenario = cls.get_scenario_by_id(scenario_id)
        scenario.stories.pop(story_index)
        return cls.save_scenario(scenario)

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
