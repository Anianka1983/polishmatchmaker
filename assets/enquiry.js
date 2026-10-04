(function(){
  'use strict';
  var form=document.getElementById('enquiry');
  if(!form)return;
  var L=form.getAttribute('data-lang')||'pl';
  var T={
    pl:{sending:'Wysyłanie…',send:'Wyślij zapytanie',err:'Coś poszło nie tak. Spróbuj ponownie lub napisz na hello@sparkedconnection.com.',req:'Uzupełnij wymagane pola, oznaczone na czerwono.'},
    en:{sending:'Sending…',send:'Send enquiry',err:'Something went wrong. Please try again, or email hello@sparkedconnection.com.',req:'Please complete the required fields, marked in red.'}
  }[L];

  // Same channels as the Sparked Connection and The Decided forms, so everything lands in one place.
  var FORMBOLD='https://formbold.com/s/3Omwk';
  var FORMSPREE='https://formspree.io/f/xojynjke';
  var FORMSUBMIT='https://formsubmit.co/ajax/hello@sparkedconnection.com';
  var CRM='https://sparked-connection-crm.vercel.app/api/intake';
  var SHEETS='https://script.google.com/macros/s/AKfycbyKrKHx4wZKvW-Xu7QLcH7Wc9H1WrOEVKdMR4iF_NrBJ7vJQjmqAieNV9JWISVxorhq/exec';
  var BRAND='Dobrani (Polish Matchmaker)';
  var RENDERED=new Date().toISOString();

  var btn=document.getElementById('enq-submit'),errBox=document.getElementById('enq-error'),ok=document.getElementById('enq-success');

  function val(){
    var good=true,first=null;
    form.querySelectorAll('[required]').forEach(function(el){
      var okf=el.type==='checkbox'?el.checked:el.value.trim()!=='';
      if(el.type==='email'&&okf)okf=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value.trim());
      el.classList.toggle('invalid',!okf);
      if(!okf){good=false;if(!first)first=el;}
    });
    var ag=form.querySelector('[name=age]');
    if(ag&&ag.value!==''){var n=Number(ag.value),okA=Number.isInteger(n)&&n>=18&&n<=99;ag.classList.toggle('invalid',!okA);if(!okA){good=false;if(!first)first=ag;}}
    errBox.textContent=good?'':T.req;errBox.classList.toggle('show',!good);
    if(first)first.scrollIntoView({behavior:'smooth',block:'center'});
    return good;
  }
  form.addEventListener('input',function(e){e.target.classList.remove('invalid')});

  function toObj(fd){var o={};fd.forEach(function(v,k){if(o[k]!==undefined){if(!Array.isArray(o[k]))o[k]=[o[k]];o[k].push(v)}else o[k]=v});return o}
  function norm(d){
    var name=((d.first_name||'')+' '+(d.last_name||'')).trim();
    var o={
      _subject:'New enquiry - Dobrani (Polish Matchmaker)',
      _replyto:d['fi-sender-email']||'',
      name:name,email:d['fi-sender-email']||'',
      phone:((d['fi-select-countryCode']||'')+' '+(d['fi-text-phoneLocal']||'')).trim(),
      formType:'Dobrani Enquiry',form_source:'Dobrani Enquiry Form ('+L.toUpperCase()+')',brand:BRAND,
      page_language:L,pageUrl:location.href,submittedAt:new Date().toISOString()
    };
    for(var k in d)o[k]=d[k];
    delete o.website;
    return o;
  }

  function toFormBold(p){return new Promise(function(res){
    var f=document.getElementById('fb-frame');
    if(!f){f=document.createElement('iframe');f.name=f.id='fb-frame';f.style.display='none';document.body.appendChild(f)}
    var t=document.createElement('form');t.action=FORMBOLD;t.method='POST';t.enctype='multipart/form-data';t.target=f.name;t.style.display='none';
    Object.keys(p).forEach(function(k){var i=document.createElement('input');i.type='hidden';i.name=k;i.value=Array.isArray(p[k])?p[k].join(', '):(p[k]==null?'':p[k]);t.appendChild(i)});
    document.body.appendChild(t);var done=false;
    function fin(){if(done)return;done=true;setTimeout(function(){t.remove()},1000);res(true)}
    f.addEventListener('load',fin,{once:true});setTimeout(fin,6000);t.submit();
  })}
  function toFormspree(p){
    var b=new URLSearchParams();Object.keys(p).forEach(function(k){b.append(k,Array.isArray(p[k])?p[k].join(', '):String(p[k]==null?'':p[k]))});
    b.append('full_raw_submission',JSON.stringify(p));
    return fetch(FORMSPREE,{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8','Accept':'application/json'},body:b.toString()}).then(function(r){if(!r.ok)throw 0;return true});
  }
  function toFormSubmit(p){
    return fetch(FORMSUBMIT,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({_subject:'Backup: New enquiry - Dobrani',_captcha:'false',name:p.name,email:p.email,phone:p.phone,message:JSON.stringify(p,null,2)})}).then(function(r){if(!r.ok)throw 0;return true});
  }
  function toSheets(p){
    return fetch(SHEETS,{method:'POST',mode:'no-cors',headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},body:new URLSearchParams({payload:JSON.stringify(p)}).toString()}).then(function(){return true});
  }
  function toCRM(p){
    var tok=(document.querySelector('[name="cf-turnstile-response"]')||{}).value||'';
    var body=Object.assign({},p,{turnstile_token:tok,form_rendered_at:RENDERED,brand:BRAND});
    return fetch(CRM,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){if(!r.ok)throw 0;return true});
  }
  function attempt(fn,p){return fn(p).then(function(v){return v},function(){return false})}

  form.addEventListener('submit',function(e){
    e.preventDefault();
    if(!val())return;
    if(form.website&&form.website.value)return; // honeypot
    btn.disabled=true;btn.textContent=T.sending;
    var p=norm(toObj(new FormData(form)));
    // sequential, as on the other sites (FormBold first, then the rest)
    attempt(toFormBold,p).then(function(a){return attempt(toFormspree,p).then(function(b){return attempt(toCRM,p).then(function(c){return attempt(toFormSubmit,p).then(function(d){return attempt(toSheets,p).then(function(s){return [a,b,c,d,s]})})})})}).then(function(r){
      if(!r.some(Boolean)){btn.disabled=false;btn.textContent=T.send;errBox.textContent=T.err;errBox.classList.add('show');return}
      form.style.display='none';errBox.classList.remove('show');ok.classList.add('show');
      ok.scrollIntoView({behavior:'smooth',block:'center'});
    });
  });
})();
