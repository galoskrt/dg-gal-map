# -*- coding: utf-8 -*-
"""Measure orphan words on the local build, at a true phone width.

Headless Chrome refuses to go below roughly 500px, so a "390px" window is
really 500 and every typographic finding at that width is measured on the
wrong page. The width is forced onto the document instead.
"""
import io
import os
import re
import subprocess

CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
W = 390

PROBE = r"""setTimeout(function(){
  var bad = [], w = %d;
  document.querySelectorAll('h1,h2,h3,p,.res,.pun,.mirror,.sub,.rel').forEach(function(e){
    var r = document.createRange(); r.selectNodeContents(e);
    /* הדגשה צבעונית בתוך שורה יוצרת כמה מלבנים באותה שורה, אז מקבצים לפי
       הגובה. בלי זה כל טקסט מודגש נראה כאילו יש בו מילה יתומה. */
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
    /* מילה יתומה היא מילה בודדת בשורה האחרונה. מודדים אותה ממש: לוקחים את
       המילה האחרונה ובודקים אם היא לבדה תופסת את כל השורה האחרונה. */
    /* innerText ולא textContent: <br> מפריד שורות, וטקסט משתי שורות
       נדבק בלעדיו למילה אחת ונספר בטעות כיתומה.
       שבירת שורה שנכתבה בכוונה אינה מילה יתומה, אז בודקים רק את
       המקטע האחרון, היחיד שיכול להישבר מעצמו. */
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
  document.title = 'orphans=' + bad.length + (bad.length ? ' :: ' + bad.join(' | ') : '');
}, 1200);""" % W

PAGES = [("", "landing"), ("/q", "survey"), ("/map", "result"),
         ("/call", "booking"), ("/privacy", "privacy")]


def check(sub, name):
    src = "C:/Users/HP/dg-gal-map%s/index.html" % sub
    h = io.open(src, encoding="utf-8").read()
    h = h.replace("</head>",
                  "<style>html,body{width:%dpx!important;max-width:%dpx!important;"
                  "margin:0!important}</style></head>" % (W, W), 1)
    h = h.replace("</body>", "<script>%s</script></body>" % PROBE, 1)
    f = os.path.abspath("_loc.html")
    io.open(f, "w", encoding="utf-8").write(h)
    url = "file:///" + f.replace(os.sep, "/")
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                          "--window-size=500,1400", "--virtual-time-budget=8000",
                          "--dump-dom", url],
                         capture_output=True).stdout.decode("utf-8", "replace")
    m = re.search(r"<title>(.*?)</title>", out, re.S)
    return (m.group(1) if m else "no title")


if __name__ == "__main__":
    total, broken = 0, []
    for sub, name in PAGES:
        r = check(sub, name)
        n = re.search(r"orphans=(\d+)", r)
        # גלאי שנשבר מחזיר את כותרת הדף, ובלי השורה הבאה
        # הכלי מדווח אפס יתומות בדיוק כשהוא לא מדד כלום.
        if not n:
            broken.append(name)
        total += int(n.group(1)) if n else 0
        print("  %-8s %s" % (name, r[:230]))
    print("\n  %d orphan lines across the funnel" % total)
    if broken:
        print("  המדידה לא רצה ב: %s" % ", ".join(broken))
        raise SystemExit(1)
