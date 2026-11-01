# Design foundation

## Typography and space

Sunday Essay Fuller carries the editorial character approved in Greedy Shortcut and MMM V9. Those pages inform visual judgment, not mandatory branding or page structure. This package contains its own assets.

`assets/theme.css` owns exact values. Use its tokens and semantic classes. The default reading column is 660px, the standard figure 672px and the wide composition 1120px. Choose width from the material. Keep prose narrow even when a nearby figure needs more room.

| Role | Face | Default |
| --- | --- | --- |
| Prose and short diagram phrases | Newsreader / `IHD Serif` | `--ihd-weight-prose`: 480; prose 18px / 1.6 |
| Display, pull quote, primary result | Newsreader | `--ihd-weight-display`: 400 |
| Sections, controls, essential labels | Manrope / `IHD Sans` | `--ihd-weight-heading`: 550 |
| Secondary UI and captions | Manrope | `--ihd-weight-ui`: 450; captions 14px |
| Quantities and code | Geist Mono / `IHD Mono` | Tabular numerals, explicit units |
| Strong emphasis | Inherited face | `--ihd-weight-strong`: 650 |

Use real bundled upright/italic Newsreader and upright Manrope/Geist Mono. `font-synthesis: none` prevents fabricated faces. Latin subsets are bundled; supply an appropriate licensed face for other scripts. Confirm rendered glyphs rather than relying on a CSS family name.

Sustained prose is justified in full reading columns. Put a reading group in `.ihd-prose`; at an actual container width of 448px or less its paragraphs align left. Older markup gets a viewport fallback. This avoids stretched word spacing in narrow panels as well as phones. Headings, decks, captions, lists, notes and controls stay aligned for reading. Set the correct document language and retain native text resizing.

## Visual language

Use light paper, neutral ink, square edges and generous spacing. Let type and space establish hierarchy. Frames communicate an apparatus, comparison or grouping; an empty border is not a default decoration. Avoid nested frames around simple process nodes.

Charts use direct labels, shapes, hatching and line styles. Warnings need an explicit word such as “Assumption”. A shade difference alone must not identify a series or state. Color is an authorized exception, not the default.

The palette is one ink on light paper. Series use only black-derived tones: `--ihd-series-1` (ink), `--ihd-series-2` (#4d4d4d) and `--ihd-series-3` (#8a8a8a). Each clears 3:1 on paper and they sit about 2:1 apart; a fourth tone would not be distinguishable, so more than three series become small multiples. This rule overrides the palette of any chart skill for documents built here. Decorative rules use `--ihd-line`, which is too light to identify anything. Control borders use `--ihd-control-line` and bar tracks use `--ihd-track-line` (both #767676, 4.4:1 on paper). The documents are light only: `color-scheme: light` is a decision, not an omission, and a dark set would need its own tones checked against the same 3:1 rule.

Essential figure labels must render at least 14px after scaling. A 16px label on a 900-unit SVG displayed at 450px is only 8px. Recompose that figure. The `ihd-svg-label`, `ihd-svg-value` and `ihd-svg-data` roles distinguish sans labels, serif phrases and monospaced quantities; chart-specific labels use `ihd-chart-label` and `ihd-chart-value`.

## Component contracts

| Pattern | Use |
| --- | --- |
| `.ihd-page`, `.ihd-reading`, `.ihd-wide` | Page shell and width tiers; one `h1`, logical headings, skip link to `main#content` |
| `.ihd-prose` | Reading container; combine with `.ihd-reading` when it needs the reading width |
| `.ihd-visual` | Inner visual container, after the figure's width is established; local diagram adaptation |
| `.ihd-hero`, `.ihd-deck`, `.ihd-meta` | Title and optional context |
| `.ihd-section`, `.ihd-section-heading` | Reading rhythm and optional numbering |
| `.ihd-figure`, `.ihd-fit-content` | A figure and its intrinsic width; caption follows the content's alignment |
| `.ihd-instrument` | Deliberate frame around an apparatus or plot |
| `.ihd-diagram-wide`, `.ihd-diagram-small` | Equivalent compositions; unique IDs and only one exposed at a time |
| `.ihd-flow`, `.ihd-node`, `.ihd-arrow` | Wrapping HTML process nodes; connectors are decorative |
| `.ihd-split`, `.ihd-panel` | Comparisons that stack when their own space becomes insufficient |
| `.ihd-table-wrap`, `.ihd-figure-scroll` | Named, focusable local scroll region when preserving relationships needs it |
| `.ihd-number` | Explicit monospaced numerical cells; ordinary table cells use sans text |
| `.ihd-toc`, `.ihd-glossary`, `.ihd-footnotes` | Optional contents, definitions and source navigation. Inside `.ihd-doc` (contents first, then `main`) the contents become a sticky left rail from 80rem and an ordinary disclosure below it |
| `.ihd-s1`–`.ihd-s3`, `.ihd-line`, `.ihd-edge`, `.ihd-shape`, `.ihd-hatch`, `.ihd-ball`, `.ihd-pin` | The primitive kit; see [the visual grammar](visual-grammar.md) |
| `.ihd-stockflow`, `.ihd-capacity`, `.ihd-swim`, `.ihd-callout` | Recipes for what builds up, which step limits, who does what and the parts of one thing |
| `.ihd-note`, `.ihd-disclosure`, `.ihd-margin-note` | Qualifications and optional depth; conclusions remain outside disclosures |
| `.ihd-controls`, `.ihd-result` | Labeled native controls and a complete static baseline |
| `.ihd-print-only`, `.ihd-screen-only` | Equivalent print alternatives for spatially dense figures |
| `.ihd-footer` | Quiet centered footer, with contact only when appropriate |

Do not put size containment on a shrink-to-fit figure itself. `.ihd-visual` goes inside a figure whose width has already been chosen. The standard container switches diagram compositions at 608px; choose another threshold in authored CSS when the content needs it. Legacy viewport classes remain supported.

See [visual recipes](visual-recipes.md) for layout choices, [the visual grammar](visual-grammar.md) for figures no recipe covers and [reading quality](reading-quality.md) for acceptance criteria. Existing classes and reader hooks remain usable. Previously delivered offline HTML does not change until deliberately repackaged.
