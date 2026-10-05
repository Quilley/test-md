# Local Markdown tracker

Use this tracker when the project has no configured issue tracker. The project can choose another layout; record that convention in the map's Notes and follow it consistently.

## Files

- Map: `.scratch/<effort>/map.md`.
- Ticket: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01` within the effort.
- Each ticket begins with `Type: research|prototype|grilling|task` and `Status: open|claimed|resolved`.
- Add `Blocked by: NN, NN` when another ticket must resolve first. An open ticket is on the frontier when all its blockers are resolved.
- Keep comments and conversation history under `## Comments` when useful.

## Work

Claim a ticket by setting `Status: claimed` before starting; check for another active claim. Record the answer under `## Answer`, set `Status: resolved` only when the question is answered at the needed level and within the applicable decision authority, then add its context pointer to the map's Decisions so far. Keep consequential choices open when user judgment or established delegation is missing.
