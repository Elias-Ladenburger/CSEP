import json
from typing import List

from domain_layer.common.auxiliary import BaseScenarioVariable
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.common.scenarios import BaseScenario, BaseStory
from infrastructure_layer.repository import Repository


class ScenarioFactory:
    """Creates scenario instances."""
    @staticmethod
    def create_scenario(title="new scenario", description="This is a new scenario", **kwargs):
        """
        Create an entirely new scenario that can be modified.
        :param title: The name or title of the scenario.
        :param description: A short description of what this scenario is about.
        :returns: A Scenario which can be edited.
        """
        scenario_description = kwargs.pop("scenario_description", None) \
                               or kwargs.pop("description", None) or description
        new_scenario = BaseScenario(title=title, scenario_description=scenario_description, **kwargs)
        return new_scenario

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

        stories = cls._build_stories_from_dict(stories_data=stories)

        variables = cls._build_vars_from_dict(scenario_vars=scenario_vars)

        scenario = cls._build_scenario(title=title, scenario_description=description, scenario_id=scenario_id,
                                       stories=stories, variables=variables, **scenario_data)

        return scenario

    @classmethod
    def _build_scenario(cls, title, scenario_description, scenario_id,
                        stories, variables, **scenario_data) -> BaseScenario:
        """Builds the scenario from the raw data."""
        return BaseScenario(title=title, scenario_description=scenario_description,
                            scenario_id=scenario_id, stories=stories, variables=variables, **scenario_data)

    @classmethod
    def _build_stories_from_dict(cls, stories_data) -> List[BaseStory]:
        """Builds the stories required for a scenario from the raw data."""
        stories = []
        for story_data in stories_data:
            story = cls._build_story_from_dict(story_data)
            stories.append(story)
        return stories

    @classmethod
    def _build_story_from_dict(cls, story_data):
        """Builds a single story from raw data. """
        injects_data = story_data.pop("injects", {})
        entry_slug = story_data.pop("entry_node", "")
        injects = {}

        for inject_data in injects_data:
            inject = cls._build_inject_from_dict(inject_data=injects_data[inject_data])
            injects[inject.slug] = inject

        story = cls._build_story(**story_data, entry_slug=entry_slug, injects=injects)
        return story

    @classmethod
    def _build_story(cls, entry_slug, injects, **story_data):
        """Creates the actual story entity.
        This method will be likely be overridden by subdomain-specific child factory-classes."""
        return BaseStory(**story_data, entry_node=entry_slug, injects=injects)

    @classmethod
    def _build_inject_from_dict(cls, **inject_data):
        """Builds a single inject from raw data."""
        inject = cls._build_inject(**inject_data)
        return inject

    @classmethod
    def _build_inject(cls, inject_data):
        """Creates the actual entity for the inject.
        This method will be likely be overridden by subdomain-specific child factory-classes."""
        return BaseChoiceInject(**inject_data)

    @classmethod
    def _build_vars_from_dict(cls, scenario_vars):
        """Builds a single scenario variable from raw data."""
        new_vars = {}
        for var_name in scenario_vars:
            new_vars[var_name] = cls._build_variable(**scenario_vars[var_name])
        return new_vars

    @classmethod
    def _build_variable(cls, **var_data):
        """Creates the actual entity for the scenario variable.
        This method will be likely be overridden by subdomain-specific child factory-classes."""
        return BaseScenarioVariable(**var_data)


class ScenarioRepository(Repository):
    """Provides methods for accessing and persisting scenarios."""
    collection_name = "scenarios"

    @classmethod
    def get_factory(cls):
        """Get the right factory for creating domain-specific instances."""
        return ScenarioFactory

    @classmethod
    def get_scenario_by_id(cls, scenario_id: str):
        """
        :param scenario_id: the ID of the scenario to return. 'new' if a new scenario or placeholder should be created.
        :returns: The scenario instance.
        """
        factory = cls.get_factory()
        if scenario_id == "new":
            return factory.create_scenario(scenario_id="new")
        else:
            scenario_id, scenario_data = cls._get_entity_by_id(entity_id=scenario_id)
            scenario = factory.build_from_dict(scenario_id=scenario_id, **scenario_data)
            return scenario

    @classmethod
    def get_all_scenarios(cls):
        """
        Yield an iterator over all scenarios in the database.
        """
        scenario_entities = cls.my_db.get_all(cls.collection_name)
        for entity in scenario_entities:
            if "_id" in entity and "scenario_id" not in entity:
                entity["scenario_id"] = str(entity["_id"])
            factory = cls.get_factory()
            scenario = factory.build_from_dict(**entity)
            yield scenario

    @classmethod
    def save_scenario(cls, scenario: BaseScenario):
        """
        Updates the database entry of an existing scenario with the same ID.
        If the ID is not found or the scenario does not yet have an ID, the object will be inserted into the database.
        :param scenario: the scenario to be saved.
        :return: the saved scenario.
        """
        scenario_dict = scenario.dict()
        scenario_id = scenario_dict.pop("scenario_id", None)
        if not scenario.scenario_id or scenario.scenario_id == "":
            scenario_id = cls._insert_entity(entity=scenario_dict)
            scenario_dict.update({"scenario_id": scenario_id})
            scenario = cls.get_factory().build_from_dict(**scenario_dict)
            return scenario
        cls._update_entity(entity=scenario_dict,
                           entity_id=scenario_id)
        return scenario

    @classmethod
    def _insert_placeholder(cls, scenario_dict: dict):
        """Utility function. Inserts a placeholder into the database to generate a new ID."""
        return cls._insert_entity(entity=scenario_dict)

    @classmethod
    def delete_by_id(cls, scenario_id):
        """Delete a scenario that has the given ID."""
        cls._delete_one(scenario_id)
