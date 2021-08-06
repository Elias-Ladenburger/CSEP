from domain.common.auxiliary import DataType, BaseScenarioVariable
from domain.common.injects import InjectResult
from domain.game_play.game import Game, GameFactory
from domain.scenario_design.injects import EditableInject, InjectChoice, InjectCondition
from domain.scenario_design.scenarios import EditableScenario, Story
from domain.scenario_design.scenario_management import EditableScenarioFactory


class MockScenarioBuilder:
    @classmethod
    def build_scenario(cls):
        scenario = EditableScenarioFactory.create_scenario(title="Going Phishing",
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
        variables = [BaseScenarioVariable(name="Budget", datatype=DataType.NUMBER, private=False, value=10000),
                     BaseScenarioVariable(name="Financial Loss", datatype=DataType.NUMBER, private=False, value=0),
                     BaseScenarioVariable(name="Reputation Damage", datatype=DataType.TEXT, private=False, value="None"),
                     BaseScenarioVariable(name="Internal Variable", datatype=DataType.BOOL, private=True, value=False)
                     ]

        for var in variables:
            scenario.add_variable(var)
        return scenario

    @classmethod
    def _build_chapter_1(cls, scenario):
        intro_inject = EditableInject(label="Introduction",
                                      text="Hello Player! In this scenario you will indulge in your dark side: "
                                   "playing through the eyes of an expert social engineer. "
                                   "Your first target is Jaffa Bezous, "
                                   "the Chief Operating Officer of a global bookstore."
                                   "What will your preparation look like?")

        second_inject = EditableInject(label="Second Inject",
                                       text="Interesting choice... "
                                    "let's see, if your preparation pays off. How will you proceed?")
        intro_inject.next_inject = second_inject

        other_first_second = InjectChoice(label="Do nothing")

        intro_inject.choices.append(other_first_second)

        introduction = Story(title="Introduction", entry_node=intro_inject)
        introduction.add_injects([intro_inject, second_inject])

        scenario.add_story(introduction)
        return scenario

    @classmethod
    def _build_chapter_2(cls, scenario):
        last_inject = EditableInject(label="Finish", text="You have completed the test scenario!")
        second_last_inject = EditableInject(label="Almost Done", text="Well done, you are almost there!",
                                            next_inject=last_inject)

        final_transition = InjectChoice(label="Walk straight ahead")
        alternative_transition = InjectChoice(label="Turn Right")
        second_last_inject.add_choices([final_transition, alternative_transition])

        final_chapter = Story(title="final chapter", entry_node=second_last_inject)

        final_chapter.add_injects(injects=[second_last_inject, last_inject])

        scenario.add_story(final_chapter)
        return scenario


class BranchingScenarioBuilder(MockScenarioBuilder):
    @classmethod
    def _build_chapter_1(cls, scenario: EditableScenario):
        scenario = MockScenarioBuilder._build_chapter_1(scenario)
        story = scenario.stories[0]
        return BranchingScenarioBuilder._insert_transition(scenario, story, "Research on Social Media")

    @classmethod
    def _build_chapter_2(cls, scenario: EditableScenario):
        scenario = MockScenarioBuilder._build_chapter_2(scenario)
        story = scenario.stories[1]
        return BranchingScenarioBuilder._insert_transition(scenario, story, "Turn left")

    @staticmethod
    def _insert_transition(scenario: EditableScenario, story: Story, transition_label: str):
        inject_0 = story.entry_node
        inject_1 = story.injects[inject_0.slug].next_inject
        new_inject = EditableInject(label="A different inject", text="Turns out that branching scenarios work now...")

        budget_var = scenario.variables["Budget"]
        condition = InjectCondition(budget_var, comparison_operator="=",
                                        variable_threshold=100000, alternative_inject=new_inject)
        choice_1 = InjectChoice(label=transition_label,
                                    outcome=InjectResult(next_inject=new_inject, variable_changes=[]))

        inject_0.choices.append(choice_1)
        story.add_inject(new_inject)
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
