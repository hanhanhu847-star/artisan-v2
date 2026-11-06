/* Real HTTP checks at the GitHub project subpath; optionally test deployed Pages. */
const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),os=require('os'),http=require('http'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..');
const serveRoot=path.resolve(process.env.ARTISAN_PAGES_ROOT||root);
const qa=path.resolve(process.env.ARTISAN_PAGES_QA||path.join(os.tmpdir(),'artisan-pages-qa'));
fs.mkdirSync(qa,{recursive:true});
const index=JSON.parse(fs.readFileSync(path.join(root,'ASSET_INDEX.json'),'utf8'));
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json','.svg':'image/svg+xml','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png','.txt':'text/plain; charset=utf-8','.md':'text/plain; charset=utf-8'};

(async()=>{
 let server,browser;
 const checks=[],pageErrors=[],httpErrors=[],requestErrors=[],requests=[];
 try{
  let base=process.env.ARTISAN_PAGES_URL;
  if(!base){
   server=http.createServer((req,res)=>{
    try{
     const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
     if(!pathname.startsWith('/artisan-v2/')){res.writeHead(404).end();return}
     let file=path.resolve(serveRoot,pathname.slice('/artisan-v2/'.length)||'index.html');
     if(!file.startsWith(serveRoot+path.sep)){res.writeHead(403).end();return}
     if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');
     res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');
     fs.createReadStream(file).on('error',()=>res.destroy()).pipe(res);
    }catch{res.writeHead(404).end()}
   });
   await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
   base='http://127.0.0.1:'+server.address().port+'/artisan-v2/';
  }
  base=base.replace(/\/?$/,'/');
  browser=await chromium.launch({executablePath:process.env.ARTISAN_CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true,...(process.env.ARTISAN_TEST_PROXY?{proxy:{server:process.env.ARTISAN_TEST_PROXY,bypass:'127.0.0.1,localhost'}}:{})});
  const context=await browser.newContext({acceptDownloads:true,viewport:{width:1440,height:1000}});
  const page=await context.newPage();page.setDefaultTimeout(45000);
  page.on('pageerror',e=>pageErrors.push(String(e)));
  page.on('request',r=>requests.push(r.url()));
  page.on('response',r=>{if(r.status()>=400)httpErrors.push({url:r.url(),status:r.status()})});
  page.on('requestfailed',r=>{if(!r.failure()?.errorText.includes('ERR_ABORTED'))requestErrors.push({url:r.url(),error:r.failure()})});
  async function download(selector){const event=page.waitForEvent('download');await page.locator(selector).click();const d=await event;assert.equal(await d.failure(),null);return JSON.parse(fs.readFileSync(await d.path(),'utf8'))}
  await page.goto(base+'?check=pages#assets');
  await page.locator('#assets:not([hidden])').waitFor();
  const assetBase=await page.evaluate(()=>window.ARTISAN_ASSET_BASE||new URL('../',location.href).href);
  assert.equal(new URL(page.url()).search,'?check=pages');assert.equal(new URL(page.url()).hash,'#assets');
  assert(page.url().startsWith(base+'BROWSER/'));
  await page.getByRole('link',{name:'风格目录',exact:true}).click();
  assert.equal(await page.locator('.style-card').count(),16);
  assert.match(await page.locator('#hero-meta').innerText(),/1,804/);
  await page.locator('.style-art img').evaluateAll(imgs=>Promise.all(imgs.map(i=>{i.loading='eager';return i.decode()})));
  await page.locator('.poster img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
  await page.screenshot({path:path.join(qa,'pages-home.png')});
  checks.push('Project-subpath entry, preserved query/hash, 16 styles and real cover images');

  await page.locator('[data-pick="dunhuang"]').click();
  await page.locator('#f-cat').selectOption('icons');await page.locator('#query').fill('搜索');
  assert.equal(await page.locator('.asset-card').count(),1);
  await page.locator('[data-fav]').click();await page.reload();
  await page.locator('#f-favorite').selectOption('yes');assert.equal(await page.locator('.asset-card').count(),1);
  await page.locator('.asset-card').click();await page.locator('#large').evaluate(i=>i.decode());
  assert.equal(await page.locator('#large').evaluate(i=>i.naturalWidth),64);
  const original=assetBase+'STYLES/dunhuang/icons/v2-search.svg';
  assert.equal(await page.locator('#original').evaluate(a=>a.href),original);
  assert.equal(await page.locator('#directory').getAttribute('href'),'https://github.com/hanhanhu847-star/artisan-v2/tree/main/STYLES/dunhuang/icons');
  await context.grantPermissions(['clipboard-read','clipboard-write']);
  await page.locator('#copy-link').click();await page.waitForFunction(()=>document.getElementById('copy-link').textContent==='已复制素材链接');
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),original);
  await page.locator('#copy').click();assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'STYLES/dunhuang/icons/v2-search.svg');
  const source=await page.evaluate(async link=>{const r=await fetch(link);const b=await r.arrayBuffer();return {status:r.status,sha256:[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(n=>n.toString(16).padStart(2,'0')).join('')}},original);
  assert.equal(source.status,200);assert.equal(source.sha256,index.assets.find(a=>a.file_path==='STYLES/dunhuang/icons/v2-search.svg').sha256);
  await page.keyboard.press('Escape');await page.locator('#select-page').click();
  const manifest=await download('#export-selected');assert.equal(manifest.file_count,1);assert.equal(manifest.base_url,assetBase);
  assert.equal(manifest.assets[0].download_url,original);assert.equal(manifest.assets[0].preview_url,original);
  assert(manifest.assets[0].license_url.startsWith(assetBase+'LICENSES/'));
  assert(manifest.assets[0].author.includes('hanhanhu847-star'));assert.equal(manifest.assets[0].license,'CC-BY-4.0');
  checks.push('Search, persistent favorite, original SVG SHA-256, both clipboard actions, GitHub directory and exported download/license URLs');

  const large=index.assets.filter(a=>a.file_format==='jpg').sort((a,b)=>b.file_bytes-a.file_bytes)[0];
  await page.locator('#reset').click();await page.locator('#f-view').selectOption('files');await page.locator('#query').fill(large.file_path);
  assert.equal(await page.locator('.asset-card').count(),1);await page.locator('.asset-card').click();
  await page.locator('#large').evaluate(i=>i.decode());
  assert((await page.locator('#large').getAttribute('src')).startsWith(assetBase+'PREVIEWS/web-detail/'));
  assert(await page.locator('#large').evaluate(i=>Math.max(i.naturalWidth,i.naturalHeight)<=1600));
  assert(await page.locator('#preview-note').isVisible());
  assert(!requests.includes(assetBase+large.file_path));
  assert.equal(await page.locator('#original').evaluate(a=>a.href),assetBase+large.file_path);
  await page.screenshot({path:path.join(qa,'pages-photo.png')});await page.keyboard.press('Escape');
  checks.push('Large photograph uses a decoded lightweight preview without fetching its multi-MB original');

  await page.locator('#reset').click();await page.locator('#f-style').selectOption('celestial-atlas');await page.locator('#f-license').selectOption('CC-BY-SA-4.0');
  assert.equal(await page.locator('.asset-card').count(),12);await page.locator('.asset-card').first().click();
  assert.match(await page.locator('#facts').innerText(),/David Nash/);assert.equal(await page.locator('#facts dt:text-is("来源") + dd a').count(),2);
  await page.locator('#large').evaluate(i=>i.decode());await page.keyboard.press('Escape');
  await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(qa,'pages-mobile.png')});
  await page.locator('.asset-card').first().click();await page.locator('#large').evaluate(i=>i.decode());
  assert(await page.locator('#detail').evaluate(d=>d.scrollWidth<=d.clientWidth+1));
  await page.screenshot({path:path.join(qa,'pages-mobile-detail.png')});await page.keyboard.press('Escape');
  await page.getByRole('link',{name:'风格目录',exact:true}).click();assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  checks.push('CC BY-SA sources, mobile home/list/detail without horizontal overflow');
  await page.goto(base+'PREVIEWS/CONTACT_SHEETS.html');assert.equal(await page.locator('details').count(),16);
  await page.locator('#dunhuang summary').click();await page.locator('#dunhuang img').first().evaluate(i=>i.decode());
  checks.push('Public contact sheet with decoded artwork');
  assert.deepEqual(pageErrors,[]);assert.deepEqual(httpErrors,[]);assert.deepEqual(requestErrors,[]);
  const report={base,assetBase,engine:await browser.version(),checks,pageErrors,httpErrors,requestErrors};
  fs.writeFileSync(path.join(qa,'pages-check.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
 }finally{if(browser)await browser.close();if(server)await new Promise(resolve=>server.close(resolve))}
})().catch(e=>{console.error(e);process.exitCode=1});
