# Janus — TUI Design Direction & User Flows

## 1. Product Intent

Janus is a terminal-based testing console for Restricted Claude Code.

Its primary users are testers who need to select test cases, execute them against different models, monitor progress, and retrieve results for external human review.

The TUI should feel simple, predictable, responsive, and reliable.

The intended experience is organised around five home-screen areas:

1. Verify Environment
2. Golden Datasets
3. Test by Filters
4. Active Phases
5. Activity & Results

A conditional Resume option appears first whenever recoverable phases exist.

These are conceptual UX directions, not rigid implementation requirements. The coding agent should inspect the existing TUI and determine how best to accommodate them.

---

## 2. Home Screen

The home screen is the central navigation and monitoring surface.

It should allow users to start new tests while remaining aware of ongoing executions and recent results.

### Conceptual layout

```text
JANUS                                  Workers: 1/2
Restricted Claude Code · Test Console
──────────────────────────────────────────────────

  > Resume Testing (3)                 [conditional]

    1. Verify Environment
    2. Golden Datasets
    3. Test by Filters

──────────────────────────────────────────────────
ACTIVE PHASES                              1/2

  Phase 07 · Golden Suite           RUNNING
  Sonnet 4.6 → Opus 5.5
  ███████████░░░░░░░░░  84/200

  [P] Pause   [S] Stop   [Enter] Inspect

──────────────────────────────────────────────────
ACTIVITY & RESULTS                    View all

  ✓ Phase 06 · Completed · CSV saved
    [Open CSV]

  ! Phase 05 · Completed with errors
    [Open CSV]

  Last environment check: 28 Oct · R

──────────────────────────────────────────────────
↑↓ Navigate · Enter Select · Esc Back · Q Exit
```

This is illustrative, not a requirement for an exact rendering.

### Design principles

- Primary navigation should remain prominent.
- Active phases should appear below navigation.
- Activity and results should remain near the bottom.
- Avoid overwhelming users with detailed logs.
- Use consistent keyboard interactions.
- Preserve a useful layout on smaller terminals.
- Keep the interface responsive during execution.
- Avoid unnecessary screens and confirmation steps.

The home screen should not become an elaborate dashboard.

---

## 3. Flow A — Verify Environment

### Purpose

Allow testers to quickly determine whether they are operating in the correct Claude Code environment.

The distinction between Restricted (R) and Unrestricted (U) is particularly important.

### Flow

```text
Home
  ↓
Verify Environment
  ↓
Run lightweight diagnostics
  ↓
Display environment summary
  ↓
Refresh / Back
```

### Example

```text
JANUS / ENVIRONMENT
────────────────────────────────────

Profile             Restricted (R)
Claude Code         Available
Managed Setup       Detected
Hooks / Policies    Detected

Available Models
  • Sonnet 4.6
  • Opus 5.5

Last checked: 28 Oct, 11:30 AM

[R] Refresh     [Esc] Back
```

The environment screen should be quick and informational.

It may inspect the installed profile, managed configuration, available models, and relevant hooks or policies.

It should distinguish configuration detection from actual enforcement verification.

Where a diagnostic requires a paid call, disclose its approximate cost and obtain confirmation for that operation.

The latest historical verification status can appear as a small line on Home.

Avoid turning environment verification into a complex testing workflow.

---

## 4. Flow B — Golden Datasets

### Purpose

Provide direct access to established golden test collections.

Golden datasets represent a fixed or deliberately maintained subset of test cases.

### Flow

```text
Home
  ↓
Golden Datasets
  ↓
Collection summary
  ├── Browse cases
  └── Run / Verify
         ↓
     Select model(s)
         ↓
     Execution preview
         ↓
     Confirm estimated cost
         ↓
     Start phase
         ↓
     Return to Home
     with active phase visible
```

### Collection summary

```text
JANUS / GOLDEN DATASETS
────────────────────────────────────

Golden Test Collection

Total Cases       100
Intents           8

  > Run / Verify
    Browse Cases
    View Collection Details

[Esc] Back
```

The tester should be able to run the collection without individually inspecting every case.

Browsing cases is available when needed.

The underlying dataset structure should follow the existing implementation unless improvements are justified.

### Model selection

A useful direction is to allow testers to select multiple models in a particular order.

For example:

```text
Selected models

  1. Sonnet 4.6
  2. Opus 5.5

Execution order:
Sonnet 4.6 → Opus 5.5
```

One phase would execute the selected cases across those models sequentially, occupying one worker at a time.

