#!/usr/bin/env python3
"""Absorb script for LLM-powered personal wiki.

Synthesizes raw entries into the persistent wiki in 03_Wiki/.
Tracks processed files via absorb_state.yaml to enable incremental runs.
"""

import datetime
import json
import logging
import sys
from pathlib import Path

import yaml
from gemini_cli import run_gemini_cli_json
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
_PLANNER_PROMPT_FILE = Path("Scripts/prompts/absorb_planner.md")


def extract_frontmatter(filepath: Path) -> dict:
  with open(filepath, "r") as f:
    content = f.read()
  if content.startswith("---"):
    parts = content.split("---", 2)
    if len(parts) >= 3:
      try:
        fm = yaml.safe_load(parts[1])
        return fm if isinstance(fm, dict) else {}
      except yaml.YAMLError:
        pass
  return {}


def plan_groups(pending: list[Path]) -> list[list[Path]]:
  if not pending:
    return []

  if not _PLANNER_PROMPT_FILE.exists():
    print(f"Error: Prompt file {_PLANNER_PROMPT_FILE} not found.", file=sys.stderr)
    return [[p] for p in pending]

  file_metadata = []
  for p in pending:
    fm = extract_frontmatter(p)
    file_metadata.append(
      {"filename": p.name, "tags": fm.get("tags", []), "summary": fm.get("summary", "")}
    )

  with open(_PLANNER_PROMPT_FILE, "r") as f:
    prompt_content = f.read()

  # Adding JSON format context
  full_prompt = (
    f"{prompt_content}\n\n"
    f"Files to group:\n"
    f"```json\n"
    f"{json.dumps(file_metadata, indent=2, ensure_ascii=False)}\n"
    f"```"
  )

  print("  Running Planner LLM to group files...", flush=True)
  try:
    response = run_gemini_cli_json(full_prompt, auto_edit=False)

    if response.return_code != 0:
      logging.warning(
        f"Planner failed (return code {response.return_code}), processing individually.\nSTDERR:\n{response.text}"
      )
      return [[p] for p in pending]

    # Standardize output (just in case LLM wraps it in markdown blocks)
    out_text = response.text.strip()
    if out_text.startswith("```json"):
      out_text = out_text[7:]
    if out_text.startswith("```"):
      out_text = out_text[3:]
    if out_text.endswith("```"):
      out_text = out_text[:-3]
    out_text = out_text.strip()

    grouped_filenames = json.loads(out_text)

    paths_by_name = {p.name: p for p in pending}
    groups = []
    for group in grouped_filenames:
      group_paths = [
        paths_by_name[name] for name in group if isinstance(name, str) and name in paths_by_name
      ]
      if group_paths:
        groups.append(group_paths)

    # Catch any missing files just in case
    grouped_names = {p.name for group in groups for p in group}
    for p in pending:
      if p.name not in grouped_names:
        groups.append([p])

    return groups

  except Exception as e:
    logging.error(f"Planner error: {e}")
    return [[p] for p in pending]


def absorb_group(filepaths: list[Path]) -> bool:
  if not _PROMPT_FILE.exists():
    print(f"Error: Prompt file {_PROMPT_FILE} not found.", file=sys.stderr)
    return False

  with open(_PROMPT_FILE, "r") as f:
    prompt_content = f.read()

  today_date = datetime.date.today().isoformat()

  context_parts = []
  for filepath in filepaths:
    with open(filepath, "r") as f:
      entry_content = f.read()
    context_parts.append(
      f"- Raw Entry File: {filepath}\n- Raw Entry Content:\n---\n{entry_content}\n---"
    )

  combined_context = "\n".join(context_parts)

  full_prompt = (
    f"{prompt_content}\n\n"
    f"Context:\n"
    f"- Today's Date: {today_date}\n"
    f"{combined_context}\n"
    f"\nTask: Absorb the information from the above entries into the wiki in {_OUTPUT_DIR}."
  )

  names = ", ".join(p.name for p in filepaths)
  print(f"  Running LLM absorption for [{names}]...", end="", flush=True)
  try:
    response = run_gemini_cli_json(full_prompt, auto_edit=True)
  except Exception as e:
    print(f" error running LLM: {e}")
    return False

  if response.return_code == 0:
    print(" done.")
    return True
  else:
    print(f" failed (return code {response.return_code}).")
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

  groups = plan_groups(pending)

  processed = {}
  for group in groups:
    names = ", ".join(p.name for p in group)
    print(f"Absorbing Group: {names}")
    success = absorb_group(group)

    for filepath in group:
      if success:
        record_success(filepath, state, status="absorbed", date=datetime.date.today().isoformat())
        processed[filepath.name] = state[filepath.name]
        print(f"✓ Absorbed: {filepath.name}")
      else:
        record_failure(filepath, state)
        print(f"✗ Failed: {filepath.name}")

    # Periodic state saving
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
