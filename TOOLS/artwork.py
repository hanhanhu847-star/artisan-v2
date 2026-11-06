"""原创 SVG 画版。以 300 单位的母题和独立构成规则生成可编辑矢量。"""
import math,random,html
from styles_data import *
sin,cos,pi=math.sin,math.cos,math.pi
def n(v):return f'{v:.2f}'.rstrip('0').rstrip('.') if isinstance(v,float) else str(v)
def g(s,t):return f'<g transform="{t}">{s}</g>'
def path(d,c='none',st='none',w=1,ex=''): return f'<path d="{d}" fill="{c}" stroke="{st}" stroke-width="{n(w)}" {ex}/>'
def rect(x,y,w,h,c,st='none',sw=1,r=0):return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{r}" fill="{c}" stroke="{st}" stroke-width="{sw}"/>'
def circle(x,y,r,c,st='none',w=1):return f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{c}" stroke="{st}" stroke-width="{n(w)}"/>'
def ell(x,y,rx,ry,c,st='none',w=1):return f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(rx)}" ry="{n(ry)}" fill="{c}" stroke="{st}" stroke-width="{n(w)}"/>'
def line(x,y,X,Y,c,w=1):return path(f'M{n(x)} {n(y)}L{n(X)} {n(Y)}','none',c,w)
def points(xy):return ' '.join(f'{n(x)},{n(y)}' for x,y in xy)
def poly(xy,c,st='none',w=1):return f'<polygon points="{points(xy)}" fill="{c}" stroke="{st}" stroke-width="{w}"/>'
def curve(xy,c,w=1):return f'<polyline points="{points(xy)}" fill="none" stroke="{c}" stroke-width="{n(w)}" stroke-linejoin="round"/>'
def txt(x,y,t,size,c,font='sans-serif',extra=''):return f'<text x="{n(x)}" y="{n(y)}" font-family="{font}" font-size="{n(size)}" fill="{c}" {extra}>{html.escape(str(t))}</text>'
def svg(w,h,body,v=None):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {v or (str(w)+" "+str(h))}">{body}</svg>'
def stamp(b,x,y,k=1,rot=0):return g(b,f'translate({n(x)} {n(y)}) scale({n(k)}) rotate({rot} 150 150)')
def star(x,y,R,r,k,c):return poly([(x+(R if i%2==0 else r)*cos(i*pi/k-pi/2),y+(R if i%2==0 else r)*sin(i*pi/k-pi/2)) for i in range(k*2)],c)
def polar(x,y,r,a):return(x+r*cos(a),y+r*sin(a))
def ringticks(x,y,r,num,c):return ''.join(line(*polar(x,y,r-(8 if i%5==0 else 4),i*2*pi/num),*polar(x,y,r,i*2*pi/num),c,1.4 if i%5==0 else .7) for i in range(num))
def leaf(x,y,sz,ang,c,vein):
    return g(path('M0 0Q-19 -13 0 -45Q16 -24 0 0Z',c)+line(0,-2,0,-37,vein,.9),f'translate({n(x)} {n(y)}) rotate({ang}) scale({sz})')
def feather(c,i):
    o=path('M62 256Q111 132 240 36Q233 106 171 147L157 145 151 161Q114 198 85 204Z',c,i,1.4)+path('M56 271Q129 153 226 56','none',i,2)
    for j in range(17):
        t=j/18;x=87+125*t;y=202-125*t;o+=line(x,y,x+4+17*t,y-29+13*t,i,.8)+line(x,y,x+25-12*t,y-7,i,.7)
    return o
