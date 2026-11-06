"""组件主体补绘：保留 V1 原件，八类常用布局和工具栏按同家族升级。"""
from v2_ui_themes import frame,figure,badge
from v2_plates import *
from primitives import texton

KINDS=['button','card','list','navbar','sidebar','tag','tooltip','empty']
TITLES=['操作按钮','图版卡片','作品列表','页眉导航','目录侧栏','分类标签','详情提示','空结果']
DIMS=[(380,110),(560,390),(580,330),(820,130),(320,440),(300,110),(410,150),(560,330)]

def boundary(P,w,h):
 z=P.S['id'];i=P.i;a=P.a;b=P.b;bg=P.bg
 if z=='swiss':return P.r(0,0,w,h,bg,'none')+P.r(0,0,8,h,a,'none')+P.l(18,h-12,w-12,h-12,i,2)
 if z=='editorial':return P.r(0,0,w,h,bg,'none')+P.l(8,12,w-8,12,i,1.2)+P.l(8,h-12,w-8,h-12,b,.8)
 if z=='blueprint':return P.r(0,0,w,h,bg,'none')+P.p(f'M6 30V6H30M{w-30} 6H{w-6}V30M6 {h-30}V{h-6}H30M{w-30} {h-6}H{w-6}V{h-30}',None,i,2)+P.l(16,h-17,w-16,h-17,b,.6)
 return frame(P,w,h)

def marker(P,x,y,n=1,k=1):
 z=P.S['id'];i=P.i;a=P.a;b=P.b;c=P.c;bg=P.bg
 if z=='bauhaus':s=P.o(0,0,12,b,'none')+P.r(-17,8,34,8,a,'none')
 elif z=='art-deco':s=P.p('M-18 9L0 -16L18 9M-12 12L0 -5L12 12',None,a,2)
 elif z=='swiss':s=P.r(-16,-16,32,32,a,'none')+P.t(-10,7,str(n).zfill(2),15,texton(a),'Arial')
 elif z=='neo-brutalism':s=P.p('M-19 -13L13 -16L19 12L-15 17Z',c,i,3)+P.p('M-9 0H10M4 -7L11 0L4 7',None,i,2)
 elif z=='memphis':s=P.p('M-20 6Q-12 -21 -3 0T17 -4',None,a,5)+P.o(15,12,5,b,'none')
 elif z=='editorial':s=P.t(-13,12,str(n).zfill(2),35,i,'Georgia')
 elif z=='wabi-sabi':s=P.p('M-18 5Q-10 -9 -1 -5Q6 -13 13 2L19 8Q0 14 -18 5Z',b,'none')+P.l(-8,4,4,-2,i,1)
 elif z=='dark-academia':s=book(P,-16,-14,32,26,bg)
 elif z=='celestial-atlas':s=P.o(0,0,17,None,b,.8)+P.l(-22,0,22,0,b,.7)+star(0,0,12,3,5,a)
 elif z=='dunhuang':s=place(cell(P.S),-30,-17,.8)
 elif z=='cartography':s=star(0,0,18,4,4,a)+P.o(0,0,12,None,i,.7)
 elif z=='natural-history':s=leaf(0,12,.8,-10,a,i)
 elif z=='retrofuturism':s=P.e(0,0,22,8,None,b,2)+P.o(0,0,12,a,'none')+P.o(17,-10,4,c,'none')
 elif z=='cyberpunk':s=P.p('M-22 12H-9L2 -4H17V-13M-20 18H-5L6 2H21',None,a,3)
 elif z=='blueprint':s=P.r(-13,-13,26,26,None,i,1)+P.o(0,0,8,None,b,1)+P.l(-21,0,21,0,a,.7)+P.l(0,-21,0,21,a,.7)
 else:s=''.join(P.p(f'M-20 {j*4-7}Q-5 {-25+j*6} 4 {j*4-4}T22 {j*4-2}',None,a if j%2 else i,1.5)for j in range(4))
 return place(s,x,y,k)

