from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, TextAreaField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import HiddenInput

from domain.scenario_design.scenario import Scenario
from domain.scenario_design.scenario_management import ScenarioFactory


class ScenarioEssentialsForm(FlaskForm):
    scenario_id = StringField([DataRequired()], widget=HiddenInput())
    title = StringField("Name", validators=[DataRequired("Please provide a short title for your scenario")])
    scenario_description = TextAreaField("Description",
                                         validators=[DataRequired("Please provide a description for your scenario")],
                                         render_kw={"id": "description",
                                                    "type": "text"})

    learning_objectives = TextAreaField("Learning Objectives",
                                        render_kw={"data-role": "tags-input",
                                                   "type": "text"})

    target_group = TextAreaField("Target Group",
                                 render_kw={"data-role": "tags-input"})

    required_knowledge = TextAreaField("Required Knowledge",
                                       render_kw={"data-role": "tags-input"})

    save_button = SubmitField("Save")

    def __init__(self, scenario=None, **kwargs):
        super().__init__(**kwargs)

    def populate_from_scenario(self, scenario):
        if scenario:
            if isinstance(scenario, Scenario):
                self.scenario_id.data = scenario.scenario_id or None
                self.title.data = scenario.title
                self.scenario_description.data = scenario.scenario_description
                self.learning_objectives.data = scenario.learning_objectives
                self.target_group.data = scenario.target_group
                self.required_knowledge.data = scenario.required_knowledge


class StoryForm(FlaskForm):
    story_title = StringField("Title", validators=[DataRequired()], render_kw={})
    save_button = SubmitField("Save")


class InjectForm(FlaskForm):
    pass


class ScenarioVariableForm(FlaskForm):
    pass


class ScenarioForm(FlaskForm):
    essentials_form = FormField(ScenarioEssentialsForm)
    story_form = FormField(StoryForm)
    inject_form = FormField(InjectForm)
    variables_form = FormField(ScenarioVariableForm)

    def __init__(self, scenario=None, **kwargs):
        super().__init__(**kwargs)
        self.essentials_form.form.populate_from_scenario(scenario)


class Form2ScenarioConverter:
    @classmethod
    def convert_form2scenario(cls, **scenario_fields):
        for field in scenario_fields:
            pass

    @classmethod
    def convert_form2story(cls, **story_fields):
        pass

    @classmethod
    def convert_form2inject(cls, **inject_fields):
        pass
