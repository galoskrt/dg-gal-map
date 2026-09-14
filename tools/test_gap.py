# -*- coding: utf-8 -*-
"""The money floor must never silence the diagnosis.

Runs real answer sets through the built survey's own compute(), then renders the
built result page with each computed map in real Chrome and reads back what the
visitor actually sees. Written 14/09/2026 after Gal found that a business with a
broken process and a small volume was told "no reason to hurry".
"""
import io, json, os, re, subprocess, tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
CH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

SURVEY = io.open(os.path.join(REPO, "q", "index.html"), encoding="utf-8").read()
RESULT = io.open(os.path.join(REPO, "map", "index.html"), encoding="utf-8").read()

# מסלול א, לפי סדר השאלות: budget, leads, reach, close, value, speed, followup, cac
CASES = [
    # גל, 14/09/2026: "כמעט אף אחת מהן לא מגיעה לפגישה, וכמעט לא חוזרים אליהן בזמן"
    ("small_broken", "a", [0, 0, 2, 1, 0, 2, 2, 3]),
    # אותו תהליך שבור בדיוק, אבל עם נפח ושווי גדולים
    ("big_broken",   "a", [3, 3, 2, 1, 3, 2, 2, 3]),
    # עסק קטן שהתהליך שלו תקין. כאן "אין סיבה למהר" הוא נכון
    ("small_clean",  "a", [0, 0, 0, 0, 0, 0, 0, 0]),
]

HARNESS = u"""<script>
window.addEventListener('load', function(){
  var out = {};
  CASES.forEach(function(c){
    S.track = c[1]; S.i = 0; S.a = {};
    S.a.source = { i:0, label:'x', score:3, val:c[1] };
    (c[1] === 'a' ? QA : QB).forEach(function(q, n){
      var i = c[2][n];
      S.a[q.k] = { i:i, label:q.o[i][2], score:q.o[i][4], val:q.o[i][5] };
    });
    var r = compute(); r.biz = 'עסק לבדיקה';
    out[c[0]] = r;
  });
  document.title = 'JSON' + JSON.stringify(out);
});
var CASES = __CASES__;
</script>"""


def chrome(path):
    out = subprocess.run([CH, "--headless=new", "--disable-gpu", "--dump-dom",
                          "--virtual-time-budget=6000", "--allow-file-access-from-files",
                          "file:///" + path.replace("\\", "/")],
                         capture_output=True, timeout=180)
    return out.stdout.decode("utf-8", "replace")


def title_of(dom):
    m = re.search(r"<title>(.*?)</title>", dom, re.S)
    return m.group(1) if m else ""


tmp = tempfile.mkdtemp()
p = os.path.join(tmp, "survey.html")
io.open(p, "w", encoding="utf-8").write(
    SURVEY + HARNESS.replace("__CASES__", json.dumps(CASES, ensure_ascii=False)))
maps = json.loads(title_of(chrome(p))[4:])

fails = []
for name, _, _ in CASES:
    m = maps[name]
    page = os.path.join(tmp, name + ".html")
    inject = (u"<script>try{sessionStorage.setItem('dg_map',%s);}catch(e){}</script>"
              % json.dumps(json.dumps(m, ensure_ascii=False), ensure_ascii=False))
    io.open(page, "w", encoding="utf-8").write(RESULT.replace("<body>", "<body>" + inject, 1))
    dom = chrome(page)
    # רק מה שהמבקר באמת רואה. בלי זה הבדיקה קוראת את נוסחי TEMP בתוך הסקריפט עצמו
    seen = re.sub(r"(?is)<script.*?</script>", " ", dom)
    text = re.sub(r"<[^>]+>", " ", seen)
    text = re.sub(r"\s+", " ", text)
    big = re.search(r'class="big"[^>]*>([^<]*)<', dom)
    head = re.search(r'<div class="sec invite" id="s-inv"><h2>([^<]*)<', dom)
    print("%-13s fails=%s fit=%s temp=%-5s main=%-7s | כותרת: %s | פסקה: %s"
          % (name, m.get("fails"), m.get("fit"), m.get("temp"), m.get("main"),
             (big.group(1) if big else "?"), (head.group(1) if head else "?")))
    say_fine = u"אין כאן סיבה למהר" in text
    if name == "small_broken":
        if say_fine: fails.append(u"small_broken עדיין מקבל 'אין כאן סיבה למהר'")
        if u"דליפה אמיתית" not in text: fails.append(u"small_broken לא מקבל את הנוסח החדש")
        if u"₪" in (big.group(1) if big else ""): fails.append(u"small_broken עדיין מציג סכום ככותרת")
    if name == "big_broken" and say_fine: fails.append(u"big_broken מקבל 'אין סיבה למהר'")
    if name == "small_clean" and not say_fine: fails.append(u"small_clean איבד את הנוסח הרגוע")

print("")
print(u"נכשל: " + "; ".join(fails) if fails else u"עבר: שלושת המקרים מתנהגים כמתוכנן")
raise SystemExit(1 if fails else 0)
