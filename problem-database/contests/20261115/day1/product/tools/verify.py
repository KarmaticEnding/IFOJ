from pathlib import Path
import subprocess,random,json,hashlib,tempfile,itertools,sys,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'));from model import solve,validate,small_dp,P
H='743822d8120213a3482f4a6e8b9846219b84218350be548a42bdfdb056fba9e3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw(b):return (str(len(b))+'\n'+' '.join(map(str,b))+'\n').encode()
def run(exe,b):return subprocess.check_output([str(R/'tools'/exe)],input=raw(b),timeout=20)
def checker(exe,inp,out,ans):return subprocess.run([str(R/'tools'/exe),str(inp),str(out),str(ans)],capture_output=True,timeout=20)
if __name__=='__main__':
    assert sha(R/'data/chk/testlib.h')==sha(R/'down/testlib.h')==H
    for src,out,flags in [('GPT/product.cpp','std',['-O2','-DLOCAL']),('GPT/product.cpp','sanitized',['-O1','-DLOCAL','-fsanitize=undefined,bounds','-D_GLIBCXX_ASSERTIONS']),('data/chk/chk.cpp','official',['-O2']),('down/checker.cpp','public',['-O2'])]:subprocess.run(['g++','-std=c++14',*flags,str(R/src),'-o',str(R/'tools'/out)],check=True)
    rng=random.Random(2026111401);cases=[]
    for n in range(1,4):cases.extend(list(b)for b in itertools.product(range(1,7),repeat=n))
    for _ in range(180):
        n=rng.randint(1,9);a=[rng.randint(1,4)for _ in range(n)];lo=100;hi=0;b=[]
        for x in a:lo=min(lo,x);hi=max(hi,x);b.append(lo*hi)
        if rng.random()<.5:b[rng.randrange(n)]=rng.randint(1,16)
        cases.append(b)
    for b in cases:
        count,alt=solve(b);assert count==small_dp(b);validate(b,run('std',b),count)
    big=[[1,P,P],[P*P,P,P],[1,10**18,10**18,10**18],[10**18],[(10**9-1)**2],[(10**9-1)**2+1],[10**18-1],[4,6,6,5],[4,2*(P+1),2*(P+1),2*(P+1)+1],[(P+1)**2,(P+1),P]]
    for b in big:
        count,a=solve(b);validate(b,run('std',b),count);validate(b,run('sanitized',b),count)
    # Test independent SPJs, non-unique constructions, count-zero feasibility,
    # integer bounds, exact two-line impossibility, and count-only .ans files.
    spj_tests=0
    with tempfile.TemporaryDirectory()as tmp:
        p=Path(tmp);inp=p/'input';out=p/'output';ans=p/'answer'
        for b in [[4,6,6],[1,P,P],[P*P,P,P],[4,7],[10**18],[1,10**18,10**18],[(10**9-1)**2+1]]:
            count,a=solve(b);inp.write_bytes(raw(b));ans.write_text(str(count)+'\n')
            good=run('std',b);alt=(str(count)+'\n'+(' '.join(map(str,a))if a else '-1')+'\n').encode()
            outputs=[(good,True),(alt,True),(b'0\n-1\n',False),(b'-1\n',False),(b'-1\n-1\nextra\n',False),(b'\n',False),(good+b'17\n',False),(b'1000000007\n1\n',False),(b'1\n1000000000000000001\n',False)]
            if count>=0:outputs.extend([(str(count).encode()+b'\n-1\n',False),(str(count).encode()+b'\n0\n',False),(str(count).encode()+b'\n' + b' '.join([b'1']*(len(b)+1))+b'\n',False)])
            else:outputs.extend([(b'-1\n-1\n',True),(b'0\n0\n',False),(b'-1 -1\n',False)])
            for contents,expected in outputs:
                out.write_bytes(contents)
                for exe in ['official','public']:
                    result=checker(exe,inp,out,ans);assert (result.returncode==0)==expected,(b,exe,contents[:100],result.stderr)
                    spj_tests+=1
        inp.write_bytes(raw([4,6,6]));ans.write_text('2\n');out.write_text('2\n2 3 3\n')
        full=p/'full';score=p/'score';info=p/'info';full.write_text('5\n')
        subprocess.run([str(R/'tools/official'),str(inp),str(out),str(ans),str(full),str(score),str(info)],check=True);assert float(score.read_text())==5
        out.write_text('2\n2 3 1000000000000000000\n')
        subprocess.run([str(R/'tools/official'),str(inp),str(out),str(ans),str(full),str(score),str(info)],check=True);assert float(score.read_text())==0
    subprocess.run(['g++','-O2','-std=c++14',str(R/'GPT/product.cpp'),'-o',str(R/'tools/file-io')],check=True)
    with tempfile.TemporaryDirectory()as tmp:
        p=Path(tmp);(p/'product.in').write_bytes(raw([4,6,6]));subprocess.run([str(R/'tools/file-io')],cwd=p,check=True);validate([4,6,6],(p/'product.out').read_bytes(),2)
    report={'passed':True,'small_cases':len(cases),'large_boundary_cases':len(big),'spj_verdicts':spj_tests,'tuack_adapter':True,'file_io':True,'std_sha256':sha(R/'GPT/product.cpp'),'official_sha256':sha(R/'data/chk/chk.cpp'),'public_sha256':sha(R/'down/checker.cpp'),'testlib_sha256':H}
    (R/'tools/verification.json').write_text(json.dumps(report,indent=2));print(report)
