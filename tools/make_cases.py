# -*- coding: utf-8 -*-
"""One source of truth for the client stories.

The landing page and the result page told the same clients' stories in
different words, without their photographs, in a different card. Two versions
of one proof is how a reader learns to trust neither. Both pages render from
this file now, so they cannot drift again.
"""
import io
import json
import re

BACKSLASH = chr(92)
QUOTE = chr(39)


def card_at(s, i):
    depth = 0
    for m in re.finditer(r"<div\b|</div>", s[i:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return s[i:i + m.end()]
    raise ValueError("unbalanced card")


def extract(path):
    l = io.open(path, encoding="utf-8").read()
    pos = l.index('<div class="cases">')
    out = []
    while True:
        k = l.find('<div class="case">', pos)
        if k < 0:
            break
        c = card_at(l, k)
        pos = k + len(c)
        g = lambda p, s=c, f=re.S: (re.search(p, s, f).group(1).strip()
                                    if re.search(p, s, f) else "")
        out.append({
            "photo": "/*CLIENT%s*/" % g(r"/\*CLIENT(\d+)\*/"),
            "name": g(r"<b>(.*?)</b>"),
            "field": g(r"<span>(.*?)</span></div></div>"),
            "res": g(r'<p class="res">(.*?)</p>'),
            "body": g(r'</p>\s*<p>(.*?)</p>\s*<p class="pun">'),
            "pun": g(r'<p class="pun">(.*?)</p>'),
        })
    return out


def esc(s):
    return (s.replace(BACKSLASH, BACKSLASH * 2)
             .replace(QUOTE, BACKSLASH + QUOTE)
             .replace("\n", " "))


HEADER = (
    "/* סיפורי הלקוחות. "
    "מקור אחד, נשתל בדף "
    "הבית ובדף התוצאה "
    "בזמן הבנייה.\n"
    "   שתי גרסאות של אותה "
    "הוכחה מלמדות קורא "
    "לא להאמין לאף אחת. */\n")

RENDER = """
/* אותה כרטיסייה בדיוק בשני הדפים */
function caseCard(c){
  return '<div class="case">'
    + '<i class="tick t1"></i><i class="tick t2"></i>'
    + '<i class="tick t3"></i><i class="tick t4"></i>'
    + '<div class="hd2"><div class="ph"><img src="' + c.photo + '" alt=""></div>'
    + '<div class="who2"><b>' + c.name + '</b><span>' + c.field + '</span></div></div>'
    + '<p class="res">' + c.res + '</p>'
    + '<p>' + c.body + '</p>'
    + '<p class="pun">' + c.pun + '</p></div>';
}
"""

if __name__ == "__main__":
    cards = extract("landing.html")
    lines = []
    for c in cards:
        lines.append(
            "  { photo:'%s', name:'%s', field:'%s',\n"
            "    res:'%s',\n"
            "    body:'%s',\n"
            "    pun:'%s' }"
            % (c["photo"], esc(c["name"]), esc(c["field"]),
               esc(c["res"]), esc(c["body"]), esc(c["pun"])))
    body = HEADER + "var CASES = [\n" + ",\n".join(lines) + "\n];\n" + RENDER
    io.open("cases.js", "w", encoding="utf-8").write(body)
    print("cases.js written with %d stories, %d bytes" % (len(cards), len(body.encode())))
    for c in cards:
        clean = re.sub(r"<[^>]+>", "", c["res"])
        print("  %-20s %s" % (c["name"], clean[:58]))
