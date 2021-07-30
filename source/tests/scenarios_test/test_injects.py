from unittest import TestCase
from domain.common.injects import BaseChoiceInject


class InjectsTest(TestCase):

    def test_create_inject_simple_forward_reference(self):
        inject_1 = BaseChoiceInject(label="test inject", text="inject text")
        inject_1.update_forward_refs()

        inject_2 = BaseChoiceInject(label="second inject", text="inject text", next_inject=inject_1)
        inject_2.update_forward_refs()
        print(inject_2)
        self.assertIsInstance(inject_2, BaseChoiceInject)

    def test_create_inject_no_forward_reference(self):
        inject_1 = BaseChoiceInject(label="test inject", text="inject text")
        inject_1.update_forward_refs()
        print(inject_1)
        self.assertIsInstance(inject_1, BaseChoiceInject)
