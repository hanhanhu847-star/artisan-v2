"""64幅主题与场景，各自编排视点、物体、结构及叙事内容。坐标域640×400。"""
from v2_objects import *
SCENES={
'bauhaus':['工坊天窗下','实验剧场排练','住宅单元街区','印刷台上的套准练习'],
'art-deco':['都会夜间天际线','剧院扇形舞台','电梯前厅','远洋码头'],
'swiss':['换乘示意图','展览张贴墙','版心校准台','赛事计时图版'],
'neo-brutalism':['叠贴的街头公告','地下印刷工位','坡道与护栏','堆叠音箱现场'],
'memphis':['弧墙泳池','客厅的几何家具','平衡玩具装配','舞池切分节拍'],
'editorial':['打开的图版跨页','编辑桌的清晨','暗房放大机','活字字盘'],
'wabi-sabi':['砂庭石岛','茶室的空壁龛','陶轮初坯','竹影过浅溪'],
'dark-academia':['闭馆前的阅览室','雨后的回廊','编目员的标本台','装帧工坊'],
'celestial-atlas':['观测台与星轨','月相序列图','太阳系次序图','银河与星云示意'],
'dunhuang':['双飞飘带','楼阁莲池叙事构成','壁画设色工坊','供养行列研究'],
'cartography':['群岛与引航路径','山口地形剖面','港城街坊与码头','三点交会测绘'],
'natural-history':['林下羽叶群落','栖枝鸟的羽翼研究','河床鱼群','化石海岸地层'],
'retrofuturism':['环形轨道船坞','跨湾单轨','模拟控制室','外行星温室穹顶'],
'cyberpunk':['雨夜高架巷道','交换机房','屋顶中继阵列','夜班站台'],
'blueprint':['泵体爆炸视图','采光厂房横剖','分支管路装配','开关与滤波示意'],
'generative-art':['最近邻胞元','分枝文法森林','规则90的演化','流场粒子切片']}
def horizon(P,x=0,y=260,w=640):
    return P.p(f'M{x} {y}Q{x+w*.23} {y-90} {x+w*.4} {y-21}T{x+w*.7} {y-30}T{x+w} {y-6}V400H{x}Z',P.b,'none')
def rope(P,ps,col=None,w=1.5):return curve(ps,col or P.i,w)
def solar(P,x,y,k=1):
    o=P.o(0,0,25,P.c,P.a,2)+''.join(P.l(*polar(0,0,29,j*pi/12),*polar(0,0,36,j*pi/12),P.c,1.2)for j in range(24))
    return place(o,x,y,k)
def vessel(P,x,y,k=1):
    o=P.p('M-54 -5Q0 13 55 -7L49 10Q14 46 -25 29Q-48 15 -54 -5Z',P.b)+P.e(0,-7,54,9,P.c)+P.e(1,-7,43,4,P.bg)+P.l(-18,32,15,32,P.a,3)
    return place(o,x,y,k)
def shelves(P,x,y,w,h,rnd,rows=3):
    o=P.r(x,y,w,h,P.bg)
    for j in range(rows):
        yy=y+(j+1)*h/rows-7;o+=P.r(x,yy,w,5,P.a);xx=x+5
        while xx<x+w-15:
            ww=rnd.randint(8,18);hh=rnd.randrange(int(h/rows*.45),int(h/rows*.82));o+=P.r(xx,yy-hh,ww,hh,[P.b,P.c,P.bg][rnd.randrange(3)],P.i,.9)+P.l(xx+2,yy-6,xx+ww-2,yy-6,P.a,1.3);xx+=ww+2
    return o
def skyline(P,x,y,w,h,rnd):return staircity(P,x,y,w,h,rnd,'tech')
def cloud(P,x,y,k):
    return place(P.p('M-39 9Q-49 -7 -30 -13Q-21 -35 -3 -17Q14 -26 23 -10Q44 -12 43 2Q42 14 26 13H-39Z',None,P.b,1.8),x,y,k)
def mountain(P,x,y,k=1):
    return place(P.p('M-116 8L-68 -32L-53 -21L-10 -77L9 -49L26 -59L63 -22L74 -29L119 8Z',P.b,P.i,1.2)+P.p('M-10 -77L-23 -30L-3 -43L13 -21M26 -59L20 -33L33 -38M-69 -32L-75 -4',None,P.bg,2),x,y,k)
