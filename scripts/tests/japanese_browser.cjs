const {chromium}=require('playwright');
const fs=require('fs');
const assert=require('node:assert/strict');
const base=process.argv[2] || 'http://127.0.0.1:1313';
const output=process.argv[3] || '/tmp/machbase-ja-browser';
fs.mkdirSync(output,{recursive:true});
const results={checks:[],errors:[],screenshots:[]};
(async()=>{
 const browser=await chromium.launch({headless:true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? {executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH} : {}),args:['--no-sandbox']});
 try {
  const context=await browser.newContext({viewport:{width:1440,height:900},permissions:['clipboard-read','clipboard-write']});
  const page=await context.newPage();
  const collectErrors=p=>{
   p.on('pageerror',e=>results.errors.push(String(e)));
   p.on('console',m=>{if(m.type()==='warning' && m.text().includes('Unable to load search index')) results.errors.push(m.text())});
  };
  collectErrors(page);
  const check=(name)=>{results.checks.push(name);console.log('PASS',name)};
  const screenshot=async(p,name)=>{const path=output+'/'+name+'.png';await p.screenshot({path,scale:'css'});results.screenshots.push(path)};
  await page.goto(base+'/ja/',{waitUntil:'networkidle'});
  assert.equal(new URL(page.url()).pathname,'/ja/neo/');
  assert.match(await page.locator('h1').innerText(),/machbase[- ]neo/i);
  for(const product of ['neo','dbms','dbms-8.5','apps']) {
   assert.ok(await page.locator('nav').first().locator(`a[href^="/ja/${product}"]`).count()>0,product);
  }
  check('Japanese Neo landing and all-product navigation');
  await screenshot(page,'desktop-home');
  await page.goto(base+'/ja/dbms/getting-started/quick-start/',{waitUntil:'networkidle'});
  const originalPath=new URL(page.url()).pathname;
  for(const [label,path] of [['English','/dbms/getting-started/quick-start/'],['한국어','/kr/dbms/getting-started/quick-start/'],['日本語',originalPath]]){
   await page.locator('.hextra-language-switcher:visible').first().click();
   await page.locator('.hextra-language-options:visible').getByRole('menuitem',{name:label,exact:true}).click();
   await page.waitForURL(u=>u.pathname===path);
  }
  check('Same-page JA -> EN -> KR -> JA language cycle');
  await screenshot(page,'desktop-article');
  const copy=page.getByRole('button',{name:'コードをコピー',exact:true}).first();
  await page.locator('pre').first().hover();
  await copy.click();
  assert.match(await page.evaluate(()=>navigator.clipboard.readText()),/CREATE LOG TABLE DBMS_GS_QUICK/);
  check('Japanese code-copy control and clipboard');
  await page.locator('.hextra-theme-toggle:visible').first().click();
  await page.locator('.hextra-theme-toggle-options:visible [data-item="dark"]').click();
  assert.ok(await page.locator('html').evaluate(e=>e.classList.contains('dark')));
  await screenshot(page,'desktop-dark');
  await page.locator('.hextra-theme-toggle:visible').first().click();
  await page.locator('.hextra-theme-toggle-options:visible [data-item="light"]').click();
  assert.ok(!await page.locator('html').evaluate(e=>e.classList.contains('dark')));
  check('Dark and light theme cycle');
  // Delay the initial index response to exercise typing before loading finishes.
  await page.route('**/ja.search-data*.json', async route => {
   await new Promise(resolve=>setTimeout(resolve,600)); await route.continue();
  });
  for(const query of ['接続','テーブル','時系列','ROLLUP']){
   const input=page.locator('.hextra-search-input:visible').first();await input.click();
   if(query==='接続') {
    await page.evaluate(text=>navigator.clipboard.writeText(text),query);
    await input.press('Control+V');
   } else await input.fill(query);
   await page.locator('.hextra-search-results:visible a').first().waitFor({timeout:20000});
   const links=await page.locator('.hextra-search-results:visible a').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
   assert.ok(links.length>0&&links.every(x=>/^\/ja\/(neo|dbms|dbms-8\.5|apps)\//.test(x)),query+': '+links);
   assert.doesNotMatch(await page.locator('.hextra-search-results:visible').innerText(),/<\/?code>/);
   check('Japanese search: '+query);
   if(query==='接続') await screenshot(page,'desktop-search');
   await input.press('Escape');
  }
  // Chromium's IME protocol exercises composition rather than synthetic DOM input events.
  const input=page.locator('.hextra-search-input:visible').first();await input.click();
  const ime=await context.newCDPSession(page);
  await ime.send('Input.imeSetComposition',{text:'せつぞく',selectionStart:4,selectionEnd:4});
  await input.press('Enter');
  assert.equal(await input.inputValue(),'せつぞく');
  await ime.send('Input.insertText',{text:'接続'});
  await page.locator('.hextra-search-results:visible a').first().waitFor();
  assert.equal(await input.inputValue(),'接続');
  check('IME composition Enter preserves text; committed Japanese runs search');
  await input.press('Escape');
  await input.click();await input.fill('zxqvzznomatch98765');
  await page.locator('.hextra-search-no-result:visible').waitFor();
  assert.match(await page.locator('.hextra-search-no-result:visible').innerText(),/結果が見つかりませんでした/);
  await input.press('Escape');assert.equal(await input.inputValue(),'');
  check('Japanese no-results and Escape reset');
  for(const action of ['replace','escape','blur']) {
   const rp=await context.newPage();collectErrors(rp);
   await rp.goto(base+originalPath,{waitUntil:'networkidle'});
   let release,started;
   const gate=new Promise(resolve=>release=resolve);
   const requested=new Promise(resolve=>started=resolve);
   await rp.route('**/ja.search-data*.json',async route=>{started();await gate;await route.continue()});
   const ri=rp.locator('.hextra-search-input:visible').first();
   await ri.click();await ri.fill('接続');await requested;
   if(action==='replace') await ri.fill('ROLLUP');
   else if(action==='escape') await ri.press('Escape');
   else await rp.locator('h1').click();
   const response=rp.waitForResponse(r=>r.url().includes('ja.search-data'));
   release();await (await response).finished();
   if(action==='replace') {
    await rp.locator('.hextra-search-results:visible a').first().waitFor();
    assert.equal(await ri.inputValue(),'ROLLUP');
    assert.match(await rp.locator('.hextra-search-results:visible').innerText(),/ROLLUP/);
   } else {
    await rp.waitForTimeout(300);
    assert.equal(await rp.locator('.hextra-search-results:visible').count(),0);
   }
   check('Delayed index loading with '+action);await rp.close();
  }
  await page.goto(base+'/neo/',{waitUntil:'networkidle'});
  await page.locator('.hextra-language-switcher:visible').first().click();
  await page.locator('.hextra-language-options:visible').getByRole('menuitem',{name:'日本語',exact:true}).click();
  await page.waitForURL(u=>u.pathname==='/ja/neo/');check('Neo same-page Japanese language switch');
  await page.goto(base+originalPath,{waitUntil:'networkidle'});
  await page.locator('nav a').first().click();await page.waitForURL(u=>u.pathname==='/ja/neo/');check('Japanese logo target');
  for(const product of ['dbms-8.5','apps']) {
   await page.goto(base+'/'+product+'/',{waitUntil:'networkidle'});
   await page.locator('.hextra-language-switcher:visible').first().click();
   await page.locator('.hextra-language-options:visible').getByRole('menuitem',{name:'日本語',exact:true}).click();
   await page.waitForURL(u=>u.pathname==='/ja/'+product+'/');
   assert.ok(await page.locator('h1').innerText());
   check(product+' same-page Japanese language switch');
  }
  const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  const mp=await mobile.newPage();collectErrors(mp);
  await mp.goto(base+originalPath,{waitUntil:'networkidle'});
  await screenshot(mp,'mobile-article');
  assert.equal(await mp.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
  await mp.getByRole('button',{name:'メニュー',exact:true}).click();
  await mp.locator('.hextra-sidebar-container .hextra-search-input:visible').waitFor();
  await mp.waitForFunction(()=>{
   const el=document.querySelector('.hextra-sidebar-container');
   const rect=el.getBoundingClientRect();
   const transform=getComputedStyle(el).transform;
   return rect.top>=0 && (transform==='none' || Math.abs(new DOMMatrixReadOnly(transform).m42)<0.5);
  });
  await screenshot(mp,'mobile-menu');
  const mi=mp.locator('.hextra-search-input:visible').first();await mi.fill('接続');
  await mp.locator('.hextra-search-results:visible a').first().waitFor();
  await screenshot(mp,'mobile-search');
  const mobileResult=mp.locator('.hextra-search-results:visible a').first();
  const target=new URL(await mobileResult.getAttribute('href'),mp.url());
  assert.match(target.pathname,/^\/ja\/(neo|dbms|dbms-8\.5|apps)\//);
  await mobileResult.click();
  await mp.waitForURL(u=>u.pathname===target.pathname && decodeURIComponent(u.hash)===decodeURIComponent(target.hash));
  check('Mobile menu, Japanese search, result navigation, and viewport fit');
  // Follow a real table-of-contents anchor in the same Japanese article.
  await page.goto(base+originalPath,{waitUntil:'networkidle'});
  const toc=page.locator('nav a[href^="#"]').first();
  await toc.click();assert.ok(new URL(page.url()).hash);
  assert.equal(new URL(page.url()).pathname,originalPath);
  check('Japanese table-of-contents anchor navigation');
  assert.equal(results.errors.length,0,JSON.stringify(results.errors));
  await mobile.close();await context.close();
 } finally {await browser.close();fs.writeFileSync(output+'/report.json',JSON.stringify(results,null,2));}
})().catch(e=>{console.error(e);process.exitCode=1});
