from domain_layer.common.auxiliary import DataType, BaseScenarioVariable
from domain_layer.common.injects import BaseInjectResult
from domain_layer.gameplay.game_management import GameFactory
from domain_layer.gameplay.games import Game
from domain_layer.scenariodesign.injects import EditableInject, InjectChoice, InjectCondition
from domain_layer.scenariodesign.scenarios import EditableScenario, EditableStory
from domain_layer.scenariodesign.scenario_management import EditableScenarioFactory


class MockScenarioBuilder:
    @classmethod
    def build_scenario(cls):
        scenario = EditableScenarioFactory.create_scenario(title="Going Phishing",
                                                   description="A scenario where you capture credentials by phishing. \n"
                                                               "You play a notorious cybercriminal, who seeks "
                                                               "financial gain by stealing the credentials off of "
                                                               "high-ranking executives.")

        cls._add_variables(scenario)
        cls._build_injects(scenario)

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
    def _build_injects(cls, scenario):
        intro_inject = EditableInject(label="Introduction",
                                      text="Hello Player! In this scenario you will indulge in your dark side: "
                                   "playing through the eyes of an expert social engineer. "
                                   "Your first target is Jaffa Bezous, "
                                   "the Chief Operating Officer of a global bookstore."
                                   "What will your preparation look like?")

        second_inject = EditableInject(label="Second Inject",
                                       text="Interesting choice... "
                                    "let's see, if your preparation pays off. How will you proceed?")
        intro_inject.next_inject = second_inject.slug

        other_first_second = InjectChoice(label="Do nothing")
        intro_inject.choices.append(other_first_second)

        last_inject = EditableInject(label="Finish", text="You have completed the test scenario!")
        second_last_inject = EditableInject(label="Almost Done", text="Well done, you are almost there!",
                                            next_inject=last_inject.slug)

        second_inject.next_inject = second_last_inject.slug

        final_transition = InjectChoice(label="Walk straight ahead")
        alternative_transition = InjectChoice(label="Turn Right")
        second_last_inject.add_choices([final_transition, alternative_transition])

        injects = [intro_inject, second_inject, second_last_inject, last_inject]

        introduction = EditableStory(title="Introduction", entry_node=intro_inject.slug, injects=injects)

        scenario.add_story(introduction)
        return scenario


class BranchingScenarioBuilder(MockScenarioBuilder):
    @classmethod
    def _build_injects(cls, scenario: EditableScenario):
        scenario = MockScenarioBuilder._build_injects(scenario)
        story = scenario.stories[0]
        return BranchingScenarioBuilder._insert_transition(scenario, story, "Research on Social Media")

    @staticmethod
    def _insert_transition(scenario: EditableScenario, story: EditableStory, transition_label: str):
        inject_0 = story.entry_node
        inject_1 = story.get_inject_by_slug(inject_0.next_inject)
        new_inject = EditableInject(label="A different inject", text="Turns out that branching scenarios work now...")

        budget_var = scenario.variables["Budget"]
        condition = InjectCondition(budget_var.name, comparison_operator="=",
                                        variable_threshold=100000, alternative_inject=new_inject.slug)
        choice_1 = InjectChoice(label=transition_label,
                                outcome=BaseInjectResult(next_inject=new_inject.slug, variable_changes=[]))

        inject_0.choices.append(choice_1)
        story.add_inject(new_inject)
        return scenario


class VariableScenarioBuilder(MockScenarioBuilder):
    pass


class MockGameProvider:
    """A scenariodesign that is currently being played or has been played."""

    @staticmethod
    def get_simple_game():
        scenario = MockScenarioBuilder.build_scenario()
        game = GameFactory.create_game(scenario)
        return game

    @staticmethod
    def get_branching_game():
        scenario = BranchingScenarioBuilder.build_scenario()
        game = GameFactory.create_game(scenario)
        return game

    @staticmethod
    def get_variable_game():
        scenario = VariableScenarioBuilder.build_scenario()
        return Game(scenario)
