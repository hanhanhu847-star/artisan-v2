"""以真实索引生成 V2 指南；计数由台账推导，科学/历史边界按实际来源记录。"""
from styles_data import *
from v2_registry import inventories,SERIES
from collections import Counter
import csv
NAMES={'backgrounds':'高清背景','textures':'纹理','ornaments':'装饰','icons':'图标','illustrations':'插画','ui':'UI 组件组'}
def mdtable(rows):
 return '\n'.join('| '+' | '.join(map(str,row))+' |'for row in rows)
def run():
 idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'));inv=inventories();assets=idx['assets']
 styles={s['id']:s for s in idx['styles']};newfiles=sum(a['revision']=='V2'for a in assets)
 head=f"{len(STYLES)} 套风格，{idx['work_count']:,} 个按家族统计的独立作品，另有 4 个共享辅助素材；合计 {idx['file_count']:,} 个原素材文件。V1 的 2,084 个源素材保留，V2 增加 {newfiles:,} 个文件。尺寸、格式、配色和状态版本不重复计入作品。"
 readme='''# ARTISAN V2 / 通用艺术设计材质库

**作者与维护者：[hanhanhu847-star](https://github.com/hanhanhu847-star)** · Codex 辅助制作

代码采用 **MIT**；自制艺术素材采用 **CC BY 4.0**，使用时保留作者署名。摄影和数据星图保留原许可。详见 [作者与署名](AUTHORS.md) 和 [许可范围](LICENSE-ASSETS.md)。

[下载完整素材包与PDF图鉴](https://github.com/hanhanhu847-star/artisan-v2/releases/latest)。Git仓库包含实际素材和离线浏览器；PDF作为Release附件提供，完整包中也附带PDF。GitHub自动生成的“Source code”压缩包不含PDF。

完整解压后打开 [离线浏览器](BROWSER/index.html)。源素材位于 STYLES 与 SHARED；浏览器、联系表与 PDF 用于选图。日常浏览无需联网、安装依赖或注册账号。

'''+head+'''

每套含 11 个独立背景、16 个纹理、28 个装饰、32 个图标、15 组 UI。通常有 10 个插画；古典天文另加 12 幅基于公开星表的星座图版，共 22 个插画。完整分项、升级口径、检查状态见 [扩容统计](AUDIT/EXPANSION_REPORT.md)，不能只以文件总数判断质量验收。

## 入口
- [逐套完整联系表](PREVIEWS/CONTACT_SHEETS.html)：呈现实际素材，保留版本另列。
- [完整预览图鉴](https://github.com/hanhanhu847-star/artisan-v2/releases/latest/download/ARTISAN_V2_Atlas.pdf)：风格说明、系列、来源与全部联系表。
- [使用指南](ASSET_USAGE_GUIDE.md)：尺寸、透明、应用接入及使用条件。
- [ASSET_INDEX.json](ASSET_INDEX.json)：每项的家族、版本、用途、实际像素、SHA-256、作者与许可。
- [来源许可总表](LICENSES/asset-sources-v2.json)：逐文件记录；许可概览见 LICENSES/README.md。
- [Codex 接入提示词](CODEX/MASTER_PROMPT.md)：供其他应用按需取用素材。
- ADAPTERS：保留 Web、React、Vue、Python、Qt 示例及颜色映射。

## 浏览和提取
默认“每个作品一个版本”展示当前代表作。“全部文件”还能查看 V1 原件及其他尺寸、格式和状态。按子系列、分辨率、透明、许可与格式筛选；JPG 筛选可选到同一矢量背景的原生栅格版本。收藏以作品家族保存于本机浏览器，不会上传或跨设备同步。

详情使用实际原件，可缩放、换背景、复制相对路径或打开原件另存。所选清单、筛选结果与整套清单导出为 JSON；清单不会自动复制素材。把 file_path 对应文件及有关许可复制进目标项目即可。

## 来源边界
自制图形与程序化纹理按 CC-BY-4.0 提供。16 幅 Poly Haven 官方全景摄影及其取景版本采用 CC0；原 JPG 为 LDR 环境照片。12 幅星座图版及所用星表、连线子集采用 CC BY-SA 4.0，带作者、固定版本和修改说明。只看缩略图不能推断许可，复制前以每项索引为准。

敦煌图形是现代再创作，不是特定洞窟或朝代的临摹；矿物色是屏幕参考色。地图为虚构，蓝图不是可加工图纸，博物学插画不提供物种鉴定。V2 天文真实数据图版与其他艺术点位明确分开。

## 维护

从Git仓库克隆后，用 `python TOOLS/integrity_check.py --source-only` 校验源码及素材；完整Release包使用不带参数的校验命令。
浏览不需生成器。重建需要 Python 3.10+、Pillow、NumPy；PDF 需 reportlab；Node 的 sharp 用于实际解码，playwright 和本机 Chromium 用于离线验收。中文字体使用本机字体，不随包分发。

V2 新素材元数据在 STYLES/<id>/v2-records/*.json，V1 的 asset-meta.json 与原件保留。新增文件先声明 family、credit、series、role、用途与许可；重制同一作品使用 upgrade 和既有 family，格式版本使用 variant。单纯增加 preview、尺寸、状态不增加家族数。外部来源必须逐项提供 source、author、license、license_file、attribution、modification_status。

常用更新顺序：
    
    node TOOLS/v2_proofs.cjs
    python TOOLS/v2_index.py
    python TOOLS/v2_audit.py
    python TOOLS/v2_contacts.py
    python TOOLS/v2_contact_gallery.py
    python TOOLS/v2_similarity_sheets.py
    node TOOLS/v2_browser_check.cjs

视觉复核、来源、图鉴与报告都完成后，再刷新 FILES_SHA256.json 并运行 package_library.py 和 integrity_check.py。见 TOOLS/V2_MAINTENANCE.md。旧 V1 生成器仅保留用于追溯，不应用来覆盖当前素材。
'''
 write(ROOT/'README.md',readme)
 write(ROOT/'START_HERE.txt','''ARTISAN V2 | 作者 hanhanhu847-star | 开始使用
1. 完整解压 ZIP，保留 ARTISAN_V2 内目录关系。
2. 打开 BROWSER/index.html，选风格、类别、系列、尺寸或许可。
3. 默认每个作品一个版本；切换“全部文件”可查保留版本。
4. 点素材查看实际原件与来源；复制相对路径或打开原件另存。
5. 勾选素材后导出清单。JSON 是清单，交付时还要复制相应原文件。
6. 全部预览：PREVIEWS/CONTACT_SHEETS.html 与 PREVIEWS/ARTISAN_V2_Atlas.pdf。
7. 应用接入：ASSET_USAGE_GUIDE.md；交给 Codex：CODEX/MASTER_PROMPT.md。
8. 实际验收和数量口径：AUDIT/EXPANSION_REPORT.md。字体、交互与布局需在宿主应用内验证。
''')
 guide='''# ARTISAN V2 素材使用指南

## 先选原件和构图
SVG 的 width/height 是固有画板，可按比例重绘；JPG/PNG/WebP 的尺寸是真实像素。背景 v2-plate-01 至 03 为 3840×2160，04 至 05 为 2160×3840，06 至 07 为 3000×3000，08 至 09 为 5120×1440，均有可编辑 SVG 与从矢量直接渲染的 JPG。V1 的 field-study-3840.jpg 提供另一幅 4K 横版，16 套各有一个 CC0 摄影来源。横竖方超宽是分别设计的图版，不能把全景照片上下拉伸填满竖屏。

程序化纹理优先选 v2- 开头的 2048 文件：每套 12 个连续平铺 WebP 和 4 个透明 PNG 叠层。V1 的 384px 纹理保留供兼容，不占 2K 指标。按纹理周期平铺，在实际显示密度下看接缝；透明叠层以低透明度组合，不能拿预览棋盘当素材。照片和普通背景不能因无透明区域就认定为可平铺。

## 图标、装饰与 UI
V2 图标使用 64 单位画板，每套 24 个常用语义和 8 个风格专属符号。SVG 适合应用资源；需要位图时从原 SVG 按实际设备密度栅格化。16 套的形态和笔画不同，同一页面宜选同一套。装饰有独立 SVG，透明 PNG 与 SVG 版本属于同一作品。

UI 目录为可编辑视觉样例：按钮、卡片、列表、页眉导航、侧栏、标签、提示、空结果、输入框、表格、进度、弹窗、错误、加载和工具栏。V1 的五态保留；V2 重排不意味着旧状态已经同步重绘。生产组件应使用新视觉构建自己的 normal、hover、focus、selected、disabled、error 状态，并在宿主实现操作、键盘路径、读屏名称与真实数据，不能直接把图片当完整交互控件。

## 许可和事实边界
索引的 license、license_file、source、author、attribution、modification_status 一起保留。CC-BY-4.0 自制图形须署名 hanhanhu847-star、保留项目与许可链接，并说明修改；CC0 摄影不强制署名，但包内仍记录实际作者。CC BY-SA 4.0 的十二星座图版及数据使用、改编时应保留署名、来源、许可链接与修改说明，并遵守其共享条件；具体条文见随包许可文本。

只有 illustrations/v2-zodiac-*.svg 使用 HYG 星表和 Stellarium modern 连线数据。其他星点、轨道、星云与银河为艺术示意；太阳系不按距离或半径比例，月相为几何示意。敦煌系列为现代再创作，不虚构洞窟出处或文物身份。古地图和蓝图不承担导航或制造用途，原创博物插画不作分类鉴定。

## 调用流程
1. 从 ASSET_INDEX.json 的 assets 按 style_id、category、series 与用途筛选。asset_id 标识文件版本，family_id 标识作品；counted=true 是当前计数代表，并不表示同家族其他文件不可使用。
2. 将选中的 file_path 原件、相关许可及该项索引复制到项目的独立资源目录。修改图形后建立新路径和修改记录。
3. Web 先接入语义色，加载 ADAPTERS/web/components.css 和 themes.css，使用 data-artisan 作用域。可离线运行 ADAPTERS/web/index.html。React/Vue/Python/Qt 的既有示例保留；各框架的实际运行状态以验收记录为准。
4. Qt 使用 QSS 与原生控件；iOS/Android 以 ADAPTERS/colors.json 映射语义色，按平台能力转换 SVG。字体依赖本机回退；交付前核对中文、数字、换行和长标题，必要时在设计软件中转曲。
5. 背景文字优先放在留白处，长文和数据表使用平整底色；纹理叠层先试 5% 至 15% 透明度。正文、控件和状态须在目标应用按实际字号测对比度。
6. 动效建议：按压约 120ms、状态约 200ms、面板进入约 280ms；这些为应用建议。系统减少动态时显示静帧，触屏不依赖悬停。生成式背景 v2-plate-09.svg 带可关闭的 SVG 动画，JPG 是同作品静态版本。

## 输出与移动端
PPT/Word 可用高清 JPG、透明 PNG 或兼容的 SVG；保留可编辑母版。所有屏幕配色为 RGB，印刷需按实际 ICC 和纸材打样。SVG 不等于 CMYK 完稿。

浏览器通过本地 file:// 打开，收藏保存于当前浏览器存储；复制整个文件夹到另一位置后收藏可能不继承。手机文件管理器可能限制加载本地脚本，遇到这种情况可看 PDF 或在桌面浏览。清单导出是 JSON，不会替用户打包所选图片。
'''
 write(ROOT/'ASSET_USAGE_GUIDE.md',guide)
 write(ROOT/'LICENSES/README.md','''# 来源与许可

完整逐文件表为 asset-sources-v2.json（含文件 SHA-256），来源也直接显示在离线浏览器详情。

| 内容 | 数量口径 | 许可与记录 |
|---|---|---|
| 自制 SVG、程序化纹理与设计文档 | 按索引逐文件识别 | CC-BY-4.0；CC-BY-4.0.txt |
| 自有程序代码 | BROWSER / TOOLS / ADAPTERS | MIT；根目录 LICENSE |
| Poly Haven 环境摄影 | 16 个官方原件，另有 16 个取景派生 | CC0-1.0；photo-sources.json、ATTRIBUTION.md、CC0 文本 |
| 十二星座图版和所用数据子集 | 12 幅 SVG；HYG/连线数据为制作依据 | CC BY-SA 4.0；celestial-data/ATTRIBUTION.md、许可原文和固定版本来源 |

第三方素材按逐项记录的许可分发。字体未打包。

星表图版与数据具有单独许可，不得以本工程自制许可覆盖其来源义务。说明中的博物馆/档案参考链接用于背景阅读，不表示复制了网站图像、文字或获得其商标授权。敦煌系列没有特定洞窟原图摹本。

首次集成时保留对应的许可文件；改编图版时同时记录修改。包内许可原文优先于本概览的简写。
''')
 # Update permission scope to include third-party data adaptations explicitly.
 p=ROOT/'LICENSES/CC-BY-4.0.txt';s=p.read_text(encoding='utf8')
 s=s.replace('不适用于明确标记第三方来源的摄影文件','不适用于明确标记第三方来源的摄影、星表、连线数据及其 CC BY-SA 图版')
 write(p,s)
 for S in STYLES:
  z=S['id'];ss=styles[z];rs=[a for a in assets if a['style_id']==z];reps=[a for a in rs if a['counted']]
  d=inv[z];lines=[f"# {S['zh']} / {S['en']} / V2",'','## 本包的视觉语言',S['form']+' '+S['layout'],S['material'],'',
   f"本套 {ss['count']} 个源素材文件，按家族计 {ss['work_count']} 个独立作品。V1 的130个源文件保留，新增文件含升级、原创和格式版本；数字不将不同尺寸或五态拆算为作品。",'',
   '## 配色与排版','| 用途 | 色号 |','|---|---|']
  for label,col in zip(['基底','正文/轮廓','主强调','次强调','点色'],S['palette']):lines.append(f'| {label} | {col} |')
  lines+=['',S['font']+' 字体使用本机回退，不随包分发。','常规间距可用4/8/16/24/40；小屏转单栏，图形不挤压长文字。文字对比度按实际使用尺寸核对。','',
    '## 数量与系列','| 类别 | 独立作品/组 |','|---|---:|']
  lines += [f"| {NAMES[k]} | {v} |"for k,v in ss['counts_by_category'].items()]
  for series in SERIES[z]:
   q=[a for a in reps if a['series']==series]
   # Show actual names across categories instead of invented coverage.
   examples=[];seen=set()
   for cat in ['backgrounds','illustrations','textures','ornaments','icons','ui']:
    candidate=next((a for a in q if a['category']==cat),None)
    if candidate:examples.append(candidate['asset_name']);seen.add(candidate['asset_id'])
   lines+=['',f"### {series} / {len(q)} 个家族",'；'.join(examples)+'。']
  lines+=['','## 原件与应用',
   '背景 v2-plate-01 至09各自为独立构图；JPG与SVG为同家族。01至03横版3840×2160，04至05竖版2160×3840，06至07方版3000×3000，08至09超宽5120×1440。加上V1的4K母版和摄影，共11幅背景。',
   '纹理使用12个原生2048连续平铺WebP和4个透明PNG叠层。旧384px版本保留。装饰选单独SVG，图标以64单位画板绘制，可按设备像素密度导出。',
   'UI共15组：14类基础组件V2视觉重排和1组工具栏。旧五态与新默认图形并非自动配套；宿主应用应同步实现焦点、错误、禁用、选中和点击区。',
   S['ui']+' 按压120ms、状态200ms、面板280ms可作起点；减少动态时直接显示终态。','',
   '## 使用判断','适用：'+S['use']+'。','避免：'+S['avoid'],'搭配：'+S['combine'],'',
   '## 内容边界与来源']
  if z=='celestial-atlas':
   lines+=['illustrations/v2-zodiac-*.svg 共12幅，采用HYG v4.0恒星位置/星等和Stellarium modern连线，以切平面投影绘制，北上东左。使用数据、不使用Stellarium插画。作者、固定版本与修改说明见 ../../LICENSES/celestial-data/ATTRIBUTION.md，图版及数据子集按CC BY-SA 4.0。',
    '其他星点和深空构图为艺术示意，不能当观测星历。太阳系不按距离或半径比例；月相使用几何明暗轮廓；星图未绘制官方天区边界。真实数据与艺术构成在索引的role、license和用途字段中区分。']
  elif z=='dunhuang':
   lines+=['藻井、莲瓣、飞天、供养人和楼阁在本包均为原创现代构成；不声明复原某窟、某朝代或某幅经变画。壁画粉化和矿物颗粒为程序拟作；石青、石绿、朱砂色只作RGB色感参考，不代表矿物成分或文物取样。',
    '史料阅读：[Getty敦煌石窟展览](https://www.getty.edu/research/exhibitions_events/exhibitions/cave_temples_dunhuang/)与[莫高窟壁画保护项目](https://www.getty.edu/projects/wall-paintings-conservation-mogao-grottoes/)。参考用于区分历史对象与本包再创作，未复制网页中的文物图像。']
  elif z=='generative-art':
   lines+=['Voronoi、L-System、细胞自动机与流场图版由TOOLS/v2_scenes.py、v2_backgrounds.py和v2_bg_technical.py中的规则生成；纹理由v2_materials.py生成。脚本保留确定性种子。动态v2-plate-09.svg有减少动态分支，JPG静帧与SVG同家族。']
  else:lines+=['本套非摄影图形为原创/程序化当代构成，不能据此推断真实馆藏、地理位置、物种鉴定、加工尺寸或历史出处。']
  photo=next(a for a in rs if a['license']=='CC0-1.0')
  lines+=['',f"摄影来源：[{photo['asset_name']}]({photo['source']})；作者：{photo['author']}；CC0-1.0。其他文件以逐项索引为准。",'',
    '完整缩略图见 ../../PREVIEWS/CONTACT_SHEETS.html；实际文件路径与许可见 ../../ASSET_INDEX.json。']
  write(ROOT/f'STYLES/{z}/STYLE_GUIDE.md','\n'.join(lines)+'\n')
  prompt=f'''使用 ARTISAN V2 的 {S['zh']}（{z}）为指定应用页面制作可运行实现。
先读本目录 STYLE_GUIDE.md、tokens.json 与总索引；只选实际存在的 file_path。以 family_id 区分作品，避免误把尺寸/状态当新增。
图形：{S['form']}
排版：{S['layout']}
适用：{S['use']}。注意：{S['avoid']}
按需复制原件和逐项许可，保存使用清单。新 UI 默认视觉需要在宿主实现完整状态与交互，不能拿静态 SVG 替代语义控件。
在宿主检查字号、中文、长标题、窄屏、键盘与减少动态；报告实际运行结果。
'''
  write(ROOT/f'STYLES/{z}/STYLE_PROMPT.md',prompt);write(ROOT/f'CODEX/STYLE_PROMPTS/{z}.md',prompt)
 master='''# ARTISAN V2 项目接入指令
先读目标工程约定、最新文件和既有主题，再读库内 README.md、ASSET_USAGE_GUIDE.md、指定风格 STYLE_GUIDE.md 与 ASSET_INDEX.json。
按任务选择实际原件，不把 PREVIEWS 缩略图接入成高清资源。以 asset_id 选择版本，以 family_id 识别同一作品。筛选维度为 style_id、category、series、file_format、尺寸、transparency、tiling和license。
只复制本项目所需子集，并记录源ID、相对路径、目标路径、SHA-256、用途、作者、许可、署名与修改。带入实际许可文件，CC BY-SA星图不得套用自制许可。
先完成一个代表性页面。语义色映射到目标工程变量，限定样式作用域；长文与表格保留平整底色。UI SVG是设计样例，宿主应使用真实控件实现键盘、点击、焦点、错误、禁用、加载与保存。
V1状态图保留供参考，V2视觉默认样例须在项目中完善对应状态；不得宣称SVG本身具有业务功能。字体、平台SVG支持、移动端、深浅底、缺图和减少动态都按实际环境验证。
明确区分真实数据星图和其他艺术化星点；敦煌现代构成不能写成特定洞窟摹本。地图/工程图/博物学素材的事实边界沿用原指南。
保留可回退版本，执行目标工程要求的检查；交付实际入口、使用资源清单和真实验证范围。
'''
 write(ROOT/'CODEX/MASTER_PROMPT.md',master)
 write(ROOT/'CODEX/CODEX_QUICK_START.txt','''将 ARTISAN_V2 解压目录和目标工程目录提供给 Codex：
“请根据 CODEX/MASTER_PROMPT.md，用【风格】完成【页面/功能】。读取真实索引，只复制所需素材和许可，在【目标工程】接入并实际运行检查。”
浏览器可勾选并导出 JSON 清单；清单不是素材包，仍须复制其中 file_path 指向的原件。
每项资产含 asset_id 和 family_id。前者是文件版本，后者是独立作品；不要把旧文件、尺寸、格式和状态另计为原创数量。
''')
 write(ROOT/'CODEX/QUICK_START.txt',(ROOT/'CODEX/CODEX_QUICK_START.txt').read_text(encoding='utf8'))
 write(ROOT/'TOOLS/V2_MAINTENANCE.md','''# V2 重建与验收入口
原件已生成，日常浏览无需重建。编辑生成器前备份；以下脚本会覆盖 V2 自制同名文件，不用于改动 V1。
素材生成顺序：v2_materials.py；v2_common_icons.py；v2_borders.py；v2_corner_badges.py；v2_sky.py（不带--acquire即可使用随包子集）；v2_objects.py；v2_scenes.py；v2_backgrounds.py；v2_raster.cjs；v2_ui_revision.py；v2_ui_completion.py；v2_ornament_revision.py。
其中最后两个补绘脚本必须在v2_borders.py之后，避免旧版外框或工具栏覆盖重绘。v2_ornament_revision.py不修改原V1饰件，而以同家族V2文件接替。
随后运行v2_proofs.cjs、v2_index.py、v2_tiles_check.py、v2_svg_tiles.cjs、v2_audit.py、v2_contacts.py、v2_contact_gallery.py、v2_similarity_sheets.py。查看实际联系表和相似候选，未观察不得改写成通过。
v2_guides.py生成说明；v2_atlas.py生成PDF（运行前确保PDF作者工具与本机字体已就绪）。
运行v2_browser_check.cjs验证断网本地浏览；测试可用ARTISAN_TEST_ROOT指向完整解压目录。
v2_pdf_check.py验证当前图鉴。实际完成视觉审查后保存对应记录；v2_release_gate.py核对这些记录与当前源文件的SHA，v2_report.py输出报告。修改原件后必须重做受影响检查，不能沿用过期视觉记录。
最终写FILES_SHA256.json，package_library.py生成上一层ARTISAN_V2_Expanded_Asset_Library.zip；integrity_check.py同时验证文件集合、每项SHA和ZIP CRC。把ZIP解压到新的中文目录后再次验证真实浏览。
v2_verify_delivery.py将最终包解压到包旁的新中文目录，重复逐文件SHA与真实断网浏览，在包旁生成ARTISAN_V2_RELEASE_VERIFICATION.json。用ARTISAN_NODE指定Node，NODE_PATH提供playwright；测试输出写包外，保持压缩包内文件不变。
旧V1生成器保留用于追溯。generate_index.py在V2目录下自动转入v2_index.py，旧make_atlas.py等不能替代V2验收。
''')
 # Human-readable complete source table, preserving actual source fields.
 with (ROOT/'LICENSES/asset-sources-v2.csv').open('w',encoding='utf-8-sig',newline='')as f:
  fields=['asset_id','file_path','sha256','source','author','license','license_file','attribution','modification_status'];cw=csv.DictWriter(f,fields);cw.writeheader();cw.writerows({k:a[k]for k in fields}for a in assets)
 print('16 guides, prompts, V2 entry docs and complete source CSV written')
if __name__=='__main__':run()
