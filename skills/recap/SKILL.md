---
name: recap
description: Grow a project's story, how the thinking evolved and why, in Souvik's voice, from everything since the last recap.
disable-model-invocation: true
argument-hint: "[setup] [read with <model>] [write with <model>]"
---

# Recap

Keep `recap.md`, one long story per project about how the thinking evolved: what we believed, what we tried, what we chose and gave up, and how and why the thinking moved. The book's shape and rules live in [STORY.md](STORY.md); read it before writing.

Every book lives in the private journals clone (`~/Documents/GitHub/journals/<project>/recap.md`). The project points at its folder through `git config recap.folder`, so nothing in the project's tree changes. All commands go through `scripts/recap` in this skill's folder (`recap` below), run from inside the project. It works the same from Claude Code (`/recap`) and Codex (`$recap`), and both read the talk of both tools.

## Invariants

- **The book is the only thing written.** Talk is read from the transcripts at run time and never saved. The project's own files stay untouched.
- **History, never context.** The book is history. Quote none of it into the project's code, docs or commits.
- **One writer.** Readers may fan out. One writer holds the whole book, so it keeps one voice, one glossary and one line of thought.

## Models

`recap status` shows the defaults (`RECAP_READ_MODEL`, `RECAP_WRITE_MODEL`). Souvik's words in the request override them for this run ("read with haiku", "write with sonnet"), in whichever tool runs Recap. Unset write model: this session writes, which keeps the live context. A named write model: dispatch one writer subagent on it with the reader notes, STORY.md and the voice guide.

## Steps

1. **Status.** Run `recap status`. With no book yet, tell Souvik what setup changes (a folder and `recap.md` in the journals clone, committed and pushed, and `recap.folder` in the project's local git config), wait for a yes, run `recap setup`, then run `recap status` again.

2. **Read everything since the last recap.** `recap sessions` lists each Claude Code and Codex session with talk since `Covered through`, with its size. `recap read <id>` prints one session's talk: each of Souvik's messages and the reply it got. Read the current session through its transcript too, since compaction drops exact words. Add `git log` since the same stamp and the docs that changed.
   - Up to about 60k tokens of talk: read it yourself.
   - More: fan out reader subagents on the read model, at most five (or read the batches one after another where subagents are unavailable), each given a batch of sessions in date order and the `recap read` commands for them. Each returns the moments the thinking moved: what was believed, what changed it, options weighed and rejected, the choice, with exact quotes, timestamps and session ids. Notes only, no prose.
   - Done when every listed session has been read by someone.

3. **Outline when the stretch is big.** On the first run, or when the stretch would add more than three chapters, show the outline and wait for his edits: chapter titles with date ranges and one line each on how the thinking moved, plus any correction footnotes for past chapters.
   - The first run also covers the project's past: old build-journal files in the folder (`recap status` lists them), every available transcript, git history and docs. With no history, the book opens with the premise. Ask up to five questions about the premise and early intent with the outline.

4. **Write.** Load the `souvik` skill for the voice, setting: thinking an idea through, for a smart outsider. When it is unavailable, read `~/.claude/VOICE.md` or `~/.codex/VOICE.md`. Load the `first` skill's method for the question underneath each chapter when available. Write per STORY.md. Done when every moment from step 2 is in a chapter or deliberately left out, every new term is in the glossary, and every footnote resolves.

5. **Commit.** `recap commit "recap: <what moved, a plain phrase>"`. It moves `Covered through` to now, commits as Roy and pushes.

6. **Report in chat**, in this order:
   - A first-principles read of the stretch: what we did and why, whether the reasoning held, and which assumption is carrying the most weight.
   - Contradictions the project now holds, such as a doc that still states a reversed decision. Report them. Fixing is Souvik's call.
   - At most three questions only Souvik can answer, where the answer would change what a chapter means. Put his answers into that chapter in his words, footnoted with the date, and run `recap commit` again. "Don't remember" goes in as not recorded.

7. **Retire the old journal.** After the first run on a project that has build-journal files, and once Souvik approves the book, ask before running `recap retire`. It deletes those files and the `journal.*` git config; the journals repo's history keeps them.
