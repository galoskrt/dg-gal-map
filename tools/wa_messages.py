# -*- coding: utf-8 -*-
"""The seven WhatsApp messages, in Gal's voice, after his revisions.

His rules: inclusive phrasing that reads correctly whoever opens it (second
person with the ך ending, impersonal imperatives, never אתה and never אתם), no
dashes, no orphan words, and a diagnostician's voice rather than a seller's.
The length of the call is never named, because "forty minutes on Zoom" reads
as a commitment before there is a reason for one.

Two of his corrections are the same lesson twice. "There is nothing to sell
here" is a claim; pointing at a map already waiting in the inbox is evidence.
And offering to reschedule in every message reads as somebody with a lot of
cancellations, which is the opposite of the position this funnel holds. His
calendar is deliberately open three days ahead and no further, so there is
little to cancel in the first place.

Emojis appear here and only here, at his explicit request. On a page they read
as noise; in a WhatsApp thread they close distance.

Placeholders: {name} first name, {link} the booking page, {map} that person's
own map link, {zoom} that meeting's own room, {when} day and hour in Hebrew.
"""

MESSAGES = {

    # ── 1 ──────────────────────────────────────────────────────────────────
    # שעה אחרי המפה. נכנסו, צפו בסרטון, ולא נגעו בקביעת מועד.
    # מי שצפה כבר יודע מה יש שם, אז אין טעם להסביר שוב. החסם הוא הצעד.
    "watched_no_booking": {
        "when": "שעה אחרי שהמפה נשלחה",
        "who": "נכנס למפה, הפעיל את הסרטון, ולא נגע בקביעת מועד",
        "text": (
            "היי {name}, גל הרוש.\n"
            "\n"
            "ראיתי שהמפה שלך נפתחה.\n"
            "\n"
            "שאלה אחת ותשובה כנה תספיק לי: המספר שיצא שם נראה מדויק, "
            "או רחוק ממה שקורה בפועל?\n"
            "\n"
            "אם הוא רחוק, אפשר להשיב כאן ואסביר בדיוק מאיפה הוא הגיע.\n"
            "אם הוא מדויק, אז יש שם שלוש נקודות ששוות שיחה אחת.\n"
            "\n"
            "{link}"
        ),
    },

    # ── 2 ──────────────────────────────────────────────────────────────────
    # שעתיים אחרי. פחות מדקה בדף, בלי לגעת בסרטון.
    # מפנים אל המפה שכבר מחכה במייל, ומשם המשפך ממשיך לרוץ לבד.
    "bounced_fast": {
        "when": "שעתיים אחרי שהמפה נשלחה",
        "who": "שהה פחות מדקה במפה ולא הפעיל את הסרטון",
        "text": (
            "היי {name}, גל הרוש.\n"
            "\n"
            "המפה שמילאת מחכה לך, ונראה שלא היה זמן לפתוח אותה.\n"
            "\n"
            "בתוכה יש מספר אחד, שלוש נקודות שבהן הוא נוצר, "
            "והחישוב עצמו גלוי כדי שאפשר יהיה לבדוק אותי.\n"
            "\n"
            "אני ממליץ לך לבדוק את המייל שלך, המפה מחכה לך שם "
            "ולא הולכת לשום מקום, וכשזה ירגיש לך נכון אפשר לכתוב לי כאן, "
            "אני עונה על הכל בעצמי :)"
        ),
    },

    # ── 3 ──────────────────────────────────────────────────────────────────
    # מיד עם קביעת הפגישה. מסירים את החרדה של "מה יקרה שם".
    # בלי הצעה להזיז: היומן פתוח שלושה ימים בלבד, ואוטומציה 4 תטפל בזה אם צריך.
    "booked_confirm": {
        "when": "מיד כשנקבעה פגישה",
        "who": "כל מי שקבע",
        "text": (
            "היי {name}, נקבע.\n"
            "\n"
            "{when}\n"
            "\n"
            "מה שקורה שם: עוברים על המפה שלך שורה שורה, "
            "מסתכלים על שלוש הנקודות לפי סדר הכסף שיושב על כל אחת, "
            "ויוצאים עם סדר עדיפויות ברור.\n"
            "\n"
            "לא צריך להביא כלום. אם יש נתון שקל להשיג עד אז, "
            "כמה פניות נכנסו בחודש האחרון וכמה מהן הפכו לעסקה, "
            "השיחה תהיה מדויקת יותר."
        ),
    },

    # ── 4 ──────────────────────────────────────────────────────────────────
    # 48 שעות לפני, ורק אם הפגישה נקבעה למרחק גדול יותר מזה.
    # זו האוטומציה היחידה שמזכירה שינוי מועד, ולכן היא לא נשמעת כתחנון.
    "remind_48h": {
        "when": "48 שעות לפני, רק אם נקבעה ליותר מ-48 שעות מראש",
        "who": "כל מי שקבע ולא ביטל",
        "text": (
            "היי {name}, תזכורת קטנה.\n"
            "\n"
            "השיחה שלנו {when}.\n"
            "\n"
            "אם משהו השתנה ביומן, אפשר להשיב כאן ונמצא מועד אחר."
        ),
    },

    # ── 5 ──────────────────────────────────────────────────────────────────
    # 24 שעות לפני. לא מבקשים אישור ולא מציעים להזיז. סימון אגודל הוא
    # מחווה קטנה שמייצרת מחויבות בלי לבקש התחייבות.
    "remind_24h": {
        "when": "24 שעות לפני",
        "who": "כל מי שקבע ולא ביטל",
        "text": (
            "היי {name}, מחר {when}.\n"
            "\n"
            "המפה שלך פתוחה מולי ואני עובר עליה לפני שנדבר.\n"
            "\n"
            "נתראה בפגישה, אפשר לסמן \U0001F44D להודעה הזו, "
            "ואם יש שאלה אפשר לכתוב לי כאן, אני אענה בהקדם :)"
        ),
    },

    # ── 6 ──────────────────────────────────────────────────────────────────
    # שעתיים לפני, עם סרטון ההוכחה. מראים מישהו שכבר עבר את זה,
    # ואומרים מה קורה עכשיו במקום להכריז מה לא יקרה.
    "remind_2h": {
        "when": "שעתיים לפני",
        "who": "כל מי שקבע ולא ביטל",
        "text": (
            "היי {name}, נדבר בעוד שעתיים.\n"
            "\n"
            "עד אז, זה מישהו שישב במקום שלך לפני כמה חודשים "
            "ומספר בעצמו מה השתנה אצלו.\n"
            "\n"
            "עוד שעתיים נעלה לשיחה, והקישור יישלח אליך פה עשר דקות לפני."
        ),
        "media": "סרטון ההוכחה החברתית, גל מייצר חדש",
    },

    # ── 7 ──────────────────────────────────────────────────────────────────
    # 10 דקות לפני, עם החדר של אותה פגישה בלבד.
    "remind_10m": {
        "when": "10 דקות לפני",
        "who": "כל מי שקבע ולא ביטל",
        "text": (
            "היי {name}, מתחילים בעוד עשר דקות.\n"
            "\n"
            "{zoom}\n"
            "\n"
            "אפשר להיכנס מהטלפון או מהמחשב, מה שנוח.\n"
            "\n"
            "יהיה גם כיף, לא רק ביזנס \U0001F60E"
        ),
    },
}

