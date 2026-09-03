# -*- coding: utf-8 -*-
"""True mobile-width screenshots.

Chrome on this machine clamps the headless viewport to a 500px minimum, so
--window-size below 500 silently crops instead of reflowing. The fix is to
render the page inside a fixed-width iframe and shoot the iframe.
"""
import os, io, subprocess, sys

CH = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
SP = os.path.dirname(os.path.abspath(__file__))


def shot(src, out, width=390, height=844, budget=6000):
    wrap = os.path.join(SP, '_wrap.html')
    io.open(wrap, 'w', encoding='utf-8').write(
        u'<!doctype html><meta charset="utf-8">'
        u'<style>html,body{margin:0;background:#fff}'
        u'iframe{width:%dpx;height:%dpx;border:0;display:block}</style>'
        u'<iframe src="%s"></iframe>' % (width, height, os.path.basename(src)))
    subprocess.run([CH, '--headless', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
                    '--force-device-scale-factor=1',
                    '--window-size=%d,%d' % (max(width, 501), height),
                    '--virtual-time-budget=%d' % budget,
                    '--screenshot=' + os.path.abspath(out),
                    'file:///' + wrap.replace('\\', '/')], capture_output=True)
    try:
        from PIL import Image
        im = Image.open(out)
        if im.size[0] > width:
            im.crop((0, 0, width, min(height, im.size[1]))).save(out)
        print(out, Image.open(out).size)
    except Exception as e:
        print(out, 'saved,', e)


if __name__ == '__main__':
    a = sys.argv[1:]
    shot(a[0], a[1], int(a[2]) if len(a) > 2 else 390, int(a[3]) if len(a) > 3 else 844)
