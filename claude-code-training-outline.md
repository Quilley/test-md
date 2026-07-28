# Claude Code for Risk & Operations — Training Document Outline

**Audience:** Credit risk, market risk infrastructure, stress testing, operations
**Assumed starting point:** CLI-naive, Excel-primary, zero prior terminal exposure
**Format:** Self-paced, 5–6 pages
**Goal state:** User can run Claude Code as a daily driver for analysis, documents, and decks

---

## Section 1 — Why This Exists (½ page)

**Purpose:** Reframe the tool before teaching the tool. Most adoption failures happen here.

Points to cover:
- Claude Code is **not a chatbot**. The distinction: a chatbot talks about your work; Claude Code *operates on your files*.
- It reads the actual `.xlsx` sitting on your drive, computes on it, and writes a new file back.
- Frame the shift as: *"stop copy-pasting data into a chat window, start pointing a tool at your folder."*
- The three things it removes from their week:
  - Manual reconciliation and cross-checking between files
  - Re-typing the same commentary each reporting cycle
  - Rebuilding the same deck / summary structure every month
- One honest line on the tradeoff: it runs in a terminal, which looks unfamiliar for about 20 minutes, and then stops mattering.
- Set the expectation that **you talk to it in plain English.** There is no syntax to memorise.

---

## Section 2 — Your First 15 Minutes (¾ page)

**Purpose:** Get them to a first successful output fast. Nothing conceptual here.

Points to cover:
- Opening it: launch terminal → type `claude` → Enter. Login is SSO and handled centrally; nothing for them to configure.
- **The working directory concept** — the single most important idea for a non-technical user:
  - Claude Code can only see files in the folder you started it from (and its subfolders).
  - Best practice: keep a working folder, drop your files there, start Claude from there.
  - Cover `/add-dir <path>` to grant access to another folder mid-session, and `/cd <path>` to move the session entirely.
