# -*- coding: utf-8 -*-
"""Document 11: every link in the funnel, in one place.

No password, key or token appears here on purpose. A PDF travels easily, and
if this one ever leaves Gal's hands it should hand nobody anything. Where a
credential is needed the document says where it lives, not what it is.
"""
import io
import os

D = u"C:/Users/HP/Downloads/\u05d4\u05de\u05e9\u05e4\u05da \u05e9\u05dc\u05d9 \u05d3\u05d9\u05d5\u05e7 \u05d3\u05d9\u05d2\u05d9\u05d8\u05dc\u05d9"
OUT = os.path.join(D, u"11-\u05de\u05e4\u05ea-\u05d4\u05e0\u05db\u05e1\u05d9\u05dd-\u05d4\u05d3\u05d9\u05d2\u05d9\u05d8\u05dc\u05d9\u05d9\u05dd.html")

CSS = u"""
.lnk{font-family:'Courier New',monospace;font-size:12.5px;color:#d81b73;
  direction:ltr;unicode-bidi:embed;display:inline-block;word-break:break-all}
td .lnk{font-size:12px}
.sec2{background:#fff;border:1px solid #dfdbe9;border-radius:14px;
  padding:14px 16px;margin:10px 0 0}
.sec2 b{display:block;font-size:14.5px;margin-bottom:3px}
.sec2 span{display:block;font-size:13px;color:#4f4d5e;line-height:1.6}
"""

# (כותרת, כתובת, מה זה, הערה)
PUBLIC = [
    (u"דף הבית", u"https://map.dg-gal.online",
     u"הדף הקצר. היעד של כל המודעות.",
     u"הפניה מפייסבוק מגיעה לכאן ולא לאתר הוותיק."),
    (u"השאלון", u"https://map.dg-gal.online/q/",
     u"עשר שאלות, שלושה מסלולים לפי התשובה הראשונה.",
     u"התשובות נשמרות, ויציאה רגעית לא מוחקת אותן."),
    (u"דף התוצאה", u"https://map.dg-gal.online/map/",
     u"המפה עצמה. נפתחת גם מקישור אישי.",
     u"בלי מזהה בכתובת היא מציגה מסך שאין מפה, וזה תקין."),
    (u"קישור אישי למפה", u"https://map.dg-gal.online/map/?id=\u2039\u05de\u05d6\u05d4\u05d4 \u05d4\u05dc\u05d9\u05d3\u203a",
     u"הקישור שנשלח בכל מייל מפה.",
     u"נפתח בכל מכשיר ובכל זמן, גם בעוד שנה, בלי לבקש כלום."),
    (u"דף הפגישות", u"https://map.dg-gal.online/call/",
     u"היומן, משובץ בצבעי המותג.",
     u"מתחת ליומן יש מייל וטלפון למי שלא מצא מועד."),
    (u"מדיניות הפרטיות", u"https://map.dg-gal.online/privacy/",
     u"בשפה פשוטה, כולל הפיקסל וההצפנה.",
     u"נפתחת תמיד בלשונית חדשה, כדי שלא לאבד שאלון באמצע."),
    (u"היומן עצמו", u"https://cal.com/dg-gal.online/map",
     u"אירוע ההזמנה ב-Cal.",
     u"פתוח שלושה ימים קדימה בלבד, במכוון."),
]

PRIVATE = [
    (u"הדשבורד", u"https://dash.dg-gal.online",
     u"רשימת השיחות לפי עדיפות, וכל תשובות האבחון.",
     u"מוגן בסיסמה. הסיסמה לא נמצאת במסמך הזה."),
]

ENGINE = [
    (u"מנוע המשפך", u"https://dg-gal-funnel.tom-harush.workers.dev",
     u"קולט לידים, שולח מיילים, מריץ את האוטומציות.",
     u"רץ על Cloudflare. לא נרדם, ולא עולה כלום."),
    (u"וובהוק היומן", u"https://dg-gal-funnel.tom-harush.workers.dev/cal",
     u"Cal מדווח לכאן על כל הזמנה, ביטול או שינוי מועד.",
     u"רשום בהגדרות Cal עם ארבעה אירועים."),
]

ASSETS = [
    (u"דומיין השליחה", u"send.dg-gal.online",
     u"כל המיילים יוצאים ממנו, מאומת ב-Resend."),
    (u"פיקסל", u"3520763671432860",
     u"מותקן על חמשת הדפים, ושולח גם משרת לשרת."),
    (u"חשבון המודעות", u"act_1188117450118774",
     u"שלוש המרות מותאמות וארבעה קהלי רימרקטינג."),
    (u"מספר הווטסאפ", u"050-9928400",
     u"ממנו יוצאות שבע האוטומציות."),
]

REPOS = [
    (u"galoskrt/dg-gal-map", u"חמשת דפי המשפך"),
    (u"galoskrt/dg-gal-dashboard", u"הדשבורד"),
    (u"galoskrt/leads-platform", u"הפלטפורמה הרב-דיירית, פרטי"),
]


