---
name: audit-repo
description: Prune and check this repo's instruction files (every AGENTS.md and CLAUDE.md, .claude/rules and the repo's skills) and the planning places plan/AGENTS.md lists. Use when asked to audit or clean up the instructions, when the upkeep hook says a review is due, after a model upgrade, or when instructions look stale or contradict each other.
---

# audit-repo

Instruction files collect sediment: lines that were true once, workarounds
for an older model, rules a tool now enforces. Each costs context in every
session and competes with the lines that still matter, so an audit is mostly
deletion.

## Steps
1. Run `sh .agents/hooks/upkeep check` from the repo root and list what it
   reports.
2. Read every instruction file: the root and folder `AGENTS.md` files, any
   `CLAUDE.md` that is more than its import (flag it), `.claude/rules/` (Claude
   Code only), and the descriptions of the skills in `.agents/skills/`.
   Flag each line that fails "would a session go wrong without this?":
   content readable from the code, rules a hook or linter now enforces,
   workarounds for an older model's limits, duplicates and contradictions
   across files, procedures that belong in a skill, and one area's rules
   sitting in the root file.
3. Run the read-only commands the files name (tests, lint, typecheck). Flag
   any that fail or no longer exist.
4. In each planning place `plan/AGENTS.md` lists, flag status lines that are
   no longer true, such as shipped or abandoned work still marked active, and
   lasting rules sitting in planning files. Then look for planning files kept
   somewhere unlisted (specs, tickets, decisions, glossary or notes in the
   root, `docs/` or a dot-folder) and register them with update-repo.
5. In Claude Code, read this repo's auto-memory notes (location below). Flag notes that hold
   for anyone working in the repo, not just this user: they are candidates
   for update-repo.
6. Report a one-line verdict, then the findings, most consequential first,
   each with its fix. Apply fixes one at a time as the user approves them,
   using update-repo for anything added. When committing, put removals
   in their own commit whose message lists the removed lines, so they can
   come back.
7. Set the `<!-- reviewed: ... -->` line in the root `AGENTS.md` to today's
   date (YYYY-MM-DD) and your model id.

In Claude Code, suggest the user run `/doctor prompt-audit` for a second
opinion on the same files.

## After a model upgrade
Offer a deletion test for lines that look like workarounds for an older
model: remove them, and add back only those whose mistake returns.

## Auto-memory location
`~/.claude/projects/<folder>/memory/`, where `<folder>` is the repo's real
path with every character other than letters, digits and `-` replaced by `-`.
For `/Users/me/code/app` that is `-Users-me-code-app`.

## Gotchas
- Planning records belong to their owner, a skill, tracker or person. Judge
  them only on whether their status and links are still true; never rewrite or
  move them.
- A block another skill's setup wrote, such as an Agent skills section, is
  configuration that skill reads. Keep it unless the user says otherwise; if it
  landed in a `CLAUDE.md` shim, move it into the `AGENTS.md` beside it.
- A folder `AGENTS.md` or a `paths:` rule that duplicates a root line costs
  twice in that folder. Keep the line in one place.
