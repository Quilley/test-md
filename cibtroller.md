# Teaching a Controller When Not to Be One

The default move when a routing skill encounters another skill is to orchestrate it. Decompose the goal, fan out workers, verify the output. That is what controllers do.

That answer is wrong about half the time.

The trouble is that skills are not functions. Some of them carry stateful pipelines: they write resumable-state files, enforce hard-refuse gates that encode correctness invariants, and run mid-flow validation logic the controller cannot replicate. If the controller decomposes around such a skill instead of through it, the user loses the skill's internal validators, its resume continuity, and the refusal logic that prevents the pipeline from proceeding on bad preconditions. The user asked for the skill. They did not ask for a controller to imitate it worse and charge more for the privilege.

The controller does not know which case it is in until it looks. So look. Read the target skill's instruction set before doing anything else. Not a grep. Not a hook nudge. Read it. Then classify it into one of four categories.

The first two categories the controller should own. An artifact skill has no resumable state, no refusal gates, and produces one deliverable. A review or analysis skill fans out read-only and uses a rubric as its gate. For both, the controller treats the skill's goal as the work unit. It decomposes with its normal routing logic: cheap workers for parallelizable pieces, more expensive reviewers for judgment calls. Then it verifies against the skill's stated criterion. The skill's instruction set becomes context, not code to invoke. In practice, this is the best case for a controller. It brings cost routing and deterministic verification to a task the target skill would have run as a single monolithic pass.

The third category the controller should hand off. A stateful pipeline writes resumable-state files, enforces hard-refuse phases, and runs mid-flow validators the controller cannot replicate. The protocol has three steps, and their order matters.

First, enrich. Run one cheap worker pass to build a brief: a map of the directories the skill will touch, pointers to existing artifacts it will need, edge cases worth flagging. Show this to the user before stepping back. If the skill is self-contained and repo context adds nothing, skip enrichment and say so.

Second, log. Record a minimal entry: goal, route type (`skill_handoff`), target, whether enrichment ran. Close the run. This is not bookkeeping. If the user re-runs the controller on the same goal after a hand-off, the log surfaces a correlation. That correlation means the classification was wrong. It appears in the data instead of hiding.

Third, invoke. Emit one line: "Handing to `/[target]`. This controller cannot verify after this point. The skill owns its own gates." Then call the skill. Control does not return. The invocation is one-way, so everything the controller wants on record must happen before it.

The fourth category, an advisory or lens skill, the controller should absorb. These skills have no phases and produce no output. They are behavioral guidance: style constraints, rubrics, correction lenses. Never invoke them. Read them and fold their content into worker and reviewer prompts. The author wrote that guidance to be applied from inside a flow, not called from outside it.

The tiebreaker for edge cases comes down to internal machinery. If a skill looks like an artifact but carries a rendering pipeline, domain-specific validators, or templates the controller cannot replicate, classify it as a stateful pipeline. Owning it produces a worse result than the skill itself. When in doubt, hand off.

A second problem surfaced while building this, and it applies well beyond controller routing. A process-exit-code gate measures whether a run completed cleanly. It does not measure whether behavior changed correctly. A thin test suite returns exit code zero just as reliably as a thorough one. Those two facts together create a specific trap in verifier logic.

The intuitive skip condition for a downstream reviewer is to bypass it when the task passed on the first try. That is exactly wrong. A task that cleared a thin test suite on the first attempt is precisely the case where a reviewer is most needed. The exit code said the process completed. It said nothing about the behavior.

The correct condition is grade-based. Skip the reviewer only when every achieved grade is at surface-inspection level: lint, typecheck. Any task that reached behavior-test grades always gets the reviewer, regardless of attempt count. And the reviewer must receive the actual diff, not a prose synthesis. A reviewer reading prose measures coherence. Only the diff reveals correctness. A clean summary can accurately describe a change and still hide the line that broke an invariant.

Both findings follow from the same forcing reason. Gates measure what they can see. A controller that assumes a gate sees more than it does will make decisions that look safe and are not.

Read before routing. Log every hand-off. Bound reviewer skips to what the gate can actually certify.

A controller that knows when not to be a controller is a better controller.