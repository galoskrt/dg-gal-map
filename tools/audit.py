# -*- coding: utf-8 -*-
"""Full audit of the funnel, run against the LIVE pages.

Written after shipping three defects Gal found himself: a result page whose
script had not parsed for hours, an email quoting a different number than the
page, and an email button leading to "the map was not found". Every one of
them would have been caught by opening the thing and looking. So this checks
the artefact that actually ships, not the source it was built from.
"""
import io
import json
import os
import re
import subprocess
import sys
import urllib.request

BASE = "https://map.dg-gal.online"
WORKER = "https://dg-gal-funnel.tom-harush.workers.dev"
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
SP = os.path.dirname(os.path.abspath(__file__))

# דף התוצאה נבדק עם מפה אמיתית. בלי מזהה הוא מציג את מסך "לא נמצאה",
# שהוא נכון בפני עצמו אבל אינו הדף שהלקוח רואה.
# המזהה אינו נכנס למאגר הציבורי, אז הוא יכול להיעלם בשיחה חדשה.
# נופלים עם הסבר, ולא עם traceback שאינו אומר מה לעשות.
_ID_FILE = os.path.join(SP, "_e2e_id.txt")
SAMPLE_ID = (os.environ.get("DG_MAP_ID", "").strip()
             or (io.open(_ID_FILE, encoding="utf-8").read().strip()
                 if os.path.exists(_ID_FILE) else ""))
if not SAMPLE_ID:
    sys.exit(u"חסר מזהה מפה לבדיקת דף התוצאה.\n"
             u"קח מזהה מ-GET /leads עם מפתח הדשבורד, וכתוב אותו ל-tools/_e2e_id.txt\n"
             u"או העבר אותו במשתנה הסביבה DG_MAP_ID.")
PAGES = [("/", "landing"), ("/q/", "survey"), ("/map/?id=" + SAMPLE_ID, "result"),
         ("/call/", "booking"), ("/privacy/", "privacy")]

DASH = re.compile(u"[\u2013\u2014]")
EMOJI = re.compile(u"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2190-\u21FF\u2B00-\u2BFF]")
# צורות זכר שהחליטו להוציא מהעותק. ניסוח כוללני, לא יחיד ולא רבים.
# צורות רבים שאינן בשימוש. גבול מילה חובה, אחרת "והגענו" נתפס בטעות כ"ענו".
GENDERED = [u"תחליטו", u"סימנתם", u"אתם", u"שלכם", u"תוכלו", u"קיבלתם", u"ענו"]
WORD = lambda t, g: re.search(r"(?<![֐-׿])" + g + r"(?![֐-׿])", t)

results = []


def rendered_dom(path, width=390, budget=9000):
    """The page after its script has run, which is what a reader gets."""
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                          "--window-size=%d,1400" % width,
                          "--virtual-time-budget=%d" % budget,
                          "--dump-dom", BASE + path],
                         capture_output=True).stdout.decode("utf-8", "replace")
    return rendered_text(out)


def add(area, ok, msg):
    results.append((area, ok, msg))


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "dg-audit"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def rendered_text(html):
    """What a reader sees: markup and scripts removed."""
    t = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style\b.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


# ─────────────────────────────────────────────── 1. every page loads and parses
def check_pages():
    for path, name in PAGES:
        try:
            h = fetch(path)
        except Exception as e:
            add("load", False, "%s did not load: %s" % (name, e))
            continue
        kb = len(h.encode()) // 1024
        add("weight", kb <= 200, "%s is %d KB" % (name, kb))

        if "<script>" in h:
            js = h[h.rindex("<script>") + 8: h.rindex("</script>")]
            io.open(os.path.join(SP, "_a.js"), "w", encoding="utf-8").write(js)
            r = subprocess.run(["node", "--check", os.path.join(SP, "_a.js")],
                               capture_output=True)
            add("script", r.returncode == 0, "%s script %s" % (
                name, "parses" if r.returncode == 0
                else "IS BROKEN: " + r.stderr.decode("utf-8", "ignore").split("\n")[1][:60]))

        # קוראים את מה שבאמת מוצג. בדף התוצאה הפוטר נבנה בזמן ריצה,
        # ובדיקה סטטית פשוט לא רואה אותו.
        txt = rendered_dom(path)
        add("punctuation", not DASH.search(txt), "%s dashes: %d" % (name, len(DASH.findall(txt))))
        add("punctuation", not EMOJI.search(txt), "%s emojis: %d" % (name, len(EMOJI.findall(txt))))
        bad = [g for g in GENDERED if WORD(txt, g)]
        add("voice", not bad, "%s gendered forms: %s" % (name, ", ".join(bad) or "none"))
        add("copyright", u"כל הזכויות שמורות" in txt, "%s carries the copyright line" % name)


