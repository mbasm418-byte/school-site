from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 64
teal = (15, 107, 92)
grey = (122, 143, 136)
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

f_name = ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Bold.ttf", 32)
f_sub  = ImageFont.truetype("/home/superlisa/.local/share/fonts/Tajawal-Regular.ttf", 21)

def text_rtl(xy, text, font, fill):
    d.text(xy, text, font=font, fill=fill, direction="rtl", language="ar", anchor="rm")

text_rtl((W - 44, H // 2 - 3), "موقع الطالب الخارجي", f_name, teal)
text_rtl((44 + 330, H // 2 - 2), "ملازم الثالث المتوسط", f_sub, grey)
d.line([(0, H - 3), (W, H - 3)], fill=teal, width=3)
img.save("band.png")
