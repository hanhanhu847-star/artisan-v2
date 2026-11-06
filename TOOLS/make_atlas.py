"""生成17页真实图版；中文字体只在生成时使用，PDF内嵌所需字形子集。"""
from styles_data import *
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
font=os.environ.get('ARTISAN_CJK_FONT',r'C:\Windows\Fonts\simhei.ttf');pdfmetrics.registerFont(TTFont('CN',font))
W,H=900,660;p=ROOT/'PREVIEWS/ARTISAN_Atlas.pdf';cv=canvas.Canvas(str(p),pagesize=(W,H),pageCompression=1);cv.setTitle('ARTISAN 通用艺术设计材质图鉴');cv.setAuthor('ARTISAN')
cream='#F5F3E9';ink='#1F2923';muted='#4C5A52';red='#943F2B'
def fill(c):cv.setFillColor(HexColor(c))
def box(x,top,w,h,c):fill(c);cv.rect(x,H-top-h,w,h,fill=1,stroke=0)
def text(x,top,s,sz=12,color=ink,f='CN'):
    fill(color);cv.setFont(f,sz);cv.drawString(x,H-top-sz,s)
def rule(x,y,w):cv.setStrokeColor(HexColor('#B2B9AD'));cv.setLineWidth(.6);cv.line(x,H-y,x+w,H-y)
def wrap(x,top,s,width,sz=11,lineh=17):
    a=''
    for char in s:
        if pdfmetrics.stringWidth(a+char,'CN',sz)>width and a:
            text(x,top,a,sz);top+=lineh;a=''
        a+=char
    if a:text(x,top,a,sz);top+=lineh
    return top
def img(file,x,t,w,h):
    cv.drawImage(str(file),x,H-t-h,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
def footer(n):rule(35,626,830);text(35,634,'ARTISAN  /  材质研究档案',9,muted);text(785,634,f'{n:02d}   /   17',9,muted,'Helvetica')
idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'));rows=idx['assets']
box(0,0,W,H,cream);text(35,23,'MATERIAL ARCHIVE    /    VOLUME 01',10,red,'Helvetica-Bold');text(32,35,'ARTISAN',56,ink,'Times-Bold')
text(37,104,'通用艺术设计材质库 · 图版索引',18);text(550,80,f'16 种风格   /   {len(rows)} 项可调用素材',12,muted)
for i,s in enumerate(STYLES):
    x=35+i%4*211;t=155+i//4*113
    img(ROOT/'PREVIEWS/plates'/f'{s["id"]}.webp',x,t,195,79);text(x,t+82,f'{i+1:02d}   '+s['zh'],12)
footer(1);cv.showPage()
for i,s in enumerate(STYLES):
    z=s['id'];base=ROOT/'STYLES'/z;d=ROOT/'PREVIEWS/details';box(0,0,W,H,cream)
    text(35,24,'FIELD NOTES    /    '+str(i+1).zfill(2),10,red,'Helvetica-Bold');text(35,43,s['zh'],28);text(36,82,s['en'],15,muted,'Times-Italic');text(667,35,s['group'],11,muted);rule(35,113,830)
    img(base/'backgrounds/field-study-1920.jpg',35,130,505,284)
    text(35,421,'01 / '+s['title']+' · 横向母版',10,muted)
    text(560,128,'视觉语言',14,red);y=wrap(560,153,s['form'],298,11,17)
    text(560,y+10,'配色',14,red)
    for j,c in enumerate(s['palette']):
        x=560+j*61;box(x,y+36,52,27,c);text(x,y+67,c,8,ink,'Helvetica')
    y+=97;text(560,y,'排版与材质',14,red);y=wrap(560,y+25,s['layout']+s['material'],298,10.8,16)
    text(560,y+9,'使用边界',14,red);wrap(560,y+34,s['avoid'],298,10.8,16)
    rule(35,451,830)
    samples=[(base/'textures/paper.png','纸纤 / 平铺'),(d/f'{z}-illustrations.png','独立插图'),(d/f'{z}-icons.png','操作图标'),(d/f'{z}-ui.png','组件 / 选中'),(base/'backgrounds/photo-window.jpg','环境摄影 / 取景')]
    for j,(src,title) in enumerate(samples):
        x=35+j*169;box(x,467,153,97,(s['palette'][0] if j in [1,2,3] else '#E7E7DA'));img(src,x+4,471,145,89);text(x,572,title,11)
    text(35,604,'STYLES/'+z+'    |    STYLE_GUIDE.md',9,muted,'Helvetica');footer(i+2);cv.showPage()
cv.save();print(p.name,17,'pages')
