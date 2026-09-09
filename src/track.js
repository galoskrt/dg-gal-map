/* ── דיוק דיגיטלי · מדידת התנהגות בדף ────────────────────────────────────
   מודול אחד לשני הדפים, כי שתי מערכות מדידה נפרדות תמיד נפרדות גם באמת.

   דף הנחיתה עוד לא מכיר ליד, ולכן הוא כותב לאחסון המקומי והשאלון מצרף
   את זה למטען. דף התוצאה כבר מכיר ליד, ולכן הוא משדר ישירות.

   הביקון נשלח כ-text/plain ולא כ-application/json. זה לא קוסמטי:
   application/json אינו ברשימת ההיתר של CORS, מחייב preflight, וכרום
   מוחק בקשת preflight שנשלחת תוך כדי יציאה מהדף. כך אבדה כל הטלמטריה
   עד 09/09/2026. אל תחזיר את זה.                                        */
(function(){
  var MODE = window.DG_TRACK || 'lead';       // 'pre' לדף הנחיתה
  var PRE_KEY = 'dg_pre';
  var t0 = Date.now(), sent = false;

  var st = { scroll: 0, video: false, video_pct: 0, video_secs: 0,
             video_done: false, booking_click: false, asked: false };

  window.__mark = function(k, v){ st[k] = (v === undefined) ? true : v; };

  /* ── מקור התנועה ──────────────────────────────────────────────────
     הקישור לדף הנחיתה יושב גם בביו באינסטגרם, גם בוואטסאפ, גם בפייסבוק
     ובסטוריז. בלי הפרדה, אחוזי המשפך מערבבים תנועה חמה של מודעה עם
     תנועה קרה אורגנית, וכל מסקנה מהם שגויה.

     מסומן paid רק אם הכתובת נשאה fbclid או utm של קמפיין. הסימון נשמר
     לשלושים יום, כי המסע נמשך על פני כמה דפים ולפעמים כמה ימים.     */
  var SRC_KEY = 'dg_src';
  function detectSrc(){
    try {
      var q = new URLSearchParams(location.search);
      if(q.get('fbclid') || q.get('utm_campaign') || q.get('utm_source')){
        localStorage.setItem(SRC_KEY, JSON.stringify({ v:'paid', at:Date.now() }));
        return 'paid';
      }
      var s = JSON.parse(localStorage.getItem(SRC_KEY) || 'null');
      if(s && s.v === 'paid' && Date.now() - s.at < 30*86400000) return 'paid';
    } catch(e){}
    return 'org';
  }
  var SRC = detectSrc();
  window.__src = SRC;

  window.__fx = function(stage, extra){
    var b = { stage: stage, src: SRC };
    if(extra) for(var k in extra) b[k] = extra[k];
    var body = JSON.stringify(b);
    try {
      if(navigator.sendBeacon)
        navigator.sendBeacon(WORKER_URL + '/funnel-event',
          new Blob([body], { type:'text/plain;charset=UTF-8' }));
      else fetch(WORKER_URL + '/funnel-event', { method:'POST', body: body, keepalive:true });
    } catch(e){}
  };

  /* ── נטישה לפי שלב ────────────────────────────────────────────────
     נרשם השלב הרחוק ביותר בלבד, פעם אחת, ביציאה. בלי זה יודעים כמה
     נטשו ולא איפה, ואי אפשר להוריד חיכוך במקום הנכון.               */
  var maxStep = 0, atContact = false;
  window.__step = function(n, contact){
    if(n > maxStep) maxStep = n;
    if(contact) atContact = true;
  };

  addEventListener('scroll', function(){
    var h = document.documentElement.scrollHeight - innerHeight;
    if(h > 0) st.scroll = Math.max(st.scroll, Math.min(100, Math.round(scrollY / h * 100)));
  }, { passive:true });

  /* ── הסרטון ──────────────────────────────────────────────────────────
     שני מספרים שונים במכוון. video_pct הוא הנקודה הרחוקה ביותר שאליה
     הגיע, ו-video_secs הוא זמן צפייה אמיתי שנצבר. מי שגורר את הסרגל
     לסוף מקבל אחוז גבוה אבל שניות נמוכות, וההבדל הזה הוא המידע.        */
  var vidLen = 0;
  function watch(v){
    if(!v || v.__dg) return; v.__dg = 1;
    var last = null;
    v.addEventListener('play', function(){ st.video = true; last = v.currentTime; });
    v.addEventListener('pause', function(){ last = null; });
    v.addEventListener('timeupdate', function(){
      var d = v.duration;
      if(last !== null){
        var dt = v.currentTime - last;
        if(dt > 0 && dt < 1.5) st.video_secs += dt;   // קפיצה קדימה אינה צפייה
        last = v.currentTime;
      }
      if(d && isFinite(d) && d > 0){
        vidLen = d;
        var p = Math.min(100, Math.round(v.currentTime / d * 100));
        if(p > st.video_pct) st.video_pct = p;
        if(p >= 95) st.video_done = true;
      }
    });
    v.addEventListener('ended', function(){ st.video_pct = 100; st.video_done = true; });
  }

  function hook(){
    var vs = document.getElementsByTagName('video');
    for(var i = 0; i < vs.length; i++) watch(vs[i]);
  }
  if(document.readyState === 'loading') addEventListener('DOMContentLoaded', hook);
  else hook();
  /* הסרטון נטען לתוך אלמנט שקיים מראש, אבל אם ייווצר אחד חדש בעתיד
     נתפוס גם אותו בלי שאיש יצטרך לזכור לקרוא לכאן. */
  setInterval(hook, 4000);

  function snap(reason){
    return {
      reason: reason, src: SRC,
      seconds: Math.round((Date.now() - t0) / 1000),
      scroll: st.scroll,
      video: st.video,
      video_pct: st.video_pct,
      video_secs: Math.round(st.video_secs),
      video_len: Math.round(vidLen),
      video_done: st.video_done,
      booking_click: st.booking_click,
      asked: st.asked
    };
  }

  /* ── דף הנחיתה: שומר מקומית, כי אין עדיין למי לשייך ─────────────── */
  function stash(){
    try { localStorage.setItem(PRE_KEY, JSON.stringify(snap('pre'))); } catch(e){}
  }

  /* ── דף התוצאה: משדר ─────────────────────────────────────────────── */
  function send(reason){
    var id = '';
    try { id = sessionStorage.getItem('dg_lead_id') || (window.mapId && mapId()) || ''; } catch(e){}
    if(!id) return;
    var b = snap(reason); b.lead_id = id;
    var body = JSON.stringify(b);
    try {
      if(navigator.sendBeacon)
        navigator.sendBeacon(WORKER_URL + '/event', new Blob([body], { type:'text/plain;charset=UTF-8' }));
      else fetch(WORKER_URL + '/event', { method:'POST', body: body, keepalive:true });
    } catch(e){}
  }

  var push = (MODE === 'pre') ? stash : send;

  function fin(reason){
    if(sent) return; sent = true;
    push(reason);
    /* דיווח למונה היומי, שהוא אנונימי לגמרי ולא תלוי בליד. כך נמדדת
       גם צפייה של מי שלא השאיר פרטים, וזה רוב האנשים. */
    if(MODE === 'pre' && st.video){
      window.__fx('vsl', { vsl: { played:1, pct: st.video_pct,
        secs: Math.round(st.video_secs), len: Math.round(vidLen), done: st.video_done } });
    }
    if(MODE === 'survey') window.__fx('step', { step: maxStep, contact: atContact ? 1 : 0 });
  }

  /* דיווח ביניים, כדי שגם מי שהדפדפן שלו לא הספיק לשלוח ביציאה
     לא יישאר בלי שום נתון. בלעדיו אף אוטומציית נטישה לא יכולה לרוץ. */
  setTimeout(function(){ if(!sent) push('landed'); }, 5000);
  setInterval(function(){ if(!sent) push('tick'); }, 20000);

  addEventListener('pagehide', function(){ fin('leave'); });
  addEventListener('visibilitychange', function(){
    if(document.visibilityState === 'hidden') fin('hidden');
    /* חזר ללשונית. פותחים מחדש כדי שהמשך הצפייה עדיין ייספר. */
    else sent = false;
  });
})();
