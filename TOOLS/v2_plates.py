"""原创主题图版的绘图工具；细部母题与场景采用不同的画面语法。所有画面不含嵌入位图。"""
from artwork import *
from v2_registry import *
from v2_borders import cell
def place(s,x,y,k=1,ang=0):return g(s,f'translate({n(x)} {n(y)}) rotate({n(ang)}) scale({n(k)})')
class Pen:
    def __init__(self,S):self.S=S;self.bg,self.i,self.a,self.b,self.c=S['palette']
    def p(self,d,fill=None,st=None,w=1.8):return path(d,fill or 'none',self.i if st is None else st,w,'stroke-linecap="round" stroke-linejoin="round"')
    def r(self,x,y,w,h,f=None,st=None,lw=1.6,rad=0):return rect(x,y,w,h,f or 'none',self.i if st is None else st,lw,rad)
    def l(self,x,y,X,Y,col=None,w=1.4):return line(x,y,X,Y,col or self.i,w)
    def e(self,x,y,rx,ry,f=None,st=None,lw=1.5):return ell(x,y,rx,ry,f or 'none',self.i if st is None else st,lw)
    def o(self,x,y,r,f=None,st=None,lw=1.5):return circle(x,y,r,f or 'none',self.i if st is None else st,lw)
    def t(self,x,y,s,sz=12,col=None,font='Georgia'):return txt(x,y,s,sz,col or self.i,font)
    def cols(self,x,y,num,space,h,col=None,tilt=0,w=1):return ''.join(self.l(x+j*space,y,x+j*space+tilt,y+h,col,w) for j in range(num))
    def bars(self,x,y,num,space,w,col=None,slant=0,lw=1):return ''.join(self.l(x,y+j*space,x+w,y+j*space+slant,col,lw)for j in range(num))
    def grid(self,x,y,w,h,nx,ny,col=None):return self.cols(x,y,nx+1,w/nx,h,col or self.b,0,.65)+self.bars(x,y,ny+1,h/ny,w,col or self.b,0,.65)
    def paper(self):return rect(0,0,640,400,self.bg)
def pane(P,x,y,w,h,nx=4,ny=3):
    return P.r(x,y,w,h,P.b,P.i,2)+P.grid(x+3,y+3,w-6,h-6,nx,ny,P.bg)
def hatch(P,x,y,w,h,step=8):return ''.join(P.l(x+i,y+h,x+min(w,i+h),y+h-min(h,w-i),P.i,.85)for i in range(0,int(w),step))
def arch(P,x,y,w,h,fill='none'):
    return P.p(f'M{x} {y+h}V{y+w/2}a{w/2} {w/2} 0 0 1 {w} 0V{y+h}Z',fill)
def lamp(P,x,y,k=1):
    s=P.e(0,0,22,5,P.b)+P.l(0,-3,0,-61,P.i,5)+P.p('M-32 -62Q-23 -91 1 -91Q23 -89 33 -62Z',P.a)+P.l(18,-61,18,-39,P.c)
    return place(s,x,y,k)
def book(P,x,y,w,h,col=None):
    return P.p(f'M{x} {y}q{w*.21} {-h*.13} {w*.5} 3q{w*.22} {-h*.18} {w*.5} -2v{h}q{-w*.25} {-h*.13} {-w*.5} 4q{-w*.25} {-h*.15} {-w*.5} -3Z',col or P.bg)+P.l(x+w/2,y+3,x+w/2,y+h+4)+''.join(P.p(f'M{x+8} {y+10+j*h*.15}q{w*.16} {-h*.08} {w*.32} 0M{x+w*.6} {y+10+j*h*.15}q{w*.15} {-h*.08} {w*.31} -1',None,P.b,.8)for j in range(4))
