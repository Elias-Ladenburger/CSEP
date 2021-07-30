from typing import List

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from markupsafe import Markup
from wtforms import StringField, FormField, TextAreaField, FieldList, SelectField, Form
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import HiddenInput

from domain.common.auxiliary import BaseScenarioVariable, DataType
from domain.scenario_design.scenario import Scenario, Story


class CustomForm(Form):
    class Meta:
        csrf = False

    def populate_from_dict(self, entity_dict: dict):
        """Child methods will override this method to """
        for field in self.form:
            field_name = field.name.replace(self._prefix, "")
            field.data = entity_dict.get(field_name)


class ScenarioEssentialsForm(CustomForm):
    scenario_id = StringField([DataRequired()], widget=HiddenInput())
    title = StringField(Markup('Name <i class="fas fa-info-circle" '
                               'data-toggle="tooltip" title="A descriptive name for your scenario!"></i>'),
                        validators=[DataRequired("Please provide a short title for your scenario")],
                        render_kw={"data-toggle": "tooltip",
                                   "title": "A descriptive name of the scenario!"})
    scenario_description = TextAreaField(Markup('Description <i class="fas fa-info-circle" '
                                                'data-toggle="tooltip" '
                                                'title="A short description of your scenario '
                                                'so that participants know what to expect!"></i>'),
                                         validators=[DataRequired("Please provide a description for your scenario")],
                                         render_kw={"id": "description",
                                                    "type": "text"})

    learning_objectives = TextAreaField(Markup('Learning Objectives <i class="fas fa-info-circle" '
                                               'data-toggle="tooltip" '
                                               'title="What do you want participants to learn from this scenario?"></i>'),
                                        render_kw={"data-role": "tags-input",
                                                   "type": "text"})

    target_group = TextAreaField(Markup('Target Group '
                                        '<i class="fas fa-info-circle" '
                                        'data-toggle="tooltip" '
                                        'title="Who is this scenario suitable for?"></i>'),
                                 render_kw={"data-role": "tags-input"})

    required_knowledge = TextAreaField(Markup('Required Knowledge '
                                              '<i class="fas fa-info-circle" '
                                              'data-toggle="tooltip" '
                                              'title="What skills do participants need to have '
                                              'before starting this scenario?"></i>'),
                                       render_kw={"data-role": "tags-input"})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def populate_from_dict(self, scenario_dict):
        if scenario_dict:
            self.scenario_id.data = scenario_dict.get("scenario_id", None)
            self.title.data = scenario_dict.get("title")
            self.scenario_description.data = scenario_dict.get("scenario_description")
            self.learning_objectives.data = scenario_dict.get("learning_objectives")
            self.target_group.data = scenario_dict.get("target_group")
            self.required_knowledge.data = scenario_dict.get("required_knowledge")


class InjectForm(CustomForm):
    label = StringField("Title", validators=[DataRequired()])
    text = TextAreaField(Markup("Inject Text <i class='fas fa-info-circle' "
                                "data-toggle='tooltip' title='What exactly does this inject say?'></i>"),
                         validators=[DataRequired()])
    image = FileField("Image", validators=[Optional()])


class StoryForm(CustomForm):
    story_title = StringField("Title", validators=[DataRequired()], render_kw={})
    inject_form = FieldList(FormField(InjectForm), min_entries=1)


class ScenarioVariableForm(CustomForm):
    name = StringField("Variable Name")
    datatype_choices = [(elem.name, elem.value) for elem in DataType]
    datatype = SelectField("Datatype", choices=datatype_choices)
    value = StringField("Default Value")


class ScenarioForm(FlaskForm):
    essentials_form = FormField(ScenarioEssentialsForm)
    stories_form = FieldList(FormField(StoryForm))
    variables_form = FieldList(FormField(ScenarioVariableForm))

    def __init__(self, scenario=None, stories: List[Story] = None, variables: List[BaseScenarioVariable] = None, **kwargs):
        super().__init__(**kwargs)
        if isinstance(scenario, Scenario):
            self.essentials_form.form.populate_from_dict(scenario.dict())
        if stories:
            if isinstance(stories[0], Story):
                for story in stories:
                    self.stories_form.append_entry(stories)


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
