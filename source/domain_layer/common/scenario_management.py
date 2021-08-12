import json
from typing import List

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
    def build_from_dict(cls, **kwargs):
        return BaseScenario(**kwargs)


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
