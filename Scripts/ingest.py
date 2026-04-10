#!/usr/bin/env python3
"""Ingest script for LLM-powered personal wiki.

Converts diverse data sources into clean Markdown format using MarkItDown.
Tracks processed files via ingest_state.yaml to enable incremental runs.
"""

import datetime
import logging
from pathlib import Path

from ingest_processor import ingest_file
from state import (
  collect_candidates,
  find_pending,
  load_state,
  record_failure,
  record_success,
  save_state,
)

_INPUT_DIR = Path("Data")
_OUTPUT_DIR = Path("01_Raw/Entities")
_SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".md", ".html"]
_STATE_FILE = Path(".state/ingest_state.yaml")


def run() -> dict:
  state = load_state(_STATE_FILE)
  candidates = collect_candidates(_INPUT_DIR, _SUPPORTED_EXTENSIONS)
  pending = find_pending(candidates, state)

  if not pending:
    print("Nothing to process — all files up to date.")
    return {}

  _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  processed = {}
  for filepath in pending:
    print(f"Processing: {filepath}")
    final_path = ingest_file(filepath, _OUTPUT_DIR)

    if final_path:
      record_success(
        filepath, state, status="ingested", output=str(final_path), date=datetime.date.today().isoformat()
      )
      processed[filepath.name] = state[filepath.name]
      print(f"✓ Ingested: {filepath.name} -> {final_path.name}")
    else:
      record_failure(filepath, state)
      print(f"✗ Failed: {filepath.name}")

    # Periodic state saving
    if len(processed) % 5 == 0:
      save_state(state, _STATE_FILE)

  save_state(state, _STATE_FILE)
  return processed


if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="Ingest script")
  parser.add_argument("--debug", action="store_true", help="Enable debug logging")
  args = parser.parse_args()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  run()
