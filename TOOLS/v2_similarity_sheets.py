"""把感知哈希候选按连通组集中展示，所有候选仍需明确的复核结论。"""
import json,math
from PIL import Image,ImageDraw,ImageFont
from styles_data import ROOT,dump
F='C:/Windows/Fonts/msyh.ttc'
def run():
 idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'));data={a['asset_id']:a for a in idx['assets']};ss={s['id']:s for s in idx['styles']}
 audit=json.loads((ROOT/'AUDIT/v2-audit.json').read_text(encoding='utf8'));pairs=audit['phash_candidates'];parent={}
 def root(a):
  parent.setdefault(a,a)
  while parent[a]!=a:a=parent[a]
  return a
 for r in pairs:
  A,B=root(r['a']),root(r['b']);parent[A]=B
 groups={}
 for a in parent:groups.setdefault(root(a),[]).append(a)
 output=[]
 for k,ids in enumerate(sorted(groups.values(),key=lambda g:(data[g[0]]['category'],-len(g)))):
  ids.sort(key=lambda id:(ss[data[id]['style_id']]['no'],id));paths=[]
  for page in range(math.ceil(len(ids)/24)):
   part=ids[page*24:page*24+24];im=Image.new('RGB',(1280,80+math.ceil(len(part)/4)*222),'#f2efe8');d=ImageDraw.Draw(im);d.text((15,15),f'相似候选组 {k+1:02} / {page+1} · {data[ids[0]]["category"]} · {len(ids)} 个文件',font=ImageFont.truetype(F,24),fill='#27302b')
   for n,id in enumerate(part):
    a=data[id];S=ss[a['style_id']];x=n%4*320;y=80+n//4*222
    tile=Image.new('RGBA',(306,170),S['palette'][0] if a['transparency'] else '#e0e0d8');src=Image.open(ROOT/a['preview_path']).convert('RGBA');src.thumbnail((300,166));tile.alpha_composite(src,((306-src.width)//2,(170-src.height)//2));im.paste(tile.convert('RGB'),(x+7,y))
    d.text((x+7,y+174),S['zh']+' / '+a['asset_name'][:12],font=ImageFont.truetype(F,14),fill='#283029');d.text((x+7,y+197),id.split('.',1)[1][:43],font=ImageFont.truetype(F,11),fill='#5b625f')
   path=f'PREVIEWS/similarity/group-{k+1:02}-{page+1}.jpg';p=ROOT/path;p.parent.mkdir(exist_ok=True);im.save(p,quality=93);paths.append(path)
  output.append(dict(group=k+1,category=data[ids[0]]['category'],assets=ids,pairs=[n for n,p in enumerate(pairs)if p['a']in ids],pages=paths,status='pending'))
 overview=[];flat=[(g['group'],id)for g in output for id in g['assets']]
 for page in range(math.ceil(len(flat)/24)):
  part=flat[page*24:page*24+24];im=Image.new('RGB',(1280,80+math.ceil(len(part)/4)*222),'#f2efe8');d=ImageDraw.Draw(im);d.text((15,15),f'感知相似总览 {page+1} · 组号对应 AUDIT/similarity-groups.json',font=ImageFont.truetype(F,23),fill='#27302b')
  for n,(group,id)in enumerate(part):
   a=data[id];S=ss[a['style_id']];x=n%4*320;y=80+n//4*222;tile=Image.new('RGBA',(306,170),S['palette'][0] if a['transparency'] else '#e0e0d8');src=Image.open(ROOT/a['preview_path']).convert('RGBA');src.thumbnail((300,166));tile.alpha_composite(src,((306-src.width)//2,(170-src.height)//2));im.paste(tile.convert('RGB'),(x+7,y))
   d.text((x+7,y+174),f'G{group:02} '+S['zh']+' / '+a['asset_name'][:10],font=ImageFont.truetype(F,14),fill='#283029');d.text((x+7,y+197),id.split('.',1)[1][:43],font=ImageFont.truetype(F,11),fill='#5b625f')
  path=f'PREVIEWS/similarity/overview-{page+1:02}.jpg';im.save(ROOT/path,quality=93);overview.append(dict(page=path,assets=[id for _,id in part],groups=sorted(set(g for g,_ in part))))
 dump(ROOT/'AUDIT/similarity-overviews.json',overview)
 dump(ROOT/'AUDIT/similarity-groups.json',output);print(len(output),'groups;',len(overview),'overview pages;',sum(len(g['assets'])for g in output),'distinct candidates')
if __name__=='__main__':run()
