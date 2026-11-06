"""从公开 HYG 星表与 Stellarium 连线绘制十二幅星图。仅 --acquire 需要网络。"""
import csv,io,gzip,urllib.request,math,json,hashlib,sys,re
from v2_registry import *
from artwork import svg,path,rect,circle,line,curve,txt,ell,ringticks,n
LIC=ROOT/'LICENSES'/'celestial-data';DATA=LIC/'zodiac-subset.json'
ZOD=list(zip('Ari Tau Gem Cnc Leo Vir Lib Sco Sgr Cap Aqr Psc'.split(),'白羊座 金牛座 双子座 巨蟹座 狮子座 室女座 天秤座 天蝎座 人马座 摩羯座 宝瓶座 双鱼座'.split(),'Aries Taurus Gemini Cancer Leo Virgo Libra Scorpius Sagittarius Capricornus Aquarius Pisces'.split()))
SURL='https://github.com/Stellarium/stellarium/tree/master/skycultures/modern';HURL='https://github.com/astronexus/HYG-Database/tree/main/hyg/CURRENT'
BY='Stellarium 团队（modern 连线）与 David Nash / Astronexus（HYG 星表）；ARTISAN 制图'
def read(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'ARTISAN-astronomical-plates/2.0'}),timeout=60)as f:return f.read()
def acquire():
    LIC.mkdir(parents=True,exist_ok=True)
    def commit(repo,branch):return json.loads(read('https://api.github.com/repos/'+repo+'/commits/'+branch))['sha']
    sc=commit('Stellarium/stellarium','master');hc=commit('astronexus/HYG-Database','main')
    sbase='https://raw.githubusercontent.com/Stellarium/stellarium/'+sc+'/skycultures/modern/'
    hbase='https://raw.githubusercontent.com/astronexus/HYG-Database/'+hc+'/hyg/CURRENT/'
    sl=read(sbase+'description.md').decode();hl=read(hbase+'LICENSE').decode();assert 'Text and data: CC BY-SA 4.0' in sl and 'by-sa/4.0' in hl.lower()
    legal=read('https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt').decode();assert 'ShareAlike' in legal
    write(LIC/'CC-BY-SA-4.0.txt',legal);write(LIC/'HYG-license.txt',hl);write(LIC/'Stellarium-license.txt',sl.split('## Authors')[-1].strip())
    stars=json.loads(read(sbase+'index.json'));codes={a for a,_,_ in ZOD};lines={s['id'].split()[-1]:s['lines'] for s in stars['constellations'] if s['id'].split()[-1] in codes}
    hips={int(i) for v in lines.values()for pair in v for i in pair};raw=read(hbase+'hygdata_v40.csv.gz');out={}
    for r in csv.DictReader(io.StringIO(gzip.decompress(raw).decode('utf-8-sig'))):
        if r['hip'] and int(r['hip']) in hips:out[r['hip']]=dict(ra=float(r['ra']),dec=float(r['dec']),mag=float(r['mag']))
    missing=hips-{int(h) for h in out};assert not missing,missing
    dump(DATA,dict(license='CC-BY-SA-4.0',attribution=BY,stellarium=sbase+'index.json',hyg=hbase+'hygdata_v40.csv.gz',hyg_md5=hashlib.md5(raw).hexdigest(),modifications='保留十二星座折线及所涉HIP编号、赤经（小时）、赤纬（度）与星等，其他字段不分发。',lines=lines,stars=out))
    write(LIC/'ATTRIBUTION.md',f'# 十二星座数据与图版\n\n{BY}。\\n坐标和星等使用 [HYG v4.0]({hbase}hygdata_v40.csv.gz)；连线使用 [Stellarium modern]({sbase}index.json)，许可说明见该项目 description.md。仅使用数据，不使用原插画。\\n\\n数据子集与据此重绘的十二幅 SVG 均按 CC BY-SA 4.0 分发。改动：筛选、切平面投影、重绘刻度、星点、图例和中英文标签。本段与来源链接应随这些图版保留，改编仍按相同许可发布。IAU 定义星座天区边界，不规定唯一的连线。本图不绘制官方边界，不代替观测星历。'.replace('\\n','\n'))
