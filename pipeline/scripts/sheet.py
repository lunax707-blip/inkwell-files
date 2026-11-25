import sys, glob
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(src + "/p*.png"))
for s in range(0, len(files), 10):
    sheet = Image.new("RGB", (5*400, 2*540), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(files[s:s+10]):
        im = Image.open(f).convert("RGB")
        print(f.split("/")[-1], im.size)
        im.thumbnail((390, 520))
        x, y = (i % 5)*400 + 5, (i // 5)*540 + 15
        sheet.paste(im, (x, y))
        d.text((x+4, y-13), f.split("/")[-1], fill="red")
    sheet.save(f"{out}/sheet{s//10+1}.png")
