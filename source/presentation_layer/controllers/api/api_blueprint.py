
import flask
from flask import Blueprint, jsonify

from application_layer.m2m_transformation import ScenarioTransformer, InjectTransformer, SolutionTransformer
from domain_layer.gameplay.game_management import GameRepository, GroupGameRepository
from domain_layer.scenariodesign.scenario_management import EditableScenarioRepository, EditableScenarioFactory
from domain_layer.scenariodesign.scenarios import EditableStory
from presentation_layer.controllers.scenario_design import auxiliary as aux

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
    scenario = aux.get_single_scenario(scenario_id)
    return jsonify(scenario.dict())


@api_bp.route("/scenarios/<scenario_id>/<path:details>", methods=["GET"])
def get_scenario_details(scenario_id, details):
    details = details.split("/")
    scenario_dict = aux.get_entity_details(scenario_id=scenario_id, details_path=details)
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
    scenario.stories[story_id] = EditableStory(**story_data)
    scenario = EditableScenarioRepository.save_scenario(scenario)
    return jsonify(scenario.dict())


@api_bp.route("/transformation/<scenario_id>/injects", methods=["GET"])
def get_transformed_injects(scenario_id):
    scenario = EditableScenarioRepository.get_scenario_by_id(scenario_id)
    injects = scenario.get_all_injects()
    nodes, edges = InjectTransformer.transform_injects_to_visjs_dict(injects)
    return jsonify({"nodes": nodes, "edges": edges})


@api_bp.route("/scenarios/<scenario_id>/<path:details>", methods=["DELETE"])
def delete_scenario_element(scenario_id, details):
    details = details.split("/")
    scenario_dict = aux.get_entity_details(scenario_id=scenario_id, details=details)


@api_bp.route("/games/<game_id>", methods=["GET"])
def get_game(game_id):
    game = GroupGameRepository.get_game_by_id(game_id)
    game_dict = game.dict()
    return jsonify(game_dict)


@api_bp.route("/games/<game_id>/<path:details>", methods=["GET"])
def get_game_details(game_id, details):
    details = details.split("/")
    game = GameRepository.get_game_by_id(game_id)
    game_dict = aux.get_entity_details(entity=game, details_path=details)
    return jsonify(game_dict)


@api_bp.route("games/<game_id>/solutions")
def solution_stats(game_id):
    game = GroupGameRepository.get_game_by_id(game_id)
    chartdata = SolutionTransformer.transform_solution_to_canvasjs(game, game.current_inject)
    return jsonify(chartdata)
