"""验证已生成图鉴的页数、图像、文字边界与实际使用的嵌入字体。"""
from pathlib import Path
import json, hashlib
import pdfplumber
from pypdf import PdfReader
from styles_data import ROOT

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    path=ROOT/'PREVIEWS/ARTISAN_V2_Atlas.pdf'
    mapping=json.loads((ROOT/'AUDIT/atlas-pages-v2.json').read_text(encoding='utf8'))
    errors=[]; pages=[]; used=set(); embedded=set()
    reader=PdfReader(path)
    assert len(reader.pages)==len(mapping)==178
    for page in reader.pages:
        for ref in page['/Resources']['/Font'].values():
            font=ref.get_object(); desc=font.get('/FontDescriptor')
            if desc and any(k in desc.get_object() for k in ['/FontFile','/FontFile2','/FontFile3']):
                embedded.add(str(font['/BaseFont']).lstrip('/'))
    with pdfplumber.open(path) as pdf:
        for n,(page,record) in enumerate(zip(pdf.pages,mapping),1):
            text=page.extract_text() or ''
            if not text.strip(): errors.append(f'empty text page {n}')
            if (page.width,page.height)!=(842,1191): errors.append(f'page size {n}')
            for ch in page.chars:
                used.add(ch['fontname'])
                if ch['x0']<-.5 or ch['x1']>page.width+.5 or ch['top']<-.5 or ch['bottom']>page.height+.5:
                    errors.append(f'text outside page {n}: {ch["text"]}')
            for im in page.images:
                if im['x0']<0 or im['x1']>page.width or im['top']<0 or im['bottom']>page.height:
                    errors.append(f'image outside page {n}')
            if record['kind']=='contact' and len(page.images)!=1: errors.append(f'contact image count {n}')
            if record['kind']=='style' and len(page.images)!=1: errors.append(f'style image count {n}')
            if record['kind']=='cover' and len(page.images)!=16: errors.append('cover image count')
            pages.append({'page':n,'kind':record['kind'],'text_characters':len(page.chars),'images':len(page.images)})
    if used-embedded: errors.append('Used unembedded fonts: '+str(used-embedded))
    result={'pdf':'PREVIEWS/ARTISAN_V2_Atlas.pdf','sha256':sha(path),'page_count':178,'used_fonts':sorted(used),'embedded_fonts':sorted(embedded),'errors':errors,'pages':pages}
    (ROOT/'AUDIT/pdf-v2-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k!='pages'},ensure_ascii=False))
    assert not errors
if __name__=='__main__':run()
