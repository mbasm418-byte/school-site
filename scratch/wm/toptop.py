import pymupdf
from PIL import Image, ImageDraw, ImageFont
NAMES=["arabic","islamiya","english","kimya","math_p1","physics","biology_sajjad","social"]
F="/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf"
def panel(nm):
    d=pymupdf.open("orig/%s.pdf"%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    Z=3.0; HH=100.0
    clip=pymupdf.Rect(0,0,W,HH)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csRGB)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    dr=ImageDraw.Draw(im); font=ImageFont.truetype(F,18)
    p=0
    while p<=HH:
        yp=p*Z
        heavy=(p%20==0)
        dr.line([(0,yp),(pix.width,yp)],fill=(255,40,40) if heavy else (255,200,200),width=2 if heavy else 1)
        if heavy: dr.text((3,yp+1),"y%d"%p,fill=(170,0,0),font=font)
        p+=10
    dr.text((pix.width-200,3),nm,fill=(0,110,0),font=ImageFont.truetype(F,26))
    return im
for k in range(0,8,2):
    a=panel(NAMES[k]); b=panel(NAMES[k+1])
    sheet=Image.new('RGB',(max(a.width,b.width),a.height+b.height+16),(255,255,255))
    sheet.paste(a,(0,0)); sheet.paste(b,(0,a.height+16))
    sheet.save("t%d.png"%(k//2)); print("t%d"%(k//2),sheet.size)
