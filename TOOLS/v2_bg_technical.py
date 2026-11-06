from v2_scenes import *
def tech(P,j,W,H,o,rnd):
    x=W/2;y=H/2;z=P.S['id'];i,a,b,c,bg=P.i,P.a,P.b,P.c,P.bg
    def grid(nx,ny):return '<g opacity=".30">'+P.grid(15,15,W-30,H-30,nx,ny,b)+'</g>'
    if z=='retrofuturism':
        if j==0:o+=P.o(W*.75,135,67,a)+horizon(P,0,385,W)+''.join(P.e(179+k*305,251,66,19,c,i,2)+P.p(f'M{123+k*305} 231q61 124 105 18M{174+k*305} 282l-36 95h85Z',None,i,3)+P.l(174+k*305,263,196+k*305,195,b,3)for k in range(3))
        if j==1:o+=horizon(P,0,335,W)+P.p(f'M{x-28} 303H{x+30}L{W*.87} 600H{W*.15}Z',i,c,1.4)+''.join(P.r(x-2,324+k*k*4,4,3+k*1.7,c,'none')for k in range(8))+P.o(W*.21,123,56,a)+P.e(W*.21,123,92,15,None,b,3)
        if j==2:o+=P.r(65,115,W-130,305,bg,b,4,37)+P.r(93,142,W-186,171,bg,c,1.5,20)+''.join(P.l(114+k*10,266,114+k*10,239-k%6*6,b,1)for k in range(84))+P.l(W*.61,153,W*.61,305,a,4)+P.o(188,363,25,b)+P.o(W-187,363,25,b)+P.bars(323,346,4,9,W*.35,c)
        if j==3:o+=P.p('M112 414Q95 209 172 64Q246 235 222 414L173 457Z',c)+P.p('M114 319L66 413V465L119 409M225 319L274 410V462L221 410',a)+P.o(170,237,25,b,i,2)+P.r(31,98,35,409,None,b,2)+P.cols(47,105,1,1,390,a)+P.bars(32,133,12,29,34,b)
        if j==4:o+=''.join(P.e(x,141+k*73,71-k*3,15,None,c,2.5)+P.r(x-36,146+k*73,72,27,b,i,1.5,12)for k in range(5))+P.p('M97 445V152Q95 72 167 65Q240 68 239 153V445ZM82 464H256V490H82Z',None,a,3)
        if j==5:o+=P.o(x,y,243,b,i,3)+P.o(x,y,208,bg,c,3)+P.o(361,248,66,a,'none')+P.e(363,251,88,17,None,c,3)+P.p('M113 384Q184 304 257 357T391 355Q434 350 471 401Q311 557 147 416Z',b)+''.join(P.o(*polar(x,y,222,k*pi/6),4,c)for k in range(12))
        if j==6:o+=grid(8,8)+''.join(g(P.e(x,y,218,64,None,co,3),f'rotate({deg} {x} {y})')for deg,co in [(0,a),(60,b),(120,c)])+P.o(x,y,38,a)+''.join(P.o(*polar(x,y,173,k*pi*.67),15,c)for k in range(3))
        if j==7:o+=horizon(P,0,369,W)+P.p(f'M0 448Q{x*.8} 287 {W} 219',None,i,14)+P.p(f'M0 438Q{x*.8} 279 {W} 211',None,c,2)+''.join(P.l(100+k*264,419-k*23,110+k*264,566,b,8)for k in range(8))+place(obj(P,2),W*.65,113,1.01)
        if j==8:o+=P.l(24,297,W-24,297,b,1)+''.join(P.o(144+k*288,297,24+(k%4)*14,[a,b,c][k%3])+P.e(144+k*288,297,68+(k%4)*9,14,None,c,1.6)+P.cols(134+k*288,380,3,8,18,a)for k in range(7))
    elif z=='cyberpunk':
        def trace(xx,yy,length,k):
            return P.p(f'M{xx} {yy}h{length*.29}l{24+k*2} {-24-k*2}h{length*.44}l25 25h{length*.18}',None,[a,b,c][k%3],1.7)+P.o(xx,yy,4,None,a,1.6)
        if j==0:o+=''.join(trace(24+(k%5)*15,99+k*14,W*.67,k)for k in range(30))+P.r(W*.74,106,W*.18,323,bg,b,2)+P.cols(W*.77,146,7,20,183,c,0,2)
        if j==1:o+=skyline(P,9,414,W-18,379,rnd)+P.r(0,271,W,34,bg,a,2)+struts(P,17,276,W-35,22,24)+P.p(f'M0 435Q{x} 380 {W} 419',None,b,3)
        if j==2:
            for l in range(10):
                for k in range(18):
                    if rnd.random()>.27:o+=P.r(44+k*55,87+l*42,rnd.randrange(12,44),rnd.randrange(4,18),[a,b,c][(k+l)%3],'none')
            o+=P.p(f'M30 62H192L214 42H{W-34}M29 526H{W*.59}l20 19H{W-24}',None,b,2)
        if j==3:o+=P.r(52,40,W-104,505,bg,b,2)+''.join(P.p(f'M72 {90+k*43}l144 -22l33 11l-147 23Z',b,a,.7)for k in range(10))+P.bars(54,493,3,8,W-108,c)
        if j==4:o+=P.p('M68 511V82L101 48H242V487L209 521H68Z',None,a,4)+P.p('M92 441V127L141 84V372L187 333V117H218V424L178 469V411L126 452Z',None,b,7)+P.bars(91,482,2,6,108,c)
        if j==5:
            for k in range(5):o+=P.o(x,y,88+k*36,None,[a,b,c,bg,a][k],1.9)
            o+=ringticks(x,y,250,156,b)+P.p('M78 304H215L237 278H279L308 315H369L388 293H525',None,c,3)+P.cols(197,390,12,17,18,a)
        if j==6:o+=grid(12,12)+P.r(205,204,190,186,bg,a,3)+''.join(trace(20,110+k*20,164,k)for k in range(15))+''.join(P.p(f'M{404+k%2*7} {211+k*11}h39l27 27h87',None,b if k%2 else c,1.6)for k in range(13))+P.grid(229,229,141,134,5,5,b)
        if j==7:o+=''.join(P.p(f'M0 {133+k*12}H{W*.27+k*5}l113 106H{W*.69}l136 -140H{W}',None,[a,b,c][k%3],1.1+k%3*.4)for k in range(24))
        if j==8:
            o+=skyline(P,0,410,W,388,rnd)+P.bars(0,433,3,12,W,b)
            for k in range(280):
                X=rnd.uniform(0,W);Y=rnd.uniform(0,H);o+=P.l(X,Y,X-4,Y+15,b,.6)
            o+=''.join(P.r(69+k*250,199+k%3*22,111,27,bg,a,2)+P.l(82+k*250,213+k%3*22,145+k*250,213+k%3*22,c,2)for k in range(8))
    elif z=='blueprint':
        o+=grid(22 if W>650 else 10,12)
        if j==0:o+=struts(P,50,177,W-100,81,12)+P.cols(83,262,6,(W-165)/5,177,i,0,3)+P.p(f'M38 465H{W-39}M38 453v25M{W-39} 453v25',None,c,1.6)
        if j==1:o+=P.p(f'M54 421H238V259H{W*.7}V116H{W-61}M{x} 259V415H{W*.69}',None,i,22)+P.p(f'M54 421H238V259H{W*.7}V116H{W-61}M{x} 259V415H{W*.69}',None,bg,15)+''.join(P.p(f'M{xx-16} {yy-12}l32 24v-24l-32 24Z',bg,c,2)for xx,yy in [(158,421),(377,259),(865,116),(643,415)])
        if j==2:o+=P.r(87,142,W-174,289,None,i,2)+P.grid(107,160,W-214,251,12,4,b)+''.join(engine(P,187+k*207,269,.89+(k%2)*.24)for k in range(4))+P.p('M88 116H982M88 103V130M982 103V131',None,c,1.4)
        if j==3:o+=P.r(91,42,116,500,None,i,2)+P.cols(112,54,3,32,477,b)+''.join(P.l(94,65+k*16,145 if k%5 else 189,65+k*16,c,1.5)for k in range(29))+P.p('M222 302L263 285V319Z',a)
        if j==4:o+=P.r(133,59,71,463,None,i,2)+P.p('M82 277L168 328L249 277V360L169 311L82 360ZM168 279V195M114 192H220M138 177H198',None,a,3)+P.bars(104,77,3,8,130,i)+P.bars(104,493,3,8,130,i)
        if j==5:o+=engine(P,x,y,4.25)+ringticks(x,y,236,96,b)+P.p('M38 300H559M300 36V563',None,c,.85)+''.join(P.o(*polar(x,y,222,k*pi/4),7,bg,i,1.4)for k in range(8))
        if j==6:o+=''.join(struts(P,42,71+k*88,516,67,8)for k in range(5))+P.cols(43,62,5,129,450,i,0,2.5)+P.l(41,543,558,543,c)
        if j==7:o+=struts(P,10,271,W-20,118,32)+''.join(P.p(f'M{37+k*308} 389L{65+k*308} 532H{103+k*308}L{122+k*308} 389',None,i,2.5)for k in range(7))+P.p(f'M20 241Q{x} -57 {W-20} 241',None,a,2.5)
        if j==8:o+=P.l(14,310,W-14,310,c,.9)+''.join(engine(P,98+k*271,312,1.2+(k%3)*.36)+P.r(165+k*271,292,117,39,None,i,1.6)for k in range(8))
    elif z=='generative-art':
        if j==0:
            for k in range(3000):
                X=rnd.uniform(0,W);Y=rnd.uniform(0,H);val=sin(X*.021+Y*.03)+cos(math.hypot(X-W*.62,Y-310)*.055)
                if val>-.44:o+=P.o(X,Y,.75+max(0,val)*2.4,[a,b,i][k%3],'none')
        if j==1:o+=place(voronoi(P,W-76,H-76,817,82),38,38)
        if j==2:o+=lsystem(P,W*.22,522,8.1,616)+lsystem(P,W*.59,523,12.2,811)+lsystem(P,W*.87,521,6.2,102)+P.l(37,526,W-37,526,b,.9)
        if j==3:
            row=[0]*61;row[30]=1;d=4.92
            for yy in range(102):
                for xx,v in enumerate(row):
                    if v:o+=rect(17+xx*d,40+yy*d,d+.02,d+.02,[a,i,b][yy//34%3])
                row=[(30>>((row[(k-1)%61]<<2)+(row[k]<<1)+row[(k+1)%61]))&1 for k in range(61)]
        if j==4:o+=lsystem(P,W*.44,544,11.5,457)+lsystem(P,W*.7,543,6.8,195)
        if j==5:o+=rec_tri(P,34,515,532,5)+P.l(35,539,566,539,b,1.3)
        if j==6:
            for k in range(980):
                d=8.4*math.sqrt(k);t=k*pi*(3-math.sqrt(5));o+=g(P.e(x+d*cos(t),y+d*sin(t),4.8,1.8,[a,i,b][k%3],'none'),f'rotate(0 {x} {y})')
        if j==7:
            for k in range(123):
                X=rnd.uniform(-50,37);Y=rnd.uniform(42,549);ps=[]
                for n_ in range(270):ps.append((X,Y));X+=8.4;Y+=2*sin(Y*.016+X*.01)+1.6*cos(.014*X-.01*Y)
                o+=curve(ps,[a,b,i][k%3],1.1)
        if j==8:
            o+='<style>@keyframes pulse{0%,100%{opacity:.34}50%{opacity:1}}.pulse{animation:pulse 9s ease-in-out infinite}@media(prefers-reduced-motion:reduce){.pulse{animation:none}}</style>'
            for k in range(108):
                X=31+k*(W-62)/107;h=34+106*(1+sin(k*.16)*cos(k*.059));o+=P.l(X,y-h,X,y+h,[a,b,i][k%3],1.2)+f'<g class="pulse" style="animation-delay:-{k%9}s">'+P.o(X,y-h,3.2,c,'none')+'</g>'
    else:raise ValueError(z)
    return o