def rows(items, four=True):
    out = []
    for it in items:
        if four:
            t, u, w, n = it
            out.append(u"<tr><td class=\"k\">%s</td><td><span class=\"lnk\">%s</span><br>%s<br>"
                       u"<b>%s</b></td></tr>" % (t, u, w, n))
        else:
            t, u, w = it
            out.append(u"<tr><td class=\"k\">%s</td><td><span class=\"lnk\">%s</span><br>%s</td></tr>"
                       % (t, u, w))
    return u"\n".join(out)


HTML = u"""<!doctype html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<title>מפת הנכסים הדיגיטליים · דיוק דיגיטלי</title>
<style>/*FONT*//*STYLE*/""" + CSS + u"""</style>
</head>
<body>
<div class="wrap">

<div class="cover">
  <p class="eyebrow">גל הרוש · דיוק דיגיטלי</p>
  <span class="docnum">מסמך 11 · מפת הנכסים הדיגיטליים · גרסה 1</span>
  <h1>מפת הנכסים הדיגיטליים</h1>
  <p class="subtitle">כל כתובת במשפך, מה היא עושה, ומה כדאי לדעת עליה. בלי סיסמאות ובלי מפתחות.</p>
  <div class="meta">
    <span><b>עבור:</b> העסק שלי, דיוק דיגיטלי</span>
    <span><b>תאריך:</b> 3 בספטמבר 2026</span>
  </div>
</div>

<div class="lead">
  <p><b>למה אין כאן אף סיסמה.</b> מסמך PDF עובר הלאה בקלות, בוואטסאפ, במייל, בטלפון של מישהו אחר. <b>אם המסמך הזה ידלוף, הוא לא ייתן לאיש כלום.</b> איפה שנדרש מפתח, המסמך אומר איפה הוא נמצא ולא מה הוא.</p>
</div>

<h2><span class="num">1</span> מה שהלקוח רואה <span class="tagr">ציבורי</span></h2>
<table>
  <thead><tr><th>נכס</th><th>כתובת ומה כדאי לדעת</th></tr></thead>
  <tbody>
%s
  </tbody>
</table>

<h2><span class="num">2</span> מה שאתה רואה <span class="tagr">מוגן</span></h2>
<table>
  <thead><tr><th>נכס</th><th>כתובת ומה כדאי לדעת</th></tr></thead>
  <tbody>
%s
  </tbody>
</table>
<div class="note">
  <span class="h">איך הדשבורד מוגן</span>
  הסיסמה נגזרת אצלך בדפדפן ב-600 אלף סבבים, <b>והתוצאה עצמה היא המפתח שהמנוע מכיר.</b> בקוד המקור של הדף אין שום סוד, <b>ולכן מי שיקרא אותו לא יקבל כלום.</b>
</div>

<h2><span class="num">3</span> המנוע <span class="tagr">לא נראה לאיש</span></h2>
<table>
  <thead><tr><th>רכיב</th><th>כתובת ומה כדאי לדעת</th></tr></thead>
  <tbody>
%s
  </tbody>
</table>

<h2><span class="num">4</span> נכסים נוספים</h2>
<table>
  <thead><tr><th>נכס</th><th>מזהה ומה הוא</th></tr></thead>
  <tbody>
%s
  </tbody>
</table>

<h2><span class="num">5</span> איפה הקוד יושב</h2>
<table>
  <thead><tr><th>מאגר</th><th>מה יש בו</th></tr></thead>
  <tbody>
%s
  </tbody>
</table>

<h2><span class="num">6</span> איפה נמצאים המפתחות</h2>
<div class="sec2">
  <b>לא במסמך הזה, ולא בשום מסמך.</b>
  <span>הסיסמה לדשבורד, הטוקנים של פייסבוק, המפתח של Resend, הטוקן של Green API והמפתח של Cloudflare <b>יושבים כולם בתיקיית סודות מקומית על המחשב שלך.</b> אף אחד מהם לא נמצא בקוד שפורסם, ולא בקבצי הזיכרון.</span>
</div>
<div class="sec2">
  <b>ואם מפתח כלשהו נחשף</b>
  <span>כל אחד מהם ניתן להחלפה בלי לגעת בקוד. <b>הכי דחוף להחליף הוא הטוקן של פייסבוק</b>, כי הוא היחיד שיכול להוציא כסף.</span>
</div>

<div class="close">
  <p><b>הקישור היחיד שכדאי לשמור בטלפון הוא הדשבורד.</b> כל השאר מגיעים אליך מעצמם: המפה במייל, הסיכום בעשר דקות, והפגישות בוואטסאפ.</p>
</div>

</div>
</body>
</html>
""" % (rows(PUBLIC), rows(PRIVATE), rows(ENGINE), rows(ASSETS, False),
       u"\n".join(u"<tr><td class=\"k\"><span class=\"lnk\">%s</span></td><td>%s</td></tr>" % r
                  for r in REPOS))

if __name__ == "__main__":
    io.open(OUT, "w", encoding="utf-8").write(HTML)
    print("written: %s  (%d KB)" % (os.path.basename(OUT), len(HTML.encode()) // 1024))
