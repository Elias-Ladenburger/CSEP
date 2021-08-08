from typing import List

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from markupsafe import Markup
from wtforms import StringField, FormField, TextAreaField, FieldList, SelectField, Form, BooleanField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import HiddenInput

from domain_layer.common.auxiliary import BaseScenarioVariable, DataType
from domain_layer.scenario_design.scenarios import EditableScenario, BaseStory


class CustomForm(Form):

    def populate_from_dict(self, entity_dict: dict):
        """Child methods will override this method to """
        for field in self.form:
            field_name = field.name.replace(self._prefix, "")
            field.data = entity_dict.get(field_name)


class ScenarioCoreForm(CustomForm):
    scenario_id = StringField([DataRequired()], widget=HiddenInput())
    title = StringField(Markup('Name <i class="fas fa-info-circle" '
                               'data-toggle="tooltip" title="A descriptive name for your scenario!"></i>'),
                        validators=[DataRequired("Please provide a short title for your scenario")])
    scenario_description = TextAreaField(Markup('Description <i class="fas fa-info-circle" '
                                                'data-toggle="tooltip" '
                                                'title="A short description of your scenario '
                                                'so that participants know what to expect!"></i>'),
                                         validators=[DataRequired("Please provide a description for your scenario")],
                                         render_kw={"id": "description",
                                                    "type": "text"})

    learning_objectives = StringField(Markup('Learning Objectives <i class="fas fa-info-circle" '
                                             'data-toggle="tooltip" '
                                             'title="What do you want participants to learn from this scenario?"></i>'),
                                      render_kw={"data-role": "tags-input",
                                                 "type": "text"})

    target_group = StringField(Markup('Target Group '
                                      '<i class="fas fa-info-circle" '
                                      'data-toggle="tooltip" '
                                      'title="Who is this scenario suitable for?"></i>'),
                               render_kw={"data-role": "tags-input"})

    required_knowledge = StringField(Markup('Required Knowledge '
                                            '<i class="fas fa-info-circle" '
                                            'data-toggle="tooltip" '
                                            'title="What skills do participants need to have '
                                            'before starting this scenario?"></i>'),
                                     render_kw={"data-role": "tags-input"})


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
    name = StringField(Markup("Variable Name <i class='fas fa-info-circle' "
                              "data-toggle='tooltip' title='What does this variable mean?'></i>"),
                       validators=[DataRequired("Please provide a name for the variable")])

    datatype_choices = [(elem.value, elem.value) for elem in DataType]
    datatype = SelectField(Markup("Datatype <i class='fas fa-info-circle' "
                                  "data-toggle='tooltip' title='Is this variable qualitative (textual), "
                                  "quantitative (numerical) or binary truth (true/false, also known as a boolean)?'></i>"),
                           choices=datatype_choices)

    value = StringField(Markup("Default Value <i class='fas fa-info-circle' "
                               "data-toggle='tooltip' title='The starting value of this variable'></i>"),
                        validators=[DataRequired("Please provide a default value for the variable")])

    is_private = BooleanField(Markup("Hide from Participants? <i class='fas fa-info-circle' "
                                     "data-toggle='tooltip' title='You might want some variables to influence the "
                                     "course of the scenario, but not make participants aware of this.'></i>"),
                              default=False)


class ScenarioForm(FlaskForm):
    core_form = FormField(ScenarioCoreForm)
    stories_form = FieldList(FormField(StoryForm))
    variables_form = FieldList(FormField(ScenarioVariableForm))

    def __init__(self, scenario=None, stories: List[BaseStory] = None, variables: List[BaseScenarioVariable] = None,
                 **kwargs):
        super().__init__(**kwargs)
        if isinstance(scenario, EditableScenario):
            self.core_form.form.populate_from_dict(scenario.dict())
        if stories:
            if isinstance(stories[0], BaseStory):
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
