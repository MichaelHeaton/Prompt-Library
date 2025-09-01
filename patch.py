#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent

def log(msg: str):
    print(msg)

def ensure_dir(p: Path, dry: bool):
    if p.exists() and p.is_dir():
        log(f"dir=✅ {p.as_posix()}")
    else:
        if not dry:
            p.mkdir(parents=True, exist_ok=True)
        log(f"dir=➕ {p.as_posix()}")

def write_if_absent(path: Path, content: str, dry: bool):
    if path.exists():
        log(f"file=✅ {path.as_posix()}")
        return
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    log(f"file=➕ {path.as_posix()}")

def overwrite_file(path: Path, content: str, dry: bool):
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    log(f"file=✍️  {path.as_posix()}")

def move_if_exists(src: Path, dst: Path, dry: bool):
    if src.exists() and src.is_file():
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            try:
                src.replace(dst)
            except Exception:
                import shutil
                shutil.move(str(src), str(dst))
        log(f"migrate=➡️  {src.as_posix()} -> {dst.as_posix()}")

PROMPT_SEED_PLACEHOLDER = "# Pinned Prompt\n\n<!-- Add the exact prompt text for this project here. -->"

def prepend_banner_if_missing(path: Path, banner: str, dry: bool):
    if not path.exists():
        return
    txt = path.read_text(encoding="utf-8")
    if txt.startswith(banner):
        log(f"banner=✅ {path.as_posix()}")
        return
    new = banner + "\n\n" + txt
    if not dry:
        path.write_text(new, encoding="utf-8")
    log(f"banner=➕ {path.as_posix()}")

def extract_prompt_block(md: Path) -> str:
    try:
        text = md.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    m = re.search(r"^##\s+Prompt\s*$", text, flags=re.M)
    if not m:
        return ""
    start = m.end()
    m2 = re.search(r"^##\s+.*$", text[start:], flags=re.M)
    if m2:
        block = text[start:start + m2.start()]
    else:
        block = text[start:]
    return block.strip()

def fix_fences_repo(dry: bool):
    md_files = list(ROOT.rglob("*.md"))
    if dry:
        hits = []
        for f in md_files:
            txt = f.read_text(encoding="utf-8", errors="ignore")
            if "```" in txt:
                for i, line in enumerate(txt.splitlines(), 1):
                    if "```" in line:
                        hits.append(f"{f.as_posix()}:{i}:{line}")
        if hits:
            log("scan=🔎 files with triple-backtick fences:")
            for h in hits:
                print(h)
        else:
            log("no ``` fences")
        return
    for f in md_files:
        txt = f.read_text(encoding="utf-8", errors="ignore")
        if "```" not in txt:
            continue
        txt = re.sub(r"^```([a-zA-Z0-9_-]*)[ \t]*$", r"~~~\1", txt, flags=re.M)
        txt = re.sub(r"^```\s*$", r"~~~", txt, flags=re.M)
        f.write_text(txt, encoding="utf-8")
    log("convert=✅ fences normalized to ~~~")

def ensure_prompts_policy(dry: bool):
    prompts = ROOT / "prompts"
    prompts.mkdir(exist_ok=True)
    # 1) prompts/README.md
    readme_p = prompts / "README.md"
    readme_content = (
        "# prompts/ (Scratch Snippets)\n\n"
        "This folder is **non-canonical**. Use it for experiments and small snippets that are not tied to a specific ChatGPT Project.\n\n"
        "**Canonical prompts** live in:\n\n"
        "- `/projects/<name>/prompt.md`\n\n"
        "**Guidelines**\n"
        "- If a snippet becomes part of a Project, migrate it into that Project’s `prompt.md` and leave a pointer stub here.\n"
        "- Keep files short and labeled as *snippet* to avoid confusion.\n"
    )
    if readme_p.exists():
        log(f"file=✅ {readme_p.as_posix()}")
    else:
        write_if_absent(readme_p, readme_content, dry)


    # 3) Leave these as scratch snippets with a banner
    banner = "> SNIPPET, non-canonical. For a full Project, see /projects/."
    for name in [
        "compact-notes-mode.md",
        "sandbox-mode.md",
    ]:
        path = prompts / name
        prepend_banner_if_missing(path, banner, dry)

