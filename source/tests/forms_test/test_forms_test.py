from unittest import TestCase

from domain.common.auxiliary import BaseScenarioVariable
from domain.game_play.mock_interface import MockScenarioBuilder
from web.controllers.scenario_design.scenario_forms import ScenarioForm, ScenarioVariableForm

from web.app_factory import AppFactory


class ScenarioPersistenceTest(TestCase):
    def setUp(self) -> None:
        self.app = AppFactory.create_app()
        self.test_dict = self._prepare_scenario()

    def tearDown(self) -> None:
        pass

    def test_form_validation(self):
        with self.app.test_request_context():
            my_form = ScenarioForm(formdata=self.test_dict)
            self.assertTrue(my_form.core_form.validate(my_form.core_form))

    def test_form_conversion(self):
        demo_scenario = MockScenarioBuilder.build_scenario()
        with self.app.test_request_context():
            my_form = ScenarioForm(obj=demo_scenario)
            print(my_form)

    def test_hidden(self):
        with self.app.test_request_context():
            my_form = ScenarioForm()
            hidden_field = my_form.core_form.scenario_id
            print(hidden_field)
            self.assertTrue('type="hidden"' in str(hidden_field))

    def test_prerender_form(self):
        with self.app.test_request_context():
            my_form = ScenarioVariableForm()
            budget = BaseScenarioVariable(name="budget", value=100000, datatype="numeric", is_private=False)
            budget_dict = budget.dict()
            for field in my_form:
                if field.name in budget_dict:
                    field.data = budget_dict[field.name]
                print(field)

    def _prepare_scenario(self):
        demo_scenario = MockScenarioBuilder.build_scenario()
        scenario_dict = demo_scenario.dict()
        new_dict = {}
        for key in scenario_dict:
            new_key = "essentials_form-" + key
            new_dict[new_key] = scenario_dict[key]
        return new_dict
