from domain_layer.game_play.mock_interface import MockScenarioBuilder
from domain_layer.scenario_design.scenario_management import EditableScenarioRepository
from infrastructure_layer.database import CustomDB


def setup_mock_db():
    CustomDB._purge_database(collection_name="scenarios")
    for i in range(0, 3):
        test_scenario = MockScenarioBuilder.build_scenario()
        EditableScenarioRepository.save_scenario(test_scenario)


if __name__ == "__main__":
    setup_mock_db()
