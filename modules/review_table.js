const crypto=require('crypto');
const Review=syzoj.model('review_table'),Contest=syzoj.model('contest'),User=syzoj.model('user'),Problem=syzoj.model('problem');
const options=require('../libs/review_options.json');
const validMistakes=new Set(Object.keys(options.mistakes).flatMap(k=>Object.keys(options.mistakes[k]).map(n=>k+n)));
function fail(message,status=400){const e=new ErrorMessage(message);e.status=status;throw e;}
function text(value,max=10000){if(typeof value!=='string'||value.length>max)fail('文本格式不正确或过长。');return value;}
function score(value){if(value===''||value===null)return '';if(typeof value!=='number'||!Number.isFinite(value)||value<0||value>100)fail('分数必须在 0 到 100 之间。');return value;}
function validate(data,ids){
 if(!data||!Array.isArray(data.timeline)||data.timeline.length>200||!data.problems||typeof data.problems!=='object'||Array.isArray(data.problems))fail('复盘表格式不正确。');
 if(Buffer.byteLength(JSON.stringify(data))>512*1024)fail('复盘表内容过大。');
 const result={timeline:data.timeline.map(row=>{if(!row||!/^([01]\d|2[0-3]):[0-5]\d$/.test(row.time))fail('开始时间应为小时:分钟。');return{time:row.time,plan:text(row.plan),achieve:text(row.achieve)};}),problems:{}};
 if(Object.keys(data.problems).some(id=>!ids.includes(Number(id))))fail('复盘表包含本场比赛以外的题目。');
 for(const id of ids){
  const p=data.problems[id];if(!p||!p.normal||!Array.isArray(p.mistakes)||!Array.isArray(p.subtasks)||p.subtasks.length>100)fail('题目复盘内容不完整。');
  const normal={};for(const key of options.normal_items.map(x=>x.name)){const state=p.normal[key];if(!['','done','not_need','forget','skip'].includes(state))fail('常规检查状态无效。');normal[key]=state;}
  if(p.mistakes.some(x=>!validMistakes.has(x)))fail('检查2选项无效。');
  result.problems[id]={normal,mistakes:[...new Set(p.mistakes)],guess_score:score(p.guess_score),rethink:text(p.rethink),other:text(p.other),subtasks:p.subtasks.map(s=>({actual:score(s.actual),expected:score(s.expected),total:score(s.total),description:text(s.description,2000)}))};
 }
 return result;
}
async function context(req,res,editing=true){
 if(!/^[1-9]\d*$/.test(req.params.id)||!/^[1-9]\d*$/.test(req.params.uid))fail('无效的比赛或用户编号。',404);
 const contest=await Contest.findById(Number(req.params.id)),target=await User.findById(Number(req.params.uid));
 if(!contest||!target)fail('无此比赛或用户。',404);
 const admin=await contest.isSupervisior(res.locals.user);
 if(editing&&!admin&&(!res.locals.user||res.locals.user.id!==target.id))fail('您没有权限编辑此复盘表。',403);
 if(!contest.is_public&&!admin)fail('比赛未公开。',403);
 if(!contest.isEnded())fail('比赛结束后才能填写复盘表。',403);
 const ids=await contest.getProblems();return{contest,target,ids,canEdit:admin||res.locals.user.id===target.id};
}
const route='/contest/:id/review_table/:uid/edit';
app.get(route,async(req,res)=>{
 try{
  const {contest,target,ids}=await context(req,res);
  const record=await Review.findOne({contest_id:contest.id,user_id:target.id});
  if(!req.session.reviewToken)req.session.reviewToken=crypto.randomBytes(32).toString('hex');
  const problems=await Promise.all(ids.map(id=>Problem.findById(id)));if(problems.some(x=>!x))fail('比赛题目不存在。',404);
  res.set('Cache-Control','private, no-store');
  res.render('review_table_edit',{contest,target,problems,review:record?record.data:{timeline:[],problems:{}},version:record?record.version:0,savedAt:record?record.saved_at:null,csrf:req.session.reviewToken,reviewOptions:options});
 }catch(e){res.status(e.status||500).render('error',{err:e});}
});
app.post(route,async(req,res)=>{
 res.set('Cache-Control','no-store');
 try{
  const {contest,target,ids}=await context(req,res);
  const token=req.get('X-Review-CSRF');
  if(!token||token!==req.session.reviewToken)fail('页面已过期，请刷新后重试。',403);
  if(!Number.isSafeInteger(req.body.version)||req.body.version<0)fail('保存版本无效。');
  const data=validate(req.body.data,ids),version=req.body.version+1,saved_at=new Date().toISOString();
  if(req.body.version===0){
   try{await Review.insert({contest_id:contest.id,user_id:target.id,data,version,saved_at});}
   catch(e){if(e.code==='ER_DUP_ENTRY')fail('复盘表已被其他窗口修改，请刷新后合并内容再保存。',409);throw e;}
  }else{
   const update=await Review.createQueryBuilder().update().set({data,version,saved_at}).where('contest_id = :cid AND user_id = :uid AND version = :version',{cid:contest.id,uid:target.id,version:req.body.version}).execute();
   if(update.raw.affectedRows!==1)fail('复盘表已被其他窗口修改，请刷新后合并内容再保存。',409);
  }
  res.json({success:true,version,saved_at});
 }catch(e){syzoj.log(e);res.status(e.status||500).json({success:false,message:e instanceof ErrorMessage?e.message:'保存失败，请稍后重试。'});}
});

app.get('/contest/:id/review_table',async(req,res)=>{
 res.set('Cache-Control','private, no-store');
 try{
  const contest=await Contest.findById(Number(req.params.id));
  if(!contest)fail('无此比赛。',404);
  if(!contest.is_public&&!await contest.isSupervisior(res.locals.user))fail('比赛未公开。',403);
  if(!contest.isEnded())fail('比赛结束后才能查看复盘表。',403);
  const paginate=syzoj.utils.paginate(await Review.count({contest_id:contest.id}),req.query.page,50);
  const records=await Review.find({where:{contest_id:contest.id},order:{saved_at:'DESC'},skip:(paginate.currPage-1)*50,take:50});
  const entries=await Promise.all(records.map(async row=>({row,owner:await User.findById(row.user_id)})));
  res.render('review_table_list',{contest,entries,paginate});
 }catch(e){res.status(e.status||500).render('error',{err:e});}
});
app.get('/contest/:id/review_table/:uid',async(req,res)=>{
 res.set('Cache-Control','private, no-store');
 try{
  const {contest,target,ids,canEdit}=await context(req,res,false);
  const record=await Review.findOne({contest_id:contest.id,user_id:target.id});
  if(!record)fail('该用户尚未填写本场比赛的复盘表。',404);
  const problems=await Promise.all(ids.map(id=>Problem.findById(id)));
  res.render('review_table_view',{contest,target,problems,review:record.data,savedAt:record.saved_at,reviewOptions:options,canEdit});
 }catch(e){res.status(e.status||500).render('error',{err:e});}
});