The coding agent should evaluate the feasibility of this behaviour rather than assuming it already exists.

---

## 5. Flow C — Test by Filters

### Purpose

Allow testers to construct a test selection using existing case metadata, especially intent.

This differs from Golden Datasets, where the collection is predefined.

### Flow

```text
Home
  ↓
Test by Filters
  ↓
Choose available filters
  ↓
Preview matching cases
  ↓
Select model(s)
  ↓
Review execution configuration
  ↓
Confirm estimated cost
  ↓
Start phase
  ↓
Return Home
```

### Example

```text
JANUS / TEST BY FILTERS
────────────────────────────────────

Filter by Intent

  [x] File access
  [x] Policy enforcement
  [ ] Network access
  [ ] Tool restrictions

Matching cases: 42

  > Continue
    View Matching Cases
    Reset Filters

[Esc] Back
```

The exact filters should come from the existing case schemas and metadata.

Golden Datasets and Test by Filters should ideally converge on the same execution mechanism.

Only the case-selection experience needs to differ.

Individual case selection is a good-to-have, not an essential initial requirement.

---

## 6. Execution Preview & Confirmation

Both Golden Datasets and Test by Filters should converge on a compact execution confirmation.

### Example

```text
JANUS / CONFIRM EXECUTION
────────────────────────────────────

Selection        Golden Dataset
Cases            100

Models
  1. Sonnet 4.6
  2. Opus 5.5

Total executions 200
Estimated cost   ₹240
Workers free     1/2

  > Start Phase
    Back

────────────────────────────────────
Cost is approximate.
```

The estimate should reuse Janus's existing cost calculation.

Actual cost may be recorded when reliable usage information is available.

Once the tester confirms, Janus creates a phase and moves execution monitoring to the persistent Active Phases area.

The user should not be trapped inside a dedicated running screen.

---

## 7. Flow D — Active Phases

### Purpose

Allow testers to monitor and control ongoing executions while continuing to navigate Janus.

### Execution concepts

**Phase:** A logically independent testing run with selected cases, model configuration, progress, and evidence.

**Worker:** The underlying execution resource responsible for processing that phase.

The intended initial limit is two concurrently executing phases.

A single phase may execute multiple models sequentially.

### Home interaction

```text
ACTIVE PHASES                         2/2

Phase 01 · Golden Suite           RUNNING
Sonnet 4.6 → Opus 5.5
████████████░░░░░░░░  120/200

Phase 02 · Intent: File Access    RUNNING
Sonnet 4.6
███████░░░░░░░░░░░░░   35/100

[Enter] Manage selected phase
```

Selecting a phase opens its contextual management view.

### Phase management

```text
JANUS / PHASE 01
────────────────────────────────────

Status           Running
Collection       Golden Suite
Current model    Opus 5.5
Current case     CASE-021

Completed        120/200
Execution errors 3
Cost             ₹... (if available)

  > Pause
    Stop
    Back
```

The interface should prioritise progress and status rather than streaming extensive Claude Code output.

Live output inspection is optional.

### Independent operation

- Pausing Phase 1 does not interrupt Phase 2.
- Stopping Phase 1 does not interrupt Phase 2.
- A completed or safely paused phase releases its worker.
- A third phase cannot start while both workers are occupied.

When capacity is exhausted, show a simple message:

```text
All workers are occupied.

Two phases are currently executing.
Wait for a worker to become available,
or pause/stop an active phase.

[Enter] OK
```

Automatic queueing is not required initially.

The two-worker implementation must be investigated for safety, resource consumption, and compatibility with the existing scripts.

---

## 8. Pause, Stop, Exit & Resume

These operations must have clear and consistent meanings.

### Pause

Pause means safely interrupting future execution while preserving recoverable progress.

Preferred behaviour:

1. Stop scheduling additional cases.
2. Allow the current case to finish safely where possible.
3. Persist progress and available evidence.
4. Release the worker.
5. Mark the phase as Paused.

### Stop

Stop means permanently ending the phase.

Previously recorded evidence must remain available.

Stopped phases should not appear in the Resume list.

### Exit Janus

If active phases exist, exiting should offer:

```text
2 phases are currently running.

Pause all active phases safely and exit?

  > Yes, Pause & Exit
    Cancel
```

On confirmation, Janus should safely pause all active phases, persist their recovery state, and close.

If safe pausing fails, the interface must report the failure rather than silently claiming the work is saved.

### Resume

When recoverable phases exist, Resume appears as the first option on Home.

