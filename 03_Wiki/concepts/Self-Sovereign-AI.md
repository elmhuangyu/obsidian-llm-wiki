---
title: Self-Sovereign AI
type: concept
tags: [ai, privacy, security, local-llm, cryptography]
created: 2026-04-08
last_updated: 2026-04-08
---

# Self-Sovereign AI

**Self-Sovereign AI** (also referred to as **Local AI**, **Private AI**, or **Secure AI**) is an approach to artificial intelligence that prioritizes individual privacy, security, and autonomy. It stands in contrast to cloud-based AI systems, where user data is processed and stored on servers controlled by third-party corporations.

## Core Principles

- **Local Inference**: LLMs are executed on the user's own hardware (e.g., laptop, personal server) rather than remote APIs.
- **Privacy by Design**: Sensitive user data (notes, messages, files) never leaves the user's device.
- **Security through Isolation**: Use of sandboxing techniques (e.g., `bubblewrap`) to restrict the AI agent's access to the broader system.
- **Human-in-the-Loop Architecture**: High-risk actions (e.g., financial transactions, sending emails) require explicit human confirmation.
- **Data Sovereignty**: The user owns and controls the "world knowledge" and "personal knowledge" that the AI uses for context.

## Key Technologies

### Infrastructure
- **[[NixOS]]**: Often used for its reproducible and declarative system configuration, making it easier to manage complex AI stacks securely.
- **Local LLM Runners**: Tools like `llama-server` (via `llama.cpp`) or `ollama` enable high-performance local inference.
- **Hardware Acceleration**: High-end consumer GPUs (e.g., NVIDIA RTX 5090) or unified memory systems (e.g., Apple Silicon, AMD Ryzen AI Max) are required for low-latency inference of larger models.

### Security and Privacy
- **Sandboxing**: `bubblewrap` is a common tool for creating isolated environments (sbox) for AI processes.
- **ZK-APIs**: Zero-Knowledge APIs allow for making remote API calls (when local models are insufficient) without revealing the user's identity or linking requests.
- **Mixnets**: Use of mixnets (e.g., Nym) and Tor to hide IP addresses and metadata when the AI must access the internet.
- **Inference in TEEs**: Trusted Execution Environments (TEEs) provide hardware-based privacy for remote inference when local hardware is unavailable.

## Multi-Layer Defense

Self-Sovereign AI systems often employ a multi-layer defense strategy:
1.  **Local First**: Attempt to solve tasks using local, privacy-preserving models.
2.  **Input Sanitization**: Local models strip private data before passing a query to a remote system.
3.  **Privacy-Preserving Communication**: Use ZK-APIs and Mixnets for any remote calls.
4.  **Hardware Attestation**: Verifying that remote models are running in TEEs.

---

## related

- [[LLM-Wiki]]
- [[Vitalik-Buterin]]
- [[Personal-Knowledge-Management]]

## source

- [[2026-04-08-vitalik-local-private-secure-llm-setup]]
