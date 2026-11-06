# V2 重建与验收入口
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
