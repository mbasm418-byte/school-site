import pymupdf, numpy as np, os
from strip5 import band
import badge as B

WM = "/home/superlisa/workspace/projects/school-site/scratch/wm/"
BAND = WM + "band.png"

# page-points geometry of the SadsHelp watermark disc: (cx, cy, R)
DISC = {
    "arabic": (833.6, 1156.6, 86.2),
    "islamiya": (526.8, 725.5, 54.0),
    "english": (850.6, 1250.4, 87.5),
    "math_p1": (851.6, 1216.0, 86.5),
    "kimya": (535.4, 782.0, 55.0),
    "physics": (850.6, 1212.9, 87.2),
    "biology_sajjad": (851.6, 1239.4, 88.0),
    "social": (856.1, 1249.9, 88.5),
}
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
AR_BOOKS = {"arabic", "islamiya", "social"}
EXTRA_CUT = {"physics": 18.0}
CUR = [""]


def strip_cut(p):
    """Y position (page pts) where the top branding strip ends; 0 if absent."""
    bx = band(p)
    return 0.0 if bx is None else bx[3] + 0.6 + EXTRA_CUT.get(CUR[0], 0.0)


def build_page(out, src, i, name, draw_strip=True, draw_badge=True):
    sp = src[i]
    CUR[0] = name
    W, H = sp.rect.width, sp.rect.height
    cut = strip_cut(sp) if draw_strip else 0.0
    BH = max(24, round(W * 0.03))
    np_ = out.new_page(width=W, height=H - cut + BH)
    np_.show_pdf_page(pymupdf.Rect(0, BH, W, BH + H - cut), src, i,
                      clip=pymupdf.Rect(0, cut, W, H))
    np_.insert_image(pymupdf.Rect(0, 0, W, BH), filename=BAND, keep_proportion=False)
    if draw_badge and name in DISC and i >= 2:
        cx, cy, R = DISC[name]
        cy -= cut
        Rb = R + 22
        num = str(i + 1)
        if name in AR_BOOKS:
            num = num.translate(AR_DIGITS)
        png = WM + "bg_%s_%d.png" % (name, i)
        B.make(png, Rb, num)
        np_.insert_image(pymupdf.Rect(cx - Rb, cy - Rb, cx + Rb, cy + Rb), filename=png)
    return np_


def build(name, pages=None, outdir=WM, chunk=20):
    """Build in chunks to keep memory bounded (badge pixmaps are big)."""
    src = pymupdf.open(WM + "orig/%s.pdf" % name)
    idx = list(range(len(src))) if pages is None else list(pages)
    parts = []
    for k in range(0, len(idx), chunk):
        out = pymupdf.open()
        for i in idx[k:k + chunk]:
            build_page(out, src, i, name)
        part = WM + "part_%s_%03d.pdf" % (name, k)
        out.save(part, garbage=3, deflate=True, clean=True)
        out.close()
        parts.append(part)
        print("  %s %d/%d" % (name, min(k + chunk, len(idx)), len(idx)), flush=True)
    dst = outdir + "new_%s.pdf" % name
    if len(parts) == 1:
        os.replace(parts[0], dst)
    else:
        merged = pymupdf.open()
        for part in parts:
            merged.insert_pdf(pymupdf.open(part))
        merged.save(dst, garbage=3, deflate=True, clean=True)
        merged.close()
        for part in parts:
            os.remove(part)
    for f in os.listdir(WM):
        if f.startswith("bg_" + name + "_"):
            os.remove(WM + f)
    print(name, len(idx), "->", dst, os.path.getsize(dst) / 1e6, "MB", flush=True)
    return dst


if __name__ == "__main__":
    import sys
    for n in sys.argv[1:]:
        build(n, pages=[6])
