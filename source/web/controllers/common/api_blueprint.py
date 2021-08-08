import collections.abc

import flask
from flask import Blueprint, jsonify

from domain.common.scenario_management import ScenarioRepository, ScenarioTransformer
from domain.scenario_design.scenario_management import EditableScenarioRepository, EditableScenarioFactory
from domain.scenario_design.scenarios import Story

api_bp = Blueprint('api', __name__, url_prefix="/api/v0")


@api_bp.route("/scenarios")
def get_scenarios():
    scenarios = EditableScenarioRepository.get_all_scenarios()
    scenarios = ScenarioTransformer.scenarios_as_dict(scenarios)
    return jsonify(scenarios)


@api_bp.route("/scenarioslist")
def get_scenarios_list():
    scenarios = EditableScenarioRepository.get_all_scenarios()
    scenarios = ScenarioTransformer.scenarios_as_json_list(scenarios)
    return jsonify(scenarios)


@api_bp.route("scenarios/<scenario_id>", methods=["GET"])
def get_scenario(scenario_id):
    scenario = _get_single_scenario(scenario_id)
    return jsonify(scenario.dict())


@api_bp.route("/scenarios/<scenario_id>/<path:details>", methods=["GET"])
def get_scenario_details(scenario_id, details):
    details = details.split("/")
    scenario = _get_single_scenario(scenario_id)
    scenario_dict = scenario.dict()
    for detail in details:
        if isinstance(scenario_dict, list) and detail.is_numeric():
            scenario_dict = scenario_dict[int(detail)]
        elif isinstance(scenario_dict, dict) and detail in scenario_dict:
            scenario_dict = scenario_dict[detail]
        else:
            pass
    return jsonify(scenario_dict)


@api_bp.route("/scenarios", methods=["POST"])
def add_scenario():
    raw_form = flask.request.json
    scenario = EditableScenarioFactory.create_scenario(**raw_form)
    scenario = EditableScenarioRepository.save_scenario(scenario)
    return jsonify(scenario.dict())


@api_bp.route("/scenarios/<scenario_id>", methods=["POST"])
def edit_scenario(scenario_id):
    raw_form = flask.request.json
    scenario = EditableScenarioFactory.build_from_dict(**raw_form)
    scenario = EditableScenarioRepository.save_scenario(scenario)
    return jsonify(scenario.dict())


@api_bp.route("/scenarios/<scenario_id>/stories/<int:story_id>", methods=["POST"])
def edit_story(scenario_id, story_id):
    story_data = flask.request.json
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id)
    scenario.stories[story_id] = Story(**story_data)
    scenario = EditableScenarioRepository.save_scenario(scenario)
    return jsonify(scenario.dict())


def _get_single_scenario(scenario_id):
    return EditableScenarioRepository.get_scenario_by_id(scenario_id)


