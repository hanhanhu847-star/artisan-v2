"""CRC/全包SHA/新中文路径解压/真实断网浏览，回执写在ZIP旁而非修改包内文件。"""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,zipfile,shutil
from integrity_check import R,hashfile,manifest

def run():
    archive=R.parent/'ARTISAN_V2_Expanded_Asset_Library.zip'
    expected=json.loads((R/'FILES_SHA256.json').read_text(encoding='utf8'))
    assert manifest()==expected,'Working package changed after manifest'
    qa=R.parent/'ARTISAN-V2-QA'
    dest=(qa/('交付解压验证_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))).resolve()
    assert dest.is_relative_to(R.parent.resolve()) and not dest.exists()
    dest.mkdir(parents=True)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None,'ZIP CRC error'
        names={i.filename for i in z.infolist()}
        assert names=={'ARTISAN_V2/'+p for p in expected}|{'ARTISAN_V2/FILES_SHA256.json'}
        assert json.loads(z.read('ARTISAN_V2/FILES_SHA256.json'))==expected
        for p,h in expected.items():
            assert (dest/'ARTISAN_V2'/p).resolve().is_relative_to(dest)
            with z.open('ARTISAN_V2/'+p)as f:assert hashfile(f)==h,p
        z.extractall(dest)
    extracted=dest/'ARTISAN_V2'
    def check_extracted():
        actual={p.relative_to(extracted).as_posix() for p in extracted.rglob('*')if p.is_file()}
        assert actual==set(expected)|{'FILES_SHA256.json'}
        for p,h in expected.items():
            with (extracted/p).open('rb')as f:assert hashfile(f)==h,p
    check_extracted()
    browser_report=dest/'browser-check.json'
    env={**os.environ,'ARTISAN_TEST_ROOT':str(extracted),'ARTISAN_TEST_QA':str(dest/'browser-screenshots'),'ARTISAN_TEST_REPORT':str(browser_report)}
    node=os.environ.get('ARTISAN_NODE')or shutil.which('node')
    assert node,'Set ARTISAN_NODE to a Node executable with playwright available'
    subprocess.run([node,str(extracted/'TOOLS/v2_browser_check.cjs')],env=env,check=True)
    check_extracted() # Tests must not alter delivered files.
    browser=json.loads(browser_report.read_text(encoding='utf8'))
    with archive.open('rb')as f:zip_sha=hashfile(f)
    result={'status':'passed','verified_at':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),'archive':archive.name,'archive_bytes':archive.stat().st_size,'archive_sha256':zip_sha,'manifest_entries':len(expected),'zip_entries':len(expected)+1,'zip_crc':'passed','zip_file_sha256':'passed','extracted_file_sha256_before_and_after_browser':'passed','extraction_directory':extracted.relative_to(R.parent).as_posix(),'browser':browser,'release_gate':json.loads((extracted/'AUDIT/release-gate.json').read_text(encoding='utf8')),'scope':'Windows Chrome断网file://；其他平台与宿主框架未在此次解压测试中验证。'}
    receipt=R.parent/'ARTISAN_V2_RELEASE_VERIFICATION.json'
    receipt.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    print('DELIVERY PASSED:',len(expected),'manifest entries;',archive.stat().st_size,'bytes;',zip_sha)
    print('Receipt:',receipt)
if __name__=='__main__':run()
