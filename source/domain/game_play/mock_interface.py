

from domain.game_play.game_content import Game
from domain.scenario_design.auxiliary import DataType
from domain.scenario_design.injects import PlainInject, Transition, Inject
from domain.scenario_design.scenario import Scenario, Story, ScenarioVariable


class MockGameProvider:
    """A scenario that is currently being played or has been played."""
    def __init__(self):
        scenario = Scenario(title="Going Phishing",
                            description="""A scenario where you capture credentials by phishing.
                            You play a notorious cybercriminal, who seeks financial gain by stealing the credentials off of high-ranking executives.""")

        MockGameProvider._add_variables(scenario)
        MockGameProvider._build_chapter_1(scenario)
        MockGameProvider._build_chapter_2(scenario)

        self.game = Game(scenario)

    @staticmethod
    def _add_variables(scenario):
        scenario.add_variable(ScenarioVariable(name="Budget", datatype=DataType.NUMBER, private=False),
                              starting_value=100000)
        scenario.add_variable(
            ScenarioVariable(name="Financial Loss", datatype=DataType.NUMBER, private=False),
            starting_value=0)
        scenario.add_variable(ScenarioVariable(name="Reputation Damage", datatype=DataType.TEXT, private=False),
                              starting_value="None")
        scenario.add_variable(ScenarioVariable(name="Internal Variable", datatype=DataType.BOOL, private=True),
                              starting_value=False)
        return scenario

    @staticmethod
    def _build_chapter_1(scenario):
        intro_inject = Inject(title="Introduction",
                              text="Hello Player! In this scenario you will indulge in your dark side: "
                                   "playing through the eyes of an expert social engineer. "
                                   "Your first target is Jaffa Bezous, "
                                   "the Chief Operating Officer of a global bookstore."
                                   "What will your preparation look like?")

        second_inject = Inject(title="Second Inject",
                                text="Interesting choice... "
                                     "let's see, if your preparation pays off. How will you proceed?")

        first_to_second = Transition(from_inject=intro_inject, to_inject=second_inject,
                                     label="Research on Social Media")

        other_first_second = Transition(from_inject=intro_inject, to_inject=second_inject, label="Do nothing")

        intro_inject.transitions = [first_to_second, other_first_second]

        introduction = Story(title="Introduction", entry_node=intro_inject,
                             injects=[intro_inject, second_inject])

        scenario.add_story(introduction)
        return scenario

    @staticmethod
    def _build_chapter_2(scenario):
        second_last_inject = Inject(title="Almost Done", text="Well done, you are almost there!")
        last_inject = Inject(title="Finish", text="You have completed the scenario!")

        final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject,
                                      label="Walk straight ahead")
        other_final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject, label="Turn left")

        final_chapter = Story(title="final chapter", entry_node=second_last_inject,
                              injects=[second_last_inject, last_inject],
                              transitions=[final_transition, other_final_transition]
                              )

        second_last_inject.transitions = [final_transition, other_final_transition]

        scenario.add_story(final_chapter)
        return scenario

    def get_game(self):
        return self.game
