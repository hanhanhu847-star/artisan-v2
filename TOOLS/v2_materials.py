"""原生 2048×2048 的周期多尺度材料。直接采样解析场，不读取小图做放大。
10 个 V1 材质家族升级，不重复计数；每套另有两种加工表面与四张透明工艺叠层。
"""
import numpy as np, math, zlib, argparse, concurrent.futures as cf
from PIL import Image
from v2_registry import *
TEX='paper metal stone textile wood plaster halftone film engraving stipple'.split()
NAMES='纸浆纤维 拉丝金属 矿脉石面 交错经纬 弦切木纹 风化灰墙 椭圆印刷网点 胶片乳剂 雕版排线 石印点刻'.split()
# 每种附加工艺对应一种形貌机理，参数为截面、沉积方向或加工密度。
FIN={
'bauhaus':('胶合板斜接面','粉末搪瓷','ply','enamel'),'art-deco':('扇区拉丝黄铜','龟裂漆器','engine','craze'),
'swiss':('胶印色带','压字凹痕','offset','blind'),'neo-brutalism':('胶带布基','刮裂丝印','tape','scrape'),
'memphis':('彩屑水磨石','粒面层压板','terrazzo','pebble'),'editorial':('书脊装订布','干式压印','tape','blind'),
'wabi-sabi':('陶釉开片','沉积砂釉','craze','ash'),'dark-academia':('压花皮革','书口云纹','pebble','marble'),
'celestial-atlas':('仪器车花盘','蚀刻铜版','engine','etch'),'dunhuang':('矿物色沉积','剥落地仗','ash','flake'),
'cartography':('旧纸折痕','铜版蚀刻纸','fold','etch'),'natural-history':('矿物晶屑','标本纸吸墨','terrazzo','wick'),
'retrofuturism':('阳极机加工铝','双色套印','engine','offset'),'cyberpunk':('微棱镜反光膜','剥漆面板','prism','flake'),
'blueprint':('蓝晒感光纸','交叠夹板断面','wick','ply'),'generative-art':('干涉压纹','胞壁结晶','moire','cell')}
def rgb(h):return np.array([int(h[i:i+2],16)for i in (1,3,5)],np.float32)
def herm(v):return v*v*(3-2*v)
def fold(x):return np.abs((x+.5)%1-.5)
def screen(x):return np.clip(x,0,1)
class Sampler:
    def __init__(self,seed):self.seed=seed;self.grids={}
    def grid(self,k,l,n):
        key=(k,l,n)
        if key not in self.grids:self.grids[key]=np.random.default_rng(self.seed+n*97+k*7+l*11).uniform(-1,1,(l,k)).astype('f')
        return self.grids[key]
    def noise(self,x,y,k,l,n):
        arr=self.grid(k,l,n);X=x*k;Y=y*l;ix=np.floor(X).astype('i');iy=np.floor(Y).astype('i');fx=herm(X-ix);fy=herm(Y-iy);ix%=k;iy%=l
        return (arr[iy,ix]*(1-fx)+arr[iy,(ix+1)%k]*fx)*(1-fy)+(arr[(iy+1)%l,ix]*(1-fx)+arr[(iy+1)%l,(ix+1)%k]*fx)*fy
    def vor(self,x,y,k,l):
        X=x*k;Y=y*l;ix=np.floor(X).astype('i');iy=np.floor(Y).astype('i');best=np.full(np.broadcast_shapes(x.shape,y.shape),9.,dtype='f');second=best.copy();chip=best.copy();jx=self.grid(k,l,201);jy=self.grid(k,l,202);col=self.grid(k,l,203)
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                gx=(ix+dx)%k;gy=(iy+dy)%l;rx=(ix+dx+.5+jx[gy,gx]*.39-X);ry=(iy+dy+.5+jy[gy,gx]*.39-Y);ds=rx*rx+ry*ry
                chip=np.where(ds<best,col[gy,gx],chip);second=np.minimum(second,np.maximum(ds,best));best=np.minimum(best,ds)
        return np.sqrt(second)-np.sqrt(best),chip
