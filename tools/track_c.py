# -*- coding: utf-8 -*-
"""The third track: a business built on content.

Somebody whose customers come from what they publish was being routed into the
referral track and asked how many came from a recommendation, then told their
income depends on people remembering to refer them. That is wrong twice. An
audience built on content is an asset, not a memory, and being told otherwise
reads as "he did not understand me", which is the fastest way to lose exactly
the audience Gal most wants: a working business with revenue and trust already
built, that wants to add a paid channel.

Their leak is different in kind. In paid, money bleeds between the inquiry and
the sale. In referrals, money is never created. In content, the money exists
and the ceiling is the person themselves.
"""
import io

CHAPTERS = u"var CH_C = ['מאיפה מגיעים הלקוחות','מה התוכן מייצר','מה קורה אחרי'];"

QUESTIONS = u"""
/* מסלול ג: העסק בנוי על תוכן. הפניות מגיעות ממי שכבר צרך, כבר מכיר, וכבר
   בנה אמון, ולכן השאלות על המלצות פשוט לא רלוונטיות לו. */
var QC = [
 { ch:0, q:'כמה פניות בחודש מגיעות מהתוכן שלך?', k:'leads', o:[
   [0.2,'p','עד 5','כל פנייה כאן יקרה, כי היא עלתה בזמן ולא בכסף.',1,5],
   [0.5,'o','בין 5 ל-15','יש זרימה. השאלה היא מה קורה לה אחר כך.',2,12],
   [0.75,'o','בין 15 ל-40','התוכן כבר עובד כמו ערוץ לכל דבר.',2,28],
   [1,'g','מעל 40','נפח שרוב העסקים הממומנים לא מגיעים אליו.',2,55]]},

 { ch:1, q:'כמה מהפניות האלה מגיעות לשיחה אמיתית?', k:'reach', o:[
   [0.9,'p','מיעוט מהן','רוב מי שפנה נעצר לפני שהיה סיכוי.',3,0.70],
   [0.7,'o','בערך חצי','חצי מהעניין שנוצר לא מגיע לשולחן.',2,0.50],
   [0.45,'o','רובן','יש כאן תהליך שעובד, עם דליפה קטנה.',1,0.28],
   [0.2,'g','כמעט כולן','נדיר. מי שפנה מגיע לדבר.',0,0.15]]},

 { ch:1, q:'מתוך השיחות, כמה הופכות ללקוח?', k:'close', o:[
   [0.25,'p','פחות מעשירית','העניין מגיע ולא מבשיל. זה לא חוסר בפניות.',3,0.08],
   [0.5,'o','בערך רבע','טווח נורמלי, ויש בו מקום גדול לשיפור.',2,0.25],
   [0.75,'o','בערך חצי','אחוז גבוה. סימן שהאמון כבר נבנה מראש.',1,0.45],
   [1,'g','יותר מחצי','מי שמגיע לשיחה כבר החליט. זה נכס.',0,0.62]]},

 { ch:1, q:'כמה שווה לקוח חדש, בממוצע, בשנה הראשונה?', k:'value', o:[
   [0.2,'p','עד 5,000 ₪','נדרש נפח כדי שהמתמטיקה תעבוד.',0,3500],
   [0.45,'o','בין 5,000 ל-15,000','הטווח שבו ערוץ ממומן מתחיל להשתלם.',2,10000],
   [0.75,'o','בין 15,000 ל-50,000','כל מקום פנוי ביומן הוא סכום שמרגישים.',3,30000],
   [1,'g','מעל 50,000','לקוח אחד נוסף בחודש משנה את השנה.',3,70000]]},

 /* השאלה שגל הוסיף, והיא מפרידה בין מי שיש לו נכס המרה למי שהתוכן
    שלו הוא גם הפרסום וגם דף המכירה. בלי דף שמחמם, כל שיחה מתחילה מאפס. */
 { ch:1, q:'כשמישהו מתעניין, יש לו איפה ללמוד על השירות עצמו?', k:'page', o:[
   [0.2,'g','יש דף שמסביר הכל','נכס המרה שעובד גם כשלא מפרסמים.',0,0],
   [0.55,'o','יש עמוד כללי באתר','קיים, אבל הוא לא מחמם ולא מסביר.',2,0.16],
   [0.95,'p','הכל דרך התוכן והשיחה','כל שיחה מתחילה מאפס, ואת ההסבר נותנים בעל פה.',3,0.30]]},

 { ch:2, q:'יש הצעה מנוסחת שחוזרת בכל שיחה?', k:'offer', o:[
   [0.2,'g','כן, ברורה וקבועה','אפשר לשכפל הצלחה, כי יודעים מה נאמר.',0,0],
   [0.6,'o','משהו כללי','הכיוון קיים, הניסוח משתנה.',2,0.10],
   [1,'p','כל שיחה יוצאת אחרת','אי אפשר ללמוד ממה שעבד, כי לא ברור מה נאמר.',3,0.20]]},

 { ch:2, q:'מה קורה בחודש שבו כמעט לא העלית תוכן?', k:'dry', o:[
   [0.2,'g','יש ערוץ נוסף שעובד','לא הכל תלוי בקצב שלך. זה נדיר.',0,0],
   [0.6,'o','הפניות יורדות, אבל יש מלאי','יש חמצן, והוא נגמר.',2,1],
   [1,'p','הפניות נעצרות כמעט לגמרי','הערוץ היחיד הוא הזמן שלך.',3,2]]},

 { ch:2, q:'ניסית פרסום ממומן?', k:'tried', o:[
   [0.35,'o','מעולם לא','אין כאן שריפה, יש כאן ערוץ שעוד לא נפתח.',1,0],
   [0.85,'p','ניסית לבד ולא הצליח','הבעיה כמעט תמיד לפני הקמפיין, לא בתוכו.',3,0],
   [1,'p','היה ליווי ולא עבד','שילמת פעם אחת על מה שלא הוגדר מראש.',3,0],
   [0.5,'o','רץ עכשיו במקביל','יש שני ערוצים, וצריך לדעת מה כל אחד מביא.',2,0]]},

 { ch:2, q:'ידוע לך כמה עולה לך להשיג לקוח, בזמן ולא בשקלים?', k:'cac', o:[
   [0.2,'g','כן, בערך','יש מספר להשוות אליו כשתשקול ממומן.',0,0],
   [0.75,'o','לא, כי התוכן לא עולה כסף','הוא עולה את הזמן שלך, וזה המשאב היקר.',2,1],
   [1,'p','לא חשבנו על זה ככה','בלי המספר הזה אין לדעת אם ערוץ נוסף זול או יקר.',2,2]]}
];
"""

