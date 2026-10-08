import sys, base64, io
from PIL import Image
from playwright.sync_api import sync_playwright
ids=sys.argv[1].split(',')
out=sys.argv[2]; N=int(sys.argv[3]) if len(sys.argv)>3 else 18; S=360
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"])
    pg=b.new_page()
    for i in ids:
        pg.goto(f"http://localhost:18931/render.html?id={i}&n={N}&s={S}&span=100", wait_until="load")
        pg.wait_for_function("window.done===true", timeout=120000)
        fr=pg.evaluate("window.frames_")
        ims=[Image.open(io.BytesIO(base64.b64decode(f.split(',')[1]))) for f in fr]
        strip=Image.new("RGBA",(S*N,S))
        for k,im in enumerate(ims): strip.paste(im,(k*S,0))
        strip.save(f"{out}/{i}.png"); print(i, flush=True)
    b.close()
