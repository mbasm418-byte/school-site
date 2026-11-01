import pymupdf, numpy as np
from collections import Counter
p = "/home/superlisa/workspace/projects/school-site/scratch/wm/orig/arabic.pdf"
d = pymupdf.open(p); pg = d[5]
W,H = pg.rect.width, pg.rect.height
clip = pymupdf.Rect(W*0.6, H*0.72, W, H)
pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(2,2), colorspace=pymupdf.csRGB)
im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
q = (im//8*8).reshape(-1,3)
c = Counter(map(tuple, q))
for col,n in c.most_common(18):
    print(col, n)
print("W,H",W,H,"clipsize",pix.width,pix.height)
