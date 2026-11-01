import pymupdf, numpy as np
from PIL import Image
Z=3.0
PILCOL=((85,85,88),(12,144,230),(230,25,32))
TOL=24
def _mask(arr):
    m=np.zeros(arr.shape[:2],bool)
    for c in PILCOL:
        m|=(np.abs(arr[...,0]-c[0])<=TOL)&(np.abs(arr[...,1]-c[1])<=TOL)&(np.abs(arr[...,2]-c[2])<=TOL)
    return m

def band(p):
    W=p.rect.width
    a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(0,0,W,min(130,p.rect.height)),colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.int16)
    m=_mask(arr)
    cnt=m.sum(1); thr=a.width*0.02
    rows=np.where(cnt>thr)[0]
    if len(rows)<3: return None
    runs=[]; s=rows[0]; pr=rows[0]
    for y in rows[1:]:
        if y-pr<=3: pr=y; continue
        runs.append((s,pr)); s=y; pr=y
    runs.append((s,pr))
    runs=[r for r in runs if r[1]-r[0]>=int(6*Z)]
    if not runs: return None
    best=max(runs,key=lambda t:cnt[t[0]:t[1]+1].sum())
    y0=best[0]/Z; y1=(best[1]+1)/Z
    sub=m[best[0]:best[1]+1]
    cols=np.where(sub.any(0))[0]
    x0=cols.min()/Z; x1=(cols.max()+1)/Z
    return (x0,y0,x1,y1)

def patch(p, bx, out_png):
    W,H=p.rect.width,p.rect.height
    x0,y0,x1,y1=bx
    # expand band until reference rows are clean
    ytop=max(0.0,y0-2); ybot=min(H,y1+2)
    for _ in range(10):
        if ytop<=0.5 or ybot>=H-0.5: break
        ok=True
        for yy in (ytop-1.5, ytop-3.5, ybot+1.5, ybot+3.5):
            if yy<0 or yy>=H: ok=False; break
            a=p.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(x0,yy-0.5,x1,yy+0.5),colorspace=pymupdf.csRGB)
            ar=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.int16)
            if _mask(ar).sum()>a.width*0.01: ok=False; break
        if ok: break
        ytop=max(0.0,ytop-2); ybot=min(H,ybot+2)
    x0=max(0.0,x0-3); x1=min(W,x1+3); ytop=max(0.0,ytop-1); ybot=min(H,ybot+1)
    pad=10.0
    cy0=max(0.0,ytop-pad); cy1=min(H,ybot+pad)
    a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(x0,cy0,x1,cy1),colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.float32)
    top=int(round((ytop-cy0)*Z)); bot=int(round((ybot-cy0)*Z))
    if bot-top<4: return None
    t_up=max(0,top-int(5*Z)); t_dn=max(0,top-1)
    b_up=min(a.height,bot+1); b_dn=min(a.height,bot+int(5*Z))
    if t_dn<=t_up or b_dn<=b_up: return None
    A=np.median(arr[t_up:t_dn],axis=0); B=np.median(arr[b_up:b_dn],axis=0)
    h=bot-top; t=np.linspace(0,1,h)[:,None,None]
    fill=A[None,:,:]*(1-t)+B[None,:,:]*t
    grain=float(np.mean(np.std(arr[t_up:t_dn],axis=0)))
    if grain>0.5: fill=np.clip(fill+np.random.normal(0,grain*0.5,fill.shape),0,255)
    out=arr.copy(); out[top:bot]=fill
    img=Image.fromarray(out.astype(np.uint8))
    al=np.full((img.size[1],img.size[0]),255,dtype=np.uint8)
    f=3
    for k in range(f):
        val=int(255*(k+1)/(f+1))
        for yy in (top+k, bot-1-k):
            if 0<=yy<img.size[1]: al[yy,:]=np.minimum(al[yy,:],val)
    img.putalpha(Image.fromarray(al)); img.save(out_png)
    return pymupdf.Rect(x0,ytop,x1,ybot)
