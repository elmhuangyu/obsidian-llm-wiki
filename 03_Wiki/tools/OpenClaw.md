---
title: OpenClaw
type: tool
tags: [ai-agents, open-source, security, llm]
created: 2026-04-08
last_updated: 2026-04-08
---

# OpenClaw

**OpenClaw** is a fast-growing open-source project designed for building AI agents that can use tools and perform complex, multi-step tasks. In early 2026, it became one of the most popular frameworks for transitioning from simple LLM chatbots to autonomous agents.

## Features and Growth

- **Agentic Workflow**: Focuses on task completion rather than just text generation.
- **Tool Integration**: Allows LLMs to use external tools (API calls, web searches, etc.).
- **Popularity**: Noted as one of the fastest-growing repositories on GitHub in 2026.

## Security Criticism

Despite its popularity, OpenClaw has faced significant criticism from security researchers and advocates for [[Self-Sovereign-AI]] like [[Vitalik-Buterin]]:
- **Lack of Human Confirmation**: Agents can modify critical system settings or prompts without user approval.
- **Vulnerability to Malicious Input**: Can be "hijacked" via malicious web pages (e.g., a prompt injection leading to remote code execution).
- **Data Exfiltration**: Silent network calls in some "skills" can leak sensitive user data to external servers.

These vulnerabilities have highlighted the importance of **sandboxing** and **human confirmation firewalls** in agent design.

---

## related

- [[Self-Sovereign-AI]]
- [[Vitalik-Buterin]]
- [[LLM-Wiki]]

## source

- [[2026-04-08-vitalik-local-private-secure-llm-setup]]
