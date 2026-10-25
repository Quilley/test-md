---
name: internal-html-design
description: Apply Souvik's shared visual design to internal HTML documents and explainers when explicitly requested.
disable-model-invocation: true
---

# Internal HTML Design

Apply this design system only when the user explicitly requests it, including when another skill is producing the document. The producing skill still owns the subject, evidence, domain language and workflow. This system supplies presentation. Existing skills keep their usual themes otherwise.

Read [the design guide](references/design-system.md), then compose from [the starter](assets/starter.html). Inspect only the relevant authored example: [visual essay](examples/source/visual-essay.html), [evidence report](examples/source/evidence-report.html), or [guided explainer](examples/source/guided-explainer.html). The stylesheet in `assets/theme.css` is the authority for exact visual values. Rendered specimens are not shipped; build one from a source file with `scripts/inline.py` when you need to see it.

Choose a composition for the material. Use a flowing reading column for an argument, wider figures for mechanisms, and comparisons or tables for evidence. Let visuals carry the difficult inference. Preserve enough prose to make the piece understandable without interacting.

When drafting new prose as Souvik, read the existing global `souvik` skill at `~/.claude/skills/souvik/SKILL.md`. Follow its voice and evidence guidance. Formatting supplied writing preserves its words and certainty unless the user also asks for an edit. If the task requests another voice, honor it.

Deliver one offline HTML file, with the required styles, scripts, font faces and visual assets inlined. Inline SVG is the default for schematics. Keep existing interactive behavior and accessibility when restyling an artifact. The guide explains the small file-inlining helper; it is not a content renderer.

Use Source Serif 4 for headings and reading prose. Use Libre Franklin for labels, captions, controls and diagram annotations. Both are bundled as variable fonts under the SIL Open Font License, so use their weights as supplied rather than synthesizing styles.

Finished internal documents may embed the bundled fonts; keep their OFL notices with any copy of the font files. See the guide's font section before changing the font pairing.

Before delivery, open the result and check desktop and narrow mobile layouts, actual font loading, light and dark appearance, keyboard operation, reduced motion, and offline behavior. Check with JavaScript disabled: every substantive explanation, figure and conclusion must remain available. Preserve the distinction between illustrative models and measured results.

Open the finished HTML in the current chat's browser panel when available. Report its absolute path and any verification gaps. Deliver HTML only unless the user requests another format.
