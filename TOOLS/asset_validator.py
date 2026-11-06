"""图像及索引一致性校验。python TOOLS/asset_validator.py；需要 Pillow 和 NumPy。"""
import json,sys,collections,xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
import numpy as np
from generate_index import ROOT,dimensions,digest
from styles_data import STYLES
FIELDS='asset_id asset_name style_id category file_format width height color_mode transparency tiling intended_usage source author license attribution modification_status'.split()
def run():
    rows=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'))['assets'];errors=[];stats=collections.Counter();seen={};ids=set();paths=set();seams=[];originals=json.loads((ROOT/'LICENSES/photo-sources.json').read_text(encoding='utf8'))
    for r in rows:
        try:
            p=ROOT/r['file_path'];assert p.resolve().is_relative_to(ROOT.resolve());assert r['asset_id'] not in ids and r['file_path'] not in paths;ids.add(r['asset_id']);paths.add(r['file_path'])
            assert all(f in r and r[f] is not None and r[f]!='' for f in FIELDS)
            w,h,cm=dimensions(p);assert (w,h,cm)==(r['width'],r['height'],r['color_mode'])
            assert p.stat().st_size==r['file_bytes'] and digest(p)==r['sha256']
            assert (ROOT/r['license_file']).is_file() and (ROOT/r['preview_path']).is_file()
            assert r['sha256'] not in seen, 'byte-identical material to '+str(seen.get(r['sha256']))
            seen[r['sha256']]=r['asset_id']
            if p.suffix=='.svg':
                e=ET.parse(p).getroot();assert e.tag.endswith('}svg') and e.get('viewBox');assert all(not node.tag.endswith('}script') for node in e.iter());stats['svg_xml']+=1
            else:
                with Image.open(p) as im:
                    assert im.format.lower() in ({'jpeg'} if p.suffix=='.jpg' else {p.suffix[1:].lower()})
                    im.verify()
                with Image.open(p) as im:
                    if im.format=='JPEG':im.draft('RGB',(1280,720))
                    im.load();stats['raster_decoded']+=1
                    if r['transparency']:
                        assert 'A' in im.getbands() and im.getchannel('A').getextrema()[0]==0 and im.getchannel('A').getextrema()[1]>0
                        stats['alpha_raster']+=1
                    if r['tiling']:
                        arr=np.asarray(im.convert('RGB'),dtype=float);dx=np.abs(np.diff(arr,axis=1)).mean(axis=(0,2));dy=np.abs(np.diff(arr,axis=0)).mean(axis=(1,2))
                        sx=np.abs(arr[:,0]-arr[:,-1]).mean();sy=np.abs(arr[0]-arr[-1]).mean()
                        # 接缝与同图内部相邻列/行的99.5分位比较；既保留实体纹理的噪声也检测宽边缝。
                        limx=max(4.,np.quantile(dx,.995)*1.65);limy=max(4.,np.quantile(dy,.995)*1.65)
                        assert sx<=limx and sy<=limy,(sx,limx,sy,limy)
                        seams.append(dict(asset_id=r['asset_id'],x=round(float(sx),2),y=round(float(sy),2),limit_x=round(float(limx),2),limit_y=round(float(limy),2)))
            if r['license']=='CC0-1.0':
                assert any(ph.get('source')==r['source'] and ', '.join(ph['authors'])==r['author'] for ph in originals)
                stats['cc0_assets']+=1
        except Exception as e:errors.append({'asset':r.get('asset_id'),'error':repr(e)})
    files={p.relative_to(ROOT).as_posix() for base in [ROOT/'STYLES',ROOT/'SHARED'] for p in base.rglob('*') if p.suffix.lower() in {'.svg','.jpg','.png','.webp'}}
    if paths!=files:errors.append(dict(missing=sorted(files-paths),extra=sorted(paths-files)))
    for s in STYLES:
        rr=[r for r in rows if r['style_id']==s['id']]
        for cat,num in dict(backgrounds=13,textures=10,ornaments=12,icons=20,ui=70,illustrations=3).items():
            if sum(r['category']==cat for r in rr)<num:errors.append({'coverage':s['id']+'/'+cat})
        for size in [(1920,1080),(2560,1440),(3840,2160)]:
            if not any((r['width'],r['height'])==size and r['file_format']=='jpg' for r in rr):errors.append({'resolution':s['id']+str(size)})
    result=dict(assets=len(rows),styles=len(STYLES),stats=dict(stats),raster_seams_tested=len(seams),seams=seams,errors=errors)
    print(json.dumps({k:v for k,v in result.items() if k!='seams'},ensure_ascii=False))
    if '--record' in sys.argv:(ROOT/'PREVIEWS/asset-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    if errors:raise SystemExit(1)
if __name__=='__main__':run()
