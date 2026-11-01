import pymupdf, numpy as np
from PIL import Image
Z=3.0
PILCOL=((85,85,88),(12,144,230),(230,25,32)); TOL=26
def pmask(arr):
    m=np.zeros(arr.shape[:2],bool)
    for c in PILCOL:
        m|=(np.abs(arr[...,0]-c[0])<=TOL)&(np.abs(arr[...,1]-c[1])<=TOL)&(np.abs(arr[...,2]-c[2])<=TOL)
    return m

def band(p):
    W=p.rect.width
    a=p.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(0,0,W,min(130,p.rect.height)),colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.int16)
    m=pmask(arr); cnt=m.sum(1); thr=a.width*0.02
    rows=np.where(cnt>thr)[0]
    if len(rows)<4: return None
    runs=[]; s=rows[0]; pr=rows[0]
    for y in rows[1:]:
        if y-pr<=3: pr=y; continue
        runs.append((s,pr)); s=y; pr=y
    runs.append((s,pr))
    runs=[r for r in runs if r[1]-r[0]>=int(6*2)]
    if not runs: return None
    best=max(runs,key=lambda t:cnt[t[0]:t[1]+1].sum())
    y0=best[0]/2.0; y1=(best[1]+1)/2.0
    sub=m[best[0]:best[1]+1]
    cols=np.where(sub.any(0))[0]
    return (cols.min()/2.0, y0, (cols.max()+1)/2.0, y1)

def _ref(arr, r0, r1):
    seg=arr[max(0,r0):max(1,r1)]
    if seg.size==0: return None,0.0
    good=~pmask(seg)
    out=np.zeros((seg.shape[1],3),np.float32)
    for c in range(seg.shape[1]):
        col=seg[:,c][good[:,c]]
        out[c]=np.median(col,axis=0) if len(col)>=2 else np.median(seg[:,c],axis=0)
    grain=float(np.mean([np.std(seg[:,c][good[:,c]]) for c in range(0,seg.shape[1],37) if good[:,c].sum()>1]) or 0)
    return out, grain

def patch(p, bx, out_png, margin=2.0):
    W,H=p.rect.width,p.rect.height
    x0,y0,x1,y1=bx
    x0=max(0.0,x0-3); x1=min(W,x1+3)
    ytop=max(0.0,y0-margin); ybot=min(H,y1+margin)
    cy0=max(0.0,ytop-9); cy1=min(H,ybot+9)
    a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(x0,cy0,x1,cy1),colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.float32)
    top=int(round((ytop-cy0)*Z)); bot=int(round((ybot-cy0)*Z))
    if bot-top<4: return None
    A,ga=_ref(arr, top-int(7*Z), top-int(2*Z))
    B,gb=_ref(arr, bot+int(2*Z), bot+int(7*Z))
    if A is None or B is None: return None
    h=bot-top; t=np.linspace(0,1,h)[:,None,None]
    fill=A[None,:,:]*(1-t)+B[None,:,:]*t
    g=max(ga,gb)
    if g>0.5: fill=np.clip(fill+np.random.normal(0,g*0.5,fill.shape),0,255)
    out=arr.copy(); out[top:bot]=fill
    img=Image.fromarray(out.astype(np.uint8))
    al=np.full((img.size[1],img.size[0]),255,dtype=np.uint8)
    f=3
    for k in range(f):
        val=int(255*(k+1)/(f+1))
        for yy in (top+k, bot-1-k):
            if 0<=yy<img.size[1]: al[yy,:]=np.minimum(al[yy,:],val)
    img.putalpha(Image.fromarray(al)); img.save(out_png)
    return pymupdf.Rect(x0,cy0,x1,cy1)
