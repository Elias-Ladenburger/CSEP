import flask
from _cffi_backend import typeof
from flask import Blueprint, render_template, redirect, url_for, jsonify

from domain.scenario_design.scenario_management import ScenarioRepository, ScenarioFactory, ScenarioTransformer

api_bp = Blueprint('api', __name__, url_prefix="/api/v0")


@api_bp.route("/scenarios")
def get_scenarios():
    scenarios = ScenarioRepository.get_all_scenarios()
    scenarios = ScenarioTransformer.scenarios_as_dict(scenarios)
    return scenarios


