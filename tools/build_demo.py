# -*- coding: utf-8 -*-
"""Wrap the LIVE result page in a test switcher so Gal can inspect every state locally."""
import io, os, shutil

SRC = r"C:/Users/HP/dg-gal-map/map/index.html"
DEST = u"C:/Users/HP/Downloads/\u05d4\u05de\u05e9\u05e4\u05da \u05e9\u05dc\u05d9 \u05d3\u05d9\u05d5\u05e7 \u05d3\u05d9\u05d2\u05d9\u05d8\u05dc\u05d9/\u05d3\u05de\u05d5-\u05d3\u05e3-\u05d4\u05ea\u05d5\u05e6\u05d0\u05d4"

t = io.open(SRC, encoding="utf-8").read()

PANEL = u"""
<style>
#demo{position:fixed;z-index:90;top:52px;left:8px;width:216px;font-size:12px;
  background:rgba(255,255,255,.98);border:1px solid var(--line2);border-radius:16px;
  padding:11px 11px 12px;backdrop-filter:blur(10px);box-shadow:var(--sh2)}
#demo.min{width:auto;padding:7px 11px}
#demo .t{display:flex;align-items:center;justify-content:space-between;gap:8px;font-weight:800;color:var(--orangeS);margin-bottom:8px}
#demo.min .t{margin:0}
#demo .t button{background:none;border:0;color:var(--mut2);font-size:13px;cursor:pointer;padding:0 2px}
#demo .lb{color:var(--txt);font-weight:800;margin:9px 0 1px}
#demo .sb{color:var(--mut2);font-weight:700;margin:0 0 4px;font-size:11px}
#demo .opts{display:flex;gap:5px;flex-wrap:wrap}
#demo .opts button{flex:1 1 auto;cursor:pointer;font-size:11.5px;font-weight:800;padding:6px;border-radius:999px;
  background:#fff;color:var(--mut);border:1px solid var(--line2)}
#demo .opts button.sel{background:var(--pink);color:#fff;border-color:var(--pink)}
#demo.min .body{display:none}
@media (max-width:560px){#demo{top:auto;bottom:12px;left:8px;right:8px;width:auto}}
</style>
<div id="demo">
  <div class="t"><span>תצוגת בדיקה</span><button id="tg">\u25be</button></div>
  <div class="body">
    <div class="lb">מקור הלקוחות</div>
    <div class="sb">התשובה לשאלה הראשונה</div>
    <div class="opts" data-k="source">
      <button data-v="paid" class="sel">ממומן</button><button data-v="mix">שילוב</button>
      <button data-v="ref">המלצות</button><button data-v="org">אורגני</button>
    </div>
    <div class="lb">טמפרטורה</div>
    <div class="sb">משנה את ההזמנה בסוף</div>
    <div class="opts" data-k="temp">
      <button data-v="hot" class="sel">חם</button><button data-v="warm">פושר</button><button data-v="ok">מסודר</button>
    </div>
    <div class="lb">מצב מודעות</div>
    <div class="sb">משנה את הפסקה הוורודה</div>
    <div class="opts" data-k="aware">
      <button data-v="sees">רואה</button><button data-v="blind" class="sel">לא רואה</button><button data-v="burned">נכווה</button>
    </div>
  </div>
</div>
<script>
var FIX = {
  paid:{ track:'a', main:55000, extra:0, biz:'סטודיו נועה, ייעוץ עסקי',
    rows:[['פניות חדשות בחודש','בין 10 ל-30'],['לא מגיעות לשיחה','פחות משליש'],
          ['זמן חזרה לפנייה','בדרך כלל למחרת'],['מעקב למי שלא ענה','בדרך כלל הוא הולך לאיבוד'],
          ['סגירה מתוך השיחות','בערך רבע'],['שווי לקוח בשנה הראשונה','בין 15,000 ל-50,000']],
    answers:{ speed:{i:2}, followup:{i:2}, reach:{i:2}, close:{i:1}, cac:{i:3} } },
  mix:{ track:'a', main:32000, extra:0, biz:'רן אדלר, ייעוץ פיננסי',
    rows:[['פניות חדשות בחודש','בין 30 ל-80'],['לא מגיעות לשיחה','בערך חצי'],
          ['זמן חזרה לפנייה','תוך כמה שעות'],['מעקב למי שלא ענה','חוזרים ידנית כשנזכרים'],
          ['סגירה מתוך השיחות','בערך רבע'],['שווי לקוח בשנה הראשונה','בין 5,000 ל-15,000']],
    answers:{ speed:{i:1}, followup:{i:1}, reach:{i:1}, close:{i:1}, cac:{i:2} } },
  ref:{ track:'b', main:160000, extra:120000, biz:'מיכל לוי, קליניקה לטיפול רגשי',
    rows:[['לקוחות חדשים בחודש','4 עד 8'],['מתוכם מהמלצה או היכרות','כמעט כולם'],
          ['שווי לקוח בשנה הראשונה','בין 15,000 ל-50,000'],['אפשר לקחת מחר עוד','6 עד 10'],
          ['בחודש שההפניות מתייבשות','בעיקר מחכים שזה יסתדר'],['הצעה מנוסחת וקבועה','אין']],
    answers:{ refer:{i:0}, capacity:{i:2}, offer:{i:2}, dry:{i:2}, cac:{i:2} } },
  org:{ track:'b', main:70000, extra:120000, biz:'דור שגיא, ליווי עסקי',
    rows:[['לקוחות חדשים בחודש','9 עד 20'],['מתוכם מהמלצה או היכרות','בערך חצי'],
          ['שווי לקוח בשנה הראשונה','בין 15,000 ל-50,000'],['אפשר לקחת מחר עוד','6 עד 10'],
          ['בחודש שההפניות מתייבשות','פונים ידנית ללקוחות עבר'],['הצעה מנוסחת וקבועה','משהו כללי']],
    answers:{ refer:{i:2}, capacity:{i:2}, offer:{i:1}, dry:{i:1}, cac:{i:2} } }
};
var T = { source:'paid', temp:'hot', aware:'blind' };
function apply(){
  var f = FIX[T.source];
  D = { track:f.track, source:T.source, score:21, temp:T.temp, aware:T.aware,
        blind:4, burn:T.aware === 'burned', main:f.main, extra:f.extra,
        name:'בדיקה', biz:f.biz, phone:'0500000000', email:'test@dg-gal.online',
        rows:f.rows, answers:f.answers };
  render();
  window.scrollTo({ top:0 });
}
document.querySelectorAll('#demo .opts').forEach(function(g){
  g.addEventListener('click', function(e){
    var b = e.target.closest('button'); if(!b) return;
    g.querySelectorAll('button').forEach(function(x){ x.classList.remove('sel'); });
    b.classList.add('sel'); T[g.dataset.k] = b.dataset.v; apply();
  });
});
document.getElementById('tg').addEventListener('click', function(){
  var d = document.getElementById('demo'); d.classList.toggle('min');
  this.textContent = d.classList.contains('min') ? '\\u25b4' : '\\u25be';
});
apply();
</script>
"""

out = t.replace("</body>", PANEL + "</body>", 1)
if not os.path.isdir(DEST):
    os.makedirs(DEST)
for name in ("index.html", u"\u05d3\u05e3-\u05d4\u05ea\u05d5\u05e6\u05d0\u05d4-\u05d3\u05de\u05d5.html"):
    io.open(os.path.join(DEST, name), "w", encoding="utf-8").write(out)
print("demo written, %.0f KB, both filenames" % (len(out.encode("utf-8")) / 1024.0))
