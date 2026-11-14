// Per-user practice access; never changes a problem's global publication flag.
const TypeORM=require('typeorm');
async function hasFinishedContest(contest,user){
  if(!user||!contest.isEnded())return false;
  return await syzoj.model('judge_state').count({user_id:user.id,type:1,type_info:contest.id,
    submit_time:TypeORM.Between(contest.start_time,contest.end_time)})>0;
}
async function getProblemIds(user){
  if(!user)return [];
  const rows=await syzoj.model('contest').createQueryBuilder('contest')
    .innerJoin(syzoj.model('judge_state'),'submission',
      'submission.type = 1 AND submission.type_info = contest.id AND submission.user_id = :uid AND submission.submit_time >= contest.start_time AND submission.submit_time <= contest.end_time',{uid:user.id})
    .where('contest.end_time <= :now',{now:syzoj.utils.getCurrentDate()})
    .select('DISTINCT(contest.problems)','problems').getRawMany();
  return [...new Set(rows.flatMap(row=>String(row.problems||'').split('|').map(Number)).filter(id=>Number.isSafeInteger(id)&&id>0))];
}
async function hasProblem(id,user){return (await getProblemIds(user)).includes(id);}
module.exports={hasFinishedContest,getProblemIds,hasProblem};
