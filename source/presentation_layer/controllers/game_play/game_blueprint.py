from flask import Blueprint, render_template, redirect, url_for, request

from domain_layer.game_play.mock_interface import MockGameProvider

game_provider = MockGameProvider()
game = game_provider.get_branching_game()

game_gp = Blueprint('games', __name__,
                        template_folder='../../templates/game', url_prefix="/games")


@game_gp.route("/")
def find_game():
    game_id = request.args.get("game_id", -1)
    if game_id:
        if int(game_id) > 0:
            return redirect(url_for('games.game_start', game_id=game_id))
    return games_page()


@game_gp.route("/singleplayer/overview")
def games_page():
    return redirect(url_for('index.index'))


@game_gp.route("/multiplayer/overview")
def multiplayer_overview():
    return render_template("group_overview.html")


@game_gp.route("/<game_id>")
def game_start(game_id):
    template_name = "game_start.html"
    first_inject = game.start_game()
    return render_template(template_name, scenario=game.scenario, scenario_name=game.name,
                           game_id=game_id, inject_slug=first_inject.slug)


@game_gp.route("/<game_id>/injects/<inject_slug>/stats")
def stats_page(game_id, inject_slug):
    template_name = "stats_page.html"
    return render_template(template_name, scenario_name=game.name, game_id=game_id,
                           inject_slug=inject_slug, game_variables=game.get_visible_vars())


@game_gp.route("/<game_id>/end")
def game_end(game_id):
    template_name = "game_end.html"
    return render_template(template_name, scenario_name=game.name, game_id=game_id)


@game_gp.route("/<game_id>/reflection")
def game_reflection(game_id):
    template_name = "game_reflection.html"
    game.end_game()
    return render_template(template_name, scenario_name=game.name, game_id=game_id)


@game_gp.route("/<game_id>/injects/<inject_slug>/show")
def inject_page(game_id, inject_slug):
    inject = game.get_inject_by_slug(inject_slug=inject_slug)
    if inject.has_choices:
        template_name = "choice_inject.html"
    else:
        template_name = "informative_inject.html"
    return render_template(template_name, scenario_name=game.name, game_id=game_id,
                           inject=inject)


@game_gp.route("/<game_id>/injects/<inject_slug>/solution")
def solution_page(game_id, inject_slug):
    solution = request.args.get("solution", 0)
    next_inject = game.solve_inject(inject_candidate=inject_slug, solution=solution)
    if next_inject:
        return inject_feedback(game_id=game_id, inject_slug=next_inject.slug)
    else:
        return game_end(game_id)


@game_gp.route("/<game_id>/injects/<inject_slug>/feedback")
def inject_feedback(game_id, inject_slug):
    template_name = "feedback_statistics.html"
    return render_template(template_name, scenario_name=game.name,  game_id=game_id,
                           next_inject_slug=inject_slug)

