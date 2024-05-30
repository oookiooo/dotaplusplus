from enum import Enum
import hashlib
import os
import time
import zlib
from typing import Optional, Tuple
from pathlib import Path

from repo import GITLIKE_OBJECTS, GITLIKE_ROOT
from config import Config, ConfigKey


class ObjectKind(str, Enum):
    commit = "commit"  # commit
    blob = "blob"      # file
    tree = "tree"      # directory


# TODO tests
class Object():
    def __init__(self):
        return

    @staticmethod
    def write_blob(
            root_path: Path,
            file_path: Path
    ) -> Tuple[Optional[str], Optional[Exception]]:
        try:
            with open(Path(root_path, file_path), "rb") as f:
                data = f.read()
            return Object.write(root_path, ObjectKind.blob, data.decode())
        except IOError as e:
            return None, e

    @staticmethod
    def write_tree(
        root_path: Path,
        dir_path: Path
    ) -> Tuple[Optional[str], Optional[Exception]]:
        entries = []
        try:
            for entry in os.scandir(Path(root_path, dir_path)):
                if entry.name == GITLIKE_ROOT:
                    continue
                if entry.is_dir():
                    mode = "40000"
                    sha, err = Object.write_tree(root_path, Path(entry.path))
                else:
                    mode = f"{entry.stat().st_mode:o}"
                    sha, err = Object.write_blob(root_path, Path(entry.path))
                if err:
                    return None, err
                entry_data = f"{mode}{entry.name}\000{sha}"
                entries.append(entry_data)
            return Object.write(root_path, ObjectKind.tree, "".join(entries))
        except IOError as e:
            return None, e

    @staticmethod
    def write_commit(
            root_path: Path,
            tree_sha: str,
            parent_sha: str,
            message: str
    ) -> Tuple[Optional[str], Optional[Exception]]:
        now = time.localtime()
        timestamp = f"{int(time.mktime(now))} {time.strftime('%z', now)}"
        user_name = Config.get_value(root_path, ConfigKey.user_name)
        if not user_name:
            # TODO do smth when user_name is not in config
            user_name = "[_not_provided_in_config]"
        data = (
            f"tree {tree_sha}\n"
            f"parent {parent_sha}\n"
            f"author {user_name} {timestamp}\n"
            f"message {message}\n"
        )
        return Object.write(root_path, ObjectKind.commit, data)

    @staticmethod
    def write(
            root_path: Path,
            kind: str,
            data: str
    ) -> Tuple[Optional[str], Optional[Exception]]:
        header = f"{kind} {len(data)}"
        full = header + "\000" + data
        sha = hashlib.sha1(full.encode()).hexdigest()
        path = Object.path(root_path, sha)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            return sha, None
        try:
            with open(path, "wb") as f:
                compressed = zlib.compress(full.encode())
                f.write(compressed)
                print(f.read())
        except IOError as e:
            return None, e
        return sha, None

    @staticmethod
    def read(
            root_path: Path,
            sha: str
    ) -> Tuple[Optional[str], Optional[Exception]]:
        try:
            with open(Object.path(root_path, sha), "rb") as f:
                decompressed = zlib.decompress(f.read()).decode()
                print(decompressed)
            return decompressed, None
        except IOError as e:
            return None, e

    @staticmethod
    def path(root_path: Path, sha: str) -> Path:
        return Path(root_path, GITLIKE_OBJECTS, sha[:2], sha[:2])
