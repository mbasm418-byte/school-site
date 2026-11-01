import pymupdf, numpy as np, glob, os
for f in sorted(glob.glob("orig/*.pdf")):
    d=pymupdf.open(f); n=len(d)
    W,H=d[0].rect.width,d[0].rect.height
    z=3.0
    pil=[]
    bgs=[]
    for i in range(0,n,max(1,n//12)):
        p=d[i]; a=p.get_pixmap(matrix=pymupdf.Matrix(z,z),colorspace=pymupdf.csRGB)
        arr=np.frombuffer(a.samples,dtype=np.uint8).reshape(a.height,a.width,3).astype(np.int16)
        top=arr[:int(60*z)]
        mx=top.max(2); mn=top.min(2)
        sat=(mx-mn)
        rows=np.where((sat>50).sum(1) > a.width*0.04)[0]
        pil.append(int(rows.max()/z) if len(rows) else 0)
        # background sample: rows y=45..60, x in left 6%
        bg=arr[int(45*z):int(60*z), :int(a.width*0.06)].reshape(-1,3)
        bgs.append(np.median(bg,0))
    bgm=np.median(np.array(bgs),0)
    print(os.path.basename(f), "W=%.0f"%W, "maxpill_y:", pil, "bg:", bgm.astype(int).tolist())
