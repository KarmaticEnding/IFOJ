#include <bits/stdc++.h>
using namespace std;
struct Query{int l,r,x,id,block;};
struct Change{int index,cell,block;};
int main(){
#if !defined(LOCAL) && !defined(__TUACK__)
	if(!freopen("span.in","r",stdin))return 1;
	if(!freopen("span.out","w",stdout))return 1;
#endif
	ios::sync_with_stdio(false);cin.tie(nullptr);
	int n,m;if(!(cin>>n>>m))return 0;
	const int INF=n+2;
	vector<int>a(n+2),count(n+2);
	for(int i=1;i<=n;i++){cin>>a[i];++count[a[i]];}
	// A globally absent/singleton value is always eligible because x>=1.
	int cap=1;while(count[cap]>=2)++cap;
	vector<int>pre(n+2),nxt(n+2,n+1),at(cap+1),head(cap+1,n+1);
	for(int i=1;i<=n;i++)if(a[i]<=cap){pre[i]=at[a[i]];if(pre[i])nxt[pre[i]]=i;else head[a[i]]=i;at[a[i]]=i;}
	int B=max(1,int(n/sqrt(double(max(m,1)))));long long sumX=0;
	vector<Query>qs(m);for(int i=0;i<m;i++){auto &q=qs[i];cin>>q.l>>q.r>>q.x;q.x=min(q.x,n);sumX+=q.x;q.id=i;q.block=(q.l-1)/B;}
	int C=max(1,int(sqrt(2.0*sumX/max(m,1))));
	sort(qs.begin(),qs.end(),[](const Query&a,const Query&b){if(a.block!=b.block)return a.block<b.block;return a.r>b.r;});
	vector<int>first(cap+1),last(cap+1),bucket(n+1,INF),low(n/C+1),bel(n+1),ans(m),touched;
	for(int s=0;s<=n;s++)bel[s]=s/C;
	vector<Change>history;history.reserve(B);
	int current=-1,R=n,base=1,cursor=1;
	auto put=[&](int s,int k,bool temporary){
		if(k>=bucket[s])return;
		int b=bel[s];if(temporary)history.push_back({s,bucket[s],low[b]});
		else if(bucket[s]==INF)touched.push_back(s);
		bucket[s]=k;low[b]=min(low[b],k);
	};
	for(const Query&q:qs){
		if(q.block!=current){
			current=q.block;base=current*B+1;R=n;
			while(cursor<base){int k=a[cursor];if(k<=cap)head[k]=nxt[cursor];++cursor;}
			first=head;last=at;
			for(int s:touched)bucket[s]=INF;touched.clear();fill(low.begin(),low.end(),INF);
			for(int k=1;k<=cap;k++)put(first[k]<=last[k]?last[k]-first[k]+1:0,k,false);
		}
		while(R>q.r){int k=a[R];if(k<=cap){last[k]=pre[R];put(first[k]<=last[k]?last[k]-first[k]+1:0,k,false);}--R;}
		// Only decreasing spans are inserted. Older records remain valid witnesses.
		history.clear();
		for(int p=base;p<q.l;p++){int k=a[p];if(k<=cap){first[k]=nxt[p];put(first[k]<=last[k]?last[k]-first[k]+1:0,k,true);}}
		int ret=INF,b=bel[q.x];
		for(int j=0;j<b;j++)ret=min(ret,low[j]);
		for(int s=b*C;s<=q.x;s++)ret=min(ret,bucket[s]);
		ans[q.id]=ret;
		for(auto it=history.rbegin();it!=history.rend();++it){bucket[it->index]=it->cell;low[bel[it->index]]=it->block;}
		for(int p=q.l-1;p>=base;p--)if(a[p]<=cap)first[a[p]]=p;
	}
	for(int x:ans)cout<<x<<'\n';
}