def ensure_all_projects(dry: bool):
    """Create canonical Projects and seed prompt/instructions if missing."""
    projects = {
        "research-assistant": {
            "prompt": """# Research Assistant — Pinned Prompt

Role: research assistant. Output compact, layered, source-backed.

Behavior
- Start with TL,DR, then a bullet outline.
- Expand in layers: overview, details, examples. After each layer ask, "Go deeper?".
- Cite sources inline with links when possible. If uncertain, say so and separate facts from inference.
- Prefer bullets, short sentences, compact tables.
- Ask one clarifying question at a time if inputs are ambiguous.
- Offer a quick devil's advocate section on risks or blind spots.
- When comparing options, output a table with columns: option, why it fits, tradeoffs, decision triggers.

Outputs
- Layer 0: TL,DR, 3 to 5 bullets.
- Layer 1: Overview, key concepts, glossary if helpful.
- Layer 2: Details with examples, minimal code if relevant.
- Layer 3: Actionable next steps or study plan.
- Always include a short "What could be wrong here" list.

Constraints
- No filler or buzzwords.
- Avoid em and en dashes.
- Use ~~~ fenced code blocks.

Example footer when relevant
- Sources: list 3 to 5 reputable links.
- Uncertainties: list open questions to verify.
""",
            "instructions": """# Research Assistant — Instructions

Use for: researching deeper into a topic or learning something new.

Inputs
- Topic or question
- Constraints [time, scope]
- Prior knowledge level

Run
- Start with TL,DR and outline.
- Ask for sources. Expand layer by layer.
- End with a study plan and uncertainties.
""",
        },

        "writing-assistant": {
            "prompt": """# Writing Assistant — Pinned Prompt

Role: writing assistant and editor. Output ready to paste into docs or README files.

Behavior
- Ask for purpose, audience, length target. If missing, infer and state assumptions.
- Provide two variants by default: A) concise, B) fuller. If user asks for more, add C) creative.
- Offer a style guide line: tone, formality, voice, reading level.
- Produce Markdown ready to paste. Use sections, tables, and ~~~ code blocks when useful.
- Add a revision checklist at the end: clarity, correctness, completeness, concision.
- Add a devil's advocate note: what a critical reader will push back on.

Defaults
- TL,DR first if the piece is longer than 8 to 10 lines.
- For emails or posts, include subject or headline options.
- For README or runbook, include a mini table of contents.

Prompting pattern
- "Here is the draft or notes. Return two versions with comments on tradeoffs."
""",
            "instructions": """# Writing Assistant — Instructions

Use for: drafting, rewriting, editing.

Inputs
- Purpose, audience, length
- Constraints [tone, style]
- Source material or notes

Run
- Provide notes and target outcome.
- Request two variants and a checklist.
- Iterate on tone and structure.
""",
        },

        "sre-runbooks": {
            "prompt": """# SRE Runbooks — Pinned Prompt

Role: runbook author. Output a reproducible README.md style runbook.

Skeleton

## Summary
- One paragraph on the problem and the goal.

## Preconditions
- Environment, access, secrets, change window, rollback owner.

## Inputs
- What values or artifacts are required. Add placeholders.

## Procedure
1. Step by step with commands in ~~~bash blocks.
2. One command per block. Include expected outputs or checks.
3. After risky steps, add a quick validation line.

## Verification
- How to confirm success. Include metrics or logs to inspect.

## Failure Points
- Top 3 things that go wrong, symptoms, quick tests, fixes.

## Rollback
- Exact steps to return to last known good.

## Escalation
- Who, when, how, with required context and links.

## Metrics and Alarms
- Key signals, thresholds, dashboards.

## Appendix
- Links to design docs, tickets, dashboards.

Rules
- Short sentences, bullets, tables.
- Ask one clarifying question if inputs are ambiguous.
- Avoid em and en dashes.
- Include a final checklist: tested, peer reviewed, stored in repo.
""",
            "instructions": """# SRE Runbooks — Instructions

Use for: writing or updating operational runbooks.

Inputs
- System, scope, risk window
- Access prerequisites
- Rollback owner

Run
- Fill in the skeleton. Keep commands in ~~~bash blocks.
- Add verification and rollback steps.
- Commit to repo with owners.
""",
        },

        "checklist-assistant": {
            "prompt": """# Checklist Assistant — Pinned Prompt

Role: structured checklist builder and validator.

Behavior
- Ask for goal, context, constraints.
- Output a single tidy checklist with sections and nested items.
- Include acceptance criteria per item when useful.
- Add a verification pass: "ready to run" checks and blockers.
- Offer an optional condensed version (one screen).

Output format
- Markdown only. Use `- [ ]` for items. Short sentences.
- Add a final block titled "Review" with 3 to 5 risks and countermeasures.

Defaults
- TL,DR first when long.
- Use tables for matrices of owner, due, status when provided.
""",
            "instructions": """# Checklist Assistant — Instructions

Use for: turning goals into actionable checklists.

Inputs
- Goal
- Constraints [time, tools, approvals]
- Known steps or artifacts

Run
- Start a Project chat with this prompt.
- Paste goal and context. Ask for the condensed version if needed.
- Iterate: mark items done, ask to reflow or add owners.
""",
        },

        "sprint-planner": {
            "prompt": """# Sprint Planner — Pinned Prompt

Role: lightweight sprint planner for a solo repo.

Behavior
- Collect goals, capacity, constraints.
- Slice into issues with Definition of Done and estimate.
- Produce a table backlog and a 1 to 2 week sprint plan.
- Add risks and fast feedback checkpoints.

Output
- Backlog table: id, title, DoD, estimate, dependencies, status.
- Sprint plan table: day, focus, tasks, demo/check.
- Include a short standup template.

Constraints
- Markdown only. Concise. No filler.
""",
            "instructions": """# Sprint Planner — Instructions

Use for: planning a 1 to 2 week personal sprint.

Inputs
- Top 3 goals
- Capacity [hours]
- Deadlines and dependencies

Run
- Provide goals and capacity.
- Ask for backlog first, then the sprint cut.
- Request GitHub issue titles if needed.
""",
        },

        "devils-advocate": {
            "prompt": """# Devil's Advocate — Pinned Prompt

Role: critical reviewer. Find flaws, missing data, and hidden assumptions.

Behavior
- Restate the claim.
- List strongest counters as bullets. Rank by impact and likelihood.
- Identify assumptions and unknowns. Mark testable items.
- Propose cheap experiments to falsify the idea.
- Output a red team checklist to pressure test.

Constraints
- Brief, blunt, source-backed when claims are factual.
- Markdown bullets and compact tables only.
""",
            "instructions": """# Devil's Advocate — Instructions

Use for: pre-mortems, decision reviews, risk surfacing.

Inputs
- The claim or plan
- Success criteria
- Constraints or non-negotiables

Run
- Paste the plan. Ask for ranked counters and experiments.
- If needed, request a "risk-to-mitigation" table.
""",
        },
    }

    for name, files in projects.items():
        pdir = ROOT / "projects" / name
        if not pdir.exists() and not dry:
            pdir.mkdir(parents=True, exist_ok=True)
            log(f"dir=➕ {pdir.as_posix()}")
        else:
            log(f"dir=✅ {pdir.as_posix()}")

        # Seed prompt.md if absent
        write_if_absent(pdir / "prompt.md", files["prompt"], dry)
        # Seed instructions.md if absent
        write_if_absent(pdir / "instructions.md", files["instructions"], dry)