def generate(S,kind,seed,p,N=2048):
    R=Sampler(seed);out=np.empty((N,N,4 if kind.startswith('overlay')else 3),dtype='uint8');bg,ink,a,b,c=[rgb(q) for q in S['palette']]
    q=S['no'];v=2*math.pi;rr=np.random.default_rng(seed);phase=rr.uniform(0,6.28,8);x=np.arange(N,dtype='f')[None,:]/N
    tone=bg*.70+b*.23+a*.07
    if kind in ['metal','engine','prism']:tone=tone*.62+np.array([125,132,130])*.38
    for top in range(0,N,96):
        y=np.arange(top,min(N,top+96),dtype='f')[:,None]/N
        def ns(k,l=None,i=0):return R.noise(x,y,k,l or k,i)
        lo=ns(5,i=1);mid=ns(35,i=2);mic=ns(401,i=3);gr=rr.normal(0,1,(len(y),N)).astype('f');extra=None
        if kind=='paper':f=12*ns(180,12,5)+9*ns(19,237,6)+6*lo+2.8*mic+1.7*gr;f+=6*screen((ns(64,5,9)-.49)*5)
        elif kind=='metal':f=8*ns(4,260,6)+11*np.sin(v*(y*(3+q%3)+.13*lo)+phase[0])+3*ns(18,704,7)+1.5*gr-12*screen((ns(7,340,11)-.71)*8)
        elif kind=='stone':wall,ch=R.vor(x+.019*lo,y+.017*mid,9+q%4,11);f=21*np.exp(-wall*21)-9*np.exp(-wall*6)+10*ch+5*mid+2*gr+3*mic
        elif kind=='textile':
            X=x*(64+q)+.09*ns(12,17,7);Y=y*(60+q)+.07*ns(17,10,8);warp=np.cos(v*X);weft=np.cos(v*Y);which=(np.floor(X).astype('i')+np.floor(Y).astype('i'))%2
            f=11*(warp+weft)+6*np.where(which,warp,weft)+4*np.sin(3*v*(X+Y))+4*lo+2*gr
        elif kind=='wood':
            dist=(fold(x-.31)/.16)**2+(fold(y-.55)/.075)**2;X=x*(15+q%5)+.45*np.sin(v*y)+1.8*np.exp(-dist*1.4)+.22*lo
            f=14*np.sin(v*X)+5*np.sin(v*3*X)+9*ns(193,8,6)+1.8*gr-14*np.exp(-dist*11)
        elif kind=='plaster':f=18*lo+8*mid+11*screen((ns(18,i=6)+.4*mic-.18)*3)-9*screen((ns(88,i=8)-.55)*4)+2.5*gr
        elif kind=='halftone':
            X=(x+y)*(32+q%5);Y=(x-y)*(32+q%5);d=(fold(X)/(.26+.05*lo))**2+(fold(Y)/(.34+.03*mid))**2;f=12-29*screen((1-d)*8)+2.2*mic+1.4*gr
        elif kind=='film':f=7*gr*(.65+.23*lo)+6*ns(233,i=7)+5*mid+3*lo+9*screen((ns(52,5,9)-.86)*9)
        elif kind=='engraving':
            X=v*(x*52+y*(23+q%4))+.6*np.sin(v*y*3)+.8*lo;Y=v*(x*16-y*47)+.6*mid
            f=8-23*screen((np.cos(X)-.36-.22*lo)*8)-14*screen((np.cos(Y)-.73)*6)*screen((lo+.45)*2)+1.5*gr
        elif kind=='stipple':wall,ch=R.vor(x,y,61,65);f=6-29*screen((.39-wall+.15*ch)*5)*screen((ch+.43)*3)+2*mid+2*gr
        elif kind in ['craze','terrazzo','pebble','enamel','cell']:
            wall,ch=R.vor(x+.013*mid,y+.017*lo,18 if kind!='enamel' else 42,22+q%7)
            if kind=='craze':f=-26*np.exp(-wall*32)+10*np.exp(-wall*12)+9*lo+3*mic
            elif kind=='terrazzo':f=12*ch+6*mid;extra=screen((wall-.075)*17)[:,:,None]*ch[:,:,None]*(a-b)*.24
            elif kind=='enamel':f=11*lo+8*mic+16*screen((ch-.66)*8)*screen(wall*8)+1.3*gr
            elif kind=='pebble':f=15*np.tanh(5*wall)-7+5*ch+4*mic+1.4*gr
            else:f=17*np.exp(-wall*16)+10*ch-9*np.cos(wall*12)+2*gr
        elif kind=='ply':X=y*16+np.where((x>.42)&(x<.72),.35,0)+.12*lo;f=14*np.sin(v*X)+7*np.cos(v*X*3)+5*ns(4,101,7)+2*gr
        elif kind=='engine':X=x*(9+q%3);Y=y*11;d=np.sqrt(fold(X)**2+fold(Y)**2);f=16*np.sin(d*82)+5*np.cos(v*X)+4*mic
        elif kind=='offset':f=9*np.sin(v*(x*4+y*2)+phase[0])+15*screen((np.cos(v*(x*42+y*24))+.5*np.cos(v*(x*24-y*42))-.4)*3)+3*gr
        elif kind=='blind':X=fold(x*7+y*2);Y=fold(y*7);edge=np.minimum(X,Y);f=12*np.exp(-((edge-.17)*65)**2)-10*np.exp(-((edge-.205)*65)**2)+3*mic+2*gr
        elif kind=='tape':f=7*np.cos(v*x*82)+7*np.cos(v*y*61)+6*np.cos(v*(x*13-y*13))+6*ns(27,6,5)+3*gr
        elif kind=='scrape':f=9*lo-23*screen((ns(3,180,9)+.2*mid-.45)*4)+13*screen((ns(9,89,10)-.69)*7)+2*gr
        elif kind=='ash':f=17*ns(21,i=3)+8*np.maximum(0,mic)*2+12*screen((lo+.3*mid-.13)*4)+4*gr
        elif kind=='marble':f=14*np.sin(v*(x*3+.43*np.sin(v*y)+.65*lo))+.45*18*np.sin(v*(x*12+lo*2))+3*mic
        elif kind=='etch':f=5*lo-16*screen((mid+.34*mic-.12)*6)-11*screen((np.cos(v*(x*45-y*21)+lo)-.82)*7)+1.8*gr
        elif kind=='flake':wall,ch=R.vor(x+.021*mid,y+.017*lo,21,17);f=-18*screen((ch+.4*lo-.32)*8)*screen(wall*15)+8*mid+3*gr
        elif kind=='fold':d=fold(x*4)+.002*lo;e=fold(y*3);f=12*np.exp(-d*80)-12*np.exp(-abs(d-.024)*80)+11*np.exp(-e*70)-8*np.exp(-abs(e-.023)*70)+7*mid+2*gr
        elif kind=='wick':f=-24*screen((lo+.55*mid+.13*mic-.03)*5)+7*ns(92,17,6)+4*mic+1.5*gr
        elif kind=='prism':X=x*63+y*21;f=17*(X%1-.5)+13*((y*21-x*14)%1-.5)+3*mic
        elif kind=='moire':f=11*np.cos(v*(x*29+y*4))+11*np.cos(v*(x*30+y*6)+.7*lo)+4*mic
        elif kind.startswith('overlay'):
            j=int(kind[-1]);col=[ink,a,b,c][j]
            if j==0:mask=screen((lo+.59*mid+.16*mic-.09)*3)*screen(.45+mid+.25*mic)
            if j==1:mask=screen((np.cos(v*(x*(23+q%7)-y*8)+lo*4)-.79)*8)*screen((mid+.45)*2.0)
            if j==2:
                wall,ch=R.vor(x+.022*mid,y+.018*lo,12+q%6,14);mask=np.exp(-wall*29)*screen(.72+lo+.2*mic)
            if j==3:
                border=np.minimum(np.minimum(x,1-x),np.minimum(y,1-y));mask=screen((.10+.042*lo+.021*mid-border)*19)*screen(.54+mid+.5*mic)
            alpha=np.uint8(np.clip(mask*210+np.where(mask>.04,gr*2,0),0,230));pix=np.empty((len(y),N,4),np.uint8);pix[:,:,:3]=np.uint8(np.clip(col[None,None,:]+(mid*7)[:,:,None],0,255));pix[:,:,3]=alpha;out[top:top+len(y)]=pix;continue
        else:raise KeyError(kind)
        rgbout=tone[None,None,:]+f[:,:,None]*np.array([1,.94,.88]);out[top:top+len(y)]=np.uint8(np.clip(rgbout+(extra if extra is not None else 0),0,255))
    im=Image.fromarray(out);p.parent.mkdir(parents=True,exist_ok=True)
    if kind.startswith('overlay'):im.save(p,format='PNG',compress_level=4)
    else:im.save(p,format='WEBP',quality=91,method=3)
