---— TUI-First Brownfield Exploration & Engineering Strategy

Mission

You are entering an existing codebase with limited prior context.

Your task is to understand Janus, an existing terminal-based testing application, and determine how it should evolve to deliver a simpler, more reliable, and more effective experience for its testers.

This is an open-ended engineering and product-design investigation, not a feature implementation checklist.

You are expected to use your own engineering judgement, challenge the ideas in this brief, discover better alternatives, and recommend the most practical direction based on the actual implementation.

Start from the tester experience, then trace inward through the TUI, application logic, execution scripts, subprocesses, persistence, and infrastructure.

The desired user experience should inform the architecture. The existing architecture should inform what is practical.

Neither is automatically correct.

1. Understand the Product

Janus is a terminal interface used by testers to evaluate a restricted distribution of Claude Code intended for business users.

Restricted Claude Code operates under managed configuration, hooks, and policy constraints. Testers may operate in restricted (R) or unrestricted (U) environments.

Janus orchestrates tests, invokes existing scripts and Claude Code, captures execution results, and generates evidence for external human review.

Test cases are primarily JSON-based and may use different schemas.

The existing application uses Rich and Questionary.

These details provide initial context. Verify them against the repository rather than assuming they are complete or accurate.

The primary users are testers, not developers of Janus.

They should be able to understand their environment, select tests, execute them, monitor progress, recover interrupted work, and retrieve evidence with minimal friction.

2. Operating Philosophy

TUI-first, not architecture-first

Begin by understanding what the tester sees and does.

Identify the most natural user journeys before deciding how the underlying implementation should change.

Do not let existing internal abstractions dictate unnecessarily complicated interactions.

Equally, do not invent elaborate interfaces when simple menus, status lines, and contextual actions would suffice.

Simplicity is the default

Prefer the smallest reliable solution that delivers the intended user benefit.

A complex solution must demonstrate a meaningful advantage over a simpler alternative.

Evaluate whether the additional capability justifies its implementation cost, maintenance burden, and failure risk.

Brownfield pragmatism

The appropriate solution may be:

- A small patch.
- A navigation or presentation improvement.
- Reuse of existing functionality.
- A modest refactor.
- A new component.
- Replacement of a subsystem.
- A larger architectural change.

Do not assume that preserving everything is always desirable.

Do not assume that rebuilding is inherently better.

Choose the least disruptive approach that adequately solves the problem.

Challenge the brief

Treat every proposed feature and workflow as a hypothesis.

You may reject, simplify, combine, or replace an idea when you can demonstrate a better alternative.

Explain why.

Do not optimise for agreement with the brief.

3. Discover the Actual System

Start from the application's TUI entry point.

Trace the user-facing workflows into their actual implementations.

Understand:

- How menus and screens are rendered.
- How users navigate and make selections.
- How test cases are discovered and organised.
- How JSON schemas and filters are handled.
- How models are selected.
- How execution scripts are invoked.
- How Claude Code processes are created and managed.
- How costs are estimated and recorded.
- How progress and errors are communicated.
- How results and CSVs are generated.
- How state survives—or fails to survive—application restarts.
- How current tests validate these behaviours.

Inspect repository instructions, relevant documentation, existing tests, and execution contracts.

Trace real call paths. Do not rely solely on filenames, comments, or architectural diagrams.

Where safe and feasible, run the existing application and representative non-destructive tests.

Avoid paid API calls, live policy changes, destructive operations, or uncontrolled execution during discovery.

If runtime verification is unavailable, state exactly what remains unverified.

4. Desired Tester Experience

The following is a conceptual direction, not a prescribed screen architecture.

Environment awareness

Testers should quickly determine whether they are in the intended R/U environment and what capabilities are available.

A lightweight diagnostic view may show the profile, managed configuration, relevant hooks, available models, and previous check information.

Avoid turning this into a complicated verification workflow.

Golden datasets

Testers should easily discover and execute established golden test collections.

Preserve existing collection definitions and schemas where practical.

Make it easy to understand what will execute before starting.

Test by filters

Testers should be able to select cases using existing metadata, such as intent.

Explore whether filtered selection and golden datasets can share a common execution pathway.

