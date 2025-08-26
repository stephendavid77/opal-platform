import json
import logging
import os
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class SharedConfigManager:
    _config_cache = {}
    _base_path = Path(__file__).parent  # This will be shared/config/

    @classmethod
    def get_config(cls, file_key: str):
        if file_key in cls._config_cache:
            return cls._config_cache[file_key]

        file_path = cls._base_path / file_key
        if not file_path.exists():
            logger.error(f"Configuration file not found: {file_path}")
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        try:
            if file_path.suffix in [".yaml", ".yml"]:
                with open(file_path, "r") as f:
                    config_data = yaml.safe_load(f)
            elif file_path.suffix == ".json":
                with open(file_path, "r") as f:
                    config_data = json.load(f)
            else:
                logger.error(f"Unsupported configuration file type: {file_path.suffix}")
                raise ValueError(
                    f"Unsupported configuration file type: {file_path.suffix}"
                )

            cls._config_cache[file_key] = config_data
            logger.info(f"Successfully loaded configuration from {file_path}")
            return config_data
        except Exception as e:
            logger.error(f"Error loading configuration from {file_path}: {e}")
            raise
