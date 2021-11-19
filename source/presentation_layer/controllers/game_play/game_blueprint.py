import random
import string

from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from application_layer.m2m_transformation import SolutionTransformer
from domain_layer.gameplay.game_management import GroupGameRepository

game_gp = Blueprint('games', __name__,
                        template_folder='../../templates/gameplay', url_prefix="/games")

game_repo = GroupGameRepository


@game_gp.route("/")
def landing_page():
    return redirect(url_for('games.multiplayer_overview'))


@game_gp.route("/find")
def find_game():
    game_id = request.args.get("game_id", -1)
    if game_id:
        game = game_repo.get_game_by_id(game_id)
        if game:
            return redirect(url_for('games.group_game', game_id=game_id))
    flash("This game was not found!", "danger")
    return redirect(url_for('games.multiplayer_overview'))


@game_gp.route("/multiplayer/overview")
def multiplayer_overview():
    games = game_repo.get_games_by_state(["open"])
    return render_template("group_overview.html", games=games)


@game_gp.route("/<game_id>/")
def group_game(game_id):
    game = game_repo.get_game_by_id(game_id)
    participant_hash = get_game_participant(game)
    if game.is_open:
        template_name = "participant_lobby.html"
    elif game.is_in_progress:
        if game.is_next_inject_allowed():
            game.advance()
            game_repo.save_game(game)
        participant_hash = get_game_participant(game)
        return play_game(game, participant_hash)
    elif game.is_closed:
        flash("This game is now closed!")
        template_name = "game_end.html"
    else:
        flash("There was an error of some sort!", "failure")
        return redirect(url_for('games.multiplayer_overview'))
    return render_template(template_name, game_id=game_id, game=game)


def play_game(game, participant_hash):
    current_inject = game.current_inject
    if game.is_closed:
        return redirect(url_for('games.group_game', game_id=game.game_id))
    if game.has_participant_solved(participant_hash):
        flash("You have already solved this inject. Please wait a few moments until the next inject becomes active.", "success")
        return show_feedback(game)  # redirect(url_for('games.inject_feedback', game_id=game.game_id))
    return render_template('choice_inject.html', game=game, inject=current_inject)


@game_gp.route("/<game_id>/feedback")
def inject_feedback(game_id):
    game = game_repo.get_game_by_id(game_id)
    return show_feedback(game)


def show_feedback(game):
    chartdata = SolutionTransformer.transform_solution_to_canvasjs(game, game.current_inject.slug)
    return render_template("feedback_statistics.html", game=game, inject=game.current_inject, chartdata=chartdata)


@game_gp.route("/<game_id>/reflection")
def game_reflection(game_id):
    game = game_repo.get_game_by_id(game_id)
    template_name = "game_reflection.html"
    game.end_game()
    game_repo.save_game(game)
    return render_template(template_name, game=game)


@game_gp.route("/<game_id>/injects/<inject_slug>/solution")
def solve_inject(game_id, inject_slug):
    game = game_repo.get_game_by_id(game_id)
    solution = request.args.get("solution", 0)
    participant_hash = session.get('participant_hash', False)
    if not participant_hash:
        participant_hash = generate_sid()
        session["participant_hash"] = participant_hash
    game.solve_inject(participant_id=participant_hash, inject_slug=inject_slug, solution=solution)
    game_repo.save_game(game)
    return redirect(url_for('games.inject_feedback', game_id=game.game_id))


@game_gp.route("/<game_id>/injects/<inject_slug>/stats")
def stats_page(game_id, inject_slug):
    game = game_repo.get_game_by_id(game_id)
    template_name = "stats_page.html"
    return render_template(template_name, game=game, inject_slug=inject_slug)


@game_gp.route("/<game_id>/end")
def game_end(game_id):
    game = game_repo.get_game_by_id(game_id)
    template_name = "game_end.html"
    return render_template(template_name, game=game)


def get_game_participant(game):
    if "participant_hash" not in session:
        participant_hash = game.add_participant()
        session["participant_hash"] = participant_hash
    participant_hash = session["participant_hash"]
    return participant_hash

