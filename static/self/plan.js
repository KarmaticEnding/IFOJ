$(function(){
 'use strict';
 const page=document.getElementById('plan-page');if(!page)return;
 const tbody=document.getElementById('plan-rows'),modal=document.getElementById('plan-editor'),form=document.getElementById('plan-form'),status=document.getElementById('plan-save-status');
 const navigationStatus=document.getElementById('plan-navigation-status'),keys=['description','completion','comment'];
 let current=null,original=null,saving=false,loading=false;
 const serverTime=Number(page.dataset.serverTime),openedAt=performance.now();
 function descriptionLocked(date){return page.dataset.admin!=='1'&&date<=new Date(serverTime+performance.now()-openedAt+8*3600000).toISOString().slice(0,10);}
 function applyDescriptionLock(){const locked=descriptionLocked(current.dataset.date);form.elements.description.readOnly=locked;form.elements.description.classList.toggle('plan-description-locked',locked);document.getElementById('plan-description-lock').hidden=!locked;}
 function content(row){return Object.fromEntries(keys.map(key=>[key,row.querySelector('[data-field="'+key+'"]').textContent]));}
 function fields(){return Object.fromEntries(keys.map(key=>[key,form.elements[key].value]));}
 function dirty(){return !!current&&JSON.stringify(fields())!==JSON.stringify(original);}
 function measure(row){const long=[...row.querySelectorAll('.plan-cell')].some(cell=>cell.scrollHeight>182),button=row.querySelector('.plan-toggle');row.classList.toggle('plan-long',long);button.hidden=!long;if(!long)row.classList.remove('plan-expanded');button.setAttribute('aria-expanded',String(row.classList.contains('plan-expanded')));button.textContent=row.classList.contains('plan-expanded')?'收起':'展开';}
 function close(){current=null;original=null;}
 async function save(){
  if(!current||saving)return;applyDescriptionLock();saving=true;status.textContent='正在保存…';const row=current,snapshot=fields();$('#plan-editor .positive').addClass('loading disabled');$('#plan-editor .cancel').addClass('disabled');form.querySelectorAll('textarea').forEach(el=>el.disabled=true);
  try{
   const response=await fetch('/schedule/'+page.dataset.user+'/entry',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json','X-Plan-CSRF':page.dataset.csrf},body:JSON.stringify({...snapshot,date:row.dataset.date,kind:row.dataset.kind,version:Number(row.dataset.version)})});
   const data=await response.json();if(!response.ok||!data.success)throw Error(data.message||'保存失败，请稍后重试。');
   for(const key of keys)row.querySelector('[data-field="'+key+'"]').textContent=snapshot[key];row.dataset.version=data.version;measure(row);close();$('#plan-editor').modal('hide');
  }catch(e){status.textContent=e.message+'\n当前输入仍保留，可重试或取消。';}
  finally{saving=false;$('#plan-editor .button').removeClass('loading disabled');form.querySelectorAll('textarea').forEach(el=>el.disabled=false);}
 }
 if(modal){$(modal).modal({closable:false,onApprove:()=>{save();return false;},onDeny:()=>{if(saving)return false;close();},onHidden:close});form.addEventListener('submit',event=>{event.preventDefault();save();});}
 tbody.addEventListener('click',event=>{
  const toggle=event.target.closest('.plan-toggle');if(toggle){const row=toggle.closest('.plan-row');row.classList.toggle('plan-expanded');measure(row);return;}
  const cell=event.target.closest('.plan-item');if(!cell||!modal)return;current=cell.closest('.plan-row');original=content(current);keys.forEach(key=>form.elements[key].value=original[key]);applyDescriptionLock();status.textContent='';document.getElementById('plan-edit-date').textContent=current.querySelector('.plan-date>span').textContent;$(modal).modal('show');
 });
 function add(date,n){return new Date(Date.parse(date+'T00:00:00Z')+n*86400000).toISOString().slice(0,10);}
 document.querySelectorAll('.plan-navigation a').forEach(link=>link.addEventListener('click',async event=>{
  event.preventDefault();if(loading)return;loading=true;const earlier=link.dataset.direction==='earlier';navigationStatus.textContent='加载中…';
  const start=earlier?add(page.dataset.start,-7):add(page.dataset.end,1),end=earlier?add(page.dataset.start,-1):add(page.dataset.end,7);
  try{const response=await fetch('/schedule/'+page.dataset.user+'/rows?start='+start+'&end='+end,{credentials:'same-origin'}),data=await response.json();if(!response.ok||!data.success)throw Error(data.message||'加载失败，请重试。');const anchor=earlier?tbody.firstElementChild:null,top=anchor?anchor.getBoundingClientRect().top:0;tbody.insertAdjacentHTML(earlier?'afterbegin':'beforeend',data.html);if(earlier)page.dataset.start=start;else page.dataset.end=end;tbody.querySelectorAll('.plan-row').forEach(measure);if(anchor)document.body.scrollTop+=anchor.getBoundingClientRect().top-top;navigationStatus.textContent='';}
  catch(e){navigationStatus.textContent=e.message;}finally{loading=false;}
 }));
 const measureAll=()=>tbody.querySelectorAll('.plan-row').forEach(measure);measureAll();window.addEventListener('resize',measureAll);if(document.fonts)document.fonts.ready.then(measureAll);
 window.addEventListener('beforeunload',event=>{if(saving||dirty()){event.preventDefault();event.returnValue='';}});
});
