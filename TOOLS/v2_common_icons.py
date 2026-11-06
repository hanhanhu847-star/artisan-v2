"""24语义×16种造型语法。保留V1共用线稿，仅将新版本计入合格作品家族。"""
import math,json
from primitives import ICON_NAMES,ICON_ZH,svg,g,write,STYLES
from v2_registry import item,outfile,save_batch,report
from v2_signs import SIGNS
from v2_icon_variants import PATHS
from v2_icon_refinement import REFINEMENTS
for _style,_paths in REFINEMENTS.items():PATHS.setdefault(_style,{}).update(_paths)
NAMES=ICON_NAMES+['edit','delete','copy','share']
LABELS=ICON_ZH+['编辑','删除','复制','分享']
class Draw:
 def __init__(self,S):
  self.S=S;self.z=S['no']-1;self.bg,self.i,self.a,self.b,self.c=S['palette'];self.v=self.z%4
  self.sw=[2,1.2,2.6,2.8,2.4,1.3,1.6,1.25,1.1,1.7,1.2,1.4,2,1.5,1,1.5][self.z]
 def p(self,d,fill='none',stroke=None,w=None):
  return f'<path d="{d}" fill="{fill}" stroke="{stroke or self.i}" stroke-width="{w or self.sw}" stroke-linecap="round" stroke-linejoin="round"/>'
 def l(self,x,y,X,Y,col=None,w=None):
  if self.z==6:return self.p(f'M{x} {y}Q{(x+X)/2+.7:g} {(y+Y)/2-1.3:g} {X} {Y}',stroke=col,w=w)
  if self.z==15:return self.p(f'M{x} {y}Q{(x+X)/2+2:g} {(y+Y)/2-2:g} {X} {Y}',stroke=col,w=w)+self.circ(x,y,.8,self.b,'none')
  return self.p(f'M{x} {y}L{X} {Y}',stroke=col,w=w)
 def r(self,x,y,w,h,fill='none'):
  z=self.z
  if z in [1,7,13]:
   k=3 if z==13 else 1.8
   d=f'M{x+k} {y}H{x+w}V{y+h-k}L{x+w-k} {y+h}H{x}V{y+k}Z'
  elif z in [6,11]:
   d=f'M{x+.8} {y+1}Q{x+w/2} {y-1} {x+w-1} {y+.4}L{x+w} {y+h-1}Q{x+w/2} {y+h+1} {x} {y+h}Z'
  elif z in [4,12,15]:
   k=min(5,w/3,h/3);d=f'M{x+k} {y}H{x+w-k}Q{x+w} {y} {x+w} {y+k}V{y+h-k}Q{x+w} {y+h} {x+w-k} {y+h}H{x+k}Q{x} {y+h} {x} {y+h-k}V{y+k}Q{x} {y} {x+k} {y}Z'
  elif z==9:
   d=f'M{x} {y+2}Q{x+w/2} {y-2} {x+w} {y+2}V{y+h-2}Q{x+w/2} {y+h+2} {x} {y+h-2}Z'
  else:d=f'M{x} {y}H{x+w}V{y+h}H{x}Z'
  out=self.p(d,fill)
  if z==0 and w>12:out+=self.p(f'M{x} {y}H{x+w*.25}V{y+h*.24}H{x}Z',self.a,'none')
  if z==1 and w>13 and h>13:out+=self.p(f'M{x+3} {y+5}V{y+h-3}H{x+w-5}',stroke=self.a,w=.6)
  if z==3:out=self.p(f'M{x+w+2} {y+4}V{y+h+3}H{x+3}',stroke=self.i,w=3)+out
  if z==4 and h>9:out+=self.circ(x+w-2,y+2,2,self.b,'none')
  if z==7 and h>10:out+=self.p(f'M{x+1} {y+6}L{x+6} {y+1}',stroke=self.a,w=.8)
  if z==10 and w>10:out+=self.l(x+3,y+h-3,x+w-3,y+h-3,self.b,.5)
  if z==14 and h>10:out+=self.p(f'M{x-2} {y-2}H{x+w+2}M{x-2} {y-4}V{y}M{x+w+2} {y-4}V{y}',stroke=self.b,w=.6)
  return out
 def circ(self,x,y,r,fill='none',stroke=None):
  z=self.z;st=stroke or self.i
  if z in [0,2]:return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{st}" stroke-width="{self.sw}"/>'
  if z in [1,3,13]:
   n=8 if z!=3 else 6;pts=[(x+r*math.cos(a*math.tau/n),y+r*math.sin(a*math.tau/n))for a in range(n)]
   return self.p('M'+'L'.join(f'{a:g} {b:g}'for a,b in pts)+'Z',fill,st)
  if z in [6,11]:
   return self.p(f'M{x-r} {y}C{x-r-1} {y-r*.6} {x-r*.2} {y-r-1} {x+r*.3} {y-r}S{x+r+1} {y+r*.3} {x+r*.5} {y+r*.8}S{x-r} {y+r} {x-r} {y}Z',fill,st)
  o=f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*(.85 if z==12 else 1)}" fill="{fill}" stroke="{st}" stroke-width="{self.sw}"/>'
  if z==8 and r>5:
   o+=''.join(self.l(x+(r+2)*math.cos(a),y+(r+2)*math.sin(a),x+(r+4)*math.cos(a),y+(r+4)*math.sin(a),self.a,.65)for a in [0,math.pi/2,math.pi,math.pi*1.5])
  if z==9 and r>6:o+=self.p(f'M{x-r+2} {y}Q{x} {y-r} {x+r-2} {y}',stroke=self.a,w=.7)
  if z==15 and r>4:o+=self.p(f'M{x-r} {y}Q{x} {y-r/2} {x+r} {y}',stroke=self.b,w=.6)
  return o
 def fill(self):return self.a if self.z in [0,2,3,4,9,12] else 'none'
