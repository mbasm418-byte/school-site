from PIL import Image, ImageDraw, ImageFont
F={}
def font(px):
    px=int(max(8,round(px)))
    if px not in F: F[px]=ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf",px)
    return F[px]
TEAL=(15,107,92,255); INK=(13,31,28,255); RING=(230,242,239,255)
def make(path, Rb, num, label="ثالث متوسط", ss=4):
    """Rb = cover radius in points, ss = px per point"""
    px=int(round(2*Rb*ss))+2
    im=Image.new("RGBA",(px,px),(0,0,0,0)); dr=ImageDraw.Draw(im)
    c=px/2.0; R=Rb*ss
    dr.ellipse([c-R,c-R,c+R,c+R],fill=(255,255,255,255))
    dr.ellipse([c-R,c-R,c+R,c+R],outline=TEAL,width=max(2,int(R*0.055)))
    r2=R*0.895
    dr.ellipse([c-r2,c-r2,c+r2,c+r2],outline=RING,width=max(1,int(R*0.016)))
    # number sized to fit inside
    s=R*1.02
    for _ in range(40):
        f=font(s); w=dr.textlength(num,font=f)
        if w<=R*1.35 and s<=R*1.02: break
        s*=0.94
    dr.text((c,c-R*0.13),num,font=f,fill=INK,anchor="mm")
    ls=R*0.195
    for _ in range(30):
        f2=font(ls); w2=dr.textlength(label,font=f2)
        if w2<=R*1.45: break
        ls*=0.95
    dr.text((c,c+R*0.46),label,font=f2,fill=TEAL,anchor="mm")
    im.save(path); return px
