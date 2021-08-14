from flask import Blueprint, render_template, redirect, url_for

from domain_layer.common.scenario_management import ScenarioRepository
from domain_layer.gameplay.game_management import GroupGameFactory, GameRepository

facilitation_bp = Blueprint('facilitation', __name__,
                            template_folder='../../templates/game_facilitation', url_prefix="/trainers")


@facilitation_bp.route("/", strict_slashes=False)
def show_scenarios():
    return redirect(url_for("facilitation.show_overview"))


@facilitation_bp.route("/overview")
def show_overview():
    scenarios = ScenarioRepository.get_all_scenarios()
    scenarios = list(scenarios)
    return render_template("game_overview.html", scenarios=scenarios)


@facilitation_bp.route("/games/<scenario_id>/open")
def open_game(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
    game = GroupGameFactory.create_game(scenario)
    game_id = GameRepository.save_game(game)
    return redirect(url_for("facilitation.show_lobby", game_id=game_id))


@facilitation_bp.route("/games/<game_id>/lobby")
def show_lobby(game_id):
    game_id, game = GameRepository.get_game_by_id(game_id)
    return render_template("trainer_lobby.html", game=game)


@facilitation_bp.route("/games/<game_id>/facilitate")
def facilitate_game(game_id):
    game_id, game = GameRepository.get_game_by_id(game_id)
    return render_template("trainer_lobby.html", game=game)
