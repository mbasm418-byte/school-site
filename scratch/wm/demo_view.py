import pymupdf
from PIL import Image, ImageDraw, ImageFont
G={"arabic":(833.6,1156.6,86.2),"english":(850.6,1250.4,87.5),"social":(856.1,1249.9,88.5)}
P={"arabic":[6,60,150],"english":[6,60,110],"social":[6,60,150]}
Z=1.4; S=270
f=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",18)
cells=[]
for b in G:
    cx,cy,R=G[b]; d=pymupdf.open("demo_%s.pdf"%b)
    for i in P[b]:
        p=d[i]; W,H=p.rect.width,p.rect.height
        r=pymupdf.Rect(cx-S/2,cy-S/2,cx+S/2,cy+S/2) & p.rect
        a=p.get_pixmap(matrix=pymupdf.Matrix(Z,Z),clip=r,colorspace=pymupdf.csRGB)
        im=Image.frombytes("RGB",(a.width,a.height),a.samples)
        cv=Image.new("RGB",(int(S*Z),int(S*Z)+22),(240,240,240))
        cv.paste(im,(int((S*Z-a.width)/2),22))
        ImageDraw.Draw(cv).text((4,2),"%s p%d"%(b,i+1),font=f,fill=(0,0,0))
        cells.append(cv)
W,H=cells[0].size
out=Image.new("RGB",(W*3,H*3),(255,255,255))
for k,c in enumerate(cells): out.paste(c,((k%3)*W,(k//3)*H))
out.save("demo1.png"); print(out.size)
