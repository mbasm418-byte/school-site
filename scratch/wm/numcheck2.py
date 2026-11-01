import pymupdf
from PIL import Image, ImageDraw, ImageFont
G={"arabic":(833.6,1156.6,86.2),"english":(850.6,1250.4,87.5),"social":(856.1,1249.9,88.5)}
f=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",16)
cells=[]
for b in G:
    cx,cy,R=G[b]; d=pymupdf.open("orig/%s.pdf"%b)
    for i in [6,60,120,150]:
        if i>=len(d): continue
        r=pymupdf.Rect(cx-R,cy+0.05*R,cx+R,cy+0.95*R)
        a=d[i].get_pixmap(matrix=pymupdf.Matrix(2.2,2.2),clip=r,colorspace=pymupdf.csRGB)
        im=Image.frombytes("RGB",(a.width,a.height),a.samples)
        cv=Image.new("RGB",(im.width,im.height+18),(255,255,255)); cv.paste(im,(0,18))
        ImageDraw.Draw(cv).text((3,0),"%s p%d"%(b,i+1),font=f,fill=(0,0,0))
        cells.append(cv)
W=max(c.width for c in cells); H=max(c.height for c in cells)
out=Image.new("RGB",(W*4,H*3),(255,255,255))
for k,c in enumerate(cells): out.paste(c,((k%4)*W,(k//4)*H))
out.save("numcheck2.png"); print(out.size)
