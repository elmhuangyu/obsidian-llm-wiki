---
title: LLM Wiki
type: pattern
tags: [llm, knowledge-management, wiki, rag]
created: 2026-04-08
last_updated: 2026-04-08
---

# LLM Wiki Pattern

The **LLM Wiki** is a pattern for building [[Personal-Knowledge-Management|personal knowledge bases]] where an LLM incrementally builds and maintains a persistent, structured, and interlinked collection of markdown files. This approach is designed to overcome the limitations of traditional [[RAG|Retrieval-Augmented Generation (RAG)]] systems, which often "rediscover" knowledge from scratch for every query.

## Core Philosophy

The primary difference between a standard RAG system and an LLM Wiki is the **compounding nature** of the latter. While RAG systems retrieve fragments of information at query time, an LLM Wiki compiles, synthesizes, and updates a persistent artifact.

- **Persistent Artifact**: The wiki is a "living" codebase of knowledge that survives between sessions.
- **Compounding Synthesis**: As new sources are added, the LLM integrates them into existing pages, updates summaries, and flags contradictions.
- **Maintenance by LLM**: The user acts as the "editor-in-chief" (sourcing, directing, and querying), while the LLM acts as the "maintainer" (summarizing, cross-referencing, and filing).

## Architecture

The LLM Wiki pattern consists of three distinct layers:

1.  **Raw Sources**: Immutable original documents (articles, papers, images, logs). This is the source of truth.
2.  **The Wiki**: A directory of LLM-generated markdown files (summaries, entity pages, concept pages). This layer is owned and updated by the LLM.
3.  **The Schema**: A configuration document (e.g., `AGENTS.md`, `CLAUDE.md`, or `SKILL.md`) that defines the wiki's structure, naming conventions, and operational workflows.

### Agentic Implementations

The [[Personal-Knowledge-Wiki]] is a specific agentic implementation of this pattern that utilizes a structured command set (`ingest`, `absorb`, `query`, etc.) and maintenance principles like **Anti-Cramming** and **Anti-Thinning** to ensure the wiki remains both comprehensive and focused.

### Implementation Strategies

- **Naming Conventions**: There are two primary schools of thought regarding entry naming:
    - **Auto-Increment**: A simpler `YYYY-MM-DD-increment` scheme popularized by [[Farza]] to avoid collisions and simplify sorting.
    - **Meaningful Filenames**: A more descriptive approach that improves human navigability but consumes more tokens. LLMs can be used to generate these titles during the ingestion process.
- **State Management**: To maintain efficiency and support incremental runs, the system tracks the state of processed files (using SHAs, hashes, and status fields) in a centralized state file (e.g., `state.json`). This ensures that only new or modified files are processed, saving both time and API costs.
- **Version Control (VCS)**: Integrating the wiki with a dedicated Git server allows for tracking automated changes and provides a critical safety net for rolling back problematic LLM updates.

### Vitalik's Implementation (2026)

In his 2026 implementation of the [[LLM-Wiki]] pattern, [[Vitalik-Buterin]] identified two critical components for enhancing local AI autonomy and privacy:

- **`AGENTS.md`**: A central configuration file that "teaches" the LLM about the wiki's contents, available tools, and personal preferences.
- **`world_knowledge/`**: A local directory containing massive dumps of public information (e.g., Wikipedia, technical documentation). This allows the LLM to answer factual queries locally, reducing privacy-leaking internet searches.

## Key Operations

- **Ingest**: Processing new sources. The LLM reads the source, discusses it with the user, and then updates relevant wiki pages (often 10-15 pages per source).
- **Query**: Asking questions against the wiki. The LLM uses the wiki and `world_knowledge` as its primary knowledge source, synthesizing answers and potentially filing those answers back into the wiki as new pages.
- **Skills**: Modular text files that teach the AI how to use external programs (e.g., search engines, messaging daemons) for specific tasks.
- **Lint**: Periodic health checks performed by the LLM to identify contradictions, stale claims, orphan pages, or missing cross-references.

## Structure and Indexing

Two central files facilitate navigation and history:

- **`index.md`**: A content-oriented catalog of all pages, organized by category, used by the LLM to locate relevant information without complex vector search.
- **`log.md`**: A chronological, append-only record of all wiki operations (ingests, queries, linting).

---

## related

- [[Obsidian]]
- [[RAG]]
- [[Memex]]
- [[Personal-Knowledge-Management]]

## source

- [[2026-04-08-karpathy-llm-compounding-wiki-pattern]]
