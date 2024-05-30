from pathlib import Path

from object import Object
from repo import Repo

# TODO add tests, make the `__init__.py` an exporter


# this is only for now
root_path = "test_repo"
repo = Repo()
object = Object(root_path)

repo.delete(root_path)
repo.init(root_path)
Path(root_path, "src").mkdir()
Path(root_path, "main.py").touch()
is_repo_valid = repo.validate(root_path)
if is_repo_valid:
    print("Repo is valid")
    sha, err = object.write_tree(Path(root_path, "src"))
    print(sha, err)
    sha, err = object.write_blob(Path(root_path, "main.py"))
    print(sha, err)

    repo.print(root_path)
else:
    print("Repo is invalid")