def capsule(P,x,y,w,h):
 z=P.S['id'];i=P.i;a=P.a;b=P.b;c=P.c;bg=P.bg
 if z=='bauhaus':s=P.r(0,0,w-25,h,a,'none')+P.o(w-25,h/2,h/2,b,'none')+P.p(f'M{w-36} {h/2}H{w-16}M{w-23} {h/2-7}L{w-16} {h/2}L{w-23} {h/2+7}',None,bg,2);ink=texton(a)
 elif z=='art-deco':s=P.p(f'M0 {h/2}L20 0H{w-20}L{w} {h/2}L{w-20} {h}H20Z',bg,a,2)+P.l(27,7,w-27,7,b,1)+P.l(27,h-7,w-27,h-7,b,1);ink=i
 elif z=='swiss':s=P.r(0,0,w,h,i,'none')+P.r(0,0,13,h,a,'none');ink=bg
 elif z=='neo-brutalism':s=P.r(6,7,w,h,i,'none')+P.r(0,0,w,h,c,i,3);ink=i
 elif z=='memphis':s=P.p(f'M0 8Q{w*.25} -6 {w*.5} 6T{w} 5V{h-4}Q{w*.75} {h+8} {w*.5} {h-3}T0 {h-2}Z',b,i,2);ink=texton(b)
 elif z=='editorial':s=P.l(0,h-4,w,h-4,i,1.3)+P.p(f'M{w-24} 10l21 14l-21 14M{w-70} 24H{w-5}',None,a,1.4);ink=i
 elif z=='wabi-sabi':s=P.p(f'M2 {h-12}Q{w*.35} {h+2} {w-4} {h-9}',None,a,3)+P.o(w-10,12,3,b,'none');ink=i
 elif z=='dark-academia':s=P.r(0,0,w,h,bg,a,1)+P.r(5,5,9,h-10,a,'none')+P.r(20,5,w-25,h-10,None,b,.7);ink=i
 elif z=='celestial-atlas':s=P.p(f'M0 {h}V{h/2}Q0 0 {h/2} 0H{w-h/2}Q{w} 0 {w} {h/2}V{h}',None,a,1.4)+P.l(15,h,w-15,h,b,.8);ink=i
 elif z=='dunhuang':s=P.p(f'M0 {h}V18Q7 5 22 10Q{w/2} -7 {w-22} 10Q{w-7} 5 {w} 18V{h}Z',bg,a,2)+P.l(12,h-6,w-12,h-6,b,.8);ink=i
 elif z=='cartography':s=P.p(f'M0 0H{w-20}L{w} {h/2}L{w-20} {h}H0L14 {h/2}Z',bg,i,1.3)+P.l(24,h-7,w-25,h-7,b,.8);ink=i
 elif z=='natural-history':s=P.p(f'M0 0H{w}V{h/2-5}q-11 5 0 10V{h}H0V{h/2+5}q11 -5 0 -10Z',bg,b,1.5)+P.l(20,6,20,h-6,a,1);ink=i
 elif z=='retrofuturism':s=P.r(0,0,w,h,a,i,1,h/2)+P.r(w-50,6,40,h-12,bg,'none',1,(h-12)/2)+P.o(w-30,h/2,8,b,'none');ink=texton(a)
 elif z=='cyberpunk':s=P.p(f'M0 15L15 0H{w}V{h-15}L{w-15} {h}H0Z',a,'none')+P.r(w-28,7,5,h-14,bg,'none')+P.r(w-18,7,3,h-14,bg,'none');ink=texton(a)
 elif z=='blueprint':s=P.p(f'M9 0H0V{h}H9M{w-9} 0H{w}V{h}H{w-9}',None,i,2)+P.r(9,5,w-18,h-10,None,b,.8)+P.o(w-20,h/2,4,None,a,1);ink=i
 else:s=P.p(f'M0 {h/2}Q8 0 30 4H{w-22}Q{w+7} 15 {w-3} {h-8}Q{w-15} {h+5} {w-32} {h-3}H22Q-4 {h+3} 0 {h/2}Z',bg,a,1.4)+''.join(P.p(f'M{9+j*4} {h-9}q-7 {-h/2} 6 {-h+18}',None,b,.7)for j in range(3));ink=i
 return place(s,x,y),ink

