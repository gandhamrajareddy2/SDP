import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
GENERATED_DIR = DATA_DIR / "generated"
DB_PATH = DATA_DIR / "lab.db"
FRONTEND_DIST_DIR = Path(os.getenv("FRONTEND_DIST_DIR", str(REPO_ROOT / "frontend" / "dist"))).resolve()


def _split_csv_env(name: str, default: list[str]) -> list[str]:
	raw_value = os.getenv(name, "")
	if not raw_value.strip():
		return default
	return [value.strip() for value in raw_value.split(",") if value.strip()]


CORS_ALLOW_ORIGINS = _split_csv_env(
	"CORS_ALLOW_ORIGINS",
	["http://localhost:5173", "http://127.0.0.1:5173"],
)
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "false").lower() == "true"

GENERATED_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
