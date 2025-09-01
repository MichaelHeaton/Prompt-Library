# Prompt Library

Source of truth for reusable ChatGPT prompt modes. Mirror these into ChatGPT Projects for daily use.

## Structure
- prompts/ scratch, experimental snippets (not canonical)
- projects/ canonical Project prompts (`prompt.md`, `instructions.md`)
- account/ AI profile and settings
- .github/ configs and templates
- LICENSE MIT

## Quick Start
1. Clone repo
2. Edit canonical prompts under `/projects/<name>/prompt.md`. Use `/prompts` for experiments only.
3. Copy a prompt into ChatGPT to switch modes
4. Submit PRs for improvements

## Modes
See `/projects` for canonical modes. `/prompts` contains scratch/experimental snippets.

## How to Use With ChatGPT

**Account-level Custom Instructions (global):** These provide stable defaults across all chats. Keep them concise and focused on tone and style rules.

**Project-level Instructions:** These define per-project behavior and override account defaults. They should include role, scope, and output formats.

**Project Files:** These are pinned prompts and reference documents used within a project. They are *snapshots* at the time of upload and do not sync live with your repo. You must update them manually if you edit the originals later.

**Note:** ChatGPT cannot automatically update files you add to a Project. You must re-upload if you change them. The repo is the source of truth; Projects are for daily use.

## Account Instruction Templates

### Traits (global defaults)
Be concise, skeptical, and devil’s advocate. Use bullet lists, tables, or checklists. One question at a time. Default to compact output. No em or en dashes.

### Anything else (support)
Optimize for ADHD readability. TL,DR first. Chunk into sections. Format for README, OneDrive, or Planner when relevant. No filler.

## Projects

The `/projects/` folder is for prompt templates that are explicitly meant to be loaded into ChatGPT Projects. These templates may include `Instructions` text and recommended pinned files. Unlike `/prompts/`, which are mode snippets you can drop anywhere, `/projects/` files are designed to structure a whole Project context.

Examples of potential project templates include:
- `projects/sre-runbooks/`
- `projects/research-assistant/`
- `projects/writing-assistant/`
- `projects/checklist-assistant/`
- `projects/sprint-planner/`
- `projects/devils-advocate/`
- `projects/compact-notes/`

## Structure

- prompts/ scratch prompt snippets (non-canonical)
- projects/ ChatGPT Projects with canonical prompts and instructions
- account/ AI profile and settings

Canonical prompts that power ChatGPT Projects live under /projects/<name>/prompt.md. Keep /prompts for experiments only.

## How to use Projects

1. Create a Project in ChatGPT with the same name as a folder under `/projects`.

2. Paste the contents of that project's `prompt.md` into the Project's **Prompt** field.

3. Paste `instructions.md` into the Project's **Instructions** field.

4. If the Project needs files, attach them in the Project so the assistant can read them.

5. Keep `/projects/<name>/prompt.md` as the single source of truth. Update here, then copy to ChatGPT when it changes.
