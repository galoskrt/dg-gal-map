# -*- coding: utf-8 -*-
"""חותך את האובייקט מתוך מודעה שכבר יוצרה, ומכין אותו לרקע חדש.

שלוש פעולות, וכל אחת נדרשה אחרי שהסתכלתי על התוצאה:

  1. תיבה צמודה לאובייקט. חיתוך רחב נושא איתו רקע זר, וב-7 גם את הזוהר
     הוורוד והירוק בפינות, שנראה כמלבן בהיר סביב הדלי.
  2. יישור רקע. מודדים את צבע הרקע בטבעת החיצונית של החיתוך ומזיזים את
     כל התמונה כך שהרקע יהיה בדיוק צבע הקנבס. האובייקט זז באותה מידה,
     וזה בלתי מורגש כי ההזזה קטנה.
  3. ריכוך למעלה ולמטה בלבד. האמנות מוצבת מקצה לקצה, אז אין
     צדדים להסתיר. הגרסה הראשונה הציבה אותה בתוך השוליים, וזה יצר מלבן.

© כל הזכויות שמורות · דיוק דיגיטלי · גל הרוש 2026
"""
import io
import os

import numpy as np
from PIL import Image

# המודעות שמהן נחתכת האמנות, בתת התיקייה "מקור".
SRC = u"C:/Users/HP/Downloads/\u05d4\u05de\u05e9\u05e4\u05da \u05e9\u05dc\u05d9 \u05d3\u05d9\u05d5\u05e7 \u05d3\u05d9\u05d2\u05d9\u05d8\u05dc\u05d9/\u05e7\u05e8\u05d9\u05d0\u05d9\u05d9\u05d8\u05d9\u05d1 2/מקור"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

# רצועת האמנות בכל מודעה, בין הכותרת לשם המוצר
BANDS = {"7": (262, 940), "10": (312, 940), "12": (290, 950), "14": (320, 910)}
CANVAS = (0xF9, 0xF3, 0xF2)      # צבע הקנבס בתבנית
PAD = 26                          # שוליים סביב האובייקט
FEATHER = 56


def object_box(a, thr=7.0):
    """התיבה שבה התמונה שונה מהותית מהרקע שסביבה."""
    h, w, _ = a.shape
    ring = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3),
                           a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    base = np.median(ring, axis=0)
    d = np.abs(a - base).sum(axis=2)
    rows = np.where((d > thr).sum(axis=1) > w * 0.012)[0]
    cols = np.where((d > thr).sum(axis=0) > h * 0.012)[0]
    if not len(rows) or not len(cols):
        return 0, 0, w, h
    return int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1


def cut(n, top, bot):
    im = Image.open(os.path.join(SRC, u"\u05de\u05d5\u05d3\u05e2\u05ea \u05ea\u05de\u05d5\u05e0\u05d4 (%s).png" % n))
    band = np.asarray(im.convert("RGB").crop((0, top, 1254, bot))).astype(float)

    # האובייקטים נמשכים כמעט לכל הרוחב בכוונה, ולכן החיתוך נשאר
    # ברוחב מלא ומוצב מקצה לקצה. כך אין תפר בצדדים בכלל.
    crop = band

    # יישור הרקע לצבע הקנבס, לפי הטבעת החיצונית של החיתוך
    h, w, _ = crop.shape
    ring = np.concatenate([crop[:5].reshape(-1, 3), crop[-5:].reshape(-1, 3),
                           crop[:, :5].reshape(-1, 3), crop[:, -5:].reshape(-1, 3)])
    shift = np.array(CANVAS, dtype=float) - np.median(ring, axis=0)
    crop = np.clip(crop + shift, 0, 255).astype(np.uint8)

    # מפתח שקיפות: כל פיקסל שקרוב לצבע הקנבס נמחק. אפשר להיות אגרסיבי
    # כאן דווקא משום שמה שנמחק מוחלף בדיוק באותו צבע, אז גם אם שפת הדלי
    # יוצאת שקופה למחצה זה בלתי נראה. בלי זה נשאר מלבן בהיר סביב
    # האובייקט בכל קנה מידה שאינו רוחב מלא.
    d = np.abs(crop.astype(float) - np.array(CANVAS, dtype=float)).sum(axis=2)
    # הסף הועלה אחרי שהמסגרת נכנסה: עם קצה מוגדר לכרטיס, שאריות
    # הזוהר הצבעוני מהמודעה המקורית נראות כלכלוך ולא כרקע.
    key = np.clip((d - 15.0) / 30.0, 0, 1) * 255.0

    # ריכוך למעלה ולמטה, מעל המפתח
    ramp = (np.linspace(0, 1, FEATHER) ** 1.5 * 255)
    ay = np.full(h, 255.0); ay[:FEATHER] = ramp; ay[-FEATHER:] = ramp[::-1]
    alpha = np.minimum(key, ay[:, None])

    # מצמצמים לגבולות האובייקט עצמו. הרצועה נחתכה לפי מיקום הטקסט במקור
    # ולכן היא נושאת שוליים ריקים, והם מקטינים את האובייקט במודעה.
    solid = alpha > 40
    ys = np.where(solid.any(axis=1))[0]
    xs = np.where(solid.any(axis=0))[0]
    if len(ys) and len(xs):
        y0 = max(0, ys[0] - 4); y1 = min(h, ys[-1] + 5)
        x0 = max(0, xs[0] - 4); x1 = min(w, xs[-1] + 5)
        crop = crop[y0:y1, x0:x1]
        alpha = alpha[y0:y1, x0:x1]
        h, w = alpha.shape

    out = Image.fromarray(crop)
    out.putalpha(Image.fromarray(alpha.astype(np.uint8)))
    p = os.path.join(OUT, "art_%s.png" % n)
    out.save(p)
    print("  art_%-3s %4dx%-4d  shift %s  ->  %d KB"
          % (n, w, h, np.round(shift, 1), os.path.getsize(p) // 1024))


if __name__ == "__main__":
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for n, (t, b) in BANDS.items():
        cut(n, t, b)
