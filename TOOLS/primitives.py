from artwork import *
ICON_NAMES='file folder image video audio document search favorite download upload settings user map time statistics database network security device task-status'.split()
ICON_ZH='文件 文件夹 图片 视频 音频 文档 搜索 收藏 下载 上传 设置 用户 地图 时间 统计 数据库 网络 安全 设备 任务状态'.split()
GLYPHS=[
'M6 3H14L19 8V21H6ZM14 3V8H19',
'M3 7V5H10L12 8H21V19H3ZM3 10H21',
'M3 4H21V20H3ZM4 18L10 11L14 15L17 12L21 16M16.5 8a1 1 0 1 0 .1 0',
'M3 6H15V18H3ZM15 10L21 7V17L15 14',
'M4 10V14M8 6V18M12 3V21M16 8V16M20 10V14',
'M5 3H19V21H5ZM8 8H16M8 12H16M8 16H13',
'M16 10a6 6 0 1 1-12 0a6 6 0 1 1 12 0ZM15 15L21 21',
'M12 3L14.6 8.8L21 9.5L16.2 14.1L17.4 20.5L12 17.2L6.6 20.5L7.8 14.1L3 9.5L9.4 8.8Z',
'M12 3V15M7 10L12 15L17 10M4 16V20H20V16',
'M12 16V4M7 9L12 4L17 9M4 16V20H20V16',
'M10 3H14L15 6L18 5L20 8L18 11L21 13L20 16L16 16L15 20H11L10 17L7 18L4 15L6 12L3 10L5 6L8 7ZM15 11.5a3 3 0 1 1-6 0a3 3 0 1 1 6 0Z',
'M16 8a4 4 0 1 1-8 0a4 4 0 1 1 8 0ZM4 21Q4 14 12 14Q20 14 20 21',
'M3 6L9 3L15 6L21 3V18L15 21L9 18L3 21ZM9 3V18M15 6V21',
'M21 12a9 9 0 1 1-18 0a9 9 0 1 1 18 0ZM12 6V12L16 14',
'M3 3V21H21M7 17V12H9V17ZM12 17V8H14V17ZM17 17V4H19V17Z',
'M4 6C4 2 20 2 20 6C20 10 4 10 4 6ZM4 6V18C4 22 20 22 20 18V6M4 12C4 16 20 16 20 12',
'M10 3H14V7H10ZM2 16H7V21H2ZM17 16H22V21H17ZM12 7V11M4.5 16V11H19.5V16',
'M12 3L20 6V12Q19 18 12 21Q5 18 4 12V6ZM8 12L11 15L16 9',
'M3 4H21V17H3ZM9 21H15M12 17V21',
'M4 4H20V20H4ZM7 12L11 16L17 8']
def icon(S,j):
    bg,ink,a,b,c=S['palette'];i=S['no']-1
    fr=['',rect(6,6,52,52,'none',a,1)+rect(9,9,46,46,'none',a,.65),rect(6,55,16,3,a),rect(8,10,50,48,ink)+rect(5,6,50,48,bg,ink,3),circle(32,32,26,b,'none')+circle(52,12,5,a),line(6,55,58,55,a,1),path('M7 47Q2 19 20 9M42 56Q58 51 58 38','none',b,1.2),rect(7,5,50,54,'none',a,1.6)+path('M8 15L17 6M47 58L56 49','none',a,2),circle(32,32,28,'none',b,.8)+ringticks(32,32,27,16,b),poly([(32,2),(62,32),(32,62),(2,32)],'none',b,1.2)+circle(32,4,2,a),path('M5 12V5H13M51 59H59V51','none',a,1.5)+line(8,57,26,57,b,.8),ell(32,31,26,27,'none',b,.9)+line(7,61,24,61,a,1),rect(4,9,56,46,'none',a,2,17)+line(19,59,45,59,c,1.2),path('M4 20L16 7H59V43L46 56H4Z','none',a,1.7)+rect(48,48,7,3,b),path('M3 12V4H12M52 4H60V12M4 52V60H12M52 60H60V52','none',a,1)+line(1,32,9,32,b,1),''.join(circle(6+k*5,52+3*sin(k*.6),1.3,b)for k in range(10))][i]
    lean=[0,0,0,0,-5,0,-3,0,0,0,0,0,-6,0,0,0][i]
    weight=[2.2,1.5,2.3,3.1,2.45,1.6,1.85,1.55,1.5,1.85,1.55,1.55,2.15,1.8,1.35,1.9][i]
    cap='round' if i in [4,6,8,9,11,12,15] else 'square'
    glyph=path(GLYPHS[j],'none',ink,weight,f'stroke-linecap="{cap}" stroke-linejoin="{("round" if cap=="round" else "miter")}"')
    # 双线、套印、断点、端帽等族系工艺适用于全部20个语义。
    if i==13:glyph=g(path(GLYPHS[j],'none',b,.9),'translate(1.2 .6)')+glyph
    if i==1:glyph+=path(GLYPHS[j],'none',bg,.38)
    if i==0:fr+=rect(7,53,7,7,a)+circle(53,9,3,c)
    return svg(64,64,fr+g(glyph,f'translate(13 13) scale(1.58) skewX({lean})'))
