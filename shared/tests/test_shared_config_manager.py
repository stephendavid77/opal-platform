import json
import os
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import yaml

from shared.config.shared_config_manager import SharedConfigManager

# Define a temporary directory for test config files
TEST_CONFIG_DIR = Path(__file__).parent.parent / "config"


@pytest.fixture(autouse=True)
def setup_and_teardown_config_files():
    # Ensure the test config directory exists
    TEST_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Create dummy config files for testing
    dummy_yaml_content = {"test_key_yaml": "test_value_yaml", "nested": {"key": 123}}
    with open(TEST_CONFIG_DIR / "test_config.yaml", "w") as f:
        yaml.dump(dummy_yaml_content, f)

    dummy_json_content = {"test_key_json": "test_value_json", "array": [1, 2, 3]}
    with open(TEST_CONFIG_DIR / "test_config.json", "w") as f:
        json.dump(dummy_json_content, f)

    # Clear the cache before each test
    SharedConfigManager._config_cache = {}

    yield

    # Clean up dummy config files after tests
    os.remove(TEST_CONFIG_DIR / "test_config.yaml")
    os.remove(TEST_CONFIG_DIR / "test_config.json")
    # If the test creates other files, remove them here as well
    if (TEST_CONFIG_DIR / "non_existent.yaml").exists():
        os.remove(TEST_CONFIG_DIR / "non_existent.yaml")


def test_get_config_yaml():
    config = SharedConfigManager.get_config("test_config.yaml")
    assert config["test_key_yaml"] == "test_value_yaml"
    assert config["nested"]["key"] == 123


def test_get_config_json():
    config = SharedConfigManager.get_config("test_config.json")
    assert config["test_key_json"] == "test_value_json"
    assert config["array"] == [1, 2, 3]


def test_get_config_from_cache():
    # First call populates cache
    config1 = SharedConfigManager.get_config("test_config.yaml")
    # Modify the file content - should not affect cached result
    with open(TEST_CONFIG_DIR / "test_config.yaml", "w") as f:
        yaml.dump({"test_key_yaml": "modified_value"}, f)
    # Second call should return cached result
    config2 = SharedConfigManager.get_config("test_config.yaml")
    assert config1["test_key_yaml"] == "test_value_yaml"
    assert config2["test_key_yaml"] == "test_value_yaml"  # Still the original value


def test_get_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        SharedConfigManager.get_config("non_existent.yaml")


def test_get_config_unsupported_file_type():
    # Create a dummy file with unsupported extension
    with open(TEST_CONFIG_DIR / "unsupported.txt", "w") as f:
        f.write("some content")
    with pytest.raises(ValueError, match="Unsupported configuration file type"):
        SharedConfigManager.get_config("unsupported.txt")
    os.remove(TEST_CONFIG_DIR / "unsupported.txt")


def test_get_config_invalid_yaml():
    with open(TEST_CONFIG_DIR / "invalid.yaml", "w") as f:
        f.write("key: - value")  # Invalid YAML
    with pytest.raises(yaml.YAMLError):
        SharedConfigManager.get_config("invalid.yaml")
    os.remove(TEST_CONFIG_DIR / "invalid.yaml")


def test_get_config_invalid_json():
    with open(TEST_CONFIG_DIR / "invalid.json", "w") as f:
        f.write("{key: value}")  # Invalid JSON
    with pytest.raises(json.JSONDecodeError):
        SharedConfigManager.get_config("invalid.json")
    os.remove(TEST_CONFIG_DIR / "invalid.json")
