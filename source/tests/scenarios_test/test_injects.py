from unittest import TestCase
from domain.scenario_design.injects import Inject
import domain.scenario_design.auxiliary as aux


class InjectsTest(TestCase):

    def test_create_inject_simple_forward_reference(self):
        inject_1 = Inject(label="test inject", text="inject text")
        inject_1.update_forward_refs()

        inject_2 = Inject(label="second inject", text="inject text", next_inject=inject_1)
        inject_2.update_forward_refs()
        print(inject_2)
        self.assertIsInstance(inject_2, Inject)

    def test_create_inject_no_forward_reference(self):
        inject_1 = Inject(label="test inject", text="inject text")
        inject_1.update_forward_refs()
        print(inject_1)
        self.assertIsInstance(inject_1, Inject)
