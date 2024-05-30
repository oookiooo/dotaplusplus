from pathlib import Path
from enum import Enum
from typing import Dict, Tuple

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
    def write(root_path: Path, config: Dict) -> Exception | None:
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
    def parse(root_path: Path) -> Tuple[Dict, Exception | None]:
        config = {}
        try:
            text = Path(root_path, consts.GITLIKE_CONFIG).read_text()
            lines = text.splitlines()
            for line in lines:
                key, value = line.split("=")
                config[key] = value
            return config, None
        except IOError as e:
            return config, e

    @staticmethod
    def set_value(
            root_path: Path,
            key: ConfigKey,
            value: str
    ) -> Exception | None:
        config, err = Config.parse(root_path)
        if err:
            return err
        config[key] = value
        return Config.write(root_path, config)

    @staticmethod
    def get_value(
        root_path: Path,
        key: ConfigKey
    ) -> Tuple[str | None, Exception | None]:
        config, err = Config.parse(root_path)
        if err:
            return "", err
        value = config.get(key)
        return value, None
