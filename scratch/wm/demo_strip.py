import pymupdf
from strip2 import patch_for, band
books={"arabic":[6,60],"english":[6,60],"math_p1":[50,150],"biology_sajjad":[6,60]}
for b,pages in books.items():
    src=pymupdf.open("orig/%s.pdf"%b); res=pymupdf.open()
    for i in range(len(src)):
        p0=src[i]; W,H=p0.rect.width,p0.rect.height
        p=res.new_page(width=W,height=H); p.show_pdf_page(p.rect,src,i)
        if i in pages:
            bx=band(p0)
            if bx:
                r=patch_for(p0,bx,"pt_%s_%d.png"%(b,i))
                if r: p.insert_image(r,filename="pt_%s_%d.png"%(b,i))
                print(b,i+1,bx)
    res.save("sdemo_%s.pdf"%b,garbage=3,deflate=True)
