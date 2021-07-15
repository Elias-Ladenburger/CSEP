import flask
from _cffi_backend import typeof
from flask import Blueprint, render_template, redirect, url_for

from domain.scenario_design.scenario_management import ScenarioRepository, ScenarioFactory

scenario_bp = Blueprint('scenarios', __name__,
                        template_folder='templates/scenario', url_prefix="/scenarios")


@scenario_bp.route("/")
def show_scenarios():
    scenarios = ScenarioRepository.get_all_scenarios()
    scenarios = list(scenarios)
    return render_template("scenarios_overview.html", scenarios=scenarios)


@scenario_bp.route("/<scenario_id>/edit")
def edit_scenario(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_edit.html", scenario=scenario)


@scenario_bp.route("/<scenario_id>/stories")
def view_stories(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_view_stories.html", scenario=scenario)


@scenario_bp.route("/<scenario_id>/stories/<story_id>")
def edit_story(scenario_id, story_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    if story_id.isnumeric():
        story_id = int(story_id)
    story = scenario.stories[story_id]
    return render_template("scenario_edit_story.html", scenario=scenario, story=story)


@scenario_bp.route("/<scenario_id>/variables")
def edit_variables(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_edit_variables.html", scenario=scenario)


@scenario_bp.route("/<scenario_id>/stories/<story_id>/injects/<inject_slug>")
def edit_inject(scenario_id, story_id, inject_slug):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    scenario.get_inject_by_slug(inject_slug=inject_slug)
    return render_template("scenario_edit_inject.html", scenario=scenario)


@scenario_bp.route("/<scenario_id>/stats")
def show_stats(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_stats.html", scenarios=[scenario])


@scenario_bp.route("/new")
def new_scenario():
    scenario = ScenarioFactory.create_scenario()
    return render_template("scenario_edit.html", scenario=scenario)


@scenario_bp.route("/save", methods=["POST"])
def save_scenario(**kwargs):
    kwargs.update(flask.request.values)
    scenario = ScenarioFactory.build_scenario_from_dict(**kwargs)
    ScenarioRepository.save_scenario(scenario)
    return redirect(url_for('scenarios.show_scenarios'))


@scenario_bp.route("/delete", methods=["DELETE"])
def delete_scenario():
    scenario_id = flask.request.args.get("scenario_id", None)
    if scenario_id:
        ScenarioRepository.delete_by_id(scenario_id)
    return redirect(url_for('scenarios.show_scenarios'))
