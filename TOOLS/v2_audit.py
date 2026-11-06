"""文件级/作品级去重、像素与配额检查。相似候选必须复核，不自动宣告独立。"""
import json,hashlib,collections,re,xml.etree.ElementTree as ET,math,time
import numpy as np
from PIL import Image
from styles_data import ROOT,dump,STYLES
from generate_index import digest
from v2_registry import TARGET
from v2_common_icons import NAMES
Image.MAX_IMAGE_PIXELS=1_500_000_000
DCT=np.cos(np.pi*(np.arange(32)[None,:]+.5)*np.arange(8)[:,None]/32)
def phash(im,bg):
 rgba=np.asarray(im.convert('RGBA').resize((32,32),Image.Resampling.LANCZOS),dtype=float)/255
 lum=(rgba[:,:,:3]@np.array([.2126,.7152,.0722]))*rgba[:,:,3]+bg*(1-rgba[:,:,3])
 d=DCT@lum@DCT.T;flat=d.flatten()[1:];bits=flat>np.median(flat)
 return int(''.join('1' if x else '0'for x in bits),2)
def canonical(el,root=False):
 tag=el.tag.split('}')[-1]
 if tag in ['title','desc','metadata','style']:return ''
 ignore={'fill','stroke','stroke-width','stroke-linecap','stroke-linejoin','opacity','fill-opacity','stroke-opacity','class','id','font-family','font-weight','font-size','color'}
 if root:ignore|={'width','height'}
 attrs=[]
 for k,v in el.attrib.items():
  k=k.split('}')[-1]
  if k in ignore:continue
  if k in ['d','points','transform','viewBox']:
   v=re.sub(r'[-+]?(?:\d*\.)?\d+(?:[Ee][-+]?\d+)?',lambda m:f'{float(m[0]):.3f}',v)
  attrs.append((k,v))
 return tag+str(sorted(attrs))+''.join(canonical(c)for c in el)
def run():
 t=time.time();idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'));rows=idx['assets'];errors=[];sha=collections.defaultdict(list);struct=collections.defaultdict(list);hashes={};all_hashes={}
 for a in rows:
  p=ROOT/a['file_path'];actual=digest(p)
  if actual!=a['sha256']:errors.append('sha mismatch '+a['asset_id'])
  sha[actual].append(a['asset_id'])
  if p.suffix=='.svg':
   el=ET.parse(p).getroot()
   for e in el.iter():
    if e.tag.split('}')[-1] in ['script','foreignObject']:errors.append('unsafe SVG '+a['asset_id'])
    for k,v in e.attrib.items():
     if k.split('}')[-1] in ['href','src'] and not v.startswith('#'):errors.append('external SVG '+a['asset_id'])
   if a['counted']:struct[hashlib.sha256(canonical(el,True).encode()).hexdigest()].append(a['asset_id'])
  if a['style_id']=='shared':continue
  with Image.open(ROOT/a['preview_path'])as im:
   h=(phash(im,0),phash(im,1));all_hashes[a['asset_id']]=[f'{x:016x}'for x in h]
   if a['counted']:hashes[a['asset_id']]=h
  if p.suffix!='.svg':
   with Image.open(p)as im:
    if im.size!=(a['width'],a['height']):errors.append('size mismatch '+a['asset_id'])
    if a['transparency'] and ('A' not in im.getbands()or im.getchannel('A').getextrema()[0]==255):errors.append('missing alpha '+a['asset_id'])
  if not p.suffix[1:].lower()==a['file_format']:errors.append('format mismatch '+a['asset_id'])
 duplicate_groups=[v for v in sha.values()if len(v)>1];struct_groups=[v for v in struct.values()if len(v)>1]
 reps=[a for a in rows if a['counted']and a['style_id']!='shared'];candidates=[]
 for n,a in enumerate(reps):
  h=hashes[a['asset_id']]
  for b in reps[n+1:]:
   if a['category']!=b['category']:continue
   hh=hashes[b['asset_id']];d0=(h[0]^hh[0]).bit_count();d1=(h[1]^hh[1]).bit_count()
   if max(d0,d1)<=5:candidates.append(dict(a=a['asset_id'],b=b['asset_id'],distance_dark=d0,distance_light=d1,cross_style=a['style_id']!=b['style_id'],status='needs-review'))
 counts=[]
 for S in STYLES:
  z=S['id'];rs=[a for a in reps if a['style_id']==z];by=collections.Counter(a['category']for a in rs);gap={cat:max(0,v-by[cat])for cat,v in TARGET.items()}
  bg=[a for a in rs if a['category']=='backgrounds']
  dims=dict(landscape=sum(a['width']>=3840 and a['height']>=2160 and 1.5<=a['width']/a['height']<2 for a in bg),portrait=sum(a['width']>=2160 and a['height']>=3840 and a['height']>a['width']for a in bg),square=sum(a['width']==a['height']and a['width']>=3000 for a in bg),ultrawide=sum(a['width']>=5120 and a['height']>=1440 and a['width']/a['height']>=3 for a in bg))
  tex=[a for a in rs if a['category']=='textures'];tiles=sum(a['tiling']and min(a['width'],a['height'])>=2048 for a in tex);alpha=sum(a['transparency']for a in tex)
  special=sum(a['role']=='special-glyph'for a in rs);scenes=sum(a['role']=='scene'for a in rs);obj=sum(a['role']=='object'for a in rs)
  common={a['file_path'].rsplit('/',1)[1][3:-4]for a in rs if a['role']=='common-glyph'}
  series=collections.Counter(a['series']for a in rs)
  bad=any(gap.values())or dims['landscape']<4 or dims['portrait']<2 or dims['square']<2 or dims['ultrawide']<2 or tiles<8 or alpha<4 or special<8 or scenes<4 or obj<6 or not set(NAMES)<=common or len(series)<3 or min(series.values())<6
  if bad:errors.append('quota '+z)
  counts.append(dict(style=z,files=sum(a['style_id']==z for a in rows),independent=len(rs),counts=dict(by),gaps=gap,background_shapes=dims,tiles_2k=tiles,alpha_overlays=alpha,special_icons=special,common_icons=len(common),scenes=scenes,objects=obj,series=dict(series)))
 out=dict(version='V2',files=len(rows),style_families=len(reps),shared=4,errors=errors,sha_duplicate_groups=duplicate_groups,sha_duplicate_files=sum(len(g)-1 for g in duplicate_groups),svg_geometry_groups=struct_groups,phash_candidates=candidates,style_counts=counts,elapsed_seconds=round(time.time()-t,2),status='technical-checks-only; similarity and full visual review pending')
 dump(ROOT/'AUDIT/v2-audit.json',out);dump(ROOT/'AUDIT/phashes.json',all_hashes)
 print(json.dumps({k:out[k]for k in ['files','style_families','errors','sha_duplicate_files','elapsed_seconds']},ensure_ascii=False));print(len(struct_groups),'geometry groups;',len(candidates),'pHash candidates')
 if errors:raise SystemExit(1)
if __name__=='__main__':run()