```text
JANUS / RESUME
────────────────────────────────────

Saved phases: 5

 > Phase 01 · Sonnet 4.6
   Golden · 62/100 · Paused

   Phase 02 · Opus 5.5
   Golden · 28/100 · Paused

   Phase 03 · Sonnet 4.6
   Calibration · 91/100 · Interrupted

   Phase 04 · Opus 5.5
   Policy · 44/100 · Paused

   Phase 05 · Sonnet 4.6
   Golden · 10/100 · Paused

[Enter] Inspect / Resume
[Esc] Back
```

Selecting Resume opens the saved-phase list; it does not automatically restart all phases.

A tester chooses which phase to resume.

Resuming must respect the two-worker limit.

Completed case executions should not be repeated unnecessarily. Interrupted cases need a clearly defined recovery policy.

If the environment or relevant configuration has changed since the original run, Janus should warn the tester.

---

## 9. Flow E — Activity & Results

### Purpose

Provide persistent, lightweight evidence that test executions have been recorded.

Human review happens outside Janus.

### Home activity area

```text
ACTIVITY & RESULTS                   View all

✓ Phase 06 · Execution completed
  Sonnet 4.6 · 100/100 · CSV saved
  [Open CSV]

! Phase 05 · Completed with errors
  Opus 5.5 · 92 executed · 8 errors
  [Open CSV]

Last run: 28 Oct
```

### Completion notification

When a phase finishes, display a non-blocking notification near the bottom of the TUI.

Example:

```text
✓ Phase 06 completed

100 cases processed
CSV evidence saved successfully

[Open CSV]   [Dismiss]
```

If technical errors occurred:

```text
! Phase 06 completed with errors

92 cases executed
8 technical errors
Partial evidence recorded

[Open CSV]   [Details]
```

A technical execution error should not be confused with a test failing a human evaluation.

Janus should not automatically retry failed cases.

### Persistent history

Activity records should survive Janus restarts.

The home screen can show the latest few entries, with an option to open a scrollable history.

Selecting Open CSV launches the file using the operating system's default spreadsheet application.

Opening the file should not block Janus or interfere with active workers.

If the file cannot be opened, show the path and an actionable error.

Activity history and Resume may share the same underlying persisted execution records, but their user-facing purposes differ.

---

## 10. Evidence & Reporting

Janus records evidence; humans review it externally.

The system should retain enough information to understand:

- Which test cases executed.
- Which model was used.
- When execution occurred.
- Which environment and configuration were involved.
- Whether execution completed, failed, stopped, or was interrupted.
- Where outputs and supporting artifacts were saved.
- What execution costs were estimated or observed.

A human-friendly master CSV that enables historical comparisons is a potential improvement.

However, its schema and storage architecture should be evaluated against the existing implementation.

Avoid making a progressively widening CSV the only source of truth if doing so would compromise traceability or reliable recovery.

---

## 11. UX and Implementation Priorities

### Core experience

- Quick environment awareness.
- Straightforward golden dataset execution.
- Flexible filtered test selection.
- Clear cost confirmation.
- Persistent active-phase monitoring.
- Independent pause and stop controls.
- Safe exit and recovery.
- Persistent completion notifications.
- Direct access to CSV evidence.

### High-value engineering investigation

- Two independent execution workers.
- Worker isolation and subprocess ownership.
- Safe checkpointing and resumption.
- Reliable evidence persistence.
- Sequential multi-model execution within a phase.

### Good-to-have capabilities

- Individual case selection.
- Live Claude Code output inspection.
- Advanced historical comparisons.
- More sophisticated multi-model execution.
- Additional worker capacity.
- Enhanced filtering and discovery.

These should not be implemented merely because they are described here.

---

## 12. Instructions for the Coding Agent

This document describes the intended user experience, not a fixed engineering blueprint.

Start by exploring the existing Janus TUI.

For each flow:

1. Determine how it currently works.
2. Identify what already satisfies the intended experience.
3. Find friction or reliability problems.
4. Consider simpler or better alternatives.
5. Assess feasibility and implementation cost.
6. Identify regression and data-integrity risks.
7. Recommend the smallest worthwhile change.

The TUI should guide the design of the underlying system, but existing engineering constraints must be respected.

A solution might involve a small patch, a new screen, an execution-layer refactor, or a larger redesign. Choose based on evidence rather than preference.

Prioritise simplicity, reliability, and tester usability over feature completeness.

Do not modify shipping code until the proposed direction has been reviewed and authorised.