# ─────────────────────────────────────────────── 2. one rule for money
def check_money_rule():
    page = fetch("/map/")
    worker = io.open(r"C:/Users/HP/dg-gal-worker/worker.js", encoding="utf-8").read()
    rule = u"פחות מ-1,000"
    add("numbers", rule in page, "result page has the sub-1000 wording")
    add("numbers", rule in worker, "the emails use the same wording")
    floor_page = "URGENCY_FLOOR" in fetch("/q/")
    floor_worker = "URGENCY_FLOOR" in worker
    add("logic", floor_page and floor_worker,
        "urgency floor present in both the survey and the worker")
    m1 = re.search(r"URGENCY_FLOOR\s*=\s*(\d+)", fetch("/q/"))
    m2 = re.search(r"URGENCY_FLOOR\s*=\s*(\d+)", worker)
    add("logic", bool(m1 and m2 and m1.group(1) == m2.group(1)),
        "the floor is the same number on both sides: %s / %s"
        % (m1.group(1) if m1 else "?", m2.group(1) if m2 else "?"))


# ─────────────────────────────────────────────── 3. nothing secret ships
def check_secrets():
    leaks = ["re_", "rnd_", "ghp_", "EAAG", "CLOUDFLARE", "PLATFORM_KEY"]
    for path, name in PAGES:
        h = fetch(path)
        body = re.sub(r"base64,[A-Za-z0-9+/=]+", "base64,", h)
        found = [k for k in leaks if k in body]
        add("security", not found, "%s carries no credential (%s)"
            % (name, ", ".join(found) or "clean"))

    for ep, need_auth in (("/leads", True), ("/cal-last", True)):
        code = urllib.request.urlopen(
            urllib.request.Request(WORKER + ep, headers={"User-Agent": "dg-audit"}),
            timeout=20).getcode() if not need_auth else None
        try:
            urllib.request.urlopen(urllib.request.Request(
                WORKER + ep, headers={"User-Agent": "dg-audit"}), timeout=20)
            add("security", False, "%s answered without a key" % ep)
        except urllib.error.HTTPError as e:
            add("security", e.code == 401, "%s refuses an unauthenticated read (%d)" % (ep, e.code))


# ─────────────────────────────────────────────── 4. mobile typography
def measure(path, script, width=390, height=1400, budget=9000):
    h = fetch(path)
    # הדפדפן ללא ראש כופה רוחב מינימלי של כ-500 פיקסלים, אז מדידה ב-390 היא
    # למעשה מדידה ב-500. כופים את הרוחב על הדף עצמו כדי למדוד באמת במובייל.
    h = h.replace("</head>",
                  "<style>html,body{width:%dpx!important;max-width:%dpx!important;"
                  "margin:0!important}</style></head>" % (width, width), 1)
    h = h.replace("</body>", "<script>%s</script></body>" % script, 1)
    f = os.path.join(SP, "_a.html")
    io.open(f, "w", encoding="utf-8").write(h)
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                          "--window-size=%d,%d" % (width, height),
                          "--virtual-time-budget=%d" % budget,
                          "--dump-dom", "file:///" + f.replace("\\", "/")],
                         capture_output=True).stdout.decode("utf-8", "replace")
    m = re.search(r"<title>(.*?)</title>", out, re.S)
    return m.group(1) if m else ""