def make_ui(P,kind,w,h):
 z=P.S['id'];i=P.i;a=P.a;b=P.b;c=P.c;bg=P.bg;no=P.S['no']
 tx=lambda x,y,t,sz=16,col=None:P.t(x,y,t,sz,col or i,'SimSun'if z in ['editorial','wabi-sabi','dark-academia','dunhuang','natural-history']else 'SimHei')
 if kind=='button':
  o=P.r(0,0,w,h,bg,'none');s,ink=capsule(P,23,28,w-50,54)
  return o+s+tx(51,63,'添加到图册',20,ink)
 if kind=='tag':
  o=P.r(0,0,w,h,bg,'none');s,ink=capsule(P,20,25,w-40,56)
  return o+s+tx(48,62,'纹理 / 16',18,ink)
 o=boundary(P,w,h)
 if kind=='card':
  # Actual motif and distinct frame orientation, with a readable metadata area.
  if z in ['bauhaus','swiss','neo-brutalism','cyberpunk']:
   o+=P.r(26,28,210,244,b,'none')+figure(P,35,63,190)+tx(264,76,'构成图版',30)+tx(266,113,'独立矢量 / 01',15)+P.l(265,140,w-30,140,a,3)+tx(265,178,'形式、色彩与结构',17)+tx(265,211,'SVG · 可编辑',14)
   s,ink=capsule(P,264,257,255,56);return o+s+tx(283,293,'查看图版',18,ink)+tx(28,337,'ARTISAN / '+str(no).zfill(2),17)
  if z in ['art-deco','dunhuang','retrofuturism','celestial-atlas']:
   o+=figure(P,185,28,175)+P.l(65,221,w-65,221,b,1)+tx(42,269,'图版 · '+str(no).zfill(2),30)+tx(44,301,'可编辑原件  /  独立构成',15)+marker(P,w-62,277,1,1.25)+tx(43,352,'查看详细信息',18)
   return o
  if z in ['editorial','dark-academia','natural-history','cartography']:
   o+=tx(34,65,'图版 '+str(no).zfill(2),31)+P.l(32,82,w-30,82,b,.9)+figure(P,36,106,194)+tx(265,147,'材料与形态',26)+tx(265,185,'独立作品 · SVG',16)+tx(265,217,'原件与来源一同保存',14)+P.l(265,248,w-35,248,a,1)+tx(266,278,'查看详情',18)+tx(34,350,'ARCHIVE / '+z.upper(),14)
   return o
  return o+figure(P,35,40,220)+tx(278,103,'形式研究',28)+tx(278,139,'材料 / 图版',16)+marker(P,330,205,1,1.7)+P.l(34,290,w-34,290,b,.8)+tx(38,335,'查看原件',21)+P.t(w-85,340,'01',35,a)
 if kind=='navbar':
  if z in ['swiss','editorial']:
   return o+tx(25,51,'ARTISAN',28)+P.t(w-110,52,'INDEX',14,a,'Arial')+''.join(tx(27+j*250,96,t,16)+P.l(27+j*250,109,130+j*250,109,a if j==0 else b,2 if j==0 else .7)for j,t in enumerate(['图册 / 01','素材 / 02','设置 / 03']))
  if z in ['art-deco','celestial-atlas','dunhuang']:
   o+=marker(P,w/2,38,1,.9)+tx(w/2-48,80,'ARTISAN',18)+P.l(34,53,w/2-82,53,b,.8)+P.l(w/2+82,53,w-34,53,b,.8)
   return o+tx(48,85,'图册',20)+tx(175,85,'素材',20)+tx(w-90,85,'设置',20)
  if z in ['dark-academia','natural-history','cartography']:
   return o+marker(P,55,62,1,1.2)+tx(91,58,'ARTISAN',24)+tx(94,86,'个人图版目录',13)+''.join(tx(350+j*145,72,t,19)+marker(P,369+j*145,99,j+1,.35)for j,t in enumerate(['图册','素材','设置']))
  o+=marker(P,54,60,1,1.2)+tx(91,70,'ARTISAN',24)
  for j,t in enumerate(['图册','素材','设置']):
   if j==0:
    s,ink=capsule(P,345,37,135,52);o+=s+tx(372,71,t,18,ink)
   else:o+=tx(390+j*152,71,t,18)
  return o
 if kind=='sidebar':
  o+=tx(35,58,'工作目录',28)+marker(P,255,49,1,.7)
  # Book chapters, hanging labels, rail stops and archival tabs use distinct motifs.
  labels=['全部作品','我的收藏','最近使用']
  for j,t in enumerate(labels):
   yy=126+j*85
   if z in ['swiss','editorial','blueprint']:
    o+=P.t(33,yy,str(j+1).zfill(2),25,a if j==0 else b,'Arial')+tx(91,yy,t,20)+P.l(33,yy+24,w-31,yy+24,i if j==0 else b,2 if j==0 else .7)
   elif z in ['cartography','celestial-atlas','retrofuturism','generative-art']:
    if j<2:o+=P.l(48,yy+20,48,yy+62,b,1)
    o+=marker(P,48,yy-5,j+1,.72)+tx(93,yy,t,20)+tx(95,yy+25,['112 项','8 项','5 项'][j],13)
   elif z in ['art-deco','dark-academia','dunhuang','natural-history']:
    s,ink=capsule(P,33,yy-31,w-65,58);o+=s+tx(62,yy+6,t,19,ink)
   else:
    o+=marker(P,48,yy-5,j+1,.78)+tx(91,yy,t,20)
    if j==0:o+=P.l(89,yy+20,244,yy+20,a,3)
  return o+P.l(34,365,w-34,365,b,.7)+tx(35,399,'素材库 / 本地',14)
 if kind=='list':
  o+=tx(34,56,'作品目录',27)+marker(P,w-57,43,1,.8)
  for j,t in enumerate(['形式研究','材料样本','出版图版']):
   yy=117+j*76
   if z in ['swiss','editorial','blueprint']:
    o+=P.t(34,yy,str(j+1).zfill(2),30,a,'Arial')+tx(99,yy,t,22)+tx(w-98,yy,['SVG','WEBP','SVG'][j],14)+P.l(34,yy+21,w-35,yy+21,b,.8)
   elif z in ['memphis','neo-brutalism','cyberpunk']:
    s,ink=capsule(P,29,yy-33,w-64,57);o+=s+tx(52,yy+2,t,21,ink)+tx(w-114,yy+2,str(j+1).zfill(2),19,ink)
   elif z in ['dark-academia','natural-history','cartography']:
    o+=marker(P,53,yy-10,j+1,.7)+tx(94,yy-4,t,21)+tx(96,yy+19,['独立构成','原生肌理','编辑图版'][j],13)+tx(w-95,yy,['SVG','WEBP','SVG'][j],13)+P.l(94,yy+30,w-33,yy+30,b,.7)
   else:o+=marker(P,56,yy-9,j+1,.8)+tx(99,yy,t,23)+P.l(99,yy+19,w-35,yy+19,b,1)+P.t(w-71,yy,str(j+1).zfill(2),18,a)
  return o
 if kind=='tooltip':
  # Structural pointer, caption rail or footnote convention differs by style.
  o+=marker(P,49,64,1,.75)+tx(92,58,'打开素材详情',22)+tx(94,88,'查看原件、尺寸和来源',13)
  if z in ['editorial','swiss','blueprint']:o+=P.l(94,106,w-27,106,a,.8)+tx(95,128,'操作提示',11)
  elif z in ['cartography','dark-academia','natural-history']:o+=P.p(f'M{w-70} 112h35l-12 17Z',None,a,1)
  else:o+=P.p(f'M{w/2-11} {h-21}l11 13l11 -13',None,a,1.4)
  return o
 if kind=='empty':
  if z in ['swiss','editorial','blueprint']:
   return o+P.t(30,160,'00',100,a,'Arial')+tx(230,122,'暂无匹配作品',28)+tx(232,163,'调整分类或搜索条件',17)+P.l(231,188,w-30,188,b,1)+tx(233,231,'清除筛选',20)
  if z in ['art-deco','dunhuang','celestial-atlas','retrofuturism']:
   o+=figure(P,40,70,183)+tx(260,115,'暂无匹配作品',26)+tx(261,155,'调整分类或搜索条件',15)
   s,ink=capsule(P,260,203,246,51);return o+s+tx(284,237,'清除筛选',18,ink)
  return o+figure(P,35,47,187)+tx(251,118,'暂无匹配作品',26)+tx(252,155,'调整分类或搜索条件',15)+marker(P,274,209,1,.7)+tx(312,218,'清除筛选',19)

def toolbar(P):
 w,h=820,140;o=boundary(P,w,h)+marker(P,48,65,1,1)
 for j,t in enumerate(['编辑','复制','分享','收藏']):
  x=105+j*176;s,ink=capsule(P,x,39,151,58)
  o+=s+P.t(x+27,77,t,19,ink,'SimHei')
 return svg(w,h,o)

def make():
 for S in STYLES:
  z=S['id'];P=Pen(S);rows=[]
  for kind,title,(w,h) in zip(KINDS,TITLES,DIMS):
   r=item(z,'ui','ui-'+kind,title+' · V2布局','独立可编辑SVG；应用使用语义控件实现交互，不把静态文字当作业务数据。',2,'component',family=kind,credit='upgrade',alpha=False)
   write(outfile(z,r),svg(w,h,make_ui(P,kind,w,h)));rows.append(r)
  save_batch(z,'ui-completion',rows)
  r=item(z,'ui','toolbar','编辑工具栏 · V2布局','同套操作按钮组；编辑、复制、分享、收藏由宿主实现。',1,'toolbar',alpha=False)
  write(outfile(z,r),toolbar(P));save_batch(z,'ui',[r])
 report()
if __name__=='__main__':make()