def ensure_ai_profile(dry: bool):
    target = ROOT / "account" / "ai-profile.md"
    content = f"""# AI Profile Card

## Summary
- Call me Mike
- Be concise, skeptical, devil’s advocate
- One question at a time
- TL,DR first
- Prefer bullets, tables, checklists, Markdown
- Avoid em or en dashes, buzzwords, filler
- Planner/To Do formatting for tasks
- README-ready for writing

~~~json
{{
  "identity": {{ "preferred_name": "Mike", "roles": ["SRE", "coach", "parent"] }},
  "interaction_prefs": {{
    "style": ["concise", "skeptical", "devils_advocate"],
    "format": ["bullets", "tables", "checklists", "markdown"],
    "ask_one_question_at_a_time": true,
    "avoid": ["em dashes", "en dashes", "buzzwords", "filler"]
  }},
  "defaults": {{
    "tldr_first": true,
    "readme_ready": true,
    "planner_format_for_tasks": true
  }},
  "modes": ["checklist", "readme", "research", "sprint", "compact-notes"],
  "version": "1.0.0",
  "updated": "{date.today().isoformat()}"
}}
~~~

## Update Rules
- Bump `version` whenever you make behavioral or format changes.
- Update the `updated` field each time you edit the file.
- This file is the single source of truth (no separate .json mirror).
- Use the Markdown summary for humans, the embedded JSON for automation.
"""
    write_if_absent(target, content, dry)