def crag(P,x,y,k=1):
    return place(P.p('M-45 0Q-39 -21 -25 -30Q-9 -48 9 -35Q28 -41 39 -19L50 -3Q12 10 -45 0Z',P.b)+P.p('M-34 -6Q-21 -20 -5 -27M-15 -3Q7 -23 20 -23M12 -3L30 -14',None,P.i,1),x,y,k)
def bird(P,x,y,k=1):
    s=P.p('M-52 -2L-25 3Q-12 -31 13 -29Q21 -42 34 -33Q43 -28 39 -18L51 -15L38 -12Q24 16 0 18Q-12 19 -25 10L-50 13Z',P.b)+P.p('M-22 6Q-8 -17 14 -14Q1 3 -22 6Z',P.a)+P.o(32,-26,2.3,P.i)+P.p('M0 18L-4 28M13 15L14 26M-10 29H2M9 27H22',None,P.i,1.2)
    return place(s,x,y,k)
def fish(P,x,y,k=1,rev=False):
    s=P.p('M-47 0Q-18 -27 15 -18Q30 -14 43 -1Q26 19 -1 17Q-29 16 -47 0ZM-45 0L-65 -17L-61 16Z',P.b)+P.p('M3 -18L-10 -34L20 -20M-5 15L-14 27L12 17',P.a)+P.p('M22 -13Q15 -1 24 11',None,P.i,1.2)+P.o(32,-4,2.2,P.i)+''.join(P.p(f'M{u} -5q5 5 0 9',None,P.bg,1)for u in [-22,-13,-4,5])
    return g(s,f'translate({x} {y}) scale({-k if rev else k} {k})')
def staircity(P,x,y,w,h,rnd,kind='deco'):
    o='';N=13
    for j in range(N):
        xx=x+j*w/N;ww=w/N*.94;H=h*rnd.uniform(.25,.88)
        if kind=='deco':
            o+=P.p(f'M{xx} {y}v{-H*.68}h{ww*.15}v{-H*.18}h{ww*.14}v{-H*.14}h{ww*.42}v{H*.14}h{ww*.14}v{H*.18}h{ww*.15}V{y}Z',P.b if j%3 else P.bg)
            o+=P.cols(xx+ww*.25,y-H*.61,3,ww*.23,H*.56,P.a,0,1.4)
        else:
            o+=P.r(xx,y-H,ww,H,P.bg,P.b,1)+P.l(xx+ww*.27,y-H-15,xx+ww*.27,y-H,P.a,1)
            for v in range(int(H/16)):
                for u in range(3):
                    if rnd.random()>.43:o+=rect(xx+5+u*ww*.24,y-H+7+v*16,ww*.14,2.2,P.a if (u+v)%4 else P.c)
    return o
def bamboo(P,x,y,k=1):
    o=P.p('M0 16Q-2 -65 24 -171',None,P.i,3)
    for j in range(6):
        xx=2+j*3.6;yy=-10-j*25;o+=P.l(xx-3,yy,xx+4,yy-1,P.b,3)
        if j%2:o+=P.p(f'M{xx} {yy}q22 -13 44 -7',None,P.i,1.5)+leaf(xx+20,yy-9,.55,76,P.b,P.i)+leaf(xx+30,yy-8,.54,120,P.b,P.i)
        else:o+=P.p(f'M{xx} {yy}q-12 -16 -29 -20',None,P.i,1.5)+leaf(xx-13,yy-12,.56,-58,P.b,P.i)
    return place(o,x,y,k)
def person(P,x,y,k=1,pose=0):
    s=P.o(0,-67,9,P.c)+P.p('M-6 -57L-17 -30L7 -23L12 -49Z',P.a)+P.p('M-8 -29L-19 -5L-29 0M5 -24L18 -6L23 -5',None,P.i,5)+P.p('M8 -46L23 -38L35 -52M-9 -47L-21 -35L-37 -36',None,P.b,4)
    return g(s,f'translate({x} {y}) scale({-k if pose else k} {k})')
