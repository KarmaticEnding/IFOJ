// Official checker: trusts the count-only jury answer, checks each prefix with 128-bit products.
#include "testlib.h"
#include <vector>
#include <sstream>
#include <cstdio>
#include <cstdlib>
#if !defined(_WIN32)
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#endif
const long long LIMIT=1000000000000000000LL,MOD=100000007;
static long long single(const std::string&line){
    std::istringstream in(line);long long v;std::string extra;
    if(!(in>>v)||(in>>extra))quitf(_wa,"the first line must contain exactly one integer");return v;
}
static int check(int argc,char**argv){
    registerTestlibCmd(argc,argv);
    int n=inf.readInt(1,1000000,"n");std::vector<long long>b(n);for(auto &v:b)v=inf.readLong(1,LIMIT,"b");
    long long expected=ans.readLong(-1,MOD-1,"count");if(!ans.seekEof())quitf(_fail,"jury answer must contain only the count");
    long long reported=single(ouf.readLine());
    if(reported!=expected)quitf(_wa,"wrong count: expected %lld, found %lld",expected,reported);
    std::istringstream row(ouf.readLine());long long v;
    if(expected==-1){if(!(row>>v)||v!=-1)quitf(_wa,"impossible instances require a second line containing -1");}
    else{
        long long low=LIMIT,high=0;
        for(int i=0;i<n;i++){
            if(!(row>>v)||v<1||v>LIMIT)quitf(_wa,"invalid or missing a[%d]",i+1);
            low=std::min(low,v);high=std::max(high,v);
            if((__int128)low*high!=b[i])quitf(_wa,"prefix %d violates max * min = b_i",i+1);
        }
    }
    std::string extra;if(row>>extra)quitf(_wa,"extra token on second line");
    if(!ouf.seekEof())quitf(_wa,"extra output after the second line");
    quitf(_ok,expected==-1?"correct impossibility":"correct count and construction");
}
int main(int argc,char**argv){
    if(argc!=7)return check(argc,argv);
#if !defined(_WIN32)
    disableFinalizeGuard();FILE*score=fopen(argv[5],"w");if(!score)return 3;
    double full=100;if(FILE*f=fopen(argv[4],"r")){if(fscanf(f,"%lf",&full)!=1)full=100;fclose(f);}else full=strtod(argv[4],nullptr);
    pid_t pid=fork();if(pid==0){int fd=open(argv[6],O_WRONLY|O_CREAT|O_TRUNC,0644);if(fd<0)_exit(3);dup2(fd,STDERR_FILENO);close(fd);char*args[]={argv[0],argv[1],argv[2],argv[3],nullptr};check(4,args);_exit(3);}
    int status=0;bool ok=pid>0&&waitpid(pid,&status,0)==pid&&WIFEXITED(status)&&WEXITSTATUS(status)==0;
    fprintf(score,"%.6f\n",ok?full:0.0);fclose(score);return 0;
#else
    fprintf(stderr,"Use the ordinary input/output/answer interface on Windows.\n");return 3;
#endif
}
