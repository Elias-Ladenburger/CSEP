
from domain.scenario_design.game import Game
from domain.scenario_design.auxiliary import DataType, TransitionCondition
from domain.scenario_design.injects import Transition, Inject, ConditionalTransition
from domain.scenario_design.scenario import Scenario, Story, ScenarioVariable


class MockScenarioBuilder:
    @classmethod
    def build_game(cls):
        scenario = Scenario(title="Going Phishing",
                                   description="""A scenario_design where you capture credentials by phishing.
                                        You play a notorious cybercriminal, who seeks financial gain by 
                                        stealing the credentials off of high-ranking executives.""")

        cls._add_variables(scenario)
        cls._build_chapter_1(scenario)
        cls._build_chapter_2(scenario)

        return scenario

    @classmethod
    def _add_variables(cls, scenario):
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

    @classmethod
    def _build_chapter_1(cls, scenario):
        intro_inject = Inject(title="Introduction",
                              text="Hello Player! In this scenario_design you will indulge in your dark side: "
                                   "playing through the eyes of an expert social engineer. "
                                   "Your first target is Jaffa Bezous, "
                                   "the Chief Operating Officer of a global bookstore."
                                   "What will your preparation look like?")

        second_inject = Inject(title="Second Inject",
                               text="Interesting choice... "
                                    "let's see, if your preparation pays off. How will you proceed?")

        other_first_second = Transition(from_inject=intro_inject, to_inject=second_inject, label="Do nothing")

        intro_inject.transitions = [other_first_second]

        introduction = Story(title="Introduction", entry_node=intro_inject,
                             injects=[intro_inject, second_inject])

        scenario.add_story(introduction)
        return scenario

    @classmethod
    def _build_chapter_2(cls, scenario):
        second_last_inject = Inject(title="Almost Done", text="Well done, you are almost there!")
        last_inject = Inject(title="Finish", text="You have completed the scenario_design!")

        final_transition = Transition(from_inject=second_last_inject, to_inject=last_inject,
                                      label="Walk straight ahead")

        final_chapter = Story(title="final chapter", entry_node=second_last_inject,
                              injects=[second_last_inject, last_inject])

        second_last_inject.transitions = [final_transition]

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
        inject_1 = inject_0.transitions[0].to_inject
        new_inject = Inject("A different inject", "Turns out that branching scenarios work now...")

        condition = BranchingScenarioBuilder._create_condition(scenario)
        new_transition = ConditionalTransition(from_inject=inject_0, to_inject=inject_1, label=transition_label,
                                               condition=condition, alternative_inject=new_inject)

        story.add_inject(new_inject)
        story.add_transition(new_transition)
        return scenario

    @staticmethod
    def _create_condition(scenario: Scenario):
        variables = scenario.variables
        random_var = variables[0]
        condition = TransitionCondition(random_var, comparison_operator="=", variable_threshold=100000)
        return condition


class VariableScenarioBuilder(MockScenarioBuilder):
    @staticmethod
    def _build_chapter_1(scenario):
        pass


class MockGameProvider:
    """A scenario_design that is currently being played or has been played."""
    @staticmethod
    def get_simple_game():
        scenario = MockScenarioBuilder.build_game()
        return Game(scenario)

    @staticmethod
    def get_branching_game():
        scenario = BranchingScenarioBuilder.build_game()
        return Game(scenario)

    @staticmethod
    def get_variable_game():
        scenario = VariableScenarioBuilder.build_game()
        return Game(scenario)
