"""标准库验证整包文件或 ZIP：python TOOLS/integrity_check.py [ZIP 路径]。"""
from pathlib import Path
import json, hashlib, sys, zipfile
R=Path(__file__).resolve().parents[1]
def hashfile(f):
    h=hashlib.sha256()
    for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def files():return sorted(p for p in R.rglob('*') if p.is_file() and p.name!='FILES_SHA256.json' and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix!='.pyc')
def manifest():return {p.relative_to(R).as_posix():hashfile(p.open('rb')) for p in files()}
if __name__=='__main__':
    if '--write' in sys.argv:
        (R/'FILES_SHA256.json').write_text(json.dumps(manifest(),ensure_ascii=False,indent=1),encoding='utf8');print('Manifest written');sys.exit()
    expected=json.loads((R/'FILES_SHA256.json').read_text(encoding='utf8'))
    if '--source-only' in sys.argv:
        included=lambda p:not(p.startswith('PREVIEWS/') and p.endswith('.pdf'))
        expected={p:h for p,h in expected.items() if included(p)}
        actual={p:h for p,h in manifest().items() if included(p)}
        assert actual==expected,'source checkout file set or checksum mismatch'
        print('Verified',len(expected),'source checkout SHA-256 entries (Release PDFs excluded)');sys.exit()
    if len(sys.argv)>1:
        with zipfile.ZipFile(sys.argv[1]) as z:
            assert z.testzip() is None,'ZIP CRC error'
            names={n.removeprefix('ARTISAN_V2/') for n in z.namelist() if not n.endswith('/')};assert names==set(expected)|{'FILES_SHA256.json'},'path mismatch'
            assert json.loads(z.read('ARTISAN_V2/FILES_SHA256.json'))==expected
            for name,h in expected.items():
                with z.open('ARTISAN_V2/'+name) as f:assert hashfile(f)==h,name
    else:assert manifest()==expected,'file set or checksum mismatch'
    print('Verified',len(expected),'SHA-256 entries')
