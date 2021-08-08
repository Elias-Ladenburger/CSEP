import flask
from flask import Blueprint, render_template, redirect, flash, url_for

from domain.scenario_design.scenario_management import EditableScenarioRepository, EditableScenarioFactory
from web.controllers.scenario_design.scenario_forms import *

scenario_bp = Blueprint('scenarios', __name__,
                        template_folder='../../templates/scenario', url_prefix="/scenarios")


@scenario_bp.route("/", strict_slashes=False)
def show_scenarios():
    scenarios = EditableScenarioRepository.get_all_scenarios()
    core_form = ScenarioCoreForm()
    scenarios = list(scenarios)
    return render_template("scenarios_overview.html", scenarios=scenarios, core_form=core_form)


@scenario_bp.route("/<scenario_id>/edit", methods=["GET", "POST"])
def edit_scenario(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return edit_scenario_view(scenario=scenario)


@scenario_bp.route("/new")
def new_scenario():
    scenario = EditableScenarioFactory.create_scenario(scenario_id="new")
    core_form = ScenarioCoreForm()
    return render_template("tab_core_info.html", scenario=scenario, core_form=core_form)


def edit_scenario_view(scenario: EditableScenario, **kwargs):
    core_form = ScenarioCoreForm()
    story_form = StoryForm()
    variables_form = ScenarioVariableForm()
    return render_template("scenario_edit.html", scenario=scenario, core_form=core_form,
                           story_form=story_form, variables_form=variables_form, **kwargs)


@scenario_bp.route("/save", methods=["POST"])
def save_scenario(**kwargs):
    raw_form = flask.request.form
    scenario_form = ScenarioCoreForm(raw_form)
    if scenario_form.validate():
        scenario_dict = scenario_form.data

        scenario = EditableScenarioFactory.build_from_dict(**scenario_dict)
        scenario = EditableScenarioRepository.save_scenario(scenario)
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
        EditableScenarioRepository.delete_by_id(scenario_id)
    return show_scenarios()


@scenario_bp.route("/<scenario_id>/stories")
def view_stories(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    form = StoryForm()
    return tab_details("tab_stories.html", scenario=scenario, form=form)


@scenario_bp.route("<scenario_id>/essentials")
def edit_core(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id)
    form = ScenarioCoreForm()
    return tab_details("tab_core_info.html", scenario=scenario, form=form)


@scenario_bp.route("/<scenario_id>/stories/<story_id>")
def edit_story(scenario_id, story_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    if story_id.isnumeric():
        story_id = int(story_id)
    story = scenario.stories[story_id]
    form = StoryForm()
    return tab_details("tab_injects.html", scenario=scenario, form=form, story=story)


@scenario_bp.route("/<scenario_id>/stories", methods=["POST"])
def insert_story(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    story_params = flask.request.form
    story = BaseStory(**story_params)
    story = scenario.add_story(story)
    flash("Successfully added story!")
    return edit_story(scenario_id=scenario_id, story_id=story.story_id)


@scenario_bp.route("/<scenario_id>/stories/<story_id>/injects/<inject_slug>")
def edit_inject(scenario_id, story_id, inject_slug):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    form = InjectForm()
    return tab_details("tab_injects.html", scenario=scenario, form=form)


@scenario_bp.route("/<scenario_id>/stats")
def show_stats(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenario_stats.html", scenarios=[scenario])


def tab_details(template, scenario, form, **kwargs):
    return render_template(template, scenario=scenario, form=form, **kwargs)
