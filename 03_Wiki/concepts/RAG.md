---
title: RAG
type: concept
tags: [artificial-intelligence, llm, information-retrieval]
created: 2026-04-08
last_updated: 2026-04-08
---

# Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** is an AI technique where a model retrieves relevant documents or information from an external database at query time to augment its generated response.

## Limitations in PKM Context

Andrej Karpathy notes several limitations of traditional RAG systems in the context of persistent knowledge management:

- **Rediscovery**: LLMs often rediscover the same fragments of knowledge from scratch for every query, rather than building a compounding synthesis.
- **Lack of Accumulation**: Standard RAG does not build a persistent artifact that grows richer with every source added.
- **Synthesis Overhead**: Ask a question that requires connecting multiple sources, and RAG must find and piece together those fragments repeatedly.

The [[LLM-Wiki]] pattern is designed as an alternative to overcome these limitations.

---

## related

- [[LLM-Wiki]]
- [[Personal-Knowledge-Management]]

## source

- [[2026-04-08-karpathy-llm-compounding-wiki-pattern]]
