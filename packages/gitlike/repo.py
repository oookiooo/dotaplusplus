from typing import Optional, List
from pathlib import Path

from object import Object
from logger import Logger
import consts

# TODO rename `Repo`, it is a bad name for `.gl` dirs and files


class Repo():
    def __init__(self):
        return

    @staticmethod
    def add(root_path: Path, entries: List[Path]) -> Optional[Exception]:
        for entry in entries:
            entry_path = Path(root_path, entry)
            if entry_path.is_dir():
                _, err = Object.write_tree(root_path, entry)
            else:
                _, err = Object.write_blob(root_path, entry)
            if err:
                return err
        return None

    @staticmethod
    def commit(root_path: Path, message: str) -> Optional[Exception]:
        try:
            head = Path(root_path, consts.GITLIKE_HEAD)
            head_ref = head.read_text().strip().split(": ")[1]
            head_file = Path(root_path, head_ref)
            if head_file.exists():
                parent_sha = head_file.read_text().strip()
            else:
                parent_sha = ""
            tree_sha, err = Object.write_tree(root_path, Path(""))
            if err:
                return err
            commit_sha, err = Object.write_commit(
                root_path,
                tree_sha,
                parent_sha,
                message
            )
            if err:
                return err
            head_file.parent.mkdir(parents=True, exist_ok=True)
            head_file.write_text(commit_sha)
            master_ref_file = Path(
                root_path,
                consts.GITLIKE_REFS_HEADS,
                consts.GITLIKE_DEFAULT_MAIN_BRANCH
            )
            master_ref_file.write_text(commit_sha)
            return None
        except IOError as e:
            return e

    # TODO better printing, error handling

    @staticmethod
    def print(root_path: Path) -> Optional[Exception]:
        try:
            dir = Path(root_path, consts.GITLIKE_ROOT)
            return Repo.print_dir(dir)
        except IOError as e:
            return e

    # TODO split, better checking, prop returning tuple [smth,except]
    @staticmethod
    def validate(repo_path: Path) -> Optional[List[str]]:
        errors = []
        root = Path(repo_path, consts.GITLIKE_ROOT)
        refs = Path(repo_path, consts.GITLIKE_REFS)
        refs_heads = Path(repo_path, consts.GITLIKE_REFS_HEADS)
        refs_heads_main_branch = Path(
            repo_path,
            consts.GITLIKE_REFS_HEADS,
            consts.GITLIKE_DEFAULT_MAIN_BRANCH
        )
        objects = Path(repo_path, consts.GITLIKE_OBJECTS)
        index = Path(repo_path, consts.GITLIKE_INDEX)
        head = Path(repo_path, consts.GITLIKE_HEAD)
        config = Path(repo_path, consts.GITLIKE_CONFIG)
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
            if not Path(repo_path, consts.GITLIKE_ROOT).exists():
                return None
            return Repo.rmrf(repo_path)
        except IOError as e:
            return e

    # TODO split, prop returning tuple [smth,except]
    @staticmethod
    def init(repo_path: Path) -> Optional[Exception]:
        try:
            # TODO do smth when exists
            if Path(repo_path, consts.GITLIKE_ROOT).exists():
                print("Repo already exists")
                return None
            Path(repo_path, consts.GITLIKE_ROOT).mkdir(
                parents=True, exist_ok=True)
            Path(repo_path, consts.GITLIKE_REFS).mkdir(
                parents=True, exist_ok=True)
            Path(repo_path, consts.GITLIKE_REFS_HEADS).mkdir(
                parents=True, exist_ok=True)
            Path(
                repo_path,
                consts.GITLIKE_REFS_HEADS, consts.GITLIKE_DEFAULT_MAIN_BRANCH
            ).touch(exist_ok=True)
            Path(repo_path, consts.GITLIKE_OBJECTS).mkdir(
                parents=True, exist_ok=True)
            Path(repo_path, consts.GITLIKE_INDEX).touch(exist_ok=True)
            Path(repo_path, consts.GITLIKE_HEAD).write_text(
                f"ref: refs/heads/{consts.GITLIKE_DEFAULT_MAIN_BRANCH}\n"
            )
            Path(repo_path, consts.GITLIKE_CONFIG).touch(exist_ok=True)
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
