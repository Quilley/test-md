const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const {measurePage,loadFonts}=require('../scripts/audit_layout.cjs');
const root=path.resolve(__dirname,'..');
const theme=fs.readFileSync(path.join(root,'assets/theme.css'),'utf8');
const {pathToFileURL}=require('node:url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  await page.setContent(`<style>${theme}</style><main><section class="ihd-prose" style="width:448px"><p>A long label and a paragraph must adapt to the actual space available inside a desktop reading group. This example is intentionally wider than a phone viewport but narrower than the full page.</p></section><div class="ihd-visual" style="width:320px"><div class="ihd-flow"><div class="ihd-node"><span class="ihd-node-label">A deliberately long category label that must wrap instead of shrinking</span></div><span class="ihd-arrow">→</span><div class="ihd-node">Next step</div></div></div></main>`);
  for(const [width,alignment] of [[447,'left'],[448,'left'],[449,'justify']]){
   await page.locator('.ihd-prose').evaluate((el,width)=>el.style.width=width+'px',width);
   assert.equal(await page.locator('p').evaluate(el=>getComputedStyle(el).textAlign),alignment,`Prose must adapt at actual ${width}px`);
  }
  const nodes=await page.locator('.ihd-node').evaluateAll(nodes=>nodes.map(x=>x.getBoundingClientRect().toJSON()));
  assert(nodes[1].top>nodes[0].bottom,'A nested desktop visual must stack its nodes');
  assert.deepEqual((await measurePage(page)).failures,[]);
  await page.setContent(`<style>${theme}</style><main><svg width="900" height="100" viewBox="0 0 900 100" style="width:300px"><text x="20" y="50" style="font-size:18px">Shrunk essential label</text></svg><div style="width:1800px">Overflow fixture</div></main>`);
  const broken=await measurePage(page);
  assert(broken.failures.some(x=>x.kind==='small-essential-label'),'Audit must catch scaled-down SVG text');
  assert(broken.failures.some(x=>x.kind==='page-overflow'),'Audit must catch document overflow');
  await page.setContent(`<style>${theme}</style><main><svg width="400" height="100"><defs><clipPath id="cut"><rect width="5" height="100"/></clipPath></defs><g clip-path="url(#cut)"><text x="20" y="50" style="font-size:18px">Clipped inside the canvas</text></g></svg></main>`);
  assert((await measurePage(page)).findings.some(x=>x.kind==='review-svg-text-clipping'),'Clip paths on essential text require explicit visual review');
  await page.setContent(`<style>${theme}</style><main><figure><svg width="100" height="40"><path d="M0 20H100" style="fill:none;stroke:#d1d1d1;stroke-width:3"/></svg></figure><p id="same" style="color:#c00">One</p><p id="same">Two</p></main>`);
  const palette=await measurePage(page);
  assert(palette.failures.some(x=>x.kind==='duplicate-id'),'Audit must catch duplicate IDs');
  assert(palette.findings.some(x=>x.kind==='figure-without-caption'),'Audit must report a figure with no caption');
  assert(palette.findings.some(x=>x.kind==='colour-outside-ink-ramp'),'Audit must report colour outside the ink ramp');
  assert(palette.findings.some(x=>x.kind==='low-graphic-contrast'),'Audit must report a line under 3:1');
  const prose=Array.from({length:300},(_,i)=>'word'+i).join(' ');
  await page.setContent(`<style>${theme}</style><main><section><h2>Long</h2><p>${prose}</p></section><section><h2>Pictured</h2><p>${prose}</p><figure><svg width="10" height="10"><rect width="10" height="10"/></svg><figcaption>x</figcaption></figure></section><div class="ihd-visual"><svg class="ihd-diagram-wide" width="100" height="40"><rect width="100" height="40"/></svg></div></main>`);
  const structure=await measurePage(page);
  assert.equal(structure.findings.filter(x=>x.kind==='prose-section-without-figure').length,1,'Only the long section with no picture is reported');
  assert(structure.failures.some(x=>x.kind==='diagram-without-narrow-alternative'),'A wide diagram with no narrow alternative fails');
  await page.goto(pathToFileURL(path.join(root,'examples/long-document.html')).href);await loadFonts(page);
  assert(await page.locator('.ihd-toc').evaluate(el=>getComputedStyle(el).position==='sticky'&&el.open),'Contents is an open sticky rail from 80rem');
  await page.mouse.wheel(0,900);await page.waitForTimeout(300);
  assert(await page.locator('.ihd-toc [aria-current="location"]').count()===1,'Scroll marks one current section in the rail');
  assert((await page.locator('.ihd-toc').boundingBox()).y>0,'Rail stays in view while scrolling');
  await page.setViewportSize({width:1279,height:900});await page.waitForTimeout(200);
  assert(await page.locator('.ihd-toc').evaluate(el=>getComputedStyle(el).position!=='sticky'&&!el.open),'Below 80rem contents is a collapsed disclosure');
  await page.locator('.ihd-toc summary').focus();await page.keyboard.press('Enter');
  assert(await page.locator('.ihd-toc').evaluate(el=>el.open),'Contents works by keyboard');
  await page.getByRole('link',{name:'The mechanism',exact:true}).click();assert((await page.url()).endsWith('#mechanism'));
  await page.locator('#cite-rule-1').click();assert((await page.url()).endsWith('#note-rule'));
  await page.getByRole('link',{name:'Return to first citation of note 1',exact:true}).click();assert((await page.url()).endsWith('#cite-rule-1'));
  await page.emulateMedia({media:'print'});assert(await page.locator('#term-capacity').isVisible());assert(await page.locator('#note-rule').isVisible());
  await page.close();console.log('Container adaptation, broken-layout detection and document navigation passed.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
