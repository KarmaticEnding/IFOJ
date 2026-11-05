from pathlib import Path
import subprocess,random,json,hashlib,itertools,time,tempfile
R=Path(__file__).resolve().parents[1]
P=998244353
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(exe,n,k,b,mode=None):
    a=[str(R/'tools'/exe)]+([mode] if mode else [])
    return int(subprocess.check_output(a,input=(f'{n} {k}\n'+ ' '.join(map(str,b))+'\n').encode(),timeout=30))
def brute(n,k,b):
    ans=0;ct=[0]*(n+2)
    def dfs(i,mex):
        nonlocal ans
        if i==n:ans+=1;return
        for x in range(n+1):
            ct[x]+=1;v=mex
            while ct[v]:v+=1
            if abs(v-b[i])<=k:dfs(i+1,v)
            ct[x]-=1
    dfs(0,0);return ans%P
if __name__=='__main__':
    subprocess.run(['g++','-O2','-std=c++14','-DLOCAL',str(R/'GPT/mex.cpp'),'-o',str(R/'tools/std')],check=True)
    subprocess.run(['g++','-O2','-std=c++14',str(R/'tools/oracle.cpp'),'-o',str(R/'tools/oracle')],check=True)
    rng=random.Random(16081107);tests=0
    for n in range(1,4):
        for k in range(3):
            for b in itertools.product(range(-k,n+k+1),repeat=n):
                expected=brute(n,k,b)
                assert run('std',n,k,b)==expected,(n,k,b)
                tests+=1
    for t in range(180):
        n=rng.randint(1,7);k=rng.randint(0,6)
        a=[rng.randrange(n+1) for _ in range(n)];seen=set();b=[]
        for x in a:
            seen.add(x);v=0
            while v in seen:v+=1
            b.append(v+rng.randint(-k,k))
        if t%3==0:b[rng.randrange(n)]=rng.randint(-k,n+k)
        expected=brute(n,k,b)
        assert run('std',n,k,b)==expected==run('oracle',n,k,b,'subset')
        tests+=1
    for t in range(180):
        n=rng.randint(8,110);k=rng.randint(0,50)
        b=[rng.randint(max(-k,i//3-k),min(n+k,i//3+k)) for i in range(n)]
        assert run('std',n,k,b)==run('oracle',n,k,b,'slow')
        tests+=1
    for n,k,b,out in [(4,0,[0]*4,256),(4,1,[0]*4,431),(4,1,[0,0,1,1],509),(5,2,[0,0,2,2,0],6546),(3,2,[-2,0,4],11)]:
        assert run('std',n,k,b)==out
    subprocess.run(['g++','-O1','-g','-fsanitize=undefined,bounds','-D_GLIBCXX_ASSERTIONS','-DLOCAL',str(R/'GPT/mex.cpp'),'-o',str(R/'tools/sanitized')],check=True)
    for t in range(40):
        n=rng.randint(1,80);k=rng.randint(0,50);b=[rng.randint(-k,n+k) for _ in range(n)]
        assert run('std',n,k,b)==run('sanitized',n,k,b)
    subprocess.run(['g++','-O2',str(R/'GPT/mex.cpp'),'-o',str(R/'tools/file-io')],check=True)
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);(p/'mex.in').write_text('4 1\n0 0 1 1\n')
        subprocess.run([str(R/'tools/file-io')],cwd=tmp,check=True)
        assert (p/'mex.out').read_text().strip()=='509'
    result={'passed':True,'comparison_cases':tests,'official_examples':5,'sanitized':40,'file_io':True,'std_sha256':sha(R/'GPT/mex.cpp'),'oracle_sha256':sha(R/'tools/oracle.cpp')}
    (R/'tools/verification.json').write_text(json.dumps(result,indent=2));print(result)
