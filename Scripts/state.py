"""YAML-backed state tracking for incremental file processing."""

import hashlib
from pathlib import Path

import yaml


def compute_sha1(filepath: Path) -> str:
  with open(filepath, "rb") as f:
    digest = hashlib.file_digest(f, "sha1")
    return digest.hexdigest()


def load_state(state_file: Path) -> dict:
  if state_file.exists():
    with open(state_file) as f:
      return yaml.safe_load(f) or {}
  return {}


def save_state(state: dict, state_file: Path) -> None:
  state_file.parent.mkdir(parents=True, exist_ok=True)
  with open(state_file, "w") as f:
    yaml.dump(state, f, default_flow_style=False, allow_unicode=True)


def needs_processing(filepath: Path, state: dict) -> bool:
  if filepath.name not in state:
    return True
  current_hash = compute_sha1(filepath)
  return state[filepath.name].get("sha1") != current_hash


def collect_candidates(input_dir: Path, extensions: list[str]) -> list[Path]:
  return [f for f in input_dir.rglob("*") if f.is_file() and f.suffix.lower() in extensions]


def find_pending(candidates: list[Path], state: dict) -> list[Path]:
  return [f for f in candidates if needs_processing(f, state)]


def record_success(filepath: Path, state: dict, status: str, **kwargs) -> None:
  state[filepath.name] = {
    "path": str(filepath),
    "sha1": compute_sha1(filepath),
    "status": status,
    **kwargs,
  }


def record_failure(filepath: Path, state: dict) -> None:
  state[filepath.name] = {
    "path": str(filepath),
    "status": "failed",
  }
