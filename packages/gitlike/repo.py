import os
from typing import Optional
from pathlib import Path


GITLIKE_ROOT = ".gitlike"
GITLIKE_REFS = Path(GITLIKE_ROOT, "refs")
GITLIKE_REFS_HEADS = Path(GITLIKE_REFS, "heads")
GITLIKE_HEAD = Path(GITLIKE_ROOT, "HEAD")
GITLIKE_OBJECTS = Path(GITLIKE_ROOT, "objects")
GITLIKE_INDEX = Path(GITLIKE_ROOT, "index")

GITLIKE_DEFAULT_MAIN_BRANCH = "master"


class Repo():
    def __init__(self):
        return

    # TODO split
    def init(self, repo_path: str) -> Optional[Exception]:
        try:
            # TODO do smth when exists
            if os.path.exists(Path(repo_path, GITLIKE_ROOT)):
                print("Repo already exists")
                return None
            os.mkdir(Path(repo_path, GITLIKE_ROOT))
            os.mkdir(Path(repo_path, GITLIKE_REFS))
            os.mkdir(Path(repo_path, GITLIKE_REFS_HEADS))
            os.mkdir(Path(repo_path, GITLIKE_HEAD))
            os.mkdir(Path(repo_path, GITLIKE_OBJECTS))
            os.mkdir(Path(repo_path, GITLIKE_INDEX))
            with open(GITLIKE_HEAD, "w") as f:
                data = f"ref: refs/heads/{GITLIKE_DEFAULT_MAIN_BRANCH}\n"
                f.write(data)
            return None
        except IOError as e:
            return e
