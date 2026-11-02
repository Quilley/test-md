# Visual recipes

## Choose the relationship

Start with the reader's question. Choose a process for order, a swimlane for who does which step, stock and flow for what builds up, branches for alternatives, bars for magnitude, a line for change along a meaningful axis, a timeline for dated events, numbered callouts for the parts of one thing, or a table for exact comparison. Whenever the material holds a relationship, draw it first and let the prose explain what the picture shows. Ask of each section: could the reader answer faster from a picture than from the paragraph? If yes, there is a figure. If the material holds no relationship, write prose and do not invent one. Decorative plots stay out. For an idea no recipe covers, read [the visual grammar](visual-grammar.md). Match all values and conclusions to the producing material.

Prefer wrapping HTML for text-heavy nodes and comparisons. Use inline SVG when geometry conveys meaning. Canvas is an optional choice for genuinely dense or dynamic geometry; provide an equivalent static explanation and accessible values. No chart library or remote rendering dependency is required by this skill.

Draw anything made of numbers with the chart builder below; do not type coordinates. The [toolkit source](../examples/source/visual-toolkit.html) demonstrates branches, bars, a line chart with a narrow table alternative, and a dated timeline. The [catalogue](../examples/source/component-catalogue.html) demonstrates a process and controls.

## Processes and branches

A simple path needs nodes, direction and clear type. Leave connectors in the gaps. Use a box only when its boundary groups something meaningful. Keep long labels as wrapping HTML, rather than shrinking SVG text. A branch must name each alternative and keep its consequence beside it.

Wrap the layout in `.ihd-visual`. `.ihd-flow` becomes vertical inside a narrow visual container, including a desktop panel. Arrow direction must follow the reflowed reading order. Use `aria-hidden="true"` on decorative connectors. Avoid duplicate spoken explanations from an image description and fully readable HTML nodes.

For SVG, measure labels with `getComputedTextLength()` or `getBBox()` after fonts load. Include side padding and keep arrowheads clear of text. Use deliberate `tspan` lines if exact authored wording must remain. Summarize labels only when authorized; preserve the complete meaning and units nearby. Never use clipping or `textLength` to conceal a label that does not fit.

## Bars and comparisons

Bars compare magnitude on a common scale; show units and direct values. Keep a common baseline and scale across small multiples. Distinguish measured inputs from assumptions with labels and a pattern, not only tone. Longer category labels wrap in HTML beside the bar. Preserve the order, values and interpretation when stacking a comparison.

`ihd-bar-row`, `ihd-track` and `ihd-bar` are simple HTML patterns, not calculation logic. An authored bar width must agree with its value and scale. Keep a result visible when controls are absent.

## Lines and time

A line connects ordered observations or explicitly constructed states. Name both axes, units and the series. Do not connect unrelated categories or imply measured continuity from invented data. Directly label the series and expose exact values in a table or prose when those values matter.

Series use the three black-derived tones, one dash and one marker each: a solid line with circles, a dashed line with squares, a dotted line with triangles, with a direct label at each line end. Tone is the last cue, never the only one. For more than three series, use small multiples on one shared scale.

A wide SVG should use the space it actually needs. Its essential labels must remain at least 14px after scaling. On a narrow view, an equivalent table or small multiples can be clearer than a shrunken plot. Preserve the same data and conclusion in both representations; use unique element IDs.

A timeline earns its axis through dates or meaningful intervals. An empty month ruler carries no evidence. If interval distances matter, preserve the scale and scroll only the timeline region:

```html
<figure class="ihd-figure ihd-fit-content">
  <p class="ihd-figure-title">Dated milestones</p>
  <div class="ihd-figure-scroll" role="region" aria-label="Milestones; scroll for later dates" tabindex="0">
    <!-- Accessible SVG at its useful intrinsic width. -->
  </div>
  <figcaption>State the event sequence or interval that matters. Add a brief scrolling cue when needed.</figcaption>
</figure>
```

Keep captions compact: state the takeaway and essential qualification, and put longer method explanations in adjacent prose. Keep implementation language out of captions. Explain what to notice and what the marks support. A short interaction hint can say “Scroll for later dates”; it need not describe a focusable frame or page overflow policy.

## Charts from data

Write the data and a chart type; `inline.py` draws the figure. The builder computes the scale, ticks, marker positions and label positions, writes a text table that replaces the chart in a narrow container and in print, and refuses anything that breaks the visual-grammar invariants. Copy the sprite from `assets/starter.html` first.

```html
<div data-ihd-chart><script type="application/json">
{"type": "range", "title": "Monthly cost by part", "caption": "Memory nodes carry the widest spread.",
 "prefix": "$", "suffix": "k", "unit": "$ thousand a month", "emph": "Memory nodes",
 "items": [{"label": "Memory nodes", "low": 14, "base": 21, "high": 38}]}
</script></div>
```

Every chart needs `type`, `title` and `caption` (what to notice). Optional on all: `prefix`, `suffix`, `unit` (axis note), `emph` (the one label or series that takes the darkest tone and heaviest stroke), `description` (the accessible description; written from the data when omitted), `item_label` or `category_label` (first column of the table). Run `python3 scripts/chart.py spec.json` to print a single figure for pasting and hand editing.

