---
title: MarkItDown
type: tool
tags: [markdown, conversion, automation, ocr]
created: 2026-04-08
last_updated: 2026-04-08
---

# MarkItDown

**MarkItDown** is a tool developed by Microsoft used to convert diverse data sources into clean, machine-readable Markdown format. It serves as a foundational component in the **ingest** phase of an [[LLM-Wiki]].

## Features and Capabilities

MarkItDown is designed to handle a wide variety of standard document formats, making it ideal for automating the ingestion of personal and professional data.

- **Supported Formats**: It supports standard Office documents (Word, Excel, PowerPoint) and PDFs.
- **OCR Integration**: For picture-based PDFs and images, it can be extended with `markitdown-ocr`, which typically requires an OpenAI-compatible LLM to perform optical character recognition.
- **Standardization**: By converting everything to Markdown, it enables LLMs to process information consistently regardless of the original source format.

## Role in the Wiki Workflow

In a [[Personal-Knowledge-Wiki]] setup, MarkItDown is often used as the primary tool for the `ingest` command. When MarkItDown is insufficient (e.g., for complex YouTube extraction or audio transcription), specialized tools or LLMs like **Gemini Flash** are used as fallbacks.

---

## related

- [[Personal-Knowledge-Wiki]]
- [[LLM-Wiki]]

## source

- [[2026-04-08-karpathy-llm-compounding-wiki-pattern]]
