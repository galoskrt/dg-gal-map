# -*- coding: utf-8 -*-
"""Render a creative at exact pixel size.

The artwork comes from Gal's image model; every letter comes from here, with
his real font. The model spelled his name "גל הרושל" and used a font that is
not his, which is the whole reason typography is rebuilt rather than reused.

Formats follow document 09: 1080x1350 for the feed and 1080x1920 for stories
and reels, plus 1080x1080 for square posts. The story format keeps 14 percent
clear at the top and 20 percent at the bottom, where Meta's own interface sits
and eats text.
"""
import base64
import io
import os
import subprocess
import sys

SP = os.path.dirname(os.path.abspath(__file__))
SK = u"C:/Users/HP/.claude/skills/carousel-diyuk-digitali/assets"
CH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

FORMATS = {
    # name: (width, height, scale of the type, top pad, bottom pad, side pad)
    "feed":   (1080, 1350, 1.00, 0.062, 0.058, 0.115),
    "story":  (1080, 1920, 0.98, 0.150, 0.205, 0.115),
    "square": (1080, 1080, 0.92, 0.062, 0.058, 0.110),
}


def b64(path):
    return base64.b64encode(io.open(path, "rb").read()).decode("ascii")


def data(path, mime):
    return "data:%s;base64,%s" % (mime, b64(path))


FONT = u""
for weight, fn in ((400, "TelAviv-Regular.ttf"), (800, "TelAviv-Bold.ttf")):
    FONT += (u"@font-face{font-family:'TelAviv';font-weight:%d;font-style:normal;"
             u"src:url(data:font/ttf;base64,%s) format('truetype');}\n"
             % (weight, b64(os.path.join(SK, "fonts", fn))))


def vars_for(w, h, s, padT, padB, padX):
    """One unit scales everything, so a format change never needs new numbers."""
    u = w / 26.0
    return {
        "W": "%dpx" % w, "H": "%dpx" % h, "u": "%.2fpx" % u,
        "blur": "%.1fpx" % (w * 0.055),
        "padT": "%.1fpx" % (h * padT), "padB": "%.1fpx" % (h * padB),
        "padX": "%.1fpx" % (w * padX),
        "colW": "%.0fpx" % (w * (1 - 2 * padX)),
        "artW": "%.0fpx" % (w * 0.86),
        "logoH": "%.1fpx" % (u * 1.34 * s), "logoT": "%.1fpx" % (u * 0.80 * s),
        "logoGap": "%.1fpx" % (u * 0.42),
        "gapA": "%.1fpx" % (h * 0.040), "gapB": "%.1fpx" % (h * 0.028),
        "gapC": "%.1fpx" % (h * 0.026), "gapD": "%.1fpx" % (h * 0.026),
        "gapE": "%.1fpx" % (h * 0.022),
        "h1": "%.1fpx" % (u * 1.28 * s),
        "specGap": "%.1fpx" % (u * 0.62), "specSep": "%.1fpx" % (u * 1.05),
        "specP": "%.1fpx %.1fpx" % (u * 0.52, u * 1.0), "specF": "%.1fpx" % (u * 0.72 * s),
        "ctaF": "%.1fpx" % (u * 0.96 * s),
        "ctaP": "%.1fpx %.1fpx" % (u * 0.66, u * 1.5),
        "ctaR": "%.1fpx %.1fpx %.1fpx %.1fpx" % (u * .78, u * .78, u * .78, u * .2),
        "faceD": "%.1fpx" % (u * 1.5), "faceB": "%.1fpx" % (u * 0.09),
        "meGap": "%.1fpx" % (u * 0.42), "nameF": "%.1fpx" % (u * 0.7 * s),
    }


def build(src, art, out_name, fmt):
    w, h, s, padT, padB, padX = FORMATS[fmt]
    html = io.open(os.path.join(SP, src), encoding="utf-8").read()
    html = html.replace("/*FONT*/", FONT)
    html = html.replace("/*LOGO*/", data(os.path.join(SP, "img", "logo.webp"), "image/webp"))
    html = html.replace("/*ART*/", data(os.path.join(SP, "img", art), "image/png"))
    html = html.replace("/*GAL*/", data(os.path.join(SP, "img", "gal.webp"), "image/webp"))
    css = ";".join("--%s:%s" % (k, v) for k, v in vars_for(w, h, s, padT, padB, padX).items())
    html = html.replace("<div class=\"ad\">", "<div class=\"ad\" style=\"%s\">" % css)

    tmp = os.path.join(SP, "_c_%s.html" % fmt)
    io.open(tmp, "w", encoding="utf-8").write(html)
    out = os.path.join(SP, "out", "%s_%s.png" % (out_name, fmt))
    if not os.path.isdir(os.path.join(SP, "out")):
        os.makedirs(os.path.join(SP, "out"))
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--default-background-color=FFFFFFFF",
                    "--force-device-scale-factor=1",
                    "--window-size=%d,%d" % (w, h),
                    "--virtual-time-budget=6000",
                    "--screenshot=" + out, "file:///" + tmp.replace("\\", "/")],
                   capture_output=True)
    from PIL import Image
    got = Image.open(out).size
    print("  %-22s %-7s %s %s" % (out_name, fmt, got, "OK" if got == (w, h) else "SIZE MISMATCH"))
    return out


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "creative.html"
    art = sys.argv[2] if len(sys.argv) > 2 else "art_map.png"
    name = sys.argv[3] if len(sys.argv) > 3 else "ad_a"
    fmts = sys.argv[4:] or ["feed"]
    for f in fmts:
        build(src, art, name, f)
