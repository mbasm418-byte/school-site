import pymupdf, numpy as np
Z=2.0
def detect(p, zw=None):
    W=p.rect.width
    a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(0,0,W,min(140,p.rect.height)),colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.int16)
    r,g,b=arr[...,0],arr[...,1],arr[...,2]
    blue=(b>170)&(r<110)&(g>110)&(g<215)
    red=(r>175)&(g<75)&(b<75)
    bw,rw=W*Z,W*Z
    ok=(blue.sum(1)>bw*0.15)&(red.sum(1)>rw*0.06)
    rows=np.where(ok)[0]
    if not len(rows): return None
    # contiguous run with gaps<=2
    runs=[]; s=rows[0]; pr=rows[0]
    for y in rows[1:]:
        if y-pr<=2: pr=y; continue
        runs.append((s,pr)); s=y; pr=y
    runs.append((s,pr))
    best=max(runs,key=lambda t:t[1]-t[0])
    y0=max(0,best[0]/Z-1); y1=min(p.rect.height,best[1]/Z+1)
    sub=arr[int(y0*Z):int(y1*Z)+1]
    mx=sub.max(2); mn=sub.min(2)
    grey=(mx-mn<=14)&(sub[...,0]>=55)&(sub[...,0]<=135)
    m=(blue[int(y0*Z):int(y1*Z)+1]|red[int(y0*Z):int(y1*Z)+1]|grey)
    cols=np.where(m.any(0))[0]
    x0=max(0,cols.min()/Z-2); x1=min(p.rect.width,(cols.max()+1)/Z+2)
    return (round(x0,1),round(y0,1),round(x1,1),round(y1,1))
