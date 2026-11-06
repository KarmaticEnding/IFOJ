const fs=require('fs-extra');
const path=require('path');
const crypto=require('crypto');
const {spawn}=require('child_process');
const yaml=require('js-yaml');
const lock=new (require('async-lock'))();
const {getProject}=require('./problem_source');

async function sourceFiles(contest) {
  const ids=await contest.getProblems();
  if(!ids.length)throw new ErrorMessage('本场比赛没有题目。');
  const days=new Map();
  for(const id of ids){
    const project=await getProject(id);
    if(!project)throw new ErrorMessage('比赛题目未关联 tuack 工程。');
    const day=path.dirname(project.directory);
    const config=yaml.load(await fs.readFile(path.join(day,'conf.yaml'),'utf8'));
    if(config.folder!=='day')throw new ErrorMessage('题目不属于完整的 tuack 比赛日工程。');
    if(!days.has(day))days.set(day,{config,projects:[]});
    days.get(day).projects.push(project);
  }
  const files=[];const names=new Set();
  async function add(source,name,boundary){
    const stat=await fs.lstat(source);
    const resolved=await fs.realpath(source);
    if(stat.isSymbolicLink()||!stat.isFile()||!resolved.startsWith(boundary+path.sep))throw new ErrorMessage('下发文件包含不支持的路径或文件类型。');
    if(names.has(name))throw new ErrorMessage('下发文件名称重复。');
    names.add(name);files.push({source:resolved,name});
  }
  for(const [day,{config,projects}] of days){
    const expected=config.subdir||[];
    if(JSON.stringify(expected)!==JSON.stringify(projects.map(p=>path.basename(p.directory))))throw new ErrorMessage('比赛题目顺序与 tuack 比赛日配置不一致，无法使用完整 PDF 题面打包。');
    const contestRoot=await fs.realpath(path.dirname(day));
    const name=config.name;
    if(typeof name!=='string'||! /^[a-zA-Z0-9_-]+$/.test(name))throw new ErrorMessage('比赛日名称无效。');
    const pdf=path.join(contestRoot,'statements','noi',name+'.pdf');
    if(!await fs.pathExists(pdf))throw new ErrorMessage('请先在 tuack 工程中生成本比赛日的 NOI 格式 PDF 题面。');
    const prefix=days.size>1?name+'/':'';
    await add(pdf,prefix+name+'.pdf',contestRoot);
    for(const project of projects){
      if(typeof project.config.name!=='string'||! /^[a-zA-Z0-9_-]+$/.test(project.config.name))throw new ErrorMessage('题目名称无效。');
      const down=path.join(project.directory,'down');
      if(!await fs.pathExists(down))continue;
      const downStat=await fs.lstat(down);
      if(downStat.isSymbolicLink()||!downStat.isDirectory())throw new ErrorMessage('下发目录类型无效。');
      async function walk(directory,relative){
        for(const entry of (await fs.readdir(directory)).sort()){
          const file=path.join(directory,entry),stat=await fs.lstat(file);
          if(stat.isSymbolicLink())throw new ErrorMessage('下发目录不允许包含符号链接。');
          if(stat.isDirectory())await walk(file,relative+entry+'/');
          else await add(file,prefix+project.config.name+'/'+relative+entry,project.directory);
        }
      }
      await walk(down,'');
    }
  }
  return files;
}

async function prepare(contest) {
  if(!contest.package_password)throw new ErrorMessage('本场比赛尚未设置下发包解压密码，请联系管理员。');
  return lock.acquire(String(contest.id),async()=>{
    const files=await sourceFiles(contest);
    const digest=crypto.createHmac('sha256',syzoj.config.session_secret);
    digest.update(JSON.stringify({format:'outer-aes-v2',id:contest.id,password:contest.package_password}));
    for(const file of files){digest.update(file.name+'\0');digest.update(await fs.readFile(file.source));}
    const cache=syzoj.utils.resolvePath(syzoj.config.upload_dir,'contest-packages');
    await fs.ensureDir(cache);await fs.chmod(cache,0o700);
    const destination=path.join(cache,contest.id+'-'+digest.digest('hex')+'.zip');
    if(await fs.pathExists(destination))return destination;
    const scratch=await fs.mkdtemp(path.join(cache,'.build-'));
    await fs.chmod(scratch,0o700);
    const output=path.join(scratch,'contest.zip');
    try{
      await new Promise((resolve,reject)=>{
        const child=spawn('python3',['-B',path.join(__dirname,'../bin/build-contest-package.py')],{stdio:['pipe','ignore','ignore']});
        const timer=setTimeout(()=>{child.kill('SIGKILL');reject(new ErrorMessage('下发包生成超时，请稍后重试。'));},180000);
        child.on('error',e=>{clearTimeout(timer);reject(e);});
        child.on('close',code=>{clearTimeout(timer);code===0?resolve():reject(new ErrorMessage('下发包生成失败，请联系管理员。'));});
        child.stdin.on('error',()=>{});
        child.stdin.end(JSON.stringify({password:contest.package_password,files,destination:output}));
      });
      await fs.rename(output,destination);return destination;
    }finally{await fs.remove(scratch);}
  },{maxPending:8});
}

module.exports={prepare,sourceFiles};
