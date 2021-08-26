from __future__ import annotations

from typing import List

from domain_layer.common.auxiliary import BaseScenarioVariable
from domain_layer.common.scenario_management import ScenarioRepository, ScenarioFactory
from domain_layer.scenariodesign.injects import EditableInject
from domain_layer.scenariodesign.scenarios import EditableScenario, EditableStory


class EditableScenarioFactory(ScenarioFactory):
    """Creates instances of editable scenarios."""
    @classmethod
    def create_scenario(cls, title="new scenario", description="This is a new scenario", **kwargs):
        """Creates a new instance of an EditableScenario."""
        return EditableScenario(title=title, description=description, **kwargs)

    @classmethod
    def _build_scenario(cls, title, scenario_description, scenario_id,
                        stories, variables, **scenario_data):
        """Re-creates an editable instance of a scenario from a dict."""
        return EditableScenario(title=title, scenario_description=scenario_description,
                                scenario_id=scenario_id, stories=stories, variables=variables, **scenario_data)

    @classmethod
    def _build_story(cls, entry_slug, injects, **story_data):
        """Re-creates an editable instance of a story from a dict."""
        return EditableStory(**story_data, entry_node=entry_slug, injects=injects)

    @classmethod
    def _build_inject(cls, inject_data):
        """Re-creates an editable instance of an inject from a dict."""
        return EditableInject(**inject_data)


class EditableScenarioRepository(ScenarioRepository):
    @classmethod
    def get_factory(cls):
        return EditableScenarioFactory

    @classmethod
    def save_variable(cls, scenario_id, variable: BaseScenarioVariable):
        """Add a scenario variable to an editable scenario."""
        scenario = cls.get_scenario_by_id(scenario_id)
        scenario.variables[variable.name] = variable
        return cls.save_scenario(scenario)
