"""校验延伸阅读地址；下载 CC0 官方法律文本，绝不将参考网页内作品纳入素材包。"""
from styles_data import *
import urllib.request, concurrent.futures as cf, re, html
def verify(S):
    try:
        req=urllib.request.Request(S['source'],headers={'User-Agent':'Mozilla/5.0 ARTISAN/1.0'})
        with urllib.request.urlopen(req,timeout=15) as r:
            s=r.read(750000).decode('utf8','replace');title=re.search(r'<title[^>]*>(.*?)</title>',s,re.I|re.S)
            return {'style':S['id'],'status':r.status,'url':r.geturl(),'title':html.unescape(re.sub('<[^>]+>','',title[1])).strip()[:170] if title else ''}
    except Exception as e:return {'style':S['id'],'url':S['source'],'error':str(e)}
if __name__=='__main__':
    with cf.ThreadPoolExecutor(max_workers=5) as ex: res=list(ex.map(verify,STYLES))
    dump(ROOT/'TOOLS'/'reference-check.json',res)
    for r in res:print(r['style'],r.get('status',r.get('error')),ascii(r.get('title','')[:100]))
    req=urllib.request.Request('https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt',headers={'User-Agent':'ARTISAN-library/1.0'})
    with urllib.request.urlopen(req,timeout=25) as r:t=r.read().decode('utf8')
    assert 'CC0' in t and 'Waiver' in t
    write(ROOT/'LICENSES/CC0-1.0.txt',t)
