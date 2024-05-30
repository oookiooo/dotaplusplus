from typing import Optional
from pathlib import Path

GITLIKE_ROOT = ".gl"
GITLIKE_REFS = Path(GITLIKE_ROOT, "refs")
GITLIKE_REFS_HEADS = Path(GITLIKE_REFS, "heads")
GITLIKE_HEAD = Path(GITLIKE_ROOT, "HEAD")
GITLIKE_OBJECTS = Path(GITLIKE_ROOT, "objects")
GITLIKE_INDEX = Path(GITLIKE_ROOT, "cos_sie_psuje_z_git_index")

GITLIKE_DEFAULT_MAIN_BRANCH = "master"


# TODO rename `Repo`, it is a bad name for `.gl` dirs and files
class Repo():
    def __init__(self):
        return

    # TODO better printing, error handling
    def print(self, root_path) -> Optional[Exception]:
        try:
            dir = Path(root_path, GITLIKE_ROOT)
            return Repo.print_dir(dir)
        except IOError as e:
            return e

    # TODO better checking, prop returning tuple [smth,except]
    def validate(self, repo_path: str) -> bool:
        if not Path(repo_path, GITLIKE_ROOT).exists():
            return False
        if not Path(repo_path, GITLIKE_ROOT).is_dir():
            return False
        if not Path(repo_path, GITLIKE_REFS).exists():
            return False
        if not Path(repo_path, GITLIKE_REFS).is_dir():
            return False
        if not Path(repo_path, GITLIKE_REFS_HEADS).exists():
            return False
        if not Path(repo_path, GITLIKE_REFS_HEADS).is_file():
            return False
        if not Path(repo_path, GITLIKE_OBJECTS).exists():
            return False
        if not Path(repo_path, GITLIKE_OBJECTS).is_dir():
            return False
        if not Path(repo_path, GITLIKE_INDEX).exists():
            return False
        if not Path(repo_path, GITLIKE_HEAD).exists():
            return False
        if not Path(repo_path, GITLIKE_HEAD).is_file():
            return False
        return True

    def delete(self, repo_path) -> Optional[Exception]:
        try:
            if not Path(repo_path, GITLIKE_ROOT).exists():
                return None
            return Repo.rmrf(repo_path)
        except IOError as e:
            return e

    # TODO split, prop returning tuple [smth,except]
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

    @staticmethod
    def rmrf(dir: Path) -> Optional[Exception]:
        try:
            dir = Path(dir)
            for item in dir.iterdir():
                if item.is_dir():
                    Repo.rmrf(item)
                else:
                    item.unlink()
            dir.rmdir()
            return None
        except IOError as e:
            return e

    @staticmethod
    def print_dir(dir_path: Path, prefix: str = "") -> Optional[Exception]:
        try:
            if dir_path.is_dir():
                print(f"{prefix}{dir_path.name}/")
                for item in dir_path.iterdir():
                    Repo.print_dir(item, prefix + "    ")
                return None
            else:
                print(f"{prefix}{dir_path.name}")
                return None
        except IOError as e:
            return e
