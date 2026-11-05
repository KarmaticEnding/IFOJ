// Contestant self-checker. Uses unmodified Mike Mirzayanov testlib.h.
// Compile: g++ -O2 -std=c++14 checker.cpp -o checker
// Usage: ./checker vector.in vector.out sample.ans
// The third file is required by testlib but its contents are intentionally ignored.
#include "testlib.h"
#include <unordered_set>
#include <cstdint>
static uint64_t pairKey(int x,int y){return (uint64_t(uint32_t(x))<<32)|uint32_t(y);}
int main(int argc,char**argv){
    registerTestlibCmd(argc,argv);
    int n=inf.readInt(1,1000000,"n"),m=inf.readInt(1,1000000,"m");
    ensuref(1LL*n*m<=1000000,"invalid input size");
    std::unordered_set<uint64_t> cells,jumps;
    cells.reserve(n*m);jumps.reserve(n*m);
    int px=0,py=0;
    for(int i=0;i<n*m;i++){
        if(ouf.seekEof())quitf(_wa,"Only %d of %d cells were provided",i,n*m);
        int x=ouf.readInt(-1,n,"row");
        if(i==0&&x==-1)quitf(_wa,"A route exists for every legal grid; -1 is incorrect");
        if(x<1)quitf(_wa,"Step %d: row must be positive",i+1);
        int y=ouf.readInt(1,m,"column");
        if(i==0&&(x!=1||y!=1))quitf(_wa,"The first cell must be (1,1), got (%d,%d)",x,y);
        if(!cells.insert(pairKey(x,y)).second)quitf(_wa,"Step %d revisits cell (%d,%d)",i+1,x,y);
        if(i){int dx=x-px,dy=y-py;
            if(!jumps.insert(pairKey(dx,dy)).second)quitf(_wa,"Jump %d repeats signed vector (%d,%d)",i,dx,dy);
        }
        px=x;py=y;
    }
    if(!ouf.seekEof())quitf(_wa,"Extra data after the required %d cells",n*m);
    quitf(_ok,"All %d cells and %d signed jump vectors are distinct",n*m,n*m-1);
}
