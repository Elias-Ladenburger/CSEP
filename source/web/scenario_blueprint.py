import flask
from flask import Blueprint, render_template, redirect, url_for, flash

from domain.scenario_design.scenario import Story, Scenario
from domain.scenario_design.scenario_management import ScenarioRepository, ScenarioFactory
from web.scenario_forms import *
from web.scenario_forms import ScenarioForm

scenario_bp = Blueprint('scenarios', __name__,
                        template_folder='templates/scenario', url_prefix="/scenarios")


@scenario_bp.route("/")
def show_scenarios():
    scenarios = ScenarioRepository.get_all_scenarios()
    scenarios = list(scenarios)
    return render_template("scenarios_overview.html", scenarios=scenarios)


@scenario_bp.route("/<scenario_id>/edit", methods=["GET", "POST"])
def edit_scenario(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return edit_scenario_view(scenario=scenario)


@scenario_bp.route("/new")
def new_scenario():
    scenario = ScenarioFactory.create_scenario()
    return edit_scenario_view(scenario=scenario)


def edit_scenario_view(scenario: Scenario, **kwargs):
    scenario_form = ScenarioForm(scenario)
    return render_template("scenario_edit.html", scenario=scenario, scenario_form=scenario_form, **kwargs)


@scenario_bp.route("/save", methods=["POST"])
def save_scenario(**kwargs):
    raw_form = flask.request.form
    scenario_form = ScenarioForm(raw_form)
    if scenario_form.essentials_form.validate(raw_form):
        scenario_dict = scenario_form.essentials_form.data

        scenario = ScenarioFactory.build_scenario_from_dict(**scenario_dict)
        scenario = ScenarioRepository.save_scenario(scenario)
        flash("Scenario saved successfully!", category="success")
        return redirect(url_for('scenarios.edit_scenario', scenario_id=scenario.scenario_id))
    else:
        flash("Something went wrong!", category="failure")
        redirect(flask.request.referrer)
    return redirect(flask.request.referrer)


@scenario_bp.route("/delete", methods=["DELETE"])
def delete_scenario():
    scenario_id = flask.request.form.get("scenario_id", None)
    if scenario_id:
        ScenarioRepository.delete_by_id(scenario_id)
    return show_scenarios()


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


@scenario_bp.route("/<scenario_id>/stories", methods=["POST"])
def insert_story(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    story_params = flask.request.form
    story = Story(**story_params)
    story = scenario.add_story(story)
    flash("Successfully added story!")
    return edit_story(scenario_id=scenario_id, story_id=story.story_id)


@scenario_bp.route("/<scenario_id>/variables")
def edit_variables(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("variable_view.html", scenario=scenario)


@scenario_bp.route("/<scenario_id>/stories/<story_id>/injects/<inject_slug>")
def edit_inject(scenario_id, story_id, inject_slug):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    scenario.get_inject_by_slug(inject_slug=inject_slug)
    return render_template("scenario_edit_inject.html", scenario=scenario)


@scenario_bp.route("/<scenario_id>/stats")
def show_stats(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_stats.html", scenarios=[scenario])

