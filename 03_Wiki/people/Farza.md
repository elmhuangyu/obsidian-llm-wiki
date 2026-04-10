---
title: Farza
type: person
tags: [pkm, automation, engineering]
created: 2026-04-08
last_updated: 2026-04-08
---

# Farza

**Farza** is an engineer and developer known for his work on agentic workflows and personal knowledge management systems. He is the creator of the **Wiki Skill**, a specialized set of instructions for LLM agents (specifically [[Claude-Code]]) to maintain a [[Personal-Knowledge-Wiki]].

## Philosophy and Contributions

Farza's approach to knowledge management emphasizes the role of the AI as a **writer** rather than a filing clerk. His work has significantly influenced the development of [[LLM-Wiki]] patterns by formalizing the "absorb" and "query" steps.

### The Wiki Skill

Farza's Wiki Skill defines a methodology for compounding knowledge:
- **Writer vs. Clerk**: The AI should synthesize understanding and "map a mind" instead of just organizing files.
- **Auto-Increment Naming**: His original implementation used a `YYYY-MM-DD-increment` naming scheme for raw entries to avoid naming collisions and simplify ordering.
- **State Management**: Using state files to track which entries have been processed to ensure efficiency and incremental updates.

### Influence on Implementations

His ideas often serve as a baseline for other implementations, though users sometimes diverge from his specific conventions—such as opting for **meaningful filenames** over his auto-increment scheme to improve human navigability.

---

## related

- [[Personal-Knowledge-Wiki]]
- [[Claude-Code]]
- [[LLM-Wiki]]

## source

- [[2026-04-08-personal-knowledge-wiki-skill-definition]]
- [[2026-04-08-karpathy-llm-compounding-wiki-pattern]]
