from unittest import TestCase

from domain_layer.common.scenario_management import ScenarioRepository
from domain_layer.scenariodesign.scenarios import EditableScenario
from presentation_layer.controllers.scenario_design.auxiliary import update_scenario_element, delete_scenario_element


class ApiTest(TestCase):
    def test_edit_element(self):
        scenario_id = "6151a4118193e14ce36cfcbb"
        scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
        element_path = "stories/0/injects/first-inject/choices/1/variable-changes/0"
        path_list = element_path.split("/")
        print(scenario.get_inject_by_slug("first-inject").choices[1].outcome.variable_changes)
        changed_scenario = update_scenario_element(scenario_id=scenario_id,
                                element_path=path_list, new_value=None)
        changed_scenario = EditableScenario(**changed_scenario)
        print(changed_scenario.get_inject_by_slug("first-inject").choices[1].outcome.variable_changes)


    def test_delete_element(self):
        scenario_id = "6151a4118193e14ce36cfcbb"
        scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
        element_path = "stories/0/injects/first-inject/choices/1/outcome/variable_changes/0"
        path_list = element_path.split("/")
        print(scenario.get_inject_by_slug("first-inject").choices[1].outcome.variable_changes)
        changed_scenario = delete_scenario_element(scenario_dict=scenario.dict(),
                                element_path=path_list)
        changed_scenario = EditableScenario(**changed_scenario)
        print(changed_scenario.get_inject_by_slug("first-inject").choices[1].outcome.variable_changes)
