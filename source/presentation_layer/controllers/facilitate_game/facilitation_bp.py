from flask import Blueprint, render_template, redirect, url_for, flash, request

from application_layer import m2m_transformation
from application_layer.m2m_transformation import SolutionTransformer, InjectTransformer
from domain_layer.common.scenario_management import ScenarioRepository
from domain_layer.gameplay.game_management import GroupGameFactory, GameRepository, GroupGameRepository

facilitation_bp = Blueprint('facilitation', __name__,
                            template_folder='../../templates/facilitation', url_prefix="/trainers")
game_repo = GroupGameRepository

@facilitation_bp.route("/", strict_slashes=False)
def show_scenarios():
    return redirect(url_for("facilitation.show_overview"))


@facilitation_bp.route("/overview")
def show_overview():
    scenarios = ScenarioRepository.get_all_scenarios()
    scenarios = list(scenarios)
    games = game_repo.get_games_by_state()
    games = list(games)
    return render_template("game_overview.html", scenarios=scenarios, games=games)


@facilitation_bp.route("/games/<scenario_id>/open")
def open_game(scenario_id):
    scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
    game = GroupGameFactory.create_game(scenario)
    game_id = game_repo.save_game(game)
    return redirect(url_for("facilitation.show_lobby", game_id=game_id))


@facilitation_bp.route("/games/<game_id>/lobby")
def show_lobby(game_id):
    game = game_repo.get_game_by_id(game_id)
    return render_template("trainer_lobby.html", game=game)


@facilitation_bp.route("/games/<game_id>/start")
def start_game(game_id):
    game = game_repo.get_game_by_id(game_id)
    game.start_game()
    game_repo.save_game(game)
    return redirect(url_for('facilitation.facilitate_game', game_id=game.game_id))


@facilitation_bp.route("/games/<game_id>")
def facilitate_game(game_id):
    game = game_repo.get_game_by_id(game_id)
    if game.is_in_progress:
        return handle_facilitation(game=game)
    if game.is_open:
        return redirect(url_for("facilitation.show_lobby", game_id=game_id))
    else:
        flash("The game is already closed and can not be facilitated any longer", category="failure")
        return redirect(url_for("facilitation.show_overview"))


def handle_facilitation(game):
    next_inject_slug = game.current_inject.next_inject
    next_inject = None
    if next_inject_slug != "":
        next_inject = game.get_inject_by_slug(next_inject_slug)
    chartdata = SolutionTransformer.transform_solution_to_canvasjs(game, game.current_inject)
    return render_template("facilitation_main.html", game=game, next_inject=next_inject,
                           chartdata=chartdata)


@facilitation_bp.route("/games/<game_id>/allownext")
def allow_next(game_id):
    game = game_repo.get_game_by_id(game_id)
    game.allow_next_inject()
    game.advance_story()
    game_repo.save_game(game)
    return redirect(url_for("facilitation.facilitate_game", game_id=game_id))


@facilitation_bp.route("/games/<game_id>/abort")
def abort_game(game_id):
    game = GameRepository.get_game_by_id(game_id)
    game.abort_game()
    GameRepository.save_game(game)
    flash("Aborted Game '{game}'".format(game=game.name), "failure")
    return redirect(url_for("facilitation.show_overview"))


@facilitation_bp.route("/games/<game_id>/variables", methods=["POST"])
def set_variables(game_id):
    game = GameRepository.get_game_by_id(game_id)
    if request.method == "POST":
        var_changes = request.form
        request_args = request
        for var in var_changes:
            try:
                game.set_game_variable(var, var_changes[var])
                GameRepository.save_game(game)
                flash("Changed value successfully!", "success")
            except ValueError as ve:
                flash(str(ve), "failure")
            except TypeError as te:
                flash(str(te), "failure")
        return redirect(url_for("facilitation.facilitate_game", game_id=game_id))
    else:
        print("error")

