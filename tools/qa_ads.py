# -*- coding: utf-8 -*-
"""WORKFLOW על המודעות: בונים, מרנדרים, ומסתכלים על כל רכיב בהגדלה.

הכלל של גל: לעולם לא למסור משהו שלא הסתכלתי עליו. הכשל שהוליד את הקובץ
הזה: הסתכלתי על ארבע המודעות בשלמותן ואמרתי שהן תקינות, וארבעת סימני
הפינה היו זהים זה לזה במקום להתמסר כל אחד לפינה שלו. במבט על המודעה
השלמה זה נראה נכון. בהגדלה זה קופץ מיד.

לכן הכלי חותך את מה שקטן מכדי להיראות ומגדיל אותו:
  · ארבע הפינות של הכרטיס
  · הבאדג', הכותרת, שם המוצר, הרצועה והכפתור

הוא לא מחליף את ההסתכלות, הוא רק דואג שיהיה על מה להסתכל.

© כל הזכויות שמורות · דיוק דיגיטלי · גל הרוש 2026
"""
import io
import os
import subprocess
import sys

from PIL import Image

import build_ads as B
import voice_check as V

SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SP, "out")
QA = os.path.join(OUT, "qa")

PROBE = """setTimeout(function(){
  var card = document.querySelector('.card'), inner = document.querySelector('.inner');
  var avail = card.getBoundingClientRect().width
            - parseFloat(getComputedStyle(inner).paddingLeft) * 2;
  var bad = [];
  function chk(el, label){
    if(!el){ bad.push(label + ' missing'); return; }
    var w = el.getBoundingClientRect().width;
    if(w > avail + 1) bad.push(label + ' ' + Math.round(w) + '>' + Math.round(avail));
  }
  chk(document.querySelector('.tag'), 'tag');
  document.querySelectorAll('h1 i').forEach(function(e,i){ chk(e, 'h1line' + (i+1)); });
  chk(document.querySelector('.name'), 'name');
  chk(document.querySelector('.brand'), 'brand');
  chk(document.querySelector('.spec'), 'spec');
  chk(document.querySelector('.cta'), 'cta');
  /* ארבעת הסימנים חייבים להיות שונים זה מזה. אם שניים יושבים על אותו
     צד אופקי וגם על אותו צד אנכי, אחד מהם לא התמסר לפינה שלו. */
  var pos = [];
  document.querySelectorAll('.tick').forEach(function(t){
    var b = t.getBoundingClientRect(), c = card.getBoundingClientRect();
    pos.push((b.top - c.top < c.height / 2 ? 'T' : 'B')
           + (b.left - c.left < c.width / 2 ? 'L' : 'R'));
  });
  if(new Set(pos).size !== 4) bad.push('ticks not on four corners: ' + pos.join(','));
  document.title = 'ticks=' + pos.join(',')
    + ' problems=' + (bad.length ? bad.join(' | ') : 'none');
}, 1500);"""


def corners(path, out, size=150, zoom=2):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    boxes = [(w - size, 0, w, size), (0, 0, size, size),
             (w - size, h - size, w, h), (0, h - size, size, h)]
    sheet = Image.new("RGB", (size * zoom * 4 + 50, size * zoom + 20), (255, 255, 255))
    for i, b in enumerate(boxes):
        sheet.paste(im.crop(b).resize((size * zoom, size * zoom), Image.NEAREST),
                    (10 + i * (size * zoom + 10), 10))
    sheet.save(out)


def bands(path, out):
    """הרכיבים לפי גובה, מוגדלים, כדי שאפשר יהיה לקרוא אותיות."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    cuts = [(0.05, 0.15), (0.14, 0.31), (0.62, 0.76), (0.74, 0.85), (0.83, 0.96)]
    tiles = [im.crop((0, int(h * a), w, int(h * b))) for a, b in cuts]
    z = 1.35
    tw = int(w * z)
    total = sum(int(t.height * z) + 8 for t in tiles) + 12
    sheet = Image.new("RGB", (tw + 20, total), (255, 255, 255))
    y = 10
    for t in tiles:
        r = t.resize((tw, int(t.height * z)), Image.LANCZOS)
        sheet.paste(r, (10, y))
        y += r.height + 8
    sheet.save(out)


def run(fmts):
    if not os.path.isdir(QA):
        os.makedirs(QA)
    bad = V.run()
    print(u"  שער הניסוח: %s" % (u"%d כשלים" % len(bad) if bad else u"נקי"))
    for f in bad:
        print(u"    FAIL " + f)
    problems = len(bad)
    for fmt in fmts:
        for ad in B.ADS:
            png = B.build(ad, fmt)
            reading = B.build(ad, fmt, PROBE)
            print(u"    %-12s %-6s %s" % (ad["id"], fmt, reading))
            if "problems=none" not in reading:
                problems += 1
            corners(png, os.path.join(QA, "%s_%s_corners.png" % (ad["id"], fmt)))
            bands(png, os.path.join(QA, "%s_%s_bands.png" % (ad["id"], fmt)))
    print(u"\n  גיליונות להסתכלות: %s" % QA)
    print(u"  %s" % (u"אפס כשלים במדידה. עכשיו להסתכל על הגיליונות."
                    if not problems else u"%d כשלים" % problems))
    return problems


if __name__ == "__main__":
    sys.exit(1 if run(sys.argv[1:] or ["square"]) else 0)
