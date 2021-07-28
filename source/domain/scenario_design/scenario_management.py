import json
from typing import List

from domain.scenario_design.auxiliary import ScenarioVariable
from domain.scenario_design.injects import Inject, InjectChoice
from domain.scenario_design.scenario import Scenario, Story
from infrastructure.repository import Repository


class ScenarioRepository(Repository):
    collection_name = "scenarios"
    story_collection_name = "stories"

    @classmethod
    def get_scenario_by_id(cls, scenario_id: str):
        scenario_id, scenario_data = cls._get_entity_by_id(collection_name=cls.collection_name, entity_id=scenario_id)
        try:
            scenario = ScenarioFactory.build_scenario_from_dict(scenario_id=scenario_id, **scenario_data)
            return scenario
        except AttributeError as attre:
            print(attre)
            return None

    @classmethod
    def get_scenario_stories(cls, scenario_id: str):
        # TODO: implement getting scenario stories
        stories = cls.get_all(collection_name=cls.story_collection_name, )

    @classmethod
    def get_scenarios_by_target_group(cls, target_group: str):
        return NotImplementedError("This has not yet been implemented!")

    @classmethod
    def get_all_scenarios(cls):
        """
        Yield an iterator over all scenarios in the database.
        """
        scenario_entities = cls.my_db.get_all(cls.collection_name)
        for entity in scenario_entities:
            scenario = ScenarioFactory.build_scenario_from_dict(**entity)
            yield scenario

    @classmethod
    def save_scenario(cls, scenario: Scenario):
        """
        Updates the database entry of an existing scenario with the same ID.
        If the ID is not found or the scenario does not yet have an ID, the object will be inserted into the database.
        :param scenario: the scenario to be saved.
        :return: the saved scenario.
        """
        scenario_dict = scenario.dict()
        scenario_id = scenario_dict.pop("scenario_id", None)
        story_dict = scenario_dict.pop("stories")
        if not scenario.scenario_id or scenario.scenario_id == "":
            scenario_id = cls._insert_entity(collection_name=cls.collection_name, entity=scenario_dict)
            scenario_dict.update({"scenario_id": scenario_id})
            return ScenarioFactory.build_scenario_from_dict(**scenario_dict)
        cls._update_entity(collection_name=cls.collection_name, entity=scenario_dict,
                           entity_id=scenario_id)
        cls._update_stories(stories_as_dict=story_dict, scenario_id=scenario_id)
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


class ScenarioFactory:

    @staticmethod
    def create_scenario(title="new scenario", description="This is a new scenario", **kwargs):
        """
        Creates a new scenario object.
        """
        new_scenario = Scenario(title=title, scenario_description=description, **kwargs)
        return new_scenario

    @staticmethod
    def build_scenario_from_dict(**scenario_data):
        """
        Takes any number of keywords as argument and tries to build a valid scenario object from the key-value pairs.
        """
        scenario_id = scenario_data.pop("scenario_id", None) or scenario_data.pop("_id", None)
        title = scenario_data.pop("title", "new scenario")
        description = scenario_data.pop("scenario_description", None) or scenario_data.pop("description")

        stories = scenario_data.pop("stories", [])
        scenario_vars = scenario_data.pop("variables", {})
        var_values = scenario_data.pop("variable_values", {})

        scenario = Scenario(title=title, scenario_description=description, scenario_id=scenario_id, **scenario_data)

        ScenarioFactory._build_stories_from_dict(
            stories_data=stories, scenario=scenario)

        ScenarioFactory._build_vars_from_dict(scenario_vars=scenario_vars, var_values=var_values, scenario=scenario)

        return scenario

    @staticmethod
    def _build_stories_from_dict(stories_data, scenario):
        for story_data in stories_data:
            scenario = ScenarioFactory._build_story_from_dict(story_data, scenario)
        return scenario

    @staticmethod
    def _build_story_from_dict(story_data, scenario):
        injects_data = story_data.pop("injects", {})
        transitions_data = story_data.pop("transitions", {})
        entry_data = story_data.pop("entry_node", {})
        entry_node = ScenarioFactory._build_inject_from_dict(entry_data)

        story = Story(**story_data, entry_node=entry_node)

        for inject_data in injects_data:
            inject = ScenarioFactory._build_inject_from_dict(inject_data=injects_data[inject_data])
            story.add_inject(inject)

        for raw_transition in transitions_data:
            transition_data = transitions_data[raw_transition]
            for transition_dao in transition_data:
                transition = ScenarioFactory._build_transition_from_dict(transition_data=transition_dao, story=story)
                story.add_transition(transition)
        scenario.add_story(story)
        return scenario

    @staticmethod
    def _build_inject_from_dict(inject_data):
        inject_data.pop("slug")
        inject = Inject(**inject_data)
        return inject

    @staticmethod
    def _build_transition_from_dict(transition_data, story):
        transition_data["from_inject"] = story.get_inject_by_slug(transition_data["from_inject"])
        transition_data["to_inject"] = story.get_inject_by_slug(transition_data["to_inject"])
        transition = InjectChoice(**transition_data)
        return transition

    @staticmethod
    def _build_vars_from_dict(scenario_vars, var_values, scenario):
        for var_name in scenario_vars:
            scenario.add_variable(ScenarioVariable(**scenario_vars[var_name]), var_values[var_name])
        return scenario


class ScenarioTransformer:
    @staticmethod
    def scenario_as_json(scenario: Scenario):
        scenario_dict = scenario.dict()
        return json.dumps(scenario_dict)

    @staticmethod
    def scenario_as_dict(scenario: Scenario):
        return scenario.dict()

    @staticmethod
    def scenarios_as_json(scenarios: List[Scenario]):
        scenario_list = []
        for scenario in scenarios:
            scenario_list.append(ScenarioTransformer.scenario_as_dict(scenario))
        scenario_dict = {"scenarios": scenario_list}
        return json.dumps(scenario_dict)

    @staticmethod
    def scenarios_as_dict(scenarios: List[Scenario]):
        scenario_list = []
        for scenario in scenarios:
            scenario_list.append(ScenarioTransformer.scenario_as_dict(scenario))
        scenarios_dict = {"scenarios": scenario_list}
        return scenarios_dict