ORNS='frame rule corner geometry pattern chapter title-frame caption-frame seal tag ribbon background-mark'.split()
ORN_LABEL='边框 分隔线 角花 几何图案 花纹 章节编号 标题框 图注框 印章 标签 角标 背景装饰'.split()
def sig(S,i=0):
    # 每种风格以自己独有的印记作为装饰语汇；坐标域 32 × 32。
    bg,ink,a,b,c=S['palette'];z=S['no']-1
    if z==0:return rect(1,16,29,8,a)+circle(14,12,9,b)
    if z==1:return ''.join(line(16,29,*polar(16,29,26,-pi+j*pi/8),a,1.5)for j in range(9))
    if z==2:return rect(1,2,5,27,ink)+rect(9,2,15,14,a)+rect(9,20,21,4,ink)
    if z==3:return path('M2 11H17V4L31 16L17 28V21H2Z',a,ink,2.5)
    if z==4:return curve([(1,9),(8,23),(15,9),(22,23),(30,9)],a,4)+circle(25,4,3,b)
    if z==5:return txt(2,29,'§',32,ink,'Georgia')
    if z==6:return path('M2 22Q7 4 16 13Q24 5 30 24Q16 28 2 22Z',b)
    if z==7:return path('M2 28L7 6H26L22 26ZM8 11H22M7 21H19','none',a,2)+line(4,28,21,28,ink,1)
    if z==8:return star(16,16,15,4,6,a)+circle(16,16,2,bg)
    if z==9:return path('M16 26Q2 24 1 11Q9 12 16 19Q9 10 16 2Q22 11 17 19Q24 10 31 11Q28 24 16 26Z',b,a,1.5)
    if z==10:return star(16,16,15,4,4,ink)+g(star(16,16,9,3,4,a),'rotate(45 16 16)')
    if z==11:return leaf(10,29,.62,24,a,ink)
    if z==12:return circle(17,16,8,a)+g(ell(16,16,15,4,'none',b,2),'rotate(-28 16 16)')
    if z==13:return path('M1 25L12 7H18L7 25ZM14 25L25 7H31L20 25Z',a)
    if z==14:return circle(16,16,10,'none',a,1.5)+path('M0 16H32M16 0V32','none',ink,1)
    return ''.join(path(f'M0 {6+j*5}Q10 {j*5-5} 18 {9+j*5}T32 {5+j*5}','none',a if j%2 else b,1.5)for j in range(5))
