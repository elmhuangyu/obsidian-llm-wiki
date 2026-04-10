#!/usr/bin/env python3
"""Absorb script for LLM-powered personal wiki.

Synthesizes raw entries into the persistent wiki in 03_Wiki/.
Tracks processed files via absorb_state.yaml to enable incremental runs.
"""

import datetime
import logging
import subprocess
import sys
from pathlib import Path

from state import (
  collect_candidates,
  find_pending,
  load_state,
  record_failure,
  record_success,
  save_state,
)

_INPUT_DIRS = [Path("01_Raw")]
_OUTPUT_DIR = Path("03_Wiki")
_SUPPORTED_EXTENSIONS = [".md"]
_STATE_FILE = Path(".state/absorb_state.yaml")
_PROMPT_FILE = Path("Scripts/prompts/absorb.md")


def absorb_file(filepath: Path) -> bool:
  if not _PROMPT_FILE.exists():
    print(f"Error: Prompt file {_PROMPT_FILE} not found.", file=sys.stderr)
    return False

  with open(_PROMPT_FILE, "r") as f:
    prompt_content = f.read()

  today_date = datetime.date.today().isoformat()

  # Read the entry content to provide as context
  with open(filepath, "r") as f:
    entry_content = f.read()

  full_prompt = (
    f"{prompt_content}\n\n"
    f"Context:\n"
    f"- Today's Date: {today_date}\n"
    f"- Raw Entry File: {filepath}\n"
    f"- Raw Entry Content:\n---\n{entry_content}\n---\n"
    f"\nTask: Absorb the information from the above entry into the wiki in {_OUTPUT_DIR}."
  )

  print(f"  Running LLM absorption for {filepath.name}...", end="", flush=True)
  try:
    # We use gemini CLI to perform the absorption.
    # It will have access to the 03_Wiki directory to read/write files.
    result = subprocess.run(
      ["gemini", "--approval-mode", "auto_edit", "-p", full_prompt],
      capture_output=True,
      text=True,
      check=False,
      stdin=subprocess.DEVNULL,
    )
    if result.returncode != 0:
      logging.info(f"Return Code: {result.returncode}")
      logging.info(f"STDOUT:\n{result.stdout}")
      logging.info(f"STDERR:\n{result.stderr}")
    else:
      logging.debug(f"Return Code: {result.returncode}")
      logging.debug(f"STDOUT:\n{result.stdout}")
      logging.debug(f"STDERR:\n{result.stderr}")
  except Exception as e:
    print(f" error running LLM: {e}")
    return False

  if result.returncode == 0:
    print(" done.")
    return True
  else:
    print(f" failed (return code {result.returncode}).")
    return False


def run() -> dict:
  state = load_state(_STATE_FILE)

  candidates = []
  for input_dir in _INPUT_DIRS:
    if input_dir.exists():
      candidates.extend(collect_candidates(input_dir, _SUPPORTED_EXTENSIONS))

  pending = find_pending(candidates, state)

  if not pending:
    print("Nothing to absorb — all entries up to date.")
    return {}

  _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

  processed = {}
  for filepath in pending:
    print(f"Absorbing: {filepath}")
    success = absorb_file(filepath)

    if success:
      record_success(filepath, state, status="absorbed", date=datetime.date.today().isoformat())
      processed[filepath.name] = state[filepath.name]
      print(f"✓ Absorbed: {filepath.name}")
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

  parser = argparse.ArgumentParser(description="Absorb script")
  parser.add_argument("--debug", action="store_true", help="Enable debug logging")
  args = parser.parse_args()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  run()
