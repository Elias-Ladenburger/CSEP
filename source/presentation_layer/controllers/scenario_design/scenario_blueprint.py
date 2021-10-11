import flask
from flask import Blueprint, render_template, redirect, flash, url_for

from application_layer.m2m_transformation import InjectTransformer
from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository, EditableScenarioFactory
from presentation_layer.controllers.scenario_design.scenario_forms import *
import presentation_layer.controllers.scenario_design.auxiliary as aux

scenario_bp = Blueprint('scenarios', __name__,
                        template_folder='../../templates/scenario_design', url_prefix="/scenarios")


@scenario_bp.route("/", strict_slashes=False)
def show_scenarios():
    scenarios = EditableScenarioRepository.get_all_scenarios()
    core_form = ScenarioCoreForm()
    scenarios = list(scenarios)
    return render_template("scenarios_overview.html", scenarios=scenarios, core_form=core_form)


@scenario_bp.route("/<scenario_id>/edit", methods=["GET", "POST"])
def edit_scenario(scenario_id):
    return redirect(url_for('scenarios.edit_core', scenario_id=scenario_id))


@scenario_bp.route("/new")
def new_scenario():
    scenario = EditableScenarioFactory.create_scenario(scenario_id="new")
    core_form = ScenarioCoreForm()
    return render_template("tab_core_info.html", scenario=scenario, core_form=core_form)


@scenario_bp.route("/save", methods=["POST"])
def save_scenario():
    raw_form = flask.request.form
    scenario_form = ScenarioCoreForm(raw_form)
    if scenario_form.validate():
        scenario_dict = scenario_form.data
        if "scenario_id" in scenario_dict and scenario_dict["scenario_id"]:
            scenario_id = scenario_dict["scenario_id"]
            scenario_id = EditableScenarioRepository.partial_update(scenario_dict, scenario_id)
            scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id)
        else:
            scenario = EditableScenarioFactory.build_from_dict(**scenario_dict)
            scenario = EditableScenarioRepository.save_scenario(scenario)
        flash("Scenario saved successfully!", category="success")
        return redirect(url_for('scenarios.edit_scenario', scenario_id=scenario.scenario_id))
    else:
        print(scenario_form.errors)
        flash("Something went wrong!", category="failure")
        redirect(flask.request.referrer)
    return redirect(flask.request.referrer)


@scenario_bp.route("/delete", methods=["DELETE"])
def delete_scenario():
    scenario_id = flask.request.form.get("scenario_id", None)
    if scenario_id:
        EditableScenarioRepository.delete_by_id(scenario_id)
    return show_scenarios()


@scenario_bp.route("/<scenario_id>/core")
def edit_core(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id)
    core_form = ScenarioCoreForm()
    return render_template("tab_core_info.html", scenario=scenario, core_form=core_form, active_tab="core")


@scenario_bp.route("/<scenario_id>/stats")
def show_stats(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_stats.html", scenarios=[scenario])
