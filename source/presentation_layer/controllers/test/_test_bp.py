from flask import Blueprint, url_for, render_template, request, redirect

from domain_layer.common.injects import BaseInjectChoice, BaseInjectResult
from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository
from presentation_layer.controllers.scenario_design.scenario_forms import InjectForm

_test_bp = Blueprint('tests', __name__,
                    template_folder='../../templates/scenario_design', url_prefix="/test")


@_test_bp.route("<scenario_id>/forms_test", methods=["GET", "POST"])
def create_new_inject(scenario_id):
    return redirect(url_for("tests.test_inject_form", scenario_id=scenario_id, inject_slug="new"))


@_test_bp.route("<scenario_id>/forms_test/<inject_slug>", methods=["GET", "POST"])
def test_inject_form(scenario_id, inject_slug):
    scenario = get_single_scenario(scenario_id)
    inject_form = InjectForm(scenario)
    if request.method == "GET":
        if inject_slug != "new":
            scenario = get_single_scenario(scenario_id)
            inject = scenario.get_inject_by_slug(inject_slug)
            inject_form = InjectForm(scenario, inject)
            for choice in inject.choices:
                inject_form.choices.append_entry(choice.dict())
    elif inject_form.validate_on_submit():
        for choice in inject_form.choices.entries:
            new_choice = BaseInjectChoice(label=choice.data["label"],
                                          outcome=BaseInjectResult(next_inject=choice.data["next_inject"],
                                                                   variable_changes=choice.data["variable_changes"]))
            print(new_choice.json())
        inject_form.choices.append_entry()
    else:
        print(inject_form.errors)
    return render_template('/forms/form_test.html', form=inject_form,
                           url=url_for('tests.test_inject_form', scenario_id=scenario_id, inject_slug=inject_slug))


def get_single_scenario(scenario_id):
    return EditableScenarioRepository.get_scenario_by_id(scenario_id)