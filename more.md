Your premise is now out of date. **PreToolUse does carry `additionalContext`** in the current Claude Code hooks implementation.

Here's the confirmed picture, cross-checked against the official hooks reference on 26 July 2026:

The full `hookSpecificOutput` fields for `PreToolUse` are: `permissionDecision`, `permissionDecisionReason`, `updatedInput`, and `additionalContext`.

The explicit description from the same source: `additionalContext` injects text the model sees — alongside `permissionDecisionReason`, and optionally `updatedInput` to rewrite tool arguments.

So the three things you can do from a PreToolUse hook are: control the permission decision, rewrite the tool input before it runs, and inject context into the model's view — all in one hookSpecificOutput block.

The GitHub issues you may have seen from late 2025 (PreToolUse hooks could control permissions and modify tool inputs, but could not inject context into Claude's conversation) were feature requests at the time — they've since been implemented. Your observation that "every local example of additional context is a user's prompt submit/session start" was accurate then but is no longer the full picture.

Your other assessments stand:

- The `deny` path is real enforcement — the tool never runs. A hook that only logs can see the same command, but it cannot stop it.
- `permissionDecision` values are `allow`, `deny`, `ask`, and `defer` — `allow` runs the tool, `deny` blocks it, `ask` escalates to the user, and `defer` hands the decision back to the normal permission flow.

The upshot for your design: the coordination nodes don't need a different channel. PreToolUse can now handle both the gating decision and the context injection in one place, at exactly the right moment.


----
