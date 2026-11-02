// Run with an existing Playwright installation. No dependencies are installed here.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const output = fs.mkdtempSync(path.join(os.tmpdir(), 'ihd-browser-check-'));
const examples = ['visual-essay', 'evidence-report', 'guided-explainer', 'landing', 'component-catalogue', 'visual-toolkit', 'long-document', 'system-explainer', 'data-charts'];
const { measurePage } = require('../scripts/audit_layout.cjs');

async function loadFonts(page) {
  await page.evaluate(async () => {
    await Promise.all([
      document.fonts.load('480 18px "IHD Serif"'),
      document.fonts.load('italic 480 18px "IHD Serif"'),
      document.fonts.load('450 18px "IHD Sans"'),
      document.fonts.load('550 20px "IHD Sans"'),
      document.fonts.load('400 14px "IHD Mono"'),
    ]);
    await document.fonts.ready;
  });
}

async function platformFonts(page, selector) {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');
  const { root: doc } = await cdp.send('DOM.getDocument');
  const index = await page.evaluate(selector => [...document.querySelectorAll(selector)].findIndex(element => element.getClientRects().length > 0), selector);
  const { nodeIds } = await cdp.send('DOM.querySelectorAll', { nodeId: doc.nodeId, selector });
  const nodeId = nodeIds[index];
  assert(nodeId, `Expected an element matching ${selector}`);
  const { fonts } = await cdp.send('CSS.getPlatformFontsForNode', { nodeId });
  await cdp.detach();
  return fonts.map(font => font.familyName);
}

