import pymupdf, numpy as np, sys, collections
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"

def analyse(page):
    W,H=page.rect.width,page.rect.height
    clip=pymupdf.Rect(W*0.58,H*0.66,W,H)
    pix=page.get_pixmap(clip=clip,matrix=pymupdf.Matrix(1,1),colorspace=pymupdf.csRGB)
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    mask=(np.abs(r-g)<=4)&((b-r)>=4)&((b-r)<=14)&(r>=145)&(r<=232)
    M=mask.astype(np.float32)
    SAT=np.pad(M.cumsum(0).cumsum(1),((1,0),(1,0)))
    h,w=M.shape
    best=(-1e9,0,0,0)
    for R in range(int(0.05*W),int(0.145*W)+1,2):
        ys=np.arange(R,h-R,2); xs=np.arange(R,w-R,2)
        if len(ys)==0 or len(xs)==0: continue
        Y,X=np.meshgrid(ys,xs,indexing='ij')
        s=SAT[Y+R,X+R]-SAT[Y-R,X+R]-SAT[Y+R,X-R]+SAT[Y-R,X-R]
        area=np.pi*R*R
        score=2*s-area
        k=int(np.argmax(score))
        if score.flat[k]>best[0]:
            best=(score.flat[k], X.flat[k], Y.flat[k], R)
    sc,cx,cy,R=best
    return sc, clip.x0+cx, clip.y0+cy, R

for nm in NAMES:
    d=pymupdf.open(BASE%nm); n=d.page_count
    idx=sorted(set([int(i*n/40) for i in range(1,40)]+[5]))
    votes=[]; out=[]
    for i in idx:
        sc,cx,cy,R=analyse(d[i])
        votes.append((round(cx),round(cy),R)); out.append((sc,i,cx,cy,R))
    c=collections.Counter([(v[0],v[1]) for v in votes])
    top=c.most_common(3)
    rs=[v[2] for v in votes if (v[0],v[1])==top[0][0]]
    out.sort(reverse=True)
    print("%-14s W=%.0f H=%.0f | top centres %s | R mode %s | bestscore %.0f cx=%.0f cy=%.0f R=%d p%d"%(
        nm,d[0].rect.width,d[0].rect.height,[(k,v) for k,v in top],
        collections.Counter(rs).most_common(3),out[0][0],out[0][2],out[0][3],out[0][4],out[0][1]+1))
    sys.stdout.flush()
