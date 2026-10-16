# The story

`recap.md` is one long story per project: how the thinking evolved, read from the beginning. The reader is a smart outsider, sharp and new to the project, and Souvik himself weeks or months later, reliving his own reasoning. He is reading, not looking up: every chapter has to carry him to the next.

## Layout

```
> Recap: the story of how the thinking on this project evolved. ...   (header, owned by the script)

Source: <origin url>
Covered through: <ISO UTC stamp>

# <the project, named in words>

## Prologue
## Chapter 1 · <what changed in the thinking, a plain sentence>
*<date range>*
...
## Glossary
## Sources
```

- **Prologue**: the premise. The question the project started with and why it was worth asking, from first principles. Written once, then only corrected.
- **Chapters**: one per stretch where the thinking moved, oldest first. The end of the latest chapter is where things stand, so there is no separate summary of now.
- **Glossary**: each project term with a plain definition and the chapter where it first appears.
- **Sources**: footnote definitions, `[^4-2]` for chapter 4's second note. Each names a file, commit, test, doc, or Souvik's message with its date and session id.
- **Parts**: once themes are clear, chapters may be grouped under `# Part <n> · <name>` headings. Grouping moves headings only, never prose.

## Past chapters stay as written

A chapter records what was thought then. Later chapters tell how the thinking changed, and that change is the story. A past chapter is touched only to fix a fact that was wrong when written: add a footnote `Correction (<date>): ...` and leave the prose. Rewriting a past chapter in hindsight erases the reasoning the book exists to keep.

## What makes a chapter

A chapter exists when the thinking moved: a belief changed, a question was replaced, a choice closed off options, a result surprised, an approach was abandoned. Routine work earns a clause inside a chapter or nothing. A stretch where nothing moved adds nothing to the book, and that is a fine run.

Work through this checklist while writing. It shapes the chapter, never shows as headings:

1. **The question underneath.** Build it up from the mechanism, the way the `first` skill does: what actually determines the answer, in the simplest terms that keep it true.
2. **What we believed going in**, and where that belief came from.
3. **What happened**: the probe, the argument, the result, with real numbers.
4. **The options really on the table**, what each would have cost, and the dead ends. A wrong turn often is how the knowledge was earned, so it stays.
5. **What was chosen and what was given up.**
6. **How the thinking moved, and why.** This is the spine. Put "what I thought then" beside "what I think now" when a belief changed.
7. **His words from the moment**: a short exact quote when one carries the reasoning better than a paraphrase.
8. **What we expected and what would make us revisit**, when recorded.
9. **The open thread** it hands to the next chapter. The chapter ends there.

Open the chapter on the moment the thinking moved, then earn it. Length follows the idea: a small turn is a few paragraphs.

## Truth rules

- **First person covers only what a source shows** Souvik said or did. A motive, expectation or feeling with no source is written plainly as not recorded. Empty is better than invented.
- **Nothing personal.** Life details, money, health, people outside the work, contacts and credentials stay out, even when the talk holds them. The story is the project's thinking.
- **Numbers are copied** from a run output, tracked file or message, with a footnote that lets them be found again. Every number carries its unit and condition.
- **Prose is for reading.** File names, function names, config keys, commands and commit ids live in footnotes only. A project term is defined in plain words the first time it appears, and goes in the glossary.
- **The transcript is evidence of thinking, the repo is evidence of what was built.** When they disagree, the chapter says so.
