from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
F="/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf"
TEXT="موقع الطالب الخارجي"
CONTAINER_W_PAD=140
W,H=0,280
BG=(247,249,248)
S=2  # supersample
f=ImageFont.truetype(F,150*S)
d0=ImageDraw.Draw(Image.new("RGB",(10,10)))
bb=d0.textbbox((0,0),TEXT,font=f,direction="rtl",language="ar")
tw,th=bb[2]-bb[0],bb[3]-bb[1]
mask=Image.new("L",(tw+20*S,th+20*S),0)
ImageDraw.Draw(mask).text((10*S-bb[0],10*S-bb[1]),TEXT,font=f,fill=255,direction="rtl",language="ar")
mask=mask.resize((mask.width//S,mask.height//S),Image.LANCZOS)
W=mask.width+CONTAINER_W_PAD

TEAL_DARK=(8,47,41); TEAL=(15,107,92); TEAL_LIGHT=(79,208,180)

def grad(w,h,shift):
    g=Image.new("RGB",(w,1))
    px=g.load()
    stops=[(0,TEAL_DARK),(0.22,TEAL),(0.42,TEAL_LIGHT),(0.60,TEAL),(1,TEAL_DARK)]
    for x in range(w):
        t=((x/w)+shift)%1.0
        for i in range(len(stops)-1):
            a,ca=stops[i]; b,cb=stops[i+1]
            if a<=t<=b:
                k=(t-a)/(b-a)
                px[x,0]=tuple(int(ca[j]+(cb[j]-ca[j])*k) for j in range(3)); break
        else: px[x,0]=stops[-1][1]
    return g.resize((w,h))

frames=[]
N=40
for i in range(N):
    p=i/N
    th=math.radians(9.5*math.sin(2*math.pi*p))
    sx=math.cos(th); sy=1-0.035*abs(math.sin(2*math.pi*p))
    mw=max(4,int(mask.width*sx)); mh=int(mask.height*sy)
    m=mask.resize((mw,mh),Image.LANCZOS)
    canvas=Image.new("RGB",(W,H),BG)
    x=(W-mw)//2; y=(H-mh)//2
    # soft ground shadow
    sh=Image.new("L",(W,H),0); sh.paste(m,(x+10,y+18))
    sh=sh.filter(ImageFilter.GaussianBlur(9)).point(lambda v:int(v*0.22))
    canvas.paste(Image.new("RGB",(W,H),(13,31,28)),(0,0),sh)
    # extrusion
    depth=Image.new("RGBA",(W,H),(0,0,0,0))
    for k in range(8,0,-1):
        dcol=(10+k,74-k*3,64-k*2)
        d=Image.new("RGBA",(W,H),(0,0,0,0))
        d.paste(dcol+(255,),(x+int(k*0.9*sx),y+k),m)
        depth=Image.alpha_composite(depth,d)
    canvas.paste(depth,(0,0),depth)
    # face with shine
    shift=(p*1.2)%1.0
    face=grad(mw,mh,shift)
    canvas.paste(face,(x,y),m)
    frames.append(canvas)

frames[0].save("/home/superlisa/workspace/projects/school-site/scratch/wm/title3d.gif",
               save_all=True,append_images=frames[1:],duration=70,loop=0,optimize=True)
frames[10].save("/home/superlisa/workspace/projects/school-site/scratch/wm/title3d-frame.jpg",quality=93)
print("ok", frames[0].size)
