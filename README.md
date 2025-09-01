# Prompt Library

Source of truth for reusable ChatGPT prompt modes. Mirror these into ChatGPT Projects for daily use.

## Structure
- prompts/ one file per mode
- projects/ project-level prompt templates
- account/ global account-level instructions
- LICENSE MIT
- .github templates for issues and PRs

## Quick Start
1. Clone repo
2. Edit prompts in `prompts/`
3. Copy a prompt into ChatGPT to switch modes
4. Submit PRs for improvements

## Modes
- Checklist Mode
- README Mode
- Sprint Mode
- Devil's Advocate Mode
- Compact Notes Mode
- Sandbox Mode
- Research Mode

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
- `sre-runbooks.md`
- `research-assistant.md`
- `writing-assistant.md`

## Structure

- prompts/ scratch prompt snippets (non-canonical)
- projects/ ChatGPT Projects with canonical prompts and instructions
- account/ AI profile and settings

Canonical prompts that power ChatGPT Projects live under /projects/<name>/prompt.md. Keep /prompts for experiments only.
