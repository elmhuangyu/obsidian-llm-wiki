---
---
type: note
author:
  - chaopeng
tags:
  - llm
  - wiki
  - automation
  - workflow
---

# My View of Karpathy's LLM Wiki

This note outlines my perspective on building an LLM-powered personal wiki, inspired by the ideas of Andrej Karpathy and Farza. My current system is already quite close to this vision, though my "absorb" step is currently manual and often leads to friction regarding note placement.

## References
- [Karpathy's LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Farza's Personal Wiki Skill Gist](https://gist.github.com/farzaa/c35ac0cfbeb957788650e36aabea836d)

---

## Core Workflow

### 1. Ingest
The goal of ingestion is to convert diverse data sources into a clean, machine-readable format (Markdown).

I use [Microsoft MarkItDown](https://github.com/microsoft/markitdown) for most standard formats.

**Supported Formats via MarkItDown:**
- **Office & PDF:** Standard documents. Picture-based PDFs require `markitdown-ocr` and an OpenAI-compatible LLM.
- **Images:** Requires LLM-based OCR.
- **YouTube:** 
  - ✅ With subtitles/captions: Straightforward extraction.
  - ❌ Without subtitles: Requires transcription (TBD).
- **Audio:** Currently limited to clips shorter than 20 seconds.

**LLM-Assisted Ingestion:**
For cases where MarkItDown is insufficient, **Gemini Flash** (via `yt-dlp` and `gemini-cli`) handles the rest. 

#### State Management
To ensure efficiency, the vault maintains a `state.json` (or YAML) file to track ingested files.
- **Tracking:** Filepath, SHA-1 hash, and ingestion status.
- **Incremental Runs:** Only process new or modified files to save tokens and time.

#### Entity Naming
Unlike Farza's approach (date + auto-increment), I prefer **meaningful filenames**. While this consumes more tokens, LLMs can be used to generate descriptive titles that make the vault more human-navigable.

### 2. Absorb
Absorption is the process of synthesizing raw data into the "Wiki" (knowledge base).

- **Consistency:** Like Ingest, Absorb will use a state file to track which notes need updating.
- **Modularity:** I plan to split absorption rules into specialized sub-agents or skills (e.g., `skills/absorb/...`).

### 3. Version Control (VCS)
Reliable versioning is critical for an automated system.
- **Infrastructure:** Moving from simple remote mounting to a dedicated [internal Git server](https://github.com/jkarlosb/git-server-docker).
- **Purpose:** Tracks automated changes and allows for easy rollback if an LLM-based update goes wrong.

---

## Folder Organization & Strategy

### /Clippings
I am refining the balance between raw web clips and "cleaned" notes.
- **Current Approach:** Use the Obsidian Web Clipper.
- **Refinement:** Use an LLM to clean up titles, remove ads, and normalize formatting. Gemini's recommendation is to run ingest to cleanup.

### /Raw/Journal
Daily occasional personal journals.
- **Strategy:** These are already well-formed Markdown. They stay in `/Raw` and act as primary sources for the Absorb step without needing a separate Ingest phase.

### /Trackers
Used for task management and checklists (e.g., annual tax returns).
- **Strategy:** These are functional logs rather than knowledge. They likely won't be "absorbed" into the Wiki but remain part of the vault as operational data.

### /Attachments
A centralized store for media (photos, document scans) related to the notes.

### /Archived
A permanent home for completed trackers or projects that are no longer active but should be preserved.

### /Templates
Standard schemas for Obsidian notes. 