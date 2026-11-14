$(function(){
 'use strict';
 const boot=JSON.parse(document.getElementById('review-bootstrap').textContent),opts=boot.options;
 let version=boot.version,saving=false,blocked=false,dirty=false,changes=0,mistakeCell=null;
 const status=$('#review-status');
 function message(t){status.text(t);}
 function changed(){dirty=true;changes++;message('有未保存的修改。');}
 function removeButton(){return $('<button type="button" class="review-remove" aria-label="删除此行"><i class="times icon"></i></button>');}
 function timeline(row){
  const tr=$('<tr class="tag line">');
  tr.append($('<td>').append($('<input class="time item" type="time" aria-label="开始时间">').val(row.time||'00:00')));
  for(const key of ['plan','achieve'])tr.append($('<td>').append($('<textarea rows="2" class="'+key+' item">').attr('aria-label',key==='plan'?'计划':'完成情况').val(row[key]||'')));
  tr.append($('<td>').append(removeButton()));tr.insertBefore($('.tag.table .add.line').closest('tr'));
 }
 function subtask(cell,row){
  const tr=$('<tr class="subtask line">');
  for(const key of ['actual','expected','total'])tr.append($('<td>').append($('<input type="number" min="0" max="100" step="any" class="'+key+' item">').attr('aria-label',{actual:'实际得分',expected:'预期得分',total:'满分'}[key]).val(row[key]===undefined?'':row[key])));
  tr.append($('<td>').append($('<input type="text" class="description item" aria-label="部分分描述">').val(row.description||'')));
  tr.append($('<td>').append(removeButton()));tr.insertBefore(cell.find('.add.line').closest('tr'));
 }
 for(const row of boot.data.timeline.length?boot.data.timeline:[{time:'00:00'}])timeline(row);
 $('tr.problem.line').each(function(){
  const tr=$(this),id=String(tr.data('pid')),data=boot.data.problems[id]||{};
  tr.find('.normal.item').each(function(){const icon=$(this).find('i'),key=icon.attr('data-name'),state=data.normal&&data.normal[key]||'';setNormal(icon,state);});
  tr.find('.mistake.items').text((data.mistakes||[]).join(' ')||'无');
  for(const key of ['rethink','other','guess_score'])tr.find('.'+key+'.item').val(data[key]===undefined?'':data[key]);
  for(const row of data.subtasks||[])subtask(tr.find('.subtask.items'),row);
 });
 function setNormal(icon,state){const entry=opts.normal_icons.find(x=>x.name===state);icon.attr('data-state',state).attr('class',(entry?entry.icon:'question circle')+' icon').attr('title',entry?entry.tooltip:'未填写');}
 $('.tooltip').popup();$('.modal.mistakes').modal({closable:false});
 $('#review-editor').on('input change','input,textarea',changed);
 $('#review-editor').on('click','.review-remove',function(){$(this).closest('tr').remove();changed();});
 $('.tag.table .add.line').attr({tabindex:0,role:'button'}).on('click',function(){
  let max=-30;$('.tag.line .time').each(function(){const v=$(this).val();if(v)max=Math.max(max,Number(v.slice(0,2))*60+Number(v.slice(3)));});
  const next=Math.min(max+30,1439);timeline({time:String(Math.floor(next/60)).padStart(2,'0')+':'+String(next%60).padStart(2,'0')});changed();
 });
 $('.subtask.items .add.line').attr({tabindex:0,role:'button'}).on('click',function(){subtask($(this).closest('.subtask.items'),{});changed();});
 $('.normal.item').attr({tabindex:0,role:'button'}).on('click',function(){const icon=$(this).find('i'),idx=opts.normal_icons.findIndex(x=>x.name===icon.attr('data-state'));setNormal(icon,opts.normal_icons[(idx+1)%4].name);changed();});
 $('.mistake.items').attr({tabindex:0,role:'button','aria-label':'选择检查2犯错情况'}).on('click',function(){
  mistakeCell=$(this);const selected=$(this).text().trim().split(/\s+/);
  $('.modal.mistakes input').each(function(){$(this).prop('checked',selected.includes(this.name));});$('.modal.mistakes').modal('show');
 });
 $('.modal.mistakes .positive').on('click',function(){if(!mistakeCell)return;const selected=$('.modal.mistakes input:checked').map(function(){return this.name;}).get();mistakeCell.text(selected.join(' ')||'无');changed();});
 $('#review-editor').on('keydown','[role=button]',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();$(this).click();}});
 function collect(){
  const data={timeline:[],problems:{}};
  $('.tag.line').each(function(){const row={};for(const k of ['time','plan','achieve'])row[k]=$(this).find('.'+k+'.item').val();data.timeline.push(row);});
  function number(input){const value=input.val();return value===''?'':Number(value);}
  $('tr.problem.line').each(function(){const tr=$(this),p={normal:{},mistakes:tr.find('.mistake.items').text().trim()==='无'?[]:tr.find('.mistake.items').text().trim().split(/\s+/),guess_score:number(tr.find('.guess_score')),subtasks:[],rethink:tr.find('.rethink').val(),other:tr.find('.other').val()};
   tr.find('.normal.item i').each(function(){p.normal[$(this).attr('data-name')]=$(this).attr('data-state')||'';});
   tr.find('tr.subtask.line').each(function(){const row={};for(const k of ['actual','expected','total'])row[k]=number($(this).find('.'+k));row.description=$(this).find('.description').val();p.subtasks.push(row);});data.problems[tr.data('pid')]=p;
  });return data;
 }
 function save(manual){
  if(saving||blocked||(!manual&&!dirty))return;
  const invalid=Array.from(document.querySelectorAll('#review-editor input')).find(x=>!x.checkValidity());if(invalid){invalid.reportValidity();message('请检查时间或分数格式。');return;}
  const data=collect(),snapshot=changes;saving=true;$('.save.button').addClass('loading').prop('disabled',true);message('正在保存…');
  $.ajax({url:location.pathname,method:'POST',contentType:'application/json',headers:{'X-Review-CSRF':boot.csrf},data:JSON.stringify({version,data}),success:function(r){version=r.version;dirty=changes!==snapshot;message((dirty?'已保存，仍有新的修改待保存。':'保存成功，保存时间：')+(dirty?'':new Date(r.saved_at).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'})));},error:function(xhr){if(xhr.status===409)blocked=true;message((xhr.responseJSON&&xhr.responseJSON.message)||'保存失败，内容尚未保存，请检查网络后重试。');},complete:function(){saving=false;$('.save.button').removeClass('loading').prop('disabled',false);}});
 }
 $('.save.button').on('click',()=>save(true));setInterval(()=>save(false),10000);
 window.addEventListener('beforeunload',function(e){if(dirty){e.preventDefault();e.returnValue='';}});
 message(boot.savedAt?'上次保存：'+new Date(boot.savedAt).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai'}):'尚未保存。');
});
