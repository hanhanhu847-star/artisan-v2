import json
from PIL import Image,ImageDraw,ImageFont
from styles_data import ROOT,STYLES
im=Image.new('RGB',(1100,1000),'#f3efe6');d=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',19)
for n,S in enumerate(STYLES):
 x=n%4*275;y=n//4*250
 tile=Image.new('RGBA',(260,210),S['palette'][0]);src=Image.open(ROOT/f'PREVIEWS/v2/{S["id"]}/ornaments/v2-corner-badge.svg.webp').convert('RGBA');src.thumbnail((200,200));tile.alpha_composite(src,((260-src.width)//2,5));im.paste(tile.convert('RGB'),(x+7,y+5));d.text((x+9,y+219),S['zh'],fill='#27302c',font=f)
im.save(ROOT/'PREVIEWS/v2-corner-badges.jpg',quality=94)