- **Referencing a file:** type `@` and start typing the filename — it autocompletes. This is how you point Claude at a specific workbook.
- **Drag and drop:** dragging a file into the terminal window pastes its path.
- The basic loop: you type a request → Claude does work → you read → you refine. Emphasise: **you are expected to iterate, not to get it right in one shot.**
- **Permission prompts:** Claude asks before editing or creating files. Explain that "yes / yes and don't ask again / no" is normal and expected, not an error.
- Key keystrokes:
  - `Esc` — interrupt Claude mid-response (use this liberally when it's going the wrong way)
  - `Shift + Tab` — cycle permission modes
  - `↑` — recall previous prompts
  - `Ctrl + C` twice, or `/exit` — quit
- **First exercise:** point it at a real spreadsheet and ask *"Explain what this workbook contains, tab by tab."* Low risk, immediately impressive, no output file needed.

---

## Section 3 — Commands You Actually Need (1 page)

**Purpose:** Give them a small, curated command set. Do **not** dump the full list — Claude Code ships with 90+ commands and most are for software engineering. Teaching 12 is better than listing 90.

Frame it as: *commands control the tool; plain English controls the work.*

### The essential twelve

| Command | What it does | When they'll use it |
|---|---|---|
| `/help` | Lists everything available | When stuck |
| `/clear` | Wipes the conversation, starts fresh | Every time they switch to a new task |
| `/compact` | Summarises the conversation to free up space | When a long session gets sluggish or forgetful |
| `/context` | Visual grid of what's filling the context window | To diagnose *why* it got sluggish |
| `/add-dir` | Grants access to another folder | Pulling in a file from a different drive location |
| `/cd` | Moves the session to a different folder | Switching to a different project entirely |
| `/model` | Switches the underlying model | Cost/speed vs. depth tradeoff |
| `/resume` | Reopens an earlier conversation | Picking up yesterday's stress test work |
| `/rewind` | Rolls back files and conversation to a checkpoint | When Claude has mangled a file |
| `/export` | Saves the conversation as text | Audit trail, handover, sharing method with a colleague |
| `/copy` | Copies the last response to clipboard | Pasting commentary straight into an email or deck |
| `/usage` (alias `/cost`) | Shows consumption | Cost awareness |

### Worth mentioning briefly (second tier)
- `/init` and `/memory` — create a `CLAUDE.md` file in their working folder that stores standing instructions (e.g. *"our fiscal year ends in March," "always use INR crore," "our risk grades run 1–10"*). Explain this as **"teach it your team's conventions once."** This is the single highest-leverage feature for a repeat-workflow team and deserves a short worked example.
- `/plan` — makes Claude propose an approach before touching anything. Recommend this as the default for anything involving an important file.
- `/btw` — ask a quick side question without polluting the main conversation.
- `/doctor` — self-diagnostic if something is broken, before raising a ticket.
- `/config` — theme and preferences.
- `/deep-research` — multi-source web research with citations, for regulatory or market context.

### Explicitly tell them to ignore
Commands aimed at software workflows (`/code-review`, `/batch`, `/security-review`, `/install-github-app`, `/hooks`, etc.). One line stating these exist and aren't relevant prevents them feeling lost when they type `/`.

---

## Section 4 — What You Can Actually Do (1½ pages)

**Purpose:** The heart of the document. Organised by *their* output type, not by feature. Each item gets a one-line description plus a verbatim example prompt.

### 4.1 Excel — the primary use case

- **Understand an inherited model**
  - *"Walk me through this workbook. List every tab, what it calculates, and which tabs feed which."*
  - *"Trace where the PD input on the Summary tab comes from. Show me the full dependency chain."*
- **Explain and audit formulas**
  - *"Explain the formula in cell H42 in plain English, then tell me if it handles blank rows correctly."*
  - *"Find every hardcoded number sitting inside a formula in this workbook and list them by tab and cell."*
- **Reconciliation and cross-checking**
  - *"Compare the exposure figures in this month's file against last month's. List every line item that moved more than 5%, with the delta."*
  - *"Check whether the totals on the Summary tab actually tie to the underlying detail tabs. Flag any that don't."*
- **Build new outputs**
  - *"Build a summary tab that aggregates exposures by rating grade and industry, with a chart for each."*
  - *"Take this raw extract and produce a clean, formatted workbook with a cover sheet, a data tab, and a pivot-style summary."*
- **Clean messy data**
  - *"This extract has merged cells, blank rows and inconsistent date formats. Clean it into a proper tabular file."*
- **Repeatable transformation**
  - *"Write me a script that takes any monthly file in this format and produces the summary tab automatically."* — introduces the idea of building a reusable tool once, running it every cycle.

### 4.2 Analysis and commentary

- **Variance and movement commentary**
  - *"Compare these two stress test outputs and write variance commentary explaining the main drivers of the change."*
- **Breach and threshold checks**
  - *"Read this limits file and this exposure file. Flag every breach and every position within 10% of its limit."*
- **Sanity checks before submission**
  - *"Review this output for anything that looks wrong — negative values where there shouldn't be, ratios outside plausible ranges, totals that don't foot."*

### 4.3 Documents and reports

- **Draft from data**
  - *"Using the attached results, draft a two-page risk commentary note for the risk committee. Factual tone, no speculation."*
- **Rewrite for audience**
  - *"Rewrite this technical note for a senior audience who won't know the model terminology. Keep it under 400 words."*
- **Summarise long inputs**
  - *"Summarise this 60-page policy document into the ten obligations that affect our reporting process."*
- **Consistency pass**
  - *"Check this document against last quarter's version and list every substantive change."*

### 4.4 PowerPoint

- **Build from a source file**
  - *"Build a 10-slide deck from this stress test output. One slide per scenario, a summary slide up front, and speaker notes on each."*
- **Convert a document to a deck**
  - *"Turn this commentary note into a deck. Keep the narrative order but make each slide standalone."*
- **Refresh an existing deck**
  - *"Update this deck with the new numbers from the attached file. Keep the formatting exactly as it is."*

### 4.5 Small tools and automation

- Frame this carefully — these people are not developers, but they *do* have repetitive tasks worth automating.
- **Single-script executables**: a small tool they run each cycle rather than redoing the work manually.
  - *"Build me a small tool that takes the monthly exposure extract and produces the standard three summary tables as an Excel file."*
- The mental model to give them: **"if you've done it manually three times, ask Claude to build it once."**

### 4.6 Multi-file work

- Emphasise this is where Claude Code beats a chat interface decisively — it can hold a whole folder in view.
  - *"There are twelve monthly files in this folder. Build a single time series of total exposure by rating grade across all of them."*

---

## Section 5 — Writing Prompts That Work (¾ page)

**Purpose:** The skill that separates a frustrated user from a productive one.

### The four rules
1. **Say what the output should be.** "Summarise this" vs. "Summarise this into a one-page Word document with three sections: what changed, why, and what we're doing about it."
2. **Name the audience.** "For the risk committee" produces different writing than "for my team."
3. **Give the constraints up front.** Format, length, tone, what to exclude, which file to use.
4. **Iterate, don't restart.** Correcting is faster and cheaper than re-prompting from scratch. "Good, but make section 2 shorter and drop the caveats" is a complete and valid prompt.

### Include a side-by-side comparison box
- **Weak:** *"Analyse this file."*
- **Strong:** *"Read `Q2_exposures.xlsx`. Compare the June figures against March on the Summary tab. Produce a table of the ten largest movements by absolute value, then write three bullets on the likely drivers. Output as a markdown summary in the chat, not a file."*

Point out explicitly what changed: named file, named comparison, defined output shape, defined length, defined delivery format.

### Two habits worth teaching
- **Ask it to plan first** on anything important: *"Before you change anything, tell me what you're planning to do."*
- **Ask it to check its own work**: *"Now verify those totals against the source and tell me if anything doesn't tie."*

---

## Section 6 — Best Practices: Context, Cost and Control (1 page)

**Purpose:** This is what turns a novice into a daily driver. Expand this section more than instinct suggests — it prevents the two most common failure modes: bloated sessions and runaway cost.

### 6.1 Context management
- **What context is**, in one sentence: everything Claude is currently holding in its head — your prompts, its responses, and every file it has read.
- **Why it matters:** a bloated context makes responses slower, more expensive, and more forgetful.
- Practical rules:
  - **One session, one task.** `/clear` between tasks. This is the single highest-impact habit.
  - Use `/context` when things feel sluggish — it shows exactly what's consuming the window.
  - Use `/compact` for a long session you want to continue; use `/clear` when you're genuinely done with the topic.
  - `/compact` accepts focus instructions: *"/compact keep the reconciliation findings, drop the file exploration."*
  - **Don't ask it to read a 200MB file "just in case."** Point it at what's needed. Reading files is the biggest context consumer.
  - Ask for **targeted reads**: *"Just read the Summary tab"* rather than the whole workbook.
- **Put standing context in `CLAUDE.md`, not in every prompt.** Team conventions, naming standards, house style, units, fiscal calendar. Written once, applied every session.

### 6.2 Cost efficiency
- Cost tracks with tokens, and tokens track with **how much it reads and how long the session runs**.
- Practical levers:
  - `/clear` aggressively — old conversation gets re-sent with every turn.
  - Use `/model` to drop to a faster, cheaper model for simple work (reformatting, summarising, straightforward extraction). Save the heavier model for genuine analysis.
  - Be specific in the first prompt. Three rounds of clarification cost more than one well-formed request.
  - Avoid open-ended exploration on large folders. Narrow the scope, then widen.
  - `/usage` to keep an eye on consumption; make checking it a weekly habit, not a crisis response.
- Counterintuitive point worth stating: **a longer, more detailed prompt is usually cheaper than a short vague one**, because it avoids the back-and-forth.

### 6.3 Control and safety-nets
- **`/plan` before anything consequential.** Read the plan, then approve.
- **Work on copies**, at least for the first few weeks. Build the trust before removing the seatbelt.
- **`/rewind`** if something goes wrong — it restores both files and conversation to an earlier checkpoint.
- **Always verify the numbers.** Claude is fast and usually right; "usually" is not a standard that survives a regulator. Spot-check outputs against source. Say this plainly — the audience will respect it and it pre-empts the objection.
- **`/export`** for anything that needs a record of how a figure was derived.

### 6.4 When *not* to use it
- Being honest here builds credibility for everything else in the document:
  - When the task is three clicks in Excel, just do it in Excel.
  - When it's a live-linked model with volatile external feeds.
  - When the answer needs to come from a system of record, not a file.
- The heuristic: **Claude Code wins on volume, repetition, cross-referencing and drafting.** It doesn't win on trivial one-offs.

---

## Section 7 — Quick Reference Prompt Library (¾ page)

**Purpose:** The page they'll actually keep open. Copy-and-adapt format, grouped by task. Suggested ~15 prompts drawn from Section 4, formatted for direct reuse with `[BRACKETED]` placeholders.

Suggested grouping:
- **Understand** (3 prompts) — explore a file, trace a dependency, explain a formula
- **Check** (3) — reconcile, breach check, sanity review
- **Build** (4) — summary tab, clean file, new workbook, reusable script
- **Write** (3) — commentary, rewrite for audience, summarise a long doc
- **Present** (2) — deck from data, refresh existing deck

---

## Appendix (½ page)

- **Glossary of the six terms they'll hit**: terminal, working directory, session, context window, prompt, model
- **Troubleshooting five-liner**: it can't see my file → check the working directory / use `/add-dir`; it's slow → `/context` then `/compact`; it forgot something → `/clear` and restate; something broke → `/doctor`; it changed the wrong thing → `/rewind`
- **Where to get help** — your internal support channel
- **A suggested 30-day ramp**: week 1 read-only exploration, week 2 build outputs on copies, week 3 one real deliverable, week 4 set up `CLAUDE.md` and a repeatable workflow

---

## Notes on Presentation

- **Every feature needs a verbatim example prompt.** For a CLI-naive audience this is the difference between a document that gets used and one that gets bookmarked and forgotten.
- **Use their vocabulary throughout** — exposure, rating grade, breach, scenario, committee — not generic business examples.
- **Screenshots for Sections 2 and 3 only.** Opening the terminal, the `@` file picker, a permission prompt, `/context` output. Beyond that, screenshots age badly.
- **One worked end-to-end example** somewhere in the middle, showing a full session from launch to finished file. This carries more weight than any list.
- Keep Section 6 dense but scannable — it's the section experienced users return to.
