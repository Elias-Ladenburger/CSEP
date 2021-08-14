from typing import List

from domain_layer.common.scenarios import BaseScenario
from domain_layer.gameplay.games import GroupGame, Game, GameState
from infrastructure_layer.repository import Repository


class GameFactory:
    @classmethod
    def create_game(cls, scenario: BaseScenario):
        game = Game(scenario=scenario)
        return game

    @classmethod
    def build_from_dict(cls, game_dict: dict):
        game = Game(**game_dict)
        return game


class GroupGameFactory(GameFactory):
    @classmethod
    def build_from_dict(cls, game_dict: dict):
        game = GroupGame(**game_dict)
        return game

    @classmethod
    def create_game(cls, scenario: BaseScenario):
        return GroupGame(scenario)


class GameRepository(Repository):
    collection_name = "games"

    @classmethod
    def save_game(cls, game: Game):
        game_id = cls._insert_entity(cls.collection_name, game.dict())
        return game_id

    @classmethod
    def get_game_by_id(cls, game_id: str):
        game_id, game_dict = cls._get_entity_by_id(cls.collection_name, entity_id=game_id)
        game = GameFactory.build_from_dict(game_dict)
        return game_id, game

    @classmethod
    def get_games_by_state(cls, states: List[GameState] = None):
        """Yield an iterator over all open games.
        :param states: a list
        """
        if not states:
            states = [GameState.Open, GameState.In_Progress]
        game_dicts = cls.get_many_by_criteria(collection_name=cls.collection_name, criteria={"status": {"$in": states}})
        for game_dict in game_dicts:
            if "_id" in game_dict and "scenario_id" not in game_dict:
                game_dict["scenario_id"] = str(game_dict["_id"])
            factory = cls.get_factory()
            scenario = factory.build_from_dict(**game_dict)
            yield scenario
