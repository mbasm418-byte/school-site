import pymupdf, numpy as np, glob, os
from PIL import Image, ImageDraw, ImageFont
books=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
Z=2.0; CUT=110
fnt=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",26)
for part in (0,1):
    grp=books[part*4:(part+1)*4]
    rows=[]
    for b in grp:
        d=pymupdf.open("orig/%s.pdf"%b)
        p=d[min(5,len(d)-1)]
        W=p.rect.width
        a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=pymupdf.Rect(0,0,W,CUT),colorspace=pymupdf.csRGB)
        im=Image.frombytes("RGB",(a.width,a.height),a.samples)
        cv=Image.new("RGB",(im.width,im.height+30),(255,255,255))
        cv.paste(im,(0,30))
        dr=ImageDraw.Draw(cv)
        dr.text((8,2),b,font=fnt,fill=(0,0,0))
        for y in range(0,CUT,10):
            yy=30+int(y*Z)
            dr.line([(0,yy),(im.width,yy)],fill=(255,0,0) if y%50==0 else (255,170,170),width=1)
            if y%50==0: dr.text((im.width-52,yy+1),"y%d"%y,font=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",20),fill=(255,0,0))
        rows.append(cv)
    Wm=max(r.width for r in rows); Hm=sum(r.height for r in rows)
    out=Image.new("RGB",(Wm,Hm),(255,255,255)); y=0
    for r in rows: out.paste(r,(0,y)); y+=r.height
    out.save("tv%d.png"%part)
    print("tv%d.png"%part, out.size)
