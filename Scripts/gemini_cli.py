import json
import logging
import os
import subprocess
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Optional

NOTE_DIR = Path(__file__).resolve().parent.parent


class ApprovalMode(StrEnum):
  plan = auto()
  default = auto()
  auto_edit = auto()
  yolo = auto()


class GeminiModel(StrEnum):
  pro = "gemini-3.1-pro-preview"
  flash = "gemini-3-flash-preview"
  flash_lite = "gemini-3.1-flash-lite-preview"
  gemini_25_pro = "gemini-2.5-pro"
  gemini_25_flash = "gemini-2.5-flash"
  gemini_25_flash_lite = "gemini-2.5-flash-lite"


@dataclass
class GeminiResponse:
  text: str
  session_id: Optional[str]
  return_code: int


def run_gemini_cli_json(prompt: str, **kwargs) -> GeminiResponse:
  """Run the Gemini CLI in JSON output mode and return a structured response.

  Invokes ``~/.npm/bin/gemini`` with ``--output-format json`` inside NOTE_DIR,
  parses the JSON output, and surfaces the result as a :class:`GeminiResponse`.

  Args:
    prompt: The prompt string to pass via ``-p``.
    **kwargs: Optional keyword arguments:

      - **session_id** (*str | None*): Resume an existing conversation by its
        session ID (passed as ``-r <id>``). Defaults to ``None``.
      - **approval_mode** (:class:`ApprovalMode`): Controls how the CLI handles
        tool-use approvals. Defaults to :attr:`ApprovalMode.default`.
      - **model** (:class:`GeminiModel` | *str | None*): The model to use.
        Defaults to ``None``.

  Returns:
    A :class:`GeminiResponse` with:

    - ``text``: The ``response`` field from the JSON payload, or raw stdout on
      parse failure.
    - ``session_id``: The ``session_id`` returned by the CLI, if any.
    - ``return_code``: The process exit code (``127`` if the binary is missing).
  """
  session_id: Optional[str] = kwargs.get("session_id")
  approval_mode: ApprovalMode = kwargs.get("approval_mode", ApprovalMode.default)
  model: Optional[GeminiModel | str] = kwargs.get("model")
  gemini_bin = os.path.expanduser("~/.npm/bin/gemini")
  cmd = [gemini_bin, "--policy", ".gemini/policies/obsidian.toml", "--output-format", "json"]
  cmd.extend(["--approval-mode", str(approval_mode)])
  if model:
    cmd.extend(["-m", str(model)])
  if session_id:
    cmd.extend(["-r", session_id])
  if prompt:
    cmd.extend(["-p", prompt])

  try:
    result = subprocess.run(
      cmd,
      cwd=NOTE_DIR,
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

    output_text = ""
    returned_session_id = None

    try:
      data = json.loads(result.stdout)
      if "response" in data:
        output_text = data["response"]
      else:
        output_text = result.stdout
      returned_session_id = data.get("session_id")
    except Exception:
      output_text = result.stdout

    return GeminiResponse(
      text=output_text, session_id=returned_session_id, return_code=result.returncode
    )
  except FileNotFoundError:
    logging.error("gemini CLI not found.")
    return GeminiResponse(text="", session_id=None, return_code=127)
  except Exception as e:
    logging.error(f"Error running gemini: {e}")
    return GeminiResponse(text="", session_id=None, return_code=1)
