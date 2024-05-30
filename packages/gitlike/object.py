import hashlib
import os
import time
import zlib
from typing import Optional, Tuple
from pathlib import Path
from repo import GITLIKE_OBJECTS, GITLIKE_ROOT

OBJ_KIND_COMMIT = "commit"  # commit
OBJ_KIND_BLOB = "blob"      # file
OBJ_KIND_TREE = "tree"      # directory


# TODO tests
class Object():
    def __init__(self, root_path):
        # TODO do not assign `.gl` path to `Object` class
        self.root_path = root_path
        return

    def write_blob(
            self,
            file_path: Path
    ) -> Tuple[Optional[str], Optional[Exception]]:
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return self.write(OBJ_KIND_BLOB, data.decode())
        except IOError as e:
            return None, e

    def write_tree(
        self,
        dir_path: Path
    ) -> Tuple[Optional[str], Optional[Exception]]:
        entries = []
        try:
            for entry in os.scandir(dir_path):
                if entry.name == GITLIKE_ROOT:
                    continue
                if entry.is_dir():
                    mode = "40000"
                    sha, err = self.write_tree(Path(entry.path))
                else:
                    mode = f"{entry.stat().st_mode:o}"
                    sha, err = self.write_blob(Path(entry.path))
                if err:
                    return None, err
                entry_data = f"{mode}{entry.name}\000{sha}"
                entries.append(entry_data)
            return self.write(OBJ_KIND_TREE, "".join(entries))
        except IOError as e:
            return None, e

    def write_commit(
            self,
            tree_sha: str,
            parent_sha: str,
            message: str
    ) -> Tuple[Optional[str], Optional[Exception]]:
        now = time.localtime()
        timestamp = f"{int(time.mktime(now))} {time.strftime('%z', now)}"
        data = (
            f"tree {tree_sha}\n"
            f"parent {parent_sha}\n"
            f"author [author] {timestamp}\n"
            f"message {message}\n"
        )
        return self.write(OBJ_KIND_COMMIT, data)

    def write(
            self,
            kind: str,
            data: str
    ) -> Tuple[Optional[str], Optional[Exception]]:
        header = f"{kind} {len(data)}"
        full = header + "\000" + data
        sha = hashlib.sha1(full.encode()).hexdigest()
        path = self.path(sha)
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

    def read(self, sha: str) -> Tuple[Optional[str], Optional[Exception]]:
        try:
            with open(self.path(sha), "rb") as f:
                decompressed = zlib.decompress(f.read()).decode()
                print(decompressed)
            return decompressed, None
        except IOError as e:
            return None, e

    def path(self, sha: str) -> Path:
        return Path(self.root_path, GITLIKE_OBJECTS, sha[:2], sha[:2])
