"""三套样式的六种同构组件重新设计，旧五态文件原样保留。"""
from v2_plates import Pen
from artwork import STYLES,svg,write
from v2_registry import item,outfile,save_batch,report
from v2_ui_themes import theme_ui
KINDS=['input','table','progress','dialog','error','loading']
TITLES=['输入框','表格','进度条','弹窗','错误提示','加载状态']
DIMS=[(440,112),(600,280),(460,125),(480,260),(460,165),(360,115)]
def art(P,kind,w,h):
 z=P.S['id'];i=P.i;a=P.a;b=P.b;bg=P.bg;c=P.c
 o=P.r(0,0,w,h,bg,'none')
 tx=lambda x,y,s,sz=15: P.t(x,y,s,sz,i,'SimHei' if z!='editorial'else 'SimSun')
 if z=='swiss':
  o+=P.r(0,0,7,h,a,'none')+tx(22,24,'MATERIAL / 02',11)
  if kind=='input':return o+tx(22,52,'作品名称',12)+tx(22,85,'无题 · 研究 01',23)+P.l(22,98,w-20,98,i,2)+P.l(w-45,63,w-45,85,a,2)
  if kind=='table':
   o+=tx(22,60,'素材目录',25)+tx(w-82,58,'03 项',13)
   for n,labels in enumerate([['编号','作品','格式'],['01','几何构成','SVG'],['02','雕版表面','WEBP'],['03','开页试样','SVG']]):
    y=96+n*48;o+=tx(22,y,labels[0],13)+tx(109,y,labels[1],16)+tx(502,y,labels[2],13)+P.l(22,y+14,w-22,y+14,i,2 if n==0 else .6)
   return o
  if kind=='progress':return o+tx(22,62,'导出中',22)+tx(344,65,'64%',30)+P.r(22,88,414,15,b,'none')+P.r(22,88,265,15,a,'none')
  if kind=='dialog':return o+tx(22,72,'加入图册',34)+P.l(22,92,w-22,92,i,3)+tx(22,126,'保留文件、相对路径和来源。',16)+tx(22,155,'3 项素材已选择。',14)+P.r(294,192,163,44,i,'none')+P.t(321,220,'确认添加',17,bg,'SimHei')+tx(219,220,'取消',16)
  if kind=='error':return o+P.t(22,102,'!',68,a,'Arial')+tx(72,75,'文件无法读取',25)+tx(72,103,'检查路径后重新打开。',15)+P.l(72,133,164,133,a,2)+tx(72,127,'重新读取',13)
  return o+tx(22,64,'读取素材',23)+''.join(P.r(227+k*26,47,17,17,i if k<3 else b,'none')for k in range(4))+tx(23,96,'请稍候',12)
 if z=='editorial':
  o+=P.l(24,22,w-24,22,i,.8)+tx(24,17,'ARTISAN   /   校样',11)+tx(w-48,h-14,'02',12)
  if kind=='input':return o+tx(24,48,'书目 · 作品名称',13)+tx(24,80,'无题研究',25)+P.l(24,92,w-24,92,i,.8)+P.l(w-55,54,w-55,82,a,1)
  if kind=='table':
   o+=tx(24,65,'目录',32)+P.l(100,37,100,242,b,.8)
   for n,labels in enumerate([['01','一页构成研究','SVG'],['02','纸面工艺样本','WEBP'],['03','正文开页','SVG']]):
    y=112+n*56;o+=tx(27,y,labels[0],20)+tx(122,y,labels[1],19)+tx(492,y,labels[2],12)+P.l(122,y+15,w-24,y+15,b,.6)
   return o
  if kind=='progress':return o+tx(24,58,'导出图版',22)+tx(331,57,'16 / 25',18)+P.l(24,82,w-24,82,b,2)+P.l(24,82,288,82,a,3)+P.p('M281 75L288 82L281 89',None,a,1)+tx(24,107,'正在写入素材清单',12)
  if kind=='dialog':return o+tx(24,75,'添加至图册',33)+tx(24,114,'所选图版将连同来源信息保存。',17)+P.l(24,142,w-24,142,b,.7)+tx(24,173,'本次选择　03 幅',14)+P.r(302,191,154,37,a,'none')+P.t(330,216,'确认添加',15,bg,'SimSun')+tx(241,216,'取消',14)
  if kind=='error':return o+tx(24,65,'校样提示',27)+P.r(24,84,3,43,a,'none')+tx(40,100,'当前文件尚未找到。',17)+tx(40,125,'检查素材相对路径，然后重试。',14)
  return o+tx(24,62,'正在编目',24)+''.join(P.l(24+k*50,84,60+k*50,84,a if k<4 else b,2)for k in range(6))
 # 工程图式侧栏、分度、实体槽道与技术表头
 o+=P.p(f'M8 30V8H{w-8}V{h-8}H8V{h-29}',None,i,1.2)+P.l(8,31,w-8,31,b,.8)+P.t(19,23,'ASSET / CONTROL',11,i,'monospace')
 if kind=='input':return o+tx(20,57,'名称',13)+P.r(85,44,331,47,None,i,1)+P.l(85,44,93,52,b,.8)+tx(99,73,'构成研究 01',20)+P.l(392,55,392,80,a,1.4)
 if kind=='table':
  o+=P.l(72,31,72,h-8,b,.8)+P.l(397,31,397,h-8,b,.8)+P.l(496,31,496,h-8,b,.8)
  for n,ls in enumerate([['#','项目名称','规格','状态'],['01','零件图版','SVG','就绪'],['02','表面肌理','2K','就绪'],['03','标题框架','SVG','就绪']]):
   y=62+n*55
   for x,t in zip([23,88,411,510],ls):o+=tx(x,y,t,14)
   o+=P.l(8,y+18,w-8,y+18,b,.8)
  return o
 if kind=='progress':return o+tx(19,57,'导出',15)+P.t(w-71,57,'64%',20,i,'monospace')+''.join(P.r(20+k*21,73,16,23,a if k<13 else bg,b,.7)for k in range(20))+P.l(20,108,w-20,108,b,.6)
 if kind=='dialog':return o+tx(24,73,'添加图版',29)+P.l(24,89,w-24,89,b,.8)+tx(24,120,'文件与来源信息将一同编目。',16)+tx(24,152,'选择数量：03',15)+P.r(280,186,174,42,None,i,1.3)+tx(317,214,'确认添加',16)+P.r(173,186,89,42,None,b,1)+tx(196,214,'取消',16)
 if kind=='error':return o+P.p('M22 113L48 57L75 113Z',None,a,2)+P.t(43,101,'!',30,a,'monospace')+tx(96,76,'文件未就绪',24)+tx(96,104,'检查路径及文件是否存在。',15)+P.l(96,125,w-24,125,b,.8)
 return o+P.o(47,73,23,None,b,1)+P.p('M47 50A23 23 0 0 1 70 73',None,a,3)+P.l(47,73,47,57,a,1)+tx(92,69,'读取素材',22)+tx(92,91,'请稍候',13)
def make():
 for S in STYLES:
  rows=[];P=Pen(S)
  specialist=S['id'] in ['swiss','editorial','blueprint']
  dims=DIMS if specialist else [(480,140),(640,340),(500,200),(520,340),(480,200),(400,160)]
  for k,title,(w,h)in zip(KINDS,TITLES,dims):
   r=item(S['id'],'ui','ui-'+k,title+' · V2布局','独立可编辑SVG视觉样例；该组V1状态原件保留备查，V2布局单独计一次。',2,'component',alpha=False,family=k,credit='upgrade')
   write(outfile(S['id'],r),svg(w,h,(art if specialist else theme_ui)(P,k,w,h)));rows.append(r)
  save_batch(S['id'],'ui-revision',rows)
 report()
if __name__=='__main__':make()
