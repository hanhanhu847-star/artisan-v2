"""Generate lightweight, same-aspect previews of large raster originals for HTTP browsing.

Uses existing source images only. Originals, asset IDs and licenses stay unchanged.
Run after v2_index.py when the source catalog changes; requires Pillow.
"""
import json
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]

def main():
    catalog = json.loads((ROOT / 'ASSET_INDEX.json').read_text(encoding='utf-8'))
    out = ROOT / 'PREVIEWS/web-detail'
    out.mkdir(parents=True, exist_ok=True)
    previews = {}
    for asset in catalog['assets']:
        if asset['file_bytes'] <= 4 * 1024 * 1024 or asset['file_format'] not in ('jpg', 'png', 'webp'):
            continue
        target = out / (asset['asset_id'] + '.webp')
        with Image.open(ROOT / asset['file_path']) as source:
            preview = ImageOps.exif_transpose(source)
            preview.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            preview.save(target, 'WEBP', quality=84, method=6)
        previews[asset['file_path']] = target.relative_to(ROOT).as_posix()
    (ROOT / 'BROWSER/web-preview-data.js').write_text(
        '/* Online detail previews; source and license remain in ARTISAN.assets. */\n'
        + 'window.ARTISAN_WEB_PREVIEWS=' + json.dumps(previews, ensure_ascii=False, indent=2) + ';\n',
        encoding='utf-8')
    print(json.dumps({'previews': len(previews), 'bytes': sum((ROOT / p).stat().st_size for p in previews.values())}))

if __name__ == '__main__':
    main()
