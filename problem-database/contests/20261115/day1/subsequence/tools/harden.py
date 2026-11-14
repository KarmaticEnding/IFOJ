from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'))
from model import pairs,greedy,binary_only

def collapsed(s,t,k):
 if t[0]==t[1]:
  q=min(len(s),s.count(t[0])+k);return q*(q-1)//2
 states={0:(0,0)}
 for old in s:
  nxt={}
  for spent,(score,a)in states.items():
   for c in {old,*t}:
    used=spent+(old!=c)
    if used<=k:nxt[used]=max(nxt.get(used,(-1,-1)),(score+(a if c==t[1]else 0),a+(c==t[0])))
  states=nxt
 return max(score for score,a in states.values())

if __name__=='__main__':
 audit=json.loads((R/'tools/data-audit.json').read_text());rows={}
 for i in range(1,21):
  p=R/f'data/{i}.in';parts=p.read_text().split();n,k=map(int,parts[:2]);s,t=parts[2:];expected=int((R/f'data/{i}.ans').read_text())
  assert audit[f'data/{i}']['answer']==expected
  row={'expected':expected,'collapsed_state':collapsed(s,t,k)}
  if t[0]!=t[1]:row.update(binary_only=binary_only(s,t,k),greedy_left=greedy(s,t,k,True),greedy_right=greedy(s,t,k))
  else:
   q=min(n,s.count(t[0])+k);row['wrong_equal_char_q_squared']=q*q
  row['wrong_count_adjacent_only_upper_bound']=n-1
  rows[str(i)]=row
 full=[str(i)for i in range(14,21)]
 report={'cases':rows,'failed_full_cases':{name:[i for i in full if rows[i][name]!=rows[i]['expected']]for name in ['binary_only','greedy_left','greedy_right','collapsed_state']},'general_cases_have_third_characters':all(audit['data/'+i]['alphabet_size']>=3 for i in full),'general_cases_budget_below_saturation':all(audit['data/'+i]['k']<audit['data/'+i]['edits_for_theoretical_maximum']for i in full),'formal_n_at_tier_maximum':all(audit[f'data/{i}']['n']==(12 if i<=2 else 200)for i in range(1,21))}
 assert len(report['failed_full_cases']['binary_only'])==7
 assert len(set(report['failed_full_cases']['greedy_left'])&set(report['failed_full_cases']['greedy_right']))>=4
 assert report['failed_full_cases']['collapsed_state']
 assert report['general_cases_have_third_characters']and report['general_cases_budget_below_saturation']and report['formal_n_at_tier_maximum']
 (R/'tools/hardening-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
