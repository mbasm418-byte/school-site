import pymupdf, numpy as np, os
from PIL import Image
Z=3.0
def band(p):
    from strip import detect
    return detect(p)

def patch_for(p, bx, out_png):
    W,H=p.rect.width,p.rect.height
    x0,y0,x1,y1=bx
    x0=max(0,x0-2); x1=min(W,x1+2)
    y0=max(0,y0-2.0); y1=min(H,y1+2.0)
    pad=8
    cy0=max(0,y0-pad); cy1=min(H,y1+pad)
    clip=pymupdf.Rect(x0,cy0,x1,cy1)
    a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=clip,colorspace=pymupdf.csRGB)
    arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.float32)
    top=int(round((y0-cy0)*Z)); bot=int(round((y1-cy0)*Z))
    w=a.width
    t_up=max(0,top-6); t_dn=max(0,top-1)
    b_up=min(a.height,bot+1); b_dn=min(a.height,bot+6)
    if t_dn<=t_up or b_dn<=b_up:
        return None
    A=np.median(arr[t_up:t_dn],axis=0)   # (w,3)
    B=np.median(arr[b_up:b_dn],axis=0)
    h=bot-top
    t=np.linspace(0,1,h)[:,None,None]
    fill=(A[None,:,:]*(1-t)+B[None,:,:]*t)
    # grain from reference rows
    grain=float(np.mean(np.std(arr[t_up:t_dn],axis=0)))
    if grain>0.5:
        fill=np.clip(fill+np.random.normal(0,grain*0.55,fill.shape),0,255)
    out=arr.copy()
    out[top:bot]=fill
    img=Image.fromarray(out.astype(np.uint8))
    # feather alpha: fade 1.5pt at top/bottom edges of the band region only
    al=np.full((img.size[1],img.size[0]),255,dtype=np.uint8)
    hh=img.size[1]
    f=3
    for k in range(f):
        val=int(255*(k+1)/(f+1))
        yy=top+k
        if 0<=yy<hh: al[yy,:]=val
        yy=bot-1-k
        if 0<=yy<hh: al[yy,:]=val
    img.putalpha(Image.fromarray(al))
    img.save(out_png)
    return pymupdf.Rect(x0,y0,x1,y1)
