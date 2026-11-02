# Visual grammar

Templates cover ideas the skill has met before. Most ideas are new. This grammar lets a new figure be drawn from the same parts, under the same rules, so it looks like part of the system and still fits the idea.

## Start with the question and its structure

Before drawing, write one line: what the reader should be able to answer, and what structure the idea has. Then pick the layout that fits the structure. These are starting points; adapt the layout and keep the invariants.

| Structure | Starting layout | Built from |
| --- | --- | --- |
| Order of steps | Process nodes; swimlane when different actors hold different steps | `.ihd-flow`; `.ihd-swim` |
| Something builds up | Stock and flow; a line when the path over time matters | `.ihd-stockflow`; `.ihd-line` |
| How much, on one scale | Bars; capacity bars when one step limits the rest | `.ihd-bar-row`; `.ihd-capacity` |
| Options against criteria | Native table with rating balls | `.ihd-ball` in a table |
| Position on two axes | 2x2 or scatter: two axes, labelled quadrants, marker shapes | `matrix` or `scatter` chart ([charts from data](visual-recipes.md#charts-from-data)) |
| What depends on what | Shapes and edges, at most seven nodes per figure | `.ihd-shape`, `.ihd-edge` |
| Feedback | Edges that return to their source; polarity written on each edge | solid and open arrowheads |
| Parts of one thing | A figure with numbered pins and a key | `.ihd-callout` |
| Dated events | Timeline with a real scale | see visual recipes |

Anything made of numbers (bars, lines, ranges, sensitivity, waterfalls, scatter, 2x2) comes from the chart builder, which computes the geometry. There is no template for a network or a loop. Compose those from the kit and check them against the invariants below.

## Invariants

A figure may change shape, layout and emphasis. It may not break these. The audit checks the ones it can.

1. **Ink only.** Black-derived tones. Three series tones: `--ihd-series-1` (ink), `--ihd-series-2` (#4d4d4d), `--ihd-series-3` (#8a8a8a); each clears 3:1 on paper and they sit about 2:1 apart. A fourth tone would sit about 1.3:1 from its neighbour, so use small multiples instead. These tones override any chart skill's own palette.
2. **Tone never identifies alone.** Every series carries a direct label, a marker shape and a dash. Meaning that depends on shade is rewritten.
3. **Labels at least 14px after scaling.** Design the SVG at the width it is shown, or rebuild it narrow.
4. **A text equivalent.** A caption that states the takeaway, plus an accessible description or table with the same values.
5. **A narrow alternative.** Reflow HTML, swap to a table, or stack small multiples. Local scrolling is for preserved scale only.
6. **Unique IDs and one sprite.** Copy the sprite from `assets/starter.html` once. Never `display: none` it.
7. **One emphasis.** The point of the figure takes the darkest tone or the thickest line. Everything else sits one step lighter.

If a bespoke figure fails an invariant, simplify the figure. If an exception is truly needed, say which invariant and why in the delivery note.

## The kit

| Part | Use |
| --- | --- |
| `.ihd-s1` `.ihd-s2` `.ihd-s3` | Series tone, for stroke and fill |
| `.ihd-line` with `.ihd-dash` or `.ihd-dot` | Solid, dashed and dotted series lines |
| `<use href="#ihd-m-circle">` and `-square`, `-triangle`, `-diamond` | Markers, drawn at 12 by 12 beside the data point |
| `.ihd-axis` | Axis and baseline |
| `.ihd-edge`, `.ihd-edge--opposite`, `.ihd-edge--block` | Arrows: closed head for a cause that raises, open head and dashes for one that lowers, bar for one that stops |
| `.ihd-shape`, `.ihd-shape--tint`, `.ihd-hatch` | Plain, quiet and hatched regions; hatch marks a limit or a level |
| `.ihd-quiet`, `.ihd-emph` | One step lighter, one step heavier |
| `.ihd-chart-label`, `.ihd-chart-value` | Sans labels and monospaced numbers at 16px |
| `.ihd-pin` | Numbered square pin placed by `--x` and `--y` percentages |
| `.ihd-ball` with `#ihd-h-0` to `#ihd-h-4` | Rating balls from empty to full, always beside the word |

## When the idea is complex

Climb only as far as the idea needs.

1. One figure.
2. One figure with callouts, so the words sit beside the parts.
3. Overview and detail: one small whole, then separate figures for the parts, each on the same scale.
4. A sequence: the figure changes one thing at a time inside guided steps, with the frame held still so the reader sees what changed.
5. A model: controls drive the figure, with a static baseline that carries the same conclusion.

If a figure needs more than about seven labelled objects, or more than two kinds of relationship, split it rather than shrink it. Shrinking breaks the 14px rule first.

## Checks

The audit catches overflow, small labels, clipping, low text contrast, duplicate IDs, colours outside the ink ramp and figures with no caption. It cannot tell whether the picture answers the question. Look at every screenshot and ask whether the reader could answer faster from the picture than from the paragraph.
