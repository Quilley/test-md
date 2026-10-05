# Map and ticket records

Use this reference when creating or updating a Wayfinder map or decision ticket. Follow the project's configured tracker and record conventions.

## Tracker operations

Use the tracker's documented Wayfinding operations for parent-child relationships, claims, blocking edges, and frontier queries. Prefer native dependency relationships when supported. If no tracker is configured, use the included [local Markdown tracker](LOCAL-TRACKER.md) and its file conventions.

Use the tracker to determine eligibility and store records; choose priority using Wayfinder's decision-value rule. A tracker's default sort order is only a tie-breaker between equally useful questions.

On an issue tracker, label the map `wayfinder:map` and make its decision tickets child issues. Create tickets before wiring dependencies that require their identifiers. Claim a ticket through the tracker's assignment convention before working on it, and check for another session's claim. Re-read affected records before updating them when concurrent work is possible.

## Map body

Keep the map as an index; the detailed reasoning belongs in the relevant ticket. Query live child tickets through the tracker instead of duplicating their state in the map.

```markdown
## Destination

The intended outcome and the evidence or artifact that establishes it.

## Notes

Domain context, standing preferences, execution scope, and skills needed in later sessions.

## Decisions so far

One linked ticket name and a brief gist per current resolution. Include a material qualification in the gist when omitting it would change the meaning.

## Not yet specified

In-scope uncertainties that cannot yet be phrased as precise ticket questions.

## Out of scope

Excluded work, the reason, and links to any tickets closed on that basis.
```

## Decision tickets

Size a ticket around a coherent decision and the context needed to resolve it. Give it a clear title, a question, and genuine blocking dependencies. Name the decision it affects and the evidence needed when these are not obvious from the question. Label the type `wayfinder:research`, `wayfinder:grilling`, `wayfinder:prototype`, or `wayfinder:task`.

An unanswered but precise question belongs in a ticket even when blocked. Fog is for questions that cannot yet be specified. As evidence sharpens the fog, create the relevant tickets and remove the graduated entries so each question has one home.

## Resolutions and reopening

Record the resolution in the tracker's resolution comment or local equivalent. Include the answer, rationale, source or reproducible check, consequential uncertainty, and what would warrant reconsideration. Identify the decision's status and authority using [decision authority](../grilling/AUTHORITY.md). Link substantial research or exploratory artifacts rather than pasting them into the record. Distinguish a decision taken under uncertainty from an empirical claim established by evidence.

Close a ticket when its question has been answered against established criteria and the choice falls within the applicable authority. A factual research question can be resolved by checked evidence; a consequential choice needs the user's judgment or an existing delegation covering it. Keep the ticket open when necessary evidence or authority is still missing. A research ticket may conclude that available evidence is insufficient; its dependent decision remains blocked if it needs that evidence.

When new evidence invalidates a resolution, reopen or supersede the affected ticket and correct the map's gist and blocking edges. Preserve the previous rationale and explain what changed. Recheck dependent decisions before treating their prerequisites as satisfied.

When scope changes with the user's agreement, close excluded tickets with the reason and move their pointers to Out of scope. Bring previously excluded work back through an explicit scope revision and new or reopened tickets as appropriate to the tracker. Keep the history understandable without forcing a new map for every change.