async function contrastRatio(page, selector) {
  return page.locator(selector).first().evaluate(element => {
    const rgb = value => {
      const channels = value.match(/[\d.]+/g);
      return channels && channels.length >= 3 ? channels.slice(0, 3).map(Number) : null;
    };
    const luminance = color => {
      const linear = color.map(value => value / 255).map(value => value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4);
      return linear[0] * .2126 + linear[1] * .7152 + linear[2] * .0722;
    };
    const foreground = rgb(getComputedStyle(element).color);
    let node = element;
    let background = null;
    while (node && !background) {
      const color = rgb(getComputedStyle(node).backgroundColor);
      if (color && getComputedStyle(node).backgroundColor !== 'rgba(0, 0, 0, 0)') background = color;
      node = node.parentElement;
    }
    if (!foreground || !background) return null;
    const a = luminance(foreground), b = luminance(background);
    return (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
  });
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE });
  const results = [];
  try {
    for (const name of examples) {
      const isolated = path.join(output, `${name}.html`);
      fs.copyFileSync(path.join(root, 'examples', `${name}.html`), isolated);
      for (const width of [320, 390, 768, 1024, 1440]) {
        const context = await browser.newContext({ viewport: { width, height: 900 }, offline: true });
        const page = await context.newPage();
        const errors = [];
        const network = [];
        page.on('pageerror', error => errors.push(error.message));
        page.on('request', request => { if (/^https?:/.test(request.url())) network.push(request.url()); });
        await page.addInitScript(() => localStorage.setItem('internal-html-design:theme', 'dark'));
        await page.goto(pathToFileURL(isolated).href);
        await loadFonts(page);

        const quality = await measurePage(page);
        assert.deepEqual(quality.failures, [], `${name} at ${width}px: ${JSON.stringify(quality.failures)}`);
        const definedFonts = await page.evaluate(() => [...document.fonts].map(face => ({ family: face.family, status: face.status })));
        await page.screenshot({ path: path.join(output, `${name}-${width}.png`), fullPage: true });
        for (const family of ['IHD Serif', 'IHD Sans', 'IHD Mono']) {
          assert(definedFonts.some(face => face.family.includes(family) && face.status === 'loaded'), `${name}: ${family} alias must load offline`);
        }
        assert.equal(await page.evaluate(() => document.documentElement.dataset.ihdTheme), 'light', 'Old appearance state is ignored.');
        assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).colorScheme), 'light');
        assert.equal(await page.locator('[data-ihd-theme-toggle]').count(), 0, 'The light-only system has no appearance toggle.');
        assert.equal(await page.locator('h1').count(), 1);
        assert(await page.locator('main').isVisible());
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${name} overflows at ${width}px`);
        assert(await page.evaluate(() => getComputedStyle(document.body).fontSynthesis === 'none'));
        const body = await page.locator('body').evaluate(element => {
          const style = getComputedStyle(element);
          return { family: style.fontFamily, size: parseFloat(style.fontSize), lineHeight: parseFloat(style.lineHeight) };
        });
        assert(body.family.includes('IHD Serif'), `${name}: body uses the serif alias`);
        assert(Math.abs(body.size - 18) < .1, `${name}: body size is ${body.size}px`);
        assert(Math.abs(body.lineHeight - 28.8) < .2, `${name}: body line height is ${body.lineHeight}px`);
        assert.equal(await page.locator('body').evaluate(element => getComputedStyle(element).fontWeight), '480');
        assert.equal(await page.locator('h1').evaluate(element => getComputedStyle(element).fontWeight), '400');
        assert((await platformFonts(page, 'h1')).some(family => family.includes('Newsreader')), `${name}: heading must render with Newsreader`);
        assert((await platformFonts(page, '.ihd-section.ihd-reading > p:not([class])')).some(family => family.includes('Newsreader')), `${name}: prose must render with Newsreader`);
        assert.equal(await page.locator('h2').first().evaluate(element => getComputedStyle(element).fontWeight), '550');
        assert((await platformFonts(page, 'h2')).some(family => family.includes('Manrope')), `${name}: section heading must render with Manrope`);
        if (await page.locator('figcaption').count()) {
          assert((await platformFonts(page, 'figcaption')).some(family => family.includes('Manrope')), `${name}: captions must render with Manrope`);
        }
        if (await page.locator('.ihd-eyebrow').count()) {
          assert((await platformFonts(page, '.ihd-eyebrow')).some(family => family.includes('Manrope')), `${name}: labels must render with Manrope`);
        }
        if (name === 'component-catalogue') {
          for (const [selector, family] of [['h2', 'Manrope'], ['figcaption', 'Manrope'], ['code', 'Geist Mono']]) {
            assert(await page.locator(selector).count(), `Component catalogue includes ${selector}`);
            assert((await platformFonts(page, selector)).some(name => name.includes(family)), `${selector} must render with ${family}`);
          }
        }
        const contrastTargets = [];
        for (const selector of ['h1', 'main p', 'figcaption', 'button', 'summary', 'code']) {
          if (await page.locator(selector).count()) contrastTargets.push(selector);
        }
        for (const selector of contrastTargets) {
          const ratio = await contrastRatio(page, selector);
          if (ratio !== null) assert(ratio >= 4.5, `${name}: ${selector} contrast ${ratio.toFixed(2)}:1 is below 4.5:1`);
        }

        // From 80rem a .ihd-doc contents disclosure becomes a rail and its summary is hidden by design.
        const details = page.locator('details:not(.ihd-doc > .ihd-toc) summary, .ihd-doc > .ihd-toc summary:visible').first();
        if (name === 'component-catalogue') assert(await details.count(), 'Component catalogue includes native details');
        if (await details.count()) {
          await details.focus();
          assert.equal(await details.evaluate(element => element.ownerDocument.activeElement === element), true, `${name}: native summary receives keyboard focus`);
          await page.keyboard.press('Enter');
          assert.equal(await details.locator('xpath=..').evaluate(element => element.open), true, `${name}: Enter opens native details`);
        }
        assert(await page.locator(':focus-visible').count() || await page.locator(':focus').count() === 0, `${name}: focused controls keep a visible focus indication`);

        if (name === 'guided-explainer') {
          const steps = page.locator('[data-ihd-step]');
          assert((await steps.count()) >= 2, 'Guided explainer keeps its guided steps');
          assert.equal(await page.locator('[data-ihd-step]:visible').count(), await steps.count(), 'All steps start available');
          const toggle = page.locator('[data-ihd-step-toggle]');
          assert.equal(await toggle.count(), 1);
          await toggle.focus();
          await page.keyboard.press('Enter');
          assert.equal(await page.locator('[data-ihd-step]:visible').count(), 1, 'Guided mode shows one step');
          const next = page.locator('[data-ihd-next]');
          while (!(await next.isDisabled())) await next.click();
          assert(await next.isDisabled());
          await page.emulateMedia({ media: 'print' });
          assert.equal(await page.locator('[data-ihd-step]:visible').count(), await steps.count(), 'Print includes every guided step');
        }

        if (name === 'component-catalogue' && await page.locator('[data-ihd-motion]').count()) {
          const motion = page.locator('[data-ihd-motion]').first();
          const toggle = page.locator('[data-ihd-motion-toggle]').first();
          assert.equal(await toggle.isVisible(), true, 'Motion control is revealed after JavaScript initializes');
          const animated = motion.locator('.ihd-orbit');
          assert.equal(await animated.count(), 1, 'Motion sample exposes its animated element');
          await motion.scrollIntoViewIfNeeded();
          await page.waitForFunction(() => document.querySelector('[data-ihd-motion]')?.dataset.ihdRunning === 'true');
          const initialTransform = await animated.evaluate(element => getComputedStyle(element).transform);
          await page.waitForTimeout(300);
          assert.notEqual(await animated.evaluate(element => getComputedStyle(element).transform), initialTransform, 'Running motion changes the sample transform');
          await toggle.click();
          assert.equal(await motion.getAttribute('data-ihd-running'), 'false');
          assert.equal(await toggle.getAttribute('aria-pressed'), 'true');
          assert.equal(await animated.evaluate(element => getComputedStyle(element).animationPlayState), 'paused');
          await animated.evaluate(async element => { await Promise.all(element.getAnimations().map(animation => animation.ready)); });
          const paused = await animated.evaluate(element => getComputedStyle(element).transform);
          await page.waitForTimeout(300);
          assert.equal(await animated.evaluate(element => getComputedStyle(element).transform), paused, 'Paused motion remains visually stable');
          await toggle.click();
          assert.equal(await motion.getAttribute('data-ihd-running'), 'true');
          await page.evaluate(() => {
            Object.defineProperty(document, 'hidden', { configurable: true, get: () => true });
            document.dispatchEvent(new Event('visibilitychange'));
          });
          assert.equal(await motion.getAttribute('data-ihd-running'), 'false', 'Simulated hidden-tab motion pauses');
          await page.evaluate(() => {
            delete document.hidden;
            document.dispatchEvent(new Event('visibilitychange'));
          });
          await page.waitForFunction(() => document.querySelector('[data-ihd-motion]')?.dataset.ihdRunning === 'true');
          await motion.evaluate(element => { element.style.position = 'fixed'; element.style.top = '150vh'; });
          await page.waitForFunction(() => document.querySelector('[data-ihd-motion]')?.dataset.ihdRunning === 'false');
          assert.equal(await motion.getAttribute('data-ihd-running'), 'false', 'Offscreen motion pauses');
          const motionContext = await browser.newContext({ viewport: { width: 390, height: 900 }, reducedMotion: 'reduce', offline: true });
          const reducedPage = await motionContext.newPage();
          await reducedPage.goto(pathToFileURL(isolated).href);
          const reducedMotion = reducedPage.locator('[data-ihd-motion]').first();
          const reducedAnimated = reducedMotion.locator('.ihd-orbit');
          assert.equal(await reducedMotion.getAttribute('data-ihd-running'), 'false', 'Reduced motion does not auto-start');
          const reducedTransform = await reducedAnimated.evaluate(element => getComputedStyle(element).transform);
          await reducedPage.waitForTimeout(300);
          assert.equal(await reducedAnimated.evaluate(element => getComputedStyle(element).transform), reducedTransform, 'Reduced motion has no automatic animation');
          assert.equal(await reducedMotion.locator('[data-ihd-motion-toggle]').isDisabled(), true, 'Reduced motion disables playback');
          await motionContext.close();
        }

        if (name === 'landing' && await page.locator('[data-ihd-landing]').count()) {
          const intro = page.locator('[data-ihd-landing]');
          assert(await page.locator('[data-ihd-wordmark]').count());
          const progress = async () => Number(await intro.evaluate(element => getComputedStyle(element).getPropertyValue('--ihd-intro-progress').trim()));
          await page.evaluate(() => scrollTo(0, 0));
          await page.waitForTimeout(80);
          const top = await progress();
          await page.mouse.wheel(0, 400);
          await page.waitForFunction(() => window.scrollY > 50);
          assert((await progress()) > top, 'Native wheel scrolling advances the intro without a lock');
          await page.keyboard.press('PageDown');
          await page.waitForFunction(() => window.scrollY > 400);
          await page.evaluate(() => scrollTo(0, document.documentElement.scrollHeight));
          await page.waitForTimeout(120);
          const bottom = await progress();
          assert(bottom >= top, 'Landing intro progress follows scroll down');
          await page.evaluate(() => scrollTo(0, 0));
          await page.waitForTimeout(120);
          assert((await progress()) <= bottom, 'Landing intro progress reverses on scroll up');
          const masthead = page.locator('[data-ihd-masthead]').first();
          if (await masthead.count()) {
            await page.evaluate(() => scrollTo(0, document.documentElement.scrollHeight));
            await page.waitForTimeout(120);
            assert.equal(await masthead.getAttribute('data-ihd-away'), 'true');
            await masthead.getByRole('link').first().focus();
            await page.waitForFunction(() => {
              const style = getComputedStyle(document.querySelector('[data-ihd-masthead]'));
              return style.transform === 'none' || style.transform === 'matrix(1, 0, 0, 1, 0, 0)';
            });
            const headerTop = await masthead.evaluate(element => element.getBoundingClientRect().top);
            assert(headerTop >= -1 && headerTop < 200, 'Focused masthead returns to view while scrolled away');
            await page.evaluate(() => scrollTo(0, 0));
            await page.waitForTimeout(120);
            assert.equal(await masthead.getAttribute('data-ihd-away'), 'false');
          }
        }

        assert.deepEqual(network, [], 'Offline documents make no HTTP requests');
        assert.deepEqual(errors, [], 'No browser runtime errors');
        results.push({ name, width, offline: true, fonts: 'loaded', body, errors });
        await context.close();
      }

      const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 900 }, offline: true });
      const page = await context.newPage();
      await page.goto(pathToFileURL(isolated).href);
      assert(await page.locator('main').isVisible());
      assert(await page.locator('h1').isVisible());
      const readableText = await page.locator('main').innerText();
      assert(readableText.trim().length > 100, `${name}: substantive content is available without JavaScript`);
      assert.equal(await page.locator('[data-ihd-theme-toggle]').count(), 0);
      if (name === 'guided-explainer') {
        assert((await page.locator('[data-ihd-step]:visible').count()) >= 2, 'Every step is available without JavaScript');
      }
      if (name === 'component-catalogue' && await page.locator('[data-ihd-motion-toggle]').count()) {
        assert.equal(await page.locator('[data-ihd-motion-toggle]').isVisible(), false, 'Motion control stays hidden when JavaScript is disabled');
      }
      await context.close();
    }
    fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify(results, null, 2));
    console.log(JSON.stringify({ passed: results.length, output, checks: results }, null, 2));
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
