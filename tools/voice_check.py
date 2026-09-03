# -*- coding: utf-8 -*-
"""שער ניסוח כוללני על הקופי של המודעות.

הכלל של גל, כפי שתיקן אותו ב-01/09/2026: ניסוח כוללני אינו רבים. הוא גוף
שני יחיד שנשען על הצורות שנכתבות זהה לזכר ולנקבה בכתיב חסר ניקוד. עבר,
סיומת ך, שם פועל, שם פעולה, ואישי-כללי.

הבדיקה סורקת את הקופי שנכנס למודעות, לא את מה שמישהו זוכר שכתב.

★ הגרסה הראשונה של הקובץ הזה נכשלה בדיוק במה שהיא נועדה לתפוס. היא
חיפשה "אתה" עם גבול מילה עברי, ולכן "ואתה מקבל", המשפט שהופיע בפועל
בכל ארבע עשרה המודעות, חמק ממנה בגלל וי"ו החיבור. לכן הבדיקה מפרקת
עכשיו למילים ומקלפת אותיות שימוש, ולא נשענת על גבול מילה.

© כל הזכויות שמורות · דיוק דיגיטלי · גל הרוש 2026
"""
import re
import sys

import build_ads as B

PREFIX = u"ובכלמשה"          # אותיות שימוש שנדבקות לתחילת מילה
STRIP = u'".,:;!?()״׳\''

# צורות שנושאות מגדר, ולכן אסורות בפנייה לקורא
BANNED = {
    u"אתה": u"גוף שני זכר",
    u"אתם": u"רבים", u"אתן": u"רבים", u"שלכם": u"רבים", u"לכם": u"רבים",
    u"עבורכם": u"רבים", u"תוכלו": u"רבים", u"קחו": u"רבים",
    u"תפסיק": u"ציווי זכר", u"תתחיל": u"ציווי זכר", u"מלא": u"ציווי זכר",
    u"קח": u"ציווי זכר", u"בחר": u"ציווי זכר", u"צפה": u"ציווי זכר",
    u"תדע": u"עתיד זכר", u"תקבל": u"עתיד זכר", u"תבדוק": u"עתיד זכר",
    u"תחליט": u"עתיד זכר", u"תראה": u"עתיד זכר",
    u"יודע": u"הווה זכר", u"מרגיש": u"הווה זכר", u"מקבל": u"הווה זכר",
    u"רוצה": u"הווה, זהה לשני המגדרים אבל נקרא כזכר בהקשר פנייה",
}

# מונחים שאסורים בקופי מול לקוח
# "את" הוא גם כינוי גוף וגם מילת יחס, ומילת היחס נפוצה בהרבה. שער
# שנופל על כל "את" הוא שער שמפסיקים להקשיב לו, אז הוא מזהיר ולא מכשיל.
WARN = {u"את": u'אם זה כינוי גוף ולא מילת יחס, זה מגדרי'}

JARGON = {u"ליד": u'בשפת לקוח אומרים "פניות"',
          u"לידים": u'בשפת לקוח אומרים "פניות"'}

DASH = re.compile(u"[–—]")
EMOJI = re.compile(u"[\U0001F300-\U0001FAFF☀-➿⬀-⯿]")

fails = []
warns = []


def forms(token):
    """המילה עצמה, וגם היא בלי אות שימוש אחת או שתיים בתחילתה."""
    t = token.strip(STRIP)
    out = {t}
    if len(t) > 2 and t[0] in PREFIX:
        out.add(t[1:])
        if len(t) > 3 and t[1] in PREFIX:
            out.add(t[2:])
    return out


def check(label, text):
    plain = re.sub(r"<[^>]+>", " ", text)
    plain = re.sub(r"\s+", " ", plain).strip()
    for token in plain.split():
        cand = forms(token)
        for word, why in BANNED.items():
            if word in cand:
                fails.append(u"%s: מופיע \"%s\" (%s)" % (label, token, why))
        for word, why in JARGON.items():
            if word in cand:
                fails.append(u"%s: מופיע \"%s\", %s" % (label, token, why))
        for word, why in WARN.items():
            if word in cand:
                warns.append(u"%s: \"%s\", %s" % (label, token, why))
    if DASH.search(plain):
        fails.append(u"%s: מקף ארוך" % label)
    if EMOJI.search(plain):
        fails.append(u"%s: אמוג'י" % label)
    words = [w for w in plain.split() if w.strip(STRIP)]
    if len(words) > 3 and len(words[-1].strip(STRIP)) <= 2:
        fails.append(u"%s: השורה נגמרת במילה בודדת קצרה" % label)


def run():
    del fails[:]
    del warns[:]
    for ad in B.ADS:
        check(ad["id"] + u" תג", ad["tag"])
        for i, line in enumerate(ad["h1"]):
            check(u"%s כותרת %d" % (ad["id"], i + 1), line)
    check(u"רצועה", B.SPEC3)
    check(u"כפתור", B.CTA)
    return list(fails)


if __name__ == "__main__":
    bad = run()
    for w in warns:
        print(u"  warn  " + w)
    for f in bad:
        print(u"  FAIL  " + f)
    if bad:
        print(u"\n  %d כשלים" % len(bad))
        sys.exit(1)
    n = sum(1 + len(a["h1"]) for a in B.ADS) + 2
    print(u"  %d מקטעי קופי, כולם כוללניים ונקיים" % n)
