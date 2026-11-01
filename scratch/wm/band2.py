from PIL import Image, ImageDraw, ImageFont

F = "/home/superlisa/.local/share/fonts/"
W, H = 3200, 96                       # aspect ~ W*0.03 like BH on the page
TEAL = (15, 107, 92)
GREY = (122, 143, 136)
PAD = 90


def layer(text, font, fill):
    """Tight RGBA layer with correct RTL shaping."""
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    bb = tmp.textbbox((0, 0), text, font=font, direction="rtl", language="ar")
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    lay = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((4 - bb[0], 4 - bb[1]), text, font=font, fill=fill + (255,),
           direction="rtl", language="ar")
    return lay


img = Image.new("RGB", (W, H), "white")
main = layer("موقع الطالب الخارجي", ImageFont.truetype(F + "Tajawal-Bold.ttf", 62), TEAL)
sub = layer("ملازم الثالث المتوسط", ImageFont.truetype(F + "Tajawal-Regular.ttf", 40), GREY)

# centre both vertically in the white area above the separator
cy = (H - 6) // 2
img.paste(main, (W - PAD - main.width, cy - main.height // 2), main)
img.paste(sub, (PAD, cy - sub.height // 2), sub)

d = ImageDraw.Draw(img)
d.rectangle([0, H - 6, W, H], fill=TEAL)

img.save("band.png")
print("band.png", img.size, "main", main.size, "sub", sub.size)
