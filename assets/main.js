(function(){
  var b=document.querySelector('.burger'),m=document.getElementById('menu');
  if(b&&m){b.addEventListener('click',function(){
    var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');
  });}

  // Consent-gated analytics. Set GA_ID in build.py to enable; with no ID this does nothing.
  var id=window.PM_GA;if(!id)return;
  var KEY='pm_consent',cc=document.getElementById('cc');
  function load(){
    if(window.__gaLoaded)return;window.__gaLoaded=1;
    var s=document.createElement('script');s.async=true;
    s.src='https://www.googletagmanager.com/gtag/js?id='+id;document.head.appendChild(s);
    window.dataLayer=window.dataLayer||[];
    function gtag(){dataLayer.push(arguments)}
    gtag('js',new Date());gtag('config',id,{anonymize_ip:true});
  }
  var v=null;try{v=localStorage.getItem(KEY)}catch(e){}
  if(v==='yes'){load();return}
  if(v==='no'||!cc)return;
  cc.style.display='block';
  function set(x){try{localStorage.setItem(KEY,x)}catch(e){}cc.style.display='none';if(x==='yes')load()}
  cc.querySelector('.y').addEventListener('click',function(){set('yes')});
  cc.querySelector('.n').addEventListener('click',function(){set('no')});
})();
