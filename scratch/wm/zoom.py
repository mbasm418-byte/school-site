import pymupdf
from PIL import Image, ImageDraw, ImageFont
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"
F="/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf"
Z=4.0; CS=250.0
def panel(nm):
    d=pymupdf.open(BASE%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    x0=max(0,W-CS); y0=max(0,H-CS)
    clip=pymupdf.Rect(x0,y0,W,H)
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csRGB)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    dr=ImageDraw.Draw(im)
    font=ImageFont.truetype(F,20)
    p=int(x0//10*10)
    while p<=W:
        xp=(p-x0)*Z
        if 0<=xp<pix.width:
            heavy=(p%50==0)
            dr.line([(xp,0),(xp,pix.height)],fill=(255,60,60) if heavy else (255,190,190),width=2 if heavy else 1)
            if heavy: dr.text((xp+3,3),"R%d"%round(W-p),fill=(170,0,0),font=font)
        p+=10
    p=int(y0//10*10)
    while p<=H:
        yp=(p-y0)*Z
        if 0<=yp<pix.height:
            heavy=(p%50==0)
            dr.line([(0,yp),(pix.width,yp)],fill=(40,90,255) if heavy else (185,200,255),width=2 if heavy else 1)
            if heavy: dr.text((3,yp+2),"B%d"%round(H-p),fill=(0,40,170),font=font)
        p+=10
    dr.text((pix.width-260,3),nm,fill=(0,120,0),font=ImageFont.truetype(F,30))
    return im
for k in range(0,8,2):
    a=panel(NAMES[k]); b=panel(NAMES[k+1])
    sheet=Image.new('RGB',(a.width+b.width+20,max(a.height,b.height)),(255,255,255))
    sheet.paste(a,(0,0)); sheet.paste(b,(a.width+20,0))
    sheet.save("/home/superlisa/workspace/projects/school-site/scratch/wm/z%d.png"%(k//2))
    print("z%d"%(k//2), sheet.size)
