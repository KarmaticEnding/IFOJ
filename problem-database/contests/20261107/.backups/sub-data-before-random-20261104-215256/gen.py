#!/usr/bin/env python3
"""Deterministic dataset builder. Run tools/verify.py successfully first.

Every official input and downloadable large example is checked against its own
constraints. Answers are produced by GPT/sub.cpp and compared byte-for-byte
with an independently implemented four-Fenwick oracle.
"""
from pathlib import Path
import hashlib, json, random, subprocess, time

ROOT = Path(__file__).resolve().parent
P = 993244853
GROUPS = [
    (1,1,100,100,False), (2,2,500,500,False), (3,3,2000,2000,False),
    (4,5,1000000,5,False), (6,9,50000,50000,True),
    (10,13,50000,50000,False), (14,16,200000,200000,False),
    (17,20,1000000,1000000,False),
]
CASES = [
    (100,100,'mixed'), (500,500,'nested'), (2000,2000,'mixed'),
    (1000000,5,'few'), (999983,5,'zero'),
    (50000,50000,'point'), (49999,50000,'hotspot'),
    (50000,49999,'endpoints'), (49157,50000,'point'),
    (50000,50000,'mixed'), (49999,50000,'nested'),
    (50000,50000,'full'), (49157,50000,'cross'),
    (200000,200000,'mixed'), (199999,200000,'full'),
    (200000,200000,'nested'), (1000000,1000000,'mixed'),
    (1000000,1000000,'full'), (999983,1000000,'nested'),
    (1000000,1000000,'cross'),
]
LARGE = [(100,100,'mixed'), (500,500,'nested'), (2000,2000,'mixed'),
         (1000000,5,'few'), (50000,50000,'point'),
         (50000,50000,'cross'), (200000,200000,'nested'),
         (1000000,1000000,'mixed')]

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()

def validate(path, group):
    _,_,maxn,maxm,point = GROUPS[group-1]
    with path.open() as f:
        fields = f.readline().split()
        assert len(fields)==2
        n,m = map(int,fields)
        assert 1<=n<=maxn and 1<=m<=maxm
        a = list(map(int,f.readline().split()))
        assert len(a)==n and all(1<=v<P for v in a)
        del a
        updates=queries=0
        for _ in range(m):
            v=list(map(int,f.readline().split()))
            assert len(v) in (3,4)
            op,l,r=v[:3]
            assert 1<=l<=r<=n
            if op==1:
                assert len(v)==4 and 1<=v[3]<P
                assert not point or l==r
                updates+=1
            else:
                assert op==2 and len(v)==3
                queries+=1
        assert not f.read().strip(), 'extra input'
    return {'n':n,'m':m,'updates':updates,'queries':queries,'group':group}

