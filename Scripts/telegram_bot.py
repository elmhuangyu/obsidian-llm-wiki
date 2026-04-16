import asyncio
import base64
import contextlib
import io
import logging
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import absorb as absorb_module
import ingest as ingest_module
import yaml
from gemini_cli import ApprovalMode, run_gemini_cli_json
from openai import OpenAI
from telegram import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
  Application,
  ApplicationBuilder,
  CallbackQueryHandler,
  CommandHandler,
  ContextTypes,
  MessageHandler,
  filters,
)

logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Quiet httpx logger to avoid leaking the bot token in request URLs
logging.getLogger("httpx").setLevel(logging.WARNING)

CONFIG_PATH = os.path.expanduser("~/.config/tg_note/config.yaml")
NOTE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Config:
  bot_token: str
  chat_id: int
  log_level: str = "INFO"
  # ASR settings
  asr_base_url: str = "http://localhost:8001/v1"
  asr_api_key: str = "llama-is-awesome"
  asr_model: str = "whisper"
  asr_voice_lang: str = "Chinese or English"
  asr_output_lang: str = "English"
  gemini_cli_asr: bool = False
  gemini_cli_asr_model: str = "flash"

  @classmethod
  def from_file(cls, path: str) -> "Config":
    with open(path, "r") as f:
      raw = yaml.safe_load(f)
    bot_token = raw.get("bot_token")
    chat_id = raw.get("chat_id")
    if not bot_token:
      raise ValueError("bot_token missing from config")
    if chat_id is None:
      raise ValueError("chat_id missing from config")
    return cls(
      bot_token=bot_token,
      chat_id=int(chat_id),
      log_level=(raw.get("log_level") or "INFO").upper(),
      asr_base_url=raw.get("base_url", "http://localhost:8001/v1"),
      asr_api_key=raw.get("api_key", "llama-is-awesome"),
      asr_model=raw.get("model", "gemma-4-e4b"),
      asr_voice_lang=raw.get("voice_lang", "Chinese or English"),
      asr_output_lang=raw.get("output_lang", "Chinese or English same with the language in audio"),
      gemini_cli_asr=raw.get("gemini_cli_asr", False),
      gemini_cli_asr_model=raw.get("gemini_cli_asr_model", "flash"),
    )


try:
  config = Config.from_file(CONFIG_PATH)
  logging.getLogger().setLevel(config.log_level)
except Exception as e:
  logging.error(f"Failed to read config from {CONFIG_PATH}: {e}")
  exit(1)

# Authorized filter for reuse across handlers
AUTH_FILTER = filters.Chat(chat_id=config.chat_id)

# Load ASR prompt template once at startup
_ASR_PROMPT_PATH = NOTE_DIR / "Scripts" / "prompts" / "asr_prompt.md"
try:
  ASR_PROMPT_TEMPLATE = _ASR_PROMPT_PATH.read_text().strip()
except Exception as e:
  logging.warning(f"Could not load ASR prompt from {_ASR_PROMPT_PATH}: {e}")
  ASR_PROMPT_TEMPLATE = (
    "Transcribe the audio in {voice_lang} to {output_lang}. Output transcription only."
  )

# Load agent prompt template once at startup
_AGENT_PROMPT_PATH = NOTE_DIR / "Scripts" / "prompts" / "agent_prompt.md"
try:
  AGENT_PROMPT_TEMPLATE = _AGENT_PROMPT_PATH.read_text().strip()
except Exception as e:
  logging.warning(f"Could not load agent prompt from {_AGENT_PROMPT_PATH}: {e}")
  AGENT_PROMPT_TEMPLATE = "{user_request}"


async def is_obsidian_running() -> bool:
  """Check if Obsidian is currently running."""
  cmd = "ps aux | grep '[e]lectron /usr/lib/obsidian/app.asar'"
  process = await asyncio.create_subprocess_shell(
    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
  )
  await process.communicate()
  return process.returncode == 0


