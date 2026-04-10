import json
import logging
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class GeminiResponse:
  text: str
  session_id: Optional[str]
  return_code: int


def run_gemini_cli_json(
  prompt: str, session_id: Optional[str] = None, auto_edit: bool = False
) -> GeminiResponse:
  cmd = ["gemini", "--output-format", "json"]
  if auto_edit:
    cmd.extend(["--approval-mode", "auto_edit"])
  if session_id:
    cmd.extend(["-r", session_id])
  if prompt:
    cmd.extend(["-p", prompt])

  try:
    result = subprocess.run(
      cmd,
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
