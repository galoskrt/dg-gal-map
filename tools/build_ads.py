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
# ירוק על החיובי, ורוד על השלילי. לכל כותרת שני הקוטבים,
# כי כותרת שכולה כאב משאירה את הקורא בלי לאן ללכת, וגם מבטלת את
# מכשיר המותג של שני הצבעים.
# ארבע מודעות, ארבעה קהלים, לפי שאלה 1 בשאלון.
# הפתיחה בכל אחת היא מהאדם ומצבו, לעולם לא מהמוצר.
# ──────────────────────────────────────────────────────────────
# ארבע הכניסות הנעולות ממסמך האסטרטגיה, בניסוח כוללני.
#
# הכלל שמעל הכל: לעולם לא לגעת בכאב ישירות ולעולם לא
# להאשים. כל כותרת היא זוג: הבטחה לצד שרוצה, ושחרור לצד
# שמתנגד. ההבטחה יושבת על הקרייטיב, והשחרור בטקסט הראשי
# של המודעה במטא. לכן הוא כאן כ-primary ולא על התמונה.
#
# הבאדג׳ זהה בכולן ומתאר סוג עסק, לא חולשה. "עסקים שחיים
# על המלצות" היה האשמה, והוא דיבר ל-3% במקום ל-37%.
# באדג׳ לכל קהל, בנוסח של גל. כולם מתארים הישג ולא תלות,
# ולכן הם מדברים ל-37% ולא ל-3%. "עסקים שחיים על המלצות" היה
# האשמה. "עסקים שבנו לעצמם שם" היא מחמאה.

ADS = [
    {   # כניסה דרך הניחוש. הפותחת, כי היא מניחה רק שיש קמפיין
        "id": "a1_guess", "art": "art_7.png", "tag": u"\u05dc\u05e2\u05e1\u05e7\u05d9\u05dd \u05e9\u05de\u05d1\u05d9\u05d0\u05d9\u05dd \u05dc\u05e7\u05d5\u05d7\u05d5\u05ea \u05de\u05e4\u05e8\u05e1\u05d5\u05dd \u05de\u05de\u05d5\u05de\u05df",
        "h1": [u'במקום <span class="mark p">לנחש</span> למה הקמפיין לא מוכר,',
               u'אפשר <span class="mark g">לדעת</span> איפה הלקוח נעצר.'],
        "primary": u"בלי לפרק את מה שכבר בנית, ובלי להתחיל הכל מחדש.",
    },
    {   # כניסה דרך התסכול. כבוד המומחה אינו נתון למשא ומתן
        "id": "b2_expert", "art": "art_12.png", "tag": u"\u05dc\u05e2\u05e1\u05e7\u05d9\u05dd \u05e9\u05d1\u05e0\u05d5 \u05e0\u05d5\u05db\u05d7\u05d5\u05ea \u05d0\u05d5\u05e8\u05d2\u05e0\u05d9\u05ea",
        "h1": [u'<span class="mark g">המומחיות שלך</span> היא בתחום שלך.',
               u'לא צריך להיות מומחה גם <span class="mark p">בשיווק</span>.'],
        "primary": u"בלי ללמוד קמפיינים, ובלי עוד קורס שנשאר פתוח בלשונית.",
    },
    {   # כניסה דרך המדידה. צרה יותר בכוונה, ולכן לא פותחת
        "id": "c3_cost", "art": "art_14.png", "tag": u"\u05dc\u05e2\u05e1\u05e7\u05d9\u05dd \u05e9\u05de\u05d7\u05d1\u05e8\u05d9\u05dd \u05d1\u05d9\u05df \u05ea\u05d5\u05db\u05df, \u05e7\u05de\u05e4\u05d9\u05d9\u05e0\u05d9\u05dd \u05d5\u05d4\u05de\u05dc\u05e6\u05d5\u05ea",
        "h1": [u'<span class="mark g">ידוע לך</span> כמה עולה פנייה.',
               u'כמה עולה <span class="mark p">עסקה</span>, כבר פחות.'],
        "primary": u"בלי להחליף מערכות, ובלי להתחיל למדוד הכל מהיום.",
    },
    {   # כניסה דרך שליטה, לאיש הפה לאוזן. בלי ורוד בכוונה:
        # הזווית שלו היא תקרה ושליטה, לעולם לא כישלון
        "id": "d4_control", "art": "art_10.png", "tag": u"\u05dc\u05e2\u05e1\u05e7\u05d9\u05dd \u05e9\u05d1\u05e0\u05d5 \u05dc\u05e2\u05e6\u05de\u05dd \u05e9\u05dd \u05e9\u05e2\u05d5\u05d1\u05e8 \u05de\u05e4\u05d4 \u05dc\u05d0\u05d5\u05d6\u05df",
        "h1": [u'ידעת להביא לקוחות בלי לפרסם.',
               u'עכשיו גם <span class="mark g">לפתוח את הברז</span> בהחלטה שלך.'],
        "primary": u"גם בלי עוקבים, וגם בלי להעלות סרטונים לרשתות.",
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
        # מסגרת הקלף, אותה מסגרת של כרטיסיות סיפור הלקוח באתר: מסגרת
        # כפולה, פינה תחתונה שמאלית קטנה, וארבעה סימני פינה ורודים.
        # הערכים יחסיים, כדי שהיא תיראה זהה בכל פורמט.
        "cardM": "%.1fpx" % (u * 0.62), "cardB": "%.1fpx" % max(2.0, u * 0.055),
        "cardR": "%.1fpx %.1fpx %.1fpx %.1fpx" % (u * 1.45, u * 1.45, u * 1.45, u * 0.45),
        "cardI": "%.1fpx" % (u * 0.39),
        "cardIR": "%.1fpx %.1fpx %.1fpx %.1fpx" % (u * 1.10, u * 1.10, u * 1.10, u * 0.30),
        "tick": "%.1fpx" % (u * 0.72), "tickW": "%.1fpx" % max(2.0, u * 0.05),
        "tickO": "%.1fpx" % (u * 0.78),
        "markP": "%.1fpx %.1fpx %.1fpx" % (u * 0.05, u * 0.30, u * 0.16),
        "markR": "%.1fpx" % (u * 0.28),
        "markSY": "%.1fpx" % (u * 0.18), "markSB": "%.1fpx" % (u * 0.55),
        "brandGap": "%.1fpx" % (h * 0.008), "brandF": "%.1fpx" % (u * 0.44 * s),
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
