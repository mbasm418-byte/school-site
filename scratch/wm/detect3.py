import pymupdf, numpy as np
from collections import defaultdict
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"

def comps(mask):
    parent={}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def uni(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    ys,xs=np.nonzero(mask)
    pts=list(zip(ys.tolist(),xs.tolist()))
    for p in pts: parent[p]=p
    for y,x in pts:
        for dy,dx in ((0,1),(1,0),(1,1),(1,-1)):
            k=(y+dy,x+dx)
            if k in parent: uni((y,x),k)
    groups=defaultdict(list)
    for p in parent: groups[find(p)].append(p)
    return groups

for nm in NAMES:
    d=pymupdf.open(BASE%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    clip=pymupdf.Rect(W*0.55,H*0.68,W,H)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(1,1),colorspace=pymupdf.csRGB)
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    mask=(np.abs(r-g)<=5)&((b-r)>=3)&((b-r)<=16)&(r>=140)&(r<=228)
    groups=comps(mask)
    if not groups: print(nm,"none"); continue
    pts=max(groups.values(), key=len)
    P=np.array(pts)
    rows=defaultdict(list)
    for y,x in pts: rows[y].append(x)
    wrow=max(rows.items(), key=lambda kv:(max(kv[1])-min(kv[1]), len(kv[1])))
    yb,xb=wrow[0],wrow[1]
    print("%-14s W=%6.1f H=%7.1f | blob=%5d | widest row y=%d w=%d x[%d,%d] | bbox x[%d,%d] y[%d,%d]"%(
        nm,W,H,len(pts),yb,max(xb)-min(xb),min(xb),max(xb),P[:,1].min(),P[:,1].max(),P[:,0].min(),P[:,0].max()))
    print("      -> page: cy=%.1f  cx=%.1f  widest=%.1f  fromright=%.1f frombottom=%.1f"%(
        clip.y0+yb, clip.x0+(min(xb)+max(xb))/2, (max(xb)-min(xb))/2, W-(clip.x0+(min(xb)+max(xb))/2), H-(clip.y0+yb)))
