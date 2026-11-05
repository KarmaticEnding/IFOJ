// Official checker: dense bitmaps, independent of the downloadable hash checker.
// Four arguments: ordinary testlib checker. Seven arguments: tuack/Lemon adapter.
#include "testlib.h"
#include <vector>
#include <cstdio>
#include <cstdlib>
#if !defined(_WIN32)
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#endif
static int checkRoute(int argc,char**argv){
    registerTestlibCmd(argc,argv);
    const int n=inf.readInt(1,1000000,"n"),m=inf.readInt(1,1000000,"m");
    ensuref(1LL*n*m<=1000000,"invalid grid");
    const int total=n*m,stride=2*m-1;
    std::vector<unsigned char> visited(total),used((2*n-1)*stride);
    int previousRow=0,previousColumn=0;
    for(int step=0;step<total;++step){
        int row=ouf.readInt(-1,n,"x");
        if(row==-1&&step==0)quitf(_wa,"incorrect impossibility claim");
        if(row<=0)quitf(_wa,"invalid row");
        int column=ouf.readInt(1,m,"y");
        if(step==0&&(row!=1||column!=1))quitf(_wa,"incorrect start");
        int cell=(row-1)*m+column-1;
        if(visited[cell])quitf(_wa,"repeated cell at step %d",step+1);
        visited[cell]=1;
        if(step){
            int dx=row-previousRow,dy=column-previousColumn;
            int key=(dx+n-1)*stride+dy+m-1;
            if(used[key])quitf(_wa,"repeated displacement at jump %d",step);
            used[key]=1;
        }
        previousRow=row;previousColumn=column;
    }
    if(!ouf.seekEof())quitf(_wa,"trailing output");
    quitf(_ok,"valid route");
}
int main(int argc,char**argv){
    if(argc!=7)return checkRoute(argc,argv);
#if !defined(_WIN32)
    disableFinalizeGuard();
    // Isolate testlib's normal exit handling; never change or replace testlib.h.
    FILE *scoreFile=fopen(argv[5],"w");
    if(!scoreFile)return 3;
    double fullScore=100;
    if(FILE *f=fopen(argv[4],"r")){if(fscanf(f,"%lf",&fullScore)!=1)fullScore=100;fclose(f);}
    else fullScore=strtod(argv[4],nullptr);
    pid_t pid=fork();
    if(pid==0){
        int fd=open(argv[6],O_WRONLY|O_CREAT|O_TRUNC,0644);
        if(fd<0)_exit(3);
        dup2(fd,STDERR_FILENO);close(fd);
        char* args[]={argv[0],argv[1],argv[2],argv[3],nullptr};
        checkRoute(4,args);_exit(3);
    }
    int status=0;bool accepted=pid>0&&waitpid(pid,&status,0)==pid&&WIFEXITED(status)&&WEXITSTATUS(status)==0;
    fprintf(scoreFile,"%.6f\n",accepted?fullScore:0.0);fclose(scoreFile);
    return 0;
#else
    fprintf(stderr,"The 7-argument tuack adapter requires Linux. Use the normal 3-file interface on Windows.\n");
    return 3;
#endif
}
