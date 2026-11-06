# ARTISAN V2 / 通用艺术设计材质库

**作者与维护者：[hanhanhu847-star](https://github.com/hanhanhu847-star)** · Codex 辅助制作

代码采用 **MIT**；自制艺术素材采用 **CC BY 4.0**，使用时保留作者署名。摄影和数据星图保留原许可。详见 [作者与署名](AUTHORS.md) 和 [许可范围](LICENSE-ASSETS.md)。

**[在线预览与挑选素材](https://hanhanhu847-star.github.io/artisan-v2/)** · [下载完整素材包与PDF图鉴](https://github.com/hanhanhu847-star/artisan-v2/releases/latest)。Git仓库包含实际素材和离线浏览器；PDF作为Release附件提供，完整包中也附带PDF。GitHub自动生成的“Source code”压缩包不含PDF。

完整解压后打开 [离线浏览器](BROWSER/index.html)。源素材位于 STYLES 与 SHARED；浏览器、联系表与 PDF 用于选图。日常浏览无需联网、安装依赖或注册账号。

16 套风格，1,804 个按家族统计的独立作品，另有 4 个共享辅助素材；合计 3,824 个原素材文件。V1 的 2,084 个源素材保留，V2 增加 1,740 个文件。尺寸、格式、配色和状态版本不重复计入作品。

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

详情可缩放、换背景、复制相对路径或打开原件另存。在线版为大于 4 MB 的位图提供同构图轻量预览，原文件通过“打开原件”获取；离线版直接显示原件。在线版还能复制素材网址，所在目录链接打开 GitHub 文件夹。

所选清单、筛选结果与整套清单导出为 JSON；在线清单另附 download_url、preview_url 和 license_url，便于下载原件并保留许可。清单不会自动打包素材。离线使用时把 file_path 对应文件及有关许可复制进目标项目即可。

## 来源边界
自制图形与程序化纹理按 CC-BY-4.0 提供。16 幅 Poly Haven 官方全景摄影及其取景版本采用 CC0；原 JPG 为 LDR 环境照片。12 幅星座图版及所用星表、连线子集采用 CC BY-SA 4.0，带作者、固定版本和修改说明。只看缩略图不能推断许可，复制前以每项索引为准。

敦煌图形是现代再创作，不是特定洞窟或朝代的临摹；矿物色是屏幕参考色。地图为虚构，蓝图不是可加工图纸，博物学插画不提供物种鉴定。V2 天文真实数据图版与其他艺术点位明确分开。

## 维护

在线站点由 gh-pages 分支发布，main 保留完整素材和代码。Pages 提供浏览器与索引，预览图和原件从公开仓库的固定提交版本读取。用 `python TOOLS/build_pages.py` 生成轻量站点，大图预览用 `python TOOLS/web_previews.py` 重建。发布与验收步骤见 [Pages 维护说明](TOOLS/PAGES.md)。

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
