import math
P=100000007
def solve(b):
    r=math.isqrt(b[0])
    if r*r!=b[0]:return -1,None
    lo=hi=r;ways=1;a=[r]
    for v in b[1:]:
        same=lo*hi==v
        grow=(v%lo==0 and v//lo>hi)
        shrink=(v%hi==0 and 0<v//hi<lo)
        if same:ways=ways*(hi-lo+1)%P;a.append(hi)
        elif grow:hi=v//lo;a.append(hi)
        elif shrink:lo=v//hi;a.append(lo)
        else:return -1,None
    return ways,a
def validate(b,out,expected):
    lines=out.decode().splitlines()
    assert len(lines)==2
    assert list(map(int,lines[0].split()))==[expected]
    a=list(map(int,lines[1].split()))
    if expected==-1:assert a==[-1];return
    assert len(a)==len(b)
    lo=10**18;hi=0
    for i,x in enumerate(a):
        assert 1<=x<=10**18
        lo=min(lo,x);hi=max(hi,x);assert lo*hi==b[i],(i,x,b[i])
def small_dp(b):
    states={(0,0):1};B=max(b)
    for v in b:
        new={}
        for (lo,hi),ways in states.items():
            for x in range(1,B+1):
                l=min(lo,x)if lo else x;h=max(hi,x)
                if l*h==v:new[l,h]=new.get((l,h),0)+ways
        states=new
    return sum(states.values())%P if states else -1
