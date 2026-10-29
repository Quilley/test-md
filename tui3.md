# Janus TUI: Simplified Design Proposal

**Status:** Proposal for review. No shipping code is to be modified until this direction is reviewed and authorised.
**Supersedes:** "Janus: TUI Design Direction & User Flows" (five-area home screen).

---

## 1. Summary

Janus is a terminal testing console for Restricted Claude Code. Testers pick test cases, run them against one or more models, watch progress, and retrieve CSV evidence for external human review.

The original direction has five home areas plus a conditional Resume, and about eight screens behind them. This proposal reduces that to **one home screen, one creation flow, and one phase-detail view**.

| Original | Proposed |
|---|---|
| Verify Environment (menu item and flow) | Always-visible header badge. Detail view on demand |
| Golden Datasets (flow) | A source inside **New Test** |
| Test by Filters (flow) | A source inside **New Test** |
| Execution Preview, then Confirm (two screens) | One **Configure & Start** screen |
| Active Phases | Part of the single **Phases** list |
| Resume (separate screen) | A status on a Phases row. Press `R` |
| Activity & Results | Part of the single **Phases** list |

The core idea: **a phase is one persisted record with a status.** Running, paused, interrupted, completed and errored are states of the same object, not separate screens. Once that holds, Active Phases, Resume and Activity & Results are three views of the same list, so they become one list.

---

## 2. Design Principles

1. **One list, one record.** Every phase appears once, with a status. Nothing is duplicated across screens.
2. **Direct keys over menu navigation.** The most common actions are single keystrokes shown on screen.
3. **Never trap the user.** Starting a phase returns to Home. Monitoring is always visible. There is no dedicated "running" screen.
4. **Confirm only what is costly or irreversible.** Cost before start. Stop. Quit with live phases. Nothing else.
5. **Disable instead of interrupting.** If an action is unavailable (for example, workers are full), show it disabled with an inline reason. Do not raise a modal.
6. **Status over logs.** Show progress, counts and state. Live Claude Code output is out of scope.
7. **Never claim what was not verified.** Saved means saved. Enforced means verified. Failures to pause or save are reported, not hidden.

---

## 3. Home Screen

Home is the only top-level screen. It has a header, a small action area, and the Phases list.

```
JANUS                      Restricted (R) ✓   Workers 1/2
Restricted Claude Code · Test Console
────────────────────────────────────────────────────────
> New Test
  Environment details

────────────────────────────────────────────────────────
PHASES

  07  Golden Suite                          RUNNING
      Sonnet 4.6 → Opus 5.5
      ████████████░░░░░░░░  84/200

  03  Policy · Intent filter                PAUSED
      Sonnet 4.6
      ███████████████████░  91/100

  06  Golden Suite                          ✓ DONE
      Sonnet 4.6 · 100/100 · CSV saved

  05  Golden Suite                          ! DONE · 8 errors
      Opus 5.5 · 92 executed · 8 errors · CSV saved

────────────────────────────────────────────────────────
N New   P Pause   R Resume   S Stop   O Open CSV
Enter Details   ↑↓ Move   Q Quit
```

**Behaviour**

- Phases are sorted: running first, then paused or interrupted, then finished (newest first).
- The list scrolls. There is no separate "View all" screen.
- Hotkeys act on the selected row and are shown dimmed when not applicable (for example, `R` on a running row).
- On small terminals, each row collapses to one line: `07 Golden 84/200 RUNNING`.
- A header with no recoverable phases simply shows no paused rows. There is no conditional "Resume (n)" menu item. Paused and interrupted rows are visible and marked.

---

## 4. Environment Awareness

### 4.1 Header badge

The environment profile is the most important fact a tester needs before running anything, so it is always visible in the header.

| Badge | Meaning |
|---|---|
| `Restricted (R) ✓` | Restricted profile detected. Last check is recent |
| `UNRESTRICTED (U)` | Shown in a warning style. Impossible to miss |
| `Unknown ?` | Check failed or not yet run |
| `Restricted (R) ⚠ changed` | Configuration differs from the last verified state |

### 4.2 Check cadence

- **On launch:** run the free, local checks (installed profile, managed configuration, hooks and policies, available models). These are quick and cost nothing.
- **On demand:** `Environment details` opens a summary, with `R` to refresh.
- **Paid diagnostics:** never run automatically. When a diagnostic needs a paid call, show the approximate cost and require confirmation for that operation only.

### 4.3 Environment detail view

