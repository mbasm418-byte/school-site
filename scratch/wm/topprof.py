import pymupdf, numpy as np
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
for nm in NAMES:
    d=pymupdf.open("orig/%s.pdf"%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    Z=2.0
    clip=pymupdf.Rect(0,0,W,H*0.10)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csGRAY)
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width).astype(np.int16)
    ink=(a<200).sum(1)
    rows=[]
    for y in range(0,pix.height,int(1*Z)):
        rows.append((y/Z, int(ink[y])))
    # print compact: y : ink
    print(nm, "W=%.0f"%W)
    print("   "+" ".join("%.0f:%d"%(y,i) for y,i in rows if i>0))
