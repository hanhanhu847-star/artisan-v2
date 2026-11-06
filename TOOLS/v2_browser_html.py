"""保留V1页面结构，只加入扩容需要的筛选与提取控件。"""
from styles_data import ROOT,write
p=ROOT/'BROWSER/index.html'
s=p.read_text(encoding='utf8')
if 'id="f-series"'not in s:
 s=s.replace('藏品版次　01 / 16','藏品版次　V2 / 16')
 s=s.replace('<label>类别<select id="f-cat"></select></label>','<label>类别<select id="f-cat"></select></label><label>子系列<select id="f-series"></select></label>')
 s=s.replace('<button id="reset" class="quiet">','<label>透明<select id="f-alpha"></select></label><label>显示<select id="f-view"><option value="family">每个作品一个版本</option><option value="files">全部文件及保留版本</option></select></label><label>收藏<select id="f-favorite"><option value="">全部</option><option value="yes">仅收藏</option></select></label><button id="reset" class="quiet">')
 s=s.replace('<div id="asset-grid"','<div class="selection-bar"><span id="selection-count" role="status">已选 0 项</span><button id="select-page">选择本页</button><button id="clear-selection">清空选择</button><button id="export-selected">导出所选清单 ↓</button></div><div id="asset-grid"')
 s=s.replace('<div class="detail-links">','<div class="detail-links"><button id="detail-favorite">收藏此作品</button>')
 s=s.replace('<a href="../LICENSES/ATTRIBUTION.md" target="_blank">摄影来源 ↗</a>','<a href="../LICENSES/asset-sources-v2.json" target="_blank">完整来源清单 ↗</a><a href="../PREVIEWS/CONTACT_SHEETS.html" target="_blank">逐套联系表 ↗</a>')
 s=s.replace('src="browser.js"','src="browser-v2.js"')
 write(p,s)
p=ROOT/'BROWSER/browser.css';s=p.read_text(encoding='utf8')
if '/* V2 controls */' not in s:
 s+='''
/* V2 controls */
.filters{grid-template-columns:repeat(auto-fit,minmax(138px,1fr));align-items:end}
.filters .search{grid-column:span 2}
.selection-bar{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin:0 0 22px}
.selection-bar span{margin-right:auto}
.asset-entry{min-width:0;border:1px solid var(--line,#ccc6ba);background:var(--paper,#f7f4ec)}
.asset-entry .asset-card{width:100%;border:0;display:block}
.asset-actions{display:flex;gap:10px;justify-content:space-between;align-items:center;padding:8px 12px;border-top:1px solid #d5d1c7;font-size:12px}
.asset-actions label{display:flex;align-items:center;gap:6px;cursor:pointer}
.asset-actions input{width:16px;height:16px;accent-color:#376052}
.asset-actions button{font-size:12px;padding:5px 9px;min-height:30px}
.asset-actions button[aria-pressed=true]{background:#e4d9b2;color:#202622}
.asset-card .media.dark-alpha{background-color:#263d46;background-image:linear-gradient(45deg,#334951 25%,transparent 25%),linear-gradient(-45deg,#334951 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#334951 75%),linear-gradient(-45deg,transparent 75%,#334951 75%)}
.detail-links{flex-wrap:wrap;gap:12px}
#detail-favorite[aria-pressed=true]{background:#e4d9b2;color:#202622}
.asset-card .meta small{overflow-wrap:anywhere}
@media(max-width:600px){.filters .search{grid-column:1/-1}.selection-bar button{font-size:12px}.asset-actions{padding:6px}.asset-actions button{padding:4px}}
'''
 write(p,s)
