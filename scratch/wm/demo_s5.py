import pymupdf
from strip5 import band, patch
books={"arabic":[6,60],"english":[6,60],"math_p1":[6,50],"biology_sajjad":[6,60,100],"social":[6,60],"physics":[6,60],"kimya":[6,60],"islamiya":[6,60]}
for b in books:
    src=pymupdf.open("orig/%s.pdf"%b); res=pymupdf.open()
    for i in range(len(src)):
        p0=src[i]; W,H=p0.rect.width,p0.rect.height
        p=res.new_page(width=W,height=H); p.show_pdf_page(p.rect,src,i)
        if i in books[b]:
            bx=band(p0)
            if bx:
                r=patch(p0,bx,"s5_%s_%d.png"%(b,i))
                if r: p.insert_image(r,filename="s5_%s_%d.png"%(b,i))
    res.save("s5_%s.pdf"%b,garbage=3,deflate=True)
print("ok")
