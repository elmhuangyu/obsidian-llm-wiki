# Personal Knowledge Wiki

This is an Obsidian vault structured around the **compounding knowledge wiki** pattern inspired by [Andrej Karpathy's ideas](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). 

The core philosophy revolves around using LLMs to automatically structure, compress, and heavily interlink notes and clippings into a dense, Wikipedia-like format. Instead of isolated, chronological journal entries, knowledge is meant to "compound" over time as new information is iteratively absorbed into a growing set of evergreen topic pages.

## Technology Stack

The data ingestion and absorption processes are heavily automated using:
- **`uv`**: Fast Python dependency and environment management.
- **`gemini-cli`**: Used via our Python scripts to leverage LLM capabilities for text processing, categorization, and structuring.

## Installation

```bash
make install
```

## Workflows

We use a Makefile to automate the processing of new information into the wiki. The core commands are:

- **`make ingest`**: Processes incoming raw data (clippings, unsorted notes) by cleaning it up, adding necessary metadata, standardizing file names (e.g., `YYYY-MM-DD-title`), and moving it into `01_Raw/Entities`.
- **`make absorb`**: Analyzes the cleaned entities in the raw folder and integrates them into the main wiki structure (`03_Wiki/`). It clusters information, updates existing stubs or pages, and applies anti-thinning rules to keep the wiki content robust and compounded rather than fragmented.
- **Querying (`gemini-cli`)**: Use the Gemini CLI agent to ask exploratory questions directly against the synthesized knowledge in `03_Wiki/`. The LLM connects patterns across articles, answers complex questions, and can generate new concept notes from its synthesis.

## Optional: Telegram Bot

A Telegram bot is available to interact with the wiki remotely. It allows you to add quick notes, run the `ingest` and `absorb` processes, and query the wiki.

**Installation Steps:**

1. Review the bot script at `Scripts/telegram_bot.py`.
2. Configure the bot by creating a configuration file at `~/.config/tg_note/config.yaml` containing your Telegram token and authorized chat ID:
   ```yaml
   bot_token: "YOUR_TELEGRAM_BOT_TOKEN"
   chat_id: YOUR_AUTHORIZED_CHAT_ID
   ```
3. A systemd service file is provided to keep the bot running in the background. Install and enable it using the provided service definition in `Scripts/services/`:
   ```bash
   mkdir -p ~/.config/systemd/user/
   cp Scripts/services/* ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable --now obsidian.service
   systemctl --user enable --now note-telegram.service
   ```
