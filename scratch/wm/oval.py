import pymupdf
from PIL import Image, ImageDraw, ImageFont
G={"arabic":(833.6,1156.6,86.2),"islamiya":(526.8,725.5,54.0),"math_p1":(851.6,1216.0,86.5)}
f=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",16)
cells=[]
for b,(cx,cy,R) in G.items():
    d=pymupdf.open("orig/%s.pdf"%b)
    for i in [6,60]:
        r=pymupdf.Rect(cx-1.0*R,cy-0.1*R,cx+1.0*R,cy+0.7*R)
        a=d[i].get_pixmap(matrix=pymupdf.Matrix(4,4),clip=r,colorspace=pymupdf.csRGB)
        im=Image.frombytes("RGB",(a.width,a.height),a.samples)
        cv=Image.new("RGB",(im.width,im.height+18),(255,255,255)); cv.paste(im,(0,18))
        ImageDraw.Draw(cv).text((3,0),"%s p%d"%(b,i+1),font=f,fill=(0,0,0))
        cells.append(cv)
W=max(c.width for c in cells); H=max(c.height for c in cells)
out=Image.new("RGB",(W*2,H*3),(255,255,255))
for k,c in enumerate(cells): out.paste(c,((k%2)*W,(k//2)*H))
out.save("oval.png"); print(out.size)
