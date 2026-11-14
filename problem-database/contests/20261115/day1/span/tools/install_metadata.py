from pathlib import Path
import hashlib,json,shutil
r=Path.home()/'IFOJ/problem-database/contests/20261115';p=r/'day1/span'
stage=Path(__file__).resolve().parents[1]
paths=list(p.rglob('*'))+[r/'README.md',r/'day1/conf.yaml']+list((r/'day1').glob('*/conf.yaml'))
state={str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file()}
(stage/'tools/original-state.json').write_text(json.dumps(state,indent=2))
text=(p/'statement/zh-cn.md').read_text();head=text.split("{{ s('input format') }}")[0]
assert '\\text{otherwise}' not in head or '0 &' in head
(stage/'statement').mkdir(exist_ok=True)
(stage/'statement/zh-cn.md').write_text(head+(stage/'tools/statement-tail.md').read_text())
print('Original description preserved; snapshots recorded.')
