# Clean and upscale line art to 2250x3000 (7.5 x 10 in at 300 dpi), crisp black on white
import sys, glob, os
from PIL import Image, ImageFilter
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(src + "/p*.png")):
    im = Image.open(f).convert("L").resize((2250, 3000), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    # steep levels: everything below 110 -> black, above 170 -> white, smooth ramp between
    lut = [0 if v < 110 else 255 if v > 170 else int((v-110)/60*255) for v in range(256)]
    im = im.point(lut)
    hist = im.histogram(); tot = sum(hist)
    black = sum(hist[:40])/tot; mid = sum(hist[40:216])/tot
    print(os.path.basename(f), f"black={black:.3f} mid={mid:.4f}")
    im.save(os.path.join(out, os.path.basename(f)), optimize=True)
