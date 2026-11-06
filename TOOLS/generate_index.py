"""由真实文件测量尺寸、格式、字节数和 SHA-256；从逐风格元数据重建 JSON 与离线数据脚本。"""
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image
from styles_data import ROOT,STYLES,dump,write
Image.MAX_IMAGE_PIXELS=1_500_000_000
CATS=dict(backgrounds='背景',textures='纹理',ornaments='装饰',icons='图标',ui='UI 组件',illustrations='插图',patterns='图样',**{'utility-assets':'辅助素材'})
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def dimensions(p):
    if p.suffix=='.svg':
        s=ET.parse(p).getroot();return int(s.get('width')),int(s.get('height')),'sRGB · 矢量'
    with Image.open(p) as im:return im.width,im.height,im.mode
def run():
    photos={p['slug']:p for p in json.loads((ROOT/'LICENSES/photo-sources.json').read_text(encoding='utf8')) if 'path' in p}
    rows=[];styles=[]
    registered=sorted([json.loads(p.read_text(encoding='utf8')) for p in (ROOT/'STYLES').glob('*/style.json')],key=lambda s:(s['no'],s['id']))
    if not registered or len({s['id'] for s in registered})!=len(registered):raise ValueError('Missing or duplicate style definitions')
    for s in registered+[dict(id='shared',zh='公用素材',en='Shared',group='公用',palette=['#f0eee8','#202523','#a64b35','#647768','#dec485'],no=0,title='通用辅助')]:
        z=s['id'];base=ROOT/'SHARED' if z=='shared' else ROOT/'STYLES'/z;count=0
        for meta in json.loads((base/'asset-meta.json').read_text(encoding='utf8')):
            p=base/meta['file'];w,h,cm=dimensions(p);rel=p.relative_to(ROOT).as_posix()
            cat=meta['file'].split('/')[0];fmt=p.suffix[1:].lower();slug=p.stem
            if meta.get('origin') not in {'original','polyhaven'}:raise ValueError('Missing or unsupported source declaration: '+rel)
            ph=photos[meta['photo']] if meta['origin']=='polyhaven' else None
            if not ph and 'photo' in meta:raise ValueError('Photo cannot be declared original: '+rel)
            author=', '.join(ph['authors']) if ph else 'hanhanhu847-star（Codex 辅助制作）'
            thumb=rel
            if ph and not meta.get('derived'):thumb=f'PREVIEWS/plates/{z}-photo.webp'
            if slug.startswith('field-study') and fmt=='jpg':thumb=f'PREVIEWS/plates/{z}.webp'
            rows.append(dict(asset_id=f'{z}.{cat}.{slug}.{fmt}',asset_name=meta['asset_name'],style_id=z,category=cat,file_format=fmt,width=w,height=h,color_mode=cm,transparency=meta['transparency'],tiling=meta['tiling'],intended_usage=meta['intended_usage'],source=ph['source'] if ph else 'ARTISAN 自制 / TOOLS 中的可重建源文件',author=author,license='CC0-1.0' if ph else 'CC-BY-4.0',license_file='LICENSES/CC0-1.0.txt' if ph else 'LICENSES/CC-BY-4.0.txt',attribution=(ph['title']+' / '+author+' / Poly Haven / CC0') if ph else 'ARTISAN V2 by hanhanhu847-star / CC BY 4.0 / https://github.com/hanhanhu847-star/artisan-v2',modification_status=('由对应官方全景原件透视取景并编码为 JPEG' if meta.get('derived') else ph['modification_status']) if ph else '本工程原创；栅格副本来自同套矢量或程序化生成源',file_path=rel,preview_path=thumb,file_bytes=p.stat().st_size,sha256=digest(p)))
            count+=1
        styles.append({**{k:s.get(k,'') for k in ['id','zh','en','group','palette','no','title','form','material','use']},'count':count,'cover':f'PREVIEWS/plates/{z}.webp' if z!='shared' else 'SHARED/patterns/alpha-grid.svg'})
    index=dict(library='ARTISAN',version='1.0.0',styles=styles,categories=CATS,assets=rows);dump(ROOT/'ASSET_INDEX.json',index)
    write(ROOT/'BROWSER/catalog-data.js','window.ARTISAN = '+json.dumps(index,ensure_ascii=False,separators=(',',':'))+';\n')
    print(len(rows),'indexed assets;',len(set(r['asset_id'] for r in rows)),'unique ids')
if __name__=='__main__':
    # V2 includes this module for dimensions/digest; do not replace the V2 catalog
    # with the retained V1-only index if a user runs the old entry point.
    if (ROOT/'TOOLS/v2_index.py').is_file():
        from v2_index import build
        build()
    else:run()
