from typing import List

from domain_layer.common.scenario_management import ScenarioRepository
from domain_layer.common.scenarios import BaseScenario
from domain_layer.gameplay.games import GroupGame, Game, GameState, GameScenario
from infrastructure_layer.repository import Repository


class GameFactory:
    """Creates instances of Games."""
    @classmethod
    def create_game(cls, scenario: BaseScenario):
        """Create a new game to play an existing scenario.
        :param scenario: the scenario to be played.
        :returns: a new Game for this scenario."""
        scenario = GameScenario(**scenario.dict())
        game = Game(scenario=scenario)
        return game

    @classmethod
    def build_from_dict(cls, scenario: BaseScenario, **game_dict):
        """Re-create a game from a dictionary.
        :param scenario: The scenario which is being played.
        :param game_dict: a collection of keywords that describe the game so far.
        :returns: the Game."""
        if isinstance(scenario, BaseScenario):
            scenario = scenario.dict()
        scenario = GameScenario(**scenario)
        game = Game(scenario=scenario, **game_dict)
        return game


class GroupGameFactory(GameFactory):
    """Creates instances of GroupGames."""
    @classmethod
    def build_from_dict(cls, scenario: BaseScenario, **game_dict):
        """Re-create a GroupGame from a dictionary.
        :param scenario: The scenario which is being played.
        :param game_dict: a collection of keywords that describe the game so far.
        :returns: the GroupGame."""
        if isinstance(scenario, BaseScenario):
            scenario = scenario.dict()
        scenario = GameScenario(**scenario)
        game = GroupGame(scenario=scenario, **game_dict)
        return game

    @classmethod
    def create_game(cls, scenario: BaseScenario):
        """Create a new GroupGame to play an existing scenario.
        :param scenario: the scenario to be played.
        :returns: a new GroupGame for this scenario."""
        if isinstance(scenario, BaseScenario):
            scenario = scenario.dict()
        scenario = GameScenario(**scenario)
        return GroupGame(scenario)


class GameRepository(Repository):
    """Provides methods for accessing and persisting games."""
    collection_name = "games"

    @classmethod
    def get_factory(cls):
        return GameFactory()

    @classmethod
    def save_game(cls, game: Game):
        """Persist a given game."""
        if not game.game_id or game.game_id == "new":
            game_id = cls._insert_entity(game.dict())
        else:
            game_id = cls._update_entity(game.dict(), game.game_id)
        return game_id

    @classmethod
    def get_game_by_id(cls, game_id: str):
        """Retrieve a game.
        :param game_id: The known id of the game."""
        game_id, game_dict = cls._get_entity_by_id(entity_id=game_id)
        scenario_id = game_dict.pop("scenario_id")
        scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
        game_dict["scenario"] = scenario.dict()
        game_dict["game_id"] = game_id
        game = cls.get_factory().build_from_dict(**game_dict)
        return game

    @classmethod
    def get_games_by_state(cls, states=None):
        """Yield an iterator over all open games.
        :param states: a list of GameState objects or one of ["open", "closed", "in_progress"]
        """
        if not states:
            states = [GameState.Open, GameState.In_Progress]
        if isinstance(states[0], GameState):
            states = [state.value for state in states]
        resultset = cls.get_many_by_criteria(criteria={"game_state": {"$in": states}})
        factory = cls.get_factory()
        for game_dict in resultset:
            game_id = str(game_dict.pop("_id"))
            scenario_id = game_dict.pop("scenario_id")
            try:
                scenario = ScenarioRepository.get_scenario_by_id(scenario_id)
                game_dict["game_id"] = game_id
                game = factory.build_from_dict(scenario=scenario, **game_dict)
                yield game
            except ValueError as ve:
                print("VALUE ERROR!")
                print(ve)
                pass


class GroupGameRepository(GameRepository):
    """Provides methods for accessing and persising GroupGames."""
    @classmethod
    def get_factory(cls):
        return GroupGameFactory()
