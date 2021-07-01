from domain.scenario_design.auxiliary import ScenarioVariable
from domain.scenario_design.scenario import Scenario
from infrastructure.repository import Repository


class ScenarioRepository(Repository):
    collection_name = "scenarios"

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
    def get_scenarios_by_target_group(cls, target_group: str):
        return NotImplementedError("This has not yet been implemented!")

    @classmethod
    def get_all_scenarios(cls):
        return cls.my_db.get_all(cls.collection_name)

    @classmethod
    def save_scenario(cls, scenario: Scenario):
        """
        Takes a scenario and saves it to the database.
        :param scenario: the scenario to be saved.
        :return: the saved scenario.
        """
        scenario_dict = scenario.dict()
        scenario_id = scenario_dict.pop("scenario_id", None)
        if not scenario.scenario_id or scenario.scenario_id == "":
            scenario_id = cls._insert_entity(collection_name=cls.collection_name, entity=scenario_dict)
            scenario_dict.update({"scenario_id": scenario_id})
            return ScenarioFactory.build_scenario_from_dict(scenario_dict)
        cls._update_entity(collection_name=cls.collection_name, entity=scenario_dict,
                           entity_id=scenario_id)
        return scenario

    @classmethod
    def insert_placeholder(cls, scenario_dict: dict):
        return cls._insert_entity(collection_name=cls.collection_name, entity=scenario_dict)


class ScenarioFactory:

    @staticmethod
    def create_scenario(title="new scenario", description="This is a new scenario"):
        new_scenario = Scenario(title=title, description=description)
        return new_scenario

    @staticmethod
    def build_scenario_from_dict(**scenario_data):
        scenario_id = scenario_data.pop("scenario_id", None) or scenario_data.pop("_id", None)
        title = scenario_data.pop("title", "new scenario")
        description = scenario_data.pop("description", "new scenario description")

        stories = scenario_data.pop("stories", [])
        scenario_vars = scenario_data.pop("variables", {})
        var_values = scenario_data.pop("variable_values", {})

        scenario = Scenario(title=title, description=description, scenario_id=scenario_id)
        for story in stories:
            scenario.add_story(story)
        for var_name in scenario_vars:
            scenario.add_variable(ScenarioVariable(**scenario_vars[var_name]), var_values[var_name])
        return scenario
