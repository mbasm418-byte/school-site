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
    """Return (x0,y0,x1,y1) in page points of the branding strip, or None."""
    W=p.rect.width
    a=p.get_pixmap(matrix=pymupdf.Matrix(2,2),clip=pymupdf.Rect(0,0,W,min(170,p.rect.height)),colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.int16)
    m=pmask(arr); cnt=m.sum(1); thr=a.width*0.25
    dense=np.where(cnt>thr)[0]
    if len(dense)<int(4*2): return None
    runs=[]; s=dense[0]; pr=dense[0]
    for y in dense[1:]:
        if y-pr<=6: pr=y; continue
        runs.append((s,pr)); s=y; pr=y
    runs.append((s,pr))
    runs=[r for r in runs if r[1]-r[0]>=int(8*2)]
    if not runs: return None
    s,e=runs[0]                       # first strip from the top
    # rows: extend while still meaningfully covered
    while s>0 and cnt[s-1]>a.width*0.10: s-=1
    while e+1<len(cnt) and cnt[e+1]>a.width*0.10: e+=1
    sub=m[s:e+1]
    cols=np.where(sub.any(0))[0]
    cw=sub.sum(0)
    strong=np.where(cw>2)[0]
    if len(strong): cols=np.array([strong.min(),strong.max()])
    return (max(0.0,cols[0]/2.0-1), max(0.0,s/2.0-0.5), min(W,(cols[-1]+1)/2.0+1), (e+1)/2.0+0.5)

def patch(p, bx, out_png, feather=3.0, ctx=16.0):
    W,H=p.rect.width,p.rect.height
    x0,y0,x1,y1=bx
    cy0=max(0.0,y0-ctx); cy1=min(H,y1+ctx)
    a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(x0,cy0,x1,cy1),colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.float32)
    top=int(round((y0-cy0)*Z)); bot=int(round((y1-cy0)*Z))
    if bot-top<4: return None
    pm=pmask(arr.astype(np.int16))
    rowfrac=pm.mean(1)
    def clean_rows(start, maxscan):
        """Rows from `start` downward that are free of pill pixels."""
        keep=[]
        y=start
        limit=min(arr.shape[0], start+maxscan)
        while y<limit:
            if rowfrac[y]<0.15: keep.append(y)
            y+=1
        return keep
    def clean_rows_up(start, maxscan):
        keep=[]
        y=start
        limit=max(0, start-maxscan)
        while y>limit:
            if 0<=y<arr.shape[0] and rowfrac[y]<0.15: keep.append(y)
            y-=1
        return keep
    def ref(rows):
        if not rows: return None
        seg=arr[rows]
        out=np.median(seg,axis=0)
        k=int(3.2*Z)|1
        pad=np.pad(out,((k//2,k//2),(0,0)),mode='edge')
        win=np.lib.stride_tricks.sliding_window_view(pad,(k,3),axis=(0,1))
        return np.median(win,axis=2).reshape(-1,3)
    below=ref(clean_rows(bot+int(1.5*Z), int(14*Z))[:5])
    above=ref(clean_rows_up(top-int(2*Z), int(14*Z)))
    if below is None: return None
    if above is None: above=below
    h=bot-top
    fill=np.repeat(below[None,:,:],h,axis=0).copy()
    f=max(1,int(round(feather*Z)))
    for k in range(min(f,h)):
        t=1.0-(k+1)/(f+1.0)
        fill[k]=fill[k]*(1-t)+above*t
    segpx=arr[max(0,top-int(4*Z)):top]
    g=float(np.std(segpx-np.median(segpx,axis=(0,1),keepdims=True))) if segpx.size else 0
    if g>1.0: fill=np.clip(fill+np.random.normal(0,min(g,5)*0.3,fill.shape),0,255)
    out=arr.copy(); out[top:bot]=fill
    img=Image.fromarray(out.astype(np.uint8))
    al=np.full((img.size[1],img.size[0]),255,dtype=np.uint8)
    for k in range(2):
        val=int(255*(k+1)/3)
        yy=bot-1-k
        if 0<=yy<img.size[1]: al[yy,:]=np.minimum(al[yy,:],val)
    img.putalpha(Image.fromarray(al)); img.save(out_png)
    return pymupdf.Rect(x0,cy0,x1,cy1)
