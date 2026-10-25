---
name: teach-bottom-up
description: Teach a topic bottom-up from its prerequisites, as a stepped HTML page, a plain HTML page, a Claude Doc, or chat. Use when Souvik asks to understand, learn, or get the idea behind something, or shares a source (paper, article, repo, chart, thread) to understand.
---

# Teach bottom-up

## When to use
- I ask to understand, learn, or explain something: "how does X work", "teach me X", "walk me through X", "help me get X".
- I share a source (paper, article, repo, chart, thread) and want to understand it.
- Prefer this over explain-2080 or first when the goal is to build up to a topic from its prerequisites. Use those only when I name them.

## Before writing (do this silently)
1. Decide: single concept, or a topic with several steps.
2. For several steps: walk backward from the topic, listing what each idea needs, until you reach something I already know. Start the chain there. I'm fluent in engineering, programming and economics, so don't reteach the basics of those unless the topic hinges on a non-obvious part. If unsure where I am, start one step lower.
3. Keep only prerequisites the topic actually needs. Order them so each depends only on earlier ones.
4. Pick one concrete example that can carry the whole page.
5. Pick the format (rules below). Never ask me.

A "page" means one artifact, one doc, or one chat reply.

## Content rules
- For a single concept, skip the prerequisite chain and just teach it.
- Each step opens with one line: what we already have, what's new, and why it matters. Name any earlier idea the step depends on.
- Introduce at most one new term per step, with a one-line gloss that uses the same example.
- One concrete example per page. If the topic needs a second, make a second page.
- End each page with one line on what it leaves out.
- On the final page, add one line on what I should now be able to predict or explain.
- When I share a source, teach the general concept behind it, not only what it says. Then say in one or two lines where the source fits that concept or departs from it.

## Format
- Process, sequence, or anything that builds or changes over time: stepped HTML artifact.
- Static but visual or interactive (a structure, a comparison, one slider or toggle): plain HTML artifact.
- Text-led explanation I'll want to reread or keep: a Claude Doc with headings, short paragraphs, a table if it helps, and a simple diagram only if it earns its place.
- Short answer that fits on a phone screen: plain chat text.

For any HTML artifact, load the artifact-design skill first and follow its page contract; the rules below narrow it.

## HTML rules
Keep it as simple and Claude-native as possible.
- Light mode only. No dark theme, and do not follow the system appearance.
- Editorial: one reading column, set like a well-edited article. The headline states the point, the body is plain prose, and there is no app chrome, dashboard framing, or filler.
- Native elements first: button, details/summary, table, input type=range, progress, figure, plain lists, inline SVG for diagrams.
- Stepped pages: Previous and Next buttons plus a "Step 3 of 7" label. Left and right arrow keys also move between steps. Previous is disabled on step 1, Next on the last step. Aim for 3 to 9 steps.
- Each step adds one piece and keeps earlier pieces visible. The last step shows the complete picture.
- Announce the new step's sentence in an aria-live region.
- Autoplay is optional, not default.
- Headline and body text in a serif. Buttons, labels and the step counter in the system font. Readable at phone width (about 380px) with no horizontal scroll.
- At most one accent color, used only to mark what's new in the current step. Earlier pieces return to the neutral color.
- No gradients, shadows, emoji, decorative icons, or animation beyond a simple fade-in of the new piece.
- No external libraries unless the topic truly needs one.
- Short labels in the visual. Put explanation in one or two plain sentences per step.

## Check before sending
- Every step opens with the have / new / why line.
- No step introduces more than one new term.
- The same example runs through the whole page.
- The accent marks only the current step's new piece.
- The page ends with what it leaves out; the final page also says what I can now predict or explain.
- For HTML: open it at phone width and confirm it reads cleanly in light mode, in an editorial layout.
