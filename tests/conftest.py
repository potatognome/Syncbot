from pathlib import Path
import sys


TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent
WORKSPACE_ROOT = PROJECT_ROOT.parents[1]

SYNCBOT_SRC = PROJECT_ROOT / "src"
TUILKIT_SRC = WORKSPACE_ROOT / "Core" / "tUilKit" / "src"

for path in [SYNCBOT_SRC, TUILKIT_SRC]:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
