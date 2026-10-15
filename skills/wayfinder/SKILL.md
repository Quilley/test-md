---
name: wayfinder
description: Develop a large plan across sessions through a shared map of decisions, evidence, dependencies, and unresolved questions.
disable-model-invocation: true
---

# Wayfinder

Use a shared map when an effort contains interdependent decisions that exceed one session. The map preserves the reasoning needed to choose the next step and revise the route as evidence changes.

Read [grilling](../grilling/SKILL.md) at the start of each planning session and apply its judgment, authority, evidence, and handoff rules. Wayfinder carries that discipline across sessions. Read [domain-modeling](../domain-modeling/SKILL.md) when changing domain concepts or recording architecture decisions.

## The map

The **destination** states the intended outcome and how to recognize it. Treat it as a revisable commitment: propose a change when the evidence or underlying need warrants it, and confirm the change with the user before redirecting the effort.

Each **decision ticket** owns a question and its resolution. The map is an index of these records. The **frontier** contains open, unblocked, unclaimed tickets; **fog** contains in-scope questions that cannot yet be specified. Scope exclusions have their own place and can be reconsidered when the user changes the destination or boundary.

When creating or updating the map or tickets, read [MAP.md](MAP.md) for record structure, tracker operations, and resolution semantics. Preserve an existing map's conventions when resuming it. Refer to maps and tickets by linked names so the human can follow the reasoning.

Planning is the default scope. Research and bounded exploratory artifacts can inform a decision; production implementation or publication requires the applicable authorization. A map's Notes may explicitly include execution. Keep exploratory evidence separate from claims that the final deliverable works.

## Chart a route

1. **Survey.** Read the relevant existing plans, decisions, code, and evidence. Use [research](../research/SKILL.md) where consequential uncertainty or prior art could change the route. Surveying is sufficient when you can explain the current commitments, significant conflicts, and gaps that shape the plan.
2. **Frame the destination.** Distinguish the desired outcome from the proposed approach. Challenge whether it serves the underlying need and offer a better framing when warranted. Proceed once the intended outcome and consequential scope choices are clear; keep unsettled premises visible.
3. **Expose the dependencies.** Find the load-bearing assumptions and decisions across the effort before following one branch deeply. Identify integration uncertainties that may need a vertical slice as well as questions answerable through reasoning, research, or user judgment. This step is complete when the next consequential decisions and their prerequisites are explicit. If the effort fits one session, continue with a proportionate plan instead of constructing a map.
4. **Record the route.** Create the map and tickets that can be specified now, then wire their blocking edges. Put the remaining fog and scope exclusions in the map. Run the grilling plan check; record any change it makes. The route is ready when each live question has a record and dependencies express genuine prerequisites.
5. **Recommend the next move.** Choose from the frontier by how much the answer could change the plan, weighing uncertainty, consequences, and downstream dependencies. Explain the choice briefly. Continue within the user's requested scope, or leave a continuation point when the request was only to chart the map.

## Work a decision

1. **Resume and claim.** Read the map, its Notes, and relevant changes since the last session. If the user names a ticket, use it and flag material prerequisites. Otherwise choose the frontier question with the greatest decision value. Claim it using the configured tracker and check for concurrent ownership. This step ends when the selected question is available and its relevance is clear.
2. **Ground the dependencies.** Read the ticket, the decisions it depends on, and their evidence. Inspect affected code or data where needed. Distinguish prior choices from verified facts. Grounding is sufficient when you can explain what this decision could invalidate or unblock.
3. **Resolve or bound it.** Apply the appropriate mode below and the grilling decision loop. A resolution explains the choice or finding, its evidence, consequential uncertainty, and what would reopen it. If a necessary experiment or external answer is outstanding, record it as a prerequisite and keep the dependent ticket open. Continue unrelated planning where useful.
4. **Record and follow the cascade.** Record a supported resolution and close the ticket when its question is answered at the required level of confidence. Update the map's index with the ticket's one-line gist, nothing more. Trace consequences through dependent tickets, prior decisions, and fog; propose and record authorized revisions, reopenings, or scope changes by rewriting each affected ticket's current state. Preserve superseded rationale in the rounds log. This step is complete when affected records and dependency edges reflect the new state.
5. **Check the whole plan.** Run the grilling plan check before choosing the next decision or handing off. Continue while the requested scope and available context support useful work. Leave a clear continuation point when judgment, evidence, or a session boundary requires a pause.

## Choose the mode

- **Research:** evidence the agent can obtain. Read [research](../research/SKILL.md). The result must explain what the finding changes in the decision; independent investigations may run concurrently when permitted.
- **Grilling:** a consequential judgment, disputed framing, or competing preferences needing collaboration. Ask the human for their own choice after doing the available legwork.
- **Prototype:** an artifact that can distinguish relevant possibilities. Apply grilling's evidence criteria before selecting the artifact. For a UI or state-model exploration, read [prototype](../prototype/SKILL.md), keeping its creation and capture within the agreed planning scope. Other uncertainties may call for a measurement, sketch, or small vertical slice. Seek human participation when the question depends on their judgment; empirical checks can run independently within authorization.
- **Task:** prerequisite work that enables a decision, such as obtaining access or preparing data. Perform authorized work the agent can do; give the user a precise request for anything requiring their action. Record the resulting facts and preserve sensitive values in their intended storage.

## Handoff

Judge readiness against the next consequential step, using grilling's handoff criteria. Open questions may remain if they do not undermine that step. Show which prerequisites still block action and which uncertainties can be carried forward with an explicit revisit condition. Close the overall map only when its agreed destination is satisfied; readiness to begin a bounded next step can be recorded while the larger map remains open.