ORPHAN = r"""setTimeout(function(){
  /* מילה יתומה היא מילה בודדת שנשארה לבדה בשורה האחרונה. מודדים אותה
     ממש, ולא לפי רוחב שורה קצרה, שמסמן גם שורות תקינות כיתומות. */
  var bad = [], w = 390;
  document.querySelectorAll('h1,h2,h3,p,.res,.pun,.mirror,.sub,.rel').forEach(function(e){
    var r = document.createRange(); r.selectNodeContents(e);
    /* הדגשה צבעונית בתוך שורה יוצרת כמה מלבנים באותה שורה, אז
       מקבצים לפי הגובה. בלי זה כל טקסט מודגש נראה כאילו יש בו יתומה. */
    var byTop = {};
    [].slice.call(r.getClientRects()).forEach(function(x){
      var k = Math.round(x.top);
      if(!byTop[k]) byTop[k] = { top:k, left:x.left, right:x.right };
      else { byTop[k].left = Math.min(byTop[k].left, x.left);
             byTop[k].right = Math.max(byTop[k].right, x.right); }
    });
    var ls = Object.keys(byTop).map(function(k){ return byTop[k]; })
      .sort(function(a,b){ return a.top - b.top; })
      .map(function(x){ return { width: x.right - x.left }; });
    if(ls.length < 2) return;
    var last = ls[ls.length - 1];
    /* innerText ולא textContent, ורק המקטע שאחרי שבירת השורה האחרונה
       שנכתבה בכוונה: <br> הוא החלטה עיצובית, לא מילה יתומה. */
    var segs = (e.innerText||e.textContent||'').trim().split(/\n+/);
    var words = segs[segs.length - 1].trim().split(/\s+/);
    if(words.length < 3) return;
    var probe = document.createElement('span');
    var cs = getComputedStyle(e);
    probe.style.cssText = 'position:absolute;visibility:hidden;white-space:nowrap;font:'
      + cs.font + ';letter-spacing:' + cs.letterSpacing;
    probe.textContent = words[words.length - 1];
    document.body.appendChild(probe);
    var wordW = probe.getBoundingClientRect().width;
    document.body.removeChild(probe);
    if(last.width > 0 && last.width <= wordW + 6)
      bad.push('"' + words[words.length - 1] + '" alone after: ...'
               + words.slice(-4, -1).join(' '));
  });
  /* הרוחב נכפה על body בלבד, והדפדפן עדיין רחב ממנו. אז מרכז הדף
     הוא מרכז ה-body, ולא מרכז החלון. בלי זה כל כותרת ממורכזת
     נמדדת כסטויה בדיוק בחצי הפרש. */
  var bb = document.body.getBoundingClientRect(), mid = bb.left + bb.width / 2;
  var off = [];
  document.querySelectorAll('h1,h2').forEach(function(e){
    var s = getComputedStyle(e);
    if(s.textAlign === 'center'){
      var r = e.getBoundingClientRect();
      var d = Math.abs((r.left + r.right)/2 - mid);
      if(d > 4) off.push(e.tagName + ' off by ' + Math.round(d));
    }
  });
  /* גלילה אופקית נמדדת על התוכן שזורם, לא על החלון: עיטורים
     ב-position:fixed נמתחים לרוחב הפרש בכוונה ואינם גוללים כלום. */
  document.title = 'orphans=' + bad.length + (bad.length ? ' :: ' + bad.join(' | ') : '')
    + ' ;; centring=' + (off.length ? off.join(', ') : 'ok')
    + ' ;; hscroll=' + (document.body.scrollWidth > w + 1);
}, 1200);"""


def check_typography():
    for path, name in PAGES:
        t = measure(path, ORPHAN)
        orph = re.search(r"orphans=(\d+)", t)
        add("typography", bool(orph and orph.group(1) == "0"),
            "%s %s" % (name, t[:150] if t else "could not measure"))
        # שתי המדידות האלה דווחו שנים בלי שאף אחד נכשל עליהן.
        # עכשיו שהן נמדדות מול ה-body ולא מול החלון, הן אמינות.
        add("typography", "centring=ok" in t,
            "%s centring: %s" % (name, (re.search(r"centring=([^;]*)", t)
                                        or ["", "not measured"])[1].strip()))
        add("typography", "hscroll=false" in t,
            "%s does not scroll sideways at 390" % name)


if __name__ == "__main__":
    which = sys.argv[1:] or ["pages", "money", "secrets", "type"]
    if "pages" in which: check_pages()
    if "money" in which: check_money_rule()
    if "secrets" in which: check_secrets()
    if "type" in which: check_typography()

    fails = [r for r in results if not r[1]]
    for area, ok, msg in results:
        print("  %s  %-12s %s" % ("ok  " if ok else "FAIL", area, msg))
    print("\n  %d checks, %d failed" % (len(results), len(fails)))
