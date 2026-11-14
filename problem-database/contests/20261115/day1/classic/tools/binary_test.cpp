#define CLASSIC_NO_MAIN
#include "../GPT/classic.cpp"
#include <boost/multiprecision/cpp_int.hpp>
using boost::multiprecision::cpp_int;
int main(){
 Binary bits(100100);vector<int>roots(1,bits.empty());vector<cpp_int>values(1,0);mt19937 rng(464265);
 for(int i=0;i<5000;i++){int old=rng()%roots.size(),x=i%37==0?100000:int(rng()%6000);roots.push_back(bits.add(roots[old],x));values.push_back(values[old]+(cpp_int(1)<<x));for(int j=0;j<3;j++){int a=rng()%roots.size(),b=rng()%roots.size();assert(bits.less(roots[a],roots[b])==(values[a]<values[b]));assert((roots[a]==roots[b])==(values[a]==values[b]));}}
 int base=bits.empty();cpp_int exact=0;for(int i=0;i<5000;i++){base=bits.add(base,i);exact+=cpp_int(1)<<i;}
 int expected=bits.add(base,0);for(int i=0;i<2000;i++)assert(bits.add(base,0)==expected);assert(exact+1==(cpp_int(1)<<5000));
 assert(bits.less(base,expected));cout<<"binary operations verified; nodes="<<bits.size()<<'\n';
}
