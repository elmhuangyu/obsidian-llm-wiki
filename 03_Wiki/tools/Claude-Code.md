---
title: Claude Code
type: tool
tags: [ai, cli, anthropic, coding, automation]
created: 2026-04-08
last_updated: 2026-04-08
---

# Claude Code

**Claude Code** is a command-line application from Anthropic that provides an agentic environment for interacting with large language models (LLMs) to perform complex tasks, including software development and personal knowledge management. It allows users to execute shell commands, read and write files, and extend its functionality through specialized **skills**.

## Skill System

Claude Code supports modular extensions called skills, which are defined in `.claude/skills/` directories. These skills "teach" the agent how to perform specific workflows or use external tools by providing high-level instructions and mapping commands to underlying processes.

## Role in Personal Knowledge Wiki

In the context of the [[Personal-Knowledge-Wiki]] pattern, Claude Code serves as the primary execution environment. A specific **Wiki Skill** (`SKILL.md`) defines the commands (`/wiki ingest`, `/wiki absorb`, etc.) and operational logic used to maintain a persistent, interlinked knowledge base.

### The Wiki Skill

Developed by [[Farza]], the **Wiki Skill** is a specialized instruction set designed for Claude Code to perform the `absorb` and `query` operations. It provides a structured workflow for synthesizing information from raw entries into a compounding, thematic knowledge base, emphasizing the role of the agent as a writer rather than a filing clerk.

## related

- [[Personal-Knowledge-Wiki]]
- [[LLM-Wiki]]
- [[Obsidian]]
- [[OpenClaw]]

## source

- [[2026-04-08-personal-knowledge-wiki-skill-definition]]
