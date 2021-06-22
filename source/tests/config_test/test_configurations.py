from unittest import TestCase
from globalconfig import config


class ConfigurationTest(TestCase):
    """
    TODO: apparently, setting up different configurations that are not strongly coupled yet
    universally accessible is non-trivial. Will develop if time.
    """

    def test_global_config(self):
        pass

    def test_global_config_env(self):
        config.set_env("TEST")
        db_config = config.get_db_config()
        print(db_config)
        self.assertEquals(db_config.DB_NAME, "csep-test")
