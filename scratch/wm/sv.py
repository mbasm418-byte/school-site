import pymupdf
from PIL import Image, ImageDraw, ImageFont
f=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",18)
items=[("arabic",6,110),("english",6,110),("math_p1",50,110),("biology_sajjad",6,110),("biology_sajjad",60,110)]
cells=[]
for b,i,cut in items:
    d=pymupdf.open("sdemo_%s.pdf"%b); p=d[i]; W=p.rect.width
    a=p.get_pixmap(matrix=pymupdf.Matrix(1.6,1.6),clip=pymupdf.Rect(0,0,W,cut),colorspace=pymupdf.csRGB)
    im=Image.frombytes("RGB",(a.width,a.height),a.samples)
    cv=Image.new("RGB",(im.width,im.height+20),(255,255,255)); cv.paste(im,(0,20))
    ImageDraw.Draw(cv).text((4,1),"%s p%d"%(b,i+1),font=f,fill=(0,0,0))
    cells.append(cv)
W=max(c.width for c in cells); H=max(c.height for c in cells)
out=Image.new("RGB",(W,H*len(cells)),(255,255,255))
for k,c in enumerate(cells): out.paste(c,(0,k*H))
out.save("sv.png"); print(out.size)
