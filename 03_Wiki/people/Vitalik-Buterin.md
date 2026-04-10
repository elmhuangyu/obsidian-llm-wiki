---
title: Vitalik Buterin
type: person
tags: [ethereum, ai, privacy, security, nixos]
created: 2026-04-08
last_updated: 2026-04-08
---

# Vitalik Buterin

**Vitalik Buterin** is a co-founder of Ethereum and a prominent researcher in blockchain, cryptography, and decentralized systems. In 2026, he has become a vocal advocate for [[Self-Sovereign-AI]], emphasizing the need for local, private, and secure AI setups to counter the privacy risks of cloud-based AI.

## AI Philosophy

Buterin advocates for a "hardline" approach to AI privacy, security, and self-sovereignty. His vision for AI involves:
- **Local Inference**: All LLM inference should happen on the user's hardware.
- **Sandboxing**: AI agents should be strictly sandboxed (e.g., using `bubblewrap`) to prevent unauthorized file access or network calls.
- **Human-in-the-Loop**: A "human confirmation firewall" for sensitive actions like sending messages or blockchain transactions.
- **Contextual Knowledge**: Enhancing local LLMs with private "world knowledge" (e.g., local Wikipedia dumps) to reduce reliance on privacy-leaking internet searches.

## Personal AI Stack (2026)

As of April 2026, Buterin's local AI setup includes:
- **Operating System**: [[NixOS]] for reproducible and declarative configuration.
- **Hardware**: High-end laptops with NVIDIA 5090 GPUs or AMD Ryzen AI Max Pro (128 GB unified memory).
- **LLM Runner**: `llama-server` (from `llama.cpp`) with `llama-swap`.
- **AI Agent**: `pi` (shittycodingagent.ai), which facilitates tool use and skill integration.
- **Security**: `bubblewrap` for sandboxing and custom daemons for firewalled messaging (Signal, email).

---

## related

- [[Self-Sovereign-AI]]
- [[LLM-Wiki]]
- [[NixOS]]
- [[OpenClaw]]

## source

- [[2026-04-08-vitalik-local-private-secure-llm-setup]]
