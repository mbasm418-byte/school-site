import pymupdf, numpy as np
from PIL import Image, ImageDraw, ImageFont
NAMES=["arabic","islamiya","english","math_p1","kimya","physics","biology_sajjad","social"]
BASE="/home/superlisa/workspace/projects/school-site/scratch/wm/orig/%s.pdf"
FONT="/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf"
TOP={"arabic":1070,"english":1164.6,"physics":1125,"biology_sajjad":1125,"social":1160.6,
     "math_p1":None,"kimya":None,"islamiya":None}
OUT=[]
for nm in NAMES:
    d=pymupdf.open(BASE%nm); pg=d[5]
    W,H=pg.rect.width,pg.rect.height
    R=0.092*W; cx=W-0.105*W
    cy = TOP[nm]+R if TOP[nm] else H-0.10*H
    clip=pymupdf.Rect(W*0.62,H*0.72,W,H)
    Z=1.6
    pix=pg.get_pixmap(clip=clip,matrix=pymupdf.Matrix(Z,Z),colorspace=pymupdf.csRGB)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    dr=ImageDraw.Draw(im)
    def P(x,y): return ((x-clip.x0)*Z,(y-clip.y0)*Z)
    dr.ellipse([P(cx-R,cy-R),P(cx+R,cy+R)],outline=(255,0,180),width=3)
    dr.line([P(cx-6,cy),P(cx+6,cy)],fill=(255,0,180),width=2)
    dr.line([P(cx,cy-6),P(cx,cy+6)],fill=(255,0,180),width=2)
    dr.text((6,6),"%s R=%.1f cx=%.1f cy=%.1f"%(nm,R,cx,cy),fill=(180,0,0),font=ImageFont.truetype(FONT,22))
    OUT.append(im)
cw=max(i.width for i in OUT); ch=max(i.height for i in OUT)
sheet=Image.new('RGB',(cw*2+30, ch*4+50),(255,255,255))
for i,im in enumerate(OUT):
    sheet.paste(im,((i%2)*(cw+30),(i//2)*(ch+16)))
sheet.save("/home/superlisa/workspace/projects/school-site/scratch/wm/verify1.png")
print(sheet.size)
