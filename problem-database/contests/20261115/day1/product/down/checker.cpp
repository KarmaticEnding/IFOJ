// Downloadable checker: recomputes the count; validates construction using division.
#include "testlib.h"
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <cctype>
using i64=long long;
const i64 MAXB=1000000000000000000LL,P=100000007;
static i64 solve(const std::vector<i64>&b){
    i64 r=(i64)std::sqrt((long double)b[0]);
    while(r>b[0]/r)--r;while(r+1<=b[0]/(r+1))++r;
    if(b[0]%r||b[0]/r!=r)return -1;
    i64 lo=r,hi=r,ways=1;
    for(size_t i=1;i<b.size();i++){
        if(b[i]==lo*hi)ways=ways*((hi-lo+1)%P)%P;
        else if(b[i]>lo*hi){if(b[i]%lo)return -1;i64 t=b[i]/lo;if(t<=hi)return -1;hi=t;}
        else{if(b[i]%hi)return -1;i64 t=b[i]/hi;if(t<1||t>=lo)return -1;lo=t;}
    }return ways;
}
int main(int argc,char**argv){
    registerTestlibCmd(argc,argv);int n=inf.readInt(1,1000000,"n");std::vector<i64>b(n);for(auto&x:b)x=inf.readLong(1,MAXB,"b");
    i64 exact=solve(b),jury=ans.readLong(-1,P-1,"count");if(jury!=exact||!ans.seekEof())quitf(_fail,"answer file must contain the correct count only");
    // Use an independent line parser rather than the official checker's testlib stream.
    std::ifstream out(argv[2]);std::string first,second,rest;std::getline(out,first);std::getline(out,second);
    std::istringstream one(first),two(second);i64 v;std::string more;
    if(!(one>>v)||v!=exact||(one>>more))quitf(_wa,"first line: expected %lld",exact);
    if(exact<0){if(!(two>>v)||v!=-1||(two>>more))quitf(_wa,"write -1 on both lines for an impossible input");}
    else{
        i64 minimum=MAXB,maximum=1;
        for(int i=0;i<n;i++){
            if(!(two>>v)||v<1||v>MAXB)quitf(_wa,"second line: invalid a[%d]",i+1);
            if(v<minimum)minimum=v;if(v>maximum)maximum=v;
            if(b[i]%maximum||b[i]/maximum!=minimum)quitf(_wa,"a[%d] creates an incorrect prefix product",i+1);
        }
        if(two>>more)quitf(_wa,"too many values on second line");
    }
    char c;while(out.get(c))if(!std::isspace((unsigned char)c))quitf(_wa,"unexpected trailing content");
    // testlib also verifies that its registered output stream was consumed.
    ouf.readLine();ouf.readLine();if(!ouf.seekEof())quitf(_wa,"unexpected trailing content");
    quitf(_ok,exact<0?"impossibility verified":"count and all prefixes verified");
}
