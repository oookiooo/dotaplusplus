from pathlib import Path
from enum import Enum
from typing import Dict, Optional

import consts


class ConfigKey(str, Enum):
    user_name = "user_name"


class Config():
    def __init__(self):
        return

    @staticmethod
    def print(root_path: Path):
        config = Config.parse(root_path)
        print("CONFIG: ", Path(root_path, consts.GITLIKE_CONFIG), "\n", config)

    @staticmethod
    def write(root_path: Path, config: Dict) -> Optional[Exception]:
        try:
            data = ""
            for key, value in config.items():
                data += key + "=" + value + "\n"
            Path(root_path, consts.GITLIKE_CONFIG).write_text(data)
            return None
        except IOError as e:
            return e

    # TODO better parsing
    @staticmethod
    def parse(root_path: Path) -> Dict:
        text = Path(root_path, consts.GITLIKE_CONFIG).read_text()
        config = {}
        lines = text.splitlines()
        for line in lines:
            key, value = line.split("=")
            config[key] = value
        return config

    @staticmethod
    def set_value(
            root_path: Path,
            key: ConfigKey,
            value: str
    ):
        config = Config.parse(root_path)
        config[key] = value
        Config.write(root_path, config)

    @staticmethod
    def get_value(
        root_path: Path,
        key: ConfigKey
    ) -> str:
        config = Config.parse(root_path)
        value = config[key]
        return value
