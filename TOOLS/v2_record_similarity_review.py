"""2026-11-06 目视裁决的候选记录。重新生成素材后须重新审阅，不能照搬旧结论。"""
import json,hashlib,datetime
from styles_data import ROOT,dump
def make():
 a=json.loads((ROOT/'AUDIT/v2-audit.json').read_text(encoding='utf8'));idx=json.loads((ROOT/'ASSET_INDEX.json').read_text(encoding='utf8'));by={r['asset_id']:r for r in idx['assets']}
 groups=json.loads((ROOT/'AUDIT/similarity-groups.json').read_text(encoding='utf8'))
 notes={
 1:'同套上传与下载；箭头方向传递相反操作，是必要的不同语义图标。不是通过旋转同一装饰增加数量。',
 2:'同套上传与下载；相反传输方向具有独立操作语义。',
 3:'共用菱格重复骨架，主体分别是卷草莲瓣、环行行星、折线电路；已在各套28项联系表比较实际轮廓，不是仅改色。',
 4:'错行构图分别由海浪/地貌、羽叶枝条、带台阶机械剖面构成；主体轮廓和内部结构不同。',
 5:'护角边缘相似，装饰主体分别是放射扇面和带卷草的莲瓣，已查看足够大的角件图。',
 6:'两个V1框使用共用矩形双线，角饰分别是波折W和双斜线；保留为各风格的基本框。仅该功能家族各计一次，不将状态或换色再拆算。',
 7:'连续莲瓣与双斜线的实际轮廓不同，低矮长条画布造成相似哈希。',
 8:'敦煌切角双边与卷草莲瓣，对比复古圆舷窗边与环行行星；48框专项联系表及透明中心检查已查看。',
 9:'共用信息留白，左侧主要标识分别为莲瓣卷草和环行行星，区别超出颜色；只作一个图注框家族。',
 10:'圆印骨架相似，内部为带行星环的天体与阶梯电路，独立平铺装饰语汇不同。',
 11:'列表均需三行信息，但有序数字/图形标识、二级说明、边界、字级和行末标注不同；16套UI联系表已比较，保留为相同功能的不同视觉方案。',
 12:'包豪斯按钮包含大圆端与箭头，瑞士为平直黑块加红侧标；不是只有颜色不同。',
 13:'卡片信息布局相近，包豪斯主图是彩色拱梁、圆端按钮，瑞士主图是网格竖柱、直边按钮；已在UI整页核查。',
 14:'加载圆环是通用进度语义。装饰艺术使用退台双框，天文使用分度弧角与星芒边界；不将动画状态另计作品。',
 15:'侘寂工具栏为石形、断续笔线按钮；生成式为流线母题、闭合曲边按钮与侧轨；主体轮廓不同。',
 16:'弹窗共享信息/确认任务，敦煌是莲纹菱藻井与切角边，博物学是甲虫插图与纸签边；实际大型主体和边界均不同。'
 }
 assert len(groups)==16 and len(a['phash_candidates'])==21,'候选发生变化，必须重新目视检查'
 result=[]
 for g in groups:
  for pair_index in g['pairs']:
   p=a['phash_candidates'][pair_index];result.append({**p,'status':'reviewed-distinct','decision':'retain','basis':notes[g['group']],'group':g['group'],'sha256_a':by[p['a']]['sha256'],'sha256_b':by[p['b']]['sha256']})
 assert len(result)==len(a['phash_candidates'])
 dump(ROOT/'AUDIT/similarity-review-v2.json',{'reviewed_at':datetime.datetime.now().isoformat(timespec='seconds'),'method':'逐项查看实际相似联系表，并对照完整装饰/UI联系表、48框专项和标题框补绘；人工判断功能与可辨形态，不以哈希阈值直接批准。','reviewed_pairs':len(result),'duplicate_pairs':0,'unresolved':0,'decisions':result})
 print(len(result),'pairs reviewed with source hashes')
if __name__=='__main__':make()