def engine(P,x,y,k=1):
    o=P.e(0,0,44,44,P.bg,P.i,2)+P.e(0,0,33,33,'none',P.b)+P.e(0,0,12,12,'none',P.a,2)
    for u in range(8):
        X,Y=polar(0,0,38,u*pi/4);o+=P.o(X,Y,2.3,P.bg,P.i,1)
    return place(o,x,y,k)
def struts(P,x,y,w,h,count=6):
    return P.r(x,y,w,h)+curve([(x+j*w/count,y if j%2 else y+h)for j in range(count+1)],P.i,2)
def pine(P,x,y,k=1):
    return place(P.p('M0 0Q8 -38 -4 -69Q-18 -91 -9 -129M3 -39Q-24 -61 -50 -53M-3 -72Q11 -91 45 -84',None,P.i,4)+''.join(P.p(f'M{a} {b}q-17 -22 -39 -6q-14 11 -32 7q23 -22 41 -22q21 -9 30 21Z',P.b,P.i,.9)for a,b in [(-24,-52),(65,-82),(18,-123)]),x,y,k)
def lotus(P,x,y,k=1):
    s=''
    for j in range(10):s+=g(P.p('M0 5C-17 -6 -20 -22 0 -42C18 -24 18 -6 0 5Z',P.b if j%2 else P.c,P.i,1.1)+P.p('M0 -2Q-5 -18 0 -31',None,P.a,.9),f'rotate({j*36})')
    return place(s+P.o(0,0,11,P.a)+P.o(0,0,5,P.c),x,y,k)
def pavilion(P,x,y,k=1):
    o=P.r(-65,-47,130,48,P.bg)+P.cols(-56,-47,5,28,47,P.a,5)+P.p('M-94 -48Q-64 -50 -51 -65Q-26 -67 -1 -90Q32 -65 55 -65Q63 -51 93 -48Q48 -38 0 -43Q-45 -37 -94 -48Z',P.b)+P.p('M-89 -48Q0 -53 87 -48M-55 -61Q-12 -66 0 -85Q17 -67 53 -61',None,P.c,2)+P.r(-77,-3,154,7,P.c)+P.r(-84,4,168,6,P.a)
    return place(o,x,y,k)
def apsara(P,x,y,k=1,flip=False):
    # 抬手、屈膝、向后飘带；为现代线描，非洞窟复制品。
    o=P.p('M-52 -6C-107 -47 -163 -27 -143 9S-67 32 -67 57C-87 40 -157 49 -170 10C-187 -44 -105 -68 -47 -21C-7 15 19 -4 7 -18',None,P.b,5)+P.p('M-59 4C-97 26 -147 12 -148 -3C-154 -18 -128 -21 -115 -9',None,P.c,2)
    o+=P.p('M-16 -8Q-35 -6 -52 2Q-71 5 -92 -12L-124 -11Q-100 13 -75 23Q-56 36 -26 24L-8 13Z',P.b)+P.p('M-17 4Q-44 22 -73 18M-39 4Q-71 15 -93 2M-64 27Q-82 46 -111 45L-135 35Q-117 54 -103 58Q-56 62 -36 27',P.a)
    o+=P.p('M-9 -30Q9 -30 17 -12L7 10Q-6 23 -29 20L-24 4Z',P.c)+P.p('M8 -22Q30 -20 43 -42L52 -55M-12 -23Q-29 -42 -46 -34L-64 -21',None,P.a,5)
    o+=P.e(6,-42,12,15,P.c)+P.p('M-7 -46Q-9 -64 9 -61Q24 -56 20 -42Q14 -52 2 -52Z',P.i)+P.o(0,-61,6,P.i)+P.p('M13 -43L18 -40L14 -39M9 -35Q12 -33 14 -35',None,P.i,.9)+P.o(12,-30,2.8,P.a)
    return g(o,f'translate({x} {y}) scale({-k if flip else k} {k})')
