#!/usr/bin/env python3
"""Generate official inputs only after standard/checker verification succeeds."""
from pathlib import Path
import hashlib,json,subprocess,time,shutil
ROOT=Path(__file__).resolve().parent
CASES=[(3,3),(2,4), (1,1000000),(1000000,1),(1,999999),(999999,1),
       (1000,1000),(1001,998),(998,1001),(400,2500),(2500,400),(512,1952),
       (999,1001),(1001,999),(997,1003),(1003,997),(101,9899),(9899,101),
       (996,1003),(1003,996)]
SMALL=[(1,1),(2,3),(3,4)]
LARGE=[(3,3),(1,1000000),(1001,998),(999,1001)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate_input(n,m,case=None,group=None):
    assert n>=1 and m>=1 and n*m<=1000000
    if group is None:group=1 if case<=2 else 2 if case<=6 else 3 if case<=12 else 4
    if group==1:assert n*m<=9
    if group==2:assert n==1 or m==1
    if group==3:assert n*m%2==0
    if group>1:assert n*m>=990000
    return group
def validate_output(n,m,path):
    seen=bytearray(n*m);used=bytearray((2*n-1)*(2*m-1));prev=None;count=0
    with path.open() as f:
        for line in f:
            tokens=line.split();assert len(tokens)==2
            x,y=map(int,tokens);assert 1<=x<=n and 1<=y<=m
            if count==0:assert (x,y)==(1,1)
            p=(x-1)*m+y-1;assert not seen[p];seen[p]=1
            if prev:
                dx=x-prev[0];dy=y-prev[1];key=(dx+n-1)*(2*m-1)+dy+m-1
                assert not used[key];used[key]=1
            prev=x,y;count+=1
    assert count==n*m
def main():
    verified=json.loads((ROOT/'tools/verification.json').read_text())
    for path,h in verified['source_hashes'].items():assert sha(ROOT/path)==h,'source changed; reverify first'
    records=[]
    def make(folder,index,n,m,group):
        start=time.time();inp=ROOT/folder/f'{index}.in';ans=inp.with_suffix('.ans')
        assert not inp.exists() and not ans.exists()
        if folder=='down' and index<=3:assert n>=1 and m>=1 and n*m<=1000000
        else:validate_input(n,m,group=group)
        inp.write_text(f'{n} {m}\n')
        with inp.open('rb') as fi,ans.open('xb') as fo:
            r=subprocess.run(['/usr/bin/time','-f','%e %M',str(ROOT/'tools/.build/vector')],stdin=fi,stdout=fo,stderr=subprocess.PIPE,check=True,timeout=20)
        validate_output(n,m,ans)
        for checker in ('official','public'):
            r2=subprocess.run([str(ROOT/'tools/.build'/checker),str(inp),str(ans),str(ans)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
            assert r2.returncode==0,(checker,r2.stderr)
        elapsed,rss=r.stderr.decode().split()
        rec={'file':str(inp.relative_to(ROOT)),'n':n,'m':m,'cells':n*m,'group':group,'input_sha256':sha(inp),'answer_sha256':sha(ans),
             'standard_seconds':float(elapsed),'peak_rss_kib':int(rss),'independent_validation':True,'both_checkers_accepted':True,'elapsed_seconds':round(time.time()-start,3)}
        records.append(rec);print(json.dumps(rec),flush=True)
        (ROOT/'tools/data-manifest.json').write_text(json.dumps({'verified':verified,'cases':records},indent=2)+'\n')
    for i,(n,m) in enumerate(SMALL,1):
        # Inline examples intentionally small, exempt from large-tier size policy.
        make('down',i,n,m,1 if n*m<=9 else 4)
    for i,(n,m) in enumerate(CASES,1):make('data',i,n,m,validate_input(n,m,case=i))
    for i,(n,m) in enumerate(LARGE,4):make('down',i,n,m,i-3)
    report={'verified':verified,'cases':records,'completed_at':time.strftime('%Y-%m-%dT%H:%M:%S%z')}
    (ROOT/'tools/data-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print('COMPLETE: 20 official tests, 3 inline examples, 4 large examples.',flush=True)
if __name__=='__main__':main()