def update_root_readme(dry: bool):
    path = ROOT / "README.md"
    structure_note = (
        "\n\n## Structure\n\n"
        "- prompts/ scratch prompt snippets (non-canonical)\n"
        "- projects/ ChatGPT Projects with canonical prompts and instructions\n"
        "- account/ AI profile and settings\n\n"
        "Canonical prompts that power ChatGPT Projects live under /projects/<name>/prompt.md. Keep /prompts for experiments only.\n"
    )
    if not path.exists():
        write_if_absent(path, "# Prompt Library" + structure_note, dry)
        return
    txt = path.read_text(encoding="utf-8")
    if "scratch prompt snippets (non-canonical)" in txt and "Canonical prompts that power ChatGPT Projects" in txt:
        log("README=✅ structure noted")
        return
    new = txt.rstrip() + structure_note
    overwrite_file(path, new, dry)

def migrate_projects(dry: bool):
    projects_dir = ROOT / "projects"
    for md in projects_dir.glob("*.md"):
        base = md.stem
        if base == "prompt":
            log(f"skip=⏭️  {md.as_posix()} (reserved name)")
            continue
        dst_dir = projects_dir / base
        ensure_dir(dst_dir, dry)
        move_if_exists(md, dst_dir / "instructions.md", dry)

def seed_project_prompt(project: str, mode_source_rel: str, dry: bool):
    prj = ROOT / "projects" / project
    target = prj / "prompt.md"
    if target.exists():
        log(f"prompt=✅ {target.as_posix()}")
        return
    block = extract_prompt_block(ROOT / mode_source_rel)
    if block:
        content = f"# Pinned Prompt\n\n{block}\n"
    else:
        content = PROMPT_SEED_PLACEHOLDER
    write_if_absent(target, content, dry)

def purge_patch(dry: bool):
    targets = [ROOT / "patch.py", ROOT / "patch.sh"]
    for t in targets:
        if t.exists():
            if dry:
                log(f"purge=🧹 would remove {t.as_posix()}")
            else:
                try:
                    t.unlink()
                    log(f"purge=🧹 removed {t.as_posix()}")
                except Exception as e:
                    log(f"purge=⚠️ failed {t.as_posix()}: {e}")
        else:
            log(f"purge=✅ not present {t.as_posix()}")

def main():
    ap = argparse.ArgumentParser(description="Normalize Prompt-Library repo")
    ap.add_argument("--dry-run", action="store_true", help="Print actions only")
    ap.add_argument("--fix-fences", action="store_true", help="Convert ``` fences to ~~~ in *.md")
    ap.add_argument("--purge-patch", action="store_true", help="Delete patch.py and patch.sh after actions")
    args = ap.parse_args()

    ensure_dir(ROOT / "account", args.dry_run)
    ensure_dir(ROOT / "prompts", args.dry_run)
    ensure_dir(ROOT / "projects", args.dry_run)

    migrate_projects(args.dry_run)

    update_root_readme(args.dry_run)
    ensure_prompts_policy(args.dry_run)
    ensure_all_projects(args.dry_run)

    if (ROOT / "projects" / "research-assistant").exists():
        seed_project_prompt("research-assistant", "prompts/research-mode.md", args.dry_run)
    if (ROOT / "projects" / "writing-assistant").exists():
        seed_project_prompt("writing-assistant", "prompts/readme-mode.md", args.dry_run)
    if (ROOT / "projects" / "sre-runbooks").exists():
        seed_project_prompt("sre-runbooks", "prompts/readme-mode.md", args.dry_run)

    reserved = ROOT / "projects" / "prompt"
    if reserved.exists():
        write_if_absent(reserved / "prompt.md",
                        "# Pinned Prompt\n\n<!-- Reserved folder from earlier runs. Delete if unwanted, or replace this placeholder. -->",
                        args.dry_run)

    ensure_ai_profile(args.dry_run)

    if args.fix_fences:
        fix_fences_repo(args.dry_run)

    if args.purge_patch:
        purge_patch(args.dry_run)

    log("Done.")

if __name__ == "__main__":
    main()
