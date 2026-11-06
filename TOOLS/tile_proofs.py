"""将十类纹理按各自原始周期拼接成 2×2，再缩小生成全套检阅图。"""
from PIL import Image, ImageDraw,ImageFont
from styles_data import *
from build_assets import TEX
W=1192;out=Image.new('RGB',(W,16*78+68),'#f3f1e8');d=ImageDraw.Draw(out)
d.text((14,12),'ARTISAN / 2 x 2 TILE PROOFS',fill='#202b26')
for j,k in enumerate(TEX):d.text((155+j*103,42),k,fill='#263b32')
for i,s in enumerate(STYLES):
    y=64+i*78;d.text((9,y+26),s['id'],fill='#202b26')
    for j,k in enumerate(TEX):
        with Image.open(ROOT/'STYLES'/s['id']/'textures'/(k+'.png')) as im:
            w,h=im.size;tile=Image.new('RGB',(2*w,2*h))
            for u in range(2):
                for v in range(2):tile.paste(im,(u*w,v*h))
            tile=tile.resize((72,72),Image.Resampling.LANCZOS);out.paste(tile,(158+j*103,y))
out.save(ROOT/'PREVIEWS/texture-proof.jpg',quality=90)
