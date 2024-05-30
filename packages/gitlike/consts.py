from pathlib import Path

GITLIKE_ROOT = Path(".gl")
GITLIKE_REFS = Path(GITLIKE_ROOT, "refs")
GITLIKE_REFS_HEADS = Path(GITLIKE_REFS, "heads")
GITLIKE_HEAD = Path(GITLIKE_ROOT, "HEAD")
GITLIKE_OBJECTS = Path(GITLIKE_ROOT, "objects")
GITLIKE_INDEX = Path(GITLIKE_ROOT, "cos_sie_psuje_z_git_index")
GITLIKE_CONFIG = Path(GITLIKE_ROOT, "config")

GITLIKE_DEFAULT_MAIN_BRANCH = "master"
