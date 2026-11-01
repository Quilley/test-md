---
name: internal-html-design
description: Present explanations, documentation, interactive builds and landing pages as readable offline HTML, picture first, with Souvik's Sunday Essay Fuller design, when explicitly requested.
disable-model-invocation: true
---

# Internal HTML Design

Apply this system only when explicitly requested. The producing skill owns content, evidence, domain logic and workflow; this skill owns presentation. Preserve supplied wording and certainty. Use the available voice skill when asked to write as Souvik.

Work from this installed directory. All references, assets and scripts are local to this package; normal use needs neither another agent's installation nor another agent's CLI.

## Compose

Read [the design foundation](references/design-system.md). Start with [the semantic shell](assets/starter.html) and reuse `assets/theme.css`. Sunday Essay Fuller uses Newsreader prose at **480**, Manrope headings, Geist Mono quantities, light paper and one ink. Exact values belong to shared CSS tokens.

State the reader's question and choose the smallest composition that answers it. Where the material holds a relationship, draw it first and let the prose explain the picture; prose-only is for material with no relationship. Series colour is black-derived only.

- **Document:** use the [visual essay](examples/source/visual-essay.html) or [evidence report](examples/source/evidence-report.html). For contents (a sticky rail on wide screens), glossary and source navigation, read [reading quality](references/reading-quality.md) and the [long document](examples/source/long-document.html).
- **Visual explanation:** read [visual recipes](references/visual-recipes.md) for processes, swimlanes, stock and flow, branches, bars, lines, timelines, callouts, comparisons and tables. The [visual toolkit](examples/source/visual-toolkit.html) and the [system explainer](examples/source/system-explainer.html) contain complete authored patterns. A figure must communicate a useful relationship; omit decorative plots.
- **A figure no recipe covers:** read [the visual grammar](references/visual-grammar.md). Compose it from the primitive kit and keep its invariants.
- **Build or landing:** read [composition recipes](references/compositions.md) for controls, guided steps, continuous motion and native-scroll compositions. Start with the [guided build](examples/source/guided-explainer.html) or [landing](examples/source/landing.html).
- **Small components:** consult the [catalogue](examples/source/component-catalogue.html) only for needed notes, disclosures, figures, legends and controls.

Read authored sources rather than rendered HTML containing embedded fonts. Open the rendered examples to judge appearance. Examples illustrate choices; their subject, branding and section count are not requirements.

Use `.ihd-prose` for reading groups and `.ihd-visual` around responsive visual content. Design at the actual available width. Essential figure labels must render at least 14px after SVG scaling. Reflow text-heavy diagrams before considering local scrolling. Preserve all claims, units and relationships in narrow alternatives. Keep the document inside the viewport without hiding overflow.

## Package and review

Run `python3 scripts/inline.py /absolute/source.html /absolute/result.html` to assemble one offline file with the bundled fonts, licenses, CSS and reader. The output must be a new path. Keep authored data and model code in the source. Read [maintenance](references/maintenance.md) for custom fonts, packaging boundaries and host installation details.

Read [the quality workflow](references/reading-quality.md#review-and-delivery) before delivery. Use `node scripts/audit_layout.cjs /absolute/result.html` when a local browser runtime is available, then inspect its screenshots. Measurements identify risks; visual judgment decides whether the argument, figure and reading rhythm are clear. A missing browser runtime is an incomplete check, never a pass.

Keep every substantive explanation and conclusion available without interaction or JavaScript. Check fonts, narrow containers, keyboard access, motion preferences, offline loading and print. Report the absolute output path and any verification gaps. Open the result in the current host's browser when available; otherwise provide its file path and saved previews. Deliver HTML unless another format was requested.
