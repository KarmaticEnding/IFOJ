#include <cstdio>
struct Output {
    char data[1 << 16]; int used=0;
    ~Output(){flush();}
    void flush(){if(used)fwrite(data,1,used,stdout);used=0;}
    void put(char c){if(used==(1<<16))flush();data[used++]=c;}
    void number(int x){char s[12];int k=0;do{s[k++]=char('0'+x%10);x/=10;}while(x);while(k)put(s[--k]);}
    void point(int x,int y){number(x);put(' ');number(y);put('\n');}
};
int main(){
#if !defined(__TUACK__) && !defined(LOCAL)
    if(!freopen("vector.in","r",stdin))return 1;
    if(!freopen("vector.out","w",stdout))return 1;
#endif
    int n,m;if(scanf("%d%d",&n,&m)!=2)return 1;
    Output out;
    for(int i=1;i<=n/2;i++)for(int j=1;j<=m;j++){
        out.point(i,j);out.point(n-i+1,m-j+1);
    }
    if(n%2){int l=1,r=m;while(l<=r){out.point(n/2+1,l++);if(l<=r)out.point(n/2+1,r--);}}
}
