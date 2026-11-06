# 接入实例
只浏览或复制素材，直接打开 ../BROWSER/index.html。下列内容面向希望编程调用的项目。

| 目标 | 最小入口 | 环境 |
|---|---|---|
| 原生 HTML / CSS | web/index.html | 本地浏览器，无需服务器 |
| React / Next.js | react/ArtisanCard.mjs | 宿主已有 React；Next.js 交互边界使用客户端组件 |
| Vue | vue/ArtisanCard.mjs | Vue 3；组件使用 h()，不用模板编译器 |
| Python 查找与过滤 | python/assets.py | Python 3.10+，只用标准库 |
| PySide6 / QSS | pyside6/example.py | 宿主已安装 PySide6 |
| PyQt6 / QSS | pyqt/example.py | 宿主已安装 PyQt6 |
| 设计与出版 | design-tools/IMPORT.md | 支持相应图片格式的软件 |

Web 组件先加载 web/components.css，再加载 web/themes.css。容器以 data-artisan 绑定风格；ui-spec.json 记录 14 个组件的语义、状态图路径和接入方式。colors.json 汇集各套语义色。tokens 中的默认过渡时间是建议，宿主应遵守系统减少动态偏好。

React 示例（将静态目录映射到 /artisan/；asset 是 ASSET_INDEX.json 的一条记录）：

    import {ArtisanCard} from './ArtisanCard.mjs';
    <ArtisanCard asset={asset} assetRoot="/artisan/" onSave={(id, saved) => update(id, saved)} />

Vue 3 示例：

    <script setup>
    import ArtisanCard from './ArtisanCard.mjs';
    defineProps({ asset: Object });
    </script>
    <template><ArtisanCard :asset="asset" asset-root="/artisan/" @save="(id, saved) => console.log(id, saved)" /></template>

示例以 preview_path 显示缩略图。只复制部分资源时请同步复制该预览文件，或改为 file_path 加载原件。选择摄影全景原件时先考虑内存和加载时间。资产链接是库根目录相对路径，不能直接从宿主页面的当前 URL 猜测路径。
