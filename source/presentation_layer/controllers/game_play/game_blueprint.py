from flask import Blueprint, render_template, redirect, url_for, request, flash

from domain_layer.gameplay.game_management import GameRepository, GroupGameRepository
from domain_layer.gameplay.mock_interface import MockGameProvider

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


@game_gp.route("/<game_id>/reflection")
def game_reflection(game_id):
    game = game_repo.get_game_by_id(game_id)
    template_name = "game_reflection.html"
    game.end_game()
    game_repo.save_game(game)
    return render_template(template_name, game=game)


@game_gp.route("/<game_id>/injects/<inject_slug>/show")
def inject_page(game_id, inject_slug):
    game = game_repo.get_game_by_id(game_id)
    inject = game.get_inject_by_slug(inject_slug=inject_slug)
    template_name = "choice_inject.html"
    return render_template(template_name, inject=inject, game=game)


@game_gp.route("/<game_id>/injects/<inject_slug>/solution")
def solve_inject(game_id, inject_slug):
    game = game_repo.get_game_by_id(game_id)
    solution = request.args.get("solution", 0)
    game.solve_inject(participant_id="placeholder", inject_slug=inject_slug, solution=solution)
    if game.is_next_inject_allowed():
        next_inject = game.advance_story()
        game_repo.save_game(game)
        if next_inject:
            return redirect(url_for('games.group_game', game_id=game.game_id))
        else:
            return game_end(game_id)
    else:
        return inject_feedback(game)


def inject_feedback(game):
    template_name = "feedback_statistics.html"
    return render_template(template_name, game=game)


@game_gp.route("/<game_id>/")
def group_game(game_id):
    game = game_repo.get_game_by_id(game_id)
    if game.is_open:
        template_name = "participant_lobby.html"
    elif game.is_in_progress:
        return play_game(game)
    elif game.is_closed:
        flash("This game is now closed!")
        template_name = "game_end.html"
    else:
        flash("There was an error of some sort!", "failure")
        return redirect(url_for('games.multiplayer_overview'))
    return render_template(template_name, game_id=game_id, game=game)


def play_game(game):
    return render_template('choice_inject.html', game=game, inject=game.current_inject)


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