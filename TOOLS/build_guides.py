from primitives import *
import json,numpy as np
from PIL import Image
def relsource(S,refs):
    r=next((r for r in refs if r['style']==S['id'] and r.get('status')==200),None)
    return f'延伸阅读：[{S["en"]} 相关馆藏或资料入口]({r["url"]})。此链接仅供研究，没有从网页提取作品。' if r else '艺术背景为本项目的简要说明。未将未经核实的在线页面、馆藏图像或历史文字收入素材。'
def run():
    photos={p['style_id']:p for p in json.loads((ROOT/'LICENSES/photo-sources.json').read_text(encoding='utf8')) if 'path'in p}
    ref=ROOT/'TOOLS/reference-check.json';refs=json.loads(ref.read_text(encoding='utf8')) if ref.exists() else []
    at=[];allcss=[];tokens={}
    for S in STYLES:
        z=S['id'];folder=ROOT/'STYLES'/z;bg,ink,a,b,c=S['palette'];ph=photos.get(z)
        photo=(f'摄影：[{ph["title"]}]({ph["source"]})，作者 {", ".join(ph["authors"])}；Poly Haven / CC0-1.0。保留官方原始全景 JPEG，另有 1440×810 透视取景。' if ph else '摄影未获取，详见来源清单。')
        guide=f"""# {S['zh']} / {S['en']}

## 来历与视觉语言
{S['history']} {relsource(S,refs)}

{S['form']} 本套主图《{S['title']}》围绕「{S['motifs']}」制作。打开 illustrations 中三幅独立图形，可分开改变位置、尺寸和层次。它们是当代原创图形，并非历史原件摹本。

## 配色与排版
| 用途 | 色号 | 应用位置 |
|---|---|---|
| 基底 | {bg} | 大面积背景 |
| 墨色 | {ink} | 正文、轮廓、信息标记 |
| 主强调 | {a} | 当前操作、首要图形 |
| 次强调 | {b} | 结构或次级图形 |
| 点色 | {c} | 少量定位与标记 |

字体建议：{S['font']} 字体不随包分发。{S['layout']} 以 4 / 8 / 16 / 24 / 40 为间距阶梯；双栏在窄屏回到单栏，避免靠缩小正文字号维持原构图。

## 图形、纹理与背景
- **图形语法：**{S['form']} 从单件主图、一个功能符号和一条边饰开始搭配，避免三者等大。
- **纹理：**{S['material']} 每个纹理的像素周期是 384；在 100% 和 200% 比例下分别查看。PNG 是程序化表面，不是材料扫描。需要实景时使用 photo 文件。
- **背景：**横版 field-study 为可编辑母版；三张 JPG 是按目标尺寸直接栅格化的同构图版本。portrait、square、panorama 按比例重排主形。alternate 是另一明暗方案。solid 为单色，wash 为渐变，repeat 是可重复图样。大字号和正文放在图形的空白一侧；不要把有纹理背景当成表格底。
- **透明层：**ornaments 中的 corner.png、seal.png 可直接叠加；SVG 可按独立节点改色。图标使用 64 单位画板；不要同时调用其他风格的同名图标。

## 组件与动效
{S['ui']} ui 目录提供 14 类组件，每类五种可编辑状态。文件名末尾 normal / hover / selected / disabled / error 分别对应默认、悬停、选中、禁用和错误。静态图是设计交付；实际键盘、焦点、错误提示应由宿主语义控件承担。

建议按压反馈 120ms，状态变化 200ms，面板进入 280ms。这是应用化建议而非历史风格参数。加载区描述实际进度；不要把图版中的示例百分比当作业务数据。系统减少动态时直接切换状态，触屏不依赖悬停。

## 使用判断
- **适用：**{S['use']}。先挑一幅主图，在次级页面只保留色彩、字体和一处识别性边饰。
- **避免：**{S['avoid']}
- **搭配：**{S['combine']}
- **制作实例：**1920×1080 横向版用于开场；章节页以 rule.svg 分割标题与说明，后续列表使用 table-normal.svg 作版式参考。需要打印时使用 SVG 母版，交由输出流程做色彩转换，本包不伪称 CMYK 印刷稿。

## 实际来源与使用条件
{photo} 这张摄影按材质和空间气氛配套，不代表该流派的历史作品或拍摄地与流派同名。其他素材由 ARTISAN 生成器制作，条件见 LICENSES/CC-BY-4.0.txt；逐文件来源、作者、修改说明和文件指纹在 ASSET_INDEX.json。
"""
        write(folder/'STYLE_GUIDE.md',guide)
        prompt=f"""# {S['zh']}风格接入指令
先确认目标页面的主要操作与信息密度；从 ASSET_INDEX.json 筛选 style_id 等于 {z}，检查 license 与 intended_usage。以 {bg} 为基底、{ink} 为正文、{a} 为主强调。{S['layout']}
主图优先调用 STYLES/{z}/illustrations/study-01.svg；选用一项同族边饰与图标，例如 ornaments/rule.svg 和 icons/search.svg。{S['form']} {S['ui']}
需要背景时按目标比例选择真实文件，不把缩略图放大；纹理必须标记 tiling=true 才按周期铺设。保留所有随所选素材对应的来源信息。{S['avoid']} {S['combine']}
交付业务代码前核对键盘、触屏、禁用、错误和减少动效状态；记录所用 asset_id、路径与本地改动。"""
        write(folder/'STYLE_PROMPT.md',prompt);write(ROOT/'CODEX/STYLE_PROMPTS'/f'{z}.md',prompt)
        p=json.loads((folder/'tokens.json').read_text(encoding='utf8'));tokens[z]=p
        i=S['no']-1;rad=[0,3,0,0,14,0,7,2,16,4,2,3,22,0,0,10][i];th=3 if i==3 else 1
        font='"Georgia","Songti SC","SimSun",serif' if i in [1,5,6,7,8,9,10,11] else '"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif'
        scope=f'[data-artisan="{z}"]'
        css=scope+'{'+''.join(f'--at-{k}:{v};'for k,v in zip(['bg','ink','accent','secondary','spot'],S['palette']))+f'--at-on-accent:{texton(a)};--at-radius:{rad}px;--at-weight:{th}px;--at-display:{font};--at-error:{("#8d2c27" if lumin(bg)>.35 else "#ffb6aa")};'+'}'
        accents=[
          'border-top:6px solid var(--at-accent)','outline:1px solid var(--at-accent);outline-offset:-6px','border-width:0 0 2px;border-radius:0','box-shadow:5px 5px 0 var(--at-ink)','box-shadow:4px 5px 0 var(--at-secondary);border-bottom-left-radius:1px','border-inline:0;border-top:2px solid var(--at-ink)','border-radius:6px 18px 8px 21px','border-left:8px double var(--at-accent)','border-top:3px double var(--at-accent)','border:4px double var(--at-secondary)','outline:1px dashed var(--at-secondary);outline-offset:-6px','border-bottom:3px double var(--at-secondary)','border:3px double var(--at-ink)','border-left:6px solid var(--at-accent);box-shadow:3px 0 var(--at-secondary)','outline:1px dashed var(--at-secondary);outline-offset:3px','border-radius:3px 22px 3px 22px']
        css+='\n'+scope+' .at-panel{'+accents[i]+'}\n';allcss.append(css);write(folder/'theme.css',css)
        qss=f"""/* {S['zh']}；用于 QApplication.setStyleSheet，由 Qt 处理键盘与状态。 */
QWidget {{background:{bg};color:{ink};font-size:14px;}}
QPushButton,QLineEdit,QComboBox,QListWidget,QTableView {{border:{th}px solid {ink};border-radius:{rad}px;padding:6px;}}
QPushButton {{background:{a};color:{texton(a)};min-height:28px;}}
QPushButton:hover,QLineEdit:focus {{border:2px solid {b};}}
QPushButton:checked,QListView::item:selected {{background:{ink};color:{bg};}}
QPushButton:disabled {{background:{bg};color:{ink};border:1px dashed {b};}}
QLineEdit[invalid="true"] {{border:2px solid {("#8d2c27" if lumin(bg)>.35 else "#ffb6aa")};}}
QProgressBar {{border:1px solid {ink};text-align:center;}} QProgressBar::chunk {{background:{b};}}"""
        write(ROOT/'ADAPTERS/pyside6/themes'/f'{z}.qss',qss)
        if ph:at.append(f'| {S["zh"]} | [{ph["title"]}]({ph["source"]}) | {", ".join(ph["authors"])} | CC0-1.0 | 官方全景原件 + 透视取景 |')
    dump(ROOT/'ADAPTERS/colors.json',tokens);write(ROOT/'ADAPTERS/web/themes.css','\n'.join(allcss))
    write(ROOT/'LICENSES/ATTRIBUTION.md','# 摄影署名与变更记录\n\n| 风格 | 摄影 | 作者（官方元数据） | 许可 | 包内状态 |\n|---|---|---|---|---|\n'+'\n'.join(at)+'\n\n逐文件原始下载地址、原件 MD5 见 photo-sources.json。CC0 不强制署名，本库保留署名便于追溯。网页截图、缩略图、商标和站点代码均未作为开放素材引入。')
    write(ROOT/'LICENSES/THIRD_PARTY_LICENSES.md','''# 第三方素材条件
包内第三方实拍图像来自 [Poly Haven](https://polyhaven.com/license)，官方说明其资源采用 CC0。使用的是资产文件接口给出的 tonemapped JPEG，不是站点展示用缩略图。CC0 允许复制、改编、商业使用与再分发，无强制署名要求；不保证画面中第三方商标、肖像、建筑或其他权利都已获得单独许可。详情见 [CC0](https://creativecommons.org/publicdomain/zero/1.0/) 和本目录的来源清单。
每种风格有两项摄影记录：一张官方 JPEG 未修改；一张以透视射线取景、双线性取样并重新编码的 1440×810 衍生背景。来源记录写明实际作者和变更。未用 CC BY、NC 或 ND 图片填充本包。推荐字体只列名称，不包含第三方字体文件。''')
    assert (ROOT/'LICENSES/CC-BY-4.0.txt').is_file(), 'Keep the official CC BY 4.0 legal text'
    shared=[]
    def make(cat,name,body,title,use,tr,til=False):
        write(ROOT/'SHARED'/cat/name,body);shared.append(dict(file=cat+'/'+name,asset_name=title,intended_usage=use,transparency=tr,tiling=til))
    make('patterns','alpha-grid.svg',svg(32,32,rect(0,0,32,32,'#F4F3ED')+rect(0,0,16,16,'#D3D4CF')+rect(16,16,16,16,'#D3D4CF')),'透明预览棋盘','底层透明度检查，不当作素材内容透明。',False,True)
    make('utility-assets','registration.svg',svg(96,96,circle(48,48,25,'none','#1D2625',1.5)+path('M3 48H93M48 3V93','none','#1D2625',1.4)),'套准线','图版边缘定位与打印检查。',True)
    make('icons','expand.svg',svg(32,32,path('M4 13V4H13M19 4H28V13M28 19V28H19M13 28H4V19','none','#263735',2)),'放大边角','素材浏览与放大。',True)
    t=ROOT/'SHARED/textures/neutral-weave.webp';t.parent.mkdir(exist_ok=True);N=256;y,x=np.mgrid[:N,:N];v=(209+7*np.cos(x*np.pi/4)+5*np.cos(y*np.pi/4)+2*np.sin((x+y)*np.pi/8)).astype('uint8');Image.fromarray(np.stack((v,v-2,v-7),axis=2)).save(t,lossless=True)
    shared.append(dict(file='textures/neutral-weave.webp',asset_name='中性细织布',intended_usage='无色系表面底层，256px 周期。',transparency=False,tiling=True));dump(ROOT/'SHARED/asset-meta.json',[dict(r,origin='original') for r in shared])
if __name__=='__main__':run()
