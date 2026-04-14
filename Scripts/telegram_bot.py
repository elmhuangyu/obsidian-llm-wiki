import asyncio
import logging
import os
from pathlib import Path

import yaml
from gemini_cli import run_gemini_cli_json
from telegram import BotCommand, Update
from telegram.constants import ParseMode
from telegram.ext import (
  Application,
  ApplicationBuilder,
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

# Load config
try:
  with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)
  bot_token = config.get("bot_token")
  # Ensure chat_id is present and convert to int for filters.Chat
  authorized_chat_id = config.get("chat_id")
  if authorized_chat_id is None:
    raise ValueError("chat_id missing from config")
  authorized_chat_id = int(authorized_chat_id)
except Exception as e:
  logging.error(f"Failed to read config from {CONFIG_PATH}: {e}")
  exit(1)

# Authorized filter for reuse across handlers
AUTH_FILTER = filters.Chat(chat_id=authorized_chat_id)


async def is_obsidian_running() -> bool:
  """Check if Obsidian is currently running."""
  cmd = "ps aux | grep '[e]lectron /usr/lib/obsidian/app.asar'"
  process = await asyncio.create_subprocess_shell(
    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
  )
  await process.communicate()
  return process.returncode == 0


async def ensure_obsidian_running(update: Update) -> bool:
  """Ensure Obsidian is running, starting it if necessary."""
  if not await is_obsidian_running():
    await update.message.reply_text("Obsidian is not running. Starting it via systemctl...")
    cmd = "systemctl start --user obsidian"
    process = await asyncio.create_subprocess_shell(
      cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    if process.returncode != 0:
      await update.message.reply_text("Failed to start Obsidian via systemctl.")
      return False
    # Brief wait to let the process spin up
    await asyncio.sleep(2)
    if not await is_obsidian_running():
      await update.message.reply_text("Obsidian still not running after start attempt.")
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
    response = await asyncio.to_thread(run_gemini_cli_json, prompt, None, True)
    # response.text contains the output/response or fallback to stdout
    output = response.text if response.text else f"Return Code: {response.return_code}"
    await msg.edit_text(f"{output[:3500]}", parse_mode=ParseMode.MARKDOWN)
  except Exception as e:
    await msg.edit_text(f"Error handling quick note: {e}")


async def quick_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update):
    return

  text = " ".join(context.args) if context.args else ""

  if not text:
    context.user_data["awaiting_quick_note"] = True
    await update.message.reply_text("please add your quick note")
    return

  await process_quick_note(update, context, text)


async def ingest(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update):
    return

  msg = await update.message.reply_text("Running make ingest...")
  try:
    stdout, stderr = await run_command_in_note_dir(["make", "ingest"])
    output = stdout if stdout else stderr
    await msg.edit_text(
      f"make ingest finished.\nOutput:\n```\n{output[:2000]}\n```", parse_mode=ParseMode.MARKDOWN
    )
  except Exception as e:
    await msg.edit_text(f"Error running ingest: {e}")


async def absorb(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update):
    return

  msg = await update.message.reply_text("Running make absorb...")
  try:
    stdout, stderr = await run_command_in_note_dir(["make", "absorb"])
    output = stdout if stdout else stderr
    await msg.edit_text(
      f"make absorb finished.\nOutput:\n```\n{output[:2000]}\n```", parse_mode=ParseMode.MARKDOWN
    )
  except Exception as e:
    await msg.edit_text(f"Error running absorb: {e}")


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update):
    return

  try:
    stdout, stderr = await run_command_in_note_dir(["obsidian", "tasks", "todo"])
    output = stdout if stdout else stderr
    await update.message.reply_text(f"Tasks:\n{output[:3500]}")
  except Exception as e:
    await update.message.reply_text(f"Error fetching tasks: {e}")


async def default_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not await ensure_obsidian_running(update):
    return

  text = update.message.text

  if context.user_data.get("awaiting_quick_note"):
    context.user_data["awaiting_quick_note"] = False
    await process_quick_note(update, context, text)
    return

  msg = await update.message.reply_text("Calling gemini agent...")
  try:
    response = await asyncio.to_thread(run_gemini_cli_json, text, None, False)
    output = response.text if response.text else f"Return Code: {response.return_code}"
    await msg.edit_text(f"{output[:3500]}", parse_mode=ParseMode.MARKDOWN)
  except Exception as e:
    await msg.edit_text(f"Error running agent: {e}")


async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE):
  """Log unauthorized access attempts."""
  chat_id = update.effective_chat.id if update.effective_chat else "Unknown"
  logging.warning(f"Unauthorized access attempt from chat ID {chat_id}")


async def post_init(application: Application):
  """Auto-register bot commands in the Telegram UI."""
  commands = [
    BotCommand("quick_note", "Add a quick note"),
    BotCommand("ingest", "Run make ingest"),
    BotCommand("absorb", "Run make absorb"),
    BotCommand("tasks", "List obsidian tasks todo"),
  ]
  await application.bot.set_my_commands(commands)


if __name__ == "__main__":
  if not bot_token or not authorized_chat_id:
    logging.error("bot_token or chat_id missing from config")
    exit(1)

  application = ApplicationBuilder().token(bot_token).post_init(post_init).build()

  # Apply AUTH_FILTER to all functional handlers
  application.add_handler(CommandHandler("quick_note", quick_note, filters=AUTH_FILTER))
  application.add_handler(CommandHandler("ingest", ingest, filters=AUTH_FILTER))
  application.add_handler(CommandHandler("absorb", absorb, filters=AUTH_FILTER))
  application.add_handler(CommandHandler("tasks", tasks, filters=AUTH_FILTER))

  # Handle all other text messages from the authorized user
  application.add_handler(
    MessageHandler(filters.TEXT & (~filters.COMMAND) & AUTH_FILTER, default_message)
  )

  # Catch and log all updates not from the authorized chat
  application.add_handler(MessageHandler(~AUTH_FILTER, unauthorized), group=1)

  logging.info("Bot is starting...")
  application.run_polling()
