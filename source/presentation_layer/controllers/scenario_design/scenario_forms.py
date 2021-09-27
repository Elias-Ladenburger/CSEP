from typing import List

from flask_wtf import FlaskForm
from flask_wtf import file as wtfile
from flask_wtf.file import FileAllowed
from markupsafe import Markup
from wtforms import StringField, FormField, TextAreaField, FieldList, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Optional, StopValidation
from wtforms.widgets import HiddenInput

from domain_layer.common.auxiliary import BaseScenarioVariable, DataType, LegalOperator
from domain_layer.common.injects import BaseInjectChoice, BaseInjectResult
from domain_layer.common.scenarios import BaseScenario
from domain_layer.scenariodesign.scenarios import EditableScenario, BaseStory

empty_pair = ("", "---")


class IgnoreIfEmpty(Optional):

    def __call__(self, form, field):
        if field.data is None or field.data == "":
            field.errors[:] = []
            raise StopValidation()
        super(IgnoreIfEmpty, self).__call__(form, field)


class CustomForm(FlaskForm):
    def populate_from_dict(self, entity_dict: dict):
        """Child methods will override this method."""
        for field in self.form:
            field_name = field.name.replace(self._prefix, "")
            field.data = entity_dict.get(field_name)


class CustomSelect(SelectField):
    def parse_available_options(self, scenario, allow_empty=True):
        """Prepare this field."""
        if not self.choices:
            self.choices = []
        if allow_empty:
            self.choices.append(empty_pair)
            self.default = empty_pair


class InjectField(CustomSelect):
    def parse_available_options(self, scenario, allow_empty=True):
        """Prepare this field such that a user can select any one of the injects of this scenario."""
        super().parse_available_options(scenario, allow_empty)
        choices = []
        injects = scenario.get_all_injects()
        for inject in injects:
            choices.append((inject.slug, inject.label))
        self.choices += choices


class VariableField(CustomSelect):
    def parse_available_options(self, scenario, allow_empty=True):
        """Prepare this field such that a user can select any one of the variables of this scenario."""
        super().parse_available_options(scenario, allow_empty)
        choices = [(var, var) for var in scenario.variables]
        self.choices += choices


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


class VariableChangeForm(CustomForm):
    variable_name = VariableField(Markup("I take this variable: <i class='fas fa-info-circle' "
                                         "data-toggle='tooltip' title='Should this choice influence any variables?'></i>"),
                                  default=empty_pair)

    value_operator = SelectField(Markup("And apply this operation <i class='fas fa-info-circle' "
                                        "data-toggle='tooltip' title='How should the variable be impacted?'></i>"),
                                 choices=LegalOperator.manipulation_operators(),
                                 validate_choice=True)

    new_value = StringField(Markup("With this value <i class='fas fa-info-circle' "
                                   "data-toggle='tooltip' title='How should the variable be impacted?'></i>"),
                            validators=[Optional()])

    def __init__(self, scenario=None, *args, **kwargs):
        super().__init__(csrf_enabled=False, **kwargs)
        if scenario:
            self.initialize(scenario)

    def initialize(self, scenario):
        self.variable_name.parse_available_options(scenario, True)

    def populate_from_dict(self, entity_dict: dict):
        self.variable_name.process_data(entity_dict.get("variable_name", "---"))
        self.value_operator.process_data(entity_dict.get("value_operator", "---"))
        self.new_value.process_data(entity_dict.get("new_value", ""))


