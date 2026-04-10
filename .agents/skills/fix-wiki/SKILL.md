---
name: fix-wiki
description: Fix or adjust a wiki page based on user suggestions. Use this skill to correct incorrectly absorbed wiki pages, such as moving them to appropriate folders, correcting content by re-reading source files, and updating the wiki index tracking.
---

# Fix Wiki Skill

Use this skill when the user requests a correction, structural adjustment, or fix to an existing wiki page (e.g., from `03_Wiki/`), especially if it was absorbed incorrectly or placed in the wrong folder.

## Workflow: Fixing a Wiki Page

1. **Understand the Suggestion**: Carefully review the user's feedback (e.g., "this should be in its own folder", "extract to a new concept", "this legal case was added to concepts instead of a new folder").
2. **Re-read the Source Files**:
   - Locate and read the existing wiki file in `03_Wiki/` that needs fixing.
   - If necessary, find and re-read the original raw file from `01_Raw/` to ensure no details were omitted or misinterpreted during the initial absorption.
3. **Execute the Fix**:
   - **Move/Rename**: If the file was placed in the wrong directory (like `concepts/` instead of `legal-cases/`), read the content, write it to the new path, and delete the old file. Create the new subdirectory if it does not yet exist.
   - **Update/Refactor Content**: If the content needs splitting or merging, create/update the necessary files based on the source texts.
   - **Taxonomy**: Ensure the new placement respects the vault taxonomy described in `absorb.md`.
4. **Update `03_Wiki/_index.md`**:
   - **CRITICAL STEP**: If a filename is changed, or a file is moved to a new directory, you MUST update `03_Wiki/_index.md`.
   - Remove the old file path reference.
   - Add the new file path reference in the appropriate categorical section of the index.
5. **Update Backlinks (Optional but Recommended)**: If the filename changed, search for wikilinks pointing to the old filename (e.g., using `grep_search`) and update them to prevent broken links.

## Guiding Principles

- **Do Not Guess**: Always verify the current state of the wiki note (`view_file`) before applying the fix.
- **Maintain Consistency**: The fixed file should still follow standard wiki formatting (YAML frontmatter, proper tags in lower-case, footnotes for related/source links).
- **Index Integrity**: Never leave dead links in `_index.md`. Always keep exactly one `_index.md` file at the root of `03_Wiki/`.
