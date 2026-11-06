"""V2索引：实际文件与独立作品分别统计。V1保留项仍可检索，但不重复占额。"""
import json,collections,csv
from pathlib import Path
from styles_data import ROOT,STYLES,dump,write
from generate_index import dimensions,digest,CATS
from v2_registry import legacy_family,SERIES,inventories
FIELDS=['source','author','license','license_file','attribution','modification_status']
def build():
 old=json.loads((ROOT/'AUDIT/v1-asset-index.json').read_text(encoding='utf8'));assets=[];styles=[];summary=inventories()
 for S in STYLES:
  z=S['id'];base=ROOT/'STYLES'/z
  render={r['file']:r for r in json.loads((ROOT/f'AUDIT/render-{z}.json').read_text(encoding='utf8'))}
  for a in old['assets']:
   if a['style_id']!=z:continue
   a=dict(a);fam,yes,why=legacy_family(a);cat=a['category'];p=ROOT/a['file_path'];rel=p.relative_to(base).as_posix()
   series=SERIES[z][2 if cat=='ui' else 1 if fam=='photo-environment' else 0]
   if cat=='illustrations':series=SERIES[z][int(p.stem[-2:])%3]
   a.update(family_id=f'{z}.{cat}.{fam}',counted=yes,credit='existing' if yes else 'retained',series=series,revision='V1',count_note=why,role='object' if cat=='illustrations' else 'component' if cat=='ui' else 'legacy',preview_path=render[rel]['preview'])
   a['sha256']=digest(p);assert a['sha256']==render[rel]['sha256']
   assets.append(a)
  for mp in sorted((base/'v2-records').glob('*.json')):
   for m in json.loads(mp.read_text(encoding='utf8')):
    p=base/m['file'];w,h,mode=dimensions(p);cat=m['file'].split('/')[0];fmt=p.suffix[1:];r=render[m['file']]
    if m.get('origin')!='original':raise ValueError('Unknown source '+str(p))
    legal=dict(source='ARTISAN 自制 / TOOLS 中可重建源文件',author='hanhanhu847-star（Codex 辅助制作）',license='CC-BY-4.0',license_file='LICENSES/CC-BY-4.0.txt',attribution='ARTISAN V2 by hanhanhu847-star / CC BY 4.0 / https://github.com/hanhanhu847-star/artisan-v2',modification_status='本工程原创矢量或原生程序生成；栅格导出不重复计数')
    if 'license' in m:
     for f in FIELDS:assert m.get(f),'Missing licensed source field '+f
     legal={f:m[f]for f in FIELDS}
    for f in ['license_file']:assert (ROOT/legal[f]).is_file()
    a=dict(asset_id=f'{z}.{cat}.{p.stem}.{fmt}',asset_name=m['asset_name'],style_id=z,category=cat,file_format=fmt,width=w,height=h,color_mode=mode,transparency=m['transparency'],tiling=m['tiling'],intended_usage=m['intended_usage'],file_path=p.relative_to(ROOT).as_posix(),preview_path=r['preview'],file_bytes=p.stat().st_size,sha256=digest(p),family_id=f'{z}.{cat}.{m["family"]}',counted=m['credit']!='variant',credit=m['credit'],series=m['series'],revision='V2',role=m['role'],count_note='同一家族的保留原件、格式、尺寸、状态不重复统计',**legal)
    assert a['sha256']==r['sha256'],'Stale render '+a['file_path']
    assets.append(a)
  group=[a for a in assets if a['style_id']==z];reps=[a for a in group if a['counted']]
  assert len(reps)==summary[z]['total'] and len({a['family_id']for a in reps})==len(reps)
  style={**{k:S.get(k,'')for k in ['id','zh','en','group','palette','no','title','form','material','use']},'count':len(group),'work_count':len(reps),'series':SERIES[z],'counts_by_category':dict(collections.Counter(a['category']for a in reps)),'series_counts':dict(collections.Counter(a['series']for a in reps)),'cover':f'PREVIEWS/plates/{z}.webp','contacts':f'PREVIEWS/contacts/{z}/01-backgrounds-1.jpg'}
  styles.append(style)
 for a in old['assets']:
  if a['style_id']=='shared':assets.append({**a,'family_id':a['asset_id'],'counted':True,'credit':'existing','series':'公用辅助','revision':'V1','role':'utility','count_note':'共享辅助，不占16套指标'})
 styles.append({**next(s for s in old['styles']if s['id']=='shared'),'work_count':4,'series':['公用辅助']})
 if len({a['asset_id']for a in assets})!=len(assets):raise ValueError('Duplicate IDs')
 indexed={a['file_path']for a in assets}
 actual={p.relative_to(ROOT).as_posix()for z in [s['id']for s in STYLES]for cat in ['backgrounds','textures','ornaments','icons','illustrations','ui']for p in (ROOT/'STYLES'/z/cat).glob('*')if p.is_file()}
 assert actual <= indexed,'Unindexed source files: '+str(actual-indexed)
 out=dict(library='ARTISAN',version='2.0.0',audit_status='provisional-pending-full-visual-and-duplicate-review',styles=styles,categories=CATS,assets=assets,work_count=sum(s['work_count']for s in styles if s['id']!='shared'),file_count=len(assets))
 dump(ROOT/'ASSET_INDEX.json',out);write(ROOT/'BROWSER/catalog-data.js','window.ARTISAN = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
 dump(ROOT/'LICENSES/asset-sources-v2.json',[{k:a[k]for k in ['asset_id','file_path','sha256']+FIELDS}for a in assets])
 print(len(assets),'source files,',out['work_count'],'independent style families (provisional), plus 4 shared')
 return out
if __name__=='__main__':build()
