import pymupdf, os, time, sys

BAND = 'scratch/wm/band.png'
files = ['arabic_web.pdf','islamiya_web.pdf','english_web.pdf','math_p1_web.pdf',
         'kimya_web.pdf','physics_web.pdf','biology_sajjad_web.pdf','social_web.pdf']
os.makedirs('scratch/wm/out', exist_ok=True)

for f in files:
    t0 = time.time()
    src = pymupdf.open(f)
    out = pymupdf.open()
    for i in range(len(src)):
        sp = src[i]
        W, H = sp.rect.width, sp.rect.height
        BH = max(24, round(W * 0.03))
        np = out.new_page(width=W, height=H + BH)
        np.show_pdf_page(pymupdf.Rect(0, BH, W, H + BH), src, i)
        np.insert_image(pymupdf.Rect(0, 0, W, BH), filename=BAND, keep_proportion=False)
    dst = f'scratch/wm/out/{f}'
    out.save(dst, garbage=3, deflate=True, clean=True)
    print(f'{f}: {len(src)} pages, {os.path.getsize(f)/1e6:.1f}MB -> {os.path.getsize(dst)/1e6:.1f}MB, {time.time()-t0:.1f}s', flush=True)
    out.close(); src.close()