async def ensure_obsidian_running(reply_fn) -> bool:
  """Ensure Obsidian is running, starting it if necessary.
  reply_fn is an async callable that sends a text message to the user.
  """
  if not await is_obsidian_running():
    await reply_fn("Obsidian is not running. Starting it via systemctl...")
    cmd = "systemctl --user start obsidian"
    process = await asyncio.create_subprocess_shell(
      cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    if process.returncode != 0:
      await reply_fn("Failed to start Obsidian via systemctl.")
      return False
    # Brief wait to let the process spin up
    await asyncio.sleep(2)
    if not await is_obsidian_running():
      await reply_fn("Obsidian still not running after start attempt.")
      return False
  return True


async def run_command_in_note_dir(cmd_list):
  """Run a shell command asynchronously in the NOTE_DIR."""
  process = await asyncio.create_subprocess_exec(
    *cmd_list, cwd=NOTE_DIR, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
  )
  stdout, stderr = await process.communicate()
  return stdout.decode(), stderr.decode()


async def process_quick_note(update: Update, context: ContextTypes.DEFAULT_TYPE, note_text: str):
  msg = await update.message.reply_text("Processing quick note...")
  try:
    prompt = f"add users note to 00_Home/Inbox.md, user note is: {note_text}"
    response = await asyncio.to_thread(
      run_gemini_cli_json, prompt, approval_mode=ApprovalMode.auto_edit
    )
    # response.text contains the output/response or fallback to stdout
    output = response.text if response.text else f"Return Code: {response.return_code}"
    await msg.edit_text(f"{output[:3500]}", parse_mode=ParseMode.MARKDOWN)
  except Exception as e:
    await msg.edit_text(f"Error handling quick note: {e}")


async def quick_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update.message.reply_text):
    return

  text = " ".join(context.args) if context.args else ""

  if not text:
    context.user_data["awaiting_quick_note"] = True
    await update.message.reply_text("please add your quick note")
    return

  await process_quick_note(update, context, text)


def run_ingest_sync() -> str:
  f = io.StringIO()
  with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
    try:
      original_cwd = os.getcwd()
      os.chdir(NOTE_DIR)
      try:
        ingest_module.run()
      finally:
        os.chdir(original_cwd)
    except Exception as e:
      print(f"Error: {e}")
  return f.getvalue()


def run_absorb_sync() -> str:
  f = io.StringIO()
  with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
    try:
      original_cwd = os.getcwd()
      os.chdir(NOTE_DIR)
      try:
        absorb_module.run()
      finally:
        os.chdir(original_cwd)
    except Exception as e:
      print(f"Error: {e}")
  return f.getvalue()


async def ingest(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update.message.reply_text):
    return

  msg = await update.message.reply_text("Running ingest...")
  try:
    output = await asyncio.to_thread(run_ingest_sync)
    if not output.strip():
      output = "No output."
    await msg.edit_text(
      f"ingest finished.\nOutput:\n```\n{output[:2000]}\n```", parse_mode=ParseMode.MARKDOWN
    )
  except Exception as e:
    await msg.edit_text(f"Error running ingest: {e}")


async def absorb(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update.message.reply_text):
    return

  msg = await update.message.reply_text("Running absorb...")
  try:
    output = await asyncio.to_thread(run_absorb_sync)
    if not output.strip():
      output = "No output."
    await msg.edit_text(
      f"absorb finished.\nOutput:\n```\n{output[:2000]}\n```", parse_mode=ParseMode.MARKDOWN
    )
  except Exception as e:
    await msg.edit_text(f"Error running absorb: {e}")


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update.message.reply_text):
    return

  try:
    stdout, stderr = await run_command_in_note_dir(["obsidian", "tasks", "todo"])
    output = stdout if stdout else stderr
    await update.message.reply_text(f"Tasks:\n{output[:3500]}")
  except Exception as e:
    await update.message.reply_text(f"Error fetching tasks: {e}")


async def call_gemini_agent(msg, user_request: str):
  """Call the gemini agent for a general request and update the given message with the result.

  The request is formatted using the agent prompt template which instructs the agent
  to classify the input as either a wiki query or a note to add to the inbox.
  """
  prompt = AGENT_PROMPT_TEMPLATE.format(user_request=user_request)
  try:
    response = await asyncio.to_thread(
      run_gemini_cli_json, prompt, approval_mode=ApprovalMode.auto_edit
    )
    output = response.text if response.text else f"Return Code: {response.return_code}"
    await msg.edit_text(f"{output[:3500]}", parse_mode=ParseMode.MARKDOWN)
  except Exception as e:
    await msg.edit_text(f"Error running agent: {e}")


async def default_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update.message.reply_text):
    return

  text = update.message.text

  if context.user_data.get("awaiting_quick_note"):
    context.user_data["awaiting_quick_note"] = False
    await process_quick_note(update, context, text)
    return

  msg = await update.message.reply_text("Calling gemini agent...")
  await call_gemini_agent(msg, text)


def transcribe_sync(file_path: str) -> str:
  """Blocking ASR call — run via asyncio.to_thread."""
  if config.gemini_cli_asr:
    prompt = ASR_PROMPT_TEMPLATE.format(
      voice_lang=config.asr_voice_lang, output_lang=config.asr_output_lang
    )
    try:
      rel_path = os.path.relpath(file_path, NOTE_DIR)
    except ValueError:
      rel_path = file_path
    full_prompt = f"@{rel_path} {prompt}"
    response = run_gemini_cli_json(full_prompt, model=config.gemini_cli_asr_model)
    return response.text.strip()

  # Convert OGG (Telegram voice) to 16kHz mono PCM WAV that llama-server accepts
  wav_path = file_path.replace(".ogg", ".wav")
  subprocess.run(
    ["ffmpeg", "-y", "-i", file_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_path],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
  )
  try:
    client = OpenAI(base_url=config.asr_base_url, api_key=config.asr_api_key)
    with open(wav_path, "rb") as f:
      audio_b64 = base64.b64encode(f.read()).decode("utf-8")
    prompt = ASR_PROMPT_TEMPLATE.format(
      voice_lang=config.asr_voice_lang, output_lang=config.asr_output_lang
    )
    response = client.chat.completions.create(
      model=config.asr_model,
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": prompt},
            {"type": "input_audio", "input_audio": {"data": audio_b64, "format": "wav"}},
          ],
        }
      ],
    )
    return response.choices[0].message.content.strip()
  finally:
    if os.path.exists(wav_path):
      os.unlink(wav_path)


