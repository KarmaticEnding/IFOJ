#include <bits/stdc++.h>
using namespace std;
// Exact hash-consing: collisions are resolved by comparing the full child pair.
// Node identifiers, not hash values, certify equal binary strings.
class Binary {
    struct Node{int left,right;};
    vector<Node>nodes;
    vector<uint64_t>keys;vector<int>ids;size_t used=0;
    static uint64_t hashKey(uint64_t x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
    void grow(){
        vector<uint64_t>oldKeys;vector<int>oldIds;oldKeys.swap(keys);oldIds.swap(ids);
        size_t capacity=oldIds.empty()?size_t(1<<18):oldIds.size()*2;keys.resize(capacity);ids.assign(capacity,0);
        for(size_t i=0;i<oldIds.size();i++)if(oldIds[i]){size_t p=hashKey(oldKeys[i])&(capacity-1);while(ids[p])p=(p+1)&(capacity-1);keys[p]=oldKeys[i];ids[p]=oldIds[i];}
    }
    int make(int l,int r){
        uint64_t key=(uint64_t(uint32_t(l))<<32)|uint32_t(r);size_t p=hashKey(key)&(ids.size()-1);
        while(ids[p]){if(keys[p]==key)return ids[p];p=(p+1)&(ids.size()-1);}
        if((used+1)*10>ids.size()*7){grow();p=hashKey(key)&(ids.size()-1);while(ids[p])p=(p+1)&(ids.size()-1);}
        int z=nodes.size();nodes.push_back({l,r});keys[p]=key;ids[p]=z;++used;return z;
    }
    int increment(int u,int h,int start,int x,bool&carry){
        if(!carry||start+(1<<h)<=x)return u;
        if(start>=x&&u==one[h])return zero[h];
        if(h==0){carry=false;return 1;}
        Node old=nodes[u];int mid=start+(1<<(h-1));
        if(x<mid)old.left=increment(old.left,h-1,start,x,carry);
        if(carry)old.right=increment(old.right,h-1,mid,x,carry);
        return make(old.left,old.right);
    }
public:
    int height;vector<int>zero,one;
    explicit Binary(int bits){height=0;while((1<<height)<bits)++height;nodes.reserve(1<<20);nodes.push_back({0,0});nodes.push_back({0,0});grow();zero.push_back(0);one.push_back(1);for(int h=1;h<=height;h++){zero.push_back(make(zero[h-1],zero[h-1]));one.push_back(make(one[h-1],one[h-1]));}}
    int empty()const{return zero[height];}
    int add(int root,int exponent){bool carry=true;int z=increment(root,height,0,exponent,carry);assert(!carry);return z;}
    bool less(int a,int b)const{
        if(a==b)return false;
        for(int h=height;h;--h){const Node A=nodes[a],B=nodes[b];if(A.right!=B.right){a=A.right;b=B.right;}else{a=A.left;b=B.left;}}
        return a<b;
    }
    size_t size()const{return nodes.size();}
};
#ifndef CLASSIC_NO_MAIN
struct Edge{int to,x,next;};struct Item{int vertex,root;};
struct Compare{const Binary*bits;bool operator()(const Item&a,const Item&b)const{if(a.root==b.root)return a.vertex>b.vertex;return bits->less(b.root,a.root);}};
int main(){
#if !defined(LOCAL) && !defined(__TUACK__)
    if(!freopen("classic.in","r",stdin))return 1;
    if(!freopen("classic.out","w",stdout))return 1;
#endif
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n,m;if(!(cin>>n>>m))return 0;vector<int>head(n,-1);vector<Edge>edges;edges.reserve(2*m);int maxX=0;
    auto insert=[&](int u,int v,int x){edges.push_back({v,x,head[u]});head[u]=edges.size()-1;};
    for(int i=0;i<m;i++){int u,v,x;cin>>u>>v>>x;--u;--v;insert(u,v,x);insert(v,u,x);maxX=max(maxX,x);}
    int s,t;cin>>s>>t;--s;--t;int extra=0;while((1LL<<extra)<n)++extra;
    Binary bits(maxX+extra+3);vector<int>dist(n,-1),parent(n,-1),px(n);vector<unsigned char>done(n);
    priority_queue<Item,vector<Item>,Compare>heap(Compare{&bits});dist[s]=bits.empty();heap.push({s,dist[s]});
    while(!heap.empty()){
        Item cur=heap.top();heap.pop();int u=cur.vertex;if(done[u]||dist[u]!=cur.root)continue;done[u]=1;if(u==t)break;
        for(int e=head[u];e!=-1;e=edges[e].next){int v=edges[e].to;if(done[v])continue;int d=bits.add(cur.root,edges[e].x);if(dist[v]<0||bits.less(d,dist[v])){dist[v]=d;parent[v]=u;px[v]=edges[e].x;heap.push({v,d});}}
    }
    if(!done[t]){cout<<-1<<'\n';return 0;}
    const int MOD=1000000007;vector<int>pow2(maxX+1,1);for(int i=1;i<=maxX;i++)pow2[i]=(pow2[i-1]*2LL)%MOD;
    vector<int>path;int answer=0;for(int v=t;v!=-1;v=parent[v]){path.push_back(v+1);if(parent[v]!=-1){answer+=pow2[px[v]];if(answer>=MOD)answer-=MOD;}}
    reverse(path.begin(),path.end());cout<<answer<<'\n'<<path.size()<<'\n';for(size_t i=0;i<path.size();i++)cout<<path[i]<<(i+1==path.size()?'\n':' ');
}
#endif
