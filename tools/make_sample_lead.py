# -*- coding: utf-8 -*-
u"""מייצר ליד לדוגמה דרך השאלון האמיתי, כדי שיהיה מזהה תקין ל-audit.py.

למה דרך השאלון ולא בבנייה ידנית של מטען: compute() בשאלון הוא לוגיקה
עסקית שמשתנה, ולשחזר אותה ביד פירושו שתי מקורות אמת שיכולים להיפרד.
מריצים את הדפדפן האמיתי מול הקוד האמיתי.

בטיחות, לפי הכלל: אין טלפון אמיתי, ואין אימייל אמיתי, וברגע שהמזהה
בידיים מסמנים demo:true מיד, לפני שהקרון של הוואטסאפ יכול להגיע אליו.
שם העסק מסומן במפורש כבדיקה כדי שאף אחד לא יתבלבל בדשבורד.

© כל הזכויות שמורות · דיוק דיגיטלי · גל הרוש 2026
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8779
BASE = "http://127.0.0.1:%d" % PORT
WORKER = "https://dg-gal-funnel.tom-harush.workers.dev"

SEC = (r"C:\Users\HP\AppData\Local\Temp\claude\C--Users-HP"
       r"\473a8323-6f8a-4eeb-a233-1f7f54aa30bf\scratchpad\secrets")


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read().strip()


def serve():
    return subprocess.Popen([sys.executable, "-m", "http.server", str(PORT),
                             "--bind", "127.0.0.1", "-d", ROOT],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def patch(id_, token):
    req = urllib.request.Request(
        WORKER + "/lead/" + id_, method="PATCH",
        data=json.dumps({"demo": True, "business": u"בדיקת audit, לא ליד אמיתי"}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token,
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dg-gal-audit/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=15).read())


def main():
    token = read(os.path.join(SEC, "dash_derived.txt"))
    srv = serve()
    time.sleep(1.2)
    lead_id = []
    try:
        with sync_playwright() as p:
            br = p.chromium.launch()
            page = br.new_page(viewport={"width": 390, "height": 844})

            def on_response(res):
                if res.url.endswith("/lead") and res.request.method == "POST":
                    try:
                        j = res.json()
                        if j.get("id"):
                            lead_id.append(j["id"])
                    except Exception:
                        pass
            page.on("response", on_response)

            page.goto(BASE + "/q/?utm_term=a1-guess&utm_content=broad-feed"
                       "&utm_campaign=leakmap-sep26", wait_until="load")
            for _ in range(20):
                if page.locator("#i-name").count():
                    break
                page.locator(".opt").first.click()
                page.wait_for_timeout(320)
                if page.locator("#next").is_enabled():
                    page.locator("#next").click()
                page.wait_for_timeout(220)
            page.fill("#i-name", u"בדיקת audit")
            page.fill("#i-biz", u"בדיקת audit, לא ליד אמיתי")
            page.fill("#i-phone", "0500000000")
            page.fill("#i-mail", "audit-sample@example.com")
            page.check("#i-ok")
            page.click("#next")
            page.wait_for_timeout(6500)
            br.close()
    finally:
        srv.terminate()

    if not lead_id:
        print(u"  FAIL: לא נתפס מזהה מתשובת /lead")
        return 1

    lid = lead_id[0]
    print(u"  ליד נוצר: %s" % lid)
    r = patch(lid, token)
    print(u"  demo=true נשלח, תשובת השרת: ok=%s" % r.get("ok"))
    wa = (r.get("lead") or {}).get("wa")
    print(u"  שדה wa על הליד: %s" % (wa if wa else u"ריק, שום הודעה לא נשלחה"))

    with open(os.path.join(ROOT, "tools", "_e2e_id.txt"), "w", encoding="utf-8") as f:
        f.write(lid)
    print(u"  tools/_e2e_id.txt עודכן")
    return 0


if __name__ == "__main__":
    sys.exit(main())
