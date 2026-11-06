"""Build a small Pages site; serve original assets from a pinned public Git commit.

Usage: python TOOLS/build_pages.py OUTPUT_DIRECTORY --revision PUSHED_COMMIT
Requires Python only. Does not delete files, change Git branches, or publish.
"""
import argparse
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--revision', required=True, help='Full SHA of a public source commit containing these assets')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-f0-9]{40}', args.revision):
        parser.error('--revision must be a full 40-character Git commit SHA')
    out = args.output.resolve()
    if out == ROOT or ROOT in out.parents:
        parser.error('output must be outside the source library')
    base = 'https://raw.githubusercontent.com/hanhanhu847-star/artisan-v2/' + args.revision + '/'
    files = [
        '.nojekyll', 'index.html', 'BROWSER/index.html', 'BROWSER/browser.css',
        'BROWSER/browser-v2.js', 'BROWSER/catalog-data.js', 'BROWSER/web-preview-data.js',
        'AUTHORS.md', 'START_HERE.txt', 'LICENSE', 'LICENSE-ASSETS.md',
        'LICENSES/asset-sources-v2.json', 'PREVIEWS/CONTACT_SHEETS.html',
        'SHARED/utility-assets/registration.svg', 'SHARED/patterns/alpha-grid.svg',
        'PREVIEWS/plates/bauhaus.webp', 'PREVIEWS/plates/dunhuang.webp', 'PREVIEWS/plates/blueprint.webp',
    ]
    for name in files:
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    config = out / 'BROWSER/deployment-config.js'
    config.write_text('window.ARTISAN_ASSET_BASE=' + json.dumps(base) + ';\n', encoding='utf-8')
    page = out / 'BROWSER/index.html'
    page.write_text(page.read_text(encoding='utf-8').replace(
        '<script defer src="catalog-data.js">',
        '<script defer src="deployment-config.js"></script><script defer src="catalog-data.js">'), encoding='utf-8')
    contacts = out / 'PREVIEWS/CONTACT_SHEETS.html'
    def asset_link(match):
        attribute, value = match.groups()
        if value.startswith(('#', 'http:', 'https:', 'data:')) or value == '../BROWSER/index.html':
            return match.group(0)
        return attribute + '="' + urljoin(base + 'PREVIEWS/', value) + '"'
    contacts.write_text(re.sub(r'(src|href)="([^"]+)"', asset_link, contacts.read_text(encoding='utf-8')), encoding='utf-8')
    (out / 'deployment.json').write_text(json.dumps({'asset_revision': args.revision, 'asset_base': base}, indent=2), encoding='utf-8')
    published = [p for p in out.rglob('*') if p.is_file() and '.git' not in p.parts]
    print(json.dumps({'output': str(out), 'files': len(published), 'bytes': sum(p.stat().st_size for p in published), 'asset_revision': args.revision}))

if __name__ == '__main__':
    main()
