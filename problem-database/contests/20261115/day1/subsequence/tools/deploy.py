from pathlib import Path
import hashlib,json,shutil,datetime,yaml
stage=Path(__file__).resolve().parents[1];root=stage.parent;day=root/'day1'
assert stage.name=='.subsequence-build'and root.name=='20261115'
old=day/'t2';dest=day/'subsequence';assert old.is_dir()and not dest.exists()
assert yaml.safe_load((old/'conf.yaml').read_text())['name']=='t2'
audit=json.loads((stage/'tools/data-audit.json').read_text());assert len(audit)==29
for label,row in audit.items():
 for ext in ['in','ans']:assert hashlib.sha256((stage/(label+'.'+ext)).read_bytes()).hexdigest()==row['sha256_'+ext]
hard=json.loads((stage/'tools/hardening-audit.json').read_text());assert hard['formal_n_at_tier_maximum']
preserve={p:hashlib.sha256((day/p/'conf.yaml').read_bytes()).hexdigest()for p in ['product','span','classic']}
config=yaml.safe_load((day/'conf.yaml').read_text());assert config['subdir']==['product','t2','span','classic']
backup=root/'.backups'/('t2-before-subsequence-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True)
for name in ['README.md','AGENTS.md','day1/conf.yaml','day1/product/conf.yaml','day1/span/conf.yaml','day1/classic/conf.yaml','statements/noi/day1.pdf']:
 p=root/name
 if p.exists():
  q=backup/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
shutil.move(str(old),str(backup/'t2'));shutil.move(str(stage),str(dest))
config['subdir'][1]='subsequence';(day/'conf.yaml').write_text(yaml.safe_dump(config,allow_unicode=True,sort_keys=False))
readme=(root/'README.md').read_text().replace('day1/t2','day1/subsequence').replace('T1 product, T3 span, T4 classic; T2 is a placeholder.','T1 product, T2 subsequence, T3 span, T4 classic.').replace('product, span and classic are complete; t2 remains a placeholder.','All four problem projects are complete.').replace('T2 retains placeholder limits.','subsequence: 1.0 second, 256 MiB.').replace('Order: product, t2, span, classic.','Order: product, subsequence, span, classic.')
readme+='\n\n## T2 subsequence completed\n\nBased on CF1409F Subsequences of Length Two; n<=200, 0<=k<=n. GPT/subsequence.cpp implements O(n^2*k) time, O(n*k) space rolling DP.\nTwenty independent five-point cases; tiers 10/10/15/10/20/35. Three inline samples and six separate full-size file samples.\nAll answers are unique integers. Standard comparison is used. No SPJ or construction is needed.\nBefore generation, 8578 cases were checked by independent forward/reverse DPs and sanitizers, plus direct search and actual file-I/O checks. All formal and public answers were independently checked.\nAll unrestricted full-size points require using third characters and have non-saturated budgets. Binary-only shortcuts, local greedy and collapsed DP counterexamples are recorded under day1/subsequence/tools/.\nBackup: '+str(backup.relative_to(root))+'\n'
(root/'README.md').write_text(readme)
agents=(root/'AGENTS.md').read_text().replace('当前 product (T1), span (T3), classic (T4); T2 remains a placeholder。','当前 product (T1), subsequence (T2), span (T3), classic (T4)，四题均已完成。')
(root/'AGENTS.md').write_text(agents)
assert preserve=={p:hashlib.sha256((day/p/'conf.yaml').read_bytes()).hexdigest()for p in preserve}
(dest/'tools/deployment.json').write_text(json.dumps({'backup':str(backup),'preserved_conf_sha256':preserve,'order':config['subdir']},indent=2))
print('Installed',dest,'backup',backup,flush=True)
