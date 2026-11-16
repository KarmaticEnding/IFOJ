const crypto=require('crypto'),calendar=require('../libs/plan_calendar');
const Entry=syzoj.model('plan_entry'),User=syzoj.model('user');
function fail(message,status=400){const e=new ErrorMessage(message);e.status=status;throw e;}
async function context(req,res){
 if(!/^[1-9]\d*$/.test(req.params.uid))fail('用户编号无效。',404);
 const target=await User.findById(Number(req.params.uid));if(!target)fail('无此用户。',404);
 const canEdit=!!res.locals.user&&(target.id===res.locals.user.id||!!res.locals.user.is_admin);
 return {target,canEdit};
}
function validate(body){
 if(!body||!calendar.valid(body.date)||!['day','week'].includes(body.kind))fail('日期或计划类型无效。');
 if(body.kind==='week'&&calendar.monday(body.date)!==body.date)fail('周计划须从星期一开始。');
 if(!Number.isSafeInteger(body.version)||body.version<0||body.version>=2147483647)fail('保存版本无效。');
 const result={};for(const key of ['description','completion','comment']){
  if(typeof body[key]!=='string'||Buffer.byteLength(body[key],'utf8')>60000)fail('每栏内容不能超过 60000 字节。');result[key]=body[key];
 }
 return result;
}
app.get('/schedule',(req,res)=>res.redirect('/schedule/'+res.locals.user.id));
app.get('/schedule/:uid',async(req,res)=>{
 res.set('Cache-Control','private, no-store');
 try{
  const {target,canEdit}=await context(req,res);
  if(req.query.start&&!calendar.valid(req.query.start))fail('起始日期无效。');
  const start=calendar.monday(req.query.start||calendar.add(calendar.today(),-7));
  const end=calendar.add(start,21),entries=calendar.entries(start,end);
  const rows=await Entry.createQueryBuilder().where('user_id=:uid',{uid:target.id}).andWhere('date>=:start AND date<=:end',{start,end}).getMany();
  const records={};for(const row of rows)records[row.kind+':'+row.date]=row;
  if(!req.session.planToken)req.session.planToken=crypto.randomBytes(32).toString('hex');
  res.render('plan',{target,canEdit,entries,records,start,end,previous:calendar.add(start,-7),next:calendar.add(end,1),csrf:canEdit?req.session.planToken:''});
 }catch(e){syzoj.log(e);res.status(e.status||500).render('error',{err:e});}
});
app.get('/schedule/:uid/rows',async(req,res)=>{
 res.set('Cache-Control','private, no-store');
 try{
  const {target,canEdit}=await context(req,res),start=req.query.start,end=req.query.end;
  if(!calendar.valid(start)||!calendar.valid(end)||start>end||end>calendar.add(start,30))fail('加载的日期范围无效。');
  const rows=await Entry.createQueryBuilder().where('user_id=:uid',{uid:target.id}).andWhere('date>=:start AND date<=:end',{start,end}).getMany(),records={};
  for(const row of rows)records[row.kind+':'+row.date]=row;
  res.render('plan_rows',{target,canEdit,entries:calendar.entries(start,end),records},(error,html)=>{
   if(error){syzoj.log(error);res.status(500).json({success:false,message:'加载失败，请稍后重试。'});return;}
   res.json({success:true,start,end,html});
  });
 }catch(e){syzoj.log(e);res.status(e.status||500).json({success:false,message:e instanceof ErrorMessage?e.message:'加载失败，请稍后重试。'});}
});
app.post('/schedule/:uid/entry',async(req,res)=>{
 res.set('Cache-Control','no-store');
 try{
  const {target,canEdit}=await context(req,res);if(!canEdit)fail('您没有权限编辑此计划。',403);
  if(!req.get('X-Plan-CSRF')||req.get('X-Plan-CSRF')!==req.session.planToken)fail('页面已过期，请刷新后重试。',403);
  const data=validate(req.body),version=req.body.version+1,saved_at=new Date().toISOString();
  const key={user_id:target.id,date:req.body.date,kind:req.body.kind};
  if(req.body.version===0){
   try{await Entry.insert({...key,...data,version,saved_at});}
   catch(e){if(e.code==='ER_DUP_ENTRY')fail('此计划已被其他窗口修改，请保留当前内容，刷新后合并。',409);throw e;}
  }else{
   const update=await Entry.createQueryBuilder().update().set({...data,version,saved_at}).where('user_id=:uid AND date=:date AND kind=:kind AND version=:version',{uid:target.id,date:key.date,kind:key.kind,version:req.body.version}).execute();
   if(update.raw.affectedRows!==1)fail('此计划已被其他窗口修改，请保留当前内容，刷新后合并。',409);
  }
  res.json({success:true,version,saved_at});
 }catch(e){syzoj.log(e);res.status(e.status||500).json({success:false,message:e instanceof ErrorMessage?e.message:'保存失败，请稍后重试。'});}
});
