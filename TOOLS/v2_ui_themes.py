"""其余13套六类UI的版式与材质边界；以独立矢量样例交付，不模拟应用功能。"""
from v2_plates import *
from primitives import texton
def frame(P,w,h):
 z=P.S['id'];i=P.i;a=P.a;b=P.b;c=P.c;bg=P.bg
 o=P.r(0,0,w,h,bg,'none')
 if z=='bauhaus':return o+P.r(0,0,12,h,i,'none')+P.r(12,0,w-12,7,a,'none')+P.o(w-18,18,10,c,'none')
 if z=='art-deco':
  return o+P.p(f'M6 29L29 6H{w-29}L{w-6} 29V{h-29}L{w-29} {h-6}H29L6 {h-29}Z',None,a,2)+P.p(f'M17 38L38 17H{w-38}L{w-17} 38V{h-38}L{w-38} {h-17}H38L17 {h-38}Z',None,b,.8)
 if z=='neo-brutalism':return P.r(10,12,w-12,h-14,i,'none')+P.r(3,3,w-15,h-15,bg,i,4)+P.r(w-56,3,44,18,c,i,3)+P.o(16,h-23,3,i,'none')
 if z=='memphis':return o+P.p(f'M6 {h-22}V28Q4 4 28 8H{w-34}Q{w-5} 3 {w-8} 30V{h-33}Q{w-5} {h-6} {w-31} {h-8}H31Q4 {h-5} 6 {h-22}Z',None,i,2.3)+P.p(f'M30 {h-9}q8 -17 16 0t16 0t16 0',None,a,4)+P.o(w-24,22,8,c,i,1.5)
 if z=='wabi-sabi':return o+P.p(f'M9 15Q{w*.3} 7 {w*.58} 13T{w-8} 12L{w-11} {h-14}Q{w*.6} {h-8} {w*.3} {h-15}T12 {h-11}Z',None,b,1.5)+leaf(w-40,33,.32,-18,a,i)
 if z=='dark-academia':return o+P.r(6,6,w-12,h-12,None,a,1)+P.r(16,16,9,h-32,a,'none')+P.r(25,16,w-41,h-32,None,b,.65)+P.p(f'M{w-63} 7H{w-24}V24L{w-43} 18L{w-63} 24Z',c,'none')
 if z=='celestial-atlas':return o+P.p(f'M8 41V8H{w-41}M{w-8} 41V{h-8}H41M8 {h-41}V{h-8}H41',None,a,1.2)+P.p(f'M{w-64} 8A56 56 0 0 1 {w-8} 64M{w-45} 8A37 37 0 0 1 {w-8} 45',None,b,.8)+star(w-31,31,11,3,5,a)
 if z=='dunhuang':return o+P.p(f'M8 30L30 8H{w-30}L{w-8} 30V{h-30}L{w-30} {h-8}H30L8 {h-30}Z',c,a,1.3)+P.r(20,20,w-40,h-40,bg,b,1)+place(cell(P.S),w-92,9,.82)
 if z=='cartography':return o+P.r(8,8,w-16,h-16,None,i,1.5)+P.r(18,18,w-36,h-36,None,b,.7)+''.join(P.l(26+k*20,8,26+k*20,14,a,.9)for k in range(int((w-48)/20)))+''.join(P.l(8,28+k*20,14,28+k*20,a,.9)for k in range(int((h-48)/20)))
 if z=='natural-history':return o+P.p(f'M10 10H{w-10}V{h-10}H10Z',None,b,1)+P.l(22,22,22,h-22,a,2)+P.r(w-66,8,47,13,c,'none')+P.l(w-60,14,w-27,14,i,.6)
 if z=='retrofuturism':return o+P.r(8,8,w-16,h-16,None,a,2.8,28)+P.r(16,16,w-32,h-32,None,b,.9,22)+P.r(w-102,9,66,10,c,'none',1,5)+P.o(22,h-29,3,c,'none')
 if z=='cyberpunk':return o+P.p(f'M6 29L29 6H{w-8}V{h-30}L{w-30} {h-8}H6Z',None,a,1.8)+P.p(f'M6 36H12V{h-23}H{w-46}M{w-21} 26H{w-35}L{w-44} 35',None,b,2.5)+P.r(32,7,49,5,c,'none')
 # flow-field frame: curved side trajectories, clear central content region.
 return o+P.p(f'M15 {h-13}Q2 {h*.7} 16 {h*.44}T15 13H{w-19}Q{w+1} {h*.42} {w-17} {h*.7}T{w-18} {h-13}Z',None,b,1.3)+''.join(P.p(f'M{27+k*4} {h-17}Q{8+k*7} {h*.6} {28+k*4} 18',None,a,.75)for k in range(3))
def figure(P,x,y,size):
 return place(motif(P.S,(P.S['no']+1)%3),x,y,size/300)
def badge(P,x,y,w,h,label):
 return P.r(x,y,w,h,P.a,'none',1,6 if P.S['id']in ['memphis','retrofuturism']else 0)+P.t(x+14,y+h*.66,label,15,texton(P.a),'SimHei')
