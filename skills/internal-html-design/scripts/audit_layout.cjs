#!/usr/bin/env node
// Measurements are diagnostics. Screenshots still need a reader's visual judgment.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const widths = [320, 390, 488, 768, 1024, 1279, 1280, 1440];

async function loadFonts(page) {
  await page.evaluate(async () => {
    await Promise.all(['480 18px "IHD Serif"', 'italic 480 18px "IHD Serif"', '550 16px "IHD Sans"', '450 14px "IHD Mono"'].map(face => document.fonts.load(face)));
    await document.fonts.ready;
  });
}

async function measurePage(page) {
  return page.evaluate(() => {
    const failures = [], findings = [];
    const visible = el => {
      const r = el.getBoundingClientRect(), c = getComputedStyle(el);
      return r.width > 0 && r.height > 0 && c.visibility !== 'hidden' && !el.closest('[aria-hidden="true"]');
    };
    const describe = el => (el.textContent || el.getAttribute('aria-label') || el.tagName).trim().replace(/\s+/g, ' ').slice(0, 110);
    const rgb = value => {
      const parts=value.match(/[\d.]+/g);
      return parts && parts.length>=3 && (parts.length<4 || Number(parts[3])===1) ? parts.slice(0,3).map(Number) : null;
    };
    const luminance = channels => channels.map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((sum,v,i)=>sum+v*[.2126,.7152,.0722][i],0);
    for(const el of [...document.querySelectorAll('h1,h2,h3,p,label,figcaption,th,td,button,summary,svg text')].filter(visible)) {
      const c=getComputedStyle(el), foreground=rgb(el instanceof SVGElement ? c.fill : c.color);
      let background=null,node=el;
      while(node && !background){background=rgb(getComputedStyle(node).backgroundColor);node=node.parentElement;}
      if(foreground){
        const a=luminance(foreground), b=luminance(background || [255,255,255]);
        const ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);
        if(ratio<4.5) failures.push({kind:'low-text-contrast',text:describe(el),ratio:Math.round(ratio*100)/100});
      }
    }
    if (document.documentElement.scrollWidth > innerWidth + 1) failures.push({kind:'page-overflow', actual:document.documentElement.scrollWidth, available:innerWidth});
    const labels = [...document.querySelectorAll('svg text, .ihd-node-label, .ihd-legend, figcaption')].filter(visible).map(el => {
      const style = getComputedStyle(el), rect = el.getBoundingClientRect();
      const matrix = el instanceof SVGElement ? el.getScreenCTM() : null;
      const size = parseFloat(style.fontSize) * (matrix ? Math.hypot(matrix.c, matrix.d) : 1);
      const result = {text:describe(el), size:Math.round(size * 100) / 100};
      if (size < 13.99) failures.push({kind:'small-essential-label', ...result});
      if (el instanceof SVGElement) {
        const svg = el.ownerSVGElement, bounds = svg.getBoundingClientRect();
        if (rect.left < bounds.left - 2 || rect.right > bounds.right + 2 || rect.top < bounds.top - 2 || rect.bottom > bounds.bottom + 2)
          failures.push({kind:'svg-label-outside-canvas', text:result.text});
        for(let node=el;node;node=node.parentElement) {
          const c=getComputedStyle(node);
          if(c.clipPath!=='none' || c.maskImage!=='none') {
            findings.push({kind:'review-svg-text-clipping',text:result.text});
            break;
          }
          if(node===svg) break;
        }
      }
      return result;
    });
    for (const svg of document.querySelectorAll('svg')) {
      const texts = [...svg.querySelectorAll('text')].filter(visible);
      for (let i=0;i<texts.length;i++) for(let j=i+1;j<texts.length;j++) {
        const a=texts[i].getBoundingClientRect(), b=texts[j].getBoundingClientRect();
        if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>2 && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>2)
          findings.push({kind:'possible-label-overlap', text:[describe(texts[i]),describe(texts[j])]});
      }
    }
    for(const frame of document.querySelectorAll('.ihd-figure-scroll, .ihd-table-wrap')) {
      if(!visible(frame) || frame.scrollWidth <= frame.clientWidth + 1) continue;
      if(!frame.getAttribute('aria-label') && !frame.getAttribute('aria-labelledby')) failures.push({kind:'unnamed-scroll-region'});
      if(frame.tabIndex < 0) failures.push({kind:'unfocusable-scroll-region'});
    }
    for(const el of [...document.querySelectorAll('h1,h2,h3,p,label,th,td,.ihd-node')].filter(visible)) {
      const c=getComputedStyle(el);
      if(['hidden','clip'].includes(c.overflowX) && el.scrollWidth > el.clientWidth + 1) failures.push({kind:'clipped-text',text:describe(el)});
    }
    for(const el of [...document.querySelectorAll('button,input,select,textarea')].filter(visible)) {
      const r=el.getBoundingClientRect();
      if(r.width < 43.5 || r.height < 43.5) findings.push({kind:'small-control-target',text:describe(el),width:r.width,height:r.height});
    }
    for(const p of [...document.querySelectorAll('p')].filter(visible)) {
      if(p.children.length || p.textContent.length < 100 || getComputedStyle(p).textAlign !== 'justify') continue;
      const node=p.firstChild;
      if(!node || node.nodeType !== Node.TEXT_NODE) continue;
      const words=[...node.textContent.matchAll(/\S+/g)], boxes=[];
      for(const word of words){ const range=document.createRange();range.setStart(node,word.index);range.setEnd(node,word.index+word[0].length);boxes.push(range.getBoundingClientRect()); }
      const threshold=parseFloat(getComputedStyle(p).fontSize)*.9;
      if(boxes.some((box,i)=>i && Math.abs(box.top-boxes[i-1].top)<2 && box.left-boxes[i-1].right>threshold)) findings.push({kind:'wide-word-spacing',text:describe(p)});
    }
    // Structure and palette checks. Duplicate IDs break aria references and sprite markers.
    const ids = new Map();
    for (const el of document.querySelectorAll('[id]')) ids.set(el.id, (ids.get(el.id) || 0) + 1);
    for (const [id, count] of ids) if (count > 1) failures.push({kind:'duplicate-id', id, count});
    for (const fig of [...document.querySelectorAll('figure')].filter(visible)) {
      if (!fig.querySelector('figcaption, caption')) findings.push({kind:'figure-without-caption', text:describe(fig)});
    }
    const offInk = new Map();
    for (const el of [...document.querySelectorAll('body *')].filter(visible)) {
      const c = getComputedStyle(el);
      for (const prop of ['color', 'backgroundColor', 'borderTopColor', 'fill', 'stroke']) {
        const channels = rgb(c[prop] || '');
        if (channels && Math.max(...channels) - Math.min(...channels) > 8 && !offInk.has(c[prop]))
          offInk.set(c[prop], el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className ? '.' + el.className.split(' ')[0] : ''));
      }
    }
    for (const [colour, where] of offInk) findings.push({kind:'colour-outside-ink-ramp', colour, where});
    // A flat line has a zero-height box, so graphics use their own visibility test.
    for (const el of [...document.querySelectorAll('svg line, svg polyline, svg path')].filter(node => getComputedStyle(node).visibility !== 'hidden' && !node.closest('[aria-hidden="true"], defs, symbol, marker, pattern'))) {
      const c = getComputedStyle(el), stroke = rgb(c.stroke || '');
      if (!stroke || c.fill !== 'none') continue;
      const a = luminance(stroke), b = luminance([252, 252, 252]), ratio = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
      if (ratio < 3) findings.push({kind:'low-graphic-contrast', ratio:Math.round(ratio * 100) / 100, where:el.tagName});
    }
    const rail = document.querySelector('.ihd-doc > .ihd-toc');
    if (rail) {
      const wide = innerWidth >= 1280, railStyle = getComputedStyle(rail);
      if (wide && railStyle.position !== 'sticky') failures.push({kind:'rail-not-sticky'});
      if (!wide && railStyle.position === 'sticky') failures.push({kind:'rail-sticky-when-narrow'});
      if (wide) {
        const railBox = rail.getBoundingClientRect(), mainBox = document.querySelector('.ihd-doc > main').getBoundingClientRect();
        if (railBox.right > mainBox.left + 1) failures.push({kind:'rail-overlaps-column'});
        if (railBox.left < 0) failures.push({kind:'rail-outside-viewport'});
      }
    }
    const prose = document.querySelector('.ihd-prose > p:not([class]), main p:not([class]), p');
    const style = prose && getComputedStyle(prose);
    return {viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,
      prose:style ? {weight:style.fontWeight,size:style.fontSize,lineHeight:style.lineHeight,alignment:style.textAlign} : null,
      fonts:[...document.fonts].map(face=>({family:face.family,status:face.status})),labels,
      failures,findings:findings.slice(0,40)};
  });
}

