Set up a self-maintaining instruction system for this repo.

1. Read the code and any existing CLAUDE.md, AGENTS.md or
   .cursorrules. Write AGENTS.md (under ~100 lines):
   - WHY: what this project is, in 2-3 lines
   - WHAT: stack and a short map of key folders
   - HOW: exact build/test/lint/run commands, and how to
     verify a change is done
   - Gotchas that aren't obvious from the code
   Skip anything inferable from code, standard conventions,
   and generic advice. Test each line: would removing it cause
   a mistake? If not, cut it. Put detail in docs/*.md and link.

2. Make CLAUDE.md just `@AGENTS.md` plus any Claude-only notes.

3. Any rule a linter, formatter or hook could enforce: set that
   up in config or .claude/settings.json instead of writing it.

4. Create a /learn skill (.claude/skills/learn/SKILL.md,
   manual-only) that, after I correct you:
   - states the lesson in one line
   - routes it: hook (must always happen), lint rule, subfolder
     AGENTS.md (one area), docs/ file (detail), or AGENTS.md
     (applies everywhere)
   - edits an existing line if it overlaps; never duplicates
   - shows me the diff before saving

5. Create a /prune skill that proposes deletions: rules you'd
   follow anyway, stale commands, anything past 150 lines.

6. Add CLAUDE.local.md to .gitignore for my personal notes.

7. If on GitHub, set up the Claude Code GitHub Action so I can
   tag @claude on a PR to record a lesson the same way.

Show me the diff and a short summary.