Avoid duplicated execution logic.

Active execution

Testers should be able to monitor ongoing work without losing access to the rest of the TUI.

Explore a compact, persistent execution area showing active phases, progress, errors, and relevant controls.

Activity and evidence

Testers should be able to find recent and historical executions, understand their technical status, and open recorded CSVs in the operating system's default spreadsheet application.

Activity should persist across application restarts.

Human review takes place outside Janus.

Do not introduce an LLM judge or an elaborate in-terminal review system.

5. Execution Model — Investigate, Do Not Assume

The desired direction includes independently manageable testing phases.

Potential behaviours:

- Start a phase from selected cases and model configuration.
- Monitor its progress.
- Pause safely.
- Resume saved work.
- Stop permanently while preserving evidence.
- Exit Janus by safely pausing active work.
- Recover from unexpected interruption.
- Maintain persistent execution history.
- Execute selected cases sequentially across multiple models within one phase, if feasible.

A paused phase should be recoverable. A stopped phase should remain recorded but not resumable.

The home interface may show Resume as its first option when recoverable work exists.

These behaviours are product intentions.

Determine which are already supported, which can be implemented simply, and which require significant architectural changes.

Do not introduce a sophisticated orchestration framework without evidence that it is necessary.

6. Priority Investigation: Parallel Workers

Treat parallel execution as a high-leverage technical investigation.

The initial product target is up to two concurrently executing phases, with one worker responsible for each phase.

A phase may eventually execute multiple models sequentially.

However, do not assume two concurrent workers are safe, efficient, or even feasible in the existing architecture.

Investigate the actual execution mechanism.

Process isolation

Determine:

- Whether Claude Code invocations are independent.
- Whether workers share mutable configuration or session state.
- Whether managed Claude Code hooks and policies behave correctly under concurrency.
- Whether working directories, temporary files, logs, and output paths can collide.
- Whether subprocess ownership and cleanup are reliable.

Execution coordination

Determine:

- Whether the TUI can remain responsive while work executes.
- Whether existing scripts are synchronous or asynchronous.
- Whether multiprocessing, subprocesses, threads, or another simple mechanism best fits the application.
- How worker capacity should be enforced.
- Whether one worker failure can affect another.
- Whether process termination can leave orphaned Claude Code processes.

Do not equate asynchronous UI updates with genuine parallel execution.

Persistence and recovery

Determine:

- What constitutes a safe checkpoint.
- Whether an interrupted case can be distinguished from a completed case.
- How partial evidence is preserved.
- How duplicate executions are prevented or clearly recorded.
- How paused work can resume after restarting Janus.
- Whether writes to shared CSVs or state files can conflict.
- What happens after a process crash, forced termination, or machine restart.

Prefer simple, durable recovery mechanisms.

Resource and cost implications

Investigate:

- Memory and CPU requirements.
- Concurrent Claude Code session behaviour.
- API rate limits and throttling.
- Cost estimation and actual usage tracking.
- Potential contention between workers.
- Performance under one versus two active phases.

Where feasible, use controlled, low-cost experiments.

Compare alternatives

At minimum, compare:

1. Existing sequential execution with improved TUI responsiveness.
2. Two independently managed execution workers.
3. A more substantial orchestration redesign, only if justified.

For each, evaluate user benefit, implementation effort, reliability, operational risk, and maintainability.

Do not assume that maximum parallelism delivers the best tester experience.

7. Failure-Oriented Engineering

Assume the system will encounter interruptions and partial failures.

Investigate failure scenarios such as:

- Janus closes unexpectedly.
- A worker crashes.
- Claude Code hangs or times out.
- A case produces partial output.
- A CSV write fails.
- Two workers attempt to write the same file.
- A tester pauses while a case is executing.
- A tester stops a phase during evidence capture.
- A previously saved phase resumes under a changed environment.
- The terminal becomes too small.
- A spreadsheet cannot be opened.

For each significant scenario, determine whether the current system handles it and what the simplest safe recovery mechanism would be.

Avoid claiming that work is completed, saved, or resumable unless the underlying state supports that claim.

Do not automatically retry failed cases. Preserve technical failures for external review.

8. Explore Better UX Alternatives

