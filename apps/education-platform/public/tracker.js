(function(){
  var e="/api/v1/marketing/track",
      t="_miau_sid",
      n=localStorage.getItem(t);
  n||(n="s_"+Date.now().toString(36)+"_"+Math.random().toString(36).slice(2,10),
      localStorage.setItem(t,n));
  function o(t){var n=new URLSearchParams(window.location.search).get(t);return n||null}
  function r(t,r){
    try{
      var a={event:t,path:window.location.pathname,session_id:n,host:window.location.host,
              referrer:document.referrer||null,
              utm_source:o("utm_source"),utm_medium:o("utm_medium"),
              utm_campaign:o("utm_campaign"),utm_term:o("utm_term"),utm_content:o("utm_content"),
              screen_width:window.screen.width,screen_height:window.screen.height,
              language:navigator.language,timestamp:new Date().toISOString()};
      for(var c in r)a[c]=r[c];
      navigator.sendBeacon(e,new Blob([JSON.stringify(a)],{type:"application/json"}))
    }catch(d){}
  }
  r("page_view");
  document.addEventListener("click",function(e){
    var t=e.target.closest("a, button, [data-track]");
    if(!t)return;
    var n=t.getAttribute("data-track-conversion");
    if(n){r("conversion",{conversion_type:n,
          conversion_value:parseFloat(t.getAttribute("data-track-value"))||null,
          metadata:{action:t.innerText.trim().slice(0,64),href:t.href||null}})}
  });
  var a=history.pushState;
  history.pushState=function(){a.apply(this,arguments);
    setTimeout(function(){r("page_view")},100)};
  window.addEventListener("popstate",function(){
    setTimeout(function(){r("page_view")},100)});
  window._miau={sid:n,track:r};
})();
