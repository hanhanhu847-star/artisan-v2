"""重建原创素材。依赖 Pillow、NumPy。照片由 acquire_photos.py 单独获取。"""
import numpy as np, hashlib, json
from PIL import Image
from primitives import *
TEX='paper metal stone textile wood plaster halftone film engraving stipple'.split()
TZ='纸纤 拉丝金属 石脉 织物 木纹 斑驳墙面 印刷网点 胶片颗粒 雕版刻线 颗粒噪点'.split()
def texture(S,kind,N=384):
    j=TEX.index(kind);seed=S['no']*1193+j*139;rr=np.random.default_rng(seed); yy,xx=np.mgrid[:N,:N]
    x=xx/N;y=yy/N;u=x*2*pi;v=y*2*pi
    def noise(k,m):
        grid=rr.uniform(-1,1,(m,k));X=x*k;Y=y*m;ix=X.astype(int)%k;iy=Y.astype(int)%m;fx=X%1;fy=Y%1;fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy)
        return (grid[iy,ix]*(1-fx)+grid[iy,(ix+1)%k]*fx)*(1-fy)+(grid[(iy+1)%m,ix]*(1-fx)+grid[(iy+1)%m,(ix+1)%k]*fx)*fy
    grain=noise(160,160);low=noise(5,5);off=rr.uniform(-pi,pi);f=S['no']%5
    if j==0:t=.46*grain+.35*noise(90,12)+.23*noise(14,85)+.16*low
    if j==1:t=.27*np.sin(v*(44+f)+np.sin(u*2+off))+.56*noise(5,150)+.28*np.cos(v+off)+.13*grain
    if j==2:t=.6*np.exp(-6*abs(np.sin(u*(2+f%2)+.6*v/pi*0+low*2.6+noise(12,12)*.3+off)))-.26+.45*noise(18,18)+.2*grain
    if j==3:t=(np.sin(u*(23+f))*.45+np.sin(v*(22+f))*.45)*(.65+.3*np.cos(u*(23+f)+v*(22+f)))+.18*grain
    if j==4:t=.38*np.sin(u*(11+f)+2.1*np.sin(v+off)+2*low)+.25*np.sin(u*(52+f)+2*low)+.32*noise(91,5)
    if j==5:t=.57*low+.32*noise(25,20)+.2*grain-.38*np.maximum(0,noise(55,53)-.52)*3
    if j==6:t=np.clip((np.cos((u+v)*(12+f)+off)+np.cos((u-v)*(12+f))-.38)*3,-1,1)*.62+.1*grain
    if j==7:t=.62*grain+.32*noise(220,197)+.2*noise(42,36)
    if j==8:t=.6*np.tanh(2.6*np.sin(u*32+v*(19+f)+.9*np.sin(v*3+off)))+.22*np.sin(u*24-v*32)+.08*grain
    if j==9:t=np.clip((noise(88,84)-.25)*4,-.5,1)*.65+.3*noise(16,16)
    def rgb(c):return np.array([int(c[i:i+2],16)for i in [1,3,5]])
    base=rgb(S['palette'][0])*.77+rgb(S['palette'][3])*.23
    img=base[None,None,:]+t[:,:,None]*np.array([34,30,25])[None,None,:]
    return Image.fromarray(np.uint8(np.clip(img,0,255)))
