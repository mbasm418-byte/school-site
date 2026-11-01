import pymupdf, numpy as np
from PIL import Image, ImageDraw, ImageFont
G={"arabic":(833.6,1156.6,86.2),"islamiya":(526.8,725.5,54.0),"english":(850.6,1250.4,87.5),
   "math_p1":(851.6,1216.0,86.5),"kimya":(535.4,782.0,55.0),"physics":(850.6,1212.9,87.2),
   "biology_sajjad":(851.6,1239.4,88.0),"social":(856.1,1249.9,88.5)}
S=300; Z=1.0
cells=[]
f=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",18)
for b,(cx,cy,R) in G.items():
    d=pymupdf.open("orig/%s.pdf"%b)
    p=d[min(6,len(d)-1)]
    clip=pymupdf.Rect(cx-S/2,cy-S/2,cx+S/2,cy+S/2)
    a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=clip,colorspace=pymupdf.csRGB)
    im=Image.frombytes("RGB",(a.width,a.height),a.samples)
    cv=Image.new("RGB",(im.width,im.height+20),(255,255,255)); cv.paste(im,(0,20))
    dr=ImageDraw.Draw(cv); dr.text((4,0),b,font=f,fill=(0,0,0))
    # mark measured circle
    dr.ellipse([S/2-R+im.width/2-S/2+ (0), 20+S/2-R, 20+S/2+R, 20+S/2+R],outline=(255,0,0),width=2)
    cells.append(cv)
W,H=cells[0].size
out=Image.new("RGB",(W*4,H*2),(255,255,255))
for i,c in enumerate(cells): out.paste(c,((i%4)*W,(i//4)*H))
out.save("dv.png"); print(out.size)
