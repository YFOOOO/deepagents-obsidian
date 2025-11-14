# Inject path for local deepagents package without installation
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
DEEPAGENTS_ROOT = HERE.parent / "deepagents_official" / "libs" / "deepagents"
if DEEPAGENTS_ROOT.exists():
    sys.path.insert(0, str(DEEPAGENTS_ROOT))
