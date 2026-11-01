# Optional compositions

## Documents

Use the starter as a shell, or omit its masthead/footer if they add no context. Keep the title, sustained argument and conclusions in a reading column. Use a wider section only for a figure, comparison or table that benefits from it. The evidence report demonstrates how to keep input assumptions beside an inference; its subject and number of sections are not requirements.

## Builds and continuous visuals

A build can introduce a mechanism with a framed visual, then provide the explanation and controls below. Keep the hero primarily visual. Prefer a short caption; put extended method and teaching below it. Include the meaning in an accessible description and static prose; keep explanatory statistics and teaching steps in the explanation where they help.

For a continuous visual, use this lifecycle wrapper (see the catalogue for the complete orbit):

```html
<figure class="ihd-figure" data-ihd-motion>
  <button type="button" data-ihd-motion-toggle aria-pressed="false" hidden>Pause motion</button>
  <!-- Accessible SVG with a meaningful static pose. -->
  <figcaption>The mechanism, stated independently of animation.</figcaption>
</figure>
```

Define the CSS animation on its moving element at all times. The shared CSS controls `animation-play-state`, preserving phase when paused. Make the loop continuous at its seam. The shared reader runs only while the wrapper intersects the viewport, the document is visible, the reader has not paused it and reduced motion is off. It pauses for printing. With no script, the figure remains still and the control stays hidden. With reduced motion, it stays still and the revealed control explains “Motion reduced”.

For a custom canvas or JavaScript renderer, listen to `ihd:motionchange` on the wrapper and read `event.detail.running`. Initialize from `wrapper.dataset.ihdRunning === 'true'`. Start/cancel the renderer's animation frame when this state changes; the reader does not render or change model values. Preserve phase across suspension and bound elapsed deltas on resumption. Render the meaningful baseline before any animation frame. A static CSS/SVG composition is simpler when it explains the same idea.

## Responsive figures and controls

Read [visual recipes](visual-recipes.md) for figure choice, essential label sizes, equivalent narrow compositions and meaningful local scrolling. Use `.ihd-visual` inside a figure with an established width, and `.ihd-prose` around text groups in interactive layouts. Keep labels, units, assumptions and a useful baseline beside controls. The producer owns calculations and data.

## Guided teaching

Guided steps are appropriate for an actual teaching sequence, independently of any hero animation. All panels appear in normal flow until the reader chooses “Guide me”. Keep the existing hooks:

```html
<section data-ihd-steps aria-label="Explanation sequence">
  <div class="ihd-controls" data-ihd-step-controls hidden>
    <button type="button" data-ihd-step-toggle aria-pressed="false">Guide me</button>
    <div class="ihd-step-nav" data-ihd-step-nav hidden>
      <button type="button" data-ihd-previous>Previous</button>
      <span data-ihd-step-status role="status" aria-live="polite"></span>
      <button type="button" data-ihd-next>Next</button>
    </div>
  </div>
  <section data-ihd-step><h2>First explanation</h2><!-- Complete content --></section>
  <section data-ihd-step><h2>Next explanation</h2><!-- Complete content --></section>
</section>
```

Panels are direct children of the group. Every group has its own controls and state. Previous/Next move focus to the newly shown heading. “Read all steps” restores the whole explanation. Printing reveals every step. Preserve a readable static baseline for any model controls inside the sequence.

## Landing pages and native scrolling

A landing page can use a simple wordmark, centered opening statement, restrained section headings and a contact link. Preserve the requested copy and information hierarchy. The landing example includes optional patterns to demonstrate them; a page need not use every pattern.

Add `data-ihd-landing` to the page container and `data-ihd-wordmark` to an optional `.ihd-wordmark`. The reader updates `--ihd-intro-progress` between 0 and 1 as the native scroll advances, then reverses it when scrolling back. The default wordmark moves slightly within its normal-flow space; text and sections remain available throughout. Geometry is cached on layout/font/viewport changes, and scroll work is scheduled once per animation frame. Reduced motion leaves the wordmark stationary.

Keep normal wheel, touch, keyboard, anchor and history behavior. Reading progress must never depend on a timer, locked gesture, forced scroll target or first-pass state. A wordmark is optional branding, not a mandatory introduction to every document.

## Contents rail

For a long document, wrap the contents disclosure and `main` in `div.ihd-doc`, contents first (see the [system explainer](../examples/source/system-explainer.html)). From 80rem the contents sit in a sticky left column, the reading column stays centered and `.ihd-wide` blocks extend over the rail's space. Below 80rem the contents are an ordinary disclosure above the page. `.ihd-margin-note` keeps the right column. The rail starts under an adaptive masthead's height and scrolls inside itself when the list is long. Nested lists indent one level; keep the list to section titles.

## Adaptive mastheads

A static `.ihd-masthead` can contain a brand and a wrapping `nav`. Add `data-ihd-masthead` only for a header that should leave on downward scroll and return upward. It uses a solid paper background and a short fade edge. Focus within the header restores it, including when a link receives keyboard focus while the header is away. Keep labels short, controls reachable and spacing fluid. Do not add a navigation bar to a document that has no navigation needs.
