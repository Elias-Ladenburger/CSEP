from typing import List

from domain_layer.common.scenario_management import ScenarioRepository
from domain_layer.common.scenarios import BaseScenario
from domain_layer.gameplay.games import GroupGame, Game, GameState, GameScenario
from infrastructure_layer.repository import Repository


class GameFactory:
    @classmethod
    def create_game(cls, scenario: BaseScenario):
        scenario = GameScenario(**scenario.dict())
        game = Game(scenario=scenario)
        return game

    @classmethod
    def build_from_dict(cls, scenario: BaseScenario, **game_dict):
        if isinstance(scenario, BaseScenario):
            scenario = scenario.dict()
        scenario = GameScenario(**scenario)
        game = Game(scenario=scenario, **game_dict)
        return game


class GroupGameFactory(GameFactory):
    @classmethod
    def build_from_dict(cls, scenario: BaseScenario, **game_dict):
        if isinstance(scenario, BaseScenario):
            scenario = scenario.dict()
        scenario = GameScenario(**scenario)
        game = GroupGame(scenario=scenario, **game_dict)
        return game

    @classmethod
    def create_game(cls, scenario: BaseScenario):
        if isinstance(scenario, BaseScenario):
            scenario = scenario.dict()
        scenario = GameScenario(**scenario)
        return GroupGame(scenario)


class GameRepository(Repository):
    collection_name = "games"

    @classmethod
    def get_factory(cls):
        return GameFactory()

    @classmethod
    def save_game(cls, game: Game):
        if not game.game_id or game.game_id == "new":
            game_id = cls._insert_entity(cls.collection_name, game.dict())
        else:
            game_id = cls._update_entity(cls.collection_name, game.dict(), game.game_id)
        return game_id

    @classmethod
    def get_game_by_id(cls, game_id: str):
        game_id, game_dict = cls._get_entity_by_id(cls.collection_name, entity_id=game_id)
        scenario_id = game_dict.pop("scenario_id")
        scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
        game_dict["scenario"] = scenario.dict()
        game_dict["game_id"] = game_id
        game = GameFactory.build_from_dict(**game_dict)
        return game

    @classmethod
    def get_games_by_state(cls, states: List[GameState] = None):
        """Yield an iterator over all open games.
        :param states: a list of GameState objects or one of ["open", "closed", "in_progress"]
        """
        if not states:
            states = [GameState.Open, GameState.In_Progress]
        states = [state.value for state in states]
        resultset = cls.get_many_by_criteria(collection_name=cls.collection_name,
                                                       criteria={"game_state": {"$in": states}})
        factory = cls.get_factory()
        for game_dict in resultset:
            game_id = str(game_dict.pop("_id"))
            scenario_id = game_dict.pop("scenario_id")
            scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
            game_dict["game_id"] = game_id
            game = factory.build_from_dict(scenario=scenario, **game_dict)
            yield game
