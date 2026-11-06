"""逐一呈现独立作品及另页的原件变体；联系表不计作品。"""
import json,math
from PIL import Image,ImageDraw,ImageFont
from styles_data import ROOT,STYLES
from v2_registry import legacy_family
F='C:/Windows/Fonts/msyh.ttc'
def font(n):return ImageFont.truetype(F,n)
def run():
 old=json.loads((ROOT/'AUDIT/v1-asset-index.json').read_text(encoding='utf8'))['assets']
 pages=[]
 for S in STYLES:
  z=S['id'];renders={x['file']:x for x in json.loads((ROOT/f'AUDIT/render-{z}.json').read_text(encoding='utf8'))};rows=[];extra=[]
  for a in old:
   if a['style_id']!=z:continue
   fam,yes,_=legacy_family(a);r=dict(file='/'.join(a['file_path'].split('/')[2:]),asset_name=a['asset_name'],category=a['category'],credit='V1',transparency=a['transparency'])
   (rows if yes else extra).append(r)
  for p in (ROOT/f'STYLES/{z}/v2-records').glob('*.json'):
   for a in json.loads(p.read_text(encoding='utf8')):
    a['category']=a['file'].split('/')[0];(extra if a['credit']=='variant' else rows).append(a)
  groups=[('01-backgrounds',[r for r in rows if r['category']=='backgrounds']),('02-textures',[r for r in rows if r['category']=='textures']),('03-ornaments',[r for r in rows if r['category']=='ornaments']),('04-icons',[r for r in rows if r['category']=='icons']),('05-illustrations',[r for r in rows if r['category']=='illustrations']),('06-ui',[r for r in rows if r['category']=='ui']),('07-retained-variants',extra)]
  for cat,group in groups:
   for page in range(math.ceil(len(group)/32)):
    part=group[page*32:page*32+32];cols=4;cw=320;ch=220;sheet=Image.new('RGB',(cols*cw,95+math.ceil(len(part)/cols)*ch),'#f3f0e8');d=ImageDraw.Draw(sheet)
    d.text((22,14),S['zh']+' / '+cat+' / '+str(page+1),font=font(24),fill='#202724');d.text((22,52),'实际文件缩略图 · 透明区域以棋盘衬底 · 原件变体另页保留',font=font(16),fill='#555f59')
    for n,r in enumerate(part):
     x=(n%cols)*cw;y=90+(n//cols)*ch;m=renders[r['file']];im=Image.open(ROOT/m['preview']).convert('RGBA');tile=Image.new('RGB',(cw-14,172),'#e4e4df');td=ImageDraw.Draw(tile)
     if r.get('transparency'):
      pal=S['palette'][0];rgb=tuple(int(pal[j:j+2],16)for j in [1,3,5]);dark=sum(rgb)<320
      td.rectangle((0,0,cw-14,172),fill='#253943' if dark else '#e4e4df')
      for yy in range(0,172,12):
       for xx in range(0,cw-14,12):
        if (yy//12+xx//12)%2:td.rectangle((xx,yy,xx+11,yy+11),fill='#33434b' if dark else '#cbcfcb')
     im.thumbnail((cw-22,168));tile.paste(im,((tile.width-im.width)//2,(172-im.height)//2),im);sheet.paste(tile,(x+7,y))
     d.text((x+9,y+176),r['asset_name'][:24],font=font(15),fill='#27302b');d.text((x+9,y+199),f"{n+1+page*32:02d} · {m['width']}×{m['height']} · {r['credit']}",font=font(12),fill='#555f59')
    dest=ROOT/f'PREVIEWS/contacts/{z}/{cat}-{page+1}.jpg';dest.parent.mkdir(parents=True,exist_ok=True);sheet.save(dest,quality=92);pages.append(dict(style=z,category=cat,page=page+1,path=dest.relative_to(ROOT).as_posix(),assets=[r['file'] for r in part]))
 (ROOT/'AUDIT/contact-pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf8')
 print(len(pages),'contact pages')
if __name__=='__main__':run()