MONEY = u"""  } else if(S.track === 'c'){
    /* אותה פיזיקה של מסלול א: פניות נכנסות, חלק לא מגיע לשיחה, וחלק ממי
       שכן היה נסגר. מה שמשתנה הוא כמה מזה בר השבה, וכאן זה נגזר משני
       הדברים שחסרים דווקא לעסק שבנוי על תוכן: דף שמחמם והצעה מנוסחת. */
    var cLeads = a.leads.val, cMiss = a.reach.val, cClose = a.close.val, cVal = a.value.val;
    var recover = Math.max(0.15, (a.page.val || 0) + (a.offer.val || 0));
    main = roundDown(cLeads * cMiss * recover * cClose * cVal);
    rows = [
      ['פניות מהתוכן בחודש', a.leads.label],
      ['לא מגיעות לשיחה', a.reach.label],
      ['מקום ללמוד על השירות', a.page.label],
      ['הצעה מנוסחת', a.offer.label],
      ['סגירה מתוך השיחות', a.close.label],
      ['שווי לקוח בשנה הראשונה', a.value.label]
    ];
"""

SCORE = u"""  } else if(S.track === 'c'){
    /* עיוורון אצל מי שבנוי על תוכן: אין דף שמחמם, אין הצעה מנוסחת,
       ואין מושג כמה עולה לקוח. כולם ניתנים לתיקון, וזו בדיוק הנקודה. */
    if(a.page && a.page.i === 2) blind++;
    if(a.offer) blind += (a.offer.val > 0 ? 1 : 0);
    if(a.cac) blind += a.cac.val;
    if(a.dry && a.dry.i === 2) blind++;
    if(a.tried && (a.tried.i === 1 || a.tried.i === 2)) burn = true;
"""

