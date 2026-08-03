// Miau Corp — Minimal analytics tracker
// Tracks page views and basic engagement
(function(){
  try {
    const sid = localStorage.getItem('_miau_sid') || 's_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,10);
    localStorage.setItem('_miau_sid', sid);
    const track = (event, data) => {
      try {
        const payload = { event, path: window.location.pathname, session_id: sid, host: window.location.host, timestamp: new Date().toISOString(), referrer: document.referrer, ...data };
        navigator.sendBeacon('/api/v1/marketing/track', JSON.stringify(payload));
      } catch(e) {}
    };
    track('page_view');
    document.addEventListener('click', (e) => {
      const el = e.target.closest('a,button');
      if (el) track('click', { text: el.innerText?.trim()?.slice(0,64), href: el.href || null });
    });
  } catch(e) {}
})();
