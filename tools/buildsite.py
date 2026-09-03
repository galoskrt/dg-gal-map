# -*- coding: utf-8 -*-
"""Inline fonts, brand CSS and images into each funnel page, then deploy to the repo."""
import base64, io, json, os, sys, subprocess

# הכלים יושבים ב-tools והמקור ב-src, שניהם בתוך המאגר ולכן שורדים כל שיחה
SP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
TOOLS = os.path.dirname(os.path.abspath(__file__))
SK = u"C:/Users/HP/.claude/skills/carousel-diyuk-digitali/assets"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"


def b64(p):
    return base64.b64encode(io.open(p, "rb").read()).decode("ascii")


FONT = u""
# גופן מכווץ לתווים שבשימוש בלבד, ב-WOFF2. שני קבצים של 5KB במקום 81KB,
# והם נשארים מוטמעים כי בגודל הזה בקשת רשת נוספת יקרה ממה שהיא חוסכת.
_FF = ("@font-face{font-family:'TelAviv';font-weight:%d;font-style:normal;"
       "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}")
for w, fn in ((400, "tlv-400.woff2"), (800, "tlv-800.woff2")):
    FONT += (_FF % (w, b64(os.path.join(SP, "fonts", fn)))) + chr(10)

BRAND = io.open(os.path.join(SP, "brand.css"), encoding="utf-8").read()


def webp(name):
    return "data:image/webp;base64," + b64(os.path.join(SP, "img", name))


LEAKS = io.open(os.path.join(SP, 'leaks.js'), encoding='utf-8').read()
CASESJS = io.open(os.path.join(SP, 'cases.js'), encoding='utf-8').read()

# סיפורי הלקוחות נקראים מהמקור האחד. דף הבית מקבל אותם כ-HTML סטטי בזמן
# הבנייה, ודף התוצאה מקבל את הקובץ עצמו ומרנדר בזמן ריצה. אותו מידע, פעם אחת.
CASES = json.loads(subprocess.run(
    ['node', '-e', CASESJS + ';process.stdout.write(JSON.stringify(CASES))'],
    capture_output=True).stdout.decode('utf-8'))


def case_html(c):
    """The card, generated once, identical to the one the result page builds."""
    parts = [
        '    <div class="case">',
        '<i class="tick t1"></i><i class="tick t2"></i>',
        '<i class="tick t3"></i><i class="tick t4"></i>',
        chr(10) + '      <div class="hd2"><div class="ph">',
        '<img src="%(photo)s" alt=""></div>',
        chr(10) + '        <div class="who2"><b>%(name)s</b>',
        '<span>%(field)s</span></div></div>',
        chr(10) + '      <p class="res">%(res)s</p>',
        chr(10) + '      <p>%(body)s</p>',
        chr(10) + '      <p class="pun">%(pun)s</p>',
        chr(10) + '    </div>' + chr(10),
    ]
    return ("".join(parts)) % c


def inline_cases(html):
    if '/*__CASES__*/' in html:
        html = html.replace('/*__CASES__*/', CASESJS)
    if '<!--CASES-->' in html:
        html = html.replace('<!--CASES-->', ''.join(case_html(c) for c in CASES))
    return html



# הפיקסל של דיוק דיגיטלי. הדפים כבר יורים אירועים, וזה מה שהופך אותם לאמיתיים.
# הקמפיין מיועל ל"התחיל אבחון", ולכן StartDiagnostic חייב להגיע לכאן.
PIXEL_ID = "3520763671432860"
PIXEL = """<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init','%s');fbq('track','PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=%s&ev=PageView&noscript=1" alt=""></noscript>
""" % (PIXEL_ID, PIXEL_ID)


def inline_pixel(html):
    return html.replace("</head>", PIXEL + "</head>", 1)

def inline_leaks(html):
    """One leak library, planted into every page that needs it."""
    return html.replace('/*__LEAKS__*/', LEAKS)

def build(src, dest_dir):
    h = io.open(os.path.join(SP, src), encoding="utf-8").read()
    h = inline_cases(inline_pixel(inline_leaks(h)))
    # פרצופי הלקוחות. שבעה מוצגים, מתוך שתים עשרה תמונות שגל סיפק.
    for i in range(1, 13):
        h = h.replace("/*CLIENT%02d*/" % i,
                      "data:image/webp;base64," + b64(os.path.join(SP, "img", "clients", "c%02d.webp" % i)))
    h = h.replace("/*FONT*/", FONT).replace("/*BRAND*/", BRAND).replace("/*LOGO*/", webp("logo.webp"))
    h = h.replace("/*AVATAR*/", webp("av1.webp"))
    h = h.replace("/*AVATAR2*/", webp("av2.webp"))
    h = h.replace("/*GAL*/", webp("gal.webp"))
    out_dir = os.path.join(REPO, dest_dir) if dest_dir else REPO
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out = os.path.join(out_dir, "index.html")
    io.open(out, "w", encoding="utf-8").write(h)
    print("  %-18s -> %-12s %6.0f KB" % (src, dest_dir or "/", len(h.encode("utf-8")) / 1024.0))
    return out


def shot(path, out, width=390, height=900, budget=6000):
    wrap = os.path.join(SP, "_w.html")
    io.open(wrap, "w", encoding="utf-8").write(
        u'<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}'
        u'iframe{width:%dpx;height:%dpx;border:0;display:block}</style>'
        u'<iframe src="file:///%s"></iframe>' % (width, height, path.replace("\\", "/")))
    subprocess.run([CH, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=%d,%d" % (max(width, 501), height),
                    "--virtual-time-budget=%d" % budget, "--screenshot=" + os.path.abspath(out),
                    "file:///" + wrap.replace("\\", "/")], capture_output=True)
    try:
        from PIL import Image
        im = Image.open(out)
        if im.size[0] > width:
            im.crop((0, 0, width, min(height, im.size[1]))).save(out)
        print("  shot", out, Image.open(out).size)
    except Exception as e:
        print("  shot", out, e)


if __name__ == "__main__":
    pages = [("survey.html", "q"), ("result.html", "map"),
             ("landing.html", ""), ("booking.html", "call"),
             ("privacy.html", "privacy")]
    want = sys.argv[1:] or [p[0] for p in pages]
    for src, dest in pages:
        if src in want and os.path.exists(os.path.join(SP, src)):
            build(src, dest)
