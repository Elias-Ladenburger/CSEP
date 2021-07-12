import flask
from flask import Blueprint, render_template, redirect, url_for

from domain.scenario_design.scenario_management import ScenarioRepository, ScenarioFactory

scenario_bp = Blueprint('scenarios', __name__,
                        template_folder='templates/scenario', url_prefix="/scenarios")


@scenario_bp.route("/")
def show_scenarios():
    scenarios = ScenarioRepository.get_all_scenarios()
    return render_template("scenarios_overview.html", scenarios=scenarios)


@scenario_bp.route("/<scenario_id>/edit")
def edit_scenario(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_edit.html", scenario=scenario)


@scenario_bp.route("/<scenario_id>/stats")
def show_stats(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_stats.html", scenarios=[scenario])


@scenario_bp.route("/new")
def new_scenario():
    scenario = ScenarioFactory.create_scenario()
    return render_template("scenario_edit.html", scenario=scenario)


@scenario_bp.route("/save")
def save_scenario(**kwargs):
    kwargs.update(flask.request.args)
    scenario = ScenarioFactory.build_scenario_from_dict(**kwargs)
    ScenarioRepository.save_scenario(scenario)
    return redirect(url_for('scenarios.show_scenarios'))
