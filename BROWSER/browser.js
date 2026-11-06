/* 静态离线浏览器。所有文件相对寻址，无 fetch、遥测、外部字体或运行时依赖。 */
(()=>{'use strict';
const data=window.ARTISAN,$=id=>document.getElementById(id),styles=data.styles.filter(s=>s.id!=='shared'),smap=Object.fromEntries(data.styles.map(s=>[s.id,s])),byId=Object.fromEntries(data.assets.map(a=>[a.asset_id,a]));
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])),url=s=>'../'+String(s).split('/').map(encodeURIComponent).join('/');
const dots=s=>'<span class="dots" aria-label="'+esc(s.palette.join('、'))+'">'+s.palette.map(c=>'<i style="background:'+esc(c)+'"></i>').join('')+'</span>';
const fmtSize=n=>n<1024?n+' B':n<1048576?(n/1024).toFixed(1)+' KB':(n/1048576).toFixed(1)+' MB';
function option(sel,v,t){const o=document.createElement('option');o.value=v;o.textContent=t;sel.append(o)}
let group='全部',page=0,results=[],picked=null,scale=1,timer;const per=40;
function notice(m){$('notice').textContent=m;clearTimeout(timer);timer=setTimeout(()=>$('notice').textContent='',2300)}
$('hero-meta').textContent=styles.length+' 种艺术风格　/　'+data.assets.length.toLocaleString('zh-CN')+' 项可调用素材　/　离线版';
function renderStyles(){
 $('groups').replaceChildren();
 ['全部',...new Set(styles.map(s=>s.group))].forEach(t=>{const b=document.createElement('button');b.textContent=t;b.setAttribute('aria-pressed',String(group===t));b.onclick=()=>{group=t;renderStyles()};$('groups').append(b)});
 $('style-grid').innerHTML=styles.filter(s=>group==='全部'||s.group===group).map(s=>'<button class="style-card" data-pick="'+esc(s.id)+'"><span class="style-art" style="display:block"><img loading="lazy" src="'+url(s.cover)+'" alt="'+esc(s.title)+'"></span><span class="card-head"><strong>'+esc(s.zh)+'</strong><span class="serial">'+String(s.no).padStart(2,'0')+'</span></span><small>'+esc(s.en)+'</small><span class="style-tail"><span>'+s.count+' 项素材</span>'+dots(s)+'</span></button>').join('');
 $('style-grid').querySelectorAll('[data-pick]').forEach(b=>b.onclick=()=>{clear(false);$('f-style').value=b.dataset.pick;filter();location.hash='assets'});
}
function populate(id,list){const sel=$(id);option(sel,'','全部');list.forEach(([v,t])=>option(sel,v,t))}
populate('f-style',data.styles.map(s=>[s.id,s.zh]));populate('f-cat',Object.entries(data.categories));populate('f-format',[...new Set(data.assets.map(a=>a.file_format))].sort().map(s=>[s,s.toUpperCase()]));populate('f-license',[['CC-BY-4.0','自制开放使用'],['CC0-1.0','CC0']]);
populate('f-size',[['4k','宽 ≥ 3840 px'],['hd','1920 × 1080'],['qhd','2560 × 1440'],['uhd','3840 × 2160'],['portrait','竖向'],['square','正方形'],['wide','宽高比 ≥ 2']]);
function renderResults(){const pages=Math.max(1,Math.ceil(results.length/per));page=Math.max(0,Math.min(page,pages-1));$('result').textContent=results.length+' 项匹配素材';$('page-no').textContent=(page+1)+' / '+pages;$('prev').disabled=page===0;$('next').disabled=page===pages-1;$('export-results').disabled=!results.length;
 const slice=results.slice(page*per,(page+1)*per);
 $('asset-grid').innerHTML=slice.length?slice.map(a=>'<button class="asset-card" data-id="'+esc(a.asset_id)+'"><span class="media '+(a.transparency?'alpha':'')+'"><img loading="lazy" src="'+url(a.preview_path)+'" alt=""></span><span class="meta"><b>'+esc(a.asset_name)+'</b><small>'+esc(smap[a.style_id].zh)+' · '+a.file_format.toUpperCase()+' · '+a.width+' × '+a.height+'</small></span></button>').join(''):'<div class="empty">没有匹配素材。清除一个筛选条件，或换个关键词。</div>';
 $('asset-grid').querySelectorAll('button').forEach(b=>b.onclick=()=>show(byId[b.dataset.id]));}
function filter(){const st=$('f-style').value,cat=$('f-cat').value,fo=$('f-format').value,li=$('f-license').value,sz=$('f-size').value,words=$('query').value.trim().toLowerCase().split(/\s+/).filter(Boolean);page=0;
 results=data.assets.filter(a=>{if(st&&st!==a.style_id||cat&&cat!==a.category||fo&&fo!==a.file_format||li&&li!==a.license)return false;const w=a.width,h=a.height;
 if(sz&&!({ '4k':w>=3840,hd:w===1920&&h===1080,qhd:w===2560&&h===1440,uhd:w===3840&&h===2160,portrait:h>w,square:h===w,wide:w/h>=2}[sz]))return false;
 const hay=[a.asset_id,a.asset_name,smap[a.style_id].zh,smap[a.style_id].en,a.file_path,a.intended_usage,a.author,a.license,data.categories[a.category]].join(' ').toLowerCase();return words.every(x=>hay.includes(x));});renderResults()}
