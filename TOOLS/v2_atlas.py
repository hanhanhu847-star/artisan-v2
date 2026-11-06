"""从实际素材与完整联系表生成 V2 图鉴。保留 V1 PDF，不覆盖它。"""
from pathlib import Path
import json,os,math
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from PIL import Image
from styles_data import ROOT,STYLES
from v2_registry import SERIES
W,H=842,1191
BG='#F3F0E8';INK='#24382F';MUTED='#566258';ACC='#92442F'
FONT=os.environ.get('ARTISAN_CJK_FONT','C:/Windows/Fonts/simhei.ttf')
pdfmetrics.registerFont(TTFont('CJK',FONT))
def hx(s):return HexColor(s)
def wrap(t,width,size):
 out=[];line=''
 for ch in t:
  if ch=='\n':out.append(line);line='';continue
  if pdfmetrics.stringWidth(line+ch,'CJK',size)>width and line:out.append(line);line=ch
  else:line+=ch
 if line:out.append(line)
 return out
def make():
 idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'));maps=json.loads((ROOT/'AUDIT/contact-pages.json').read_text(encoding='utf8'));styles={s['id']:s for s in idx['styles']};page_map=[];dest=ROOT/'PREVIEWS/ARTISAN_V2_Atlas.pdf'
 c=canvas.Canvas(str(dest),pagesize=(W,H),pageCompression=1,invariant=1);c.setTitle('ARTISAN V2 完整素材图鉴');c.setAuthor('hanhanhu847-star / Codex 辅助制作');c.setSubject('16套艺术风格、实际原件联系表、系列、应用说明与许可')
 def text(x,y,t,size=12,col=INK):
  c.setFillColor(hx(col));c.setFont('CJK',size);c.drawString(x,y,t)
 def para(x,y,t,width=746,size=12,leading=20):
  for line in wrap(t,width,size):text(x,y,line,size);y-=leading
  return y
 def line(x,y,X,Y,col='#C0C5B9',lw=.7):
  c.setStrokeColor(hx(col));c.setLineWidth(lw);c.line(x,y,X,Y)
 def start(title,sub='',key=None,level=0):
  c.setFillColor(hx(BG));c.rect(0,0,W,H,fill=1,stroke=0)
  text(42,H-39,'ARTISAN  /  EXPANDED ASSET LIBRARY',10,ACC);text(W-158,H-39,'V2  /  16 STYLES',10,MUTED)
  line(42,H-52,W-42,H-52);text(42,H-85,title,25)
  if sub:text(42,H-108,sub,10,MUTED)
  if key:c.bookmarkPage(key);c.addOutlineEntry(title,key,level=level,closed=True)
 def finish(record):
  no=c.getPageNumber();line(42,37,W-42,37);text(42,21,'原件路径相对于 ARTISAN_V2；预览不是原件替代品。',9,MUTED);text(W-88,21,str(no).zfill(3),10,ACC)
  page_map.append({'page':no,**record});c.showPage()
 def picture(p,x,y,w,h):
  with Image.open(p) as im:iw,ih=im.size
  k=min(w/iw,h/ih);ww=iw*k;hh=ih*k
  c.drawImage(str(p),x+(w-ww)/2,y+(h-hh)/2,ww,hh,preserveAspectRatio=True,mask='auto')
  return ww,hh
 start('通用艺术设计材质库','完整原件联系表与应用图鉴',key='cover')
 text(42,1010,'ARTISAN',64)
 y=para(45,966,f"16 套风格 / {idx['work_count']:,} 个独立作品家族 / {idx['file_count']:,} 个原素材文件",size=18,leading=28)
 y=para(45,y-8,'保留 V1 原件。尺寸、格式、颜色和状态版本不重复计为独立作品。新增背景由矢量原生渲染；2K纹理由规则在目标像素生成。',size=13)
 text(44,870,'作者与维护：hanhanhu847-star  /  自制素材 CC BY 4.0  /  Codex 辅助制作',12)
 for n,S in enumerate(STYLES):
  x=44+(n%4)*191;yy=760-(n//4)*148
  picture(ROOT/f"STYLES/{S['id']}/backgrounds/v2-plate-01.jpg",x,yy-92,177,100)
  text(x,yy-109,f"{S['no']:02d}  {S['zh']}",11)
 y=para(44,184,'使用顺序：离线浏览器选图 → 查看原件、来源与许可 → 复制项目所需子集 → 在宿主应用检查字号、交互和性能。',size=13,leading=22)
 para(44,y-14,'全库按逐文件许可分发。原创图形、CC0摄影与CC BY-SA数据星图各有独立记录。实时验收状态以 AUDIT/EXPANSION_REPORT.md 为准。',size=11,leading=19)
 finish({'kind':'cover'})
 start('阅读与使用','规格、计数、许可与事实边界',key='reading')
 blocks=[
 ('01 / 如何找素材','BROWSER/index.html支持系列、格式、尺寸、透明与许可筛选。默认每个作品一个版本，切换全部文件可看到V1与格式/状态副本。收藏只保存在当前浏览器。'),
 ('02 / 如何提取','点开素材可使用实际原件大图、深浅底和缩放。复制相对路径或打开原件另存；批量导出的JSON包含路径、作者、许可与SHA-256，仍须复制对应原文件。'),
 ('03 / 背景与纹理','各套有4幅4K横版、2幅4K竖版、2幅3000方版、2幅5120超宽独立构图，另有1个摄影来源。16个纹理包含12个原生2048连续平铺与4个透明叠层。不要用缩略图替代高清原件。'),
 ('04 / UI与应用','UI SVG是可编辑视觉交付。V1旧五态保留，V2重排默认视觉需要宿主同步实现完整状态、键盘焦点、读屏语义及真实数据。先接入一个代表页，再扩展。'),
 ('05 / 来源与许可','自制图形采用CC-BY-4.0；16幅Poly Haven全景及取景派生为CC0。十二星座图版、HYG/连线子集采用CC BY-SA 4.0。逐项作者、来源、修改与许可文件见ASSET_INDEX.json和LICENSES目录。'),
 ('06 / 天文与敦煌','只有v2-zodiac系列使用真实恒星数据。其他星云、轨道与星点为艺术示意；太阳系不按比例，月相为几何示意。敦煌图形为现代再创作，不标成特定洞窟、朝代或文物原件。'),
 ('07 / 联系表','每套先列使用页，再列背景、纹理、装饰、图标、插画和UI的当前独立作品；最后保留版本另列。棋盘表示透明区域。每页实际文件映射见AUDIT/contact-pages.json。'),
 ('08 / 生产边界','RGB色板不等于矿物测色或印刷保证。地图无真实基准、蓝图不可直接加工、博物插图不用于物种鉴定。字体由本机提供；输出前核对中文、长标题、换行和设备密度。')]
 y=H-156
 for title,body in blocks:
  text(44,y,title,17,ACC);y=para(44,y-29,body,size=12,leading=19)-28
 if y<60:raise ValueError('Reading page overflow '+str(y))
 finish({'kind':'reading'})
 catnames={'01-backgrounds':'高清背景','02-textures':'纹理与透明叠层','03-ornaments':'独立装饰','04-icons':'24通用 + 8专属图标','05-illustrations':'插画与场景','06-ui':'15组UI视觉样例','07-retained-variants':'保留原件与格式/状态版本'}
 for S in STYLES:
  z=S['id'];ss=styles[z];rs=[a for a in idx['assets']if a['style_id']==z];key='style-'+z
  start(f"{S['no']:02d} / {S['zh']}",S['en']+'  /  '+z,key=key)
  picture(ROOT/f'STYLES/{z}/backgrounds/v2-plate-01.jpg',44,803,500,280)
  for n,col in enumerate(S['palette']):
   c.setFillColor(hx(col));c.rect(579,1026-n*47,38,29,fill=1,stroke=0);text(630,1035-n*47,col,12)
  y=para(44,774,S['form']+' '+S['layout'],size=13,leading=22)-12
  y=para(44,y,f"{ss['work_count']}个独立家族 / {ss['count']}个源文件；背景11、纹理16、装饰28、图标32、插画{ss['counts_by_category']['illustrations']}、UI15组。",size=12,leading=20)-22
  text(44,y,'三组子系列',18,ACC);y-=30
  for name in SERIES[z]:
   n=ss['series_counts'][name];text(44,y,f"{name}  /  {n} 个独立作品",13);y-=25
  y-=10;text(44,y,'应用与排版',18,ACC);y-=30
  y=para(44,y,S['font']+' '+S['material'],size=12,leading=20)-13
  y=para(44,y,'适用：'+S['use']+'。'+S['ui'],size=12,leading=20)-13
  y=para(44,y,'避免：'+S['avoid'],size=12,leading=20)-24
  text(44,y,'事实与来源',18,ACC);y-=29
  if z=='celestial-atlas':note='十二星座图版采用 HYG v4.0 与 Stellarium modern 数据，北上东左，切平面投影；署名与固定版本见 LICENSES/celestial-data/ATTRIBUTION.md。其他星点与深空图为艺术示意。'
  elif z=='dunhuang':note='莲瓣、藻井、飞天、供养人与楼阁均为现代原创构成，不宣称复原特定洞窟。矿物颗粒为程序拟作，石青、石绿和朱砂色为RGB色感参考；背景阅读见本套STYLE_GUIDE.md中的Getty来源链接。'
  elif z=='generative-art':note='Voronoi、L-System、细胞自动机、流场与周期噪声由随包源脚本生成；保留种子与参数。v2-plate-09.svg带减少动态支持，JPG是同作品静帧。'
  else:note='非摄影图形为原创现代构成或程序化生成，不作为文物原件、科学测量、物种鉴定或制造依据。完整说明与来源见本套STYLE_GUIDE.md。'
  y=para(44,y,note,size=11,leading=19)-14
  photo=next(a for a in rs if a['license']=='CC0-1.0')
  y=para(44,y,'摄影：'+photo['author']+' / CC0-1.0。其他自制图形为CC-BY-4.0，单独声明CC BY-SA的星图除外。',size=10,leading=17)
  if y<56:raise ValueError('Style page overflow '+z+' '+str(y))
  finish({'kind':'style','style':z})
  for p in (m for m in maps if m['style']==z):
   no=p['page'];cat=p['category'];title=f"{S['no']:02d} / {S['zh']} / {catnames[cat]}"
   # Contact page carries its own title, so upper page header stays compact.
   c.setFillColor(hx(BG));c.rect(0,0,W,H,fill=1,stroke=0)
   text(42,H-35,title,15);text(42,H-55,f"第{no}页 / {len(p['assets'])}个实际文件 / "+('保留版本，不额外占作品指标'if cat.startswith('07')else'当前代表作品'),10,MUTED)
   c.bookmarkPage(f'{key}-{cat}-{no}')
   if no==1:c.addOutlineEntry(catnames[cat],f'{key}-{cat}-{no}',level=1,closed=True)
   ip=ROOT/p['path'];picture(ip,42,53,W-84,H-130)
   finish({'kind':'contact','style':z,'contact':p['path'],'asset_count':len(p['assets'])})
 c.save();(ROOT/'AUDIT/atlas-pages-v2.json').write_text(json.dumps(page_map,ensure_ascii=False,indent=2),encoding='utf8')
 print(len(page_map),'pages;',dest.stat().st_size,'bytes')
if __name__=='__main__':make()