```
JANUS / ENVIRONMENT
────────────────────────────────────
Profile             Restricted (R)
Claude Code         Available
Managed Setup       Detected
Hooks / Policies    Detected

Available Models
  • Sonnet 4.6
  • Opus 5.5

Checks run          Detection only
Enforcement         Not verified      [V] Verify (≈ ₹__)
Last checked        29 Oct, 11:30 AM

R Refresh   Esc Back
```

**Detection and enforcement are shown separately.** "Hooks detected" does not mean "hooks are enforcing". Enforcement verification is the paid, opt-in action.

### 4.4 Guard before starting a phase

If the environment is `Unknown`, `Unrestricted`, or `changed` since the last verification, **Configure & Start** shows a one-line warning above the Start action. It does not block, because the tester may be intentionally testing the Unrestricted profile. The environment is recorded in the phase's evidence either way.

---

## 5. Flow: New Test

One flow covers both Golden Datasets and Test by Filters. They differ only in how cases are chosen. Everything after selection is shared.

```
Home → N
   ↓
Choose source
   ↓
Configure & Start
   ↓
Back to Home (phase visible, running)
```

That is two screens, down from six or seven.

### 5.1 Step 1: Choose source

```
JANUS / NEW TEST
────────────────────────────────────
> Golden Suite            100 cases · 8 intents
  By Intent               choose filters

Esc Back
```

- **Golden Suite** goes straight to Configure & Start with the whole collection selected.
- **By Intent** opens a filter checklist with a live matching count:

```
JANUS / NEW TEST / BY INTENT
────────────────────────────────────
  [x] File access            24
  [x] Policy enforcement     18
  [ ] Network access         31
  [ ] Tool restrictions      27

Matching cases: 42

Space Toggle   A All   C Clear
Enter Continue   Esc Back
```

The filters come from the existing case schema and metadata. Intent is the first filter. Others are added only if the schema already carries them. Browsing individual cases is optional (`B` on either screen) and not a required step.

### 5.2 Step 2: Configure & Start

Model choice, preview and cost confirmation share one screen.

```
JANUS / CONFIGURE & START
────────────────────────────────────
Selection        Golden Suite
Cases            100

Models (run in this order)
  [1] Sonnet 4.6
  [2] Opus 5.5
  [ ] —

Total executions   200
Estimated cost     ≈ ₹240   (approximate)
Workers free       1/2
Environment        Restricted (R) ✓

> Start Phase
  Back
```

**Behaviour**

- Selecting a model appends it to the order. Selecting it again removes it.
- Executions and cost update live as models change.
- The cost estimate reuses the existing Janus cost calculation. It is labelled approximate.
- If both workers are busy, **Start Phase** is disabled, with the reason inline:

```
  Start Phase  (disabled)
  Both workers are busy. Pause or stop a phase to free one.
```

- Pressing Start creates the phase and returns to Home. The phase appears in the list as `RUNNING`.

### 5.3 Multi-model execution

One phase can execute its cases against several models sequentially, occupying one worker. This is the simple version: the phase iterates models in the selected order, and each model completes all selected cases before the next begins. Anything more elaborate (interleaving, parallel models inside one phase) is out of scope.

Feasibility depends on the existing execution scripts and must be confirmed during investigation (see Section 11).

---

## 6. Flow: Phase Detail

`Enter` on any row opens its detail view. It is contextual to the phase's status.

```
JANUS / PHASE 07
────────────────────────────────────
Status           Running
Source           Golden Suite
Current model    Opus 5.5  (2 of 2)
Current case     CASE-021

Completed        84/200
Technical errors 3
Cost             ≈ ₹__ (observed, if available)
Environment      Restricted (R)

P Pause   S Stop   O Open CSV   Esc Back
```

For finished phases, the view shows the summary, the evidence path, and `O` to open the CSV. For paused or interrupted phases, it shows `R` to resume.

The same actions work from the Home row without opening this view. The detail view exists for those who want the context, not as a required step.

---

## 7. Phase Lifecycle

### 7.1 States

| State | Meaning | Worker held? | Resumable? |
|---|---|---|---|
| Running | Executing cases | Yes | n/a |
| Paused | Safely interrupted by the user | No | Yes |
| Interrupted | Ended unexpectedly (crash, kill, power loss) | No | Yes |
| Done | All cases processed, no technical errors | No | No |
| Done with errors | All cases processed, some technical errors | No | No (see 7.6) |
| Stopped | Permanently ended by the user | No | No |

