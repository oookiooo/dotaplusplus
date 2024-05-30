from typing import Optional, List
from pathlib import Path

GITLIKE_ROOT = Path(".gl")
GITLIKE_REFS = Path(GITLIKE_ROOT, "refs")
GITLIKE_REFS_HEADS = Path(GITLIKE_REFS, "heads")
GITLIKE_HEAD = Path(GITLIKE_ROOT, "HEAD")
GITLIKE_OBJECTS = Path(GITLIKE_ROOT, "objects")
GITLIKE_INDEX = Path(GITLIKE_ROOT, "cos_sie_psuje_z_git_index")
GITLIKE_CONFIG = Path(GITLIKE_ROOT, "config")

GITLIKE_DEFAULT_MAIN_BRANCH = "master"


# TODO rename `Repo`, it is a bad name for `.gl` dirs and files


class Repo():
    def __init__(self):
        return

    # TODO better printing, error handling
    @staticmethod
    def print(root_path) -> Optional[Exception]:
        try:
            dir = Path(root_path, GITLIKE_ROOT)
            return Repo.print_dir(dir)
        except IOError as e:
            return e

    # TODO split, better checking, prop returning tuple [smth,except]
    @staticmethod
    def validate(repo_path: Path) -> Optional[List[str]]:
        errors = []
        root = Path(repo_path, GITLIKE_ROOT)
        refs = Path(repo_path, GITLIKE_REFS)
        refs_heads = Path(repo_path, GITLIKE_REFS_HEADS)
        refs_heads_main_branch = Path(
            repo_path, GITLIKE_REFS_HEADS, GITLIKE_DEFAULT_MAIN_BRANCH)
        objects = Path(repo_path, GITLIKE_OBJECTS)
        index = Path(repo_path, GITLIKE_INDEX)
        head = Path(repo_path, GITLIKE_HEAD)
        config = Path(repo_path, GITLIKE_CONFIG)
        check_path(errors, root, should_be_dir=True)
        check_path(errors, refs, should_be_dir=True)
        check_path(errors, refs_heads, should_be_dir=True)
        check_path(errors, refs_heads_main_branch, should_be_file=True)
        check_path(errors, objects, should_be_dir=True)
        check_path(errors, index, should_be_file=True)
        check_path(errors, head, should_be_file=True)
        check_path(errors, config, should_be_file=True)
        if len(errors) > 0:
            return errors
        return None

    @staticmethod
    def delete(repo_path: Path) -> Optional[Exception]:
        try:
            if not Path(repo_path, GITLIKE_ROOT).exists():
                return None
            return Repo.rmrf(repo_path)
        except IOError as e:
            return e

    # TODO split, prop returning tuple [smth,except]
    @staticmethod
    def init(repo_path: Path) -> Optional[Exception]:
        try:
            # TODO do smth when exists
            if Path(repo_path, GITLIKE_ROOT).exists():
                print("Repo already exists")
                return None
            Path(repo_path, GITLIKE_ROOT).mkdir(parents=True, exist_ok=True)
            Path(repo_path, GITLIKE_REFS).mkdir(parents=True, exist_ok=True)
            Path(repo_path, GITLIKE_REFS_HEADS).mkdir(
                parents=True, exist_ok=True)
            Path(
                repo_path,
                GITLIKE_REFS_HEADS, GITLIKE_DEFAULT_MAIN_BRANCH
            ).touch(exist_ok=True)
            Path(repo_path, GITLIKE_OBJECTS).mkdir(parents=True, exist_ok=True)
            Path(repo_path, GITLIKE_INDEX).touch(exist_ok=True)
            Path(repo_path, GITLIKE_HEAD).touch(exist_ok=True)
            Path(repo_path, GITLIKE_HEAD).write_text(
                data=f"ref: refs/heads/{GITLIKE_DEFAULT_MAIN_BRANCH}\n",
            )
            Path(repo_path, GITLIKE_CONFIG).touch(exist_ok=True)
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


def check_path(
        errors: List[str],
        path: Path,
        should_be_dir=False,
        should_be_file=False


):
    NOT_DIR = "NOT DIR"
    NOT_FILE = "NOT FILE"
    NOT_EXISTS = "NOT EXISTS"
    if not path.exists():
        errors.append(str_err(path, NOT_EXISTS))
    elif should_be_dir and not path.is_dir():
        errors.append(str_err(path, NOT_DIR))
    elif should_be_file and not path.is_file():
        errors.append(str_err(path, NOT_FILE))


def str_err(path: Path, err: str) -> str:
    return f"{path} {err}"
