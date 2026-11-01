import pymupdf, numpy as np
from PIL import Image, ImageDraw
import sys
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"

def lbl(mask):
    import scipy.ndimage as ndi
    lab,n = ndi.label(mask)
    if n==0: return None,0
    sizes = ndi.sum(mask, lab, range(1,n+1))
    k = int(np.argmax(sizes))+1
    return lab==k, sizes[k-1]

try:
    import scipy; HAVE=True
except Exception:
    HAVE=False
print("scipy",HAVE)

for nm in NAMES:
    d=pymupdf.open(BASE%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    Z=2.0
    clip=pymupdf.Rect(0,H*0.70,W,H)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csRGB)
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    mask=(np.abs(r-g)<=4)&((b-r)>=4)&((b-r)<=14)&(r>=150)&(r<=225)
    if HAVE:
        blob,sz=lbl(mask)
    else:
        blob,sz=None,0
    print(nm,"W,H",W,H,"maskpx",int(mask.sum()),"blob",int(sz) if blob is not None else None)