LEAKS = u"""  } else if(d.track === 'c'){
    if(a.dry && a.dry.i === 2)
      out.push({k:'p',w:5,h:'התקרה היא הזמן שלך',t:'התוכן מייצר את הפניות, ואי אפשר להכפיל אותן בלי להכפיל אותך.'});
    if(a.page && a.page.i === 2)
      out.push({k:'p',w:5,h:'אין איפה ללמוד על השירות',t:'מי שמתעניין מגיע לשיחה בלי לדעת מה בדיוק מוצע, וכל שיחה מתחילה מאפס.'});
    if(a.reach && (a.reach.i === 0 || a.reach.i === 1))
      out.push({k:'o',w:4,h:'עניין שלא מגיע לשולחן',t:'האמון כבר נבנה בתוכן. הפנייה נעצרת אחריו, ובדיוק שם נגמר הסיפור.'});
    if(a.offer && a.offer.i !== 0)
      out.push({k:'g',w:3,h:'הצעה שלא מנוסחת',t:'כשכל שיחה יוצאת אחרת אי אפשר ללמוד ממה שעבד, וגם אי אפשר להעביר את זה הלאה.'});
    if(a.close && a.close.i === 0)
      out.push({k:'o',w:3,h:'סגירה בשיחה',t:'הקהל מגיע חם ולא הופך ללקוח. זו לא בעיית תנועה, וכדאי לדעת את זה לפני שקונים תנועה.'});
    if(a.cac && a.cac.i !== 0)
      out.push({k:'g',w:2,h:'לתשומת הלב אין מחיר',t:'התוכן מרגיש חינם, ולכן אין מספר להשוות אליו כשתשקול ערוץ נוסף.'});
"""

if __name__ == "__main__":
    s = io.open("survey.html", encoding="utf-8").read()

    assert "var QC" not in s, "track C already present"
    s = s.replace("var SRC2TRACK = { paid:'a', mix:'a', ref:'b', org:'b' };",
                  "/* אורגני קיבל את שאלות ההמלצות ונאמר לו שהוא תלוי בזיכרון של אנשים.\n"
                  "   מי שבנה קהל בתוכן בנה נכס, ולכן יש לו מסלול משלו. */\n"
                  "var SRC2TRACK = { paid:'a', mix:'a', ref:'b', org:'c' };")
    s = s.replace("var CH_B = ['מאיפה מגיעים הלקוחות','הקצב והתקרה','כשהברז נסגר'];",
                  "var CH_B = ['מאיפה מגיעים הלקוחות','הקצב והתקרה','כשהברז נסגר'];\n" + CHAPTERS)
    s = s.replace("function qs(){ return S.track === 'a' ? QA : QB; }",
                  "function qs(){ return S.track === 'a' ? QA : (S.track === 'c' ? QC : QB); }")
    s = s.replace("function chapters(){ return S.track === 'b' ? CH_B : CH_A; }",
                  "function chapters(){ return S.track === 'c' ? CH_C : (S.track === 'b' ? CH_B : CH_A); }")

    i = s.rindex("var QB")
    j = s.index("\n];", i) + 3
    s = s[:j] + "\n" + QUESTIONS + s[j:]

    # המודל הכספי
    k = s.index("  } else {\n    main  = roundDown(a.clients.val")
    s = s[:k] + MONEY + s[k + len("  } else {\n"):]

    # ניקוד העיוורון
    m = s.index("  } else {\n    if(a.refer && a.refer.i === 0) blind++;")
    s = s[:m] + SCORE + s[m + len("  } else {\n"):]

    # כותרת הסכום למסלול ג היא main, כמו במסלול א
    s = s.replace("var headline = (S.track === 'b') ? (extra || main) : main;",
                  "var headline = (S.track === 'b') ? (extra || main) : main;")
    io.open("survey.html", "w", encoding="utf-8").write(s)
    print("survey: track C wired")

    l = io.open("leaks.js", encoding="utf-8").read()
    n = l.index("  } else {\n    if(a.refer && (a.refer.i === 0 || a.refer.i === 1))")
    l = l[:n] + LEAKS + l[n + len("  } else {\n"):]
    io.open("leaks.js", "w", encoding="utf-8").write(l)
    print("leaks: track C library added")
