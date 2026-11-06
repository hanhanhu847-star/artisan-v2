"""发布前核对证据与当前源文件。不会自行授予目视审查结果。"""
import json,hashlib,csv
from styles_data import ROOT

def read(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):(ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def run():
    idx=read('ASSET_INDEX.json');assets=idx['assets'];by={a['asset_id']:a for a in assets}
    assert len(assets)==3824 and idx['work_count']==1804
    for a in assets:
        assert sha(ROOT/a['file_path'])==a['sha256'],a['file_path']
        assert (ROOT/a['preview_path']).is_file(),a['preview_path']
    audit=read('AUDIT/v2-audit.json')
    assert not audit['errors'] and not audit['sha_duplicate_groups'] and not audit['svg_geometry_groups']
    review=read('AUDIT/similarity-review-v2.json')
    valid={(p['a'],p['b']) for p in review['decisions'] if p['sha256_a']==by[p['a']]['sha256'] and p['sha256_b']==by[p['b']]['sha256']}
    assert all((p['a'],p['b']) in valid for p in audit['phash_candidates'])
    contacts=read('AUDIT/contact-pages.json'); visual=read('AUDIT/visual-review-v2.json')['pages']
    assert len(contacts)==160
    for p in contacts:
        r=visual[p['path']]
        assert r['status']=='reviewed' and r['contact_sha256']==sha(ROOT/p['path']),p['path']
        assert set(r['source_sha256'])==set(p['assets'])
        for f in p['assets']:assert r['source_sha256'][f]==sha(ROOT/'STYLES'/p['style']/f),f
    pdf=read('AUDIT/pdf-v2-check.json');pv=read('AUDIT/pdf-visual-review-v2.json')
    assert not pdf['errors'] and pdf['page_count']==178
    assert pdf['sha256']==pv['pdf_sha256']==sha(ROOT/pdf['pdf'])
    assert pv['overview_pages_reviewed']==list(range(1,179))
    tiles=read('AUDIT/v2-texture-check.json');svg=read('AUDIT/svg-tiling.json')
    assert len(tiles)==256 and len(svg)==113 and all(x['ok'] for x in tiles+svg)
    frames=read('AUDIT/frame-apertures.json')
    assert len(frames)==48 and all(x['apertureMaxAlpha']==0 and sha(ROOT/x['file'])==x['sha256'] for x in frames)
    browser=read('AUDIT/browser-v2-check.json')
    assert browser['network']=='offline' and browser['protocol']=='file:'
    assert not browser['pageErrors'] and not browser['externalRequests'] and not browser['localResourceErrors']
    csvrows=list(csv.DictReader((ROOT/'LICENSES/asset-sources-v2.csv').open(encoding='utf-8-sig')))
    assert len(csvrows)==len(assets)
    for row in csvrows:
        a=by[row['asset_id']]
        assert all(row[k]==a[k] for k in row),row['asset_id']
        assert (ROOT/a['license_file']).is_file()
    # 保留原工程全部清单项；V2中仅源素材副本要求与V1逐字节相同。
    baseline=read('AUDIT/v1-files-sha256.json');old=ROOT.parent/'ARTISAN'
    assert old.is_dir(),'原V1目录不可用，不能更新保留验收'
    mismatches=[p for p,h in baseline.items() if not (old/p).is_file() or sha(old/p)!=h]
    sources=read('AUDIT/v1-asset-index.json')['assets']
    copied=[a['file_path']for a in sources if sha(ROOT/a['file_path'])!=a['sha256']]
    assert not mismatches and not copied
    save('AUDIT/v1-preservation.json',{'original_files_verified':len(baseline),'original_mismatches':mismatches,'source_assets_verified':len(sources),'copied_source_mismatches':copied})
    groups=read('AUDIT/similarity-groups.json')
    for g in groups:g['status']='reviewed-see-similarity-review-v2.json'
    save('AUDIT/similarity-groups.json',groups)
    audit['status']='technical-checks-passed; manual evidence in similarity-review-v2.json and visual-review-v2.json'
    save('AUDIT/v2-audit.json',audit)
    idx['audit_status']='assets-and-atlas-validated; final ZIP result in adjacent ARTISAN_V2_RELEASE_VERIFICATION.json'
    save('ASSET_INDEX.json',idx)
    (ROOT/'BROWSER/catalog-data.js').write_text('window.ARTISAN = '+json.dumps(idx,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
    summary={'status':'assets-and-atlas-validated','source_files':len(assets),'independent_style_families':idx['work_count'],'visual_pages':160,'pdf_pages':178,'similarity_pairs_reviewed':len(audit['phash_candidates']),'source_fingerprint':hashlib.sha256(json.dumps({a['file_path']:a['sha256']for a in assets},sort_keys=True,separators=(',',':')).encode()).hexdigest(),'evidence_sha256':{p:sha(ROOT/p)for p in ['AUDIT/v2-audit.json','AUDIT/visual-review-v2.json','AUDIT/similarity-review-v2.json','AUDIT/pdf-v2-check.json','AUDIT/pdf-visual-review-v2.json','AUDIT/v1-preservation.json']}}
    save('AUDIT/release-gate.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='evidence_sha256'},ensure_ascii=False))
if __name__=='__main__':run()
