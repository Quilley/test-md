{{purpose}}

## Where things go
Work falls into two buckets, whichever skill or tool produced it.
- Thinking: specs, tickets, plans, decisions, glossary, research.
  `plan/AGENTS.md` lists where this repo keeps each. Read it before you start,
  resume or record any of these. Skills keep their own layout, so leave their
  files where they put them.
- Shipping: code and tests, in `ship/`. It is the project root for tooling:
  the manifest, lockfile and tool config live there, and build, test and lint
  commands run from there. Read `ship/AGENTS.md` before you run or change
  checks.
- The repo root holds repo and agent config, plus files that skills keep
  there.

## How work moves
Work that needs a plan gets one on disk, not only in chat, so the next session
can pick it up. When the plan changes while you build, update its file in the
same change.

## Keeping instructions true
Instructions live in the AGENTS.md files; each CLAUDE.md only imports its
sibling, so edit AGENTS.md. When the user corrects you, a mistake shows a
lesson the next session would hit too, or a skill starts keeping planning
files somewhere new, use update-repo. `sh .agents/hooks/upkeep check` lists
stale paths.

<!-- reviewed: {{date}} {{model}} -->
