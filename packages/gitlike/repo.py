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
            if Path(repo_path, GITLIKE_ROOT).exists():
                print("Repo already exists")
                return None
            Path(repo_path, GITLIKE_ROOT).mkdir(parents=True, exist_ok=True)
            Path(repo_path, GITLIKE_REFS).mkdir(parents=True, exist_ok=True)
            Path(repo_path, GITLIKE_REFS_HEADS).touch(exist_ok=True)
            Path(repo_path, GITLIKE_OBJECTS).mkdir(parents=True, exist_ok=True)
            Path(repo_path, GITLIKE_INDEX).touch(exist_ok=True)
            Path(repo_path, GITLIKE_HEAD).write_text(
                data=f"ref: refs/heads/{GITLIKE_DEFAULT_MAIN_BRANCH}\n"
            )
            print("Repo created")
            return None
        except IOError as e:
            print(e)
            return e
