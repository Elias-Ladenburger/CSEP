import json
from typing import List

from domain_layer.common.auxiliary import BaseScenarioVariable
from domain_layer.common.injects import BaseChoiceInject
from domain_layer.common.scenarios import BaseScenario, BaseStory
from infrastructure_layer.repository import Repository


class ScenarioFactory:
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
                        stories, variables, **scenario_data):
        return BaseScenario(title=title, scenario_description=scenario_description,
                            scenario_id=scenario_id, stories=stories, variables=variables, **scenario_data)

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
        entry_slug = story_data.pop("entry_node", "")
        injects = {}

        for inject_data in injects_data:
            inject = cls._build_inject_from_dict(inject_data=injects_data[inject_data])
            injects[inject.slug] = inject

        story = cls._build_story(**story_data, entry_slug=entry_slug, injects=injects)
        return story

    @classmethod
    def _build_story(cls, entry_slug, injects, **story_data):
        return BaseStory(**story_data, entry_node=entry_slug, injects=injects)

    @classmethod
    def _build_inject_from_dict(cls, **inject_data):
        inject = cls._build_inject(**inject_data)
        return inject

    @classmethod
    def _build_inject(cls, inject_data):
        return BaseChoiceInject(**inject_data)

    @classmethod
    def _build_vars_from_dict(cls, scenario_vars):
        new_vars = {}
        for var_name in scenario_vars:
            new_vars[var_name] = cls._build_variable(**scenario_vars[var_name])
        return new_vars

    @classmethod
    def _build_variable(cls, **var_data):
        return BaseScenarioVariable(**var_data)


class ScenarioRepository(Repository):
    collection_name = "scenarios"
    story_collection_name = "stories"

    @classmethod
    def get_factory(cls):
        return ScenarioFactory

    @classmethod
    def get_scenario_by_id(cls, scenario_id: str):
        factory = cls.get_factory()
        if scenario_id == "new":
            return factory.create_scenario(scenario_id="new")
        else:
            scenario_id, scenario_data = cls._get_entity_by_id(
                collection_name=cls.collection_name, entity_id=scenario_id)
            scenario = factory.build_from_dict(scenario_id=scenario_id, **scenario_data)
            return scenario

    @classmethod
    def update_stories(cls, scenario_id: str, new_stories: List[BaseStory]):
        scenario = cls.get_scenario_by_id(scenario_id=scenario_id)
        scenario.stories = new_stories
        cls.save_scenario(scenario)

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
            scenario_id = cls._insert_entity(collection_name=cls.collection_name, entity=scenario_dict)
            scenario_dict.update({"scenario_id": scenario_id})
            scenario = cls.get_factory().build_from_dict(**scenario_dict)
            return scenario
        cls._update_entity(collection_name=cls.collection_name, entity=scenario_dict,
                           entity_id=scenario_id)
        return scenario

    @classmethod
    def _update_stories(cls, stories_as_dict: dict, scenario_id):
        for story_dict in stories_as_dict:
            story_id = story_dict.pop("_id")
            story_dict["scenario_id"] = scenario_id
            cls._update_entity(collection_name="stories", entity=story_dict,
                               entity_id=story_id)
        return

    @classmethod
    def _insert_placeholder(cls, scenario_dict: dict):
        """Utility function. Inserts a placeholder into the database to generate a new ID."""
        return cls._insert_entity(collection_name=cls.collection_name, entity=scenario_dict)

    @classmethod
    def delete_by_id(cls, scenario_id):
        cls._delete_one(cls.collection_name, scenario_id)


class ScenarioTransformer:
    @staticmethod
    def scenario_as_json(scenario: BaseScenario):
        scenario_dict = scenario.dict()
        return json.dumps(scenario_dict)

    @staticmethod
    def scenario_as_dict(scenario: BaseScenario):
        return scenario.dict()

    @staticmethod
    def scenarios_as_json(scenarios: List[BaseScenario]):
        scenario_list = []
        for scenario in scenarios:
            scenario_list.append(ScenarioTransformer.scenario_as_dict(scenario))
        scenario_dict = {"scenarios": scenario_list}
        return json.dumps(scenario_dict)

    @staticmethod
    def scenarios_as_dict(scenarios: List[BaseScenario]):
        scenario_list = ScenarioTransformer.scenarios_as_json_list(scenarios)
        scenarios_dict = {"scenarios": scenario_list}
        return scenarios_dict

    @staticmethod
    def scenarios_as_json_list(scenarios: List[BaseScenario]):
        scenario_list = []
        for scenario in scenarios:
            scenario_list.append(ScenarioTransformer.scenario_as_dict(scenario))
        return scenario_list
