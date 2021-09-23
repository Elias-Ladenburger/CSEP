
from flask import Flask
from flask_wtf import CSRFProtect

from globalconfig import config
from flask_bootstrap import Bootstrap


def not_found():
    return "Not found", 404


def not_allowed():
    return "Not allowed", 403


def bad_request():
    return "Bad Request", 400


http_errors = {404: not_found, 403: not_allowed, 400: bad_request}


class AppFactory:
    @classmethod
    def create_app(cls):
        """ Flask application factory """

        # Setup Flask and load app.config
        new_app = Flask(__name__)
        new_app.config.update(config.get_flask_config())
        new_app = cls._register_blueprints(new_app)

        new_app.url_map.strict_slashes = False
        Bootstrap(new_app)

        return new_app

    @classmethod
    def _register_blueprints(cls, new_app):
        from presentation_layer.controllers.api.api_blueprint import api_bp
        from presentation_layer.controllers.game_play.game_blueprint import game_gp
        from presentation_layer.controllers.common.index_blueprint import index_gp
        from presentation_layer.controllers.scenario_design.scenario_blueprint import scenario_bp
        from presentation_layer.controllers.scenario_design.variables_blueprint import variables_bp
        from presentation_layer.controllers.scenario_design.injects_blueprint import injects_bp
        from presentation_layer.controllers.facilitate_game.facilitation_bp import facilitation_bp
        from presentation_layer.controllers.test._test_bp import _test_bp
        blueprints = [api_bp, game_gp, index_gp, scenario_bp,
                      variables_bp, injects_bp, facilitation_bp, _test_bp]
        for bp in blueprints:
            new_app.register_blueprint(bp)
        return new_app

    @classmethod
    def _register_error_handlers(cls, new_app):
        for err_code in http_errors:
            new_app.register_error_handler(err_code, http_errors[err_code])
        return new_app

    @classmethod
    def _register_csrf(cls, new_app):
        csrf = CSRFProtect()
        csrf.init_app(new_app)
        return new_app

