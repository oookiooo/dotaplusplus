from enum import Enum
import hashlib
import os
import time
import zlib
from typing import Optional, Tuple
from pathlib import Path

import consts
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
    ) -> Tuple[str, Optional[Exception]]:
        try:
            with open(Path(root_path, file_path), "rb") as f:
                data = f.read()
            return Object.write(root_path, ObjectKind.blob, data.decode())
        except IOError as e:
            return "", e

    @staticmethod
    def write_tree(
        root_path: Path,
        dir_path: Path
    ) -> Tuple[str, Optional[Exception]]:
        entries = []
        try:
            abs_dir_path = Path(root_path, dir_path)
            for entry in os.scandir(abs_dir_path):
                entry_path = Path(entry.path)
                relative_entry_path = entry_path.relative_to(root_path)
                if relative_entry_path.parts[0] == consts.GITLIKE_ROOT.name:
                    continue
                if entry.is_dir():
                    mode = "40000"
                    sha, err = Object.write_tree(
                        root_path,
                        relative_entry_path
                    )
                else:
                    mode = f"{entry.stat().st_mode:o}"
                    sha, err = Object.write_blob(
                        root_path,
                        relative_entry_path
                    )
                if err:
                    return "", err
                entry_data = f"{mode}{entry.name}\000{sha}"
                entries.append(entry_data)
            return Object.write(root_path, ObjectKind.tree, "".join(entries))
        except IOError as e:
            return "", e

    @staticmethod
    def write_commit(
            root_path: Path,
            tree_sha: str,
            parent_sha: str,
            message: str
    ) -> Tuple[str, Optional[Exception]]:
        now = time.localtime()
        timestamp = f"{int(time.mktime(now))} {time.strftime('%z', now)}"
        user_name, err = Config.get_value(root_path, ConfigKey.user_name)
        if err:
            return "", err
        if user_name is None:
            user_name = "[user_name_not_provided_in_config]"
        data = (
            f"tree {tree_sha}\n"
            f"parent {parent_sha}\n"
            f"author {user_name} {timestamp}\n"
            f"\n"
            f"{message}\n"
        )
        return Object.write(root_path, ObjectKind.commit, data)

    @staticmethod
    def write(
            root_path: Path,
            kind: str,
            data: str
    ) -> Tuple[str, Optional[Exception]]:
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
        except IOError as e:
            return "", e
        return sha, None

    @staticmethod
    def read(
            root_path: Path,
            sha: str
    ) -> Tuple[str, Optional[Exception]]:
        try:
            with open(Object.path(root_path, sha), "rb") as f:
                decompressed = zlib.decompress(f.read()).decode()
            return decompressed, None
        except IOError as e:
            return "", e

    @staticmethod
    def path(root_path: Path, sha: str) -> Path:
        return Path(root_path, consts.GITLIKE_OBJECTS, sha[:2], sha[:2])
