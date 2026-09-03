# -*- coding: utf-8 -*-
"""QA every built funnel page: true-mobile screenshot + language audit."""
import io, os, re, shutil, subprocess, sys

SP = os.path.dirname(os.path.abspath(__file__))
REPO = u"C:/Users/HP/dg-gal-map"
CH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

PAGES = [("", "landing"), ("q", "survey"), ("map", "result"),
         ("call", "booking"), ("privacy", "privacy")]

SEED = u"""<script>
sessionStorage.setItem('dg_map', JSON.stringify({
  track:'a', score:21, temp:'hot', aware:'blind', blind:4, burn:false,
  main:55000, extra:0, name:'נועה', biz:'סטודיו נועה, ייעוץ עסקי',
  phone:'0501234567', email:'a@b.com',
  rows:[['פניות חדשות בחודש','בין 10 ל-30'],['לא מגיעות לשיחה','פחות משליש'],
        ['זמן חזרה לפנייה','בדרך כלל למחרת'],['מעקב למי שלא ענה','בדרך כלל הוא הולך לאיבוד'],
        ['סגירה מתוך השיחות','בערך רבע'],['שווי לקוח בשנה הראשונה','בין 15,000 ל-50,000']],
  answers:{ speed:{i:2}, followup:{i:2}, reach:{i:2}, close:{i:1}, cac:{i:3} }
}));
</script>"""

BAD = [u'אתם', u'שלכם', u'לכם ', u'סימנתם', u'תחליטו', u'קחו ', u'תכתבו',
       u'תרצו', u'אתכם', u'איתכם', u'ידעתם', u'שים לב', u'תדע ']
DASH = re.compile(u"[\u2013\u2014\u05be\u2212]")
EMOJI = re.compile(u"[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def shot(local, out, w=390, h=1100, budget=7000, seed=False):
    src = io.open(local, encoding="utf-8").read()
    if seed:
        src = src.replace("<script>", SEED + "<script>", 1)
    tmp = os.path.join(SP, "_p.html")
    io.open(tmp, "w", encoding="utf-8").write(src)
    wrap = os.path.join(SP, "_w.html")
    io.open(wrap, "w", encoding="utf-8").write(
        u'<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}'
        u'iframe{width:%dpx;height:%dpx;border:0;display:block}</style>'
        u'<iframe src="_p.html"></iframe>' % (w, h))
    subprocess.run([CH, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=%d,%d" % (max(w, 501), h),
                    "--virtual-time-budget=%d" % budget, "--screenshot=" + os.path.abspath(out),
                    "file:///" + wrap.replace("\\", "/")], capture_output=True)
    try:
        from PIL import Image
        im = Image.open(out)
        if im.size[0] > w:
            im.crop((0, 0, w, min(h, im.size[1]))).save(out)
    except Exception:
        pass


for d, name in PAGES:
    p = os.path.join(REPO, d, "index.html") if d else os.path.join(REPO, "index.html")
    raw = io.open(p, encoding="utf-8").read()
    body = re.sub(r"@font-face\{.*?\}", "", raw, flags=re.S)
    body = re.sub(r"data:[^\)\"']+", "", body)
    body = re.sub(r"<style.*?</style>", "", body, flags=re.S)
    hits = dict((w, body.count(w)) for w in BAD if body.count(w))
    print("%-9s %6.0f KB | dashes=%d emojis=%d | %s"
          % (name, len(raw.encode("utf-8")) / 1024.0,
             len(DASH.findall(body)), len(EMOJI.findall(body)),
             hits if hits else "language clean"))
    shot(p, os.path.join(SP, "qa_%s.png" % name), seed=(d == "map"))
print("screenshots written")

def js_ok(path):
    """Every built page must have a script that actually parses."""
    import subprocess, tempfile
    h = io.open(path, encoding="utf-8").read()
    if "<script>" not in h:
        return "no script"
    body = h[h.rindex("<script>") + 8: h.rindex("</script>")]
    f = os.path.join(tempfile.gettempdir(), "_qa_check.js")
    io.open(f, "w", encoding="utf-8").write(body)
    r = subprocess.run(["node", "--check", f], capture_output=True)
    if r.returncode == 0:
        return "js clean"
    return "JS BROKEN: " + r.stderr.decode("utf-8", "ignore").split("
")[1].strip()[:70]
