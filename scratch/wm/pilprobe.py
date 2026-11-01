import pymupdf, numpy as np, glob, os
books=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
Z=2.0
for b in books:
    d=pymupdf.open("orig/%s.pdf"%b); n=len(d)
    ys=[]; xs0=[]; xs1=[]
    idx=list(range(0,n,max(1,n//25)))
    for i in idx:
        p=d[i]; W,H=p.rect.width,p.rect.height
        a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(0,0,W,140),colorspace=pymupdf.csRGB)
        arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.int16)
        r,g,bb=arr[...,0],arr[...,1],arr[...,2]
        blue=(bb>170)&(r<110)&(g>110)&(g<215)
        red=(r>175)&(g<75)&(bb<75)
        m=blue|red
        cnt=m.sum(1)
        rows=np.where(cnt> a.width*0.02)[0]
        if not len(rows):
            ys.append(None); continue
        y0,y1=rows.min()/Z,rows.max()/Z
        cols=np.where(m.any(0))[0]
        ys.append((round(y0,1),round(y1,1)))
        xs0.append(cols.min()/Z); xs1.append(cols.max()/Z)
    print("%-14s n=%3d  y-ranges=%s  x=[%.0f,%.0f]"%(b,n,sorted(set(ys),key=str),min(xs0) if xs0 else -1,max(xs1) if xs1 else -1))
