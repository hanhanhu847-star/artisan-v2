"""检查每项原生平铺材质的真实边缘；同时构造2×2检阅样张，透明叠层另验 alpha。"""
import numpy as np,json
from PIL import Image,ImageDraw
from v2_registry import *
def edges(im):
    a=np.array(im.convert('RGB'),dtype='int16');sx=float(np.abs(a[:,0]-a[:,-1]).mean());sy=float(np.abs(a[0]-a[-1]).mean())
    dx=np.abs(np.diff(a,axis=1)).mean((0,2));dy=np.abs(np.diff(a,axis=0)).mean((1,2))
    lim=lambda b:float(max(3.5,np.quantile(b,.995)*1.60+1.0))
    return dict(x=round(sx,3),y=round(sy,3),max_x=round(lim(dx),3),max_y=round(lim(dy),3),ok=bool(sx<=lim(dx) and sy<=lim(dy)))
def run():
    total=[]
    for s in STYLES:
        z=s['id'];rows=json.loads((meta_folder(z)/'textures.json').read_text(encoding='utf8'))
        proof=Image.new('RGB',(4*198,4*142),'#d6d2c3');d=ImageDraw.Draw(proof)
        for j,r in enumerate(rows):
            p=outfile(z,r)
            with Image.open(p)as im:
                im.load();assert im.size==(2048,2048);rec=dict(style=z,file=r['file'],size=im.size)
                if r['tiling']:
                    native=edges(im);macro=edges(im.resize((256,256),Image.Resampling.BOX));rec.update(native=native,macro=macro,ok=native['ok'] and macro['ok'])
                    small=im.convert('RGB').resize((85,60),Image.Resampling.LANCZOS);tile=Image.new('RGB',(170,120))
                    for xx in (0,85):
                        for yy in (0,60):tile.paste(small,(xx,yy))
                else:
                    al=im.getchannel('A');lo,hi=al.getextrema();rec.update(alpha=[lo,hi],ok=lo==0 and hi>0)
                    sm=im.convert('RGBA');sm.thumbnail((123,123));tile=Image.new('RGB',(170,120),'#c6bdae');tile.paste(sm,(22,0),sm.getchannel('A'))
                X=j%4*198+6;Y=j//4*142+4;proof.paste(tile,(X,Y));d.text((X,Y+121),r['process'],fill='#272e2c');total.append(rec)
        dpath=ROOT/'PREVIEWS/v2-tile-proofs';dpath.mkdir(exist_ok=True);proof.save(dpath/(z+'.jpg'),quality=91)
    dump(ROOT/'AUDIT/v2-texture-check.json',total);bad=[x for x in total if not x['ok']]
    print('tested',len(total),'tiles',sum('native' in r for r in total),'alpha',sum('alpha' in r for r in total),'failures',len(bad));print(json.dumps(bad[:8],ensure_ascii=False))
    if bad:raise SystemExit(1)
if __name__=='__main__':run()