async function actualFonts(page) {
  const cdp=await page.context().newCDPSession(page);
  try {
    await cdp.send('DOM.enable'); await cdp.send('CSS.enable');
    const {root}=await cdp.send('DOM.getDocument');
    const result={};
    for(const selector of ['h1','.ihd-prose > p:not([class])','h2']) {
      const {nodeIds}=await cdp.send('DOM.querySelectorAll',{nodeId:root.nodeId,selector});
      if(nodeIds.length) result[selector]=(await cdp.send('CSS.getPlatformFontsForNode',{nodeId:nodeIds[0]})).fonts.map(font=>font.familyName);
    }
    return result;
  } finally {await cdp.detach();}
}

async function audit(input) {
  const output=fs.mkdtempSync(path.join(os.tmpdir(),'ihd-audit-'));
  let browser;
  const report={input:path.resolve(input),output,status:'incomplete',screens:[],failures:[],notes:['Review screenshots for communicative purpose, spacing and meaningful visual hierarchy.','The zoom case simulates 200% browser reflow with a 720px CSS viewport and 2x pixel density; verify native zoom in the delivery browser where available.']};
  try {
    if(!fs.existsSync(report.input)) throw new Error('Input HTML does not exist.');
    let chromium;
    try {({chromium}=require('playwright'));} catch {throw new Error('Playwright is unavailable. Set NODE_PATH to an existing installation; no dependency was installed.');}
    try {browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE});}
    catch(error){throw new Error('Browser could not launch. Set PLAYWRIGHT_CHROMIUM_EXECUTABLE to an installed Chromium and allow the local browser process. '+error.message.split('\n')[0]);}
    const cases=[...widths.map(width=>({name:String(width),width,deviceScaleFactor:1})),{name:'zoom-200-reflow',width:720,deviceScaleFactor:2}];
    for(const spec of cases) {
      const context=await browser.newContext({viewport:{width:spec.width,height:900},deviceScaleFactor:spec.deviceScaleFactor,offline:true});
      const page=await context.newPage(), runtime=[], network=[];
      page.on('pageerror',error=>runtime.push(error.message));
      page.on('request',request=>{if(/^https?:/.test(request.url())) network.push(request.url());});
      await page.goto(pathToFileURL(report.input).href); await loadFonts(page);
      const measured=await measurePage(page);
      for(const family of ['IHD Serif','IHD Sans','IHD Mono']) {
        if(!measured.fonts.some(face=>face.family.replace(/["']/g,'')===family && face.status==='loaded')) measured.failures.push({kind:'missing-local-font',family});
      }
      if(runtime.length) measured.failures.push({kind:'runtime-errors',messages:runtime});
      if(network.length) measured.failures.push({kind:'network-dependencies',urls:network});
      const fonts=await actualFonts(page);
      const screenshot=path.join(output,spec.name+'.png'); await page.screenshot({path:screenshot,fullPage:true});
      report.screens.push({name:spec.name,...measured,platformFonts:fonts,screenshot});
      report.failures.push(...measured.failures.map(f=>({screen:spec.name,...f})));
      await context.close();
    }
    const plain=await browser.newContext({javaScriptEnabled:false,offline:true,viewport:{width:390,height:900}});
    const page=await plain.newPage(); await page.goto(pathToFileURL(report.input).href); await loadFonts(page);
    report.noJavaScript={substantiveText:(await page.locator('main').innerText()).trim().length,screenshot:path.join(output,'no-javascript.png')};
    await page.screenshot({path:report.noJavaScript.screenshot,fullPage:true});
    if(report.noJavaScript.substantiveText < 100) report.failures.push({kind:'insufficient-static-content'});
    await plain.close();
    // A4 minus two 16mm margins is approximately 673 CSS pixels.
    const print=await browser.newPage({viewport:{width:673,height:952}}); await print.goto(pathToFileURL(report.input).href);await loadFonts(print);await print.emulateMedia({media:'print'});
    report.print={pdf:path.join(output,'print.pdf'),layout:await measurePage(print)};
    report.failures.push(...report.print.layout.failures.map(f=>({screen:'print-a4',...f})));
    await print.pdf({path:report.print.pdf,format:'A4',margin:{top:'16mm',right:'16mm',bottom:'16mm',left:'16mm'},printBackground:true});await print.close();
    report.status=report.failures.length?'failed':'passed';
  } catch(error) {report.reason=error.message;}
  finally {if(browser) await browser.close();fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2));}
  return report;
}

module.exports={measurePage,loadFonts,actualFonts,audit};
if(require.main===module) {
  if(process.argv.length!==3){console.error('Usage: node scripts/audit_layout.cjs /absolute/page.html');process.exitCode=2;}
  else audit(process.argv[2]).then(report=>{console.log(JSON.stringify({status:report.status,output:report.output,failures:report.failures.length,reason:report.reason},null,2));process.exitCode=report.status==='passed'?0:report.status==='failed'?1:2;}).catch(error=>{console.error(error.message);process.exitCode=2;});
}
