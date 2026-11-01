import pymupdf, numpy as np, os
from PIL import Image, ImageDraw, ImageFont
G={"arabic":(833.6,1156.6,86.2),"islamiya":(526.8,725.5,54.0),"english":(850.6,1250.4,87.5),
   "math_p1":(851.6,1216.0,86.5),"kimya":(535.4,782.0,55.0),"physics":(850.6,1212.9,87.2),
   "biology_sajjad":(851.6,1239.4,88.0),"social":(856.1,1249.9,88.5)}
F="/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf"
from badge import make
def build(out, sample, pages, Rpad=12):
    d=pymupdf.open("orig/%s.pdf"%out); res=pymupdf.open()
    src=pymupdf.open("orig/%s.pdf"%out)
    for i in range(len(src)):
        W,H=src[i].rect.width,src[i].rect.height
        p=res.new_page(width=W,height=H)
        p.show_pdf_page(p.rect,src,i)
        if i in pages:
            cx,cy,R=G[out]
            Rp=R+Rpad
            px=make("scratchbadge_%s.png"%out,Rp,str(i+1)) if os.path.isdir(".") else None
            p.insert_image(pymupdf.Rect(cx-Rp,cy-Rp,cx+Rp,cy+Rp),filename="scratchbadge_%s.png"%out)
    res.save(sample,garbage=3,deflate=True)
    print("wrote",sample)
for b,pages in [("arabic",{6,60,150}),("english",{6,60,110}),("social",{6,60,150})]:
    build(b,"demo_%s.pdf"%b,pages)
