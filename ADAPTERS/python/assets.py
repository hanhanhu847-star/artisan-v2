"""只用标准库；既可导入，也可作为命令行筛选器。"""
from pathlib import Path
import json,argparse
ROOT=Path(__file__).resolve().parents[2]
def load(root=ROOT):return json.loads((Path(root)/'ASSET_INDEX.json').read_text(encoding='utf8'))
def find(index,style=None,category=None,file_format=None,license=None,min_width=0):
    return [a for a in index['assets'] if (not style or style==a['style_id']) and (not category or category==a['category']) and (not file_format or file_format==a['file_format']) and (not license or license==a['license']) and a['width']>=min_width]
def path_for(asset,root=ROOT):
    base=Path(root).resolve();p=(base/asset['file_path']).resolve()
    if not p.is_relative_to(base) or not p.is_file():raise FileNotFoundError(p)
    return p
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--style');ap.add_argument('--category');ap.add_argument('--format');ap.add_argument('--license');ap.add_argument('--min-width',type=int,default=0);a=ap.parse_args()
    for row in find(load(),a.style,a.category,a.format,a.license,a.min_width):print(path_for(row))
