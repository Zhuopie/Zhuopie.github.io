(() => {
  'use strict';
  const API='https://zhuopie-guestbook.frolickingpancake3.chatgpt.site';
  const form=document.getElementById('guestbook-form');if(!form)return;
  const status=document.getElementById('guestbook-status'),list=document.getElementById('guestbook-comments'),more=document.getElementById('guestbook-more');
  const read=(key)=>{try{return localStorage.getItem(key);}catch{return null;}};
  const save=(key,value)=>{try{localStorage.setItem(key,value);}catch{/* In-memory fallback still works. */}};
  let visitor=read('zhuopie-guestbook-visitor');
  if(!visitor || !/^[a-f0-9-]{36}$/i.test(visitor)){visitor=crypto.randomUUID();save('zhuopie-guestbook-visitor',visitor);}
  const states={visit:read('zhuopie-reaction-visit')==='true',like:read('zhuopie-reaction-like')==='true'};
  let next=null,challenge=null,challengeAt=0,challengePromise=null;
  async function api(path,body){const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),15000);try{const r=await fetch(API+path,{method:body?'POST':'GET',headers:body?{'Content-Type':'application/json'}:{},credentials:'omit',signal:controller.signal,...(body?{body:JSON.stringify({...body,visitor})}:{})});const data=await r.json();if(!r.ok)throw new Error(data.error||'Please try again later.');return data;}finally{clearTimeout(timeout);}}
  const errorMessages={
    'Failed to fetch':'The guestbook is temporarily unavailable. Please try again later. / 留言服务暂时无法连接，请稍后重试。',
    'The guestbook is temporarily unavailable.':'The guestbook is temporarily unavailable. Please try again later. / 留言服务暂时无法连接，请稍后重试。',
    '暂时无法连接留言板，请稍后重试。':'The guestbook is temporarily unavailable. Please try again later. / 留言服务暂时无法连接，请稍后重试。',
    'Please try again later.':'Please try again later. / 请稍后重试。',
    '操作太频繁，请稍后再试。Please try again later.':'Too many requests. Please try again later. / 操作太频繁，请稍后再试。',
    'This origin is not allowed.':'Please open the guestbook on the official website. / 请在本站打开留言板。',
    'Invalid request origin.':'Please open the guestbook on the official website. / 请在本站打开留言板。',
    'Method not allowed.':'Unable to process this request. Please refresh and try again. / 无法处理本次请求，请刷新后重试。',
    'Use application/json.':'Unable to process this request. Please refresh and try again. / 无法处理本次请求，请刷新后重试。',
    'Invalid JSON.':'Unable to process this request. Please refresh and try again. / 无法处理本次请求，请刷新后重试。',
    'Invalid request.':'Unable to process this request. Please refresh and try again. / 无法处理本次请求，请刷新后重试。',
    'Not found.':'The guestbook service could not be found. Please try again later. / 暂未找到留言板服务，请稍后重试。',
    'Message too long.':'Your message is too long. Please shorten it and try again. / 留言过长，请缩短后重试。',
    'Please refresh the page and try again.':'Please refresh the page and try again. / 请刷新页面后重试。',
    'Unable to submit this request.':'Unable to submit this request. Please refresh and try again. / 无法提交本次请求，请刷新后重试。',
    'Invalid reaction.':'Unable to save this reaction. Please refresh and try again. / 无法保存本次互动，请刷新后重试。',
    '昵称最多 40 字，留言需为 1–1000 字。':'Names can contain up to 40 characters; messages must contain 1–1,000 characters. / 昵称最多 40 字，留言需为 1–1000 字。',
    '请刷新后重试。':'Please refresh the page and try again. / 请刷新页面后重试。',
    '提交已过期，请重试。':'Your submission has expired. Please try again. / 提交已过期，请重试。',
    '请稍等片刻再提交。':'Please wait a moment before submitting. / 请稍等片刻再提交。',
    '这条留言已经提交过了。':'This message has already been submitted. / 这条留言已经提交过了。',
    '这次提交已经处理，请刷新留言。':'This submission has already been processed. Please refresh to see the messages. / 这次提交已经处理，请刷新查看留言。'
  };
  function showError(error){status.textContent=error.name==='AbortError'?'Connection timed out. Please refresh to check whether your submission went through. / 连接超时，请刷新查看是否已提交。':errorMessages[error.message]||'Something went wrong. Please refresh to check the latest status before trying again. / 暂时出现问题，请刷新确认最新状态后再试。';}
  function counts(data){for(const kind of ['visit','like']){document.querySelector(`[data-count="${kind}"]`).textContent=data[kind];document.querySelector(`[data-reaction="${kind}"]`).setAttribute('aria-pressed',String(states[kind]));}}
  function render(comments,append=false){if(!append)list.replaceChildren();if(!comments.length && !append){const p=document.createElement('p');p.className='guestbook-empty';p.textContent='Be the first to say hello. / 来留下第一条留言吧。';list.append(p);}for(const c of comments){const article=document.createElement('article'),header=document.createElement('header'),name=document.createElement('strong'),time=document.createElement('time'),body=document.createElement('p');article.className='guestbook-message';name.textContent=c.name;body.textContent=c.body;const date=new Date(c.created);time.dateTime=date.toISOString();time.textContent=date.toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'});header.append(name,time);article.append(header,body);list.append(article);}}
  async function load(append=false){const data=await api('/api/guestbook'+(append&&next?'?before='+encodeURIComponent(next):''));counts(data.counts);render(data.comments,append);next=data.next;more.hidden=!next;}
  async function prepareChallenge(){if(challenge && Date.now()-challengeAt<540000)return;if(challengePromise)return challengePromise;challengePromise=api('/api/challenge',{website:form.elements.website.value}).then(data=>{challenge=data.challenge;challengeAt=Date.now();}).finally(()=>{challengePromise=null;});return challengePromise;}
  form.addEventListener('focusin',()=>{prepareChallenge().catch(()=>{});});
  for(const button of document.querySelectorAll('[data-reaction]')){const kind=button.dataset.reaction;button.setAttribute('aria-pressed',String(states[kind]));button.addEventListener('click',async()=>{button.disabled=true;status.textContent='';try{const data=await api('/api/reaction',{kind,active:!states[kind],website:''});states[kind]=data.active;save('zhuopie-reaction-'+kind,String(data.active));counts(data.counts);status.textContent=data.active?'Thank you! / 谢谢你来。':'Reaction removed. / 已取消。';}catch(e){showError(e);}finally{button.disabled=false;}});}
  form.addEventListener('submit',async event=>{event.preventDefault();const button=form.querySelector('button[type=submit]');button.disabled=true;status.textContent='Submitting… / 正在提交…';try{await prepareChallenge();const delay=2800-(Date.now()-challengeAt);if(delay>0)await new Promise(resolve=>setTimeout(resolve,delay));await api('/api/comment',{name:form.elements.name.value,body:form.elements.message.value,website:form.elements.website.value,challenge});form.elements.message.value='';challenge=null;status.textContent='Published. Thank you! / 已公开发表，谢谢你的留言。';try{await load();}catch{status.textContent+=' Please refresh to see your message. / 请刷新查看留言。';}}catch(e){challenge=null;showError(e);}finally{button.disabled=false;}});
  more.addEventListener('click',async()=>{more.disabled=true;try{await load(true);}catch(e){showError(e);}finally{more.disabled=false;}});
  load().catch(showError);
})();
