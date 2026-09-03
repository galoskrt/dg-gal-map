# -*- coding: utf-8 -*-
u"""החזרה ממדיניות הפרטיות, נבדקת כמו שאדם חווה אותה.

הכשל שהוליד את הקובץ: הקישור נפתח בלשונית חדשה, ובלשונית חדשה אין
היסטוריה, אז history.back() לא עשה כלום. מסך הטעינה נשאר מסתובב, וגל
נטש. זה קרה שנייה לפני שליחת הטופס, נקודת הנטישה היקרה ביותר במשפך.

הבדיקה מריצה את המסלול המלא: עונים על השאלון, מקלידים פרטים, יוצאים
למדיניות, חוזרים, ומוודאים שהכל עדיין שם. ובנוסף את המקרה הפתולוגי,
כניסה ישירה למדיניות בלי היסטוריה בכלל.

הכל מול מה שנבנה ונשלח, לא מול המקור.

© כל הזכויות שמורות · דיוק דיגיטלי · גל הרוש 2026
"""
import os
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8777
BASE = "http://127.0.0.1:%d" % PORT

FIELDS = {"i-name": u"בדיקה חוזרת", "i-biz": u"סטודיו בדיקה, ייעוץ",
          "i-phone": "0501234567", "i-mail": "check@example.com"}

fails = []


def ok(cond, msg):
    print((u"  ok    " if cond else u"  FAIL  ") + msg)
    if not cond:
        fails.append(msg)


def serve():
    return subprocess.Popen([sys.executable, "-m", "http.server", str(PORT),
                             "--bind", "127.0.0.1", "-d", ROOT],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def fill_survey(page):
    u"""עד מסך הפרטים, ואז מקלידים בו."""
    for _ in range(20):
        if page.locator("#i-name").count():
            break
        page.locator(".opt").first.click()
        page.wait_for_timeout(320)
        if page.locator("#next").is_enabled():
            page.locator("#next").click()
        page.wait_for_timeout(220)
    for k, v in FIELDS.items():
        page.fill("#" + k, v)
    page.check("#i-ok")
    page.wait_for_timeout(150)


def main():
    srv = serve()
    time.sleep(1.2)
    try:
        with sync_playwright() as p:
            br = p.chromium.launch()
            ctx = br.new_context(viewport={"width": 390, "height": 844})

            # ── המסלול האמיתי
            page = ctx.new_page()
            page.goto(BASE + "/q/?utm_term=a1-guess", wait_until="load")
            fill_survey(page)
            ok(page.locator("#i-name").count() == 1, u"הגענו למסך הפרטים")

            link = page.locator(".consent a")
            ok(link.get_attribute("target") is None,
               u"קישור המדיניות נפתח באותה לשונית, לא בלשונית חדשה")

            before = len(ctx.pages)
            link.click()
            page.wait_for_url("**/privacy/**", timeout=5000)
            ok(len(ctx.pages) == before, u"לא נפתחה לשונית נוספת")

            t0 = time.time()
            page.click("button.cta.quiet")
            page.wait_for_url("**/q/**", timeout=5000)
            page.wait_for_selector("#i-name", timeout=5000)
            back_ms = int((time.time() - t0) * 1000)
            ok(back_ms < 2500, u"החזרה לשאלון ארכה %d מילישניות" % back_ms)

            for k, v in FIELDS.items():
                got = page.input_value("#" + k)
                ok(got == v, u"השדה %s חזר עם מה שהוקלד" % k)
            ok(page.is_checked("#i-ok"), u"סימון ההסכמה חזר")
            ok(page.locator("#qn").inner_text().strip() == u"שאלה 10 מתוך 10",
               u"חזרנו בדיוק לשאלה שבה היינו")
            ok(page.locator(".proof").count() == 1, u"מסך הפרטים נבנה במלואו")

            # ── המקרה שנתקע: כניסה ישירה, בלי היסטוריה
            fresh = ctx.new_page()
            fresh.goto(BASE + "/privacy/", wait_until="load")
            ok(fresh.evaluate("document.referrer") == "",
               u"נחתנו כאן בלי מאיפה לחזור, בדיוק כמו בתקלה")
            fresh.click("button.cta.quiet")
            fresh.wait_for_timeout(1600)
            stuck = fresh.evaluate(
                "!!document.querySelector('.gate.on')"
                " && location.pathname.indexOf('/privacy') === 0")
            ok(not stuck, u"בלי היסטוריה לא נתקעים על מסך הטעינה")
            ok(fresh.url.rstrip("/").endswith("127.0.0.1:%d" % PORT),
               u"בלי היסטוריה נוחתים בעמוד הבית, ולא בשום מקום")

            # ── חזרה לעמוד המדיניות דרך המטמון לא משאירה מסך דלוק
            page.goto(BASE + "/privacy/", wait_until="load")
            page.evaluate("document.getElementById('gate').classList.add('on')")
            page.go_back()
            page.wait_for_timeout(300)
            page.go_forward()
            page.wait_for_timeout(500)
            ok(not page.evaluate("!!document.querySelector('.gate.on')"),
               u"מסך הטעינה כבוי גם בחזרה מהמטמון")

            br.close()
    finally:
        srv.terminate()

    print(u"\n  %s" % (u"הכל עבר" if not fails else u"%d כשלים" % len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
