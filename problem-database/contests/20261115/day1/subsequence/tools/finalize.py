from pathlib import Path
import hashlib,json,csv,yaml,re
R=Path(__file__).resolve().parents[1];root=R.parent.parent
rows=list(csv.reader((R/'result.csv').open()));summary=rows[0].index('summary');sample=rows[0].index('sample1')
assert float(rows[1][summary])==100
assert all(float(x)==5 for x in rows[1][1:summary]+rows[1][sample:sample+9])
audit=json.loads((R/'tools/data-audit.json').read_text());assert len(audit)==29
for label,row in audit.items():
 for ext in ['in','ans']:assert hashlib.sha256((R/(label+'.'+ext)).read_bytes()).hexdigest()==row['sha256_'+ext]
verification=json.loads((R/'tools/verification.json').read_text())
for key,path in [('std','GPT/subsequence.cpp'),('oracle','tools/oracle.cpp'),('brute','tools/brute.cpp')]:assert hashlib.sha256((R/path).read_bytes()).hexdigest()==verification[key+'_sha256']
deploy=json.loads((R/'tools/deployment.json').read_text())
for p,h in deploy['preserved_conf_sha256'].items():assert hashlib.sha256((root/'day1'/p/'conf.yaml').read_bytes()).hexdigest()==h
assert yaml.safe_load((root/'day1/conf.yaml').read_text())['subdir']==['product','subsequence','span','classic']
config=yaml.safe_load((R/'conf.yaml').read_text());assert config['time limit']==1.0 and config['memory limit']=='256 MiB'
report={'score':100,'formal_points':20,'points_each':5,'tier_scores':[10,10,15,10,20,35],'inline_samples':3,'large_file_samples':6,'max_formal_seconds':max(map(float,rows[2][1:summary])),'max_sample_seconds':max(map(float,rows[2][sample:sample+9])),'max_peak_kib':max(v['std_kib']for v in audit.values()),'time_limit_seconds':1.0,'memory_limit':'256 MiB','all_input_answer_hashes_checked':True,'standard_matches_pre_generation_verification':True,'other_problem_configurations_unchanged':True,'backup':deploy['backup']}
(R/'tools/final-check.json').write_text(json.dumps(report,indent=2))
p=root/'README.md';text=p.read_text()
line=f'Final subsequence validation: tuack score 100; all nine public samples accepted. Max formal time {report["max_formal_seconds"]:.3f}s; max sample time {report["max_sample_seconds"]:.3f}s. Limit 1.0s / 256 MiB.'
if 'Final subsequence validation:'in text:text=re.sub(r'(?m)^Final subsequence validation:.*$',line,text,count=1)
else:text+='\n'+line+'\n'
p.write_text(text)
print(json.dumps(report,indent=2),flush=True)
