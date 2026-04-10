## Directory Structure & Purpose

This document outlines the purpose of each directory in the vault, following the patterns described in the vault's design notes.

- `00_Home/`: The entry points and dashboards for the vault, including `0_Home.md` and the `Inbox`.
- `01_Raw/`: The ingestion point for unprocessed or primary source data before it is "absorbed."
  - `Entities/`: Structured raw entities and intermediate outputs from the ingestion process.
  - `Journal/`: Daily occasional personal journals. These are already well-formed Markdown and act as primary sources for the Absorb step without needing a separate Ingest phase.
  - `Notes/`: General unstructured notes and quick captures.
- `03_Wiki/`: The synthesized knowledge base. Contains refined notes that have been processed and absorbed from raw data into structured categories (concepts, patterns, people, tools).
- `04_Trackers/`: Used for task management and checklists (e.g., annual tax returns). These are functional logs rather than knowledge, acting as operational data. They are generally not "absorbed" into the Wiki.
- `97_Attachments/`: A centralized store for media, such as photos and document scans, related to the notes.
- `98_Archived/`: A permanent home for completed trackers or projects that are no longer active but need to be preserved for the record.
- `99_Templates/`: Standard schemas and templated structures for Obsidian notes.
- `Data/`: Stores external data inputs waiting to be processed.
  - `Clippings/`: Raw web clips (from Obsidian Web Clipper). These are processed via the Ingest step using an LLM to clean titles, remove ads, and normalize formatting.
- `Scripts/`: Contains the Python workflows and LLM prompts that power the automated Ingest and Absorb processes of the LLM-powered wiki system.

## How to Query the Wiki

Querying is the process of asking questions against the synthesized knowledge base (`03_Wiki/`). Instead of scanning raw notes, queries rely on the connections and compounding knowledge already built into the wiki.

When searching for answers or exploring context, use the following approach:

### 1. Explore & Search
Use the Obsidian CLI or built-in tools to locate entry points:
- `obsidian tags`: View all available tags to find relevant categories.
- `obsidian tag name=<tagname>`: Find all articles grouped under a specific tag.
- `obsidian search:context query="<query>"`: Locate related articles and extract the immediate context lines surrounding the keyword.
- `obsidian backlinks <file>`: Understand an entity's relationships by checking what other pages link to it.

### 2. Gather Context
- Start by checking index pages (like `03_Wiki/_index.md`) to get a high-level map of concepts.
- Choose and read 3–8 highly relevant articles based on your search. Follow `[[wikilinks]]` and check "related" sections.
- **Strict Scope**: Querying focuses on `03_Wiki/`. Do not default to reading `01_Raw/` files unless specifically necessary, as the wiki contains the digested, canonical knowledge.

### 3. Synthesize the Answer
- Connect the dots across multiple articles rather than just summarizing facts.
- Cite the articles you reference using `[[wikilinks]]`.
- Answer what the information *means*, recognizing themes, patterns, and tensions that surface in the vault.

### 4. Compound the Knowledge
- If answering a query leads to a novel comparison, analysis, or previously unmapped connection, **save that insight back into the wiki**! Compile the answer into a new concept or pattern page so your explorations become permanent, searchable knowledge.
