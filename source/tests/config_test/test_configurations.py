from unittest import TestCase
from globalconfig import config


class ConfigurationTest(TestCase):

    def test_global_config(self):
        pass

    def test_global_config_env(self):
        config.set_env("TEST")
        db_config = config.get_db_config()
        print(db_config)
        self.assertEqual(db_config.DB_NAME, "csep-test")