Do not limit yourself to the five conceptual home areas.

Evaluate whether they should be:

- Separate menu entries.
- Contextual views.
- Persistent status sections.
- Collapsible summaries.
- Combined workflows.
- Different navigation structures.

Investigate the trade-offs.

Prefer a coherent, keyboard-friendly experience that works within the capabilities of Rich and Questionary.

Avoid adding dependencies unless they materially improve usability or reliability.

Make the important actions obvious and keep secondary complexity out of the way.

9. Evaluate Improvements Systematically

For each meaningful recommendation, establish:

Problem: What tester difficulty or engineering limitation exists?

Evidence: Where is it visible in the code or observed behaviour?

Options: What are the simplest viable alternatives?

Recommendation: Which option provides the best practical outcome?

Effort: What is the approximate engineering complexity?

Risk: What could break, and how can that risk be reduced?

Validation: What tests or experiments would demonstrate success?

Confidence: Which conclusions are verified, inferred, or uncertain?

Distinguish cosmetic improvements from changes that improve task completion, execution safety, or evidence integrity.

Avoid assigning numerical precision to speculative effort estimates.

10. Prioritisation

Use the following order of importance:

1. Correctness and preservation of test evidence.
2. Clear and predictable tester workflows.
3. Reliable execution, pause, stop, and recovery.
4. Parallel-worker feasibility and practical benefits.
5. Cost visibility and operational feedback.
6. Navigation and presentation polish.
7. Optional advanced capabilities.

This is a starting priority order. Adjust it if repository evidence reveals a more urgent issue.

Consider individual case selection, live output viewing, expanded multi-model workflows, and sophisticated historical comparisons as exploratory rather than mandatory.

11. Deliverables

Deliverable A — Current-state map

Explain how Janus actually works today.

Include the TUI navigation structure, execution architecture, data flow, persistence, and evidence outputs.

Identify existing strengths and limitations with code references.

Deliverable B — UX and architecture gap analysis

Compare the current implementation with the intended tester experience.

Classify findings as:

- Keep
- Improve
- Build
- Explore
- Defer

Challenge requirements that appear unnecessary or disproportionate.

Deliverable C — Parallel-worker feasibility assessment

Provide a dedicated analysis of concurrency.

Include:

- Existing process model.
- Shared-state and isolation risks.
- Simplest viable implementation.
- Recovery implications.
- Controlled experiments needed.
- Expected engineering effort.
- Whether two-worker execution is worth pursuing.

Be explicit about what remains unverified.

Deliverable D — Recommended evolution plan

Propose a small number of coherent implementation increments.

For each increment, explain:

- User-facing improvement.
- Required code changes.
- Dependencies.
- Risks.
- Tests and acceptance criteria.
- Whether it can be delivered independently.

Distinguish quick wins from architectural investments.

Deliverable E — Decisions requiring approval

Surface only consequential product or architectural decisions that cannot be resolved confidently through repository evidence.

Recommend a default for each.

Avoid asking questions that can be answered by inspecting the code.

12. Working Boundaries

Follow existing repository and agent instructions.

If the repository contains a "plan/" directory, keep planning artifacts there.

Preserve the existing shipping application structure unless a change is explicitly approved.

During this assignment:

- Inspect code and documentation.
- Trace existing workflows.
- Run safe, non-destructive verification where possible.
- Develop hypotheses and compare alternatives.
- Produce an evidence-based recommendation.

Do not modify shipping implementation code until authorised.

Do not introduce dependencies, change managed Claude Code configuration, invoke paid testing workloads, or restructure the repository without approval.

After approval, implement incrementally and validate each change before proceeding.

Final Instruction

Your job is not to implement this document.

Your job is to determine what Janus should become, what it should retain, and the simplest reliable path from its current state to a better tester experience.

Think critically and independently.

Challenge the proposed workflows.

Find opportunities the brief may have missed.

Give particular attention to the feasibility and value of two independent execution workers.

Prefer small, well-tested improvements. Recommend larger changes only when their benefits clearly justify their complexity and regression risk.

Begin by exploring the existing TUI. Produce the discovery, feasibility assessment, and recommended direction before requesting implementation approval.