def write_case(path,n,m,mode,seed):
    rng=random.Random(seed)
    with path.open('x') as f:
        f.write('%d %d\n'%(n,m))
        for lo in range(0,n,10000):
            if mode=='few': values=['1']*min(10000,n-lo)
            elif mode in ('zero','full'): values=[str(P-1)]*min(10000,n-lo)
            else:
                values=[str((1 if i%11==0 else P-1 if i%11==1 else rng.randrange(1,P)))
                        for i in range(lo,min(n,lo+10000))]
            f.write((' ' if lo else '')+' '.join(values))
        f.write('\n')
        if mode=='few':
            f.write('2 1 %d\n1 2 %d %d\n2 1 %d\n2 %d %d\n2 2 %d\n'%(n,n,P-1,n,n,n,n-1))
            assert m==5
            return
        if mode=='zero':
            f.write('1 1 %d 1\n2 1 %d\n2 1 1\n1 %d %d %d\n2 %d %d\n'%(n,n,n,n,P-1,n-1,n))
            assert m==5
            return
        buffer=[]
        for i in range(m):
            l,r=sorted((rng.randint(1,n),rng.randint(1,n)))
            update=(i%2==1)
            if mode=='nested':
                inset=(i//2)%max(1,n//2)
                l,r=1+inset,n-inset
            elif mode=='full' and update: l,r=1,n
            elif mode=='cross':
                if i%4<2: l,r=1,r
                else: l,r=l,n
                if i%31==0:
                    b=1<<rng.randrange(n.bit_length())
                    l,r=max(1,b-1),min(n,b+1)
            if i%37==0 and not update: l,r=1,n
            if i%41==0 and not update: l=r
            if update:
                if mode=='point': r=l
                elif mode=='hotspot': l=r=n//2
                elif mode=='endpoints': l=r=(1 if i%4==1 else n)
                x=1 if i%7==1 else P-1 if i%7==3 else rng.randrange(1,P)
                buffer.append('1 %d %d %d\n'%(l,r,x))
            else: buffer.append('2 %d %d\n'%(l,r))
            if len(buffer)==10000: f.writelines(buffer); buffer=[]
        f.writelines(buffer)

SMALL = [
    ('3 6\n1 2 3\n2 1 3\n1 1 2 2\n2 1 3\n2 2 3\n1 2 3 1\n2 1 2\n','20\n34\n14\n16\n'),
    ('1 5\n993244852\n2 1 1\n1 1 1 1\n2 1 1\n1 1 1 993244852\n2 1 1\n','993244852\n0\n993244852\n'),
    ('4 7\n2 1 3 2\n2 2 4\n1 2 2 4\n2 1 4\n1 4 4 2\n2 3 4\n1 1 1 3\n2 1 2\n','21\n64\n14\n20\n'),
]

def main():
    verification=json.loads((ROOT/'tools/verification.json').read_text())
    assert verification['standard_sha256']==sha(ROOT/'GPT/sub.cpp'), 'reverify changed standard first'
    assert verification['reference_sha256']==sha(ROOT/'tools/reference.cpp'), 'reverify changed oracle first'
    assert verification['brute_force_cases']>=1000
    std,ref=ROOT/'tools/.build/sub',ROOT/'tools/.build/reference'
    for folder in ('data','down'): (ROOT/folder).mkdir(exist_ok=True)
    manifest={'verification':verification, 'seed_base':2026110700, 'cases':[]}
    def finish(path,group,mode,known=None):
        started=time.time()
        stats=validate(path,group)
        ans=path.with_suffix('.ans')
        assert not ans.exists()
        with path.open('rb') as fin, ans.open('xb') as fout:
            t=time.time()
            measured=subprocess.run(['/usr/bin/time','-f','%e %M',str(std)],stdin=fin,stdout=fout,
                                    stderr=subprocess.PIPE,check=True,timeout=60)
            stats['std_wall_seconds']=round(time.time()-t,4)
            elapsed,rss=measured.stderr.decode().split()
            stats['program_wall_seconds']=float(elapsed)
            stats['peak_rss_kib']=int(rss)
        with path.open('rb') as fin:
            oracle=subprocess.run([str(ref)],stdin=fin,stdout=subprocess.PIPE,check=True,timeout=60).stdout
        assert ans.read_bytes()==oracle, 'oracle mismatch: '+str(path)
        if known is not None: assert oracle.decode()==known, 'manual sample mismatch'
        numbers=oracle.split()
        assert len(numbers)==stats['queries'] and all(0<=int(v)<P for v in numbers)
        stats.update({'file':str(path.relative_to(ROOT)),'mode':mode,'input_sha256':sha(path),
                      'answer_sha256':sha(ans),'bytes':path.stat().st_size,
                      'validated_and_cross_checked':True,'elapsed_seconds':round(time.time()-started,3)})
        manifest['cases'].append(stats)
        (ROOT/'tools/data-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(json.dumps(stats),flush=True)
    # No official or sample files are written until the verification gate above passed.
    for i,(text,known) in enumerate(SMALL,1):
        path=ROOT/'down'/('%d.in'%i)
        with path.open('x') as f: f.write(text)
        finish(path,1 if i<3 else 5,'small sample',known)
    for i,(n,m,mode) in enumerate(CASES,1):
        group=next(j for j,g in enumerate(GROUPS,1) if g[0]<=i<=g[1])
        path=ROOT/'data'/('%d.in'%i)
        write_case(path,n,m,mode,2026110700+i)
        finish(path,group,mode)
    for group,(n,m,mode) in enumerate(LARGE,1):
        path=ROOT/'down'/('%d.in'%(group+3))
        write_case(path,n,m,mode,2026110800+group)
        finish(path,group,'large '+mode)
    manifest['completed_at']=time.strftime('%Y-%m-%dT%H:%M:%S%z')
    (ROOT/'tools/data-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE: 20 official cases, 3 inline samples, 8 large downloadable samples.',flush=True)

if __name__=='__main__': main()
