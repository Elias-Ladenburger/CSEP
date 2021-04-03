from time import time

from domain.scenario_design.scenario import Scenario, Story


class Game:
    """A scenario that is currently being played or has been played."""
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.start_time = time()

