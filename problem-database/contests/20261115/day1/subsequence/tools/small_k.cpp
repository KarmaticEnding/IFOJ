#include <bits/stdc++.h>
using namespace std;
int main(){
 int n,k;string s,t;cin>>n>>k>>s>>t;assert(k<=2);
 auto value=[&](){int a=0,v=0;for(char c:s){if(c==t[1])v+=a;if(c==t[0])a++;}return v;};
 int best=value();string alphabet=t;sort(alphabet.begin(),alphabet.end());alphabet.erase(unique(alphabet.begin(),alphabet.end()),alphabet.end());
 if(k)for(int i=0;i<n;i++)for(char a:alphabet){char old=s[i];s[i]=a;best=max(best,value());if(k==2)for(int j=i+1;j<n;j++)for(char b:alphabet){char save=s[j];s[j]=b;best=max(best,value());s[j]=save;}s[i]=old;}
 cout<<best<<'\n';
}
