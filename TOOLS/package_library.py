"""生成可搬移整包。先用 integrity_check.py --write 刷新清单。"""
from integrity_check import R,files
from zipfile import ZipFile,ZIP_DEFLATED,ZIP_STORED
with ZipFile(R.parent/'ARTISAN_V2_Expanded_Asset_Library.zip','w',allowZip64=True) as z:
    for p in files()+[R/'FILES_SHA256.json']:
        z.write(p,'ARTISAN_V2/'+p.relative_to(R).as_posix(),compress_type=ZIP_STORED if p.suffix in {'.jpg','.png','.webp','.pdf'} else ZIP_DEFLATED)
print('Archive written')
