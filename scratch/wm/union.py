import pymupdf, numpy as np
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
for nm in NAMES:
    d=pymupdf.open("orig/%s.pdf"%nm); n=d.page_count
    W,H=d[0].rect.width,d[0].rect.height
    clip=pymupdf.Rect(W*0.55,H*0.62,W,H)
    acc=None; cnt=0
    for i in range(0,n,max(1,n//40)):
        pg=d[i]
        if abs(pg.rect.width-W)>1 or abs(pg.rect.height-H)>1: continue
        pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(1,1),colorspace=pymupdf.csRGB)
        a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
        r,g,b=a[...,0],a[...,1],a[...,2]
        m=(np.abs(r-g)<=5)&((b-r)>=3)&((b-r)<=16)&(r>=140)&(r<=232)
        acc = m.astype(np.uint16) if acc is None else acc+m
        cnt+=1
    frac=acc/cnt
    strong=frac>0.5
    ys,xs=np.nonzero(strong)
    if len(ys)==0:
        print(nm,"no strong pixels"); continue
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    print("%-14s n=%d strong=%5d  page bbox x[%6.1f,%6.1f] y[%6.1f,%6.1f]  w=%.0f h=%.0f cx=%.1f cy=%.1f"%(
        nm,cnt,len(ys),clip.x0+x0,clip.x0+x1,clip.y0+y0,clip.y0+y1,x1-x0,y1-y0,
        clip.x0+(x0+x1)/2,clip.y0+(y0+y1)/2))
