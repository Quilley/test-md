# Reading quality and long documents

## Reading task

State what the reader should understand or decide. The page should reveal the question, the relationship that explains it, and the supported conclusion without requiring an interaction. The producer supplies the argument and evidence. Presentation may organize that material without inventing data, definitions or certainty.

Use one title and a clear heading hierarchy. A deck adds context rather than repeating the title. Keep sustained text in the reading column and alternate prose with figures only where that helps the argument. Avoid filling a page with components just because they are available.

Prose uses Newsreader 480 at 18px / 1.6. `.ihd-prose` switches narrow text groups to left alignment at 448px. In narrow left-aligned prose, keep whole words where possible and let unbreakable strings wrap. Inspect word spacing, not just box width. Retain whitespace that separates ideas; trim empty figure canvas and repeated framing. Captions, controls and lists are aligned left and use their own roles.

## Optional long-document navigation

The [long-document source](../examples/source/long-document.html) is the complete example. Use these patterns only when the material warrants them:

- A native `details.ihd-toc` contains `nav aria-label="Contents"` and ordinary section links. Put it first inside `div.ihd-doc`, before `main`. Below 80rem it is a collapsed disclosure above the page that opens by keyboard. From 80rem the same markup becomes a sticky left rail beside the reading column, with the current section marked in ink and a square marker. The rail fades while a `.ihd-wide` figure or an element marked `data-ihd-breakout` crosses it, and stays reachable by keyboard. Without the script the links and disclosure still work. Use a rail for documents with enough sections to need a map; a short page needs neither.
- Heading IDs are stable, descriptive and unique. Links land on readable headings without an overlay covering them. Native browser history, keyboard and anchor behavior remain intact.
- A `dl.ihd-glossary` renders supplied terms and definitions. Use `dfn` IDs for direct links. Essential explanations remain in the argument; definitions are not hidden in hover tooltips.
- Source notes use `.ihd-footnotes`, numbered links with unique citation IDs and explicit return links. Repeated references to a note receive separate backlinks. Keep evidence, assumptions and calculations distinguishable.

Printing includes glossary and source notes and omits the contents disclosure. Supplied copy and source meaning remain intact. Navigation aids are optional, never a mandatory opening ceremony.

## Review and delivery

Run `node scripts/audit_layout.cjs /absolute/result.html` from the installed skill directory when Playwright and Chromium are available. `NODE_PATH` and `PLAYWRIGHT_CHROMIUM_EXECUTABLE` can point to an existing installation. The audit writes a report and screenshots to a new temporary directory; it never installs dependencies. Its report distinguishes failed checks, advisory findings and incomplete browser access.

Review all generated screenshots. Automation cannot decide whether a plot makes a relationship clear or whether a page feels balanced. Check:

| Area | Acceptance |
| --- | --- |
| Reader task | The question, explanatory relationship and supported conclusion are visible without interaction |
| Type | Actual fonts load; prose is 480/18px/1.6; labels and captions are readable |
| Geometry | No page overflow, clipped text, colliding labels, cropped arrows or wasteful canvas |
| Adaptation | 320, 390, 768, 1024 and 1440px; also 1279 and 1280px for the rail, narrow desktop containers and layout transition widths |
| Figures | Every figure has a caption that states the takeaway and a text or table equivalent; series are told apart without shade; every graphic clears 3:1 on paper |
| Reading rhythm | Comfortable headings, paragraph spacing, captions and word spacing; no accidental dense wall or empty panel |
| Interaction | Keyboard focus, 44px controls, labels/units, meaningful baseline and reversible state |
| Access | Contrast at least 4.5:1 for ordinary text, 200% zoom, no essential hover-only content |
| Fallbacks | Offline fonts/assets, meaningful static content without JavaScript, reduced motion and complete print content |

Stress long headings, labels, URLs, table cells and control groups. SVG labels are checked at their effective screen size, not their authored font size. Likely overlaps and clip paths on SVG text are review findings, since intentional overlays can be valid. The audit also measures labels at an A4 content width before saving the print PDF. Compare default model marks with their labels before interacting.

Before delivery, correct failures and inspect again at affected sizes. State remaining unverified behavior plainly; never turn a blocked check into a pass. Give the absolute artifact path, relevant previews and the verification result. Use the current host's available browser/image tools; no particular host integration is required.
