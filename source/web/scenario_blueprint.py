from flask import Blueprint, render_template

from domain.scenario_design.scenario_management import ScenarioRepository

scenario_bp = Blueprint('scenarios', __name__,
                        template_folder='templates/scenario', url_prefix="/scenarios")


@scenario_bp.route("/")
def show_scenarios():
    scenarios = ScenarioRepository.get_all_scenarios()
    return render_template("scenarios_overview.html", scenarios=scenarios)


@scenario_bp.route("/<scenario_id>")
def edit_scenario(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id=scenario_id)
    return render_template("scenarios_overview.html", scenarios=[scenario])