def glyph(D,k):
 R,L,C,P=D.r,D.l,D.circ,D.p;v=D.v;f=D.fill();a=D.a;b=D.b;i=D.i
 # 四套语义呈现：正视实体、历史器具、导向符号、层叠系统。每种风格再用独立构造规则绘制。
 if k in ['file','document']:
  if v==0:o=R(10,5,26,36,f)+L(14,13,31,13)+L(14,19,27,19)
  elif v==1:o=P('M12 7Q18 3 24 7T37 7V38Q31 42 24 38T12 38Z')+C(12,8,3,'none')+L(18,15,31,15)+L(18,21,31,21)
  elif v==2:o=R(7,5,22,32,f)+R(14,12,23,31)+L(19,20,31,20)
  else:o=P('M10 5H28L39 16V42H10Z',f)+P('M28 5V16H39')+L(16,24,32,24)
  if k=='document':o+=L(16,29,31,29)+L(16,34,26,34)
  return o
 if k=='folder':
  if v==0:return P('M5 12H18L23 18H42L36 39H5Z',f)+L(5,18,36,18)
  if v==1:return R(7,11,34,30)+R(12,6,13,7,f)+L(12,24,36,24)+R(19,20,10,7)
  if v==2:return R(5,10,37,31,f)+L(5,17,26,17)+R(8,5,15,5)
  return P('M6 10H20L24 15H40V21H11L6 39Z',f)+P('M11 21H44L37 39H6Z')
 if k=='image':
  o=R(6,6,36,34)
  if v==0:return o+P('M8 38L19 18L29 38Z',a)+P('M23 38L34 25L40 38Z',b)+C(33,14,4,a)
  if v==1:return o+P('M10 33Q17 20 24 27T38 26')+C(18,15,4)+L(10,36,38,36)
  if v==2:return o+R(9,9,15,25,f)+C(33,15,5,a)+P('M26 32L32 24L39 32Z',i)
  return o+P('M10 35L19 23L27 30L34 19L39 27')+C(15,15,3,a)
 if k=='video':
  if v==0:return R(5,12,27,25,f)+P('M32 20L43 14V35L32 29Z',b)
  if v==1:return C(14,12,7)+C(32,12,7)+R(8,21,30,18)+P('M21 24L29 29L21 34Z',a)
  if v==2:return R(5,6,37,36)+''.join(R(x,y,3,3,a)for y in [8,36]for x in [8,18,28,37])+P('M18 17L31 24L18 31Z',i)
  return P('M6 13L40 5L43 15L8 23Z',a)+R(8,23,35,17)+P('M19 27L29 31L19 36Z',b)
 if k=='audio':
  if v==0:return R(7,18,8,13,f)+P('M15 18L29 7V42L15 31Z',b)+P('M34 15Q44 24 34 33')
  if v==1:return P('M6 28Q6 5 24 5Q42 5 42 28')+R(5,25,9,16,f)+R(34,25,9,16,f)
  if v==2:return ''.join(R(5+j*8,24-h/2,4,h,f)for j,h in enumerate([10,25,38,21,13]))
  return L(18,34,18,10)+L(18,10,37,6)+L(37,6,37,29)+C(12,35,6,f)+C(31,30,6,f)
 if k=='search':
  if v in [0,1]:return C(20,19,13,f if v==0 else 'none')+L(30,29,42,41)+L(13,19,27,19,a,.8)
  if v==2:return P('M5 17V6H17M31 6H42V17M42 31V42H31M17 42H5V31')+C(24,24,8)+L(20,24,28,24)
  return C(23,21,15)+C(23,21,9)+P('M8 34L5 43H16')+L(26,18,31,13,a)
 if k=='favorite':
  if v==0:return P('M24 5L30 17L43 19L34 28L37 42L24 35L11 42L14 28L5 19L18 17Z',f)
  if v==1:return P('M12 6H36V42L24 32L12 42Z',f)+C(24,17,5)
  if v==2:return P('M24 40C-6 20 5 1 19 13L24 18L29 13C43 1 54 20 24 40Z',f)
  return C(24,24,17)+''.join(C(24+8*math.cos(j*math.tau/5),24+8*math.sin(j*math.tau/5),5,'none')for j in range(5))+C(24,24,3,a)
 if k in ['download','upload']:
  up=k=='upload';yy=9 if up else 32;yt=32 if up else 9;d=1 if up else -1
  o=L(24,yt,24,yy)+P(f'M{16 if v<2 else 13} {yy+d*8}L24 {yy}L{32 if v<2 else 35} {yy+d*8}',a if v==2 else 'none')
  if v==0:o+=R(6,35,36,7,f)
  elif v==1:o+=P('M6 29V41H42V29')+C(10,37,1,a)
  elif v==2:o+=L(7,40,41,40)+R(5,35,5,5,f)+R(38,35,5,5,f)
  else:o+=P('M6 34L12 43H36L42 34')+L(12,38,36,38,b,.8)
  return o
 if k=='settings':
  if v in [0,2]:
   return ''.join(L(8,y,40,y)+R(x,y-4,7,8,f)for y,x in [(11,13),(24,29),(37,18)])
  if v==1:return C(24,24,14)+C(24,24,6)+''.join(L(24+16*math.cos(j*math.pi/4),24+16*math.sin(j*math.pi/4),24+20*math.cos(j*math.pi/4),24+20*math.sin(j*math.pi/4),a,3)for j in range(8))
  return R(5,5,38,38)+C(24,24,12)+L(24,24,29,16,a)+L(10,39,17,39,b)
 if k=='user':
  if v==0:return C(24,13,8,f)+P('M6 42L13 27H35L42 42Z',b)
  if v==1:return C(24,14,8)+P('M8 40Q10 27 24 27Q38 27 40 40Z')+P('M18 29L24 35L30 29')
  if v==2:return C(17,15,7,f)+P('M4 40Q5 27 17 27Q29 27 30 40Z',f)+C(35,17,5)+P('M32 29Q43 27 44 40')
  return C(24,24,19)+C(24,17,6)+P('M11 37Q24 17 37 37')
 if k=='map':
  if v==0:return P('M5 11L18 6L30 12L43 6V36L30 42L18 36L5 42Z',f)+L(18,6,18,36)+L(30,12,30,42)
  if v==1:return R(6,6,36,36)+P('M9 30Q16 13 25 24T39 17')+P('M13 16L17 9L20 16Z',a)+L(9,38,21,38)
  if v==2:return P('M24 43C24 43 8 27 8 17A16 16 0 0 1 40 17C40 27 24 43 24 43Z',f)+C(24,17,6,D.bg)
  return C(24,24,18)+P('M24 8L31 30L24 26L17 30Z',a)+L(24,27,24,38)
 if k=='time':
  if v==0:return C(24,24,18)+P('M24 11V24H35')+R(21,3,6,4,a)
  if v==1:return P('M10 6H38M10 42H38M13 7Q13 18 24 24Q35 30 35 41M35 7Q35 18 24 24Q13 30 13 41')+P('M17 39L24 30L31 39Z',a)
  if v==2:return R(5,11,38,27)+R(10,17,10,15,f)+R(28,17,10,15,f)+C(24,21,1,a)+C(24,28,1,a)
  return C(24,26,16)+R(19,3,10,5,f)+L(24,10,24,24)+L(24,26,34,26)+L(37,12,41,8)
 if k=='statistics':
  if v==0:return R(7,25,9,16,f)+R(20,15,9,26,b)+R(33,5,9,36,a)
  if v==1:return L(6,6,6,41)+L(6,41,43,41)+P('M10 33L20 21L29 26L40 12')+''.join(C(x,y,2,a)for x,y in [(10,33),(20,21),(29,26),(40,12)])
  if v==2:return C(24,24,18)+P('M24 6V24H42',f)+L(24,24,11,37)
  return R(5,6,38,35)+P('M10 31Q16 35 23 22T39 16')+L(10,36,39,36,b)
 if k=='database':
  if v==0:return ''.join(R(6,y,36,9,f)+C(36,y+4,1,D.bg)for y in [6,20,34])
  if v==1:return ''.join(R(6,y,36,11)+R(19,y+4,10,3,a)for y in [5,18,31])
  if v==2:return P('M6 12C6 2 42 2 42 12V37C42 46 6 46 6 37Z',f)+P('M6 12C6 22 42 22 42 12M6 25C6 35 42 35 42 25')
  return ''.join(P(f'M6 {y}L24 {y-6}L42 {y}L24 {y+6}Z')for y in [11,24,37])
 if k=='network':
  if v==0:return L(24,9,24,25)+L(9,25,39,25)+L(9,25,9,35)+L(39,25,39,35)+R(18,4,12,10,f)+R(3,35,12,9,b)+R(33,35,12,9,a)
  if v==1:return C(24,24,19)+P('M24 5Q5 24 24 43Q43 24 24 5M7 16H41M7 32H41')+L(24,5,24,43)
  if v==2:return ''.join(L(24,24,x,y)+C(x,y,5,f)for x,y in [(9,9),(39,9),(39,39),(9,39)])+C(24,24,7,D.bg)
  return C(24,37,3,a)+P('M16 29Q24 20 32 29M9 22Q24 7 39 22M4 15Q24-4 44 15')
 if k=='security':
  if v==0:return P('M24 5L41 11V23Q41 34 24 43Q7 34 7 23V11Z',f)+P('M15 23L22 30L33 17')
  if v==1:return R(10,20,28,23)+P('M16 20V13Q16 1 24 5Q32 3 32 13V20')+C(24,29,3,a)+L(24,32,24,36)
  if v==2:return C(14,18,9,f)+L(23,18,43,18)+L(34,18,34,26)+L(41,18,41,23)
  return P('M8 8H39V26L24 43L8 26Z')+R(17,18,14,12,f)+P('M20 18V13Q24 6 28 13V18')
 if k=='device':
  if v==0:return R(5,6,38,27)+L(24,33,24,42)+L(14,43,34,43)
  if v==1:return R(8,5,32,32)+R(12,9,24,20)+P('M8 37L4 43H44L40 37Z',a)
  if v==2:return R(12,4,24,40)+L(18,9,30,9)+C(24,38,2,f)
  return R(4,9,29,27)+R(30,19,13,25)+L(16,36,16,42)+L(8,42,24,42)
 if k=='task-status':
  if v==0:return R(8,8,33,35)+R(16,4,17,8,f)+P('M15 26L22 33L35 18')
  if v==1:return ''.join(C(10,y,3,a)+L(18,y,40,y)for y in [11,24,37])
  if v==2:return ''.join(R(5,y-4,8,8,f)+L(19,y,42,y)for y in [10,24,38])+P('M5 23L8 27L15 18')
  return C(24,24,19)+P('M13 24L21 32L35 15')
 if k=='edit':
  if v==0:return P('M8 33L31 7L40 16L17 41L6 43Z',f)+L(10,32,18,39)
  if v==1:return P('M24 5L38 24L24 42L10 24Z')+L(24,5,24,29)+C(24,30,3,a)
  if v==2:return R(5,9,28,34)+P('M16 30L35 10L41 16L22 36L15 37Z',a)
  return P('M7 34Q13 28 21 31L35 7L41 11L27 37Q13 46 7 34Z',f)+L(21,31,27,37)
 if k=='delete':
  if v==0:return R(11,15,27,28)+R(6,9,37,5,f)+R(18,4,14,5)+L(19,21,19,36)+L(29,21,29,36)
  if v==1:return P('M8 13H40M12 15L16 42H33L37 15M18 7H30V13')+L(20,21,22,36)+L(29,21,27,36)
  if v==2:return R(7,7,34,34,f)+P('M15 15L33 33M33 15L15 33',stroke=D.i if f=='none' else D.bg)
  return P('M6 17L25 4L43 28L25 41H16Z',f)+L(14,13,34,36)+L(24,43,43,43)
 if k=='copy':
  if v==0:return R(5,5,26,30,b)+R(17,17,26,26,f)
  if v==1:return R(5,11,23,31)+R(20,5,23,31)+L(26,12,38,12)+L(26,18,38,18)
  if v==2:return P('M5 14L24 4L43 14L24 24Z',f)+P('M5 25L24 35L43 25M5 35L24 45L43 35')
  return R(5,6,25,29)+R(16,18,25,25)+P('M12 36H8V31M35 8H41V14',stroke=a)
 if k=='share':
  if v==0:return L(12,24,36,10)+L(12,24,36,38)+C(12,24,7,f)+C(36,10,6,b)+C(36,38,6,a)
  if v==1:return R(5,21,30,22)+P('M17 31V15H39M31 7L39 15L31 23',stroke=a)
  if v==2:return P('M4 22L43 4L32 43L23 29Z',f)+L(23,29,43,4)
  return C(24,24,6)+''.join(L(24,24,x,y)+R(x-4,y-4,8,8,f)for x,y in [(8,9),(40,9),(24,40)])
 raise ValueError(k)
def make():
 for S in STYLES:
  z=S['id'];D=Draw(S);rows=[]
  for k,label in zip(NAMES,LABELS):
   r=item(z,'icons',k,label+' · V2构型','64×64，核心48单位；保持造型语法，不依赖全套外框来区分风格。',0,'common-glyph',family=k if k in ICON_NAMES else 'v2-'+k,credit='upgrade' if k in ICON_NAMES else 'new')
   body=D.p(PATHS[z][k]) if k in PATHS.get(z,{}) else glyph(D,k)
   write(outfile(z,r),svg(64,64,g(body,'translate(8 8)')));rows.append(r)
  special=json.loads((ROOT/'STYLES'/z/'v2-records/icons.json').read_text(encoding='utf8'))
  for key,title,d in SIGNS[z]:
   write(ROOT/'STYLES'/z/'icons'/('v2-'+key+'.svg'),svg(64,64,g(D.p(d),'translate(8 8)')))
  save_batch(z,'icons',rows+[r for r in special if r['role']=='special-glyph'])
 report()
if __name__=='__main__':
 from styles_data import ROOT
 make()
