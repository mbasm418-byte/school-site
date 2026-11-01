import pymupdf, numpy as np
from collections import defaultdict
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"

def comps(mask):
    H,W=mask.shape
    parent={}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def uni(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
    ys,xs=np.nonzero(mask)
    for y,x in zip(ys.tolist(),xs.tolist()):
        parent[(y,x)]=(y,x)
    for y,x in zip(ys.tolist(),xs.tolist()):
        for dy,dx in ((0,1),(1,0),(1,1),(1,-1)):
            k=(y+dy,x+dx)
            if k in parent: uni((y,x),k)
    groups=defaultdict(list)
    for p in parent: groups[find(p)].append(p)
    return groups

def kasa(pts):
    x=pts[:,0]; y=pts[:,1]
    A=np.c_[2*x,2*y,np.ones(len(x))]
    b=x*x+y*y
    c,*_=np.linalg.lstsq(A,b,rcond=None)
    cx,cy=c[0],c[1]
    R=np.sqrt(c[2]+cx*cx+cy*cy)
    return cx,cy,R

for nm in NAMES:
    d=pymupdf.open(BASE%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    Z=1.0
    clip=pymupdf.Rect(W*0.55,H*0.68,W,H)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csRGB)
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3).astype(np.int16)
    r,g,b=a[...,0],a[...,1],a[...,2]
    mask=(np.abs(r-g)<=4)&((b-r)>=4)&((b-r)<=14)&(r>=150)&(r<=225)
    groups=comps(mask)
    big=sorted(groups.items(), key=lambda kv:-len(kv[1]))[:3]
    print("==",nm,"regions",len(groups))
    for k,pts in big:
        P=np.array(pts,float)
        # boundary only: keep points with a neighbour outside
        cy,cx=k
        print("   size",len(pts),"bbox px x[%d,%d] y[%d,%d]"%(P[:,1].min(),P[:,1].max(),P[:,0].min(),P[:,0].max()))
