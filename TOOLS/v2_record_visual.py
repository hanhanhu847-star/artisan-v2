"""人工查看联系表后记录证据；不得在尚未实际查看页面时调用。"""
from pathlib import Path
import hashlib,json,sys,datetime
from styles_data import ROOT
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(paths,note):
 f=ROOT/'AUDIT/visual-review-v2.json';data=json.loads(f.read_text(encoding='utf8'))if f.exists()else {'method':'实际打开联系表逐项目视检查；技术解码结果另列。不是自动评分。','pages':{}}
 pages={r['path']:r for r in json.loads((ROOT/'AUDIT/contact-pages.json').read_text(encoding='utf8'))}
 for rel in paths:
  p=ROOT/rel;r=pages[rel];base=ROOT/'STYLES'/r['style']
  data['pages'][rel]={'status':'reviewed','note':note,'contact_sha256':sha(p),'source_sha256':{file:sha(base/file)for file in r['assets']},'reviewed_at':datetime.datetime.now().isoformat(timespec='seconds')}
 f.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8');print(len(data['pages']),'contact pages recorded')
if __name__=='__main__':
 if len(sys.argv)<4:raise SystemExit('usage: v2_record_visual.py NOTE CATEGORY STYLE [STYLE...]')
 record([f'PREVIEWS/contacts/{z}/{sys.argv[2]}-1.jpg'for z in sys.argv[3:]],sys.argv[1])