def gauge(P,x,y,w,h):
 z=P.S['id'];a=P.a;b=P.b;c=P.c;i=P.i;bg=P.bg
 if z=='bauhaus':return P.r(x,y,w*.64,h,a,'none')+P.r(x+w*.64,y,w*.36,h,b,'none')+P.o(x+w*.64,y+h/2,h*.8,c,i,1)
 if z=='art-deco':
  return ''.join(P.p(f'M{x+k*w/16} {y+h}l{w/32} {-h}l{w/32} {h}Z',a if k<10 else bg,b,.8)for k in range(16))
 if z=='neo-brutalism':return P.r(x+4,y+5,w,h,i,'none')+P.r(x,y,w,h,c,i,3)+''.join(P.p(f'M{x+5+k*22} {y+2}l10 0l-9 {h-4}h-10Z',i,'none')for k in range(int(w*.64/22)))
 if z=='memphis':return ''.join(P.o(x+12+k*(w-24)/11,y+h/2,8 if k%2 else 11,[a,b,c][k%3]if k<8 else bg,i,1.6)for k in range(12))
 if z=='wabi-sabi':return P.p(f'M{x} {y+h/2}Q{x+w*.3} {y-2} {x+w*.65} {y+h*.6}T{x+w} {y+h/2}',None,b,3)+P.p(f'M{x} {y+h/2}Q{x+w*.3} {y-2} {x+w*.64} {y+h*.6}',None,a,6)
 if z=='dark-academia':return ''.join(P.r(x+k*w/20,y,w/20-3,h,a if k<13 else bg,b,1)+P.l(x+k*w/20+3,y+4,x+k*w/20+3,y+h-4,c,.6)for k in range(20))
 if z=='celestial-atlas':
  return P.l(x,y+h/2,x+w,y+h/2,b,1)+''.join(P.l(x+k*w/25,y+2 if k%5==0 else y+9,x+k*w/25,y+h-2,a,.8)for k in range(26))+P.p(f'M{x+w*.64-6} {y-3}h12l-6 10Z',a,'none')
 if z=='dunhuang':return ''.join(place(cell(P.S),x+k*w/8,y-1,w/8/86)for k in range(8))+P.l(x,y+h+3,x+w*.64,y+h+3,a,3)
 if z=='cartography':
  return ''.join(P.r(x+k*w/10,y,w/10,h,i if k%2==0 else bg,i,1)for k in range(10))+P.p(f'M{x+w*.64} {y-9}v{h+18}',None,a,2.5)+P.o(x+w*.64,y-9,3,a,'none')
 if z=='natural-history':return P.l(x,y+h*.75,x+w,y+h*.75,i,1)+''.join(leaf(x+14+k*w/9,y+h*.6,.32,25,a if k<6 else c,i)for k in range(9))
 if z=='retrofuturism':return P.r(x,y,w,h,bg,b,1.5,h/2)+P.r(x+4,y+4,(w-8)*.64,h-8,a,'none',1,(h-8)/2)+P.l(x+w*.64,y-4,x+w*.64,y+h+4,c,2)
 if z=='cyberpunk':return ''.join(P.p(f'M{x+k*w/20} {y+h}l8 {-h}h{w/20-12}l-8 {h}Z',a if k<13 else b,'none')for k in range(20))+P.l(x,y+h+6,x+w,y+h+6,b,1)
 return ''.join(P.o(x+(k+.5)*w/28,y+h/2+math.sin(k*.32)*h*.24,2.2+(k%3),a if k<18 else b,'none')for k in range(28))
