import pymupdf, numpy as np
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"
print_header="%-14s %6s %6s %6s %6s %6s"
print(print_header%("book","cx","cy","R","from_r","score"))
for nm in NAMES:
    d=pymupdf.open(BASE%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    Z=1.0
    clip=pymupdf.Rect(W*0.60,H*0.68,W,H)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csGRAY)
    g=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width).astype(np.float32)
    gy,gx=np.gradient(g)
    mag=np.hypot(gx,gy)
    th=np.percentile(mag,96)
    ys,xs=np.nonzero(mag>th)
    ux=gx[ys,xs]/(mag[ys,xs]+1e-6); uy=gy[ys,xs]/(mag[ys,xs]+1e-6)
    # vote centres
    acc=np.zeros((pix.height//2+1, pix.width//2+1),np.float32)
    Rmin=int(0.03*W); Rmax=int(0.16*W)
    for R in range(Rmin,Rmax,2):
        cxp=(xs-R*ux).astype(int); cyp=(ys-R*uy).astype(int)
        ok=(cxp>=0)&(cxp<pix.width)&(cyp>=0)&(cyp<pix.height)
        np.add.at(acc,(cyp[ok]//2,cxp[ok]//2),1)
    iy,ix=np.unravel_index(np.argmax(acc),acc.shape)
    cx0,cy0=ix*2,iy*2
    # refine radius: distance histogram of edge px near that centre
    dist=np.hypot(xs-cx0,ys-cy0)
    hist,edges=np.histogram(dist,bins=np.arange(0,max(pix.width,pix.height),2))
    Rr=edges[np.argmax(hist)]+1
    px,py=clip.x0+cx0, clip.y0+cy0
    print("%-14s %6.1f %6.1f %6.1f %6.1f %6.0f"%(nm,px,py,Rr,W-px,acc.max()))
