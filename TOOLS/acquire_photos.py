"""仅重建摄影库时需要联网；只下载 Poly Haven API 指定的 CC0 资产原件。"""
import json, hashlib, urllib.request, time, concurrent.futures as cf
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
CHOICES=dict(zip('bauhaus art-deco swiss neo-brutalism memphis editorial wabi-sabi dark-academia celestial-atlas dunhuang cartography natural-history retrofuturism cyberpunk blueprint generative-art'.split(),'artist_workshop dancing_hall glass_passage parking_garage colorful_studio art_studio mossy_forest historic_cloister_passage clarens_night_01 drackenstein_quarry kiara_1_dawn epping_forest_01 aviation_museum dresden_station_night aerodynamics_workshop mirrored_hall'.split()))
def read(url):
    for i in range(3):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'ARTISAN-asset-library/1.0 (local educational asset collection)'})
            with urllib.request.urlopen(req,timeout=90) as r:return r.read()
        except Exception:
            if i==2:raise
            time.sleep(1+i)
def acquire(item):
    style,slug=item
    try:
        meta=json.loads(read('https://api.polyhaven.com/info/'+slug))
        files=json.loads(read('https://api.polyhaven.com/files/'+slug)); desc=files['tonemapped']; url=desc['url']
        assert urlparse(url).hostname in ('dl.polyhaven.org','dl.polyhaven.com')
        path=ROOT/'STYLES'/style/'backgrounds'/('photo-'+slug+'.jpg')
        path.parent.mkdir(parents=True,exist_ok=True)
        data=path.read_bytes() if path.exists() else b''
        if hashlib.md5(data).hexdigest()!=desc['md5']:data=read(url)
        assert len(data)==desc['size'] and hashlib.md5(data).hexdigest()==desc['md5']
        path.write_bytes(data)
        result=dict(style_id=style,slug=slug,title=meta['name'],authors=list(meta['authors']),url=url,source='https://polyhaven.com/a/'+slug,license='CC0-1.0',license_url='https://polyhaven.com/license',md5=desc['md5'],file_size=len(data),path=path.relative_to(ROOT).as_posix(),modification_status='官方色调映射 JPEG，原样保留')
        print(style,slug,len(data),flush=True);return result
    except Exception as e:print('DOWNLOAD FAILED',style,repr(e),flush=True);return dict(style_id=style,slug=slug,error=str(e))
if __name__=='__main__':
    with cf.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(acquire,CHOICES.items()))
    dest=ROOT/'LICENSES'/'photo-sources.json';dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    print('Downloaded:',len([r for r in rows if 'path'in r]),'of',len(rows))