def make():
    d=json.loads(DATA.read_text(encoding='utf8'));S=next(s for s in STYLES if s['id']=='celestial-atlas');bg,ink,gold,blue,red=S['palette'];rows=[]
    for nr,(code,zh,en) in enumerate(ZOD,1):
        ls=d['lines'][code];stars={hip:d['stars'][str(hip)] for l in ls for hip in l}
        rad=math.radians;cs=math.cos;sn=math.sin;at=math.atan2
        xyz=[(cs(rad(r['dec']))*cs(rad(r['ra']*15)),cs(rad(r['dec']))*sn(rad(r['ra']*15)),sn(rad(r['dec'])))for r in stars.values()]
        a0=at(sum(t[1]for t in xyz),sum(t[0]for t in xyz));d0=at(sum(t[2]for t in xyz),math.hypot(sum(t[0]for t in xyz),sum(t[1]for t in xyz)))
        def proj(ra,dec):
            a,dd=rad(ra*15),rad(dec);den=sn(d0)*sn(dd)+cs(d0)*cs(dd)*cs(a-a0)
            return -cs(dd)*sn(a-a0)/den,-(cs(d0)*sn(dd)-sn(d0)*cs(dd)*cs(a-a0))/den
        pts={hip:proj(r['ra'],r['dec'])for hip,r in stars.items()};xs,ys=zip(*pts.values());scale=min(790/max(.001,max(xs)-min(xs)),450/max(.001,max(ys)-min(ys)));cx=(min(xs)+max(xs))/2;cy=(min(ys)+max(ys))/2
        def draw(pt):return 600+(pt[0]-cx)*scale,449+(pt[1]-cy)*scale
        o=rect(0,0,1200,900,bg)+rect(25,25,1150,850,'none',gold,2)+rect(32,32,1136,836,'none',blue,.8)
        o+=txt(65,100,zh,46,ink,'SimSun,serif')+txt(65,139,en.upper()+'   /   '+code,20,gold,'Georgia')+txt(942,93,f'PLATE  {nr:02d}',23,gold,'Georgia')
        o+=line(61,162,1138,162,gold,1)+line(61,746,1138,746,gold,1)
        o+='<defs><clipPath id="field"><rect x="67" y="172" width="1065" height="561"/></clipPath></defs><g clip-path="url(#field)">'
        ra0=math.degrees(a0)/15;dd0=math.degrees(d0)
        for ra in [round(ra0*2)/2+i*.5 for i in range(-8,9)]:o+=curve([draw(proj(ra,dd0+i*.5))for i in range(-66,67)],blue,.5)
        for dec in [round(dd0/5)*5+i*5 for i in range(-8,9)if abs(round(dd0/5)*5+i*5)<80]:o+=curve([draw(proj(ra0+i*.06,dec))for i in range(-67,68)],blue,.5)
        for seq in ls:o+=curve([draw(pts[h])for h in seq],gold,2.6)
        for hip,r in stars.items():
            x,y=draw(pts[hip]);rr=max(2.9,8.3-r['mag']*1.02);o+=circle(x,y,rr+2,bg)+circle(x,y,rr,ink)
        for j,(hip,r) in enumerate(sorted(stars.items(),key=lambda a:a[1]['mag'])[:2]):
            x,y=draw(pts[hip]);o+=line(x+7,y-7,x+20,y-21,gold,1)+txt(x+22,y-23,'HIP '+str(hip),13,ink,'monospace')
        o+='</g>'+txt(65,791,'星等',15,ink,'SimSun')+''.join(circle(132+i*50,785,8.3-(i+1)*1.02,ink)+txt(124+i*50,816,str(i+1),13,gold,'monospace')for i in range(4))
        o+=txt(408,790,'切平面投影   /   北向上，东向左',17,ink,'SimSun')+txt(408,822,'HYG 4.0 · Stellarium modern · CC BY-SA 4.0',15,gold,'Georgia')
        o='<metadata>'+BY+' | CC BY-SA 4.0 | '+HURL+' | '+SURL+' | 选择数据、投影并重新绘制</metadata>'+o
        r=item(S['id'],'illustrations','zodiac-'+code.lower(),zh+' · 恒星连线图','文化星图与真实恒星位置对照；北上东左，星等映射点径。',0,'data-plate',alpha=False,license='CC-BY-SA-4.0',author=BY,source=HURL+' ; '+SURL,license_file='LICENSES/celestial-data/CC-BY-SA-4.0.txt',attribution=BY+' / CC BY-SA 4.0',modification_status='HYG v4.0 星表子集与 Stellarium modern 连线：切平面投影，重新绘制；不是官方星座边界。')
        write(outfile(S['id'],r),svg(1200,900,o));rows.append(r)
    save_batch(S['id'],'zodiac',rows);report()
if __name__=='__main__':
    if '--acquire' in sys.argv:acquire()
    make()