def theme_ui(P,kind,w,h):
 z=P.S['id'];i=P.i;a=P.a;b=P.b;bg=P.bg;no=P.S['no'];o=frame(P,w,h)
 tx=lambda x,y,s,sz=16:P.t(x,y,s,sz,i,'SimSun'if z in ['wabi-sabi','dark-academia','dunhuang','cartography','natural-history']else 'SimHei')
 # 13套独立主体，按读写任务分配艺术区，确保文本不压在母题上。
 if kind=='input':
  if z in ['bauhaus','neo-brutalism','cyberpunk']:
   return o+tx(27,45,'作品名称',14)+P.r(26,61,w-54,51,None,b,1)+tx(42,94,'构成研究 01',22)+P.l(w-50,76,w-50,101,a,2)+P.l(26,116,w*.64,116,a,2)
  if z in ['wabi-sabi','natural-history','dunhuang']:
   return o+figure(P,25,27,79)+tx(124,49,'作品名称',13)+tx(124,87,'无题 · 图版一',23)+P.l(124,103,w-36,103,a,1.2)
  if z in ['art-deco','dark-academia','cartography']:
   return o+tx(38,45,'作品名称',13)+P.l(38,56,w-38,56,b,.8)+tx(39,91,'档案研究 01',23)+P.r(w-87,66,43,35,None,a,.8)+P.t(w-76,89,'01',15,a,'monospace')
  return o+tx(31,49,'作品',14)+P.r(94,30,w-129,76,None,b,1.2,16 if z=='retrofuturism'else 5)+tx(112,75,'无题研究 01',23)+P.l(114,92,w-61,92,a,1)
 if kind=='table':
  side=z in ['bauhaus','dark-academia','celestial-atlas','natural-history','retrofuturism']
  if side:
   o+=figure(P,30,74,121)+tx(31,54,'图版目录',19)+tx(42,h-45,'03 项',13)+P.l(165,30,165,h-30,b,.8);left=187;top=64;right=w-31;cols=[left,left+47,right-60]
  else:
   o+=tx(32,58,'素材目录',29)+place(cell(P.S),w-131,29,1.04)+P.l(32,78,w-32,78,a,1.4);left=32;top=112;right=w-32;cols=[left,left+85,right-75]
  for row,labels in enumerate([['编号','作品名称','格式'],['01','构成练习','SVG'],['02','纹理样本','WEBP'],['03','装饰图版','SVG']]):
   yy=top+row*47
   if z in ['neo-brutalism','memphis','cyberpunk']and row%2:o+=P.r(left-5,yy-23,right-left+9,39,P.c if z=='neo-brutalism'else bg,b,.6)
   for xx,lab in zip(cols,labels):o+=tx(xx,yy,lab,13 if row==0 else 16)
   o+=P.l(left,yy+15,right,yy+15,b,.7)
  return o
 if kind=='progress':
  if z in ['celestial-atlas','cartography','retrofuturism']:
   o+=P.o(69,84,37,None,b,1.2)+P.p('M69 47A37 37 0 1 1 40.5 107.6',None,a,3)+P.t(48,91,'64',25,i,'monospace')+tx(124,73,'正在导出',25)+tx(124,103,'16 / 25 项素材',14)
   return o+gauge(P,36,139,w-72,18)
  if z in ['dunhuang','natural-history','wabi-sabi']:
   return o+figure(P,28,29,88)+tx(143,67,'导出图版',25)+tx(143,99,'已完成 64%',16)+gauge(P,39,136,w-78,21)
  return o+tx(32,54,'导出素材',25)+P.t(w-99,59,'64%',31,i,'monospace')+gauge(P,32,84,w-64,32)+tx(34,155,'16 / 25 项  ·  正在写入清单',14)
 if kind=='dialog':
  if z in ['art-deco','dunhuang','dark-academia','natural-history']:
   return o+figure(P,30,70,140)+P.l(185,42,185,h-42,b,.8)+tx(214,72,'加入图册',28)+tx(214,113,'已选择 3 项素材。',16)+tx(214,141,'文件与来源将一同保存。',15)+P.l(214,163,w-33,163,b,.8)+badge(P,214,197,209,43,'确认添加')+tx(215,274,'取消',16)
  if z in ['bauhaus','memphis','retrofuturism','generative-art']:
   return o+tx(33,65,'加入图册',32)+place(cell(P.S),w-135,36,1.15)+P.l(33,91,w-33,91,b,1)+tx(34,132,'保留文件、相对路径和来源。',18)+tx(34,166,'本次选择 03 项',15)+badge(P,33,213,192,48,'确认添加')+tx(258,243,'取消',17)
  return o+P.r(30,31,w-60,51,bg,a,1.4)+tx(46,65,'加入图册',27)+tx(32,125,'文件与来源信息将一同保存。',18)+tx(32,160,'已选择 3 项素材。',16)+P.l(32,186,w-32,186,b,1)+badge(P,w-220,221,184,47,'确认添加')+tx(w-290,250,'取消',16)
 if kind=='error':
  if z in ['wabi-sabi','natural-history','dark-academia','cartography']:
   return o+figure(P,25,45,95)+tx(144,65,'文件未找到',26)+tx(144,99,'检查素材相对路径。',16)+P.l(144,121,w-38,121,b,.7)+tx(145,153,'重新读取',16)
  if z in ['celestial-atlas','retrofuturism','art-deco']:
   return o+P.o(66,90,31,None,a,2)+P.t(59,102,'!',36,a,'Georgia')+tx(119,82,'读取未完成',25)+tx(119,116,'检查路径后重新打开。',16)+P.l(119,141,w-36,141,a,1)
  return o+P.p('M29 117L63 49L97 117Z',None,a,3)+P.t(57,103,'!',33,i,'Arial')+tx(126,73,'无法读取文件',26)+tx(126,110,'请检查素材路径。',17)+badge(P,126,132,147,35,'重新读取')
 # 加载样例采用每套进度语汇；真实应用按系统偏好驱动动效。
 if z in ['celestial-atlas','art-deco','retrofuturism']:
  return o+P.o(60,75,27,None,b,1)+P.p('M60 48A27 27 0 0 1 87 75',None,a,3)+P.l(60,75,73,57,a,1.4)+tx(112,68,'正在读取',24)+tx(112,97,'素材编目中',14)
 if z in ['wabi-sabi','dunhuang','natural-history']:
  return o+figure(P,25,28,77)+tx(122,65,'正在编目',24)+gauge(P,121,89,w-157,15)
 return o+tx(32,55,'正在读取素材',24)+gauge(P,32,83,w-64,21)+tx(33,131,'请稍候',13)
