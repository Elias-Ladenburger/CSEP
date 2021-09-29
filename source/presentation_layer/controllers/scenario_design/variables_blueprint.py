from flask import Blueprint, render_template, redirect, flash, url_for, request

from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository
from presentation_layer.controllers.scenario_design import auxiliary as aux
from presentation_layer.controllers.scenario_design.scenario_forms import *

variables_bp = Blueprint('variables', __name__,
                        template_folder='../../templates/scenario', url_prefix="/scenarios")


@variables_bp.route("/<scenario_id>/variables")
def edit_variables(scenario_id):
    scenario = aux.get_single_scenario(scenario_id=scenario_id)
    var_form = ScenarioVariableForm()
    return render_template("tab_variables.html", scenario=scenario, variables_form=var_form, active_tab="variables")


@variables_bp.route("/<scenario_id>/variables/add", methods=["POST"])
def save_variable(scenario_id):
    raw_form = request.form
    variable_form = ScenarioVariableForm(raw_form)
    if variable_form.validate():
        variable_dict = variable_form.data
        variable_dict["is_private"] = not variable_dict["visible_to_participants"]

        variable = BaseScenarioVariable(**variable_dict)
        scenario = EditableScenarioRepository.save_variable(scenario_id=scenario_id, variable=variable)
        flash("Save successful!", category="success")
        return redirect(request.referrer)
    else:
        flash("Something went wrong!", category="failure")
        redirect(request.referrer)
    return redirect(request.referrer)


@variables_bp.route("/<scenario_id>/variables/delete", methods=["DELETE"])
def delete_variable(scenario_id):
    scenario_var = request.form.get("variable_name", "")
    scenario = aux.get_single_scenario(scenario_id=scenario_id)
    scenario.remove_variable(scenario_var)
    EditableScenarioRepository.save_scenario(scenario)
    return redirect(url_for('variables.edit_variables', scenario_id=scenario_id))


@variables_bp.route('<scenario_id>/variables/<var_name>/edit')
def edit_variable(scenario_id, var_name):
    scenario = aux.get_single_scenario(scenario_id=scenario_id)
    scenario_var = scenario.variables.get(var_name)
    return variables_form(scenario, title="Edit variable", variable=scenario_var)


@variables_bp.route('<scenario_id>/variables/new')
def add_variable(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id)
    return variables_form(scenario=scenario, title="Add a variable")


def variables_form(scenario, title="Edit Variable", variable=None):
    form = ScenarioVariableForm()
    return render_template('/forms/variables_modal_form.html', title=title, variable=variable,
                           scenario=scenario, variables_form=form)
