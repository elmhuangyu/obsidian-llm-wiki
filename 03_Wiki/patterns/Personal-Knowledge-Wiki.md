---
title: Personal Knowledge Wiki
type: pattern
tags: [pkm, automation, knowledge-management, markdown, llm]
created: 2026-04-08
last_updated: 2026-04-08
---

# Personal Knowledge Wiki

The **Personal Knowledge Wiki** is an agentic implementation of the [[LLM-Wiki]] pattern designed to compile fragmented personal data—such as journals, notes, and messages—into a structured, interlinked knowledge base. Unlike traditional filing systems, it positions the maintainer (the LLM) as a **writer** whose primary task is to synthesize understanding rather than mechanically categorize information.

## Core Principles

The Personal Knowledge Wiki is governed by two balancing maintenance rules:

- **Anti-Cramming Rule**: Discourages the bloating of existing articles. If an existing article begins to accumulate excessive information on a sub-topic (typically defined as adding a third paragraph to that sub-topic), the sub-topic is promoted to its own dedicated page.
- **Anti-Thinning Rule**: Discourages the creation of "stub" pages with minimal content. A new article should only be created if it can contain at least three non-obvious insights or meaningful sentences. Otherwise, the information is linked back to a parent page or a general index.

## Operational Workflow

The pattern defines a standard set of commands for managing the wiki's lifecycle:

- **`ingest`**: Mechanically converts various source formats (e.g., iMessage, Apple Notes, Obsidian vaults, Day One JSON, email, and Twitter archives) into a standardized raw markdown format.
- **`absorb`**: The core compilation step where the LLM processes raw entries chronologically, synthesizes their meaning, and updates the wiki articles. To manage complexity, this process can be modularized into specialized sub-agents or skills (e.g., `skills/absorb/...`) that handle specific data types or themes.
- **`query`**: A read-only operation where the LLM answers questions about the subject's life by navigating the wiki's synthesized articles rather than searching raw logs.
- **`cleanup`**: An audit and enrichment phase where parallel agents restructure diary-driven articles into narrative, theme-driven formats.
- **`breakdown`**: A proactive expansion step that identifies concrete entities and themes (people, places, concepts) that deserve their own pages based on reference density.
- **`reorganize`**: A structural review to merge, split, or rename articles and directories as the knowledge base evolves.

## Directory Structure

A Personal Knowledge Wiki project typically adheres to a tiered directory structure, often expanding on the following categories:

1.  **`01_Raw/`**: Contains immutable original sources and standardized markdown entries.
    - **`Journal/`**: Daily logs that serve as primary sources for the `absorb` step.
    - **`Entities/`**: Specific reports or documents generated from external data.
2.  **`03_Wiki/`**: The synthesized knowledge base, containing the master index (`_index.md`) and thematic subdirectories (e.g., `people/`, `projects/`, `concepts/`).
3.  **`Clippings/`**: A staging area for raw web content. LLMs are often used to "clean" these clips—removing ads, normalizing titles, and fixing formatting—before they move to the ingestion phase.
4.  **`Trackers/`**: Functional data (e.g., task lists, tax logs) that remain in the vault but are typically not "absorbed" into the persistent knowledge base.
5.  **`Attachments/`**: Central store for media (photos, scans) linked to wiki articles.
6.  **`Archived/`**: A permanent home for completed trackers or projects that should be preserved but are no longer active.
7.  **`Templates/`**: Standard schemas for creating consistent note types.

## Implementation Standards

The wiki emphasizes a "Wikipedia-style" tone—neutral, factual, and concise—where emotional weight is carried by direct quotes from the source material rather than the AI's editorial voice. Articles are organized by theme rather than chronology, moving away from "event logs" toward conceptual maps of a mind.

## Maintenance and Safety

As an automated, LLM-driven system, the Personal Knowledge Wiki requires robust maintenance and safety protocols to ensure data integrity.

- **Version Control (VCS)**: It is recommended to host the wiki on a dedicated **internal Git server**. This provides a complete history of all automated changes made by the LLM, enabling easy audits and rapid rollbacks if an update introduces errors or unwanted changes.
- **State Tracking**: The system uses a centralized state file (e.g., `state.json`) to track the status of files in the `01_Raw/` directory. This ensures incremental processing, preventing redundant token usage and minimizing the risk of duplicate entries.
- **Periodic Audits**: In addition to the `cleanup` and `reorganize` commands, regular manual reviews by the user (the "Editor-in-Chief") are essential to ensure the synthesized knowledge remains accurate and aligned with the user's personal perspective.

---

## related

- [[LLM-Wiki]]
- [[Personal-Knowledge-Management]]
- [[Claude-Code]]
- [[Obsidian]]

## source

- [[2026-04-08-personal-knowledge-wiki-skill-definition]]
- [[2026-04-08-karpathy-llm-compounding-wiki-pattern]]
- [[My view of Karpathy LLM Wiki]]