def symbol(S,x,y,size=32,rotate=0):return g(sig(S),f'translate({n(x)} {n(y)}) scale({n(size/32)}) rotate({rotate} 16 16)')
def ornament(S,j):
    bg,ink,a,b,c=S['palette'];s=symbol
    if j==0:
        w,h=640,360;o=rect(8,8,624,344,'none',ink,2)+rect(16,16,608,328,'none',a,1)+''.join(s(S,x,y,38,r)for x,y,r in [(10,10,0),(592,10,90),(592,310,180),(10,310,270)])
    elif j==1:w,h=640,40;o=line(0,20,284,20,ink,1.5)+line(356,20,640,20,ink,1.5)+s(S,304,4)
    elif j==2:w=h=96;o=path('M5 90V5H90','none',ink,3)+s(S,14,14,64)
    elif j==3:w=h=192;o=''.join(g(symbol(S,84,8,28),f'rotate({i*45} 96 96)')for i in range(8))+symbol(S,68,68,56)
    elif j==4:w,h=320,72;o=''.join(symbol(S,i*40,18+(i%2)*8,31,0 if i%2 else 180)for i in range(8))
    elif j==5:w,h=128,80;o=symbol(S,4,12,22)+txt(33,60,f'{S["no"]:02d}',48,ink,'Georgia')+line(9,70,118,70,a,2)
    elif j==6:w,h=640,120;o=rect(4,8,632,102,'none',ink,2)+line(27,99,612,99,a,1)+symbol(S,17,31,45)
    elif j==7:w,h=480,80;o=path('M8 6V70H472','none',ink,2)+symbol(S,17,14,22)+line(48,28,104,28,a,2)
    elif j==8:w=h=128;o=circle(64,64,58,'none',a,2)+circle(64,64,50,'none',b,1)+symbol(S,33,33,62)
    elif j==9:w,h=200,65;o=poly([(4,32),(22,5),(195,5),(195,60),(22,60)],bg,a,2)+circle(24,32,4,'none',ink)+symbol(S,45,19,25)
    elif j==10:w=h=112;o=poly([(6,6),(105,6),(6,105)],a)+symbol(S,14,14,29)
    else:
        w,h=720,240
        o='<g opacity=".27">'+stamp(motif(S,2),-30,-25,.94)+stamp(motif(S,1),362,70,.43)+stamp(motif(S,2),568,-2,.60)+'</g>'+line(202,191,554,191,a,.8)
    return svg(w,h,o)
UIN='button card tag input navbar sidebar table list progress dialog tooltip empty error loading'.split()
UIZH='按钮 卡片 标签 输入框 导航栏 侧边栏 表格 列表 进度条 弹窗 提示框 空状态 错误状态 加载状态'.split()
STATES=['normal','hover','selected','disabled','error']
STLAB=['就绪','悬停','已选中','不可用','需检查']
def lumin(c):
    rgb=[int(c[j:j+2],16)/255 for j in [1,3,5]];return sum(v*k for v,k in zip([t/12.92 if t<=.04045 else ((t+.055)/1.055)**2.4 for t in rgb],[.2126,.7152,.0722]))
def texton(c):
    L=lumin(c)
    def contrast(candidate):
        x=lumin(candidate)
        return (max(x,L)+.05)/(min(x,L)+.05)
    best=max(['#161819','#FFF9EE'],key=contrast)
    return best if contrast(best)>=4.5 else max(['#000000','#FFFFFF'],key=contrast)
