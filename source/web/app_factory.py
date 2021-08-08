from enum import Enum

from flask import Flask
from flask_wtf import CSRFProtect

from globalconfig import config


class CustomerErrors(Enum):
    def not_found(self):
        return "Not found", 404

    def not_allowed(self):
        return "Not allowed", 403

    def bad_request(self):
        return "Bad Request", 400


class AppFactory:
    @classmethod
    def create_app(cls):
        """ Flask application factory """

        # Setup Flask and load app.config
        new_app = Flask(__name__)
        new_app.config.update(config.get_flask_config())
        new_app = cls._register_blueprints(new_app)
        # new_app = cls._register_error_handlers(new_app)
        # new_app = cls._register_csrf(new_app)

        new_app.url_map.strict_slashes = False

        return new_app


    @classmethod
    def _register_blueprints(cls, new_app):
        from web.controllers.common.api_blueprint import api_bp
        from web.controllers.game_play.game_blueprint import game_gp
        from web.controllers.common.index_blueprint import index_gp
        from web.controllers.scenario_design.scenario_blueprint import scenario_bp
        from web.controllers.scenario_design.variables_blueprint import variables_bp
        blueprints = [api_bp, game_gp, index_gp, scenario_bp, variables_bp]
        for bp in blueprints:
            new_app.register_blueprint(bp)
        return new_app

    @classmethod
    def _register_error_handlers(cls, new_app):
        errors = {404: CustomerErrors.not_found,
                  400: CustomerErrors.bad_request,
                  403: CustomerErrors.not_allowed,
                  }
        for err_code in errors:
            new_app.register_error_handler(err_code, errors[err_code])
        return new_app

    @classmethod
    def _register_csrf(cls, new_app):
        csrf = CSRFProtect()
        csrf.init_app(new_app)
        return new_app