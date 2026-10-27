# Shared settings: active use case, data/index paths, and env toggles (default on).
# Every module reads paths from here so a new use case is a new folder, not a code change.
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USE_CASE = "vendor-risk-compliance"
DEFAULT_EMBEDDINGS_MODEL = "text-embedding-3-small"
DEFAULT_LLM_MODEL = "gpt-4o-mini"


def load_env() -> None:
    # .env at the repo root holds the API key; it's gitignored and never read by code beyond this
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")


def flag(name: str, default: bool = True) -> bool:
    # Toggles default to on; only an explicit false/0/no/off turns one off
    return os.environ.get(name, str(default)).strip().lower() not in {"false", "0", "no", "off"}


def use_case() -> str:
    return os.environ.get("USE_CASE", DEFAULT_USE_CASE)


def raw_dir(case: str | None = None) -> Path:
    return ROOT / "data" / (case or use_case()) / "raw"


def index_dir(case: str | None = None, embeddings_model: str | None = None) -> Path:
    # S7: one index per embeddings model, so switching models can't mix incompatible vectors
    model = embeddings_model or os.environ.get("EMBEDDINGS_MODEL", DEFAULT_EMBEDDINGS_MODEL)
    return ROOT / "data" / (case or use_case()) / "index" / model
