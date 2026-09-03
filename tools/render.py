# -*- coding: utf-8 -*-
"""Inject font+style, render via ASCII path, audit, rasterize."""
import io, os, re, sys, subprocess, fitz

SP = os.path.dirname(os.path.abspath(__file__))
D  = u"C:/Users/HP/Downloads/\u05d4\u05de\u05e9\u05e4\u05da \u05e9\u05dc\u05d9 \u05d3\u05d9\u05d5\u05e7 \u05d3\u05d9\u05d2\u05d9\u05d8\u05dc\u05d9"
CH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"

font  = io.open(os.path.join(SP, "heebo-embed.css"), encoding="utf-8").read()
style = io.open(os.path.join(SP, "docstyle.css"),   encoding="utf-8").read()

DASH  = re.compile(u"[\u2013\u2014\u05be\u2212]")
EMOJI = re.compile(u"[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def build(base, idx):
    src = os.path.join(D, base + ".html")
    html = io.open(src, encoding="utf-8").read()
    html = html.replace("/*FONT*/", font).replace("/*STYLE*/", style)
    tmp_html = os.path.join(SP, "b%d.html" % idx)
    tmp_pdf  = os.path.join(SP, "b%d.pdf" % idx)
    io.open(tmp_html, "w", encoding="utf-8").write(html)
    subprocess.run([CH, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    "--print-to-pdf=" + tmp_pdf, "file:///" + tmp_html],
                   capture_output=True)
    raw = io.open(tmp_pdf, "rb").read()
    doc = fitz.open(tmp_pdf)
    txt = "".join(p.get_text() for p in doc)
    dashes = DASH.findall(txt)
    emojis = EMOJI.findall(txt)
    hy = [txt[max(0, m.start() - 22):m.start() + 12].replace("\n", " ")
          for m in re.finditer("-", txt)]
    print("=" * 60)
    print("DOC %d: %s" % (idx, base))
    print("  pages=%d  bytes=%d  Heebo=%s" % (doc.page_count, len(raw), b"Heebo" in raw))
    print("  ai-dashes=%d  emojis=%d  hyphens=%d" % (len(dashes), len(emojis), len(hy)))
    seen = set()
    for h in hy:
        if h not in seen:
            seen.add(h)
            print("     hyphen:", h)
    for i, p in enumerate(doc):
        p.get_pixmap(dpi=100).save(os.path.join(SP, "d%d_p%d.png" % (idx, i + 1)))
    n = doc.page_count
    doc.close()
    io.open(os.path.join(D, base + ".pdf"), "wb").write(raw)
    return n


if __name__ == "__main__":
    for i, b in enumerate(sys.argv[1:], 1):
        build(b, i)