Stopped phases remain in history but are not offered for resume.

### 7.2 Pause

Pause means safely interrupting future work while preserving recoverable progress.

1. Stop scheduling new cases.
2. Let the current case finish where possible.
3. Persist progress and evidence.
4. Release the worker.
5. Mark the phase `PAUSED`.

No confirmation is required. Pause is non-destructive.

While the current case finishes, the row shows `PAUSING…`. If the case does not finish within a reasonable bound, the tester can choose to abandon it. That case is then marked interrupted and re-run on resume.

### 7.3 Stop

Stop permanently ends the phase. It requires **one inline confirmation**, because it is irreversible:

```
Stop Phase 07 permanently? Evidence recorded so far is kept.
  > Stop        Cancel
```

Previously recorded evidence is preserved. The worker is released.

### 7.4 Quit

If no phases are running, Quit exits immediately. If phases are running:

```
2 phases are running.
Pause all safely and exit?

  > Yes, Pause & Exit
    Cancel
```

On confirmation, Janus pauses every running phase, persists recovery state, then exits. **If any pause fails, Janus does not exit silently.** It reports which phase failed and what state it is in, and lets the tester decide.

### 7.5 Resume

Resume is `R` on a `PAUSED` or `INTERRUPTED` row. There is no separate screen and no "resume all".

- Resume is blocked (disabled with reason) when both workers are busy.
- Before resuming, Janus compares the current environment and configuration against the phase's recorded ones. If they differ, it warns the tester and asks them to confirm.
- **Recovery policy:**
  - Completed cases are never re-run.
  - An interrupted case is re-run from the start and marked as such in the evidence.
  - Cases with technical errors are not retried automatically.

### 7.6 Technical errors

A technical execution error (the harness or the call failed) is not the same as a test failing a human evaluation. Janus labels them differently everywhere and never auto-retries. A phase "done with errors" is closed. Re-running its failed cases is a manual, deliberate action (starting a new phase from those cases), not a resume. Whether to offer that shortcut is deferred.

---

## 8. Workers

- **Limit:** two concurrent phases.
- **A phase holds a worker only while running or pausing.** Paused, interrupted, done and stopped phases hold none.
- **Isolation:** pausing or stopping one phase never affects the other.
- **No automatic queueing** in the first version. When both workers are busy, starting or resuming is disabled with an inline explanation.

The two-worker design is the highest-risk engineering item. It must be investigated before it is committed to (see Section 11).

---

## 9. Notifications and Activity

### 9.1 Completion toast

When a phase finishes, a non-blocking one-line notice appears at the bottom of the screen and fades after a few seconds. It never steals focus or blocks keys.

```
✓ Phase 06 completed · 100 cases · CSV saved        [O] Open
! Phase 05 completed with errors · 92 run · 8 errors [O] Open  [Enter] Details
```

### 9.2 History is the Phases list

There is no separate Activity area. The permanent record of a completed phase is its row in Phases, which survives restarts because it comes from the same persisted store as everything else.

### 9.3 Open CSV

`O` on a finished phase opens its CSV in the operating system's default application.

- It runs detached. It never blocks Janus or touches active workers.
- If it cannot be opened, Janus shows the file path and a specific, actionable error.

---

## 10. Evidence and Data Model

Janus records evidence. Humans review it outside Janus.

### 10.1 Source of truth

Each phase writes **per-case records** as it executes (JSONL, or SQLite if the repository already uses a database). This is the source of truth for progress, recovery, history and exports.

**CSV is an export generated from those records.** It is never the only copy. A growing wide master CSV is convenient for humans but poor for recovery and traceability, so it should not be the primary store.

### 10.2 Per-case record (minimum)

- Phase ID, case ID, intent
- Model
- Start and end time
- Outcome: `completed`, `technical_error`, `interrupted`, `stopped`
- Environment and configuration identifier
- Path to outputs and supporting artifacts
- Estimated cost and, when reliable, observed cost

### 10.3 Per-phase record (minimum)

- Phase ID, source (Golden or intent filter set), selected case IDs
- Ordered model list
- Status and timestamps
- Environment profile and configuration fingerprint at start
- Estimated total cost, observed cost if available
- Evidence directory and CSV path

### 10.4 Master CSV (optional)

A cross-phase CSV for historical comparison is a worthwhile later addition, generated from the records above. Its schema should be decided against the existing implementation and is deferred.

---

## 11. Instructions for the Coding Agent

