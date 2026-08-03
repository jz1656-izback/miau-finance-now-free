(function () {
  var SCRIPT_URL = '/api/v1/marketing/track';
  var SID_KEY = '_miau_sid';
  var sid = localStorage.getItem(SID_KEY);
  if (!sid) {
    sid = 's_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 10);
    localStorage.setItem(SID_KEY, sid);
  }

  function getUtm(name) {
    var m = new URLSearchParams(window.location.search).get(name);
    return m || null;
  }

  function send(event, extra) {
    try {
      var payload = {
        event: event,
        path: window.location.pathname,
        session_id: sid,
        host: window.location.host,
        referrer: document.referrer || null,
        utm_source: getUtm('utm_source'),
        utm_medium: getUtm('utm_medium'),
        utm_campaign: getUtm('utm_campaign'),
        utm_term: getUtm('utm_term'),
        utm_content: getUtm('utm_content'),
        screen_width: window.screen.width,
        screen_height: window.screen.height,
        language: navigator.language,
        timestamp: new Date().toISOString(),
      };
      for (var k in extra) { payload[k] = extra[k]; }
      navigator.sendBeacon(SCRIPT_URL, JSON.stringify(payload));
    } catch (e) {}
  }

  send('page_view');

  function handleClick(e) {
    var t = e.target.closest('a, button, [data-track]');
    if (!t) return;
    var action = t.getAttribute('data-track') || t.innerText.trim().slice(0, 64);
    var type = 'click';
    if (t.getAttribute('data-track-conversion')) {
      type = 'conversion';
      send(type, {
        conversion_type: t.getAttribute('data-track-conversion') || action,
        conversion_value: parseFloat(t.getAttribute('data-track-value')) || null,
        metadata: { action: action, href: t.href || null },
      });
    }
  }
  document.addEventListener('click', handleClick);

  var origPushState = history.pushState;
  history.pushState = function () {
    origPushState.apply(this, arguments);
    setTimeout(function () { send('page_view'); }, 100);
  };
  window.addEventListener('popstate', function () {
    setTimeout(function () { send('page_view'); }, 100);
  });

  if (window.__NEXT_DATA__ || document.querySelector('[data-next-page]')) {
    var origReplaceState = history.replaceState;
    history.replaceState = function () {
      origReplaceState.apply(this, arguments);
      setTimeout(function () { send('page_view'); }, 100);
    };
  }

  window._miau = { sid: sid, track: send };
})();
