/* V2 检索：本地离线使用或同源静态托管，无外部字体和运行时依赖。 */
(()=>{'use strict';
const data=window.ARTISAN,$=id=>document.getElementById(id);
if(!data?.assets){$('hero-meta').textContent='索引未加载，请完整解压素材包后重新打开。';return}
const styles=data.styles.filter(s=>s.id!=='shared'),smap=Object.fromEntries(data.styles.map(s=>[s.id,s]));
const byId=new Map(data.assets.map(a=>[a.asset_id,a])),validFamilies=new Set(data.assets.filter(a=>a.counted).map(a=>a.family_id));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const url=s=>'../'+String(s).split('/').map(encodeURIComponent).join('/');
const online=/^https?:$/.test(location.protocol),repository='https://github.com/hanhanhu847-star/artisan-v2';
const absolute=s=>new URL(url(s),location.href).href;
const detailPath=a=>online&&(window.ARTISAN_WEB_PREVIEWS||{})[a.file_path]||a.file_path;
$('copy-link').hidden=!online;
const dots=s=>'<span class="dots" aria-label="'+esc(s.palette.join('、'))+'">'+s.palette.map(c=>'<i style="background:'+c+'"></i>').join('')+'</span>';
const bytes=n=>n<1024?n+' B':n<1048576?(n/1024).toFixed(1)+' KB':(n/1048576).toFixed(1)+' MB';
const dark=s=>{const c=s.palette[0];return [1,3,5].reduce((v,j)=>v+parseInt(c.slice(j,j+2),16),0)<320};
let favorites=new Set(),saved=true;
try{const raw=JSON.parse(localStorage.getItem('ARTISAN_V2_FAVORITES')||'[]');if(Array.isArray(raw))favorites=new Set(raw.filter(x=>validFamilies.has(x)))}catch{saved=false}
let group='全部',page=0,results=[],picked=null,scale=1,timer,matchedFiles=0;const per=40,selected=new Set();
function notice(m){$('notice').textContent=m;clearTimeout(timer);timer=setTimeout(()=>{$('notice').textContent=''},3500)}
function option(sel,v,t){const o=document.createElement('option');o.value=v;o.textContent=t;sel.append(o)}
function populate(id,list,all=true){const sel=$(id);sel.replaceChildren();if(all)option(sel,'','全部');for(const [v,t]of list)option(sel,v,t)}
function fav(a){return favorites.has(a.family_id)}
function toggleFavorite(a){
 if(fav(a))favorites.delete(a.family_id);else favorites.add(a.family_id);
 try{localStorage.setItem('ARTISAN_V2_FAVORITES',JSON.stringify([...favorites]));saved=true}catch{saved=false}
 if(!saved)notice('浏览器未允许本地保存，收藏仅在本次打开期间保留。');
 filter(false);if(picked)updateDetailFavorite();
}
function updateDetailFavorite(){$('detail-favorite').textContent=fav(picked)?'已收藏此作品':'收藏此作品';$('detail-favorite').setAttribute('aria-pressed',String(fav(picked)))}
$('hero-meta').textContent=styles.length+' 种艺术风格 / '+data.work_count.toLocaleString('zh-CN')+' 个独立作品家族 / '+data.assets.length.toLocaleString('zh-CN')+' 个源文件（含变体与公用素材）';
function renderStyles(){
 $('groups').replaceChildren();
 for(const t of ['全部',...new Set(styles.map(s=>s.group))]){const b=document.createElement('button');b.textContent=t;b.setAttribute('aria-pressed',String(group===t));b.onclick=()=>{group=t;renderStyles()};$('groups').append(b)}
 $('style-grid').innerHTML=styles.filter(s=>group==='全部'||s.group===group).map(s=>'<button class="style-card" data-pick="'+s.id+'"><span class="style-art" style="display:block"><img loading="lazy" src="'+url(s.cover)+'" alt="'+esc(s.title)+'"></span><span class="card-head"><strong>'+esc(s.zh)+'</strong><span class="serial">'+String(s.no).padStart(2,'0')+'</span></span><small>'+esc(s.en)+'</small><span class="style-tail"><span>'+s.work_count+' 个作品 / '+s.count+' 个文件</span>'+dots(s)+'</span></button>').join('');
 $('style-grid').querySelectorAll('[data-pick]').forEach(b=>b.onclick=()=>{clear(false);$('f-style').value=b.dataset.pick;facets();filter();location.hash='assets'});
}
populate('f-style',data.styles.map(s=>[s.id,s.zh]));
populate('f-format',[...new Set(data.assets.map(a=>a.file_format))].sort().map(x=>[x,x.toUpperCase()]));
populate('f-license',[['CC-BY-4.0','CC BY 4.0（须署名）'],['CC0-1.0','CC0'],['CC-BY-SA-4.0','CC BY-SA 4.0（须署名）']]);
populate('f-size',[['4k','长边 ≥ 3840 px'],['2k','双边 ≥ 2048 px'],['hd','1920 × 1080'],['qhd','2560 × 1440'],['uhd','3840 × 2160'],['portrait','竖向'],['square','正方形'],['wide','宽高比 ≥ 2']]);
populate('f-alpha',[['yes','含透明区'],['no','不透明']]);
function facets(){
 const st=$('f-style').value,series=$('f-series').value,cat=$('f-cat').value;
 const scope=data.assets.filter(a=>a.counted&&(!st||a.style_id===st)),counts={};
 for(const a of scope)counts[a.category]=(counts[a.category]||0)+1;
 populate('f-cat',Object.entries(data.categories).filter(([k])=>counts[k]).map(([k,v])=>[k,v+' · '+counts[k]+' 个作品']));
 if([...$('f-cat').options].some(o=>o.value===cat))$('f-cat').value=cat;
 populate('f-series',[...new Set(scope.map(a=>a.series))].sort().map(s=>[s,s]));
 if([...$('f-series').options].some(o=>o.value===series))$('f-series').value=series;
}
function updateSelection(){
 $('selection-count').textContent='已选 '+selected.size+' 个文件';
 $('clear-selection').disabled=$('export-selected').disabled=!selected.size;
 $('select-page').disabled=!results.length;
}
function renderResults(){
 const pages=Math.max(1,Math.ceil(results.length/per));page=Math.max(0,Math.min(page,pages-1));
 $('result').textContent=$('f-view').value==='files'?results.length+' 个文件 / '+new Set(results.map(a=>a.family_id)).size+' 个家族（含保留项）':results.length+' 个匹配作品 / '+matchedFiles+' 个可用版本';
 $('page-no').textContent=(page+1)+' / '+pages;$('prev').disabled=!page;$('next').disabled=page===pages-1;$('export-results').disabled=!results.length;
 $('asset-grid').innerHTML=results.length?results.slice(page*per,(page+1)*per).map(a=>'<article class="asset-entry"><button class="asset-card" data-id="'+esc(a.asset_id)+'"><span class="media '+(a.transparency?(dark(smap[a.style_id])?'alpha dark-alpha':'alpha'):'')+'"><img loading="lazy" decoding="async" src="'+url(a.preview_path)+'" alt=""></span><span class="meta"><b>'+esc(a.asset_name)+'</b><small>'+esc(smap[a.style_id].zh)+' · '+a.file_format.toUpperCase()+' · '+a.width+' × '+a.height+'</small><small>'+esc(a.series)+' / '+a.revision+(a.credit==='retained'?' 保留原件':'')+'</small></span></button><div class="asset-actions"><label><input type="checkbox" data-select="'+esc(a.asset_id)+'" '+(selected.has(a.asset_id)?'checked':'')+' aria-label="选择 '+esc(a.asset_name)+'">选择</label><button data-fav="'+esc(a.asset_id)+'" aria-pressed="'+fav(a)+'">'+(fav(a)?'★ 已收藏':'☆ 收藏')+'</button></div></article>').join(''):'<div class="empty">没有匹配素材。请清除一个筛选条件，或换个关键词。</div>';
 $('asset-grid').querySelectorAll('[data-id]').forEach(b=>b.onclick=()=>show(byId.get(b.dataset.id)));
 $('asset-grid').querySelectorAll('[data-fav]').forEach(b=>b.onclick=()=>toggleFavorite(byId.get(b.dataset.fav)));
 $('asset-grid').querySelectorAll('[data-select]').forEach(b=>b.onchange=()=>{if(b.checked)selected.add(b.dataset.select);else selected.delete(b.dataset.select);updateSelection()});
 updateSelection();
}
function filter(reset=true){
 if(reset)page=0;
 const st=$('f-style').value,cat=$('f-cat').value,fo=$('f-format').value,li=$('f-license').value,sz=$('f-size').value,se=$('f-series').value,al=$('f-alpha').value;
 const onlyFav=$('f-favorite').value==='yes',fileMode=$('f-view').value==='files',words=$('query').value.trim().toLowerCase().split(/\s+/).filter(Boolean);
 let matches=data.assets.filter(a=>{
  if(st&&st!==a.style_id||cat&&cat!==a.category||fo&&fo!==a.file_format||li&&li!==a.license||se&&se!==a.series)return false;
  if(al==='yes'&&!a.transparency||al==='no'&&a.transparency||onlyFav&&!fav(a))return false;
  if(!fileMode&&!validFamilies.has(a.family_id))return false;
  const w=a.width,h=a.height;
  if(sz&&!({'4k':Math.max(w,h)>=3840,'2k':Math.min(w,h)>=2048,hd:w===1920&&h===1080,qhd:w===2560&&h===1440,uhd:w===3840&&h===2160,portrait:h>w,square:h===w,wide:w/h>=2}[sz]))return false;
  const hay=[a.asset_id,a.asset_name,smap[a.style_id].zh,smap[a.style_id].en,a.file_path,a.intended_usage,a.author,a.license,a.series,data.categories[a.category]].join(' ').toLowerCase();
  return words.every(word=>hay.includes(word));
 });
 matchedFiles=matches.length;
 if(!fileMode){matches.sort((a,b)=>Number(b.counted)-Number(a.counted));const found=new Set();matches=matches.filter(a=>{if(found.has(a.family_id))return false;found.add(a.family_id);return true})}
 results=matches;renderResults();
}
function clear(repaint=true){
 for(const id of ['query','f-style','f-cat','f-format','f-license','f-size','f-alpha','f-series','f-favorite'])$(id).value='';
 $('f-view').value='family';facets();if(repaint)filter();
}
$('f-style').onchange=()=>{facets();filter()};
for(const id of ['f-cat','f-format','f-license','f-size','f-alpha','f-series','f-favorite','f-view'])$(id).onchange=()=>filter();
$('query').oninput=()=>filter();$('reset').onclick=()=>clear();
$('prev').onclick=()=>{page--;renderResults();$('result').scrollIntoView({block:'start'})};
$('next').onclick=()=>{page++;renderResults();$('result').scrollIntoView({block:'start'})};
function exportRows(rows,name){
 const a=document.createElement('a'),manifest={library:data.library,version:data.version,file_count:rows.length,family_count:new Set(rows.map(r=>r.family_id)).size,paths_relative_to:'ARTISAN_V2 root',assets:rows};
 if(online){manifest.base_url=new URL('../',location.href).href;manifest.assets=rows.map(r=>({...r,download_url:absolute(r.file_path),preview_url:absolute(detailPath(r)),license_url:absolute(r.license_file)}))}
 const object=URL.createObjectURL(new Blob([JSON.stringify(manifest,null,2)],{type:'application/json'}));a.download=name+'.json';a.href=object;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(object),2000);notice('清单已导出，包含路径、校验值和许可信息');
}
$('export-results').onclick=()=>exportRows(results,'ARTISAN_V2-filtered');
$('export-style').onclick=()=>{const st=$('f-style').value;exportRows(data.assets.filter(a=>!st||st===a.style_id),'ARTISAN_V2-'+(st||'all'))};
$('select-page').onclick=()=>{for(const a of results.slice(page*per,(page+1)*per))selected.add(a.asset_id);renderResults()};
$('clear-selection').onclick=()=>{selected.clear();renderResults()};
$('export-selected').onclick=()=>exportRows([...selected].map(id=>byId.get(id)),'ARTISAN_V2-selected');
function zoom(v){scale=Math.min(4,Math.max(.5,v));$('large').style.width=scale*100+'%';$('large').style.height=scale*100+'%';$('zoom').textContent=Math.round(scale*100)+'%';$('zoom-out').disabled=scale<=.5;$('zoom-in').disabled=scale>=4}
function sourceHTML(v){
 return String(v).split(/\s*;\s*/).map(s=>s.startsWith('https://')?'<a target="_blank" rel="noreferrer" href="'+esc(s)+'">'+esc(s)+'</a>':esc(s)).join('<br>');
}
function show(a){
 picked=a;zoom(1);$('stage').scrollTo(0,0);$('detail-style').textContent=smap[a.style_id].zh+' / '+data.categories[a.category]+' / '+a.series;$('detail-name').textContent=a.asset_name;
 $('large').src=url(detailPath(a));$('large').alt=a.asset_name;
 $('preview-note').hidden=detailPath(a)===a.file_path;$('preview-note').textContent='当前显示轻量预览；打开原件可查看完整分辨率（'+bytes(a.file_bytes)+'）。';
 const facts=[['规格',a.width+' × '+a.height+' · '+a.file_format.toUpperCase()],['文件大小',bytes(a.file_bytes)],['版本',a.revision+' / '+({'existing':'原有独立作品','retained':'保留原件，不额外计数','upgrade':'同家族升级','new':'新增作品','variant':'同作品的格式或尺寸版本'}[a.credit]||a.credit)],['特性',[a.color_mode,a.transparency?'含透明区':'不透明',a.tiling?'可平铺':'单幅'].join(' / ')],['用途',a.intended_usage],['许可',a.license],['作者',a.author],['署名',a.attribution],['来源',a.source],['改动',a.modification_status],['作品家族',a.family_id],['计数说明',a.count_note]];
 $('facts').innerHTML=facts.map(([k,v])=>'<dt>'+k+'</dt><dd>'+(k==='来源'?sourceHTML(v):esc(v))+'</dd>').join('')+'<dt>许可全文</dt><dd><a target="_blank" href="'+url(a.license_file)+'">打开随包许可文本 ↗</a></dd>';
 $('path').value=a.file_path;$('original').href=url(a.file_path);$('original').textContent='打开原件 / 另存为 ↗';$('directory').href=url(a.file_path.slice(0,a.file_path.lastIndexOf('/')+1));
 if(online){$('directory').href=repository+'/tree/main/'+a.file_path.slice(0,a.file_path.lastIndexOf('/')).split('/').map(encodeURIComponent).join('/');$('directory').textContent='GitHub 所在目录 ↗'}
 $('copy-link').textContent='复制素材链接';
 updateDetailFavorite();$('detail').showModal();$('close').focus();
}
$('detail-favorite').onclick=()=>{if(picked)toggleFavorite(picked)};
$('close').onclick=()=>$('detail').close();$('detail').addEventListener('close',()=>{$('large').removeAttribute('src');$('copy').textContent='复制相对路径'});
$('zoom-in').onclick=()=>zoom(scale+.5);$('zoom-out').onclick=()=>zoom(scale-.5);
document.querySelectorAll('[data-bg]').forEach(b=>b.onclick=()=>{$('stage').className='stage '+b.dataset.bg;document.querySelectorAll('[data-bg]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))});
$('copy').onclick=async()=>{if(!picked)return;let ok=false;try{await navigator.clipboard.writeText(picked.file_path);ok=true}catch{try{$('path').select();ok=document.execCommand('copy')}catch{}}$('copy').textContent=ok?'已复制相对路径':'已选路径，请手动复制';if(!ok)$('path').focus()};
$('copy-link').onclick=async()=>{if(!picked)return;const link=absolute(picked.file_path);let ok=false;try{await navigator.clipboard.writeText(link);ok=true}catch{const input=document.createElement('textarea');input.value=link;$('detail').append(input);input.select();try{ok=document.execCommand('copy')}catch{}input.remove()}$('copy-link').textContent=ok?'已复制素材链接':'复制失败';if(!ok)notice('请打开原件，从地址栏复制素材链接。')};
function compareBox(id,n){
 const s=smap[id],opts=styles.map(t=>'<option value="'+t.id+'"'+(t.id===id?' selected':'')+'>'+esc(t.zh)+'</option>').join('');
 return '<article class="compare-card"><label>对照 '+n+'<select aria-label="对照 '+n+'">'+opts+'</select></label><img src="'+url(s.cover)+'" alt="'+esc(s.title)+'"><h2>'+esc(s.zh)+'</h2>'+dots(s)+'<p>'+esc(s.form)+'</p><div class="samples">'+[['textures/v2-paper.webp','原生2K纸纤'],['icons/v2-search.svg','V2 搜索图标'],['illustrations/v2-scene-1.svg','新增主题插画']].map(([p,t])=>'<figure><img src="'+url('STYLES/'+id+'/'+p)+'" alt="'+t+'"><figcaption>'+t+'</figcaption></figure>').join('')+'</div><p><b>适用：</b>'+esc(s.use)+'</p><a href="'+url('STYLES/'+id+'/STYLE_GUIDE.md')+'" target="_blank">风格规范 ↗</a></article>';
}
let comp=['bauhaus','dunhuang'];
function compare(){const r=$('comparisons');r.innerHTML=comp.map((s,i)=>compareBox(s,i+1)).join('');r.querySelectorAll('select').forEach((sel,i)=>sel.onchange=()=>{comp[i]=sel.value;compare();r.querySelectorAll('select')[i].focus()})}
$('matrix').innerHTML=styles.map(s=>'<tr><td>'+String(s.no).padStart(2,'0')+'　'+esc(s.zh)+'</td><td>'+esc(s.title)+'</td><td>'+esc(s.use)+'</td><td>'+dots(s)+'</td></tr>').join('');
function route(){const view=['styles','assets','compare'].includes(location.hash.slice(1))?location.hash.slice(1):'styles';for(const id of ['styles','assets','compare'])$(id).hidden=id!==view;document.querySelectorAll('header nav a').forEach(a=>{if(a.hash==='#'+view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});window.scrollTo(0,0)}
facets();renderStyles();filter();compare();route();addEventListener('hashchange',route);
})();
