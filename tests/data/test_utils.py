from src.data.utils import get_project_root, load_config
import pytest
import yaml
import os
import pathlib


class TestGetProjectRoot:
    def test_on_repo_name(self):
        repo_name = "rooms-for-rent-in-malaysia"
        length_repo_name = len(repo_name)
        assert f"{get_project_root()}"[-length_repo_name:] == repo_name
        assert isinstance(get_project_root(), pathlib.PosixPath)


@pytest.fixture
def parameters_configuration_file():
    conf_file = "test_params_conf.yaml"
    conf_path = f"{get_project_root().joinpath('conf', 'parameters', conf_file)}"
    with open(conf_path, "w") as file:
        yaml.dump({"param1": 1, "param2": ["smart", "rich", "good-looking"]}, file)
    yield conf_file
    os.remove(conf_path)


@pytest.fixture
def credentials_configuration_file():
    conf_file = "test_creds_conf.yaml"
    conf_path = f"{get_project_root().joinpath('conf', 'credentials', conf_file)}"
    with open(conf_path, "w") as file:
        yaml.dump({"cred1": "titus", "cred2": "ashley", "cred3": 1225}, file)
    yield conf_file
    os.remove(conf_path)


class TestLoadConfig:
    def test_on_paramaters_configuration(self, parameters_configuration_file):
        conf_file = parameters_configuration_file
        conf = load_config("conf", "parameters", conf_file)
        assert conf == {"param1": 1, "param2": ["smart", "rich", "good-looking"]}
        assert isinstance(conf, dict)

    def test_on_credentials_configuration(self, credentials_configuration_file):
        conf_file = credentials_configuration_file
        conf = load_config("conf", "credentials", conf_file)
        assert conf == {"cred1": "titus", "cred2": "ashley", "cred3": 1225}
        assert isinstance(conf, dict)

    def test_input_type_error(self):
        with pytest.raises(TypeError):
            load_config("conf", 12)

    def test_input_file_not_found_error(self):
        with pytest.raises(FileNotFoundError):
            load_config("conf", "parameters", "test_params_conf.yaml")
