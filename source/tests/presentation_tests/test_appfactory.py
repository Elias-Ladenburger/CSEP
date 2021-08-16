from unittest import TestCase

from flask import Flask

from domain_layer.gameplay.mock_interface import MockScenarioBuilder
from presentation_layer import app_factory

class AppFactoryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_app_factory(self):
        new_app = app_factory.AppFactory.create_app()
        self.assertIsInstance(new_app, Flask)


