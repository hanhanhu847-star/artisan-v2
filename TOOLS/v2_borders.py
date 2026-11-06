"""V2 边饰：16套风格各自的连续饰带语汇、三种框、五种分隔、三类角件和五款重复单元。"""
from artwork import *
from v2_registry import *
def cell(S):
    bg,i,a,b,c=S['palette'];z=S['id']
    if z=='bauhaus':return path('M3 32V19A13 13 0 0 1 29 19V32Z',a)+rect(31,9,8,23,i)+poly([(41,32),(57,8),(72,32)],b)+circle(76,13,4,c)
    if z=='art-deco':return ''.join(poly([(40,36),polar(40,36,31,-pi/2+(j-4)*.23-.07),polar(40,36,31,-pi/2+(j-4)*.23+.07)],a)for j in range(9))+path('M2 33H12V27H20M60 27H68V33H78','none',b,1.7)
    if z=='swiss':return ''.join(rect(4+j*8,5+(j%3)*4,3+j%4,29-(j%3)*4,[i,a,b][j//3%3])for j in range(9))
    if z=='neo-brutalism':return poly([(4,10),(60,7),(73,14),(61,22),(70,29),(11,32)],a,i,3)+path('M9 8L18 16M13 6L22 14M48 23H61','none',i,2)
    if z=='memphis':return path('M2 28Q8 2 17 11T32 28T47 13','none',a,5)+poly([(48,28),(61,8),(70,30)],c,i,1.5)+circle(72,10,4,b)
    if z=='editorial':return path('M3 21H22Q36 20 39 8Q45 20 56 20H77M6 26H24M55 26H75','none',i,1.4)+circle(39,24,3,a)
    if z=='wabi-sabi':return path('M1 32Q28 30 68 8','none',i,1.7)+''.join(leaf(12+10*j,30-j*3,.34+j*.019,42 if j%2 else -28,b,i)for j in range(6))
    if z=='dark-academia':return path('M2 22Q17 3 32 17T56 23Q73 18 75 9M17 13Q18 2 28 4Q28 13 17 13M49 25Q54 37 63 33Q59 24 49 25','none',a,1.8)+circle(38,22,2,c)
    if z=='celestial-atlas':return path('M1 29Q38 4 78 16','none',b,1)+''.join(line(x,24-y,x+1,20-y,a,1)for x,y in [(9,0),(16,3),(23,5),(30,6)])+star(39,14,8,2,4,a)+path('M65 9A9 9 0 1 0 71 24Q60 22 65 9Z',c)
    if z=='dunhuang':return path('M2 28C14 32 19 14 29 17C35 20 32 25 28 23M50 22C62 21 64 5 77 12','none',a,2)+path('M40 29Q24 28 26 13Q35 14 40 22Q33 10 40 4Q48 12 41 22Q48 12 55 14Q53 29 40 29Z',b,i,1.35)+circle(40,27,2,c)
    if z=='cartography':return path('M1 26Q10 13 19 24T36 24T53 23T76 19M3 31Q15 25 25 31T47 30M43 11L48 5L56 13','none',b,1.6)+star(63,11,7,2,4,a)
    if z=='natural-history':return curve([(3+j*3,24+5*sin(j*.2))for j in range(25)],i,1.4)+''.join(leaf(12+j*10,28-j*.5,.42,52 if j%2 else -37,a,bg)for j in range(6))
    if z=='retrofuturism':return g(ell(35,21,27,10,'none',b,2),'rotate(-18 35 21)')+circle(36,20,9,a)+circle(63,13,4,c)+path('M4 29H18M63 27H77','none',i,1.5)
    if z=='cyberpunk':return path('M1 29H17L27 17H46L56 8H76M1 34H23L32 23H52L61 15H77','none',a,2.3)+circle(45,16,3,'none',c,1.4)+rect(11,10,11,3,b)
    if z=='blueprint':return path('M2 21H18V11H28V16H40V8H51V17H65V21H78M2 27H18V34H28V30H40V36H51V29H65V27H78','none',i,1.4)+line(2,24,78,24,b,.7)
    return ''.join(curve([(2+j*2,12+k*3.3+6*sin(j*.22+k*.36))for j in range(38)],a if k%2 else i,1.25)for k in range(5))
def units(S,x,y,k=1,deg=0):return g(cell(S),f'translate({n(x)} {n(y)}) rotate({deg}) scale({n(k)})')
def tile(S,v):
    bg,i,a,b,c=S['palette'];w=h=192;o=''
    if v==0: # 两条反向连续纹带，外框接续有完整周期
        o=rect(0,21,192,3,b)+rect(0,79,192,1,a)+rect(0,144,192,2,i)
        o+=units(S,9,26,1)+units(S,105,26,1)+units(S,90,138,.96,180)+units(S,186,138,.96,180)
    elif v==1:
        for dx in [-192,0,192]:
            o+=g(path('M-48 96L48 0L144 96L48 192ZM48 96L144 0L240 96L144 192Z','none',b,1.6),f'translate({dx} 0)')
        o+=units(S,9,74,.94)+units(S,106,74,.94)+circle(96,96,5,a)+circle(48,12,3,c)+circle(144,180,3,c)
    elif v==2:
        for x,y in [(48,48),(144,144)]:
            o+=circle(x,y,38,'none',a,2)+circle(x,y,31,'none',b,1)+units(S,x-27,y-14,.68)
        for x,y in [(144,48),(48,144)]:o+=g(path('M0 -21L17 0L0 21L-17 0Z','none',i,2),f'translate({x} {y})')+circle(x,y,4,c)
    elif v==3:
        for x,y in [(16,44),(102,139)]:
            o+=units(S,x,y,.97,-22)+g(path('M0 0L55 -22M0 4L55 -18','none',b,1.5),f'translate({x+8} {y+16})')
        o+=units(S,75,94,.54)+circle(45,153,5,a)+rect(140,43,13,4,c)
    else:
        for y in (0,96):
            for x in (0,96):
                if (x+y)%192==0:o+=rect(x+5,y+5,86,86,'none',a,2)+units(S,x+8,y+30,.98)
                else:o+=poly([(x+48,y+8),(x+89,y+48),(x+48,y+90),(x+7,y+48)],'none',b,2)+units(S,x+25,y+37,.59)
    return svg(w,h,o)
def art(S,kind,j):
    bg,i,a,b,c=S['palette'];m=cell(S)
    if kind=='frame':
        w,h=900,600;o=''
        if j==0:
            o=path('M22 90V22H230M670 22H878V90M878 510V578H670M230 578H22V510','none',i,3)+rect(38,38,824,524,'none',b,1)
            for x,y,k in [(38,40,0),(862,560,180)]:o+=units(S,x,y,1.8,k)
        elif j==1:
            o=path('M14 63L65 14H835L886 65V535L835 586H65L14 535Z','none',a,4)+path('M30 68L70 30H830L870 69V529L828 568H72L30 528Z','none',i,1.6)
            for x in range(158,700,125):o+=units(S,x,34,.73)+units(S,x,532,.73)
        else:
            o=rect(16,18,862,559,'none',i,2)+rect(28,30,26,535,b)+rect(66,30,801,535,'none',a,1)
            for y in range(80,536,80):o+=units(S,52,y,.57,90)
            o+=path('M660 564V527H866','none',a,2)+line(680,546,795,546,i,1)
    elif kind=='rule':
        w,h=720,80
        if j==0:o=line(4,40,245,40,i,2)+line(472,40,716,40,i,2)+units(S,258,17,1.18)+units(S,462,64,1.18,180)
        if j==1:o=path('M2 51H196L218 30H504L525 51H718M2 57H191M529 57H718','none',i,2)+units(S,321,4,.83)+circle(207,41,4,a)+circle(516,41,4,a)
        if j==2:o=rect(4,30,63,17,a)+units(S,79,18,1)+line(172,42,714,42,i,1.8)+''.join(line(188+j*23,42,188+j*23,34 if j%4 else 27,b,1)for j in range(22))
        if j==3:o=rect(8,38,704,2,b)+''.join(units(S,25+108*k,15,.8)for k in range(6))+''.join(circle(107+k*108,39,3,a)for k in range(6))
        if j==4:o=path('M6 23H147L169 40H551L573 23H714M6 59H147L169 43M551 43L573 59H714','none',i,1.5)+units(S,7,25,.64)+units(S,712,57,.64,180)
    elif kind=='corner':
        w=h=160
        if j==0:o=path('M7 149V8H149M19 123V20H124','none',i,2.5)+units(S,26,24,.99)+units(S,55,47,.82,90)
        if j==1:o=poly([(8,8),(147,8),(122,32),(99,32),(32,99),(32,124),(8,148)],'none',a,3)+units(S,24,56,.92,-34)+circle(18,19,4,b)
        if j==2:o=path('M7 121Q8 58 46 34Q76 12 137 10M18 140Q12 81 53 47Q95 17 148 24','none',i,1.9)+units(S,43,65,.96,-22)+circle(19,123,5,a)+circle(129,18,4,b)
    return svg(w,h,o)
def make():
    for S in STYLES:
        z=S['id'];rows=[]
        for k,labels in [('frame',['开放四角框','裁角双轨框','装订侧脊框']),('rule',['对向饰带','阶梯折线分栏','标距分隔','节奏串饰','双端括线']),('corner',['跨边角件','斜面护角','弧线角花']),('repeat',['双向饰带循环','菱格交接','圆印与菱花','错行斜织','棋格嵌花'])]:
            for j,title in enumerate(labels):
                r=item(z,'ornaments',k+'-'+str(j+1),S['zh']+' · '+title,'独立透明矢量装饰；'+('以192单位为周期。' if k=='repeat' else '适合章节、标签或画板边缘。'),[0,1,2,1,2][j],k,alpha=True,tile=k=='repeat')
                write(outfile(z,r),tile(S,j) if k=='repeat' else art(S,k,j));rows.append(r)
        save_batch(z,'borders',rows)
        # 原有14类组件缺工具栏；使用真实操作符号，不将各状态另计。
        body=rect(3,3,714,76,S['palette'][0],S['palette'][1],2,3)+units(S,11,21,.88)+line(100,16,100,65,S['palette'][3],1)
        for j,(title,D) in enumerate([('编辑','M2 16L14 4L18 8L6 20L1 21Z'),('复制','M6 5H17V18H6ZM2 14V2H13'),('分享','M5 10L16 4M5 12L16 18M4 9a2 2 0 1 0 0 4a2 2 0 1 0 0-4ZM16 3h3v3h-3ZM16 17h3v3h-3Z'),('收藏','M11 1L14 7L21 8L16 13L17 20L11 17L4 20L5 13L1 8L8 7Z')]):
            x=126+139*j;body+=g(path(D,'none',S['palette'][1],1.8),f'translate({x} 27) scale(1.06)')+txt(x+34,47,title,17,S['palette'][1],'Microsoft YaHei,sans-serif')
        r=item(z,'ui','toolbar','编辑工具栏','可拆分按钮组：编辑、复制、分享、收藏；应用中使用原生按钮并提供焦点。',1,'toolbar');write(outfile(z,r),svg(720,82,body));save_batch(z,'ui',[r])
    report()
if __name__=='__main__':make()
