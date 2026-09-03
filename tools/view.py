# -*- coding: utf-8 -*-
"""Make any image readable, every time.

A conversation that has accumulated many images enforces a much smaller cap on
each one, and reading a file at full size then fails with nothing useful to
say. The fix is never to read the original: always write a small copy first
and read that. Text stays legible far below the cap, so nothing is lost.

  python view.py "C:/path/to/image.png"        one image
  python view.py --latest 3                    the newest files Gal added
  python view.py --tight "C:/path/img.png"     when even the normal size fails

It prints the path to read. Feed that path to the Read tool, never the source.
"""
import os
import shutil
import sys
import time

from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "view")
NORMAL = 900          # comfortably readable, comfortably under the cap
TIGHT = 620           # when a conversation is already heavy with images
EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")


def preview(src, cap=NORMAL, tag=None):
    os.makedirs(OUT, exist_ok=True)
    im = Image.open(src)
    w, h = im.size
    im = im.convert("RGB")
    if max(w, h) > cap:
        im.thumbnail((cap, cap), Image.LANCZOS)
    name = (tag or os.path.splitext(os.path.basename(src))[0])
    name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:40]
    dst = os.path.join(OUT, "%s.png" % name)
    im.save(dst, "PNG", optimize=True)
    print("  %-42s %sx%s -> %sx%s  %d KB"
          % (os.path.basename(src), w, h, im.size[0], im.size[1],
             os.path.getsize(dst) // 1024))
    print("  READ: %s" % dst.replace("\\", "/"))
    return dst


def latest(n=3, root=r"C:\Users\HP\Downloads", within_hours=48):
    cut = time.time() - within_hours * 3600
    hits = []
    for dp, dirs, files in os.walk(root):
        if dp.count(os.sep) - root.count(os.sep) > 2:
            continue
        for f in files:
            if not f.lower().endswith(EXT):
                continue
            p = os.path.join(dp, f)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if m > cut:
                hits.append((m, p))
    hits.sort(reverse=True)
    return [p for _, p in hits[:n]]


if __name__ == "__main__":
    args = sys.argv[1:]
    cap = NORMAL
    if "--tight" in args:
        cap = TIGHT
        args.remove("--tight")
    if args and args[0] == "--latest":
        n = int(args[1]) if len(args) > 1 else 3
        for i, p in enumerate(latest(n), 1):
            preview(p, cap, tag="latest%d" % i)
    else:
        for p in args:
            preview(p, cap)
