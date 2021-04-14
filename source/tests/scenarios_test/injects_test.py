import unittest
import networkx as nx

from domain.scenario_design.injects import Inject
from domain.scenario_design.scenario import Story
from domain.scenario_design.injects import Transition


class GraphTest(unittest.TestCase):


    def test_networkx(self):
        inject = Inject(title="one", text="two")
        inject2 = Inject(title="two", text="three")
        inject3 = Inject(title="three", text="some text, yippie yay!")
        transition = Transition(label="transition!", from_inject=inject, to_inject=inject2)
        transition2 = Transition(label="Continue", from_inject=inject, to_inject=inject3)
        story = Story(title="story", entry_node=inject, story_id=1,
                      injects=[inject2, inject, inject3], transitions=[transition, transition2])
        story.add_inject(inject)
        story.add_inject(Inject(title="another inject", text="some text!"))
        print(story._injects)
        transitions = story.get_transitions_by_inject(inject)
        print(transitions)

