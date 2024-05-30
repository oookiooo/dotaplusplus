from pathlib import Path

from object import Object
from repo import Repo
from config import Config, ConfigKey

# TODO add tests, make the `__init__.py` an exporter


# this is only for now
root_path = Path("test_repo")
repo = Repo()
Config.set_value(root_path, ConfigKey.user_name, "Ktos")
Config.print(root_path)

repo.delete(root_path)
repo.init(root_path)
Path(root_path, "src").mkdir()
Path(root_path, "main.py").touch()
repo_errors = repo.validate(root_path)
if not repo_errors:
    print("Repo is valid")
    sha, err = Object.write_tree(root_path, Path("src"))
    print(sha, err)
    sha, err = Object.write_blob(root_path, Path("main.py"))
    print(sha, err)

    repo.print(root_path)
    err = Repo.add(root_path, [Path("src"), Path("main.py")])
    if err:
        print(err)
    err = Repo.commit(root_path, "feat: cos")
    if err:
        print(err)
else:
    print(repo_errors)
