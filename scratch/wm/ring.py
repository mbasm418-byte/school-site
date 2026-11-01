import pymupdf, numpy as np
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"
def comps(mask):
    parent={}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    ys,xs=np.nonzero(mask); pts=list(zip(ys.tolist(),xs.tolist()))
    for p in pts: parent[p]=p
    for y,x in pts:
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dy==0 and dx==0: continue
                k=(y+dy,x+dx)
                if k in parent:
                    ra,rb=find((y,x)),find(k)
                    if ra!=rb: parent[rb]=ra
    from collections import defaultdict
    g=defaultdict(list)
    for p in parent: g[find(p)].append(p)
    return max(g.values(), key=len) if g else []
for nm in NAMES:
    d=pymupdf.open(BASE%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    clip=pymupdf.Rect(W*0.55,H*0.65,W,H)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(1,1),colorspace=pymupdf.csRGB)
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=(g>r+4)&(g>=b-2)&(g>150)&(g<250)
    pts=comps(m)
    if not pts: print(nm,"none"); continue
    P=np.array(pts); y0,x0=P[:,0].min(),P[:,1].min(); y1,x1=P[:,0].max(),P[:,1].max()
    print("%-14s n=%5d bbox page x[%.0f,%.0f] y[%.0f,%.0f] -> w=%.0f h=%.0f cx=%.0f cy=%.0f"%(
        nm,len(pts),clip.x0+x0,clip.x0+x1,clip.y0+y0,clip.y0+y1,x1-x0,y1-y0,
        clip.x0+(x0+x1)/2,clip.y0+(y0+y1)/2))
