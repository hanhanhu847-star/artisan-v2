"""V2 作品台账。源文件、预览和业务状态不等于独立作品；不改动 V1 素材。"""
import json,hashlib,collections,sys,os
from pathlib import Path
from styles_data import ROOT,STYLES,dump,write
from generate_index import dimensions,digest
TARGET=dict(backgrounds=10,textures=16,ornaments=24,icons=32,illustrations=10,ui=12)
SERIES={
'bauhaus':'几何印刷所|现代建筑工坊|实验舞台',
'art-deco':'剧院之夜|退台都会|金工工艺',
'swiss':'字级与基线|交通导向|信息网格',
'neo-brutalism':'街头张贴|铆接结构|地下印刷',
'memphis':'层压板工坊|玩具建筑|舞池节奏',
'editorial':'书籍装帧|杂志开页|编辑校样',
'wabi-sabi':'手作器物|枯山庭院|植物与和纸',
'dark-academia':'古籍装帧|阅览室|博物馆档案',
'celestial-atlas':'古典星图|深空天体|天文观测',
'dunhuang':'壁画叙事|藻井纹样|矿物色工坊',
'cartography':'海路测绘|山川地貌|城市地图',
'natural-history':'植物图版|动物标本|地质档案',
'retrofuturism':'轨道航行|模拟终端|明日交通',
'cyberpunk':'雨夜都市|地下电路|数据终端',
'blueprint':'机械装配|建筑测绘|管线与电路',
'generative-art':'离散生长|连续流场|计算几何'}
SERIES={k:v.split('|') for k,v in SERIES.items()}
def legacy_family(a):
    cat=a['category'];f=Path(a['file_path']);stem=f.stem
    if cat=='ui':
        kind=stem.rsplit('-',1)[0]
        revised=True
        return kind,stem.endswith('-normal') and not revised,'同组状态合并；有V2布局的旧组不再占额'
    if cat=='textures':return stem,False,'保留384px原件；原生2K重制通过验收后按同一家族计一次'
    if cat=='icons':return stem,False,'V1共用轮廓保留；V2构型重绘按同一语义家族计一次'
    if cat=='backgrounds':
        if stem.startswith('photo-'):return 'photo-environment',stem!='photo-window','官方全景及取景派生合并'
        if stem in ['solid','wash','repeat']:return stem,False,'保留基础色面或重复纹样，不占高清独立构图指标'
        return 'field-study',stem=='field-study-3840','同一母题、尺寸、重排与配色只计一次'
    if cat=='ornaments':return stem,f.suffix=='.svg' and stem not in ['ribbon','title-frame','caption-frame','chapter'],'同名PNG与SVG只计一次；角标和信息饰件以V2重绘占额'
    return stem,True,'通过V1资产校验的独立语义或形态'
def meta_folder(s):return ROOT/'STYLES'/s/'v2-records'
def save_batch(s,batch,rows):
    paths=set()
    for r in rows:
        p=ROOT/'STYLES'/s/r['file'];assert p.is_file() and r['file'] not in paths and r['series'] in SERIES[s];paths.add(r['file'])
    dump(meta_folder(s)/(batch+'.json'),rows)
def item(s,cat,name,title,use,series,role,*,ext='svg',alpha=True,tile=False,family=None,credit='new',**extra):
    return dict(file=f'{cat}/v2-{name}.{ext}',asset_name=title,intended_usage=use,series=SERIES[s][series],role=role,transparency=alpha,tiling=tile,origin='original',family=family or 'v2-'+name,credit=credit,**extra)
def outfile(s,r):return ROOT/'STYLES'/s/r['file']
def inventories():
    old=json.loads((ROOT/'AUDIT/v1-asset-index.json').read_text(encoding='utf8'))['assets'];result={}
    for S in STYLES:
        z=S['id'];files=[a for a in old if a['style_id']==z];legacy=collections.Counter();new=collections.Counter();upgrade=collections.Counter();groups=collections.defaultdict(set);families=set();extra_rows=[]
        for a in files:
            fam,eligible,_=legacy_family(a)
            if eligible:legacy[a['category']]+=1;families.add((a['category'],fam))
        for p in sorted(meta_folder(z).glob('*.json')):
            for r in json.loads(p.read_text(encoding='utf8')):
                cat=r['file'].split('/')[0];key=cat,r['family']; extra_rows.append(r)
                if r.get('credit')=='variant':continue
                if key in families:raise ValueError('Family counted twice: '+str((z,key)))
                families.add(key);(upgrade if r.get('credit')=='upgrade' else new)[cat]+=1;groups[r['series']].add(key)
        total=legacy+new+upgrade;gaps={k:max(0,v-total[k])for k,v in TARGET.items()}
        result[z]=dict(title=S['zh'],original_files=len(files),original_eligible=dict(legacy),upgraded_families=dict(upgrade),new_families=dict(new),v2_files=len(extra_rows),eligible=dict(total),total=sum(total.values()),count_gaps=gaps,series={k:len(groups[k])for k in SERIES[z]})
    return result
def report():
    res=inventories();dump(ROOT/'AUDIT/progress.json',res)
    lines=['# ARTISAN V2 分批进度','', '数量仅表示台账内可独立使用的作品家族；最终验收见EXPANSION_REPORT.md与包旁交付回执。每套 V1 有130个素材文件；十个384px纹理、20个共用轮廓图标和低对比三角角标均保留原件，V2重制按同一家族计一次。14类旧UI的V2默认视觉均已重排；组件五态不重复计。','', '| 风格 | 原有达标家族 | 升级或重绘家族 | 新增家族 | 当前合计 | 数量缺口（背景/纹理/装饰/图标/插画/UI） |','|---|---:|---:|---:|---:|---|']
    for d in res.values():lines.append(f"| {d['title']} | {sum(d['original_eligible'].values())} | {sum(d['upgraded_families'].values())} | {sum(d['new_families'].values())} | {d['total']} | "+' / '.join(str(d['count_gaps'][k])for k in TARGET)+' |')
    write(ROOT/'AUDIT/PROGRESS.md','\n'.join(lines)+'\n')
if __name__=='__main__':report()