def build_style(z):
    S=next(s for s in STYLES if s['id']==z);names=FIN[z];rows=[]
    for j,kind in enumerate(TEX+[names[2],names[3]]+['overlay'+str(k)for k in range(4)]):
        alpha=j>=12;ext='png' if alpha else 'webp'
        name=(NAMES+[names[0],names[1],'干墨转印叠层','断续刻痕叠层','细裂线叠层','磨损边缘叠层'])[j]
        r=item(z,'textures',kind,S['zh']+' · '+name,'透明蒙版可叠在其他图形上。' if alpha else '2048像素原生周期材料，可直接平铺或作为色彩纹理。',0 if j<5 else (1 if j in [5,6,10,12,14] else 2),'transparent-overlay' if alpha else 'tile',ext=ext,alpha=alpha,tile=not alpha,family=kind if j<10 else None,credit='upgrade' if j<10 else 'new',process=kind)
        p=outfile(z,r)
        if not p.exists():generate(S,kind,zlib.crc32((z+':'+kind).encode())&0x7fffffff,p)
        with Image.open(p)as im:
            assert im.size==(2048,2048)
            if alpha:assert im.getchannel('A').getextrema()[0]==0 and im.getchannel('A').getextrema()[1]>0
        rows.append(r)
    save_batch(z,'textures',rows);print(z,'16 native 2K surfaces',flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--styles',nargs='*');ap.add_argument('--workers',type=int,default=2);args=ap.parse_args()
    with cf.ProcessPoolExecutor(max_workers=args.workers)as pool:list(pool.map(build_style,args.styles or [s['id']for s in STYLES]))
    report()