async def voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Transcribe an incoming voice message and ask for confirmation."""
  logging.info("Received voice message")
  msg = await update.message.reply_text("Transcribing voice message...")
  tmp_path = None
  try:
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    # Ensure tmp dir exists in current project root
    tmp_dir = NOTE_DIR / "tmp"
    tmp_dir.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".ogg", dir=tmp_dir, delete=False) as tmp:
      tmp_path = tmp.name
    await voice_file.download_to_drive(tmp_path)
    text = await asyncio.to_thread(transcribe_sync, tmp_path)

    context.user_data["pending_voice_text"] = text
    keyboard = [
      [
        InlineKeyboardButton("✅ Yes", callback_data="voice_yes"),
        InlineKeyboardButton("❌ No", callback_data="voice_no"),
      ]
    ]
    await msg.edit_text(
      f"Are you saying?\n\n_{text}_",
      parse_mode=ParseMode.MARKDOWN,
      reply_markup=InlineKeyboardMarkup(keyboard),
    )
  except Exception as e:
    await msg.edit_text(f"Error transcribing voice message: {e}")
  finally:
    if tmp_path and os.path.exists(tmp_path):
      os.unlink(tmp_path)


async def voice_confirmation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Handle Yes / No confirmation after ASR transcription."""
  query = update.callback_query
  await query.answer()

  if query.data == "voice_no":
    context.user_data.pop("pending_voice_text", None)
    await query.edit_message_text("Voice message cancelled.")
    return

  # voice_yes — treat transcribed text as a normal agent request
  text = context.user_data.get("pending_voice_text", "")
  if not text:
    await query.edit_message_text("No transcribed text found.")
    return

  # Remove buttons from the "You are asking" message
  await query.edit_message_text(f"You are asking:\n\n_{text}_", parse_mode=ParseMode.MARKDOWN)

  if not await ensure_obsidian_running(query.message.reply_text):
    return

  context.user_data.pop("pending_voice_text", None)

  msg = await query.message.reply_text("Calling gemini agent...")
  await call_gemini_agent(msg, text)


async def unsupported_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Reply to unsupported message types."""
  await update.message.reply_text("Message type not supported")


async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Log unauthorized access attempts."""
  chat_id = update.effective_chat.id if update.effective_chat else "Unknown"
  logging.warning(f"Unauthorized access attempt from chat ID {chat_id}")


async def post_init(application: Application):
  """Auto-register bot commands in the Telegram UI."""
  commands = [
    BotCommand("quick_note", "Add a quick note"),
    BotCommand("ingest", "Run ingest"),
    BotCommand("absorb", "Run absorb"),
    BotCommand("tasks", "List obsidian tasks todo"),
  ]
  await application.bot.set_my_commands(commands)


if __name__ == "__main__":
  application = ApplicationBuilder().token(config.bot_token).post_init(post_init).build()

  # Apply AUTH_FILTER to all functional handlers
  application.add_handler(CommandHandler("quick_note", quick_note, filters=AUTH_FILTER))
  application.add_handler(CommandHandler("ingest", ingest, filters=AUTH_FILTER))
  application.add_handler(CommandHandler("absorb", absorb, filters=AUTH_FILTER))
  application.add_handler(CommandHandler("tasks", tasks, filters=AUTH_FILTER))

  # Handle all other text messages from the authorized user
  application.add_handler(
    MessageHandler(filters.TEXT & (~filters.COMMAND) & AUTH_FILTER, default_message)
  )

  # Handle voice messages from the authorized user
  application.add_handler(MessageHandler(filters.VOICE & AUTH_FILTER, voice_message))

  # Handle Yes / No callback from voice confirmation keyboard
  application.add_handler(CallbackQueryHandler(voice_confirmation_callback, pattern="^voice_"))

  # Reply to any other unsupported message type from the authorized user
  application.add_handler(
    MessageHandler(
      (~filters.TEXT & ~filters.COMMAND & ~filters.VOICE) & AUTH_FILTER,
      unsupported_message,
    )
  )

  # Catch and log all updates not from the authorized chat
  application.add_handler(MessageHandler(~AUTH_FILTER, unauthorized), group=1)

  logging.info("Bot is starting...")
  application.run_polling()
