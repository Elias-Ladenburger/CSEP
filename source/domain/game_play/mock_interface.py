from domain.game_play.game import Game, GameFactory
from domain.scenario_design.auxiliary import DataType, TransitionCondition
from domain.scenario_design.injects import Choice, Inject
from domain.scenario_design.scenario import Scenario, Story, ScenarioVariable
from domain.scenario_design.scenario_management import ScenarioFactory


class MockScenarioBuilder:
    @classmethod
    def build_scenario(cls):
        scenario = ScenarioFactory.create_scenario(title="Going Phishing",
                                                   description="A scenario where you capture credentials by phishing. \n"
                                                               "You play a notorious cybercriminal, who seeks "
                                                               "financial gain by stealing the credentials off of "
                                                               "high-ranking executives.")

        cls._add_variables(scenario)
        cls._build_chapter_1(scenario)
        cls._build_chapter_2(scenario)

        return scenario

    @classmethod
    def _add_variables(cls, scenario):
        variables = [(ScenarioVariable(name="Budget", datatype=DataType.NUMBER, private=False), 10000),
                     (ScenarioVariable(name="Financial Loss", datatype=DataType.NUMBER, private=False), 0),
                     (ScenarioVariable(name="Reputation Damage", datatype=DataType.TEXT, private=False), "None"),
                     (ScenarioVariable(name="Internal Variable", datatype=DataType.BOOL, private=True), False)
                     ]

        for var, starting_value in variables:
            scenario.add_variable(var, starting_value=starting_value)
        return scenario

    @classmethod
    def _build_chapter_1(cls, scenario):
        intro_inject = Inject(label="Introduction",
                              text="Hello Player! In this scenario you will indulge in your dark side: "
                                   "playing through the eyes of an expert social engineer. "
                                   "Your first target is Jaffa Bezous, "
                                   "the Chief Operating Officer of a global bookstore."
                                   "What will your preparation look like?")

        second_inject = Inject(label="Second Inject",
                               text="Interesting choice... "
                                    "let's see, if your preparation pays off. How will you proceed?")

        other_first_second = Choice(from_inject=intro_inject, to_inject=second_inject, label="Do nothing")

        introduction = Story(title="Introduction", entry_node=intro_inject)
        introduction.add_injects([intro_inject, second_inject])
        introduction.add_transition(other_first_second)

        scenario.add_story(introduction)
        return scenario

    @classmethod
    def _build_chapter_2(cls, scenario):
        second_last_inject = Inject(label="Almost Done", text="Well done, you are almost there!")
        last_inject = Inject(label="Finish", text="You have completed the test scenario!")

        final_transition = Choice(from_inject=second_last_inject, to_inject=last_inject,
                                  label="Walk straight ahead")

        final_chapter = Story(title="final chapter", entry_node=second_last_inject)

        final_chapter.add_injects(injects=[second_last_inject, last_inject])
        final_chapter.add_transition(final_transition)

        scenario.add_story(final_chapter)
        return scenario


class BranchingScenarioBuilder(MockScenarioBuilder):
    @classmethod
    def _build_chapter_1(cls, scenario: Scenario):
        scenario = MockScenarioBuilder._build_chapter_1(scenario)
        story = scenario.stories[0]
        return BranchingScenarioBuilder._insert_transition(scenario, story, "Research on Social Media")

    @classmethod
    def _build_chapter_2(cls, scenario: Scenario):
        scenario = MockScenarioBuilder._build_chapter_2(scenario)
        story = scenario.stories[1]
        return BranchingScenarioBuilder._insert_transition(scenario, story, "Turn left")

    @staticmethod
    def _insert_transition(scenario: Scenario, story: Story, transition_label: str):
        inject_0 = story.entry_node
        inject_1 = story.transitions[inject_0.slug][0].to_inject
        new_inject = Inject(label="A different inject", text="Turns out that branching scenarios work now...")

        budget_var = scenario.variables["Budget"]
        condition = TransitionCondition(budget_var, comparison_operator="=",
                                        variable_threshold=100000, alternative_inject=new_inject)
        new_transition = Choice(from_inject=inject_0, to_inject=inject_1,
                                label=transition_label, condition=condition)

        story.add_inject(new_inject)
        story.add_transition(new_transition)
        return scenario


class VariableScenarioBuilder(MockScenarioBuilder):
    pass


class MockGameProvider:
    """A scenario_design that is currently being played or has been played."""

    @staticmethod
    def get_simple_game():
        scenario = MockScenarioBuilder.build_scenario()
        game = GameFactory.create_singleplayer_game(scenario)
        return game

    @staticmethod
    def get_branching_game():
        scenario = BranchingScenarioBuilder.build_scenario()
        game = GameFactory.create_singleplayer_game(scenario)
        return game

    @staticmethod
    def get_variable_game():
        scenario = VariableScenarioBuilder.build_scenario()
        return Game(scenario)