def donor(P,x,y,k=1):
    s=P.e(0,-84,10,13,P.c)+P.p('M-11 -87Q-13 -107 4 -105L12 -92Q-1 -99 -11 -87Z',P.i)+P.p('M-8 -68Q4 -76 11 -64L23 -37L10 -28L18 -4L-29 0L-17 -32Z',P.b)+P.p('M-1 -57L10 -43L23 -55M-8 -49L7 -37L24 -51',None,P.a,3)+P.p('M-13 -28L-19 -7M-2 -28L-5 -7M10 -24L10 -8',None,P.c,1.3)
    return place(s,x,y,k)
def moonphase(P,x,y,r,k):
    # 以晨昏线椭圆投影表示明暗，八相为示意（北半球常见示图方位）。
    base=P.o(x,y,r,P.bg,P.a,1.5)
    ph=(1-cos(2*pi*k/8))/2
    for j in range(-int(r),int(r)+1):
        half=math.sqrt(max(0,r*r-j*j));length=2*half*ph
        if length>.2:
            left=x+half-length if k<=4 else x-half
            base+=P.l(left,y+j,left+length,y+j,P.c,1.25)
    return base
def clipcell(poly_,a,b,c):
    res=[]
    for p,q in zip(poly_,poly_[1:]+poly_[:1]):
        f=a*p[0]+b*p[1]-c;g_=a*q[0]+b*q[1]-c
        if f<=0:res.append(p)
        if (f<0)!=(g_<0):
            t=f/(f-g_);res.append((p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t))
    return res
def voronoi(P,w,h,seed,count=42):
    rnd=random.Random(seed);sites=[(rnd.uniform(0,w),rnd.uniform(0,h))for _ in range(count)];o=''
    for j,(x,y) in enumerate(sites):
        pts=[(0,0),(w,0),(w,h),(0,h)]
        for X,Y in sites:
            if(x,y)!=(X,Y):pts=clipcell(pts,2*(X-x),2*(Y-y),X*X+Y*Y-x*x-y*y)
        o+=poly(pts,[P.bg,P.bg,P.b,P.c,P.a][(j*7)%5],P.i,1)+P.o(x,y,2,P.i,'none')
    return o
def lsystem(P,x,y,sz,seed):
    seq='X';rnd=random.Random(seed)
    for _ in range(4):seq=''.join({'X':'F[+X]F[-X]+X','F':'FF'}.get(ch,ch)for ch in seq)
    st=[];angle=-pi/2;o=''
    for ch in seq:
        if ch=='F':
            X=x+sz*cos(angle);Y=y+sz*sin(angle);o+=P.l(x,y,X,Y,P.a if len(st)>2 else P.i,max(.65,3-len(st)*.6));x,y=X,Y
        elif ch=='+':angle+=rnd.uniform(.27,.48)
        elif ch=='-':angle-=rnd.uniform(.27,.48)
        elif ch=='[':st.append((x,y,angle))
        elif ch==']':x,y,angle=st.pop()
    return o
def ca(P,w=640,h=400):
    row=[0]*101;row[50]=1;o=''
    for y in range(59):
        for x,v in enumerate(row):
            if v:o+=rect(19+x*5.9,17+y*6,5.9,6,P.a if y<23 else P.i if y<40 else P.b)
        row=[(row[i-1] if i>0 else 0)^(row[i+1] if i<100 else 0) for i in range(101)]
    return o
