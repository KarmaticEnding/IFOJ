const DAY=86400000;
function valid(date){
 if(typeof date!=='string'||!/^20\d{2}-\d{2}-\d{2}$/.test(date))return false;
 const n=Date.parse(date+'T00:00:00Z');return Number.isFinite(n)&&new Date(n).toISOString().slice(0,10)===date;
}
function add(date,days){return new Date(Date.parse(date+'T00:00:00Z')+days*DAY).toISOString().slice(0,10);}
function monday(date){const day=new Date(date+'T00:00:00Z').getUTCDay();return add(date,-((day+6)%7));}
function today(){return new Date(Date.now()+8*3600000).toISOString().slice(0,10);}
function range(start){return Array.from({length:4},(_,i)=>{const date=add(start,i*7);return{date,end:add(date,6),days:Array.from({length:7},(_,j)=>add(date,j))};});}
function entries(start,end){const result=[];for(let date=start;date<=end;date=add(date,1)){if(monday(date)===date)result.push({date,kind:'week',label:date+' ~ '+add(date,6)+' 周计划'});result.push({date,kind:'day',label:date});}return result;}
module.exports={valid,add,monday,today,range,entries};
