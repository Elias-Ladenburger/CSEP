from flask import Blueprint, render_template, redirect, url_for, request

from domain.game_play.mock_interface import MockGameProvider
from domain.scenario_design.injects import InjectType

game_provider = MockGameProvider()
game = game_provider.get_branching_game()

game_gp = Blueprint('games', __name__,
                        template_folder='templates/game', url_prefix="/games")


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
                           game_id=game_id, inject_id=first_inject.id)


@game_gp.route("/<game_id>/injects/<inject_id>/stats")
def stats_page(game_id, inject_id):
    template_name = "stats_page.html"
    return render_template(template_name, scenario_name=game.name, game_id=game_id,
                           inject_id=inject_id, game_variables=game.get_visible_vars())


@game_gp.route("/<game_id>/end")
def game_end(game_id):
    template_name = "game_end.html"
    return render_template(template_name, scenario_name=game.name, game_id=game_id)


@game_gp.route("/<game_id>/reflection")
def game_reflection(game_id: int):
    template_name = "game_reflection.html"
    game.end_game()
    return render_template(template_name, scenario_name=game.name, game_id=game_id)


@game_gp.route("/<game_id>/injects/<inject_id>/show")
def inject_page(game_id: int, inject_id: int):
    inject = game.get_inject_by_slug(inject_id=int(inject_id))
    if inject.type == InjectType.SIMPLE:
        transitions = []
    else:
        transitions = inject.transitions
    if not transitions or len(transitions) < 2:
        template_name = "informative_inject.html"
    else:
        template_name = "choice_inject.html"
    return render_template(template_name, scenario_name=game.name, game_id=game_id,
                           inject=inject, transitions=transitions)


@game_gp.route("/<game_id>/injects/<inject_id>/solution")
def solution_page(game_id: int, inject_id: int):
    solution = request.args.get("solution", 0)
    next_inject = game.solve_inject(inject=inject_id, solution=int(solution))
    if next_inject:
        return inject_feedback(game_id=game_id, inject_id=next_inject.id)
    else:
        return game_end(game_id)


@game_gp.route("/<game_id>/injects/<inject_id>/feedback")
def inject_feedback(game_id: int, inject_id: int):
    template_name = "feedback_statistics.html"
    return render_template(template_name, scenario_name=game.name,  game_id=game_id,
                           next_inject_id=inject_id)


@game_gp.route("/<game_id>/injects/<inject_id>/feedback_wordcloud")
def inject_wordcloud(game_id: int, inject_id: int):
    template_name = "feedback_wordcloud.html"
    return render_template(template_name, scenario_name="Going Phishing",  game_id=game_id,
                           next_inject_id=inject_id)
