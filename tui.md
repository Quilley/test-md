# Janus — TUI-First Exploration & Improvement

You are entering an existing codebase for Janus, a terminal-based testing application for Restricted Claude Code.

I want you to independently explore the current system and help determine how to make it significantly easier, more reliable, and more effective for testers.

This is an exploratory product and engineering exercise, not a request to implement a predefined specification.

The ideas below represent the experience I have in mind. They may not match the current architecture, terminology, screens, or capabilities. That's completely fine.

Your job is to understand the existing system, evaluate these ideas, challenge them where appropriate, and identify the best practical direction forward.

## 1. Start from the TUI

Take a TUI-down approach.

Start with what testers see, how they navigate, what they need to accomplish, and where the current experience creates friction.

Then trace those interactions into the underlying code, execution scripts, state management, and outputs.

The user experience should guide the architecture, rather than forcing testers to navigate around implementation details.

However, do not assume the proposed TUI is necessarily better than what exists. If the current application already solves a problem effectively, preserve it.

The objective is not to create more screens or features. It is to make testing simpler and more dependable.

## 2. The Experience I'm Envisioning

Think of Janus as a straightforward testing console with a central home screen.

There are five broad areas I imagine being useful.

### A. Verify Environment

A quick way for testers to understand their current Claude Code environment.

For example:

- Are they running Restricted (R) or Unrestricted (U)?
- Is the managed Claude Code setup detected?
- What relevant configurations, hooks, or policies are present?
- Which models are available for testing?

This should be a lightweight diagnostic experience, not a complicated workflow.

### B. Golden Datasets

A simple way to access and execute established golden test collections.

Testers should be able to understand what they're about to run, choose the relevant model configuration, review the estimated cost, and begin testing without unnecessary steps.

### C. Test by Filters

An alternative way to select test cases using existing categories, intents, or other available metadata.

The experience should make it easy to narrow down cases, understand the selection, and launch testing.

Ideally, Golden Datasets and Test by Filters should reuse common execution capabilities rather than create separate systems.

### D. Active Phases

A compact area where testers can see ongoing executions while continuing to use Janus.

I imagine testers being able to:

- See which tests and models are running.
- Monitor meaningful progress.
- Understand errors or interruptions.
- Pause or stop an execution.
- Continue navigating the TUI.

The interface should remain responsive and should not overwhelm testers with unnecessary output.

### E. Activity & Results

A lightweight, persistent record of recent and historical testing activity.

Testers should be able to find completed executions, understand their technical status, and open generated CSV evidence in their default spreadsheet application.

Human review happens outside Janus. We do not need to turn the TUI into a review or LLM-judging platform.

These five areas are conceptual, not a required screen structure.

You may combine, rearrange, simplify, or replace them if the resulting user experience is better.

## 3. Execution and Recovery

I'd like you to explore whether testing can be organised into independently manageable execution phases.

Potentially, testers could:

- Start a testing phase.
- Monitor its progress.
- Pause safely and resume later.
- Stop permanently while preserving available evidence.
- Exit Janus without losing recoverable work.
- Resume interrupted phases after reopening the application.
- Select multiple models and execute them sequentially within a single phase.

A conditional Resume entry on Home might be useful when recoverable executions exist.

But these are intended behaviours, not prescribed technical mechanisms.

Inspect what the codebase already supports and determine which behaviours are genuinely valuable, feasible, and safe.

## 4. Pay Particular Attention to Parallel Workers

This is probably the most valuable area for deeper engineering investigation.

I am interested in the possibility of two independent testing executions running concurrently, while the TUI remains responsive.

For example, one worker might execute a golden collection against a sequence of models, while another executes a filtered collection independently.

However, I do not want parallelism introduced at the expense of reliability.

Investigate:

- How the current execution scripts work.
- Whether Claude Code processes can run independently.
- Whether configurations, sessions, hooks, files, or outputs are shared.
- How worker processes would be started, monitored, and terminated.
- Whether evidence or CSV writes could collide.
- How pause, stop, and resume would work.
- What happens if a worker crashes or Janus exits unexpectedly.
- What additional complexity and resource usage parallelism introduces.

