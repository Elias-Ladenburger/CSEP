from unittest import TestCase

from domain_layer.gameplay.mock_interface import MockScenarioBuilder
from domain_layer.scenariodesign.scenarios import EditableStory


class ScenarioTest(TestCase):
    def setUp(self) -> None:
        self.scenario = MockScenarioBuilder.build_scenario()

    def test_create_story_from_dict(self):
        stories_dict = [{'title': 'Introduction',
                         'entry_node': 'introduction',
                         'injects': {
            'second-inject': {'label': 'Second Inject',
                              'text': "Interesting choice... let's see, if your preparation pays off. "
                                      "How will you proceed?",
                              'slug': 'second-inject',
                              'media_path': '',
                              'choices': [], 'condition': None,
                              'next_inject': ""},
            'introduction': {'label': 'Introduction',
                             'text': 'Hello Player! In this scenario_design you will indulge in your dark side: '
                                     'playing through the eyes of an expert social engineer. Your first target is '
                                     'Jaffa Bezous, the Chief Operating Officer of a global bookstore. '
                                     'What will your preparation look like?',
                             'slug': 'introduction', 'media_path': '',
                             'choices': [{'label': 'Do nothing',
                                          'outcome': {
                                              'next_inject': "",
                                              'variable_changes': []}}],
                             'condition': None,
                             'next_inject': 'Second Inject'},
            'finish': {'label': 'Finish',
                       'text': 'You have completed the test scenario_design!',
                       'slug': 'finish',
                       'media_path': '', 'choices': [],
                       'condition': None, 'next_inject': ""},
            'almost-done': {'label': 'Almost Done',
                            'text': 'Well done, you are almost there!',
                            'slug': 'almost-done',
                            'media_path': '', 'choices': [
                    {'label': 'Walk straight ahead',
                     'outcome': {'next_inject': "",
                                 'variable_changes': []}},
                    {'label': 'Turn Right',
                     'outcome': {'next_inject': "",
                                 'variable_changes': []}}],
                            'condition': None,
                            'next_inject': 'Finish'}}}]

        stories = []
        for story_dict in stories_dict:
            story = EditableStory(**story_dict)
            stories.append(story)
        self.assertIsInstance(stories[0], EditableStory)
