from pathlib import Path
import random,json,subprocess,hashlib,time
ROOT=Path(__file__).resolve().parent
GROUPS=[(1,2,6,6),(3,5,18,18),(6,9,100,50),(10,11,500,50),(12,15,2000,0),(16,19,2000,3),(20,25,2000,50)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def make(n,k,seed,variant):
    rng=random.Random(seed);a=[];mex=0;seen=set()
    # Witnesses vary first-occurrence order, repetitions and large MEX jumps.
    # The resulting noisy b is not promised monotone, nonnegative or smooth.
    speed=rng.uniform(.30,.90)
    pool=list(range(n+1));rng.shuffle(pool)
    for i in range(n):
        if rng.random()<speed:x=mex
        elif rng.random()<.5 and seen:x=rng.choice(tuple(seen))
        else:x=pool[rng.randrange(n+1)]
        a.append(x);seen.add(x)
        while mex in seen:mex+=1
    b=[];seen=set();mex=0
    for x in a:
        seen.add(x)
        while mex in seen:mex+=1
        noise=k//4 if variant=='wide' else k
        b.append(mex+rng.randint(-noise,noise))
    if variant=='unsat':
        # Contradiction only near the end: never let all zero-output cases exit early.
        b[-2]=n+k;b[-1]=-k
    return b
def answer(n,k,b,exe):
    raw=f'{n} {k}\n'+' '.join(map(str,b))+'\n';start=time.monotonic()
    out=subprocess.check_output([str(ROOT/'tools'/exe)],input=raw.encode(),timeout=30).decode()
    return out,time.monotonic()-start
def save(folder,index,n,k,b,group):
    assert len(b)==n and all(-k<=v<=n+k for v in b)
    out,t=answer(n,k,b,'std');other,u=answer(n,k,b,'oracle');assert out==other
    if group<=2:
        exact=subprocess.check_output([str(ROOT/'tools/oracle'),'subset'],input=(f'{n} {k}\n'+' '.join(map(str,b))+'\n').encode(),timeout=60).decode();assert out==exact
    p=ROOT/folder/f'{index}.in';q=p.with_suffix('.ans')
    assert not p.exists() and not q.exists()
    p.write_text(f'{n} {k}\n'+' '.join(map(str,b))+'\n');q.write_text(out)
    return {'input':str(p.relative_to(ROOT)),'n':n,'k':k,'group':group,'answer':int(out),'seconds':t,'oracle_seconds':u,'input_sha256':sha(p),'answer_sha256':sha(q)}
if __name__=='__main__':
    gate=json.loads((ROOT/'tools/verification.json').read_text());assert gate['passed'] and gate['std_sha256']==sha(ROOT/'GPT/mex.cpp') and gate['oracle_sha256']==sha(ROOT/'tools/oracle.cpp')
    for d in ['data','down']:(ROOT/d).mkdir(exist_ok=True)
    manifest=[]
    small=[(4,0,[0,0,0,0]),(4,1,[0,0,1,1]),(3,2,[-2,0,4])]
    for i,(n,k,b) in enumerate(small,1):manifest.append(save('down',i,n,k,b,1))
    for g,(left,right,n,k) in enumerate(GROUPS,1):
        for idx in range(left,right+1):
            variant='unsat' if idx in (9,19,25) else ('wide' if idx in (8,10,20,22,24) else 'witness')
            b=make(n,k,2026110700+idx,variant)
            row=save('data',idx,n,k,b,g);row['generation']=variant;manifest.append(row);print(row,flush=True)
        b=make(n,k,2026111700+g,'wide' if g==7 else 'witness');manifest.append(save('down',g+3,n,k,b,g))
    (ROOT/'tools/data-manifest.json').write_text(json.dumps(manifest,indent=2))
