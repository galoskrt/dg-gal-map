# -*- coding: utf-8 -*-
"""Read a rendered creative the way an eye would, but in numbers.

Measuring the DOM in a separate headless pass lied once, because the embedded
font had not applied there and the text was narrower than it really renders.
The rendered PNG cannot lie: it is the artefact that ships. This finds where
the ink actually sits, whether anything crosses the safe margin, and whether
each band is centred.
"""
import sys

import numpy as np
from PIL import Image


def bands(mask, min_gap):
    """Contiguous runs of True, merged across gaps smaller than min_gap."""
    idx = np.where(mask)[0]
    if not len(idx):
        return []
    out, start, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev > min_gap:
            out.append((start, prev))
            start = i
        prev = i
    out.append((start, prev))
    return out


def inspect(path, margin_pct=0.05):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    a = np.asarray(im).astype(int)

    # Ink is anything meaningfully darker or more saturated than the paper.
    lum = a.sum(axis=2) / 3.0
    sat = a.max(axis=2) - a.min(axis=2)
    ink = (lum < 232) | (sat > 42)

    safe = int(round(w * margin_pct))
    print("%s  %dx%d   safe margin %dpx" % (path.split("/")[-1], w, h, safe))

    rows = ink.sum(axis=1) > (w * 0.002)
    print("\n  band            top  bottom   left right   width  centre offset")
    worst = 0
    for top, bot in bands(rows, int(h * 0.012)):
        if bot - top < h * 0.004:
            continue
        block = ink[top:bot + 1]
        cols = np.where(block.sum(axis=0) > 0)[0]
        if not len(cols):
            continue
        l, r = int(cols[0]), int(cols[-1])
        centre_off = ((l + r) / 2.0) - (w / 2.0)
        flag = ""
        if l < safe or r > w - safe:
            flag = "  <-- CROSSES THE MARGIN"
            worst = max(worst, max(safe - l, r - (w - safe)))
        print("  %-14s %5d %6d  %5d %5d  %5d  %+6.0f%s"
              % ("", top, bot, l, r, r - l + 1, centre_off, flag))

    all_cols = np.where(ink.sum(axis=0) > 0)[0]
    print("\n  overall ink  x[%d, %d]   page width %d" % (all_cols[0], all_cols[-1], w))
    if worst:
        print("  WORST OVERFLOW: %dpx past the safe margin" % worst)
    else:
        print("  nothing crosses the safe margin")
    return worst


if __name__ == "__main__":
    for p in sys.argv[1:]:
        inspect(p)
        print()