def motif(S,v=0):
    bg,ink,a,b,c=S['palette'];z=S['id'];rnd=random.Random(S['no']*101+v);o=''
    if z=='bauhaus':
        if v==0:return rect(58,111,48,144,ink)+rect(106,184,136,71,a)+path('M43 112A102 102 0 0 1 247 112Z',b)+circle(174,151,29,c)+rect(38,258,226,6,ink)
        if v==1:return poly([(28,241),(135,58),(242,241)],a)+circle(186,109,64,c)+rect(64,200,199,24,ink)+rect(93,224,29,41,b)
        return ''.join(path(f'M{40+33*j} 242V{100+13*j}A{75-15*j} {75-15*j} 0 0 1 {190+3*j} {100+13*j}V242','none',[a,b,ink,c][j],18) for j in range(4))
    if z=='art-deco':
        if v==0:
            for j in range(17):
                t=(-80+j*10)*pi/180;o+=poly([(150,248),polar(150,248,188,t-pi/2-.06),polar(150,248,188,t-pi/2+.06)],[a,b][j%2],ink,.8)
            return o+path('M117 245V209H130V185H142V165H158V185H170V209H183V245Z',bg,a,2)
        if v==1:
            for j in range(5):o+=rect(40+j*23,170-j*26,220-j*46,94+j*26,[b,bg][j%2],a,2)
            return o+line(150,30,150,258,a,2)+''.join(line(51+10*j,185,51+10*j,252,a,.9)for j in range(21))
        return ringticks(150,150,116,72,a)+circle(150,150,94,'none',a,3)+star(150,150,86,35,16,a)+circle(150,150,36,bg,a,2)
    if z=='swiss':
        if v==0:return txt(9,214,'63',178,ink,'Arial','font-weight="700" letter-spacing="-16"')+rect(19,230,249,9,a)+rect(19,250,80,4,ink)
        if v==1:return ''.join(rect(40+i*26,48+(i%3)*21,12 if i%2 else 21,183-(i%4)*29,[ink,a,b][i%3])for i in range(8))+line(30,255,270,255,ink,3)
        return ''.join(rect(41+j*51,41+i*51,45,45,[a,ink,b][(i+j)%3]) for i in range(4)for j in range(4) if j<=i)+txt(208,98,'04',30,ink)
    if z=='neo-brutalism':
        if v==0:
            p=[(28,116),(167,116),(167,62),(272,157),(167,253),(167,192),(28,192)];return g(poly(p,ink),'translate(8 9)')+poly(p,a,ink,7)+line(47,141,130,141,bg,8)
        if v==1:return g(star(150,146,126,88,10,ink),'translate(7 11)')+star(150,146,126,88,10,c)+path('M105 149L140 180L204 111','none',ink,14)
        return rect(40,73,220,165,ink)+rect(29,57,220,165,b,ink,6)+circle(48,77,5,ink)+circle(232,77,5,ink)+txt(61,175,'02!',79,ink,'Arial','font-weight="900"')
    if z=='memphis':
        if v==0:return path('M48 215Q47 96 109 100T174 200T249 77','none',ink,32)+path('M44 210Q43 91 105 95T170 195T245 72','none',a,22)+circle(219,203,32,c)+poly([(45,92),(87,43),(102,112)],b,ink,3)
        if v==1:return ''.join(circle(54+j*31+(i%2)*10,60+i*30,4+(i+j)%6,[ink,b,a][(i+j)%3]) for i in range(6)for j in range(6) if (j-2.3)**2+(i-2.3)**2<10)+poly([(160,217),(230,120),(265,238)],c,ink,3)
        return curve([(30+j*30,102+(j%2)*77)for j in range(9)],ink,20)+curve([(30+j*30,95+(j%2)*77)for j in range(9)],b,12)+circle(69,223,24,a)+rect(191,54,48,18,c,ink,2)
    if z=='editorial':
        if v==0:return txt(34,230,'R',253,ink,'Georgia')+circle(203,85,30,'none',a,2)+line(25,246,274,246,a,1)+txt(39,266,'PLATE   /   RECTO',11,ink)
        if v==1:return path('M55 63Q110 57 149 82Q202 54 251 64V233Q196 224 149 251Q106 226 55 232Z',c,ink,2)+line(149,81,149,245,ink,2)+''.join(path(f'M68 {89+j*13}Q110 {85+j*13} 137 {103+j*13}M164 {103+j*13}Q196 {89+j*13} 236 {86+j*13}','none',ink,.8)for j in range(9))
        return txt(40,176,'“',178,a,'Georgia')+line(40,184,258,184,ink,1)+''.join(rect(42,204+j*13,190-j*25,2,ink) for j in range(4))
    if z=='wabi-sabi':
        if v==0:
            o=path('M36 122Q137 104 268 120Q258 199 196 216L180 231L112 228L97 213Q53 207 36 122Z',a)+path('M38 122Q150 143 266 120','none',ink,4)
            return o+''.join(path(f'M{57+j*2} {153+j*5}Q143 {184+j*5} {248-j*3} {150+j*5}','none',b if j%3 else ink,1)for j in range(9))+ell(148,236,57,4,b)
        if v==1:return path('M51 254Q137 169 230 44M109 188L87 115M148 144L214 125M181 102L168 61','none',ink,5)+''.join(leaf(x,y,.48,ang,b,ink)for x,y,ang in [(93,136,-30),(110,185,35),(169,130,68),(215,125,95),(185,101,45),(172,77,-35)])
        return path('M35 214Q55 130 106 137Q150 132 168 213Q97 239 35 214Z',b)+path('M119 196Q149 80 192 93Q254 106 271 192Q204 212 119 196Z',a)+path('M155 153Q191 120 228 131','none',bg,2)
    if z=='dark-academia':
        if v==1:return feather(a,ink)
        if v==2:return rect(57,40,185,222,bg,a,2)+rect(65,48,169,206,'none',a,1)+ell(149,143,53,67,'none',a,2)+g(feather(b,ink),'translate(93 87) scale(.38)')+txt(91,225,'EX  LIBRIS',17,ink,'Georgia')
        for j,(x,y,w,h)in enumerate([(40,61,47,180),(90,44,43,197),(136,78,48,163),(189,55,49,186)]):
            o+=rect(x,y,w,h,[b,c,bg,a][j],a,2)+''.join(rect(x+2,yy,w-4,3,ink)for yy in [y+12,y+18,y+h-25])+rect(x+8,y+48,w-16,37,bg,a,1)+line(x+14,y+62,x+w-14,y+62,a,1)
        return o+rect(28,244,232,9,a)
    if z=='celestial-atlas':
        if v==0:
            o=circle(150,150,119,'none',a,2)+ringticks(150,150,115,90,a)
            for j in (32,59,86,102):o+=circle(150,150,j,'none',b,.7)
            for j in range(12):o+=line(150,150,*polar(150,150,101,j*pi/6),b,.5)
            pts=[(rnd.randint(85,216),rnd.randint(78,224))for j in range(9)]
            return o+curve(pts,a,1.2)+''.join(star(x,y,4,1.5,4,ink)for x,y in pts)
        if v==1:return ''.join(g(ell(150,150,117,37,'none',[a,b,ink][j],1.4),f'rotate({j*47} 150 150)')for j in range(3))+circle(150,150,18,c)+circle(237,171,8,a)
        return star(150,150,115,23,8,a)+star(150,150,58,18,8,bg)+circle(150,150,11,ink)+ringticks(150,150,125,36,b)
    if z=='dunhuang':
        if v==0:
            for j in range(8):o+=g(path('M150 158Q99 112 150 43Q198 112 150 158Z',b,ink,2)+path('M150 137Q130 106 150 73Q170 106 150 137Z',c,a,1.5),f'rotate({j*45} 150 150)')
            return o+circle(150,150,27,a,ink,2)+circle(150,150,14,c)+ringticks(150,150,121,48,a)
        if v==1:return ''.join(g(path('M150 228C49 190 49 87 104 83C147 79 141 137 109 122Q94 104 114 99','none',[a,b,ink][j],7),f'rotate({j*120} 150 150)')for j in range(3))+circle(150,150,13,c)
        return ''.join(poly([(150,150-r),(150+r,150),(150,150+r),(150-r,150)],col,ink,2)for r,col in [(123,b),(103,c),(91,a),(77,bg),(54,b)])+star(150,150,38,16,8,c)
    if z=='cartography':
        if v==0:return circle(150,150,105,'none',a,1.6)+ringticks(150,150,113,64,ink)+''.join(g(poly([(150,37 if j%2==0 else 76),(163,150),(150,142)],ink)+poly([(150,37 if j%2==0 else 76),(137,150),(150,142)],c),f'rotate({j*45} 150 150)')for j in range(8))+circle(150,150,8,a)
        if v==1:
            for j in range(8):
                ps=[(148+(107-j*10)*(1+.21*sin(t*3)+.13*cos(t*7))*cos(t),146+(81-j*7)*(1+.18*cos(t*5))*sin(t))for t in [i*pi/110 for i in range(221)]]
                o+=curve(ps,b if j<2 else a,1.6 if j==2 else .9)
            return o
        return ''.join(line(49,219,*polar(49,219,202,j*pi/28-pi/2),b,.8) for j in range(13))+path('M51 216Q119 92 230 67','none',ink,3,'stroke-dasharray="7 5"')+circle(52,217,9,a)+star(228,66,16,5,4,a)
    if z=='natural-history':
        if v==0:
            o=path('M100 275Q140 180 185 37','none',ink,2.5)
            for j in range(13):
                t=j/14;x=108+72*t;y=248-191*t;k=1.2*(1-.63*t)
                o+=leaf(x,y,k,-55-j*.7,a,ink)+leaf(x+3,y-7,k,58-j*.6,b,ink)
            return o
        if v==1:
            o=ell(150,164,48,70,a,ink,2)+ell(150,100,33,22,ink)+ell(150,72,21,16,b,ink,1)+line(150,114,150,230,ink,1.5)
            for sign in [-1,1]:
                o+=curve([(150+sign*12,63),(150+sign*30,38),(150+sign*43,32)],ink,2)
                for j in range(3):o+=curve([(150+sign*31,118+j*26),(150+sign*(60+j*5),107+j*36),(150+sign*(79+j*7),84+j*52)],ink,3)
                for j in range(4):o+=g(ell(150+sign*(8+j*8),172,2,35-j*5,'none',ink,.7),f'rotate({sign*-5} 150 160)')
            return o
        ps=[(150+3.2*t*cos(t),153+3.2*t*sin(t))for t in [i*.065 for i in range(420)]]
        return curve(ps,ink,3)+''.join(line(*ps[i],*ps[max(0,i-97)],a,.7)for i in range(110,420,5))
    if z=='retrofuturism':
        if v==0:return g(ell(150,150,126,29,'none',c,8),'rotate(-23 150 150)')+circle(150,145,69,a)+''.join(path(f'M{102+j*2} {110+j*12}Q145 {128+j*12} {200-j} {102+j*12}','none',b,3)for j in range(6))+g(path('M24 150A126 29 0 0 0 276 150','none',c,8),'rotate(-23 150 150)')
        if v==1:return rect(51,50,198,192,b,ink,3,48)+rect(66,65,168,144,bg,c,4,45)+circle(157,128,28,a)+star(112,97,6,2,4,ink)+rect(96,222,110,5,ink)
        return path('M25 192L101 124L139 162L187 98L275 193Z',b)+circle(132,89,31,a)+''.join(line(150,186,j*49-20,260,c,1.6) for j in range(8))+''.join(line(24,190+j*j*3,275,190+j*j*3,c,1.5)for j in range(5))
    if z=='cyberpunk':
        if v==0:
            for j in range(7):
                x=20+j*37;y=rnd.randint(65,170);o+=rect(x,y,34,250-y,bg,a,1.5)+line(x+17,y-25,x+17,y,b,2)
                for k in range(int((235-y)/14)):o+=rect(x+5+(k%2)*7,y+8+k*14,9 if k%2 else 21,3,[b,a,c][(k+j)%3])
            return o+line(16,255,285,255,a,2)
        if v==1:return path('M50 53H152L174 77V146L199 167H251V232H184L129 179V103H50Z',a,ink,2)+path('M51 71H141L151 85V157L187 194H249','none',bg,4)+circle(76,70,7,b)
        return poly([(41,88),(61,62),(251,62),(251,207),(225,235),(41,235)],bg,a,4)+''.join(rect(60+i*15,95,8,30+(i%4)*12,[b,a][i%2])for i in range(12))+rect(59,190,112,7,c)
    if z=='blueprint':
        if v==0:
            o=path('M30 134H72V111H95V98H136V120H172V91H212V117H234V134H270V170H234V185H212V201H172V181H136V197H95V181H72V170H30Z','none',ink,2)
            for x in [72,95,136,172,212,234]:o+=line(x,108 if x%2 else 119,x,184,a,1)
            return o+path('M15 151H283','none',b,1,'stroke-dasharray="10 4 2 4"')+line(30,220,270,220,c,1)+path('M30 204V232M270 204V232M38 216L30 220 38 224M262 216L270 220 262 224','none',c,1)
        if v==1:return circle(150,150,103,'none',ink,2)+circle(150,150,74,'none',a,2)+circle(150,150,31,'none',ink,2)+''.join(circle(*polar(150,150,90,j*pi/4),6,'none',a,2)for j in range(8))+line(23,150,277,150,b,1)+line(150,24,150,276,b,1)
        ps=[polar(150,150,105 if j%4 in [1,2] else 92,j*pi/32)for j in range(64)]
        return poly(ps,'none',ink,2.5)+circle(150,150,65,'none',a,2)+circle(150,150,25,'none',ink,2)+ringticks(150,150,118,48,b)
    # 不同的流场、涡线、采样阵列
    if v==0:
        for j in range(52):
            ps=[(18+i*3.6,60+j*3.5+24*sin(i*.083+j*.051)+18*cos(i*.033-j*.082))for i in range(74)];o+=curve(ps,[ink,a,b][j//18%3],1.6)
    elif v==1:
        for j in range(53):o+=curve([polar(150,150,27+1.32*i+6*sin(i*.08+j*.09),j*2*pi/53+i*.017)for i in range(68)],[ink,a,b][j%3],1.6)
    else:
        for r in range(15):
            for k in range(15):
                t=sin(r*.45+k*.2);x=37+k*16+7*t;y=35+r*16+6*cos(k*.4);o+=circle(x,y,1.2+(1+t)*2.2,[a,b,ink][(k//5+r//6)%3])
    return o
def cover(S,w,h,mode='light'):
    bg,ink,a,b,c=S['palette'];p=S.copy()
    if mode=='dark' and sum(int(bg[i:i+2],16)for i in (1,3,5))>360:p['palette']=[ink,bg,a,b,c]
    if mode=='light' and sum(int(bg[i:i+2],16)for i in (1,3,5))<360:p['palette']=[ink,bg,a,b,c]
    bg,ink,a,b,c=p['palette'];W=1000.;H=1000*h/w;land=W/H>1.3
    o=rect(0,0,W,H,bg);kind=S['id']
    if kind in ['blueprint','swiss','bauhaus','generative-art']:
        o+='<g opacity=".13">'+''.join(line(i,0,i,H,b,1)for i in range(15,1000,45))+''.join(line(0,j,W,j,b,1)for j in range(15,int(H),45))+'</g>'
    elif kind in ['art-deco','cartography','celestial-atlas','dark-academia','dunhuang','natural-history']:
        o+=rect(16,16,W-32,H-32,'none',a,1.5)+rect(23,23,W-46,H-46,'none',b,.7)
        for x,y in [(35,35),(965,35),(35,H-35),(965,H-35)]:o+=circle(x,y,2,a)
    elif kind in ['memphis','neo-brutalism']:
        o+=poly([(0,H*.74),(W*.26,H),(0,H)],c)+''.join(circle(55+i*20,68+j*20,2.6,ink)for i in range(8)for j in range(3))
    elif kind in ['retrofuturism','cyberpunk']:
        o+='<g opacity=".38">'+''.join(line(0,H*.70+j*j*1.3,W,H*.70+j*j*1.3,b,1)for j in range(12))+''.join(line(W*.5,H*.64,i*W/7,H,a,.8)for i in range(-4,13))+'</g>'
    else:o+=line(39,H*.12,960,H*.12,ink,.85)+line(39,H*.91,960,H*.91,ink,.85)
    k=min(2.08,H/330) if land else min(2.55,H/460)
    x=W*.65-150*k if land else W*.5-150*k
    y=H*.50-150*k if land else H*.39-150*k
    # 主题主图与第二幅独立细部；背景无伪史料或占位正文
    o+=stamp(motif(p,0),x,y,k)
    ks=min(.65,H/670) if land else min(.91,H/900)
    o+=stamp(motif(p,1),W*.12 if land else W*.14,H*.30 if land else H*.66,ks)
    o+=line(45,H-65,226,H-65,ink,1.4)+txt(45,H-42,f'AT / {S["no"]:02d}     STUDY  I',12,ink,'monospace','letter-spacing="1.8"')
    return svg(w,h,o,f'1000 {n(H)}')
