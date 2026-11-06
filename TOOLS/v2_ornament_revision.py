"""边框与信息饰件重绘；保留共同用途，同时以明确的不同轮廓承载各套图形语法。"""
from v2_ui_completion import boundary,marker,capsule
from v2_ui_themes import gauge
from v2_plates import *

def open_frame(P,j):
 # Transparency is preserved: only strokes and corner motifs, no opaque paper.
 w,h=900,600;z=P.S['id'];i=P.i;a=P.a;b=P.b;c=P.c
 # boundary() first rectangle is solely the paper background.
 import re
 out=re.sub(r'^<rect\b[^>]*/>','',boundary(P,w,h),count=1)
 # A frame must leave its content aperture transparent; UI paper fills are not
 # appropriate for an ornament that is placed over an existing image.
 def outline(m):
  tag=m.group(0);f=re.search(r'fill="([^"]*)"',tag)
  if f and f[1]!='none' and 'stroke="none"' in tag:tag=tag.replace('stroke="none"','stroke="'+f[1]+'"')
  return re.sub(r'fill="[^"]*"','fill="none"',tag)
 out=re.sub(r'<[^>]+>',outline,out)
 if j==0:
  out+=marker(P,90,80,1,2.3)+marker(P,w-90,h-80,2,2.3)
  out+=P.l(155,80,360,80,b,1.2)+P.l(w-360,h-80,w-155,h-80,b,1.2)
 elif j==1:
  out+=marker(P,w/2,77,1,2.4)
  out+=P.l(55,77,w/2-97,77,b,1)+P.l(w/2+97,77,w-55,77,b,1)
  out+=P.r(55,137,w-110,h-190,None,i,1.5)+P.l(70,154,w-70,154,b,.7)
 else:
  # Style-specific spine structures, avoiding a shared colored stripe.
  if z in ['bauhaus','swiss','blueprint']:
   out+=P.l(101,71,101,h-68,a,3)+''.join(marker(P,67,120+j*115,j+1,1.1)for j in range(4))
  elif z in ['art-deco','celestial-atlas','retrofuturism']:
   out+=P.p('M112 78Q36 294 112 522',None,b,1.3)+''.join(marker(P,91-j*10 if j<2 else 71+(j-2)*10,130+j*110,j+1,1.15)for j in range(4))
  elif z in ['dunhuang','dark-academia','natural-history','cartography']:
   out+=''.join(marker(P,76,115+j*122,j+1,1.5)+P.l(120,110+j*122,149,110+j*122,b,.8)for j in range(4))
   out+=P.l(145,72,145,h-70,b,.9)
  else:
   out+=''.join(marker(P,75+(j%2)*26,100+j*97,j+1,1.3)for j in range(5))
   out+=P.p('M126 64Q167 250 130 330T140 535',None,b,1.1)
  out+=P.l(170,62,170,h-62,i,1.3)+P.r(w-240,h-103,182,43,None,b,.8)
 return svg(w,h,out)

def rule(P,j):
 w,h=720,110;z=P.S['id'];i=P.i;a=P.a;b=P.b
 if j==2:
  # Full decorative ruler uses the style's own segmentation/curve mechanism.
  out=marker(P,52,48,1,1.35)+gauge(P,108,40,590,21)
 elif j==3:
  # Repeated motif is the principal silhouette, not a tiny change to a line.
  out=''.join(marker(P,45+k*124,52,k+1,1.3)for k in range(6))
  out+=P.l(28,88,692,88,b,.7)
 else:
  out=marker(P,79,55,1,2.1)+marker(P,641,55,2,2.1)
  if z in ['bauhaus','swiss','neo-brutalism','blueprint']:out+=P.r(151,51,418,7,a,'none')+P.l(151,66,569,66,b,.8)
  elif z in ['art-deco','dark-academia','dunhuang','cartography']:out+=P.p('M152 58H276L293 41H427L445 58H568M174 67H268M452 67H546',None,i,1.3)
  elif z in ['editorial','wabi-sabi','natural-history','generative-art']:out+=P.p('M153 60Q268 30 360 55T569 50',None,i,1.5)
  else:out+=P.p('M150 59H256L285 38H434L461 59H570',None,a,2)+P.l(286,47,434,47,b,.8)
 return svg(w,h,out)

