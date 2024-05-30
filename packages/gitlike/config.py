from pathlib import Path
from enum import Enum
from typing import Dict, Tuple, Optional

from repo import GITLIKE_ROOT

GITLIKE_CONFIG = Path(GITLIKE_ROOT, "config")

ConfigKey = Enum("ConfigKey", ["user_name"])


class Config():
    def __init__(self):
        return

    @staticmethod
    def write(root_path: Path, config: Dict) -> Optional[Exception]:
        try:
            data = "\n".join(config)
            Path(root_path, GITLIKE_CONFIG).write_text(data)
            return None
        except IOError as e:
            return e

    # TODO better parsing
    @staticmethod
    def parsed(root_path: Path) -> Tuple[Optional[Dict], Optional[Exception]]:
        text, err = Config.raw(root_path)
        if err:
            return None, err
        if not text:
            return None, None
        config = {}
        lines = text.splitlines()
        for line in lines:
            key, value = line.split("=")
            config[key] = value
        return config, None

    @staticmethod
    def raw(root_path: Path) -> Tuple[
            Optional[str],
            Optional[Exception],
    ]:
        try:
            path = Path(root_path, GITLIKE_CONFIG)
            if not path.exists():
                return None, None
            data = path.read_text()
            return data, None
        except IOError as e:
            return None, e

    @staticmethod
    def set_value(root_path: Path, key: ConfigKey, value: str) -> bool:
        config, err = Config.parsed(root_path)
        if not config or err:
            return False
        config[key] = value
        Config.write(root_path, config)
        return True

    @staticmethod
    def get_value(
            root_path: Path,
            key: ConfigKey
    ) -> Tuple[Optional[str], Optional[Exception]]:
        config, err = Config.parsed(root_path)
        if err:
            return None, err
        if not config:
            return None, None
        value = config[key]
        return value, None
