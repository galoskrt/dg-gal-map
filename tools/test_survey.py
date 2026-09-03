# -*- coding: utf-8 -*-
"""Drive the survey logic headlessly and assert the computed map."""
import io, os, re, subprocess

SP = os.path.dirname(os.path.abspath(__file__))
CH = r"C:/Users/HP/Google/Chrome/Application/chrome.exe"
if not os.path.exists(CH):
    CH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

h = io.open(os.path.join(SP, "_survey_built.html"), encoding="utf-8").read()

harness = u"""<script>
window.addEventListener('load', function(){
  var out = [];
  function run(track, picks, label){
    S.track = track; S.i = 0; S.a = {};
    var list = track === 'a' ? QA : QB;
    S.a.source = { i:0, label:'x', score:3, val:track };
    list.forEach(function(q, n){
      var i = picks[n];
      S.a[q.k] = { i:i, label:q.o[i][2], score:q.o[i][4], val:q.o[i][5] };
    });
    var r = compute();
    out.push(label + ' | track=' + r.track + ' score=' + r.score + ' temp=' + r.temp +
             ' aware=' + r.aware + ' blind=' + r.blind + ' burn=' + r.burn +
             ' main=' + r.main + ' extra=' + r.extra + ' rows=' + r.rows.length);
  }
  // מסלול א: הדוגמה מהמפרט. 30 פניות, שני שליש לא מגיעות, למחרת, בלי מעקב, רבע, 20 אלף
  run('a', [1,1,2,1,2,2,2,3], 'A-spec');
  // מסלול א: הכל תקין, ציון נמוך
  run('a', [0,0,0,0,1,0,0,0], 'A-clean');
  // מסלול א: עיוור לגמרי
  run('a', [2,2,3,3,2,3,2,3], 'A-blind');
  // מסלול ב: הדוגמה מהמפרט. 6 לקוחות, כמעט כולם מהמלצה, 20 אלף, עוד 3 עד 5
  run('b', [1,0,2,1,2,0,2,2], 'B-spec');
  // מסלול ב: נכווה
  run('b', [1,0,2,1,1,2,1,1], 'B-burned');
  document.title = 'RES::' + out.join(' ;; ');
});
</script></body>"""

io.open(os.path.join(SP, "_t.html"), "w", encoding="utf-8").write(h.replace("</body>", harness, 1))
r = subprocess.run([CH, "--headless", "--disable-gpu", "--no-sandbox", "--virtual-time-budget=5000",
                    "--dump-dom", "file:///" + os.path.join(SP, "_t.html").replace("\\", "/")],
                   capture_output=True)
s = r.stdout.decode("utf-8", "replace")
m = re.search(r"<title>RES::(.*?)</title>", s, re.S)
if not m:
    print("NO RESULT. head of dom:\n", s[:400])
else:
    for line in m.group(1).split(" ;; "):
        print(" ", line.strip())