def scene(P,j):
    z=P.S['id'];i,a,b,c,bg=P.i,P.a,P.b,P.c,P.bg;rnd=random.Random(P.S['no']*79+j*601);o=P.paper()
    if z=='bauhaus':
        if j==0:return o+P.p('M0 151L139 53V124L296 41V111L451 34V100L640 21V317H0Z',c)+''.join(pane(P,17+k*150,155,121,106,4,2)for k in range(4))+P.r(0,306,640,17,i)+P.p('M80 311L152 261H337L285 311Z',a)+P.r(108,318,17,55,b)+P.r(255,317,15,52,b)
        if j==1:return o+P.r(34,48,572,279,b)+P.o(315,170,93,c)+P.p('M34 49L189 49L73 276Z',a)+P.p('M608 49H507L578 275Z',a)+P.r(25,316,591,19,i)+person(P,251,296,1.6)+person(P,409,290,1.35,1)+P.r(65,342,516,8,a)
        if j==2:
            o+=P.p('M0 300L640 133V174L0 341Z',i)
            for k in range(4):
                x=35+k*151;y=210-k*33;o+=P.p(f'M{x} {y}l75 -23l51 19l-75 26Z',c)+P.p(f'M{x} {y}v75l51 23v-76Z',a)+P.p(f'M{x+51} {y+24}l75 -26v74l-75 29Z',bg)+P.cols(x+65,y+28,4,15,24,b,0,5)
            return o
        return o+P.r(77,47,499,300,c)+P.r(120,82,179,209,bg)+P.p('M137 267L213 112L279 267Z',a)+P.o(226,186,40,b)+P.r(349,68,76,183,i)+P.p('M425 88H466V186H482',None,a,9)+P.cols(321,273,12,14,26,b,0,4)+P.l(90,334,558,334,i,3)
    if z=='art-deco':
        if j==0:return o+P.o(459,105,66,c)+staircity(P,5,319,631,280,rnd)+''.join(P.p(f'M0 {330+k*9}Q178 {314+k*10} 310 {332+k*9}T640 {328+k*9}',None,a if k%2 else b,1.2)for k in range(6))
        if j==1:
            o+=P.r(45,37,550,267,bg,a,3)
            for k in range(17):o+=poly([(320,290),polar(320,290,259,-pi/2+(k-8)*.094-.032),polar(320,290,259,-pi/2+(k-8)*.094+.032)],a if k%3 else b)
            return o+P.r(65,287,514,17,b)+''.join(P.p(f'M{27+k*62} 340q21 -26 41 0v35h-41Z',b,a,1.5)for k in range(10))+P.p('M48 35Q95 162 142 167L77 291H48ZM592 35Q553 162 498 167L565 291H592Z',b)
        if j==2:return o+''.join(arch(P,55+k*184,74,154,227,b) for k in range(3))+''.join(P.r(73+k*184,164,118,133,bg,a,2)+P.l(132+k*184,164,132+k*184,296,a,1.6)+ringticks(132+k*184,137,29,28,a)for k in range(3))+P.p('M0 385L220 306M160 400L271 306M474 400L369 306M640 378L423 306',None,a,1.3)
        return o+P.o(485,102,45,c)+staircity(P,3,243,630,153,rnd)+P.p('M77 236L480 230L557 217L524 279H131Z',i,a,2)+P.r(164,207,285,25,b)+P.r(196,182,193,24,bg,a,1.5)+P.p('M244 181L236 134H262L277 181M317 181L308 124H341L354 181',b)+P.bars(40,301,5,12,551,a,-4,.9)
    if z=='swiss':
        if j==0:return o+P.grid(31,37,575,314,12,6,b)+P.p('M50 305L177 178H324L461 59H592',None,a,12)+P.p('M61 81H218L345 225H585',None,i,10)+''.join(P.o(x,y,10,bg,i,3)for x,y in [(112,243),(177,178),(294,178),(389,121),(197,81),(345,225),(473,225)])+P.t(45,367,'03  /  07',21,i,'Arial')
        if j==1:return o+P.r(32,42,576,285,'none',b,1)+P.r(56,63,158,235,a)+P.t(65,182,'01',72,bg,'Arial')+P.r(230,63,158,235,bg)+P.cols(247,80,8,16,185,i,0,5)+P.r(404,63,178,235,i)+P.t(411,263,'A',130,bg,'Arial')+P.l(32,333,607,333,i,2)
        if j==2:return o+P.r(49,55,394,270,bg,i,2)+P.grid(63,72,363,234,9,6,b)+P.r(70,80,113,84,a)+P.r(195,82,224,22,i)+P.bars(198,122,9,13,203,i,0,1.5)+P.p('M466 308L566 77V308ZM524 265H548V210Z',c,i,2)+P.r(40,342,556,13,b)+P.cols(55,342,35,15,8,i)
        return o+P.t(31,136,'09',107,a,'Arial')+''.join(P.l(170,81+k*60,605,81+k*60,i,1)+P.r(177,52+k*60,230+((k*79)%171),20,[i,a,b][k%3])+P.t(179,96+k*60,[31,42,57,63,76][k],10,i,'monospace')for k in range(5))+P.p('M39 272H118M95 244L124 271L95 300',None,i,9)
    if z=='neo-brutalism':
        if j==0:return o+P.grid(0,0,640,400,8,5,b)+place(P.r(0,0,198,220,c,i,5)+P.t(15,118,'A!',80,i,'Arial')+P.bars(14,144,4,12,148,i,0,3),39,63,1,-7)+place(P.r(0,0,195,170,b,i,5)+star(90,76,58,32,11,a)+P.l(17,145,171,145,i,5),256,119,1,6)+P.p('M408 58H597V207L570 197L549 211L523 198L496 214L468 199L438 209L408 200Z',a,i,4)+P.t(423,157,'→',67,i,'Arial')
        if j==1:return o+P.r(22,278,593,31,i)+P.r(44,309,21,62,a)+P.r(564,309,21,62,a)+place(obj(P,2),16,104,.86)+P.p('M278 257L385 217L485 244L375 278Z',c,i,3)+P.r(422,125,109,72,b,i,4)+P.o(476,160,21,c,i,4)+P.l(254,93,566,93,i,5)+P.cols(298,94,5,54,39,a,0,2)
        if j==2:return o+P.o(507,91,46,c)+P.p('M9 286Q132 285 146 130H217V298H9ZM267 298L405 186H504L605 298Z',b,i,5)+P.p('M397 170H548M414 170V209M531 170V249',None,i,6)+P.p('M47 318H603M74 348L209 330M385 353L545 329',None,a,3)+person(P,345,183,.8)
        return o+''.join(P.r(x,y,w,h,co,i,5)+P.o(x+w*.5,y+h*.55,min(w,h)*.32,None,i,4)+P.o(x+w*.5,y+h*.55,min(w,h)*.12,i)for x,y,w,h,co in [(70,131,126,177,b),(194,190,134,119,c),(98,57,98,71,a),(365,96,167,213,a)])+P.p('M33 320H609M296 81L320 60L334 89L363 52',None,i,6)
    if z=='memphis':
        if j==0:return o+arch(P,52,56,185,185,b)+P.p('M76 240V157A68 68 0 0 1 211 157V240Z',bg)+P.p('M190 271Q296 182 420 218T589 256Q570 333 378 340T190 271Z',b)+P.p('M177 269Q288 181 417 207T601 252',None,a,10)+P.p('M491 201V125Q491 108 509 111V207M535 209V139Q535 126 552 129V217',None,i,4)+P.o(325,106,38,c)
        if j==1:return o+P.grid(24,30,596,295,7,4,c)+P.p('M65 201Q51 169 80 162H279Q310 165 303 201Q335 205 321 242H68Q42 211 65 201Z',a,i,3)+P.p('M82 242L70 286M284 242L295 286',None,i,7)+place(obj(P,0),348,116,.91)+P.o(507,86,35,b)+P.p('M509 121L478 183',None,i,5)
        if j==2:return o+P.r(38,307,564,14,i)+P.p('M90 307L162 182L235 307Z',b)+P.r(78,164,214,18,c,i,3)+P.o(221,121,42,a)+P.r(321,202,178,105,bg,i,3)+arch(P,361,226,90,80,b)+P.p('M310 198L348 154L386 196L422 145L457 194L500 139',None,a,8)
        return o+''.join(poly([(x,y),(x+61,y),(x+90,y+26),(x+24,y+26)],[a,b,c,bg][(k+l)%4],i,1)for l in range(4)for k in range(8)for x,y in [(k*79-40+l*13,230+l*31)])+P.p('M63 160Q105 31 150 106T247 105T343 102',None,b,17)+P.o(460,105,64,c)+P.cols(416,67,7,14,69,i,15,2)+star(100,167,23,9,5,a)
    if z=='editorial':
        if j==0:return o+book(P,39,45,559,278,bg)+P.r(75,87,101,153,b)+P.t(190,150,'Aa',46,i)+P.bars(190,175,6,11,87,i)+P.r(373,96,149,56,a)+P.bars(360,174,9,11,179,b)
        if j==1:return o+P.r(0,277,640,123,c,'none')+pane(P,28,28,190,179,3,3)+book(P,214,193,223,99,bg)+lamp(P,515,276,1.53)+P.p('M61 312Q109 290 164 307L187 340Q122 327 71 346Z',bg)+P.l(416,316,498,298,a,5)
        if j==2:return o+P.r(49,302,539,17,i)+P.r(110,91,14,210,b)+P.r(99,65,126,23,a)+P.p('M167 89H239L224 142H182Z',i)+P.p('M183 145L144 275H281L223 145',None,b,1.4)+P.r(125,276,172,11,bg)+P.r(389,247,122,46,c)+P.p('M373 95H551M396 95V115H446V164H391V115M485 95V119H533V174H479V119',None,i,2)
        return o+P.r(38,40,565,301,c,i,2)+''.join(P.r(54+x*80,56+y*66,72,57,bg,b,.8)+P.t(66+x*80,99+y*66,chr(65+(x+7*y)%26),29,i)for x in range(7)for y in range(4))+P.p('M428 332L530 307L542 323L440 350Z',a)
    if z=='wabi-sabi':
        if j==0:
            for k in range(21):o+=P.e(319,232,59+k*12,15+k*4,None,b,.8)
            return o+crag(P,304,225,1.32)+crag(P,411,236,.59)+crag(P,193,250,.42)+pine(P,87,209,1.12)
        if j==1:return o+P.r(50,49,269,267,bg,b,2)+P.r(83,69,191,177,None,b,1)+P.r(117,89,111,134,c,'none')+P.p('M161 201Q173 163 197 118M177 157L154 141',None,i,2)+P.r(35,310,572,16,a)+vessel(P,206,284,.66)+vessel(P,422,285,.88)+P.cols(370,62,6,39,172,b,0,1.4)
        if j==2:return o+P.e(313,284,150,36,b,i,2)+P.e(313,276,141,27,c)+P.p('M246 255Q249 225 271 200Q295 169 280 144Q267 119 285 105Q314 90 341 108Q356 121 348 143Q336 166 359 204Q385 236 377 258Q326 284 246 255Z',a)+P.e(315,107,30,9,bg)+''.join(P.p(f'M{267-j*2} {216+j*5}Q318 {233+j*5} {364+j} {214+j*5}',None,c,.9)for j in range(8))+P.l(308,319,308,362,i,7)
        return o+horizon(P,0,267,640)+P.p('M0 350Q154 242 301 299T640 259V400H0Z',c,'none')+''.join(P.p(f'M0 {349+k*8}Q153 {268+k*9} 303 {310+k*8}T640 {270+k*9}',None,b,1.1)for k in range(5))+bamboo(P,89,280,1.35)+bamboo(P,137,266,.93)+crag(P,446,311,.9)
    if z=='dark-academia':
        if j==0:return o+shelves(P,23,43,204,209,rnd)+shelves(P,416,43,198,209,rnd)+arch(P,253,31,138,196,b)+P.r(105,269,423,16,a)+P.cols(137,284,2,346,72,a,0,9)+book(P,234,222,138,44,bg)+lamp(P,393,263,.89)
        if j==1:
            for k in range(5):o+=arch(P,15+k*127,68,121,218,b)+arch(P,29+k*127,88,93,198,bg)+P.r(22+k*127,278,26,23,a)
            return o+P.p('M0 385L236 299M163 400L280 298M412 400L345 299M640 389L399 299',None,b,1)+P.bars(0,312,5,15,640,b)
        if j==2:return o+P.r(37,258,570,33,a)+place(obj(P,2),37,64,.93)+book(P,330,208,181,43,bg)+place(feather(b,i),375,46,.54)+P.r(238,195,54,63,bg,a,1.5)+P.e(265,197,25,7,c)+P.bars(47,310,3,14,540,b)
        return o+shelves(P,320,39,277,160,rnd,2)+P.r(15,291,609,25,a)+place(obj(P,0),33,83,1.05)+book(P,312,224,216,56,bg)+P.p('M347 151V185M393 151V184M441 151V186',None,c,1.7)
    if z=='celestial-atlas':
        if j==0:
            for k in range(27):o+=P.p(f'M{218-k*7} 25Q{244-k*9} {93+k*4} {378+k*6} {111+k*5}',None,b if k%4 else a,.8 if k%4 else 1.4)
            return o+P.p('M0 340Q125 238 235 304T501 286T640 306V400H0Z',b)+P.r(274,235,192,111,bg,a,2)+P.p('M257 236A115 115 0 0 1 487 236Z',bg,a,2)+P.p('M355 124Q394 173 404 236M367 122Q409 177 417 236',None,a,3)+P.r(345,282,43,64,bg,b)+P.bars(284,249,4,8,171,b)
        if j==1:
            for k in range(8):
                x=99+(k%4)*146;y=105+k//4*160;o+=moonphase(P,x,y,40,k)+P.t(x-30,y+65,['新月','蛾眉月','上弦','盈凸月','满月','亏凸月','下弦','残月'][k],15,i,'SimSun')
            return o+P.l(32,198,608,198,a,1)
        if j==2:
            o+=solar(P,63,191,1.55)+P.l(109,192,609,192,b,.8)
            for k,(name,r)in enumerate(zip(['水','金','地','火','木','土','天王','海王'],[5,10,11,7,29,23,16,15])):
                x=133+k*63;y=190+(-1 if k%2 else 1)*29;o+=P.l(x,192,x,y,b,.7)+P.o(x,y,r,[a,b,c][k%3],i,1)+P.t(x-12,272,name,14,i,'SimSun')
                if k==5:o+=g(P.e(x,y,36,8,None,c,2),f'rotate(-22 {x} {y})')
            return o+P.t(36,352,'轨道次序示意  /  大小、间距不按比例',13,a,'SimSun')
        for q in range(930):
            x=rnd.random()*640;y=89+sin(x/151)*36+x*.19+rnd.gauss(0,17+20*sin(x/190)**2);o+=circle(x,y,rnd.uniform(.4,1.7),[a,b,c,i][q%4])
        for k in range(14):o+=P.p(f'M{366-k*3} {283+k*.9}Q{418+k*2} {165+k*2} {477+k*3} 253T{589+k} {214-k}',None,b,.8)
        return o+P.t(33,358,'银河带与星云  /  艺术示意',14,a,'SimSun')
    if z=='dunhuang':
        if j==0:return o+cloud(P,95,101,.88)+cloud(P,514,97,.85)+apsara(P,255,191,1.09)+apsara(P,402,262,.81,True)+lotus(P,98,313,.46)+P.p('M21 345Q119 318 213 344T419 340T619 331',None,b,2)
        if j==1:return o+pavilion(P,318,202,1.5)+pavilion(P,107,230,.72)+pavilion(P,539,231,.72)+P.p('M35 312Q157 257 304 287T609 275Q599 343 416 351T35 312Z',b)+lotus(P,205,293,.45)+lotus(P,458,311,.52)+P.p('M52 254H589M60 264H582',None,a,3)+P.cols(68,243,14,38,29,c,0,3)
        if j==2:return o+P.r(28,59,203,214,c,a,2)+lotus(P,128,161,1.68)+P.r(244,263,366,31,a)+place(obj(P,2),279,64,1.1)+P.p('M447 235L543 126Q554 116 563 128L472 246Z',b)+P.r(314,300,12,56,b)+P.r(559,300,12,56,b)
        return o+P.r(24,36,592,282,'none',a,2)+pavilion(P,457,166,1.07)+''.join(donor(P,87+k*82,284,1.18-k*.065)for k in range(5))+lotus(P,530,250,.68)+''.join(place(cell(P.S),31+k*82,326,.97)for k in range(7))
    if z=='cartography':
        if j==0:
            o+=P.grid(24,26,592,345,8,5,b)+place(motif(P.S,1),39,64,.91)+place(motif(P.S,1),317,125,.63)+place(motif(P.S,0),467,13,.39)
            return o+P.p('M71 306Q168 260 251 269T398 228T553 250',None,a,2.2)+''.join(P.o(x,y,4,bg,i)for x,y in [(72,306),(251,269),(399,228),(551,250)])
        if j==1:
            for k in range(12):o+=rope(P,[(20+x*6,186+30*sin(x*.09+k*.04)+50*cos(x*.13)+k*4)for x in range(101)],a if k%4 else i,1.1)
            return o+mountain(P,198,160,.9)+mountain(P,397,159,.76)+P.l(30,301,608,301,i,1.6)+P.p('M32 295L121 279L191 230L239 260L281 238L343 285L388 253L476 225L535 275L609 293',None,b,2)
        if j==2:
            o+=P.p('M0 66Q162 58 225 156T420 211T640 290V400H0Z',b)
            for k in range(11):
                for l in range(3):
                    x=18+52*k;y=20+l*26+max(0,(k-2)*13);o+=P.r(x,y,32+(k%3)*4,16,bg,i,.8)
            return o+''.join(P.p(f'M{242+k*39} {200+k*4}l-17 43h9l18 -42',c,i,1)for k in range(6))+place(motif(P.S,0),487,266,.33)
        return o+P.grid(30,33,577,321,8,5,b)+P.p('M74 309L312 65L546 277ZM74 309L446 158L546 277M312 65L227 257L74 309',None,a,1.6)+''.join(P.o(x,y,8,bg,i,2)+P.t(x+15,y-11,lab,18,i)for x,y,lab in [(74,309,'A'),(312,65,'B'),(546,277,'C'),(446,158,'D')])+P.p('M66 351H221M66 344V358M116 344V358M171 344V358M221 344V358',None,i,1.5)
    if z=='natural-history':
        if j==0:return o+P.p('M0 316Q155 265 339 310T640 300V400H0Z',c,'none')+''.join(place(motif(P.S,0),x,y,k,ang)for x,y,k,ang in [(32,64,.85,-9),(206,38,.98,6),(386,100,.71,11)])+crag(P,508,327,.6)+P.t(29,366,'林下层  /  形态研究',13,i,'SimSun')
        if j==1:return o+P.p('M10 288Q175 284 305 207T598 139M247 235Q312 219 324 161M394 182L453 223',None,i,5)+bird(P,205,233,1.83)+bird(P,420,152,.85)+leaf(309,208,.7,36,a,i)+leaf(445,215,.8,82,b,i)+P.e(492,300,65,48,None,b)+place(feather(a,i),440,241,.37)
        if j==2:
            o+=P.p('M0 123Q105 95 226 118T440 109T640 119V400H0Z',c,'none')+P.p('M0 322Q113 272 258 321T460 314T640 283V400H0Z',a,'none')
            for x,y,k,rev in [(161,193,1.28,0),(312,245,.93,0),(462,166,1.11,1),(529,250,.49,1)]:o+=fish(P,x,y,k,rev)
            return o+P.p('M72 311Q97 265 70 237M81 306Q111 284 117 259M562 300Q546 279 570 252',None,b,3)
        for k in range(6):o+=P.p(f'M0 {173+k*27}Q135 {115+k*31} 277 {174+k*23}T640 {133+k*31}V400H0Z',[b,c,bg,a,c,b][k],i,.8)
        return o+place(motif(P.S,2),89,135,.42)+place(obj(P,0),414,169,.56)+P.p('M35 139L127 104L167 112L237 75L296 127L359 97L391 109L456 72L598 104',None,b,2)
    if z=='retrofuturism':
        if j==0:return o+place(motif(P.S,0),-11,16,.90)+P.e(407,223,169,69,None,b,7)+P.e(407,228,148,55,None,a,2)+place(obj(P,0),328,87,.88)+P.p('M345 284L318 348H287M473 268L512 319H565',None,c,6)
        if j==1:return o+P.o(490,103,62,a)+horizon(P,0,231,640)+P.p('M0 297Q256 241 640 237',None,i,10)+P.p('M0 304Q256 248 640 244',None,c,2)+P.cols(63,276,5,125,124,i,8,7)+place(obj(P,2),199,108,.98)
        if j==2:return o+P.r(32,43,575,235,bg,b,2,14)+pane(P,55,64,172,144,3,2)+place(motif(P.S,1),245,44,.63)+P.r(46,271,553,75,a)+''.join(P.o(89+j*43,305,11,bg,i,2)+P.l(89+j*43,305,93+j*43,298,c,1.3)for j in range(6))+P.bars(385,293,4,8,136,i,0,1.5)
        return o+P.o(497,89,42,a)+P.p('M0 279Q173 203 315 274T640 242V400H0Z',b)+P.p('M111 271A185 185 0 0 1 481 271Z',bg,c,3)+P.p('M173 271Q182 111 295 87Q411 119 424 271M112 220H479M136 165H453',None,c,2)+''.join(leaf(190+q*36,259,.8+q%2*.2,18*(q%3)-19,a,bg)for q in range(7))
    if z=='cyberpunk':
        if j==0:
            o+=skyline(P,8,264,630,211,rnd)+P.p('M0 0L139 60L185 281L0 379ZM640 22L495 83L461 275L640 350Z',bg,b,2)+P.p('M15 111L117 132V177L15 155ZM625 101L535 126V177L625 148Z',None,a,4)
            for q in range(70):
                x=rnd.randrange(640);y=rnd.randrange(400);o+=P.l(x,y,x-4,y+11,b,.6)
            return o+P.p('M49 400L226 280M569 400L433 279M175 348L261 307M382 348L430 359',None,a,2)
        if j==1:
            for k in range(4):
                x=39+k*150;o+=P.r(x,54,117,254,bg,b,2)+''.join(P.r(x+7,65+j*32,101,25,bg,i,.8)+P.l(x+16,77+j*32,x+63,77+j*32,a if j%2 else b,2)+P.o(x+96,77+j*32,2,c)for j in range(7))
            return o+P.p('M40 309V335H229L255 356H603M312 309V321H459L478 339H589',None,a,2)
        if j==2:return o+skyline(P,0,342,640,157,rnd)+P.p('M52 275H599V324H52Z',bg,b,2)+''.join(P.p(f'M{x-27} 275L{x} {h}L{x+24} 275ZM{x-16} 230L{x+15} 212M{x-11} 192L{x+11} 174',None,a,2)+P.o(x,h-6,4,c)for x,h in [(125,105),(306,47),(485,131)])+P.p('M123 156Q197 221 303 132Q397 240 484 192',None,b,1.6)
        return o+P.p('M0 311L263 212H640V262L141 381H0Z',b)+P.r(10,99,596,101,bg,a,2)+''.join(pane(P,28+k*83,113,62,51,2,1)for k in range(7))+P.p('M0 278H638M0 306H638',None,a,2)+P.r(443,38,109,29,i)+P.t(455,58,'N / 04',15,bg,'monospace')+person(P,327,293,.8)
    if z=='blueprint':
        o+=P.grid(13,15,610,367,23,14,b)
        if j==0:return o+P.p('M34 197H605',None,c,1)+engine(P,109,198,1.25)+P.r(194,171,74,53,bg,i,2)+engine(P,354,196,1.51)+P.p('M444 162H516L548 181V214L516 233H444Z',bg,i,2)+P.r(535,187,57,20,bg,i,2)+P.p('M108 121V90H351V112M108 90L117 85M351 90L342 95',None,c,1.5)
        if j==1:return o+P.p('M49 294V141L187 73V133L326 68V130L477 61V124L581 77V294ZM39 302H601',None,i,3)+''.join(P.r(x,150,9,141,None,i)+struts(P,x,148,124,28,6)for x in [56,193,331,465])+P.p('M39 334H592M41 322V344M590 321V345',None,c,1.3)+P.t(274,353,'A : A',15,i,'monospace')
        if j==2:return o+P.p('M45 290H171V184H469V89H583M175 184V94H242M316 184V297H397',None,b,19)+P.p('M45 290H171V184H469V89H583M175 184V94H242M316 184V297H397',None,bg,12)+''.join(P.r(x-3,y-13,6,26,bg,i)for x,y in [(65,290),(247,184),(410,184),(557,89)])+''.join(P.p(f'M{x-16} {y-9}l32 18v-18l-32 18Z',bg,c,2)for x,y in [(327,184),(218,94),(365,297)])
        return o+P.p('M70 124H146M151 124L199 92M209 124H263L275 112L289 136L303 112L317 136L331 124H454V183M431 184H478M431 195H478M454 195V266H71V192M61 185H82M54 174H90M71 173V124',None,i,3)+''.join(P.o(x,y,4,c)for x,y in [(146,124),(207,124),(454,124),(454,266)])+P.t(150,78,'S1',15,c,'monospace')+P.t(278,92,'R1',15,c,'monospace')+P.t(486,194,'C1',15,c,'monospace')+P.t(45,343,'原理连线示意 / 非施工图',14,i,'SimSun')
    if j==0:return o+place(voronoi(P,570,320,724),35,37)
    if j==1:return o+lsystem(P,163,354,6.2,718)+lsystem(P,348,354,4.8,14)+lsystem(P,473,354,5.7,730)+P.l(35,355,605,355,b,.8)
    if j==2:return o+ca(P)
    for k in range(78):
        x,y=5,rnd.uniform(20,380);ps=[]
        for t in range(140):
            ps.append((x,y));x+=4.55;y+=1.7*sin(x*.018+y*.014)+1.1*cos(y*.023-x*.012)
        o+=curve(ps,[i,a,b][k%3],1.1)+''.join(P.o(xx,yy,1.7,c,'none')for xx,yy in ps[::31])
    return o
def make():
    for S in STYLES:
        z=S['id'];rows=[]
        for j,title in enumerate(SCENES[z]):
            r=item(z,'illustrations','scene-'+str(j+1),title,'完整原创场景或主题图。'+('科学次序或形态示意；无精确比例、轨道或观测能力。' if z in ['blueprint','celestial-atlas','natural-history'] else '现代构成，非对历史原件的复原。'),[1,0,2,1][j],'scene',alpha=False)
            write(outfile(z,r),svg(1600,1000,scene(Pen(S),j),'640 400'));rows.append(r)
        save_batch(z,'scenes',rows)
    report()
if __name__=='__main__':make()
