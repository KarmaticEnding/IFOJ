"""One-time, backed-up installation of the approved T4 placeholder replacement."""
from pathlib import Path
import json,hashlib,shutil,datetime,yaml
stage=Path(__file__).resolve().parents[1]
root=stage.parent
assert root.name=='20261115' and stage.name=='.classic-build'
day=root/'day1';old=day/'t4';dest=day/'classic'
assert old.is_dir()and not dest.exists()
assert yaml.safe_load((old/'conf.yaml').read_text())['name']=='t4'
audit=json.loads((stage/'tools/data-audit.json').read_text());assert len(audit)==36
for label,row in audit.items():
 for ext in ['in','ans']:
  assert hashlib.sha256((stage/(label+'.'+ext)).read_bytes()).hexdigest()==row['sha256_'+ext]
hard=json.loads((stage/'tools/hardening-audit.json').read_text());assert hard['cpp_int']['accepted']
before={p:hashlib.sha256((day/p/'conf.yaml').read_bytes()).hexdigest()for p in ['product','t2','span']}
config=yaml.safe_load((day/'conf.yaml').read_text());assert config['subdir']==['product','t2','span','t4']
backup=root/'.backups'/('t4-before-classic-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
backup.mkdir(parents=True)
for p in ['README.md','AGENTS.md','day1/conf.yaml','day1/product/conf.yaml','day1/span/conf.yaml','day1/t2/conf.yaml']:
 q=backup/p;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/p,q)
shutil.move(str(old),str(backup/'t4'))
shutil.move(str(stage),str(dest))
config['subdir'][-1]='classic';(day/'conf.yaml').write_text(yaml.safe_dump(config,allow_unicode=True,sort_keys=False))
readme=(root/'README.md').read_text().replace('day1/t4','day1/classic').replace('T1 product, T3 span; T2 and T4 are placeholders.','T1 product, T3 span, T4 classic; T2 is a placeholder.').replace('product and span are complete; t2 and t4 remain placeholders.','product, span and classic are complete; t2 remains a placeholder.').replace('T2/T4 retain placeholder limits.','classic: 5.0 seconds, 512 MiB. T2 retains placeholder limits.').replace('Order: product, t2, span, t4.','Order: product, t2, span, classic.')
readme+='\n\n## T4 classic completed\n\nBased on CF464E The Classic Problem; n<=100000, m<=200000, 0<=x<=100000, modulus=1000000007.\nGPT/classic.cpp implements exact canonical persistent binary trees with Dijkstra. Twenty-five independent four-point cases; tiers 12/8/4/8/16/16/24/12.\nThree inline samples plus eight full-size file samples. Reference .ans files contain a complete shortest path; different optimal paths are accepted.\nOfficial and downloadable SPJs are independent exact implementations using the unmodified official testlib.h.\nAll data were verified against independent exact integer or structural oracles before installation. Verification, data and hardening audits are under day1/classic/tools/.\nTree and unicyclic full-size points have 99999 and 100000 edges; unique-exponent points have the maximal compatible 100001 edges.\nBackup: '+str(backup.relative_to(root))+'\n'
(root/'README.md').write_text(readme)
agents=(root/'AGENTS.md').read_text().replace('当前 product (T1), span (T3); T2/T4 remain placeholders。','当前 product (T1), span (T3), classic (T4); T2 remains a placeholder。')
(root/'AGENTS.md').write_text(agents)
assert before=={p:hashlib.sha256((day/p/'conf.yaml').read_bytes()).hexdigest()for p in before}
(dest/'tools/deployment.json').write_text(json.dumps({'backup':str(backup),'preserved_conf_sha256':before,'order':config['subdir']},indent=2))
print('Installed',dest,'backup',backup,flush=True)