**This is a design direction, not a blueprint. Do not modify shipping code until the proposal is reviewed and authorised.**

### 11.1 Investigation (read-only)

For each flow below, inspect the existing TUI and scripts and report:

1. How it works today.
2. What already satisfies the intended experience.
3. Friction and reliability problems.
4. Simpler or better alternatives.
5. Feasibility and implementation cost.
6. Regression and data-integrity risks.
7. The smallest worthwhile change.

**Flows to review:** Home layout, Environment, New Test (Golden and filters), Configure & Start (cost and multi-model), Phase lifecycle (pause, stop, quit, resume), Notifications and Open CSV, Evidence persistence.

### 11.2 Specific questions to answer

1. **Phase record:** Is there already a persisted record per run? Can it carry status, selected cases, model order and environment, so that Home, Resume and history can all read from it?
2. **Workers:** Can two executions run concurrently without shared-state conflicts (working directories, temp files, config, lock files, rate limits, evidence paths)? How are subprocesses owned, tracked and cleaned up?
3. **Pause and checkpointing:** Can execution stop between cases cleanly? What is the true unit of recovery?
4. **Multi-model phases:** Do the scripts accept an ordered model list, or run one model per invocation? What is the cost of looping in the TUI layer versus the execution layer?
5. **Cost:** Where does the existing cost calculation live? Can it be called with a case count and a model list without side effects?
6. **Environment checks:** Which checks can run locally and for free? Which need a paid call? Can detection and enforcement be separated cleanly?
7. **Evidence:** What does the current CSV contain? Can it be regenerated from per-case records, and if not, what is missing?
8. **Terminal behaviour:** How does the current TUI handle small terminals, keyboard input and redraw while workers run?

### 11.3 Recommended delivery order

Smallest and safest first. Each step should be independently reviewable and shippable.

1. **Phase record and per-case evidence.** Foundation for everything else. No UI change required.
2. **Home with the unified Phases list** and the environment header badge.
3. **New Test flow:** Golden Suite, then By Intent, with Configure & Start.
4. **Pause, Stop and Quit** with the recovery policy.
5. **Resume** with the environment-change warning.
6. **Second worker**, only after the investigation confirms it is safe.
7. **Completion toast and Open CSV.**

Steps 1 and 2 give testers most of the value even if the second worker is later deferred.

---

## 12. Scope

### Included

- Header environment badge and detail view
- New Test: Golden Suite and By Intent
- Ordered multi-model selection within one phase
- Configure & Start with cost confirmation
- Unified Phases list with status
- Pause, Stop, Quit, Resume with a defined recovery policy
- Completion toast, Open CSV
- Per-case evidence records with CSV export

### Dropped from the original direction

- Collection Details screen
- Separate Resume screen
- Separate Activity & Results area and "View all" screen
- The "All workers occupied" modal (replaced by a disabled Start with an inline reason)
- Separate Execution Preview and Confirm screens

### Deferred (not to be built unless justified)

- Individual case selection
- Live Claude Code output inspection
- Automatic queueing
- More than two workers
- Cross-phase master CSV and historical comparison
- Retry-failed-cases shortcut
- Filters beyond intent

---

## 13. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Two workers share state in existing scripts | Corrupted evidence, flaky runs | Investigate first. Per-phase working and evidence directories. Ship with one worker if unsafe |
| Pause cannot stop cleanly mid-case | Lost or duplicated work | Define the case as the atomic unit. Interrupted cases re-run and are marked |
| CSV is the only current store | Weak recovery | Introduce per-case records before any UI work |
| Cost estimate drifts from reality | Tester surprise | Label as approximate. Record observed cost when reliable |
| Tester confuses technical error with test failure | Misread results | Separate labels and CSV columns throughout |
| Hotkeys collide with terminal or multiplexer bindings | Unusable keys | Verify in common terminals. Keep arrow and Enter navigation as a full fallback |
| Detection mistaken for enforcement | False assurance | Show both separately. Never label detection as "verified" |

---

## 14. Open Questions for Review

1. Is the **first version limited to intent filters**, or does the existing schema justify more?
2. Should starting a phase in an **Unrestricted** environment be allowed with a warning (proposed), or blocked?
3. Is it acceptable for **Stop** to require a confirmation, given the goal of minimal prompts?
4. Does the existing **evidence format** need to remain backward compatible with past CSVs?
5. Is a **retry-failed-cases** action needed soon, or can it wait?
6. What is the acceptable **bound for a case to finish** when pausing before it can be abandoned?
