import json,html
from styles_data import ROOT,STYLES,write
pages=json.loads((ROOT/'AUDIT/contact-pages.json').read_text(encoding='utf8'))
idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'))
body='<h1>ARTISAN V2 · 完整素材联系表</h1><p>独立作品按六类展示；原件变体单独列页。图中编号与文件映射见 AUDIT/contact-pages.json。缩略图与本页不计素材。</p><p><a href="../BROWSER/index.html">返回离线浏览器</a> · <a href="../AUDIT/PROGRESS.md">数量台账</a></p>'
for S in STYLES:
 group=[p for p in pages if p['style']==S['id']]
 body+=f'<details id="{S["id"]}"><summary>{S["no"]:02} {S["zh"]} · {len(group)} 页</summary>'
 for p in group:
  src=p['path'].removeprefix('PREVIEWS/');title=p['category']+' / '+str(p['page'])
  body+=f'<figure><a href="{src}" target="_blank"><img loading="lazy" src="{src}" alt="{html.escape(S["zh"]+" "+title)}"></a><figcaption>{title} · {len(p["assets"])} 个文件</figcaption></figure>'
 body+='</details>'
write(ROOT/'PREVIEWS/CONTACT_SHEETS.html','<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ARTISAN V2 联系表</title><style>body{font:16px/1.6 system-ui,sans-serif;max-width:1320px;padding:28px;margin:auto;background:#f4f0e6;color:#25322d}a{color:#315e55}summary{padding:15px;border-top:1px solid #b3b8aa;font-size:20px;cursor:pointer}figure{margin:24px 0}img{width:100%;height:auto}figcaption{font-size:14px;padding:8px}</style>'+body+'</html>')
print(len(pages),'pages linked')