| Type | Use it for | Data |
| --- | --- | --- |
| `bar` | How much, on one scale | `items: [{label, value, assumed?}]`, optional `max` |
| `grouped` | One quantity per category, up to three series | `categories`, `series: [{name, values}]`, optional `max` |
| `stacked` | Parts of a whole per category, up to three parts | `categories`, `series: [{name, values}]` |
| `line` | Change along an ordered axis, up to three series | `x`, `series`, optional `x_label`, `y_label`, `zero` |
| `range` | A low, base and high per item | `items: [{label, low, base, high}]` |
| `tornado` | Which assumption moves the answer most | `base`, `items: [{label, low, high, low_case?, high_case?}]`, sorted by swing |
| `waterfall` | A total built from steps | `steps: [{label, value, kind?}]`; the first step and any `"kind": "total"` are totals and must match the running sum |
| `slope` | Before and after, up to nine items | `items: [{label, before, after}]`, `before_label`, `after_label` |
| `scatter` | Position on two measures, up to twelve points | `points: [{label, x, y}]`, `x_label`, `y_label`, `x_format`, `y_format` |
| `matrix` | A scatter with named quadrants | as `scatter` plus `quadrants: {tl, tr, bl, br}`, `mid_x`, `mid_y` |

More than three series is an error: split into several charts on one shared `max`. A label that would collide is an error: shorten it, spread the points or drop one. Bars start at zero; use `range` or `waterfall` for values that can be negative. Write the case that produced each end of a tornado bar in `low_case` and `high_case`, so the reader sees the input and not only the result. A chart that fits none of these is a hand-drawn figure: read [the visual grammar](visual-grammar.md). The [data charts example](../examples/source/data-charts.html) shows every type in a sizing story.

## Tables and exact values

Use native `table`, `caption`, scoped headers and text cells. Mark quantitative cells with `.ihd-number`; ordinary prose cells use Manrope. State units once in the appropriate header or caption. Align comparable numbers consistently and retain qualifiers.

Reflow a small comparison into an equivalent labeled layout when row relationships remain clear. Preserve an intrinsically wide data table in a named, focusable `.ihd-table-wrap` when columns must be compared together. Do not convert every cell to a block and discard header relationships. Link long source names descriptively rather than displaying full unwieldy URLs.

## Stock and flow

Use it when something collects because one rate exceeds another: backlog, balance, queue, inventory. Pipe thickness is a rate on one shared scale (`--rate` against `--max`); the hatched level is the accumulated stock against a stated capacity (`--level` as a percentage).

```html
<div class="ihd-stockflow" style="--max:12">
  <div class="ihd-sf-pipe"><span class="ihd-sf-rate">Arrivals 6 a minute</span><span class="ihd-sf-bar" style="--rate:6" aria-hidden="true"></span></div>
  <div class="ihd-sf-stock" style="--level:50"><span class="ihd-sf-fill" aria-hidden="true"></span><span class="ihd-sf-label">Unfinished orders: 20 after ten minutes</span></div>
  <div class="ihd-sf-pipe"><span class="ihd-sf-rate">Completed 4 a minute</span><span class="ihd-sf-bar" style="--rate:4" aria-hidden="true"></span></div>
</div>
```

State the tank's capacity in the caption so the level can be checked. The picture reflows to a vertical stack in a narrow container. Put it inside `.ihd-visual`.

## Capacity bars and ratings

`.ihd-capacity` draws several quantities on one scale (`--v` against `--max`) with the limiting step hatched. Use it when one step caps the others. Plain `ihd-bar-row` bars remain right for labelled comparisons with direct values.

For options against criteria, use a native table with `<svg class="ihd-ball" aria-hidden="true"><use href="#ihd-h-2"/></svg>` and the word beside it ("Half"). Wrap a table with three or more columns in `.ihd-table-wrap` with a name and `tabindex="0"`, and give the table a `min-width` so it scrolls inside the region instead of the page. A `fit-content` figure does not stop a wide table overflowing a phone.

## Swimlane

Use it to document who does which step. Columns are actors, rows are time. Each step names its column with `--lane` and its row with `--row`, and carries `data-lane` for the narrow view. The visible numbers are generated, so step order stays in the document order.

```html
<div class="ihd-swim" style="--lanes:3">
  <p class="ihd-lane-name" style="--lane:1">Customer</p> <!-- one per lane -->
  <ol class="ihd-swim-steps" role="list">
    <li style="--lane:1;--row:1" data-lane="Customer">Places the order.<span class="ihd-handoff">Passes to Preparation</span></li>
  </ol>
</div>
```

Write each hand-off in words; do not rely on drawn arrows. The swimlane is HTML, so it keeps its type size. A swimlane with several lanes can sit in `.ihd-wide`. In a narrow container the lanes disappear and each step becomes a numbered line naming its actor.

## Numbered callouts

Use them to explain the parts of one figure. Put the figure and a key in `.ihd-callout`; place each `.ihd-pin` on its part with `--x` and `--y` percentages, and link it to the matching key item. The pin is a 28px square with a 44px hit area, and the key carries all the words. Pins are percentages of the stage, so they stay on their part as the figure scales. In a container of 40rem or more the key sits beside the figure; below that it sits under it. Keep the SVG's text at least 14px at the narrowest stage width.

## Controls and visual states

Labels include units and current values. Keep the assumption and consequence in the same reading group. Use native inputs with 44px minimum hit areas, visible focus and no hover-only essential values. A reset or stated baseline makes changes reversible.

The producer owns calculations. Bind listeners before revealing functional controls. Match initial marks to initial input values, and retain the substantive explanation without JavaScript. Announce concise user-triggered results politely; animation frames must not flood a live region. Read [composition recipes](compositions.md) for motion lifecycle and guided steps.

## Adaptation order

1. Give the figure only the width its content needs.
2. Wrap, stack or simplify while preserving every claim and relationship.
3. Provide an equivalent narrow composition when rearrangement is clearer.
4. Use local scrolling only to preserve meaningful scale or spatial relations.

Keep essential labels at least 14px, captions at least 14px, and the document within the viewport. Do not hide page overflow to mask failures. For print, split dense figures or supply an equivalent table with `.ihd-print-only`; captions and conclusions remain available.
