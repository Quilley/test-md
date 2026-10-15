---
name: implement-spec
description: "Implement the result of /to-spec and /to-tickets in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph. Raise any ticket blocked by an open question with the user now, so the answer is ready when the frontier reaches it.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 5 (a branch with no commits ahead of main can't open one), marked as closing the spec and tickets.

4. Use **implementer subagents** to implement each ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the ticket, treating the seams named in the spec's Testing Decisions as confirmed;
   - stops and reports the ID, rather than choosing, when the ticket depends on an item still open in the spec's Carried Forward or cannot meet a user story or decision as written;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**. The merger runs the test suite after merging and sends a failing ticket back to its implementer rather than leaving the integration branch red. A merged ticket counts as done for the frontier; unless the tracker closes work through the PR, resolve it now.

   If an implementer stopped on a question, take it to the user. Record the answer in the spec, as a new decision or a settled Carried Forward item, before rerunning that ticket. The rest of the frontier carries on meanwhile.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `code-review` on the integration branch, passing the spec's path or issue reference. In a single **implementer subagent**, fix the Spec findings and breaches of documented standards; baseline smells are judgement calls to fix only where they clearly help.

8. List the spec's decisions that meet the bar in [When to offer an ADR](../domain-modeling/ADR-FORMAT.md) and offer to record them, so the reasons outlive the spec.

9. If a draft PR exists, mark it ready for review. Otherwise, report the integration branch. Either way, list the Carried Forward items still awaiting the user's confirmation.

10. Clean up all **implementer subagent** worktrees.
