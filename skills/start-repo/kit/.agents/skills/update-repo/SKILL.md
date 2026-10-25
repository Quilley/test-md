---
name: update-repo
description: Record a lesson in this repo's instruction files as one line in the narrowest AGENTS.md, rule or skill. Use when the user says "update AGENTS.md", "update CLAUDE.md" or "add this to the instructions", when the user corrects a mistake that could happen again, when a skill starts keeping planning files somewhere new, or when the upkeep hook reports instruction drift or a new auto-memory correction.
---

# update-repo

A lesson is a mistake or a correction the next session would repeat unless
told. Record it once, in the narrowest home that covers it, as one specific
line. Every line in an always-loaded file is paid for in every session, so a
line earns its place only if a session would go wrong without it.

## Where a lesson goes
| The lesson | Home |
|---|---|
| holds everywhere in the repo | root `AGENTS.md` |
| holds in one folder | that folder's `AGENTS.md`, created with a `CLAUDE.md` shim beside it if the folder has none (see Folder files) |
| holds for a kind of file spread across folders, such as tests or schema changes | Claude Code only: `.claude/rules/<topic>.md` with a `paths:` list of globs in its frontmatter. Other agents ignore it, so put the line in the nearest `AGENTS.md` when it matters to them |
| is a procedure with several steps | a skill in `.agents/skills/<name>/`, with a relative symlink `.claude/skills/<name>` to it for Claude Code (`paths:` is Claude Code only) |
| must hold every time | a hook, lint rule, test or `permissions.deny` entry; write the line too, until the tool exists |
| is personal to the user | their own user-level instructions or auto memory, not the repo |
| is a decision or the state of some work | the place `plan/AGENTS.md` lists for it |

## Steps
1. Name the lesson in one sentence and its source: something that happened in
   this session, the user's explicit request, a hook report, or an
   auto-memory note. A lesson with no source is speculation: tell the user
   why it doesn't need a rule, and stop.
2. Choose its home from the table, then read that file and any file that may
   already cover the lesson.
3. If a line already says it, the rule existed and wasn't followed: sharpen
   that line rather than adding one, and propose a tool if one could enforce
   it.
4. Write one imperative line specific enough to check: "Run migrations with
   the migrate script in ship/bin", not "Be careful with migrations". Add the
   reason only when the rule would look arbitrary without it.
5. When the change adds or sharpens one line in an existing file and
   contradicts nothing, apply it and report `Added to <file>: <line>`.
   Anything bigger (a new file, removing or rewriting lines, moving content
   between files) or a tentative request: show the diff and ask first. In a
   non-interactive run, put that proposal in your reply and change nothing.
6. When the source was an auto-memory note, delete the note and its
   `MEMORY.md` line once the rule is in, so it isn't loaded twice.

## Folder files
Edit the `AGENTS.md` files, never a `CLAUDE.md`: each `CLAUDE.md` is a shim
that only imports the `AGENTS.md` beside it, so Codex and the other agents see
the same text. A new folder gets both files, the shim being exactly:

```
<!-- Edit AGENTS.md, not this file. It only imports AGENTS.md so Claude Code and other agents read the same text. -->
@AGENTS.md
```

## Registering a planning location
When a skill, tracker or person keeps planning files (specs, tickets,
decisions, glossary, notes) somewhere `plan/AGENTS.md` doesn't list, add one
line there: the path from the repo root in backticks without a trailing slash,
what it holds, and where its layout is defined, pointing at the owner's config or skill instead
of restating the layout. The first line replaces the "Nothing listed yet."
sentence. Move no files and edit no skill. Use the same step when the hook
reports an unlisted place.

## Drift reports
The upkeep hook reports paths an instruction file names that no longer exist,
planning places `plan/AGENTS.md` doesn't list, a `CLAUDE.md` that holds more
than its import (move the content into the `AGENTS.md` beside it), and
unfilled `{{...}}` placeholders. Fix the instruction file to match the repo. If the change that
caused the drift looks accidental, ask instead.

## Gotchas
- A lesson recorded only as a tool proposal is lost when nobody builds the
  tool. Write the line now; audit-repo removes it once a tool enforces
  the rule.
- "Maybe we should add a rule that..." is a question. Answer it with a
  recommendation and wait.
- What an agent can find by reading the repo, such as directory tours,
  dependency lists or what a module does, raises cost in every session
  without helping. The homes above are for what reading can't reveal:
  conventions, gotchas and the reasons behind odd-looking code.
- Claude Code loads a folder's instructions or a `paths:` rule only when it
  touches matching files, and Codex loads a folder's `AGENTS.md` only when the
  session starts there or below. A lesson that must reach every session goes in
  the root file, or the root file points at the folder file.
