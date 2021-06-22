import os
import yaml
import munch


def _load_config_dict():
    _dir_path = os.path.dirname(os.path.realpath(__file__))
    _conf_path = os.path.join(_dir_path, 'config.yml')

    with open(_conf_path, "r") as config_stream:
        _config = yaml.safe_load(config_stream)
        _config_dict = munch.munchify(_config)  # allows accessing the more concise: dict.KEY
    return _config_dict


class _Config:
    _config_dict = _load_config_dict()
    _env = "DEV"

    @classmethod
    def get_flask_config(cls):
        return cls._config_dict.FLASK

    @classmethod
    def get_db_config(cls):
        return cls._config_dict.DATABASE[cls._env]

    @classmethod
    def set_env(cls, new_env: str):
        cls._env = new_env


config = _Config()
