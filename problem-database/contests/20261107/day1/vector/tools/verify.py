#!/usr/bin/env python3
from pathlib import Path
import hashlib,itertools,json,random,subprocess,tempfile,time
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(n,m,text):
    words=text.split()
    assert len(words)==2*n*m
    points=list(zip(map(int,words[::2]),map(int,words[1::2])))
    assert points[0]==(1,1)
    assert all(1<=x<=n and 1<=y<=m for x,y in points)
    assert len(set(points))==n*m
    vectors=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
    assert len(set(vectors))==len(vectors)
    return points
def main():
    started=time.time();build=ROOT/'tools/.build';build.mkdir(exist_ok=True)
    for src,name,flags in [('GPT/vector.cpp','vector',['-DLOCAL']),('down/checker.cpp','public',[]),('data/chk/chk.cpp','official',[])]:
        subprocess.run(['g++','-O2','-std=c++14','-Wall','-Wextra',*flags,str(ROOT/src),'-o',str(build/name)],check=True)
    subprocess.run(['g++','-O1','-std=c++14','-DLOCAL','-fsanitize=undefined,bounds','-fno-sanitize-recover=all',str(ROOT/'GPT/vector.cpp'),'-o',str(build/'vector-ubsan')],check=True)
    rng=random.Random(1179);dims=list(itertools.product(range(1,26),repeat=2))
    dims += [(rng.randint(1,200),rng.randint(1,200)) for _ in range(100)]
    for i,(n,m) in enumerate(dims):
        r=subprocess.run([str(build/'vector')],input=f'{n} {m}\n'.encode(),stdout=subprocess.PIPE,check=True,timeout=5)
        validate(n,m,r.stdout)
        if i<40:
            r2=subprocess.run([str(build/'vector-ubsan')],input=f'{n} {m}\n'.encode(),stdout=subprocess.PIPE,check=True,timeout=5)
            assert r.stdout==r2.stdout
    check_count=0
    with tempfile.TemporaryDirectory() as folder:
        t=Path(folder);inp,out,ans=t/'input',t/'output',t/'answer'
        ans.write_text('intentionally not a route\n')
        def check(n,m,text,ok,lemon=False):
            nonlocal check_count
            inp.write_text(f'{n} {m}\n');out.write_text(text)
            for checker in ('public','official'):
                r=subprocess.run([str(build/checker),str(inp),str(out),str(ans)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
                assert (r.returncode==0)==ok,(checker,n,m,text[:150],r.returncode,r.stderr)
            if lemon:
                score,info=t/'score',t/'info'
                if score.exists():score.unlink()
                r=subprocess.run([str(build/'official'),str(inp),str(out),str(ans),'100',str(score),str(info)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
                assert r.returncode==0 and score.exists(),r.stderr
                assert float(score.read_text())==(100 if ok else 0),(score.read_text(),info.read_text())
            check_count+=1
        # Legal alternative route includes opposite vectors; answer contents must be ignored.
        check(2,3,'1 1\n1 3\n1 2\n2 2\n2 3\n2 1\n',True,True)
        check(1,1,'1 1\n',True,True)
        for n,m in [(1,9),(9,1),(2,7),(7,2),(3,3),(4,7),(7,5)]:
            text=subprocess.check_output([str(build/'vector')],input=f'{n} {m}\n'.encode()).decode()
            check(n,m,text,True,True)
        good=subprocess.check_output([str(build/'vector')],input=b'3 3\n').decode()
        mutations=['','-1\n','1 1\n','4 1\n'+good,'0 1\n'+good,'1.5 1\n'+good,'999999999999999999999999999 1\n',good+'1 1\n',good+'garbage\n','1 1\n1 1\n'+good,
                   '1 1\n1 2\n1 3\n2 1\n2 2\n2 3\n3 1\n3 2\n3 3\n',
                   good.replace('1 1','2 2',1)]
        for text in mutations:check(3,3,text,False,True)
        # Exhaustive output permutations on small grids establish checker agreement with the oracle.
        for n,m in [(1,4),(2,2),(2,3)]:
            cells=list(itertools.product(range(1,n+1),range(1,m+1)))
            for tail in itertools.permutations(cells[1:]):
                points=[(1,1),*tail];text=''.join(f'{x} {y}\n' for x,y in points)
                try:validate(n,m,text);ok=True
                except AssertionError:ok=False
                check(n,m,text,ok)
        # Actual contestant file I/O behavior.
        subprocess.run(['g++','-O2','-std=c++14',str(ROOT/'GPT/vector.cpp'),'-o',str(build/'vector-file')],check=True)
        (t/'vector.in').write_text('3 4\n')
        subprocess.run([str(build/'vector-file')],cwd=t,check=True,timeout=5)
        validate(3,4,(t/'vector.out').read_bytes())
    source=json.loads((ROOT/'tools/testlib-source.json').read_text())
    assert digest(ROOT/'data/chk/testlib.h')==digest(ROOT/'down/testlib.h')==source['sha256']
    report={'verified_at':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'grid_cases':len(dims),'checker_cases':check_count,
            'sanitizer_cases':40,'file_io_checked':True,'testlib_sha256':source['sha256'],
            'source_hashes':{x:digest(ROOT/x) for x in ('GPT/vector.cpp','down/checker.cpp','data/chk/chk.cpp')},
            'elapsed_seconds':round(time.time()-started,3)}
    (ROOT/'tools/verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
