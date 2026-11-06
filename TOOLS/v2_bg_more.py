"""自然、人文和数字艺术分册的大画板图案。"""
from v2_scenes import *
from v2_bg_technical import tech
def more(P,j,W,H,o,rnd):
    x=W/2;y=H/2;z=P.S['id'];i,a,b,c,bg=P.i,P.a,P.b,P.c,P.bg
    def ref(k,X,Y,s):return place(motif(P.S,k),X-s/2,Y-s/2,s/300)
    def ob(k,X,Y,s):return place(obj(P,k),X-s/2,Y-s/2,s/240)
    def radial(X,Y,N,fun):return ''.join(g(fun(k),f'translate({X} {Y}) rotate({k*360/N})')for k in range(N))
    def gradgrid(nx,ny):return '<g opacity=".32">'+P.grid(20,18,W-40,H-36,nx,ny,b)+'</g>'
    def leafset(X,Y,N,k):
        return ''.join(leaf(X+rnd.uniform(-24,24),Y+rnd.uniform(-21,19),k*rnd.uniform(.6,1.1),rnd.randrange(0,360),[a,b,c][q%3],i)for q in range(N))
    if z=='wabi-sabi':
        if j==0:
            for k in range(26):o+=rope(P,[(t*W/90,230+k*7+22*sin(t*.09+k*.13)+12*cos(t*.16))for t in range(91)],b,.9)
            o+=crag(P,W*.27,307,1.35)+crag(P,W*.70,376,.72)
        if j==1:o+=''.join(P.e(W*.63,364,57+k*14,16+k*4.3,None,b,.8)for k in range(24))+crag(P,W*.62,348,1.6)+pine(P,100,298,1.42)
        if j==2:o+=P.l(W*.05,419,W*.95,419,a,1.2)+''.join(vessel(P,150+k*191,348-26*(k%2),.76+(k%3)*.24)+P.e(150+k*191,417,56,3,b,'none')for k in range(5))
        if j==3:o+=pane(P,34,50,W-68,344,3,4)+bamboo(P,98,510,2.1)+leaf(190,310,1.08,90,a,i)
        if j==4:
            for k in range(40):o+=rope(P,[(57+k*5+15*sin(t*.08+k*.14)+5*cos(t*.2),31+t*6.9)for t in range(77)],b if k%5 else a,.7 if k%5 else 1.7)
            o+=crag(P,201,526,1.42)
        if j==5:o+=''.join(P.e(284,323,32+k*20,13+k*9,None,b,1)for k in range(12))+leafset(341,283,6,.87)+P.e(164,391,26,12,a)
        if j==6:o+=P.r(66,74,464,440,c,a,1,5)+P.e(224,241,97,91,bg,i,2)+P.e(225,238,76,70,b,a,1.8)+P.e(222,235,66,60,a,i,1)+P.p('M390 158Q418 179 410 213L394 398L379 399L388 212Q374 178 390 158Z',b)+P.r(154,408,141,12,bg)
        if j==7:
            for k in range(3):o+=rope(P,[(t*W/130,303+k*51+58*sin(t*.085+k)+22*cos(t*.21+k*.9))for t in range(131)],[b,a,i][k],1+k*.5)
            o+=pine(P,W*.87,380,1.55)+P.o(W*.23,132,37,c,'none')
        if j==8:o+=''.join(bamboo(P,53+k*169,376+(k%3)*17,1.26+(k%4)*.18)for k in range(13))+''.join(P.p(f'M0 {291+k*21}Q{W*.26} {240+k*18} {W*.48} {293+k*20}T{W} {270+k*21}',None,b,.9)for k in range(5))
    elif z=='dark-academia':
        if j==0:o+=shelves(P,46,90,W-92,394,rnd,3)+P.r(39,489,W-78,14,a)
        if j==1:
            o+=''.join(arch(P,55+k*248,66,196,337,b)+arch(P,69+k*248,87,168,317,bg)+P.l(152+k*248,86,152+k*248,398,a,2)+P.l(74+k*248,233,231+k*248,233,a,2)for k in range(4))+lamp(P,W*.47,433,1.36)
        if j==2:
            for l in range(3):
                for k in range(6):
                    xx=45+k*163;yy=63+l*148;o+=P.r(xx,yy,151,130,[b,bg][(k+l)%2],a,1.2)+P.r(xx+27,yy+31,99,27,bg,a,1)+P.e(xx+76,yy+86,22,7,'none',a,2)
        if j==3:o+=arch(P,39,37,W-78,447,b)+arch(P,55,66,W-110,407,bg)+P.r(x-13,333,26,132,c,i,1.7)+P.p(f'M{x} 329q-20 -27 2 -54q21 32 -2 54Z',a)+P.e(x,472,63,12,a)+P.l(34,503,W-34,503,a,2)
        if j==4:o+=shelves(P,20,30,W-40,499,rnd,5)+P.p('M38 574L201 72M91 574L255 72',None,a,6)+''.join(P.l(55+k*18,520-k*55,106+k*18,520-k*55,i,5)for k in range(8))
        if j==5:o+=P.r(24,24,552,552,'none',a,2)+P.r(36,36,528,528,None,a,1)+P.e(x,y,153,189,None,a,2)+P.e(x,y,135,172,None,b,1)+radial(x,y,7,lambda k:leaf(0,-26,.98,0,b,a))+P.t(208,496,'EX   LIBRIS',26,a)
        if j==6:o+=P.r(37,36,526,526,c)+P.r(78,84,346,399,bg,a,2)+P.l(119,86,119,483,a,6)+P.bars(141,223,12,14,237,i)+P.p('M435 102L479 80L532 451L490 471Z',b)+P.l(469,153,503,410,a,1.5)
        if j==7:o+=''.join(arch(P,18+k*227,53,206,423,b)+arch(P,34+k*227,76,174,400,bg)+P.r(22+k*227,470,30,36,a)for k in range(10))+P.l(0,509,W,509,a,2)
        if j==8:o+=''.join(P.p(f'M{90+k*258} 416V258q7 -110 84 -110q82 2 89 109v159Z',None,a,2)+ref((k+1)%3,178+k*258,294,164)+P.e(178+k*258,421,94,10,b)for k in range(8))
    elif z=='celestial-atlas':
        if j==0:
            for k in range(12):
                xx=27+k*84;yy=257+85*sin(k*pi/6);o+=P.l(xx,yy-41,xx+44,yy+35,b,.9)+P.o(xx+20,yy,21,None,a,1.3)+P.t(xx+10,yy+6,str(k+1).zfill(2),15,i,'Georgia')
            o+=rope(P,[(t*W/150,257+85*sin(t/150*2*pi))for t in range(151)],a,1.5)+P.bars(39,427,2,7,W-78,a)
        if j==1:o+=P.o(W*.65,300,236,None,a,2)+ringticks(W*.65,300,227,144,a)+''.join(P.o(W*.65,300,r,None,b,.85)for r in [44,82,120,163,201])+radial(W*.65,300,24,lambda k:P.l(0,-32,0,-204,b,.6))+P.p('M84 355L237 122L347 359ZM97 358Q203 431 336 361',None,a,2)
        if j==2:
            for k in range(129):
                xx=rnd.uniform(0,W);yy=rnd.uniform(53,550);dx=xx-W*.29;dy=yy-201;f=rnd.uniform(.018,.13);o+=P.l(xx,yy,xx+dx*f,yy+dy*f,[a,b,i][k%3],rnd.uniform(.35,1.7))+P.o(xx+dx*f,yy+dy*f,rnd.uniform(.4,1.8),c,'none')
            o+=P.o(W*.29,201,13,None,b,1)+P.o(W*.29,201,22,None,b,.6)
        if j==3:o+=P.p('M52 451L185 91L251 113L118 476ZM176 80L198 43L274 70L258 122ZM59 456L40 487L85 509L110 469Z',b,a,2)+P.p('M125 307L155 331L75 548M155 331L247 544M155 331L154 559',None,a,4)+P.cols(68,118,4,8,125,b,0,.9)
        if j==4:o+=P.p('M49 521V86A431 431 0 0 1 320 414L49 521Z',None,a,2)+''.join(P.l(49,521,49+cos(-pi/2+k*.046)*243,521+sin(-pi/2+k*.046)*243,b,.85)for k in range(25))+P.l(49,521,269,169,c,3)+P.o(49,521,12,bg,a,2)
        if j==5:o+=P.o(x,y,233,None,a,2)+ringticks(x,y,249,180,b)+''.join(P.e(x,y,abs(cos(k*pi/12))*228+1,228,None,b,1.0)for k in range(7))+''.join(P.e(x,y+sin(k*pi/12)*228,cos(k*pi/12)*228,8,None,b,.8)for k in range(-5,6))+P.l(46,306,551,294,a,1.6)
        if j==6:
            o+=P.o(x,y,230,bg,a,2)+P.o(x,y,222,None,b,1)
            for k in range(75):
                theta=rnd.uniform(0,2*pi);rr=math.sqrt(rnd.random())*199;xx=x+rr*cos(theta);yy=y+rr*sin(theta);r=rnd.uniform(3,13);o+=P.e(xx,yy,r*1.2,r,None,b if k%3 else a,1)+P.p(f'M{xx-r*.8} {yy+1}q{r*.35} {r*.76} {r*1.56} {r*.41}',None,b,.7)
        if j==7:
            for k in range(54):o+=P.p(f'M{-60+k*17} 0Q{W*.42+k*4} {455-k*3} {W+36} {94+k*6}',None,a if k%6==0 else b,.55+(k%3)*.22)
            o+=P.p(f'M0 565L{W*.22} 437L{W*.39} 518L{W*.53} 455L{W*.72} 534L{W} 429V600H0Z',b,'none')
        if j==8:
            for k in range(4100):
                xx=rnd.uniform(0,W);mid=295+75*sin(xx/251);yy=mid+rnd.gauss(0,47+22*cos(xx/290));dust=abs(yy-(mid+17*sin(xx/74)))<11 and rnd.random()<.82
                if not dust:o+=circle(xx,yy,rnd.uniform(.35,1.9),[a,b,c,i][k%4])
    elif z=='dunhuang':
        if j==0:o+=''.join(P.p(f'M0 {280+k*23}Q{W*.18} {204+k*26} {W*.39} {278+k*23}T{W*.77} {277+k*21}T{W} {249+k*24}',None,b,1.8)for k in range(9))+lotus(P,W*.35,254,2.2)+lotus(P,W*.72,359,1.15)
        if j==1:o+=''.join(arch(P,45+k*255,84,217,342,c)+arch(P,60+k*255,106,187,320,a)+arch(P,78+k*255,130,151,294,bg)+lotus(P,153+k*255,332,.93)for k in range(4))
        if j==2:
            for k in range(9):o+=place(P.p('M0 220Q-48 161 3 125Q-8 159 14 155Q51 111 30 64Q104 121 63 160Q93 152 91 114Q129 178 72 220Z',a,i,1.2)+P.p('M23 216Q17 183 51 150Q42 188 64 194L52 216Z',c,'none'),18+k*118,93+26*sin(k),.94)
            o+=P.bars(0,352,3,9,W,b,0,1.3)
        if j==3:o+=apsara(P,217,217,.97)+P.p('M41 369C113 293 241 351 209 417S38 445 75 505S255 520 296 415',None,b,8)+P.p('M36 380C115 305 231 358 200 416S33 463 70 511',None,c,2)+cloud(P,110,121,.71)
        if j==4:o+=pavilion(P,x,170,1.34)+P.p('M73 453Q161 407 260 453L233 494H100Z',b)+P.r(114,499,111,14,c)+P.l(x,433,x,286,b,4)+lotus(P,x,268,1.27)+leaf(x,368,.96,-54,b,i)+leaf(x,389,1.05,64,b,i)
        if j==5:o+=P.r(29,29,542,542,c,a,3)+P.r(53,53,494,494,bg,b,3)+radial(x,y,12,lambda k:P.p('M0 -70Q-54 -134 -1 -221Q57 -151 0 -70Z',a if k%2 else b,i,1.7))+lotus(P,x,y,2.41)
        if j==6:
            for r,co in [(276,a),(249,b),(216,c),(186,bg),(153,b),(126,c)]:o+=poly([(x,y-r),(x+r,y),(x,y+r),(x-r,y)],co,i,1.7)
            o+=radial(x,y,8,lambda k:P.e(0,-66,20,48,a,i,1.3))+lotus(P,x,y,1.08)+''.join(lotus(P,X,Y,.46)for X,Y in [(64,64),(536,64),(64,536),(536,536)])
        if j==7:o+=''.join(pavilion(P,123+k*253,345,1.16 if k%3 else 1.43)for k in range(8))+P.bars(0,376,2,18,W,a,0,3)+P.cols(19,361,67,32,64,b,0,4)+''.join(cloud(P,72+k*262,108+(k%3)*22,.97)for k in range(8))
        if j==8:o+=rope(P,[(k*W/180,301+64*sin(k/180*14*pi))for k in range(181)],b,5)+''.join(lotus(P,68+k*185,300+48*sin(k*1.3),.78)+leaf(110+k*185,327,.92,67,b,i)for k in range(12))+''.join(P.o(13+k*34,165,6,c,i,.9)+P.o(13+k*34,445,6,c,i,.9)for k in range(63))
    elif z in ['cartography','natural-history']:
        cart=z=='cartography'
        if j==0:
            if cart:
                pts=[(rnd.uniform(50,W-50),rnd.uniform(63,530))for k in range(23)]
                for k,v in enumerate(pts):
                    nb=sorted((p for p in pts if p!=v),key=lambda p:math.dist(v,p))[:3];o+=''.join(P.l(*v,*p,b,1)for p in nb)+P.o(*v,3.3,a)
                o+=gradgrid(13,7)
            else:o+=''.join(place(motif(P.S,0),-22+k*174,82+(k%3)*53,1.02+k%2*.36,(-1)**k*12)for k in range(6))+P.p(f'M0 474Q{x*.5} 401 {x} 469T{W} 430',None,a,2)
        if j==1:
            if cart:o+=gradgrid(12,7)+''.join(ref(1,124+k*178,206+sin(k*1.7)*111,145+k%3*57)for k in range(6))+ref(0,W*.81,436,135)
            else:
                for k in range(9):o+=P.p(f'M0 {100+48*k}Q{W*.20} {42+51*k} {W*.45} {117+44*k}T{W*.79} {97+46*k}T{W} {68+46*k}V600H0Z',[c,b,bg,a][k%4],i,1.0)
                o+=ob(0,W*.38,330,129)+ob(1,W*.81,416,108)
        if j==2:
            if cart:o+=mountain(P,285,291,1.66)+mountain(P,706,304,1.94)+P.p('M29 431L129 408L225 362L340 402L409 369L524 411L648 365L724 337L843 387L1027 345',None,a,2.3)+P.cols(30,440,39,26,14,b,0,1)
            else:o+=P.p(f'M0 240Q{x*.55} 165 {x} 245T{W} 212V600H0Z',c,'none')+''.join(P.p(f'M{30+k*75} 521q-30 -75 0 -123t-4 -90M{33+k*75} 475q29 -33 33 -64',None,b,2.5)for k in range(14))+fish(P,421,320,1.32)+fish(P,738,366,.81,True)
        if j==3:
            if cart:o+=P.p('M195 -10Q85 124 164 187T129 352T190 609',None,b,15)+P.p('M19 55Q95 91 132 160M317 128Q210 169 183 227M11 285Q71 288 136 343M317 451Q197 478 155 522',None,b,6)+ref(0,71,481,100)
            else:o+=P.p('M101 571Q159 368 154 266T215 35',None,i,4)+''.join(leaf(134+k*6,461-k*47,1.18-k*.065,70 if k%2 else -48,a if k%3 else b,i)for k in range(9))+P.cols(282,62,2,7,459,b,0,.8)
        if j==4:
            if cart:o+=mountain(P,161,223,1.17)+mountain(P,174,334,.92)+ref(0,176,443,145)+P.p('M29 362Q61 290 124 274T210 194T308 116',None,a,1.7)
            else:o+=''.join(P.r(74+k*48,70,37,432,None,i)+''.join(P.r(77+k*48,76+l*61,31,56,[a,b,c,bg][(k+l*l)%4],i,.7)for l in range(7))for k in range(4))+P.bars(266,76,27,15,16,b,0,.8)
        if j==5:
            if cart:o+=P.grid(30,31,539,535,11,10,b)+P.p('M-10 450Q154 224 249 345T431 308T615 187',None,b,34)+''.join(P.r(37+k*49,52+l*56,29+(l%2)*5,25,c,i,.8)for l in range(8)for k in range(11)if (k+l)%4!=1 and (l<4 or k>5))
            else:
                for k in range(9):
                    xx=119+k%3*181; yy=116+k//3*178;rr=34+(k%3)*5;o+=P.o(xx,yy,rr,None,i,2)+radial(xx,yy,12+k,lambda n:P.l(0,-rr+4,0,-rr-8,a,1.5))+''.join(P.o(xx+cos(t*2.4)*math.sqrt(t)*4,yy+sin(t*2.4)*math.sqrt(t)*4,2.7,b)for t in range(24))
        if j==6:
            if cart:o+=ref(0,222,261,333)+''.join(P.p(f'M{252+k*3} 567Q{185+k*8} 426 {358+k*5} 365T{558+k} 97',None,b,.9)for k in range(20))
            else:o+=''.join(P.p(f'M302 489Q{59+k*7} {424-k*3} {58+k*8} {190+k*3}Q{117+k*6} {90+k*6} 302 {74+k*8}Q{504-k*6} {102+k*6} {546-k*7} {208+k*2}Q{530-k*6} {424-k*2} 302 489Z',None,[i,a,b][k%3],1.2)for k in range(23))
        if j==7:
            if cart:o+=''.join(mountain(P,141+k*286,291+sin(k)*34,1.22+(k%4)*.19)for k in range(8))+''.join(rope(P,[(W*t/110,372+k*13+29*sin(t*.15+k*.08)+19*cos(t*.33))for t in range(111)],b,.9)for k in range(10))
            else:o+=P.l(24,350,W-24,350,i,1.3)+''.join(place(motif(P.S,0),83+k*306,172,.37+k*.095)+P.l(136+k*306,358,136+k*306,384,b,2)for k in range(7))
        if j==8:
            if cart:o+=gradgrid(30,6)+''.join(ref(1,144+k*309,254+(k%3)*57,170+(k%2)*75)for k in range(7))+rope(P,[(23+k*W/47,291+102*sin(k*.43))for k in range(47)],a,2)
            else:
                for k in range(7):o+=P.p(f'M0 {157+k*51}Q{W*.19} {107+k*42} {W*.42} {177+k*43}T{W*.75} {149+k*46}T{W} {120+k*44}V600H0Z',[b,bg,c,a][k%4],i,.9)
                o+=''.join(ref(2,128+k*287,300+(k%3)*48,102+(k%2)*44)for k in range(7))
    else:return tech(P,j,W,H,o,rnd)
    return o
