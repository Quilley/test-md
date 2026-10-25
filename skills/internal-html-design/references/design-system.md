# Shared design reference

This is a presentation system for internal documents and explanations. A calling skill keeps its task, evidence standards and domain vocabulary. Apply these presentation defaults when the user explicitly requests this system; a task-specific request takes precedence. It does not automatically restyle other skills or provide an application UI kit.

## Identity and composition

Warm paper, dark slate-green ink, restrained emerald emphasis and generous whitespace. Serif titles give the page an editorial character; precise schematics carry difficult relationships. Avoid surrounding every paragraph with a box. Use borders to group a figure or comparison rather than decorate the whole page.

Use `assets/theme.css` for exact color, typography, width, spacing, radius and motion values. Change that stylesheet when adjusting a shared value. The files in `examples/source/` are authored examples, not competing token sources.

- Source Serif 4 supplies titles, headings, reading prose, quotations and display conclusions. Libre Franklin supplies labels, captions, controls, diagram annotations, table data and code. Small explanatory paragraphs still use Source Serif 4; text size alone does not determine the font. Use `.ihd-label` for annotations without another semantic pattern. Both families are bundled as variable fonts, so use their weights as supplied and do not synthesize styles. No italic files are bundled; a real italic needs its companion file.
- A reading column carries sustained prose. A wider figure can occupy the full page width. `ihd-split` stacks comparisons on narrow screens; `ihd-flow` turns a horizontal process into a vertical sequence.
- Use an emerald accent for emphasis and selection. Red and amber have semantic meanings and require labels or line patterns alongside color. Charts needing more categories should add distinguishable marks and a legend rather than improvise another visual theme.
- Default to the light treatment. `data-ihd-theme="dark"` on the root selects the matched dark treatment. The reader script supplies an optional persistent toggle; without JavaScript the page stays readable in light appearance.

Visuals should establish a relationship, change, mechanism or limit. Introduce the question, show the figure, and explain what it establishes. One piece may need several compositions. Use inline SVG for custom schematics; render library-created charts or graphs to inline SVG at authoring time rather than loading a remote runtime. Keep labels legible on mobile: reflow or simplify a diagram instead of shrinking a dense canvas into unreadable text. Pair each substantive visual with a caption or accessible description.

## Compose from semantic patterns

The starter supplies the page shell, optional theme control and two inlining markers. It is an authoring input, not a finished artifact. Keep one descriptive H1 and a logical heading hierarchy. Add language and meaningful page title.

| Need | Pattern |
| --- | --- |
| Sustained argument | `.ihd-reading` inside a section; headings only where orientation helps |
| Wide explanation | `figure.ihd-figure` with a label, diagram and `figcaption` |
| Comparison | `.ihd-split` containing independently labeled figures or panels |
| Sequential mechanism | `.ihd-flow`, labeled `.ihd-node` elements and decorative arrows hidden from assistive technology |
| Evidence or assumptions | A real `table` with caption and scoped headers inside `.ihd-table-wrap` |
| Important qualification | `.ihd-note`, or `.ihd-note--warning` with a textual warning |
| Source support | Linked superscripts, body caveats and `.ihd-footnotes`; preserve the caller's citation requirements |
| Controls | Real labeled inputs and buttons inside `.ihd-controls`; render a useful static baseline |

Use domain labels rather than architecture-specific terms inherited from the original report. Keep source, observation, assumption and inference distinguishable. Constructed values in a mockup must be identified as such.

## Guided explanations and simulations

Scrolling is the default. In a guided sequence, put each complete step in a direct child with `data-ihd-step` inside a `data-ihd-steps` section. Use ordinary headings and prose. Put the controls in `data-ihd-step-controls`, initially `hidden`, with:

```html
<div class="ihd-controls" data-ihd-step-controls hidden>
  <button type="button" data-ihd-step-toggle aria-pressed="false">Guide me</button>
  <div class="ihd-step-nav" data-ihd-step-nav hidden>
    <button type="button" data-ihd-previous>Previous</button>
    <span class="ihd-step-status" data-ihd-step-status role="status" aria-live="polite"></span>
    <button type="button" data-ihd-next>Next</button>
  </div>
</div>
```

`assets/reader.js` progressively adds guidance. It leaves all steps visible until the reader chooses “Guide me”, supports ordinary keyboard activation, moves focus to the new step heading, and allows returning to the full text. Use one step group per sequence; groups operate independently.

Keep a simulation's domain logic in its own inline script. The shared reader script only handles appearance and step navigation. Explain units, assumptions, the baseline and limitations in static text. Reveal interactive controls after their handlers are attached. Respect reduced motion, avoid autoplay, and keep each result accessible to assistive technology. JavaScript-disabled reading must retain the baseline figure and substantive explanation.

## Fonts and offline delivery

`assets/fonts/` holds Source Serif 4 and Libre Franklin as variable TrueType files, each with its SIL Open Font License text. `assets/fonts.css` declares them as `IHD Source Serif 4` and `IHD Libre Franklin`, and `assets/theme.css` maps those names to the serif and sans roles. Both licenses allow embedding and redistribution when the license notice is kept, so finished internal documents may use these files directly.

Change the pairing in `theme.css` and `fonts.css` together. Do not swap a family silently inside a single document.

For a document, author semantic HTML containing exactly one `<!-- ihd:styles -->` marker in the head and one `<!-- ihd:reader -->` marker near the end of the body, then run:

```sh
python3 ~/.claude/skills/internal-html-design/scripts/inline.py input.html output.html --bundled-fonts
```

Every output embeds both families, adding about 1.9 MB of base64 to the page. Subsetting would shrink that, but this skill does not include a subsetting step.

For other licensed fonts, pass `--font-css /absolute/path/to/font-faces.css` instead. That file defines the families and weights, using font files beneath its directory. The helper does not check licenses; that remains the author's responsibility.

The helper inserts the canonical theme and reader, embeds referenced font bytes without conversion, and refuses to overwrite an existing output. It rejects external or remaining local rendering dependencies. It does not render Markdown, rewrite prose, fetch resources or publish anything. Inline other images and scripts before using it. Ordinary citation links are allowed. Validate any authored runtime offline as well; static dependency checks cannot prove arbitrary JavaScript never makes network requests.

## Verification and reuse

Open every result in a browser. Check actual font-face loading, mobile reflow, readable figure labels, light/dark contrast, focus visibility, controls, reduced motion and offline behavior. With JavaScript disabled, all sections, figure descriptions and baseline conclusions must remain accessible. Check that applying the system preserved supplied wording and any prior interactions.

The bundled unit tests cover the inliner:

```sh
python3 -m unittest discover -s ~/.claude/skills/internal-html-design/tests -p 'test_*.py'
```

Browser checks are not bundled. Use the host's browser tooling and record what was checked.

Invoke `/internal-html-design` together with the task that produces the document. The skill is manual only.
