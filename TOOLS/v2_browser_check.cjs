/* 真实 Chromium、断网 file:// 验收：检索/收藏/导出/复制原件路径/移动端。 */
const {chromium}=require('playwright'),fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),assert=require('assert/strict'),crypto=require('crypto');
const root=process.env.ARTISAN_TEST_ROOT?path.resolve(process.env.ARTISAN_TEST_ROOT):path.resolve(__dirname,'..');
const qa=process.env.ARTISAN_TEST_QA?path.resolve(process.env.ARTISAN_TEST_QA):path.resolve(root,'..','ARTISAN-V2-QA');fs.mkdirSync(qa,{recursive:true});
const idx=JSON.parse(fs.readFileSync(path.join(root,'ASSET_INDEX.json'),'utf8'));
const hash=f=>crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.ARTISAN_CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const ctx=await browser.newContext({offline:true,acceptDownloads:true,viewport:{width:1440,height:1000}});
 const page=await ctx.newPage(),errors=[],external=[],missing=[],checks=[];
 page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url())});
 page.on('requestfailed',r=>missing.push({url:r.url(),error:r.failure()}));
 async function download(button){const p=page.waitForEvent('download');await page.locator(button).click();const d=await p;assert.equal(await d.failure(),null);return await d.path()}
 try{
  await page.goto(pathToFileURL(path.join(root,'BROWSER/index.html')).href);await page.locator('.style-card').first().waitFor();
  assert.equal(await page.locator('.style-card').count(),16);
  assert.match(await page.locator('#hero-meta').innerText(),new RegExp(idx.work_count.toLocaleString('zh-CN')));
  await page.screenshot({path:path.join(qa,'browser-v2-home.png')});
  await page.locator('[data-pick="dunhuang"]').click();assert.match(await page.locator('#result').innerText(),/^112 个匹配作品/);
  await page.locator('#f-cat').selectOption('icons');await page.locator('#query').fill('搜索');assert.equal(await page.locator('.asset-card').count(),1);
  await page.locator('[data-fav]').click();assert.equal(await page.locator('[data-fav]').getAttribute('aria-pressed'),'true');
  await page.reload();await page.locator('#f-favorite').selectOption('yes');assert.equal(await page.locator('.asset-card').count(),1);
  await page.locator('.asset-card').click();await page.locator('#detail[open]').waitFor();
  assert.equal(await page.locator('#path').inputValue(),'STYLES/dunhuang/icons/v2-search.svg');
  await page.locator('#large').evaluate(i=>i.decode());assert.equal(await page.locator('#large').evaluate(i=>i.naturalWidth),64);
  await page.locator('[data-bg="dark"]').click();await page.locator('#zoom-in').click();assert.equal(await page.locator('#zoom').innerText(),'150%');
  await ctx.grantPermissions(['clipboard-read','clipboard-write']);await page.locator('#copy').click();await page.waitForFunction(()=>document.getElementById('copy').textContent!=='复制相对路径');assert.equal(await page.locator('#copy').innerText(),'已复制相对路径');
  const pop=ctx.waitForEvent('page');await page.locator('#original').click();const raw=await pop;await raw.waitForLoadState();assert(raw.url().endsWith('/STYLES/dunhuang/icons/v2-search.svg'));await raw.close();
  await page.keyboard.press('Escape');checks.push('实际离线打开；按作品计数；关键词搜索；收藏跨刷新保留；原始大图、深底、缩放；复制路径成功与新页打开实际原件');
  await page.locator('#reset').click();await page.locator('#f-style').selectOption('dunhuang');await page.locator('#f-cat').selectOption('textures');await page.locator('#f-alpha').selectOption('yes');
  assert.equal(await page.locator('.asset-card').count(),4);
  await page.locator('#select-page').click();assert.equal(await page.locator('#selection-count').innerText(),'已选 4 个文件');
  const batch=JSON.parse(fs.readFileSync(await download('#export-selected'),'utf8'));assert.equal(batch.file_count,4);assert.equal(batch.family_count,4);
  for(const a of batch.assets){assert.equal(a.width,2048);assert(a.transparency);assert.equal(hash(path.join(root,a.file_path)),a.sha256);assert(a.license&&a.author&&a.source)}
  await page.locator('#clear-selection').click();assert(await page.locator('#export-selected').isDisabled());
  checks.push('透明叠层筛选；全选本页；批选清单实际包含4项原件路径、许可、校验值；清空选择');
  await page.locator('#reset').click();await page.locator('#f-style').selectOption('celestial-atlas');await page.locator('#f-series').selectOption('古典星图');await page.locator('#f-license').selectOption('CC-BY-SA-4.0');
  assert.equal(await page.locator('.asset-card').count(),12);await page.locator('.asset-card').first().click();
  assert.match(await page.locator('#facts').innerText(),/David Nash/);assert.match(await page.locator('#facts').innerText(),/CC-BY-SA-4.0/);assert.equal(await page.locator('#facts a[href^="https"]').count(),2);
  await page.screenshot({path:path.join(qa,'browser-v2-zodiac.png')});await page.keyboard.press('Escape');
  checks.push('子系列、星图共享许可、12项真实数据图版及双来源链接');
  await page.locator('#reset').click();await page.locator('#f-style').selectOption('bauhaus');await page.locator('#f-cat').selectOption('backgrounds');await page.locator('#f-format').selectOption('jpg');await page.locator('#f-size').selectOption('portrait');
  assert.equal(await page.locator('.asset-card').count(),2);await page.locator('.asset-card').first().click();
  assert.match(await page.locator('#path').inputValue(),/v2-plate-0[45]\.jpg/);await page.keyboard.press('Escape');
  await page.locator('#f-view').selectOption('files');await page.locator('#reset').click();await page.locator('#f-style').selectOption('bauhaus');await page.locator('#f-view').selectOption('files');
  const styleFiles=idx.assets.filter(a=>a.style_id==='bauhaus').length;
  assert.match(await page.locator('#result').innerText(),new RegExp('^'+styleFiles+' 个文件'));
  const all=JSON.parse(fs.readFileSync(await download('#export-style'),'utf8'));assert.equal(all.file_count,styleFiles);
  checks.push('尺寸与格式组合能选择同作品JPG版本；全部文件模式含V1原件；整套导出'+styleFiles+'文件');
  await page.locator('#query').fill('不存在的素材_xyz');assert.equal(await page.locator('.empty').count(),1);
  await page.getByRole('link',{name:'风格对照',exact:true}).click();await page.locator('#comparisons select').first().selectOption('cyberpunk');
  assert.equal(await page.locator('.compare-card h2').first().innerText(),'赛博朋克');
  await page.locator('#comparisons img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
  assert.equal(await page.locator('#matrix tr').count(),16);
  await page.getByRole('link',{name:'素材检索',exact:true}).click();await page.locator('#reset').click();await page.locator('#f-style').selectOption('dunhuang');await page.locator('#f-cat').selectOption('icons');
  await page.locator('.asset-grid img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
  assert(await page.locator('.asset-grid img').evaluateAll(imgs=>imgs.length>0&&imgs.every(i=>i.naturalWidth>0&&i.getBoundingClientRect().height>0)));
  await page.screenshot({path:path.join(qa,'browser-v2-assets.png')});
  await page.setViewportSize({width:390,height:844});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(qa,'browser-v2-mobile.png')});
  await page.locator('.asset-card').first().scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(qa,'browser-v2-mobile-assets.png')});
  await page.locator('#reset').click();await page.locator('#next').click();assert.match(await page.locator('#page-no').innerText(),/^2 \//);
  checks.push('空结果、风格对照、全部16套比较表、移动端无横向溢出、分页');
  await page.goto(pathToFileURL(path.join(root,'PREVIEWS/CONTACT_SHEETS.html')).href);assert.equal(await page.locator('details').count(),16);
  await page.locator('#dunhuang summary').click();await page.locator('#dunhuang img').first().evaluate(i=>i.decode());
  await page.goto(pathToFileURL(path.join(root,'ADAPTERS/web/index.html')).href);await page.locator('#style').selectOption('art-deco');await page.locator('#form button').click();assert.equal(await page.locator('#name').getAttribute('aria-invalid'),'true');
  await page.locator('#name').fill('窗饰研究');await page.locator('#form button').click();assert.equal(await page.locator('#list li').innerText(),'窗饰研究');
  checks.push('完整联系表本地链接；保留的Web接入示例实际验证与添加');
  assert.deepEqual(errors,[]);assert.deepEqual(external,[]);
  // Chromium取消懒加载请求可产生ERR_ABORTED；其他本地资源失败属于失败。
  assert.deepEqual(missing.filter(r=>!r.error?.errorText?.includes('ERR_ABORTED')),[]);
  const report={engine:await browser.version(),network:'offline',protocol:'file:',checks,pageErrors:errors,externalRequests:external,localResourceErrors:missing.filter(r=>!r.error?.errorText?.includes('ERR_ABORTED'))};
  fs.writeFileSync(process.env.ARTISAN_TEST_REPORT||path.join(root,'AUDIT/browser-v2-check.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
