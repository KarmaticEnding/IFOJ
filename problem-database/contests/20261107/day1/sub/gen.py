#!/usr/bin/env python3
"""Deterministic dataset builder. Run tools/verify.py successfully first.

Every official input and downloadable large example is checked against its own
constraints. Answers are produced by GPT/sub.cpp and compared byte-for-byte
with an independently implemented four-Fenwick oracle.
"""
from pathlib import Path
import argparse, hashlib, json, random, shutil, subprocess, time

ROOT = Path(__file__).resolve().parent
P = 993244853
GROUPS = [
    (1,1,100,100,False), (2,2,500,500,False), (3,3,2000,2000,False),
    (4,5,1000000,5,False), (6,9,50000,50000,True),
    (10,13,50000,50000,False), (14,16,200000,200000,False),
    (17,20,1000000,1000000,False),
]
# Every case uses its tier's exact upper bounds. Only the announced point-update
# tier has restricted update intervals. Seeds, not structural tricks, vary cases.
CASES = [(g[2],g[3],'point' if g[4] else 'random')
         for g in GROUPS for _ in range(g[0],g[1]+1)]
LARGE = [(g[2],g[3],'point' if g[4] else 'random') for g in GROUPS]

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
        updates=queries=switches=0
        previous=None
        lengths={1:0,2:0}
        full={1:0,2:0}
        singleton={1:0,2:0}
        point_locations={}
        for _ in range(m):
            v=list(map(int,f.readline().split()))
            assert len(v) in (3,4)
            op,l,r=v[:3]
            assert 1<=l<=r<=n
            if previous is not None: switches += op != previous
            previous=op
            assert op in (1,2)
            lengths[op]+=r-l+1
            full[op]+=int(l==1 and r==n)
            singleton[op]+=int(l==r)
            if op==1:
                assert len(v)==4 and 1<=v[3]<P
                assert not point or l==r
                updates+=1
                if point: point_locations[l]=point_locations.get(l,0)+1
            else:
                assert op==2 and len(v)==3
                queries+=1
        assert not f.read().strip(), 'extra input'
    return {'n':n,'m':m,'updates':updates,'queries':queries,'group':group,
            'operation_switches':switches,
            'mean_update_length':lengths[1]/max(1,updates),
            'mean_query_length':lengths[2]/max(1,queries),
            'full_updates':full[1],'full_queries':full[2],
            'singleton_updates':singleton[1],'singleton_queries':singleton[2],
            'distinct_updated_positions':len(point_locations) if point else None,
            'max_updates_at_one_position':max(point_locations.values(),default=0) if point else None}

def write_case(path,n,m,mode,seed):
    rng=random.Random(seed)
    with path.open('x') as f:
        f.write('%d %d\n'%(n,m))
        for lo in range(0,n,10000):
            values=[str(rng.randrange(1,P)) for _ in range(lo,min(n,lo+10000))]
            f.write((' ' if lo else '')+' '.join(values))
        f.write('\n')
        # Reject the all-update/all-query sequence for m=5, so both operations
        # are exercised. No fixed count, order, or alternation is imposed.
        kinds=bytearray(rng.getrandbits(1)+1 for _ in range(m))
        while 1 not in kinds or 2 not in kinds:
            kinds=bytearray(rng.getrandbits(1)+1 for _ in range(m))
        buffer=[]
        for op in kinds:
            l,r=sorted((rng.randint(1,n),rng.randint(1,n)))
            if op==1:
                if mode=='point': l=r=rng.randint(1,n)
                x=rng.randrange(1,P)
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
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT,
                        help='empty output directory; an existing dataset is never overwritten')
    parser.add_argument('--seed-base',type=int,default=202611071000)
    args=parser.parse_args()
    out=args.output_dir.resolve()
    verification=json.loads((ROOT/'tools/verification.json').read_text())
    assert verification['standard_sha256']==sha(ROOT/'GPT/sub.cpp'), 'reverify changed standard first'
    assert verification['reference_sha256']==sha(ROOT/'tools/reference.cpp'), 'reverify changed oracle first'
    assert verification['brute_force_cases']>=1000
    std,ref=ROOT/'tools/.build/sub',ROOT/'tools/.build/reference'
    for folder in ('data','down','tools'): (out/folder).mkdir(exist_ok=True,parents=True)
    for folder,count in [('data',20),('down',11)]:
        assert not any((out/folder/('%d.%s'%(i,s))).exists()
                       for i in range(1,count+1) for s in ('in','ans')), 'output files already exist'
    manifest={'verification':verification, 'seed_base':args.seed_base,
              'generation_policy':'independent random operations and endpoints at exact tier bounds',
              'cases':[]}
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
        if mode!='small sample':
            bounds=GROUPS[group-1]
            assert stats['n']==bounds[2] and stats['m']==bounds[3]
            assert stats['updates'] and stats['queries']
            if stats['m']>=100:
                assert .3 <= stats['updates']/stats['m'] <= .7
                assert .25 <= stats['operation_switches']/(stats['m']-1) <= .75
                assert .2 <= stats['mean_query_length']/stats['n'] <= .5
                if not bounds[4]:
                    assert .2 <= stats['mean_update_length']/stats['n'] <= .5
        stats.update({'file':str(path.relative_to(out)),'mode':mode,'input_sha256':sha(path),
                      'answer_sha256':sha(ans),'bytes':path.stat().st_size,
                      'validated_and_cross_checked':True,'elapsed_seconds':round(time.time()-started,3)})
        manifest['cases'].append(stats)
        (out/'tools/data-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(json.dumps(stats),flush=True)
    # No official or sample files are written until the verification gate above passed.
    for i,(text,known) in enumerate(SMALL,1):
        path=out/'down'/('%d.in'%i)
        if out!=ROOT and (ROOT/'down'/('%d.in'%i)).exists():
            shutil.copy2(ROOT/'down'/('%d.in'%i),path)
            finish(path,1 if i<3 else 5,'small sample')
            assert path.with_suffix('.ans').read_bytes()==(ROOT/'down'/('%d.ans'%i)).read_bytes()
        else:
            with path.open('x') as f: f.write(text)
            finish(path,1 if i<3 else 5,'small sample',known)
    for i,(n,m,mode) in enumerate(CASES,1):
        group=next(j for j,g in enumerate(GROUPS,1) if g[0]<=i<=g[1])
        path=out/'data'/('%d.in'%i)
        write_case(path,n,m,mode,args.seed_base+i)
        finish(path,group,mode)
    for group,(n,m,mode) in enumerate(LARGE,1):
        path=out/'down'/('%d.in'%(group+3))
        write_case(path,n,m,mode,args.seed_base+100+group)
        finish(path,group,'large '+mode)
    manifest['completed_at']=time.strftime('%Y-%m-%dT%H:%M:%S%z')
    (out/'tools/data-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE: 20 official cases, 3 inline samples, 8 large downloadable samples.',flush=True)

if __name__=='__main__': main()