function clear(repaint=true){['query','f-style','f-cat','f-format','f-license','f-size'].forEach(id=>$(id).value='');if(repaint)filter()}
['f-style','f-cat','f-format','f-license','f-size'].forEach(id=>$(id).onchange=filter);$('query').oninput=filter;$('reset').onclick=()=>clear();
$('prev').onclick=()=>{page--;renderResults();$('result').scrollIntoView({block:'start'})};$('next').onclick=()=>{page++;renderResults();$('result').scrollIntoView({block:'start'})};
function exportRows(rows,name){const a=document.createElement('a'),obj=URL.createObjectURL(new Blob([JSON.stringify({library:data.library,version:data.version,count:rows.length,assets:rows},null,2)],{type:'application/json'}));a.download=name+'.json';a.href=obj;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(obj),1000);notice('清单已导出')}
$('export-results').onclick=()=>exportRows(results,'ARTISAN-filtered');$('export-style').onclick=()=>{const s=$('f-style').value;exportRows(data.assets.filter(a=>!s||s===a.style_id),'ARTISAN-'+(s||'all'))};
function zoom(v){scale=Math.min(4,Math.max(.5,v));$('large').style.width=scale*100+'%';$('large').style.height=scale*100+'%';$('zoom').textContent=Math.round(scale*100)+'%';$('zoom-out').disabled=scale<=.5;$('zoom-in').disabled=scale>=4}
function show(a){picked=a;zoom(1);$('stage').scrollTo(0,0);$('detail-style').textContent=smap[a.style_id].zh+' / '+data.categories[a.category];$('detail-name').textContent=a.asset_name;
 $('large').src=url(a.file_path.includes('/photo-')&&!a.file_path.endsWith('photo-window.jpg')?a.preview_path:a.file_path);$('large').alt=a.asset_name;
 const facts=[['规格',a.width+' × '+a.height+' · '+a.file_format.toUpperCase()],['文件大小',fmtSize(a.file_bytes)],['特性',[a.color_mode,a.transparency?'含透明区':'不透明',a.tiling?'可平铺':'单幅'].join(' / ')],['用途',a.intended_usage],['许可',a.license],['作者',a.author],['来源',a.source],['改动',a.modification_status]];
 $('facts').innerHTML=facts.map(([k,v])=>'<dt>'+k+'</dt><dd>'+(k==='来源'&&String(v).startsWith('https://')?'<a target="_blank" rel="noreferrer" href="'+esc(v)+'">'+esc(v)+'</a>':esc(v))+'</dd>').join('');$('path').value=a.file_path;$('original').href=url(a.file_path);$('directory').href=url(a.file_path.slice(0,a.file_path.lastIndexOf('/')+1));$('detail').showModal();$('close').focus()}
$('close').onclick=()=>$('detail').close();$('detail').addEventListener('close',()=>{$('large').removeAttribute('src');$('copy').textContent='复制相对路径'});$('zoom-in').onclick=()=>zoom(scale+.5);$('zoom-out').onclick=()=>zoom(scale-.5);
document.querySelectorAll('[data-bg]').forEach(b=>b.onclick=()=>{$('stage').className='stage '+b.dataset.bg;document.querySelectorAll('[data-bg]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))});
$('copy').onclick=async()=>{if(!picked)return;let ok=false;try{await navigator.clipboard.writeText(picked.file_path);ok=true}catch{try{$('path').select();ok=document.execCommand('copy')}catch{}}$('copy').textContent=ok?'已复制相对路径':'已选路径，请手动复制';if(!ok)$('path').focus()};
function compareBox(id,n){const s=smap[id];const options=styles.map(s2=>'<option value="'+s2.id+'"'+(s2.id===id?' selected':'')+'>'+esc(s2.zh)+'</option>').join('');
 return '<article class="compare-card"><label>对照 '+n+'<select aria-label="对照 '+n+'">'+options+'</select></label><img src="'+url(s.cover)+'" alt="'+esc(s.title)+'"><h2>'+esc(s.zh)+'</h2>'+dots(s)+'<p>'+esc(s.form)+'</p><div class="samples">'+[['textures/paper.png','纸纤纹理'],['icons/search.svg','搜索图标'],['illustrations/study-02.svg','独立插图']].map(([i,t])=>'<figure><img src="'+url('STYLES/'+id+'/'+i)+'" alt="'+t+'"><figcaption>'+t+'</figcaption></figure>').join('')+'</div><p><b>适用：</b>'+esc(s.use)+'</p><a href="'+url('STYLES/'+id+'/STYLE_GUIDE.md')+'" target="_blank">风格规范 ↗</a></article>'}
let comp=['bauhaus','dunhuang'];function compare(){const r=$('comparisons');r.innerHTML=comp.map((s,i)=>compareBox(s,i+1)).join('');r.querySelectorAll('select').forEach((sel,i)=>sel.onchange=()=>{comp[i]=sel.value;compare();r.querySelectorAll('select')[i].focus()})}
$('matrix').innerHTML=styles.map(s=>'<tr><td>'+String(s.no).padStart(2,'0')+'　'+esc(s.zh)+'</td><td>'+esc(s.title)+'</td><td>'+esc(s.use)+'</td><td>'+dots(s)+'</td></tr>').join('');
function route(){const view=['styles','assets','compare'].includes(location.hash.slice(1))?location.hash.slice(1):'styles';['styles','assets','compare'].forEach(id=>$(id).hidden=id!==view);document.querySelectorAll('header nav a').forEach(a=>{if(a.hash==='#'+view)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});window.scrollTo(0,0)}
renderStyles();filter();compare();route();addEventListener('hashchange',route);
})();
