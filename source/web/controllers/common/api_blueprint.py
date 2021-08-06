from flask import Blueprint, jsonify

from domain.common.scenario_management import ScenarioRepository, ScenarioTransformer
from domain.scenario_design.scenario_management import EditableScenarioRepository

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
