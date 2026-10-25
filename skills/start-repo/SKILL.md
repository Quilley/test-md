---
name: start-repo
description: Set up a repo for Claude Code, Codex and other AGENTS.md tools with plan/ and ship/ folders, an AGENTS.md in each, and the hooks and skills that keep those files current. Use when starting a new repo, bringing an existing repo into this layout, or updating a repo's copy of the kit.
---

# start-repo

`kit/` mirrors what a set-up repo contains. You copy it, fill in what only
this repo knows, and check that it loads. Below, `<skill>` is this skill's
folder and `<repo>` is the target repo.

What each piece is for, so you can explain it:
- Instructions live in `AGENTS.md`, which Codex and most other agents read.
  Each `CLAUDE.md` is a two-line shim that imports the `AGENTS.md` beside it,
  so Claude Code reads the same text. Edit `AGENTS.md`, never the shim.
- The root `AGENTS.md` is the router. It loads in every session, so it holds
  only the two buckets (thinking and shipping), a pointer to each folder file,
  and the upkeep pointer. The pointers matter: Codex loads a folder's file only
  when the session starts there, and Claude Code loads it when it touches
  files there.
- `plan/AGENTS.md` indexes wherever the repo's skills and trackers keep
  planning files, and never dictates a layout. `ship/AGENTS.md` holds the
  checks.
- `.agents/skills/` holds the `update-repo` skill, which records a lesson as
  one line in the narrowest home, and the `audit-repo` skill, which prunes.
  Codex reads that folder; `.claude/skills/` has symlinks to it for Claude Code.
- `.agents/hooks/upkeep` decides when upkeep happens. At the end of each turn
  it reports instruction drift, planning places missing from the index, a shim
  that gained content, and (Claude Code only) new auto-memory corrections,
  once each. At session start it says when a review is due. Otherwise it is
  silent. `.claude/settings.json` and `.codex/hooks.json` wire it to each tool.

## 1. Pick the path
- Empty (nothing tracked except a README, LICENSE or .gitignore): step 2.
- `<repo>/.agents/skills/update-repo/` exists: step 4.
- Anything else: step 3.

## 2. New repo
1. Run `git init` if there is no `.git`.
2. Run `cp -Rn <skill>/kit/. <repo>/`. It copies the symlinks as symlinks.
3. In the root `AGENTS.md`, replace `{{purpose}}` with one line on what the
   repo is for, in the user's words. If the user hasn't said, ask once; with
   no answer, delete the line. Replace `{{date}}` and `{{model}}` with today's
   date (YYYY-MM-DD) and your model id.
4. Verify (step 5).

## 3. Existing repo
Show the plan first, and change nothing until the user says go.
1. Read the existing instruction files, README, manifests, scripts and CI. Run
   the check commands you find (tests, lint, typecheck) read-only, and note
   which work.
2. Plan the changes:
   - Code stays where it is. Put ship/'s content in an `AGENTS.md` in the real
     code root, and have the router name that folder instead of `ship/`. Move
     code into `ship/` only if the user asks, as its own change, with the
     checks run before and after.
   - Instruction files become `AGENTS.md` plus a shim, in every folder that has
     one. A `CLAUDE.md` alone moves into a new `AGENTS.md`. An `AGENTS.md`
     alone gets a shim. Both present, or one a symlink to the other: merge
     into one `AGENTS.md` and replace the other with the shim. Shim text is in
     update-repo's Folder files section.
   - `plan/AGENTS.md` comes from the kit. Existing planning docs and the
     places skills write to (specs, ADRs, TODO files, `.scratch/`,
     `CONTEXT.md`) stay where they are and get a line each in its index, with
     update-repo's format. Move one only if the user asks.
   - Fold the existing instruction content into the router and the folder
     files, keeping every constraint. List each line you would cut and why,
     judged by update-repo's table and gotchas.
   - If `.claude/settings.json` or `.codex/hooks.json` exists, merge in the
     kit's two hooks and keep everything else in it. Skills already in
     `.claude/skills/` stay.
3. Show the plan, the drafts and the command results. On go: moves first,
   then the instruction files, then `cp -Rn <skill>/kit/. <repo>/` for the
   rest of the kit and the settings merges, then verify (step 5).

## 4. Update the kit
For `.agents/hooks/upkeep` and each skill in `.agents/skills/`, diff the copy
in `<skill>/kit/` against the repo's and summarize what differs. Point out any
difference that looks like a deliberate local edit, since updating replaces
it. Copy the files the user approves. Instruction files belong to the repo;
audit-repo looks after them.

## 5. Verify
1. `sh <repo>/.agents/hooks/upkeep check` prints nothing.
2. Start a fresh session from the repo root:
   `claude -p "Where would a plan for a new feature go, and where do checks run from?"`.
   Both answers must come from the files. In a repo that already had planning
   files, also ask where its specs and decisions live; the answer must name the
   indexed places. If `codex` is installed, ask the same through
   `codex exec "<question>"`.
3. Report what you wrote, what you verified and how, and what you couldn't
   verify. Claude Code asks once to trust the repo's hooks; in Codex the user
   runs `/hooks` once to review and trust them. Commit only when the user asks.
