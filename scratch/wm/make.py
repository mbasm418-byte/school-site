from PIL import Image, ImageDraw, ImageFont
F="/home/superlisa/.local/share/fonts/"
OUT="/home/superlisa/workspace/projects/school-site/scratch/wm/"
TEAL=(15,107,92); SLATE=(60,80,92); WHITE=(255,255,255)
def font(n,s): return ImageFont.truetype(F+n,s)

def line(text,f,fill,alpha=255):
    """returns RGBA tight-ish layer with correct RTL shaping"""
    tmp=ImageDraw.Draw(Image.new("RGB",(10,10)))
    bb=tmp.textbbox((0,0),text,font=f,direction="rtl",language="ar")
    w,h=bb[2]-bb[0],bb[3]-bb[1]
    lay=Image.new("RGBA",(w+8,h+8),(0,0,0,0))
    d=ImageDraw.Draw(lay)
    d.text((4-bb[0],4-bb[1]),text,font=f,fill=fill+(alpha,),direction="rtl",language="ar")
    lay.putalpha(lay.getchannel("A").point(lambda v:int(v*alpha/255)))
    return lay

# ---------- A: horizontal band ----------
W,H=1600,380
a=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(a)
t=line("موقع الطالب الخارجي",font("Tajawal-Bold.ttf",98),TEAL)
a.alpha_composite(t,((W-t.width)//2,70))
d.line([(W/2-330,262),(W/2+330,262)],fill=TEAL+(130,),width=3)
s=line("ملازم الثالث المتوسط  ·  2026 – 2027",font("Tajawal-Medium.ttf",44),SLATE)
a.alpha_composite(s,((W-s.width)//2,292))
a.save(OUT+"wm-A.png")

# ---------- B: round stamp ----------
S=560; b=Image.new("RGBA",(S,S),(0,0,0,0)); d=ImageDraw.Draw(b)
d.ellipse([16,16,S-16,S-16],outline=TEAL+(255,),width=7)
d.ellipse([38,38,S-38,S-38],outline=TEAL+(140,),width=2)
t1=line("موقع الطالب",font("Tajawal-Bold.ttf",72),TEAL)
t2=line("الخارجي",font("Tajawal-Bold.ttf",72),TEAL)
b.alpha_composite(t1,((S-t1.width)//2,150)); b.alpha_composite(t2,((S-t2.width)//2,232))
d.line([(S/2-120,330),(S/2+120,330)],fill=TEAL+(150,),width=2)
t3=line("ملازم مجانية لطلاب الثالث",font("Tajawal-Medium.ttf",30),SLATE)
b.alpha_composite(t3,((S-t3.width)//2,352))
b.save(OUT+"wm-B.png")

# ---------- C: tiled diagonal ----------
T=800
base=line("موقع الطالب الخارجي",font("Tajawal-Bold.ttf",46),TEAL)
base=base.rotate(28,expand=True,resample=Image.BICUBIC)
base.putalpha(base.getchannel("A").point(lambda v:int(v*0.75)))  # low-opacity ink
tw,th=base.size
tile=Image.new("RGBA",(T,T),(0,0,0,0))
cx,cy=(T-tw)//2,(T-th)//2
for ox in (-T,0,T):
    for oy in (-T,0,T):
        tile.alpha_composite(base,(cx+ox,cy+oy))
tile.save(OUT+"wm-C-tile.png")

pg=Image.new("RGBA",(1000,1414),WHITE+(255,))
for y in range(0,1414,T):
    for x in range(0,1000,T): pg.alpha_composite(tile,(x,y))
pg.convert("RGB").save(OUT+"preview-C.jpg",quality=88)

for src,size,nm in [(OUT+"wm-A.png",(1000,440),"A"),(OUT+"wm-B.png",(700,700),"B")]:
    im=Image.open(src); cv=Image.new("RGBA",size,WHITE+(255,))
    cv.alpha_composite(im,((size[0]-im.width)//2,(size[1]-im.height)//2))
    cv.convert("RGB").save(OUT+f"preview-{nm}.jpg",quality=93)
print("ok")