def legacy(P,kind):
 z=P.S['id'];i=P.i;a=P.a;b=P.b
 if kind=='title-frame':
  w,h=720,170
  # Empty title panel, with 510px clear text region.
  o,ink=capsule(P,16,28,688,106)
  mark=P.o(72,81,30,P.bg,ink,.8)+marker(P,72,81,1,1.1)
  return svg(w,h,o+mark+P.l(124,109,617,109,ink,.8))
 if kind=='caption-frame':
  w,h=650,150
  if z in ['swiss','editorial','blueprint']:
   o=P.r(15,20,13,103,a,'none')+P.l(46,34,635,34,i,1)+P.l(46,117,635,117,b,.8)+marker(P,68,76,1,.75)
  elif z in ['art-deco','celestial-atlas','dunhuang','retrofuturism']:
   o=marker(P,64,73,1,1.7)+P.p('M123 24H625V126H123M138 38H610M138 112H610',None,i,1)
  elif z in ['dark-academia','natural-history','cartography']:
   o=marker(P,55,58,1,1.4)+P.l(105,21,105,130,b,1)+P.l(120,115,624,115,a,1)+P.l(120,125,408,125,b,.7)
  else:o=marker(P,63,62,1,1.5)+P.p('M120 25Q345 12 630 28M122 117Q373 129 627 115',None,i,1.5)
  return svg(w,h,o)
 # Chapter device: number is a replaceable element, underlying silhouette differs.
 w,h=320,220;no=str(P.S['no']).zfill(2)
 if z in ['bauhaus','swiss','blueprint','neo-brutalism']:
  o=marker(P,51,53,1,1.8)+P.t(111,153,no,95,i,'Arial')+P.l(27,188,291,188,a,5)
 elif z in ['art-deco','celestial-atlas','retrofuturism']:
  o=marker(P,161,49,1,1.6)+P.p('M57 187V105Q160 68 264 105V187',None,a,1.4)+P.t(112,172,no,76,i)
 elif z in ['dunhuang','dark-academia','cartography','natural-history']:
  o=marker(P,53,112,1,2)+P.l(110,28,110,190,b,1.1)+P.t(135,145,no,82,i)+P.l(136,173,284,173,a,2)
 else:o=marker(P,74,65,1,2)+P.t(131,161,no,88,i)+P.p('M26 189Q156 202 291 183',None,a,2)
 return svg(w,h,o)

def make():
 for S in STYLES:
  z=S['id'];P=Pen(S);rows=[]
  for kind,title in [('title-frame','标题框'),('caption-frame','图注框'),('chapter','章节编号')]:
   r=item(z,'ornaments','info-'+kind,title+' · V2构图','可编辑信息装饰；文字放入留白区，章节号可替换。',0,kind,family=kind,credit='upgrade')
   write(outfile(z,r),legacy(P,kind));rows.append(r)
  save_batch(z,'information-revision',rows)
  meta=ROOT/f'STYLES/{z}/v2-records/borders.json';bs=json.loads(meta.read_text(encoding='utf8'))
  for r in bs:
   if r['role']=='frame':
    no=int(Path(r['file']).stem.rsplit('-',1)[1])-1
    r['asset_name']=S['zh']+' · '+['双角标记框','页眉分区框','侧栏档案框'][no]
    r['intended_usage']=['对角标记围合完整画面，中心透明。','独立页眉区与主体画面框，中心透明。','侧栏目录与右下档案签独立分区，中心透明。'][no]
  save_batch(z,'borders',bs)
  for j in range(3):write(ROOT/f'STYLES/{z}/ornaments/v2-frame-{j+1}.svg',open_frame(P,j))
  for j in [2,3,4]:write(ROOT/f'STYLES/{z}/ornaments/v2-rule-{j+1}.svg',rule(P,j))
 report()
if __name__=='__main__':make()
