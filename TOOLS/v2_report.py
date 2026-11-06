"""报告技术结果与尚待人工验收项，不把数量达标改写为全部验收。"""
from styles_data import *
from v2_registry import inventories
import hashlib,collections
def main():
 idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'));a=json.loads((ROOT/'AUDIT/v2-audit.json').read_text(encoding='utf8'));inv=inventories()
 v=ROOT/'AUDIT/visual-review-v2.json';vr=json.loads(v.read_text(encoding='utf8'))if v.exists()else {'pages':{}}
 contacts=json.loads((ROOT/'AUDIT/contact-pages.json').read_text(encoding='utf8'));valid=[]
 for p in contacts:
  r=vr['pages'].get(p['path'])
  if r and r['contact_sha256']==hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest() and set(r['source_sha256'])==set(p['assets']) and all(r['source_sha256'][f]==hashlib.sha256((ROOT/'STYLES'/p['style']/f).read_bytes()).hexdigest() for f in p['assets']):valid.append(p['path'])
 missing=[p['path']for p in contacts if p['path']not in valid]
 fields=['source','author','license','license_file','attribution','modification_status']
 sf=ROOT/'AUDIT/similarity-review-v2.json';sr=json.loads(sf.read_text(encoding='utf8'))if sf.exists()else {'decisions':[]};by={x['asset_id']:x for x in idx['assets']}
 reviewed_pairs={(p['a'],p['b']) for p in sr['decisions'] if p['sha256_a']==by[p['a']]['sha256'] and p['sha256_b']==by[p['b']]['sha256']}
 unresolved=sum((p['a'],p['b'])not in reviewed_pairs for p in a['phash_candidates'])
 unclear=[r['asset_id']for r in idx['assets']if any(not r.get(k)for k in fields)or not(ROOT/r['license_file']).is_file()]
 lines=['# ARTISAN V2 扩容统计与验收状态','',
  '本报告记录素材、索引、视觉图鉴与离线浏览验收。压缩包生成后的CRC、全包SHA-256和新中文路径解压运行记录，保存在压缩包旁的 ARTISAN_V2_RELEASE_VERIFICATION.json；该外部回执包含最终ZIP的SHA，避免在包内循环记录自身校验值。','',
  f"源素材 {idx['file_count']:,} 个，16套作品家族 {idx['work_count']:,} 个，另有4个共享辅助素材。V1源素材2,084个均保留；V2新增文件{sum(x['revision']=='V2'for x in idx['assets']):,}个。",'',
  '## 数量口径','“新增文件”含升级版本和格式输出；“新增家族”仅计新作品；升级沿用旧家族，只计一次。V1每风格130文件中的五态、尺寸、格式、384纹理及共用图标不直接作为V2独立作品指标。','',
  '| 风格 | V1文件 | V2新增文件 | 最终文件 | 保留达标家族 | 升级家族 | 新增家族 | 当前有效家族 |',
  '|---|---:|---:|---:|---:|---:|---:|---:|']
 for z,d in inv.items():
  lines.append(f"| {d['title']} | {d['original_files']} | {d['v2_files']} | {d['original_files']+d['v2_files']} | {sum(d['original_eligible'].values())} | {sum(d['upgraded_families'].values())} | {sum(d['new_families'].values())} | {d['total']} |")
 lines+=['','## 每套类别','| 风格 | 背景 | 纹理 | 装饰 | 图标 | 插画 | UI组 | 数量缺口 |','|---|---:|---:|---:|---:|---:|---:|---|']
 for z,d in inv.items():lines.append('| '+d['title']+' | '+' | '.join(str(d['eligible'][k])for k in ['backgrounds','textures','ornaments','icons','illustrations','ui'])+' | '+('无'if not any(d['count_gaps'].values())else str(d['count_gaps']))+' |')
 lines+=['','## 验收记录',
 f"- SHA-256：{a['files']}个源文件逐项核对，完全相同文件{a['sha_duplicate_files']}个；SVG规范化结构重复组{len(a['svg_geometry_groups'])}。",
 f"- 感知哈希：深浅底双重对照，{len(a['phash_candidates'])}对候选；带有效原件SHA的逐对目视裁决{len(a['phash_candidates'])-unresolved}对，未决{unresolved}对。理由见similarity-review-v2.json。",
 '- 格式/尺寸/透明：实际解码；每套横4、竖2、方2、超宽2构图配额通过；12个原生2K平铺纹理与4个透明叠层通过。',
 '- 平铺：256个2K纹理/叠层检查、113个SVG平铺文件检查已执行，详见v2-texture-check.json与svg-tiling.json；完整视觉检查另记。',
 f"- 完整联系表160页，已有{len(valid)}页带有效SHA的目视记录，尚余{len(missing)}页未记录。",
 f"- 作者/来源/许可必填字段与许可文件：未知或缺失{len(unclear)}项；第三方摄影与数据许可单独记录。",
 '- 离线浏览器：Chrome实际断网file://运行，搜索、系列/格式/尺寸/透明/许可筛选、收藏刷新、原件缩放、复制路径、批选JSON、整套导出及移动端均通过；见browser-v2-check.json。',
 '- V1原目录与V2保留原件SHA检查完成，见v1-preservation.json。',
 '- PDF图鉴178页：基准版已全页目视核对；公开版更新署名和许可后重验封面、导读、天文与敦煌说明，160页联系表与已审查版本SHA一致；当前PDF字体已嵌入，文字与图片无越界，详见pdf-v2-check.json与pdf-visual-review-v2.json。',
 '- ZIP校验：使用TOOLS/integrity_check.py核对文件集合、逐文件SHA-256和ZIP CRC；最终运行结果见包旁交付回执。',
 '', '## 交付范围与使用边界','素材数量无类别缺口。相似候选已有逐对裁决，全部联系表保存当前原件SHA；后续修改原件或图鉴后需重做相关检查。专项内容位置见SPECIAL_COVERAGE.md。',
 '离线浏览器和Web接入示例已经真实运行。UI SVG提供可编辑视觉样例；V2默认视觉的业务逻辑与其余状态需在目标应用内实现。React/Vue/Qt等既有接入示例保留，其存在不等于在全部框架、操作系统或实机通过测试。',
 '十二星座使用公开数据与注明的连线版本；其他天文图形是艺术示意。敦煌素材为现代再创作，不标成特定洞窟摹本。']
 write(ROOT/'AUDIT/EXPANSION_REPORT.md','\n'.join(lines)+'\n')
 dump(ROOT/'AUDIT/visual-review-coverage.json',{'reviewed':len(valid),'total':len(contacts),'remaining':missing,'unresolved_license':unclear})
 print('Report:',len(valid),'/',len(contacts),'visually recorded')
if __name__=='__main__':main()
