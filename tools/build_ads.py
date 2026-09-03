# -*- coding: utf-8 -*-
"""ארבע המודעות של הקמפיין הקרוב, מרונדרות כאן ולא במודל תמונות.

למה זה קיים: מודל התמונות מקבל משימה אחת, האובייקט. כל אות במודעה נכתבת
כאן, בפונט תל אביב האמיתי, עם שליטה מלאה על שבירת השורות. שתי משימות
לאותו מודל נותנות ארבע תוצאות שלא נראות כמו סט, וזה מה שעצר את גל בכל
משפך בשלב הזה.

האמנות נחתכה מהמודעות שגל כבר ייצר, `crop_art.py`, ולכן לא צריך לייצר
כלום מחדש כדי לשנות קופי.

כל שורת כותרת היא בלוק שלא נשבר, ולכן אין מילים יתומות לעולם.
הניסוח כוללני: עבר בגוף שני, סיומת ך, ושם פעולה. בלי אתה, בלי הווה,
בלי ציווי.

© כל הזכויות שמורות · דיוק דיגיטלי · גל הרוש 2026
"""
import base64
import io
import os
import subprocess
import sys

SP = os.path.dirname(os.path.abspath(__file__))
SK = u"C:/Users/HP/.claude/skills/carousel-diyuk-digitali/assets"
CH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

FORMATS = {          # name: (w, h, type scale, padTop, padBottom, padX)
    "square": (1080, 1080, 1.00, 0.052, 0.050, 0.070),
    "feed":   (1080, 1350, 1.02, 0.052, 0.046, 0.070),
}

SPEC3 = u"והמספר שלך על המסך"
CTA = u"למפת הדליפה שלי"

# ─────────────────────────────────────────────────────────────────────
# ארבע מודעות, ארבעה קהלים, לפי שאלה 1 בשאלון.
# הפתיחה בכל אחת היא מהאדם ומצבו, לעולם לא מהמוצר.
ADS = [
    {
        "id": "a1_paid", "art": "art_7.png",
        "tag": u"לעסקים שהעסקה שלהם נסגרת בשיחה או פגישה",
        "h1": [u'שילמת על כל פנייה שנכנסה.',
               u'אף אחד לא הראה לך איפה הן <span class="mark p">נעצרות</span>.'],
    },
    {
        "id": "b2_referral", "art": "art_12.png",
        "tag": u"לעסקים שחיים על המלצות",
        "h1": [u'ההמלצות בנו לך עסק.',
               u'הן <span class="mark p">לא נפתחות</span> ביום שצריך עוד.'],
    },
    {
        "id": "c3_organic", "art": "art_14.png",
        "tag": u"לעסקים שהתוכן שלהם מביא פניות ולא עסקאות",
        "h1": [u'שנים של תוכן הביאו לך פניות.',
               u'הדרך מהפנייה לעסקה נשארה <span class="mark p">חשוכה</span>.'],
    },
    {
        "id": "d4_mix", "art": "art_10.png",
        "tag": u"לעסקים שמפרסמים וגם חיים על המלצות",
        "h1": [u'מול לקוח זה <span class="mark g">נסגר</span> אצלך.',
               u'הקושי מתחיל הרבה <span class="mark p">לפני השולחן</span>.'],
    },
]


def b64(path):
    return base64.b64encode(io.open(path, "rb").read()).decode("ascii")


FONT = u""
for weight, fn in ((400, "TelAviv-Regular.ttf"), (800, "TelAviv-Bold.ttf")):
    FONT += (u"@font-face{font-family:'TelAviv';font-weight:%d;font-style:normal;"
             u"src:url(data:font/ttf;base64,%s) format('truetype');}\n"
             % (weight, b64(os.path.join(SK, "fonts", fn))))


def vars_for(w, h, s, padT, padB, padX):
    """יחידה אחת מניעה הכל, כדי שמעבר פורמט לא ידרוש מספרים חדשים."""
    u = w / 26.0
    return {
        "W": "%dpx" % w, "H": "%dpx" % h, "cell": "%.1fpx" % (w / 47.0),
        "padT": "%.1fpx" % (h * padT), "padB": "%.1fpx" % (h * padB),
        "padX": "%.1fpx" % (w * padX),
        "tagF": "%.1fpx" % (u * 0.60 * s), "tagB": "%.1fpx" % (u * 0.075),
        "tagP": "%.1fpx %.1fpx" % (u * 0.34, u * 0.86),
        "gapA": "%.1fpx" % (h * 0.034), "gapB": "%.1fpx" % (h * 0.012),
        "gapC": "%.1fpx" % (h * 0.012), "gapD": "%.1fpx" % (h * 0.022),
        "gapE": "%.1fpx" % (h * 0.024),
        "h1": "%.1fpx" % (u * 1.10 * s),
        "nameF": "%.1fpx" % (u * 1.44 * s),
        "specF": "%.1fpx" % (u * 0.64 * s), "specI": "%.1fpx" % (u * 0.72),
        "specIG": "%.1fpx" % (u * 0.26), "specGap": "%.1fpx" % (u * 0.52),
        "specP": "%.1fpx %.1fpx" % (u * 0.44, u * 0.92),
        "dot": "%.1fpx" % (u * 0.20),
        "ctaF": "%.1fpx" % (u * 0.92 * s),
        "ctaP": "%.1fpx %.1fpx" % (u * 0.60, u * 1.55),
        "ctaSY": "%.1fpx" % (u * 0.22), "ctaSB": "%.1fpx" % (u * 0.75),
    }


def build(ad, fmt, probe=""):
    w, h, s, padT, padB, padX = FORMATS[fmt]
    html = io.open(os.path.join(SP, "ad2.html"), encoding="utf-8").read()
    html = html.replace("/*FONT*/", FONT)
    html = html.replace("/*ART*/", "data:image/png;base64,%s"
                        % b64(os.path.join(SP, "img", ad["art"])))
    html = html.replace("/*TAG*/", ad["tag"])
    html = html.replace("/*H1*/", "".join(u"<i>%s</i>" % l for l in ad["h1"]))
    html = html.replace("/*SPEC3*/", SPEC3)
    html = html.replace("/*CTA*/", CTA)
    css = ";".join("--%s:%s" % (k, v) for k, v in vars_for(w, h, s, padT, padB, padX).items())
    html = html.replace('<div class="ad">', '<div class="ad" style="%s">' % css)
    if probe:
        html = html.replace("</body>", "<script>%s</script></body>" % probe)

    tmp = os.path.join(SP, "_ad_%s_%s.html" % (ad["id"], fmt))
    io.open(tmp, "w", encoding="utf-8").write(html)
    outdir = os.path.join(SP, "out")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    out = os.path.join(outdir, "%s_%s.png" % (ad["id"], fmt))
    cmd = [CH, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=1", "--window-size=%d,%d" % (w, h),
           "--virtual-time-budget=6000"]
    cmd += (["--dump-dom"] if probe else ["--screenshot=" + out])
    cmd += ["file:///" + tmp.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True)
    if probe:
        import re
        m = re.search(r"<title>(.*?)</title>", r.stdout.decode("utf-8", "replace"), re.S)
        return m.group(1) if m else "no reading"
    from PIL import Image
    got = Image.open(out).size
    print("  %-14s %-7s %s  %s" % (ad["id"], fmt, got,
                                   "OK" if got == (w, h) else "SIZE MISMATCH"))
    return out


if __name__ == "__main__":
    fmts = sys.argv[1:] or ["square"]
    for f in fmts:
        for ad in ADS:
            build(ad, f)
