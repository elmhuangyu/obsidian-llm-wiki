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

When searching for answers or exploring context, use the following tiered approach:

### 1. Consult the Map
Always start by reading the main index file: `03_Wiki/_index.md`. This provides the curated structure and hierarchy of the knowledge base. Use it to identify the primary entry points for your query.

### 2. Deep Context Gathering
- **Read Full Files**: Once you identify relevant articles from the index, read them in their entirety. Wiki entries are distilled knowledge and are designed to be understood as complete units.
- **Follow Links**: Follow `[[wikilinks]]` within those articles to explore related concepts and dependencies.
- **Strict Scope**: Querying focuses on `03_Wiki/`. Do not default to reading `01_Raw/` files unless specifically necessary, as the wiki contains the digested, canonical knowledge.

### 3. Advanced Discovery
If the index and direct links do not provide sufficient information, use the `obsidian` CLI.
- **Tags**: Use `obsidian tags` to view all available tags or `obsidian tag name=<tagname>` to find all articles grouped under a specific tag.
- **Search**: Use `obsidian search:context query="<query>"` to locate related articles with immediate context, or `grep_search` and `glob` to locate specific keywords or patterns.
- **Backlinks**: Use `obsidian backlinks <file>` to understand an entity's relationships by checking what other pages link *to* it.

### 4. Synthesize the Answer
- Connect the dots across multiple articles rather than just summarizing facts.
- Cite the articles you reference using `[[wikilinks]]`.
- Answer what the information *means*, recognizing themes, patterns, and tensions that surface in the vault.

### 5. Compound the Knowledge
- If answering a query leads to a novel comparison, analysis, or previously unmapped connection, **save that insight back into the wiki**! Compile the answer into a new concept or pattern page so your explorations become permanent, searchable knowledge.
