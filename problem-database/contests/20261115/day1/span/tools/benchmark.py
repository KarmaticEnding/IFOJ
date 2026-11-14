from pathlib import Path
import subprocess,time,json,tempfile,resource,argparse,hashlib
R=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--limit',type=float,default=6);parser.add_argument('--medium-only',action='store_true');parser.add_argument('--full-only',action='store_true');args=parser.parse_args()
 subprocess.run(['g++','-O2','-std=c++14',str(R/'tools/brute_fast.cpp'),'-o',str(R/'tools/brute_fast')],check=True)
 source=(R/'GPT/span.cpp').read_text()
 old='''int ret=INF,b=bel[q.x];
        for(int j=0;j<b;j++)ret=min(ret,low[j]);
        for(int s=b*C;s<=q.x;s++)ret=min(ret,bucket[s]);'''
 assert source.count(old)==1
 (R/'tools/scan_span.cpp').write_text(source.replace(old,'int ret=INF;for(int s=0;s<=q.x;s++)ret=min(ret,bucket[s]);'))
 subprocess.run(['g++','-O2','-std=c++14','-DLOCAL',str(R/'tools/scan_span.cpp'),'-o',str(R/'tools/scan_span')],check=True)
 value_source=(R/'tools/oracle.cpp').read_text().replace('auto update=[&](int k){if(mode=="scan")return;', 'vector<int>cur(K+1);auto update=[&](int k){cur[k]=f[k]<g[k]?pos[k][g[k]-1]-pos[k][f[k]]+1:0;if(mode=="scan")return;').replace('while(f[k]<g[k]&&pos[k][g[k]-1]-pos[k][f[k]]+1>t.x)++k;','while(cur[k]>t.x)++k;')
 (R/'tools/scan_values.cpp').write_text(value_source)
 subprocess.run(['g++','-O2','-std=c++14',str(R/'tools/scan_values.cpp'),'-o',str(R/'tools/scan_values')],check=True)
 todo=[(13,'brute_fast',[]),(14,'brute_fast',[]),(15,'brute_fast',[]),(16,'brute_fast',[]),(17,'oracle',['scan']),(18,'oracle',['scan']),(19,'oracle',['scan']),(20,'oracle',['scan']),(17,'scan_span',[]),(18,'scan_span',[]),(19,'scan_span',[]),(20,'scan_span',[])]
 todo.extend((case,'scan_values',['scan'])for case in range(17,21))
 report=[]
 if args.medium_only:
  todo=todo[:4]
  report=[x for x in json.loads((R/'tools/complexity-benchmarks.json').read_text())if x['case']>=17]
 if args.full_only:
  todo=[x for x in todo if x[0]>=17]
  report=[x for x in json.loads((R/'tools/complexity-benchmarks.json').read_text())if x['case']<17]
 for case,exe,flags in todo:
  start=time.monotonic();before=resource.getrusage(resource.RUSAGE_CHILDREN);status='completed'
  with (R/f'data/{case}.in').open('rb')as inp,tempfile.TemporaryFile()as out:
   try:
    subprocess.run([str(R/'tools'/exe),*flags],stdin=inp,stdout=out,check=True,timeout=args.limit)
    out.seek(0);assert out.read()==(R/f'data/{case}.ans').read_bytes(),(case,exe)
   except subprocess.TimeoutExpired:status='timeout'
  after=resource.getrusage(resource.RUSAGE_CHILDREN)
  row={'case':case,'algorithm':exe,'flags':flags,'status':status,'wall':time.monotonic()-start,'cpu':after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,'timeout':args.limit,'input_sha256':hashlib.sha256((R/f'data/{case}.in').read_bytes()).hexdigest()};report.append(row);print(row,flush=True)
  (R/'tools/complexity-benchmarks.json').write_text(json.dumps(report,indent=2))
