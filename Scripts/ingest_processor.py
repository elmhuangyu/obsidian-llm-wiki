#!/usr/bin/env python3

import datetime
import re
import shutil
import sys
from pathlib import Path

from gemini_cli import run_gemini_cli_json
from markitdown import MarkItDown

_MARKITDOWN_EXTENSIONS = [".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".html"]


def ingest_file(filepath: Path, output_dir: Path) -> Path | None:
  try:
    if filepath.suffix in _MARKITDOWN_EXTENSIONS:
      output_file = to_markdown(filepath, output_dir)
    else:
      output_file = output_dir / filepath.name
      shutil.copy2(filepath, output_file)

    final_output_file = post_process_with_llm(output_file, filepath)
    return final_output_file

  except Exception as e:
    print(f"Error processing {filepath}: {e}", file=sys.stderr)
    return None


def to_markdown(filepath: Path, output_dir: Path) -> Path:
  md = MarkItDown()
  result = md.convert(filepath)
  markdown_content = result.text_content

  output_file = output_dir / f"{filepath.stem}.md"
  with open(output_file, "w") as f:
    f.write(markdown_content)

  return output_file


def post_process_with_llm(filepath: Path, original_filepath: Path) -> Path:
  prompt_file = Path("Scripts/prompts/ingest.md")
  if not prompt_file.exists():
    return filepath

  with open(prompt_file, "r") as f:
    prompt_content = f.read()

  today_date = datetime.date.today().isoformat()
  original_ext = original_filepath.suffix or "unknown"

  full_prompt = (
    f"{prompt_content}\n\n"
    f"Context:\n"
    f"- Today's Date: {today_date}\n"
    f"- Original File Extension/Source Type: {original_ext}\n"
    f"\nTask: Please process this file: {filepath}"
  )

  print(f"  Running LLM post-processing on {filepath.name}...", end="", flush=True)

  response = run_gemini_cli_json(full_prompt, auto_edit=True)
  if response.return_code != 0 and response.return_code != 127:
    print(f" error running LLM (code {response.return_code})")
    return filepath
  elif response.return_code == 127:
    return filepath

  llm_output = response.text
  session_id = response.session_id

  match = re.search(r"<final_file>(.*?)</final_file>", llm_output, re.DOTALL)

  if not match and session_id:
    print(" (incomplete, asking to finish and rename)...", end="", flush=True)
    with open("Scripts/prompts/ingest_recovery.md", "r") as f:
      recovery_prompt = f.read().strip()

    rec_response = run_gemini_cli_json(recovery_prompt, session_id=session_id, auto_edit=True)
    if rec_response.return_code == 0:
      llm_output = rec_response.text
      match = re.search(r"<final_file>(.*?)</final_file>", llm_output, re.DOTALL)
    else:
      print(f" error recovering (code {rec_response.return_code})")

  if match:
    new_path_str = match.group(1).strip()
    new_path = Path(new_path_str)

    if new_path.exists() and new_path.resolve() != filepath.resolve():
      if filepath.exists():
        filepath.unlink()
      print(f" done -> {new_path.name}")
      return new_path
    elif filepath.exists() and new_path.resolve() != filepath.resolve():
      new_path.parent.mkdir(parents=True, exist_ok=True)
      shutil.move(str(filepath), str(new_path))
      print(f" done -> {new_path.name}")
      return new_path
    elif filepath.exists() and new_path.resolve() == filepath.resolve():
      print(f" done -> {new_path.name}")
      return new_path

  print(" done (no rename detected).")
  return filepath
