import pymupdf, numpy as np, sys
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"

def best(page):
    W,H=page.rect.width,page.rect.height
    clip=pymupdf.Rect(W*0.60,H*0.68,W,H)
    pix=page.get_pixmap(clip=clip,matrix=pymupdf.Matrix(1,1),colorspace=pymupdf.csRGB)
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
    mx=a.max(2); mn=a.min(2); mean=a.mean(2)
    mask=((mx-mn)<=26)&(mean>=150)&(mean<=228)
    M=mask.astype(np.float32)
    SAT=np.pad(M.cumsum(0).cumsum(1),((1,0),(1,0)))
    h,w=M.shape
    def disc_sum(cy,cx,R):
        y0=np.clip(cy-R,0,h); y1=np.clip(cy+R,0,h); x0=np.clip(cx-R,0,w); x1=np.clip(cx+R,0,w)
        return SAT[y1,x1]-SAT[y0,x1]-SAT[y1,x0]+SAT[y0,x0], (y1-y0)*(x1-x0)
    bestv=(-1,0,0,0)
    Rs=np.arange(int(0.05*W),int(0.15*W)+1,2)
    for R in Rs:
        ys=np.arange(R, h-R, 3); xs=np.arange(R, w-R, 3)
        for cy in ys:
            for cx in xs:
                s,area=disc_sum(cy,cx,R)
                v=s/area
                if v>bestv[0]: bestv=(v,cx,cy,R)
    v,cx,cy,R=bestv
    return v, clip.x0+cx, clip.y0+cy, R

for nm in NAMES:
    d=pymupdf.open(BASE%nm); n=d.page_count
    idx=[i for i in range(n) if i%max(1,n//8)==0][:8]
    res=[]
    for i in idx:
        res.append((i,)+best(d[i]))
    res.sort(key=lambda t:-t[1])
    print(nm, "pages", n)
    for r in res[:4]:
        print("   p%-4d fill=%.3f cx=%.1f cy=%.1f R=%.1f"%(r[0]+1,r[1],r[2],r[3],r[4]))
    sys.stdout.flush()
