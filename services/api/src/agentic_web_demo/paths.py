from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
API_DIR = PACKAGE_DIR.parents[1]
REPOSITORY_ROOT = PACKAGE_DIR.parents[3]
DATA_DIR = API_DIR / "data"
SPECS_DEMO_DIR = REPOSITORY_ROOT / "specs" / "demo"