class InjectChoiceForm(CustomForm):
    choice_label = StringField(Markup("Label <i class='fas fa-info-circle' "
                                      "data-toggle='tooltip' title='The actual choice that the participants see?'></i>"),
                               validators=[DataRequired()], default=" ")
    next_inject = InjectField(Markup("Alternative Inject <i class='fas fa-info-circle' "
                                     "data-toggle='tooltip' title='If this choice is taken, "
                                     "should participants be redirected to a different inject?'></i>"),
                              validate_choice=False)
    variable_changes = FieldList(FormField(VariableChangeForm), min_entries=0)

    def __init__(self, scenario=None, choice=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if scenario:
            self.initialize(scenario, choice)

    def initialize(self, scenario, choice: BaseInjectChoice = None):
        self.next_inject.parse_available_options(scenario)
        if choice:
            self.populate(choice)
            if choice.outcome.variable_changes:
                for var_change in choice.outcome.variable_changes:
                    new_var_change = self.variable_changes.append_entry()
                    new_var_change.initialize(scenario=scenario)
                    new_var_change.variable_name.process_data(var_change.var.name)
                    new_var_change.value_operator.process_data(var_change.operator)
                    new_var_change.new_value.process_data(var_change.new_value)
        new_var_change = self.variable_changes.append_entry()
        new_var_change.initialize(scenario=scenario)

    def populate(self, choice: BaseInjectChoice):
        self.choice_label.process_data(choice.label)
        if choice.outcome:
            if choice.outcome.next_inject:
                self.next_inject.process_data(choice.outcome.next_inject)


class InjectChoicesForm(CustomForm):
    choice_forms = FieldList(FormField(InjectChoiceForm), min_entries=0)

    def __init__(self, scenario: BaseScenario, **kwargs):
        super().__init__(**kwargs)
        self.scenario = scenario
        self.initialize()

    def initialize(self):
        for choice_entry in self.choice_forms.entries:
            choice_entry.initialize(scenario=self.scenario)
            for var_change in choice_entry.variable_changes:
                var_change.initialize(scenario=self.scenario)

    def populate(self, inject):
        for choice in inject.choices:
            new_entry = self.choice_forms.append_entry()
            new_entry.initialize(scenario=self.scenario, choice=choice)

    def add_option(self):
        new_entry = self.choice_forms.append_entry()
        new_entry.initialize(scenario=self.scenario)

    def validate(self, extra_validators=None):
        for i, choice_entry in enumerate(self.choice_forms.entries):
            choice_label = choice_entry.data["choice_label"]
            if not choice_label or choice_label == " ":
                self.choice_forms.entries.pop(i)
            else:
                to_remove = []
                for j, var_change in enumerate(choice_entry.variable_changes.entries):
                    if not var_change.validate(form=self):
                        to_remove.append(j)
                        print(var_change.errors)
                        print(var_change.data)
                    elif not var_change.variable_name.data:
                        to_remove.append(j)
                for j in reversed(to_remove):
                    choice_entry.variable_changes.entries.pop(j)
        return super().validate(extra_validators=extra_validators)


class InjectConditionForm(CustomForm):
    variable_name = VariableField(Markup("If I take this variable: <i class='fas fa-info-circle' "
                                         "data-toggle='tooltip' title='Which variable should have an impact, "
                                         "whether this inject is shown?'></i>"))
    comparison_operator = SelectField(Markup("And use this operator to compare <i class='fas fa-info-circle' "
                                             "data-toggle='tooltip' title='How should the variable be compared?'></i>"),
                                      choices=LegalOperator.comparison_operators())
    variable_threshold = StringField(Markup("Against this value <i class='fas fa-info-circle' "
                                            "data-toggle='tooltip' title='What value should the variable be compared against?'></i>"))
    alternative_inject = InjectField(Markup("Then I should go to this inject instead <i class='fas fa-info-circle' "
                                            "data-toggle='tooltip' title='What happens if the condition is met?'></i>"))

    def initialize(self, scenario, inject=None):
        self.variable_name.parse_available_options(scenario)
        self.alternative_inject.parse_available_options(scenario)
        if inject and inject.condition:
            self.populate_from_dict(inject.condition.dict())

    def populate_from_dict(self, entity_dict: dict):
        self.variable_name.process_data(entity_dict.get("variable_name", "---"))
        self.comparison_operator.process_data(entity_dict.get("comparison_operator", "---"))
        self.variable_threshold.process_data(entity_dict.get("variable_threshold", ""))
        self.alternative_inject.process_data(entity_dict.get("alternative_inject", "---"))


class InjectForm(CustomForm):
    slug = HiddenField("Inject Slug", default="new-inject")

    label = StringField(Markup("Title <i class='fas fa-info-circle' "
                               "data-toggle='tooltip' title='A short descriptive title for this injct.'></i>"),
                        validators=[DataRequired()])

    text = TextAreaField(Markup("Inject Text <i class='fas fa-info-circle' "
                                "data-toggle='tooltip' title='What exactly does this inject say?'></i>"),
                         validators=[DataRequired()], render_kw={'class': 'form-control', 'rows': 6})

    media_path = wtfile.FileField(Markup("Image <i class='fas fa-info-circle' "
                                         "data-toggle='tooltip' title='Images and perhaps even short video clips make injects much more immersive.'></i>")
                                  , validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp',
                                                                         'mp4', 'mov'])])
    remove_image = BooleanField("Remove Image?", validators=[Optional()], default=False, widget=HiddenInput())

    next_inject = InjectField(Markup("Next Inject <i class='fas fa-info-circle' "
                                     "data-toggle='tooltip' title='Which inject should follow this one per default?'></i>"),
                              validators=[Optional()])

    preceded_by = InjectField(Markup("Preceding Inject <i class='fas fa-info-circle' "
                                     "data-toggle='tooltip' title='Should one of the existing injects point to this new inject per default?'></i>"),
                              validators=[Optional()])

    is_entry_node = BooleanField(Markup("Is Entry Node <i class='fas fa-info-circle' "
                                        "data-toggle='tooltip' title='Should this inject be the first inject in the scenario?'></i>"),
                                 default=False)

    def __init__(self, scenario=None, inject=None, *args, **kwargs):
        self.condition = InjectConditionForm()
        super().__init__(*args, **kwargs)
        if scenario:
            self.initialize(scenario, inject)

    def initialize(self, scenario, inject=None):
        self.next_inject.parse_available_options(scenario)
        self.preceded_by.parse_available_options(scenario)
        self.condition.initialize(scenario)
        if inject:
            self.populate(scenario, inject)

    def populate(self, scenario, inject):
        """Populate this form with the values of an existing inject."""
        self.next_inject.process_data(inject.next_inject)
        self.media_path.process_data(inject.media_path)
        self.slug.process_data(inject.slug)
        self.label.process_data(inject.label)
        self.text.process_data(inject.text)
        if scenario.stories[0].entry_node.slug == inject.slug:
            self.is_entry_node.process_data(True)


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