Compare a simple sequential system with improved responsiveness against a two-worker approach.

If two workers offer substantial value at reasonable complexity, recommend how to introduce them safely.

If the current architecture makes parallel execution unnecessarily risky or expensive, explain why and propose a better alternative.

Do not assume that a worker manager, queueing framework, database, or new TUI framework is necessary.

Look for the simplest mechanism that works reliably.

## 5. Simplicity and Brownfield Pragmatism

Prefer simple solutions unless a more complex approach delivers a clearly meaningful improvement.

Some changes may require only small patches. Others may benefit from modest refactoring. A few might justify building a subsystem differently.

You have the freedom to recommend any of these.

Do not preserve poor architecture merely because it exists, but do not replace working architecture without a compelling reason.

Be particularly careful about changes that could break:

- Existing test case execution.
- JSON schemas and collections.
- Restricted Claude Code configuration.
- Cost calculations.
- Generated CSVs and evidence.
- Process cleanup.
- Existing tester workflows.

Reliability and evidence integrity matter more than interface sophistication.

## 6. Explore the Existing System Before Designing

Start by understanding the actual repository.

Trace the current TUI from its entry point through the important user journeys and underlying execution mechanisms.

Identify:

- What already works well.
- What partially supports the intended experience.
- What is missing.
- What is unnecessarily complicated.
- What can be improved with small changes.
- What might require architectural work.
- What assumptions in this prompt are incorrect.

Where safe, run the application and existing non-destructive tests.

Do not invoke paid model workloads or make destructive changes without authorisation.

Use code references and observed behaviour to support your conclusions.

## 7. Think Independently

I don't want you to simply agree with the ideas above.

If there is a better home-screen organisation, propose it.

If persistent active-phase cards are awkward with Rich and Questionary, suggest a simpler interaction.

If sequential multi-model execution is more complicated than separate phases, compare the trade-offs.

If an existing CSV structure is already sufficient, don't redesign it.

If a feature introduces more failure modes than user benefit, recommend deferring it.

Also identify opportunities I may have overlooked.

The aim is to arrive at a better system, not merely reproduce my initial ideas.

## 8. What I Want Back

Before implementing anything, provide a concise but substantive assessment covering:

1. **Current Janus experience**

   How the TUI and underlying execution system actually work today, including the main user flows.

2. **Opportunities for improvement**

   Where the existing experience can be made simpler, clearer, faster, or more reliable.

3. **Evaluation of the proposed direction**

   Which ideas are already supported, which make sense, which need modification, and which should be reconsidered.

4. **Parallel-worker feasibility**

   A focused technical assessment of independent concurrent execution, its benefits, risks, implementation alternatives, and what needs to be proven experimentally.

5. **Recommended approach**

   Your preferred direction, including alternatives you rejected and why.

6. **Incremental roadmap**

   A practical sequence of improvements, distinguishing:

   - Quick patches and UX improvements.
   - Moderate extensions or refactors.
   - Larger architectural investments.
   - Ideas worth deferring.

For each meaningful change, provide a rough effort estimate, regression risk, and a way to validate that it works.

Do not manufacture precise estimates where uncertainty is high.

## 9. Working Boundaries

Follow the repository's existing instructions and conventions.

Keep planning artifacts separate from shipping code, using "plan/" if that convention exists.

During this initial exercise, you may inspect code, trace workflows, and run safe verification, but do not modify shipping code or begin implementation without my approval.

Do not add dependencies or restructure the application merely for exploration.

Ask questions only when the answer cannot reasonably be determined from the repository and materially affects the recommendation.

## Guiding Principle

Build toward the simplest, most reliable testing experience that the existing Janus system can reasonably support.

Use my proposed TUI flows as inspiration and direction, not as constraints.

Start from tester needs, work inward through the implementation, and let evidence determine whether the best solution is a patch, a refactor, a new capability, or a different approach entirely.

Pay special attention to parallel workers, safe execution, recoverability, and preserving test evidence.

Explore first. Challenge assumptions. Recommend a direction. Wait for approval before building.
