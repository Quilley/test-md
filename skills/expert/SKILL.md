---
name: expert
description: Deepen a task within its existing scope by assessing expert judgment, source material, methods and tools, and verification. Use when the user invokes /expert or explicitly asks for an expert approach or extra rigor on a specific task. Not for quick lookups or casual questions.
---

# Expert

Improve the depth and quality of the requested task while preserving
its scope and constraints. Expertise may mean challenging a premise,
removing unnecessary work, or recognizing that the existing approach
is sufficient.

## Assess the four points

Before substantive work, inspect enough context to understand the
intended outcome and establish what material and tools are available.
Then assess all four points below, classifying each as:

- Active: materially useful and feasible during this task.
- Limited: materially useful, but access, information, capability,
  or authorization prevents full execution.
- Not needed: would not materially improve this task.

An unavailable source or tool is a limitation, not evidence of
irrelevance.

Each assessment must be specific to this task. If it could be pasted
into a different task unchanged, it is too generic: make it concrete
or drop it.

### 1. Expert judgment

Whose judgment matters most here, and what would that practitioner
notice that the request leaves unstated?

Look for the hidden premise, the failure mode common in this domain,
or the question behind the question. Name what you noticed and the
error or uncertainty it exposes. If nothing material stands out,
say so.

If the most valuable insight lies outside the requested scope, state
it and leave the decision to the user. Do not act on it.

### 2. Raw material

What original documents, data, or artifacts would ground this work?

Name the actual sources where known. Distinguish inspected material,
accessible but uninspected material, and unavailable material.
Identify a needed source by type when its exact identity is unknown.

Prefer direct, relevant evidence. Assess its provenance and fitness
for the question; raw material is not automatically reliable.

### 3. Methods and tools

What method acts on what you noticed, applied to which material,
and why?

Connect each method to the uncertainty it resolves or the quality
it improves. Name tools when they serve that method, checking their
availability before promising their use. A useful method may require
no external tool.

### 4. Verification

What observable check or independent evidence would support or
contradict the result?

Specify a runnable check, comparison source, or evaluation procedure,
and what outcome would count against the conclusion. Prefer checks
independent of how the result was produced; a check that cannot fail
is not a check. Match the strength of the claim to the strength of
the check.

For subjective work, identify the criteria and whose judgment matters.
Distinguish preference feedback from factual verification.

## What to show the user

Do the full assessment, but surface only what changes the user's
picture:

- Before work: any Limited point the user could remedy (a file to
  attach, a tool to connect, a decision only they can make), with
  the fallback you will use meanwhile. Flag it and continue unless
  it blocks meaningful progress.
- Active points: report in the closing summary, not as a preamble.
- Not needed: mention only when the user would reasonably expect
  the point to apply.

If nothing needs flagging up front, start the work without an
assessment header.

## Execute and close the loop

Apply the active points within existing authorization. For limited
points, use a justified fallback and keep the gap visible. Reassess
when new evidence changes what is useful or feasible.

Finish with:
- the requested result
- checks actually performed, and what they showed
- checks proposed but not performed
- material uncertainty, including what limited points left unresolved

## Example

Request: "/expert, is this cohort retention chart right?" with a CSV
attached and no access to the product database.

Up front:
> The CSV has last-activity dates but no cancellation events, so I'm
> treating 30 days of inactivity as churn. If you can export the
> cancellations table, the answer gets firmer.

Closing:
> - Judgment: the newest cohort is 9 days old, so its steep "drop"
>   is incomplete data, not churn.
> - Method: recomputed retention by days since signup, excluding
>   windows that haven't closed yet.
> - Checked: recomputed cohort sizes sum to the CSV's 4,212 signups.
> - Not checked: whether inactivity matches actual cancellation.
>   That needs the cancellations export.
