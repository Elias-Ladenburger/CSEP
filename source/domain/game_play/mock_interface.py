

from domain.game_play.game_content import Game
from domain.scenario_design.injects import Inject, Transition, InformativeInject
from domain.scenario_design.scenario import Scenario, Story, ScenarioVariable, DataType


class MockGameProvider:
    """A scenario that is currently being played or has been played."""
    def __init__(self):
        scenario = Scenario(title="Going Phishing", description="A scenario where you capture credentials by phishing.")

        intro_inject = Inject(title="Introduction", text="Welcome to the story!")
        second_inject = Inject(title="Second Inject", text="This is the second inject")

        introduction = Story(title="Introduction", entry_node=intro_inject,
                             injects=[intro_inject, second_inject])

        scenario.add_variable(ScenarioVariable(name="Budget", datatype=DataType.NUMBER, hidden=False),
                              starting_value=100000)
        scenario.add_variable(
            ScenarioVariable(name="Financial Loss", datatype=DataType.NUMBER, hidden=False),
            starting_value=0)
        scenario.add_variable(ScenarioVariable(name="Reputation Damage", datatype=DataType.TEXT, hidden=False),
                              starting_value="None")
        scenario.add_variable(ScenarioVariable(name="Internal Variable", datatype=DataType.BOOL, hidden=True),
                              starting_value=False)

        second_last_inject = Inject(title="Almost Done", text="Well done, you are almost there!")
        last_inject = Inject(title="Finish", text="You have completed the scenario!")

        final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject,
                                      label="Walk straight ahead")
        other_final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject, label="Turn left")
        first_to_second = Transition(from_inject=intro_inject, to_inject=second_inject, label="Talk to the mayor")
        second_to_last = Transition(from_inject=second_inject, to_inject=second_last_inject, label="Do nothing")
        other_first_second = Transition(from_inject=intro_inject, to_inject=second_inject, label="Do nothing")
        other_second_third = Transition(from_inject=second_inject, to_inject=second_last_inject, label="Work stuff out")
        introduction.add_transitions([first_to_second, second_to_last, other_first_second, other_second_third])

        final_chapter = Story(title="final chapter", entry_node=second_last_inject,
                              injects=[second_last_inject, last_inject],
                              transitions=[final_transition, other_final_transition]
                              )

        scenario.add_story(introduction)
        scenario.add_story(final_chapter)
        self.game = Game(scenario)

    def get_game(self):
        return self.game
