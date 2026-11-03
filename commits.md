# Pre-commit testing (local only, no CI)

## Goal
Before each commit, run a fast check that catches most breakage.
Run the slow, full suite locally before merging to main.

## 1. Find the checks
If the **Commands** section below is filled in, use it.
Otherwise look in this order:
1. Build/task files (Makefile, justfile, package.json, pyproject.toml,
   Cargo.toml, go.mod, etc.)
2. Existing git hooks (.git/hooks, .pre-commit-config.yaml)
3. README / CONTRIBUTING

Record what you find in **Commands** and ask me to confirm once.
Don't create new scripts, configs or test frameworks unless asked.

## 2. Scale the check to the change
- Docs, comments or text only: skip checks, or lint those files only
- Config or build files: static check (step 2 below)
- Code: run the full check below

## 3. The check (in order)
1. **Lint/format:** the changed files only. Autofix is allowed on those
   files only.
2. **Static check:** typecheck, compile or build, whichever the repo has.
3. **Tests:** the unit tests related to the change. If the test runner
   can't target them or you're unsure what's affected, run the whole
   unit suite.

Skip any step the repo has no tool for, and say which one you skipped.
Skip tests that need network, secrets or external services, and say so.

## 4. When something fails
- **Already broken?** If it also fails without your change
  (`git stash`, rerun, `git stash pop`), report it. Don't fix it.
- **Flaky?** Rerun once. If it passes, note it as flaky and continue.
- **Caused by you?** Fix it and rerun the check from step 1.
- **Attempt limit:** at most 3 fix attempts. Then stop and report what's
  failing and what you tried.

## 5. Test rules
- Never use --no-verify, and never skip, delete or weaken a test to pass.
- Update an existing test only if the behavior change is intended.
  Say which test and why.
- If you changed behavior and a test runner exists, add one test that
  covers it.
- If the repo has no tests, say so. Don't build a test suite unasked.

## 6. Scope
- Fix only what the check flags in code you changed.
- No unrelated refactors or repo-wide reformatting.

## 7. Report (every commit)
- Which checks ran and which were skipped (and why)
- Pass/fail for each
- Rough total time; if it was slow (over ~2 minutes), flag it
- Any failures that were already there, flaky tests or skipped tests

Commit only when everything that applies passes, or when the only
failures were already there and you've reported them.

## Before merging to main
There's no CI, so run the full suite locally (all tests, including
integration and e2e) before merging a branch or after a large change.
Same failure rules as section 4.

## Git hook (one-time setup)
If there's no pre-commit hook yet, offer to add one that runs the
fast check (lint, static check, unit tests). Ask before installing it.

## Commands
<!-- the agent fills this in once, then I confirm -->
- lint:
- static check:
- unit tests (targeted):
- unit tests (all):
- full suite:
