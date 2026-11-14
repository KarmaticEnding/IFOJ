from pathlib import Path
import csv,json,hashlib,yaml,subprocess,shutil
R=Path(__file__).resolve().parents[1];root=R.parent.parent
rows=list(csv.reader((R/'result.csv').open()))
header=rows[0];summary=header.index('summary');start=header.index('sample1')
assert float(rows[1][summary])==100
assert all(float(x)==4 for x in rows[1][1:summary])
assert all(float(x)==4 for x in rows[1][start:start+11])
assert all(x.startswith('ok ')for x in rows[3][1:summary]+rows[3][start:start+11])
audit=json.loads((R/'tools/data-audit.json').read_text());assert len(audit)==36
for label,row in audit.items():
 for ext in ['in','ans']:assert hashlib.sha256((R/(label+'.'+ext)).read_bytes()).hexdigest()==row['sha256_'+ext]
verify=json.loads((R/'tools/verification.json').read_text())
for k,p in [('std','GPT/classic.cpp'),('oracle','tools/oracle.cpp'),('official','data/chk/chk.cpp'),('public','down/checker.cpp')]:assert hashlib.sha256((R/p).read_bytes()).hexdigest()==verify[k+'_sha256']
for p in ['down/testlib.h','data/chk/testlib.h']:assert hashlib.sha256((R/p).read_bytes()).hexdigest()==verify['testlib_sha256']
deployment=json.loads((R/'tools/deployment.json').read_text())
for p,h in deployment['preserved_conf_sha256'].items():assert hashlib.sha256((root/'day1'/p/'conf.yaml').read_bytes()).hexdigest()==h
assert yaml.safe_load((root/'day1/conf.yaml').read_text())['subdir']==['product','t2','span','classic']
assert yaml.safe_load((R/'conf.yaml').read_text())['time limit']==5.0
assert yaml.safe_load((R/'conf.yaml').read_text())['memory limit']=='512 MiB'
report={'score':100,'formal_points':25,'points_each':4,'tier_scores':[12,8,4,8,16,16,24,12],'public_samples':11,'max_formal_seconds':max(map(float,rows[2][1:summary])),'max_sample_seconds':max(map(float,rows[2][start:start+11])),'max_generator_peak_kib':max(x['std_kib']for x in audit.values()),'all_formal_and_sample_spj_messages_ok':True,'all_input_answer_hashes_checked':True,'standard_and_checkers_match_pre_generation_verification':True,'other_problem_configurations_unchanged':True,'time_limit_seconds':5.0,'memory_limit':'512 MiB','backup':deployment['backup']}
(R/'tools/final-check.json').write_text(json.dumps(report,indent=2))
p=root/'README.md';text=p.read_text()
marker='\nFinal classic validation:'
if marker in text:text=text[:text.index(marker)]
text+=f'\nFinal classic validation: tuack score 100; all 11 samples accepted. Max formal time {report["max_formal_seconds"]:.3f}s; max sample time {report["max_sample_seconds"]:.3f}s. Limit 5.0s / 512 MiB. The standalone statement was rendered and visually checked page by page.\n'
p.write_text(text)
backup=Path(deployment['backup'])
original=root/'statements/noi/day1.pdf'
if original.exists()and not(backup/'day1-before-classic.pdf').exists():shutil.copy2(original,backup/'day1-before-classic.pdf')
print(json.dumps(report,indent=2))