def make():
    photos={r['style_id']:r for r in json.loads((ROOT/'LICENSES/photo-sources.json').read_text(encoding='utf8')) if 'path'in r}
    for S in STYLES:
        folder=ROOT/'STYLES'/S['id'];assets=[];bg,ink,a,b,c=S['palette'];jobs=[]
        def record(cat,name,title,use,alpha=False,tile=False,**extra):
            rel=f'{cat}/{name}';row=dict(file=rel,asset_name=title,intended_usage=use,transparency=alpha,tiling=tile,origin='polyhaven' if 'photo' in extra else 'original');row.update(extra);assets.append(row);return folder/rel
        def vec(cat,name,title,body,use,alpha=False,tile=False):
            p=record(cat,name+'.svg',title,use,alpha,tile);write(p,body);return p
        coverpath=vec('backgrounds','field-study',S['title']+' · 横向母版',cover(S,1920,1080,'native'),'可编辑横向封面、演示文稿主图。')
        for w,h in [(1920,1080),(2560,1440),(3840,2160)]:
            p=record('backgrounds',f'field-study-{w}.jpg',f'{S["title"]} · {w} 横幅','由同一矢量母版按目标像素直接栅格化，适合桌面、演示与视频。')
            jobs.append(dict(src=coverpath.relative_to(ROOT).as_posix(),dst=p.relative_to(ROOT).as_posix(),w=w,h=h))
        for key,w,h,label in [('portrait',1080,1920,'竖幅'),('square',1600,1600,'方形'),('panorama',3440,1440,'超宽')]:
            vec('backgrounds',key,S['title']+' · '+label,cover(S,w,h,'native'),label+'图版；为该比例重新排列主图与细部。')
        dark=lumin(bg)<.35
        vec('backgrounds','alternate',S['title']+(' · 浅色' if dark else ' · 深色'),cover(S,1920,1080,'light' if dark else 'dark'),'与默认版配对的明暗背景。')
        vec('backgrounds','solid','单色底纸',svg(1920,1080,rect(0,0,1920,1080,bg)),'纯色静区，供图表和长正文叠放。',tile=True)
        grad='<defs><linearGradient id="wash" x2="1" y2=".65"><stop stop-color="'+bg+'"/><stop offset=".60" stop-color="'+b+'"/><stop offset="1" stop-color="'+a+'"/></linearGradient></defs>'
        vec('backgrounds','wash','三色过渡底',svg(1920,1080,grad+rect(0,0,1920,1080,'url(#wash)')),'色彩过渡背景；不是表面纹理。')
        pattern=rect(0,0,128,128,bg)+symbol(S,12,12,34)+symbol(S,76,76,34,180)
        vec('backgrounds','repeat','连续图样底',svg(128,128,pattern),'横纵重复使用的图形背景；以128为完整周期。',tile=True)
        for j,k in enumerate(TEX):
            p=record('textures',k+'.png',S['zh']+' · '+TZ[j],'程序拟作的'+TZ[j]+'，以原尺寸平铺；正文后建议混合 6% 至 18%。',tile=True)
            p.parent.mkdir(exist_ok=True);texture(S,k).save(p,optimize=False)
        for j,k in enumerate(ORNS):
            p=vec('ornaments',k,ORN_LABEL[j],ornament(S,j),'编辑、框选、重排或叠在透明图层上。',True)
            if j in [2,8]:
                side=288 if j==2 else 384;dst=record('ornaments',k+'.png',ORN_LABEL[j]+' · 透明 PNG','透明栅格副本，可直接拖入 Office、海报或视频。',True)
                jobs.append(dict(src=p.relative_to(ROOT).as_posix(),dst=dst.relative_to(ROOT).as_posix(),w=side,h=side))
        for j,k in enumerate(ICON_NAMES):vec('icons',k,ICON_ZH[j],icon(S,j),'64单位画板；界面操作图标，搭配文字或可访问名称。',True)
        for j,k in enumerate(UIN):
            for q,st in enumerate(STATES):vec('ui',k+'-'+st,UIZH[j]+' · '+STLAB[q],ui(S,j,q),'独立可编辑组件视觉稿；状态：'+STLAB[q]+'。交互语义由宿主实现。',True)
        for v,label in enumerate(S['motifs'].split(' / ')):vec('illustrations',f'study-{v+1:02d}',label,svg(300,300,motif(S,v)),'原创独立插图，可作封面图形或章节标识。',True)
        ph=photos.get(S['id'])
        if ph:
            name=Path(ph['path']).name;record('backgrounds',name,'环境摄影 · '+ph['title'],'官方全景 JPEG 原件，可再取景。是配套摄影，不是历史流派文物照片。',photo=ph['slug'])
            p=record('backgrounds','photo-window.jpg','摄影取景 · '+ph['title'],'从原件截取校正透视的横向环境画面。',photo=ph['slug'],derived=True)
            photo_window(folder/'backgrounds'/name,p)
        dump(folder/'style.json',S);dump(folder/'asset-meta.json',assets);dump(folder/'raster-jobs.json',jobs);dump(folder/'tokens.json',dict(style_id=S['id'],colors=dict(zip(['background','ink','accent','secondary','highlight'],S['palette'])),font=S['font'],group=S['group'],motion_ms=[120,200,280],reduced_motion=True))
        print(S['id'],len(assets),flush=True)
    dump(ROOT/'TOOLS'/'style-definitions.json',STYLES)
def photo_window(src,dst):
    # 官方原件保留不动。JPEG 解码下采样后用透视射线从球面取景；不把此派生图称为4K原片。
    im=Image.open(src);im.draft('RGB',(3200,1600));im=im.convert('RGB');src_a=np.asarray(im);H,W=src_a.shape[:2]
    w,h=1440,810;xx,yy=np.meshgrid((np.arange(w)+.5-w/2)/(w/2),(np.arange(h)+.5-h/2)/(w/2))
    lon=np.arctan(xx*1.28);lat=np.arctan2(-yy*1.28,np.sqrt(1+(xx*1.28)**2))
    X=(.5+lon/(2*pi))*W;Y=(.5-lat/pi)*H
    x0=np.floor(X).astype(int)%W;y0=np.clip(np.floor(Y).astype(int),0,H-2);fx=(X-np.floor(X))[:,:,None];fy=(Y-np.floor(Y))[:,:,None]
    rgb=(src_a[y0,x0]*(1-fx)+src_a[y0,(x0+1)%W]*fx)*(1-fy)+(src_a[y0+1,x0]*(1-fx)+src_a[y0+1,(x0+1)%W]*fx)*fy
    Image.fromarray(np.uint8(rgb)).save(dst,quality=90,optimize=True)
if __name__=='__main__':
    # Only process explicitly downloaded files already checked against upstream MD5.
    Image.MAX_IMAGE_PIXELS=1_500_000_000
    make()