def ui(S,j,q):
    bg,ink,a,b,c=S['palette'];z=S['no'];err='#802E2B' if lumin(bg)>.35 else '#FFB5A4'
    fg=ink;rim=[ink,b,a,b,err][q];rad=[0,1,0,0,14,0,8,2,16,3,1,2,22,0,0,12][z-1]
    w,h=[(256,80),(360,210),(184,64),(368,88),(580,92),(230,260),(520,232),(370,210),(400,88),(440,228),(272,92),(336,200),(350,170),(280,100)][j]
    def tx(x,y,t,sz=15,col=None):return txt(x,y,t,sz,col or fg,'Microsoft YaHei, SimHei, sans-serif')
    def frame(x,y,W,H,fill,edge,r=rad):
        if z in [2,10,14]:
            f=6 if z!=14 else 13
            return poly([(x+f,y),(x+W,y),(x+W,y+H-f),(x+W-f,y+H),(x,y+H),(x,y+f)],fill,edge,2)
        return rect(x,y,W,H,fill,edge,3 if z==4 else 1.6,r)
    o=frame(4,4,w-12,h-12,bg,rim)
    if z==4:o=rect(9,10,w-12,h-12,ink)+o
    if z in [2,8,10,11]:o+=rect(10,10,w-24,h-24,'none',a,.7,max(0,rad-2))
    if q==1:o+=line(14,h-11,w-18,h-11,rim,3)
    if q==2:o+=path('M8 4H36L8 32Z',a)+path('M11 13L14 16L20 9','none',texton(a),1.7)
    if q==4:o+=rect(w-9,12,3,h-30,err)
    left=23
    if j==0:o+=symbol(S,20,22,28)+tx(63,47,['添加到图册','添加到图册','已加入图册','暂不可添加','重新添加'][q],18)
    elif j==1:o+=rect(21,21,84,94,b)+g(sig(S),'translate(35 40) scale(1.6)')+tx(124,52,S['zh'],24)+tx(124,83,'材质研究 / 图版',13)+line(22,137,w-23,137,rim)+tx(23,170,'查看样本',16)
    elif j==2:o+=symbol(S,20,18,23)+tx(55,39,['样本','浏览样本','已选样本','已停用','待核对'][q],15)
    elif j==3:o+=tx(22,29,'作品名称',12)+tx(22,59,['输入名称','输入名称','素描手记','只读名称','请填写名称'][q],17,err if q==4 else ink)+line(22,68,w-26,68,rim,1.2)
    elif j==4:o+=symbol(S,24,23,30)+tx(69,48,S['zh'],18)+tx(274,46,'图册',16)+tx(377,46,'素材',16)+tx(474,46,'设置',16)+line(271,62,322,62,rim,3)
    elif j==5:
        o+=tx(23,40,'工作目录',21)+line(21,58,w-25,58,rim)
        for k,t in enumerate(['全部素材','已收藏','待整理']):o+=rect(16,74+k*44,w-37,34,b if k==1 and q==2 else bg)+symbol(S,23,84+k*44,14)+tx(53,98+k*44,t)
    elif j==6:
        for k,lineitems in enumerate([('名称','编号','状态'),('构成研究','AT–01','已编目'),('表面研究','AT–02','待校对'),('图版底稿','AT–03','已归档')]):
            yy=43+k*43;o+=tx(24,yy,lineitems[0])+tx(225,yy,lineitems[1],14)+tx(382,yy,lineitems[2],14)+line(22,yy+13,w-22,yy+13,rim,.7)
    elif j==7:
        for k,t in enumerate(['形式研究','材料样本','出版图版']):o+=symbol(S,23,24+k*50,24)+tx(70,45+k*50,t)+line(24,59+k*50,w-25,59+k*50,rim,.8)
    elif j==8:o+=tx(22,34,'导出素材',15)+tx(323,34,'64%',15)+rect(23,46,350,9,b)+rect(23,46,224,9,rim)
    elif j==9:o+=tx(24,50,'添加到图册',24)+line(25,66,w-26,66,rim)+tx(24,103,'保留素材路径与来源信息。',16)+frame(236,136,170,43,rim,rim,rad)+tx(265,164,'确认添加',15,texton(rim))
    elif j==10:o+=symbol(S,19,23,24)+tx(55,45,'打开素材详情',17)
    elif j==11:o+=symbol(S,137,23,56)+tx(89,116,'暂无匹配素材',20)+tx(76,146,'调整分类或搜索条件',14)
    elif j==12:o+=circle(47,51,17,'none',err,2)+tx(43,58,'!',20,err)+tx(80,57,'无法加载文件',20)+tx(28,104,'检查路径后重试。',14)
    elif j==13:o+=''.join(circle(32+k*15,42,3+k*.8,[a,b,ink][k])for k in range(3))+tx(90,48,'正在读取素材',16)
    if j not in [0,2,3]:o+=tx(w-72,h-16,STLAB[q],10,err if q==4 else ink)
    if q==3:o='<g opacity=".58">'+o+'</g>'
    return svg(w,h,o)
