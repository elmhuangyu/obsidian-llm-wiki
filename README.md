# Personal Knowledge Wiki

This is an Obsidian vault structured around the **compounding knowledge wiki** pattern inspired by [Andrej Karpathy's ideas](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). 

The core philosophy revolves around using LLMs to automatically structure, compress, and heavily interlink notes and clippings into a dense, Wikipedia-like format. Instead of isolated, chronological journal entries, knowledge is meant to "compound" over time as new information is iteratively absorbed into a growing set of evergreen topic pages.

## Technology Stack

The data ingestion and absorption processes are heavily automated using:
- **`uv`**: Fast Python dependency and environment management.
- **`gemini-cli`**: Used via our Python scripts to leverage LLM capabilities for text processing, categorization, and structuring.

## Workflows

We use a Makefile to automate the processing of new information into the wiki. The core commands are:

- **`make ingest`**: Processes incoming raw data (clippings, unsorted notes) by cleaning it up, adding necessary metadata, standardizing file names (e.g., `YYYY-MM-DD-title`), and moving it into `01_Raw/Entities`.
- **`make absorb`**: Analyzes the cleaned entities in the raw folder and integrates them into the main wiki structure (`03_Wiki/`). It clusters information, updates existing stubs or pages, and applies anti-thinning rules to keep the wiki content robust and compounded rather than fragmented.
- **Querying (`gemini-cli`)**: Use the Gemini CLI agent to ask exploratory questions directly against the synthesized knowledge in `03_Wiki/`. The LLM connects patterns across articles, answers complex questions, and can generate new concept notes from its synthesis.
