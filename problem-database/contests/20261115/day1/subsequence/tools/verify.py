from pathlib import Path
import subprocess,hashlib,json,random,itertools,tempfile,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from model import encode,exhaustive,binary_only,pairs
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
 for src,out,flags in [('GPT/subsequence.cpp','std',['-O2','-DLOCAL']),('tools/oracle.cpp','oracle',['-O2']),('tools/brute.cpp','brute',['-O2']),('tools/batch.cpp','batch',['-O2']),('tools/batch.cpp','sanitized',['-O1','-fsanitize=undefined,bounds','-D_GLIBCXX_ASSERTIONS'])]:
  subprocess.run(['g++','-std=c++14',*flags,str(R/src),'-o',str(R/'tools'/out)],check=True)
 rng=random.Random(140920261114);cases=[];expected=[];binary=0
 for n in range(2,6):
  for letters in itertools.product('abc',repeat=n):
   s=''.join(letters)
   for t in ['ab','aa']:
    values=exhaustive(s,t)
    for k,ans in enumerate(values):cases.append((s,t,k));expected.append(ans)
 for z in range(60):
  n=rng.randint(6,8);s=''.join(rng.choices('abc',k=n));t=rng.choice(['ab','aa','ba','cc']);values=exhaustive(s,t)
  for k,ans in enumerate(values):cases.append((s,t,k));expected.append(ans)
 for n in range(2,9):
  for letters in itertools.product('ab',repeat=n):
   s=''.join(letters)
   # The polynomial special-case formula was independently brute-tested before
   # this project; here it is compared to both general DPs for every budget.
   for k in range(n+1):cases.append((s,'ab',k));expected.append(binary_only(s,'ab',k));binary+=1
 for s,t,k,ans in [('bbaa','ab',2,3),('asddsaf','sd',3,10),('abacaba','aa',2,15),('cccc','ab',4,4),('aaaa','ab',4,4),('aaaa','aa',4,6),('ababa','ab',0,3),('ba','ab',1,0),('ba','ab',2,1)]:cases.append((s,t,k));expected.append(ans)
 data=str(len(cases))+'\n'+''.join(f'{k} {s} {t}\n'for s,t,k in cases)
 for name in ['batch','sanitized']:
  output=subprocess.check_output([str(R/'tools'/name)],input=data.encode(),timeout=180).decode().splitlines()
  assert len(output)==len(cases)
  for case,ans,line in zip(cases,expected,output):assert list(map(int,line.split()))==[ans,ans],(case,ans,line,name)
 # Check actual stdin/stdout and file-I/O executables as well as the harness.
 for z in range(20):
  n=rng.randint(2,12);s=''.join(rng.choices('abc',k=n));t=rng.choice(['ab','aa','ba']);k=rng.randint(0,n);text=encode(s,t,k)
  got=[int(subprocess.check_output([str(R/'tools'/exe)],input=text.encode(),timeout=15))for exe in ['std','oracle','brute']]
  assert len(set(got))==1,(text,got)
 subprocess.run(['g++','-O2','-std=c++14',str(R/'GPT/subsequence.cpp'),'-o',str(R/'tools/file-io')],check=True)
 with tempfile.TemporaryDirectory()as tmp:
  p=Path(tmp);(p/'subsequence.in').write_text('4 2\nbbaa\nab\n');subprocess.run([str(R/'tools/file-io')],cwd=tmp,check=True);assert(p/'subsequence.out').read_text().strip()=='3'
 report={'passed':True,'python_exact_and_fixed_cases':len(cases)-binary,'binary_special_cases':binary,'total_dp_comparisons':len(cases),'sanitized_cases':len(cases),'three_way_cli_cases':20,'file_io':True,'std_sha256':sha(R/'GPT/subsequence.cpp'),'oracle_sha256':sha(R/'tools/oracle.cpp'),'brute_sha256':sha(R/'tools/brute.cpp')}
 (R/'tools/verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
