Restructure this brownfield repo into dev/ and plan/ and set up its agent instructions. Work on a new branch chore/plan-dev-layout; stop if the working tree is dirty. Use subagents for exploration so your context stays small. Don't write anything until I approve the phase.

Target layout
- dev/: everything that ships (for example dev/backend, dev/frontend). Nothing in dev/ may reference plan/.
- plan/: everything that doesn't ship. It reuses the default paths of the Matt Pocock skills, prefixed with plan/: plan/CONTEXT.md, plan/docs/adr/, plan/docs/agents/, plan/.scratch/, plan/.out-of-scope/, plus plan/inbox/ for files I drop in.
- Root: only repo tooling (.git, .github, .claude, workspace config that must sit at root) and the instruction files.

Phase 1: Survey (read only)
Find the stack, every app and package, and how each is built, tested, linted, run and deployed (CI workflows, Dockerfiles, deploy configs). Find existing instruction files (CLAUDE.md, AGENTS.md, .cursorrules, copilot instructions) and planning material (docs, specs, notes, ADRs, TODOs, CONTEXT.md, .scratch). Run every build, test and lint command you find. Record which pass, from which directory, and how long they take. Classify every top-level path as dev, plan, root or unclear.

Phase 2: Propose and ask
Show the classification and a move list. For moving code into dev/, list everything it breaks: CI paths, Docker contexts, deploy root directories, path aliases, scripts, absolute imports. Then ask me with AskUserQuestion, recommendation first:
1. Move shipped code into dev/ now, or only create plan/ for now?
2. Tickets: GitHub Issues (default if the remote is GitHub) or local files in plan/.scratch/?
3. Commit plan/inbox/ or gitignore it?
4. Where each unclear path goes.

Phase 3: Move (one commit per step)
a. Move planning material into plan/ with git mv and fix links.
b. If approved, move code into dev/ using only git mv, in its own commit, so history and blame follow. Fix configs in a separate commit. Re-run every Phase 1 command: anything that passed before must pass now. Things outside the repo (deploy dashboard root directory, CI secrets) go on a list for me; don't change them.

Phase 4: Instruction files (show the diff first)
- Root AGENTS.md, under 60 lines: what the project is and why, in one line; the layout; "plan/ never ships, dev/ never imports plan/"; "before working under dev/ or plan/, read that folder's AGENTS.md"; what done means (exact commands plus one end-to-end check); gotchas that apply everywhere.
- dev/AGENTS.md, under 80 lines: exact commands and the directory to run each from, the done check, gotchas. A sub-app gets its own AGENTS.md only if its commands differ.
- plan/AGENTS.md, under 40 lines: what goes where, which skill writes where, and "when a skill names a root path (CONTEXT.md, docs/adr/, docs/agents/, .scratch/, .out-of-scope/), use that path under plan/".
- Next to each AGENTS.md, a CLAUDE.md containing only @AGENTS.md.
- Move anything useful from old instruction files into the right file, then delete the old files. Drop anything already in ~/.claude/CLAUDE.md, anything inferable from code, and generic advice. Test every line: would removing it cause a mistake? If not, cut it.
- Add CLAUDE.local.md to .gitignore.

Phase 5: Enforce instead of writing
- Write a small check script that fails if dev/ references plan/, or if CONTEXT.md, docs/adr/, docs/agents/, .scratch/ or .out-of-scope/ appear at the root. Run it in CI.
- In .claude/settings.json, add a Stop hook that runs the layout check and the fast dev checks (lint, typecheck; under about a minute). Skip it when nothing under dev/ changed. Leave out any check that already failed in Phase 1 and list it for me. Add a formatter hook after edits only if the repo already has a formatter.
- Make builds and deploys exclude plan/ (.dockerignore, build roots).
- Remove from the prose any rule a linter or hook now enforces.

Phase 6: Skill config
Read ~/.claude/skills/setup-matt-pocock-skills/SKILL.md and follow it, with these overrides: the tracker chosen in Phase 2; config files in plan/docs/agents/; domain docs at plan/CONTEXT.md and plan/docs/adr/; the "## Agent skills" block goes in the root AGENTS.md, because CLAUDE.md is only an import.

Phase 7: Verify
Run every documented command from its documented directory, plus the layout check. Then give a fresh subagent only the root AGENTS.md and ask it three things: how do I run the backend tests, where does a new spec go, what counts as done. Fix the files wherever it answers wrong. Finish with the full diff, each instruction file's line count, and the list of things I must change by hand.
