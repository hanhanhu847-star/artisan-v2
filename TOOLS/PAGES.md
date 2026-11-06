# GitHub Pages 发布与验收

在线入口：https://hanhanhu847-star.github.io/artisan-v2/

仓库 Settings → Pages → Deploy from a branch → `gh-pages` / `/ (root)`。根目录 `.nojekyll` 使资源按静态文件发布，不经过 Jekyll；index.html 保留查询参数和页面片段并跳转到浏览器。该站点无服务器、登录或外部运行时依赖。

main 保存完整素材与代码；gh-pages 只保存浏览器、索引和入口文件。首次直接发布完整目录时，服务端在同步文件阶段超时，因此采用轻量发布。站点从 raw.githubusercontent.com 读取固定提交版本的预览和原件，URL 中使用完整提交 SHA，避免索引和文件版本错配。完整 ZIP 和 PDF 从 Release 下载。新提交不会修改已有版本的 Release 附件。

更新时先把源文件变更提交、推送到 main，再用 `python TOOLS/build_pages.py <站点目录> --revision <已推送的完整提交SHA>` 生成站点，将该目录的内容提交并推送到 gh-pages。该分支更新后 GitHub 自动部署。输出目录必须位于源库外；脚本只生成文件，不执行删除或 Git 操作。deployment.json 记录素材版本。离线包不需要 deployment-config.js，仍直接读取本地素材。

在线版与离线版共用索引。在线模式下，大于 4 MB 的 JPG、PNG、WebP 使用最长边 1600 像素的预览；原件不变，详情显示其大小并提供原文件链接。预览继承相应源文件的来源和许可，不计为新增作品。源文件变动后运行 `python TOOLS/web_previews.py`。

在线导出 JSON 在既有字段之外增加 base_url，以及各项的 download_url、preview_url、license_url。复制素材链接得到原件地址；“所在目录”链接打开 GitHub。离线模式不增加网络请求，继续使用原来的相对路径。

维护检查：

1. 使用本机 Chromium 和 Playwright 运行 `node TOOLS/pages_check.cjs`。默认会启动临时本地 HTTP 服务，在 `/artisan-v2/` 项目子路径下检查。设置 `ARTISAN_PAGES_ROOT` 可改为检查生成的轻量站点。报告默认输出到系统临时目录，也可设置 `ARTISAN_PAGES_QA`。
2. 部署后设置 `ARTISAN_PAGES_URL=https://hanhanhu847-star.github.io/artisan-v2/` 再运行同一脚本，验证实际线上站点。必要时通过 `ARTISAN_TEST_PROXY` 指定已有 HTTP 代理。
3. 运行既有 `node TOOLS/v2_browser_check.cjs` 验证断网 file:// 使用；用 `ARTISAN_TEST_QA` 和 `ARTISAN_TEST_REPORT` 把报告放在仓库外。
4. 代码和资源变更完成后运行 `python TOOLS/integrity_check.py --write`，再运行 `python TOOLS/integrity_check.py --source-only`。不要将临时测试报告放入源文件目录。
5. 提交、推送并等待 Pages 构建成功；验证公开网址后再宣布发布完成。可用 GitHub CLI 的 `gh api repos/hanhanhu847-star/artisan-v2/pages/builds/latest` 查看构建状态。

Pages 有站点体积与流量限制，后续扩充前应重新核对 [GitHub 官方限制](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)。