ORDER = ["watched_no_booking", "bounced_fast", "booked_confirm",
         "remind_48h", "remind_24h", "remind_2h", "remind_10m"]

# חלון השליחה, לפי הקהל של גל: רובם עובדים ביום, גוללים בערב, וקמים מוקדם.
# ליד שנכנס ב-07:00 מקבל תוך שעה, ומי שהשאיר בלילה מוצא הודעה כשהוא קם.
SEND_WINDOW = (8, 22)

if __name__ == "__main__":
    import io
    import re

    out, bad, note = [], [], []
    for i, k in enumerate(ORDER, 1):
        m = MESSAGES[k]
        out.append("=" * 66)
        out.append("%d. %s" % (i, m["when"]))
        out.append("   למי: %s" % m["who"])
        if m.get("media"):
            out.append("   מצורף: %s" % m["media"])
        out.append("")
        out.append(m["text"])
        out.append("")
        t = m["text"]
        if re.search(u"[–—]", t):
            bad.append("%s has a dash" % k)
        for g in (u"אתה", u"אתם", u"שלכם", u"תגיד", u"תכתוב", u"תבדוק", u"תאשר"):
            if re.search(u"(?<![֐-׿])" + g + u"(?![֐-׿])", t):
                bad.append("%s uses %s" % (k, g))
        if len(t) > 700:
            bad.append("%s is %d characters, long for WhatsApp" % (k, len(t)))
        # אמוג'ים מותרים כאן ורק כאן, בבקשה מפורשת של גל
        emo = re.findall(u"[\U0001F300-\U0001FAFF☀-➿]", t)
        if emo:
            note.append("%s: %s" % (k, "".join(emo)))

    out.append("=" * 66)
    out.append("")
    out.append("חלון שליחה: %02d:00 עד %02d:00" % SEND_WINDOW)
    out.append("בדיקה: %s" % ("; ".join(bad) if bad
                              else "כל שבעת הנוסחים עומדים בכללים"))
    if note:
        out.append("אמוג'ים, מכוונים: %s" % "; ".join(note))
    body = "\n".join(out)
    io.open("wa_messages.txt", "w", encoding="utf-8").write(body)
    print(body)
