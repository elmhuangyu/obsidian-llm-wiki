---
title: Obsidian
type: tool
tags: [knowledge-management, tools, markdown, wiki]
created: 2026-04-08
last_updated: 2026-04-08
---

# Obsidian

**Obsidian** is a powerful markdown-based [[Personal-Knowledge-Management|personal knowledge management (PKM)]] application that operates on a local collection of files. In the context of the [[LLM-Wiki|LLM Wiki pattern]], it serves as the "IDE" where the user explores, reads, and interacts with the knowledge base while an LLM agent serves as the "programmer" maintaining the wiki.

## Role in LLM Wiki Pattern

Obsidian's architecture and features make it particularly suited for the LLM Wiki pattern:

- **Local Markdown Files**: The knowledge base is a simple directory of markdown files, making it easily accessible to both the user and LLM agents.
- **Graph View**: A visual representation of the interconnections between wiki pages, showing the "shape" of the knowledge and identifying hubs or orphan pages.
- **Bi-directional Linking**: Essential for the interlinked structure that defines a compounding wiki.

## Recommended Plugins and Tools

Andrej Karpathy recommends several specific tools and settings for optimizing Obsidian as a wiki interface:

- **Web Clipper**: A browser extension used to quickly convert web articles into markdown format for ingest.
- **Dataview**: A plugin for running complex queries over page YAML frontmatter, allowing for dynamic tables and lists (e.g., summarizing sources or categories).
- **Marp**: A markdown-based slide deck format and plugin for generating presentations directly from wiki content.
- **Attachment Management**: Configuring Obsidian to download and store images locally (e.g., in a `raw/assets/` directory) ensuring the wiki remains self-contained and accessible even if external links break.

## Workflow Tips

- Use the "Download attachments for current file" hotkey to locally store images after clipping.
- Use the LLM to write and maintain YAML frontmatter, which can then be queried by Dataview.

---

## related

- [[LLM-Wiki]]
- [[Personal-Knowledge-Management]]

## source

- [[2026-04-08-karpathy-llm-compounding-wiki-pattern]]
