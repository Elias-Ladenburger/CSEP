import os
from unittest import TestCase

from werkzeug.datastructures import FileStorage

from domain_layer.common.auxiliary import BaseScenarioVariable
from domain_layer.gameplay.mock_interface import MockScenarioBuilder
from presentation_layer import app_factory
from presentation_layer.controllers.scenario_design.scenario_forms import ScenarioForm, ScenarioVariableForm, InjectForm

from presentation_layer.app_factory import AppFactory


class ScenarioPersistenceTest(TestCase):
    def setUp(self) -> None:
        self.app = AppFactory.create_app()
        self.scenario = MockScenarioBuilder.build_scenario()
        self.test_dict = self._prepare_scenario(self.scenario)

    def tearDown(self) -> None:
        pass

    def test_form_conversion(self):
        demo_scenario = MockScenarioBuilder.build_scenario()
        with self.app.test_request_context():
            my_form = ScenarioForm(obj=demo_scenario)
            print(my_form)

    def test_image_form(self):
        demo_scenario = MockScenarioBuilder.build_scenario()
        value = "cybersecurity001-gr-bo.webp"
        with self.app.test_request_context():
            from presentation_layer.app import app
            import flask
            response = flask.send_from_directory(app.config["UPLOAD_FOLDER"], value)
            file_stream = response.response.file.raw
            file = FileStorage(stream=file_stream)
            my_form = InjectForm()
            my_form.media_path.process_data(file)
            print(my_form.media_path)

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

    def test_set_choices(self):
        with self.app.test_request_context():
            my_form = InjectForm()
            choices = app_factory.process_field_choices(self.scenario.get_all_injects(), "slug", "label")
            my_form.next_inject.choices = choices
            print(my_form.next_inject.choices)

    def _prepare_scenario(self, scenario):
        scenario_dict = scenario.dict()
        new_dict = {}
        for key in scenario_dict:
            new_key = "essentials_form-" + key
            new_dict[new_key] = scenario_dict[key]
        return new_dict
