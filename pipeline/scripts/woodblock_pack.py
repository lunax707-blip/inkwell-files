# Wall art set packer (25 Nov 2026): 6 upscaled JPGs -> named 300 dpi JPGs, READ_ME, zip, two titled covers
# usage: python3 woodblock_pack.py <hi_dir with 1.jpg..6.jpg> <out_dir>
import sys, os, zipfile, glob
from PIL import Image, ImageDraw, ImageFilter, ImageFont
hi, out = sys.argv[1], sys.argv[2]
F = "/home/claude/fonts/ttf"
NAME = "Japanese_Woodblock_Landscapes"
TITLE = "Japanese Woodblock Landscapes"
SUB = "SET OF 6 PRINTABLE ART PRINTS   3:4 RATIO   HIGH RESOLUTION JPG"
ITEMS = ["01_Mountain_at_Dawn", "02_Pine_and_Waves", "03_Maple_Waterfall", "04_Moon_over_the_Lake", "05_Blossom_Bridge", "06_Summer_Rain"]
README = """Thank you for your purchase.

Japanese Woodblock Landscapes, a set of 6 art prints:
01 Mountain at Dawn
02 Pine and Waves
03 Maple Waterfall
04 Moon over the Lake
05 Blossom Bridge
06 Summer Rain

These are high resolution 3:4 ratio JPG files (3072 x 4096 pixels). They print well at 6 x 8, 9 x 12 and 12 x 16 inches (15 x 20, 30 x 40 cm) with no cropping.
For A4, A3 or 8 x 10 frames, choose 'fill page' or 'fit to frame' when printing and a small edge will be trimmed.

Print at home on matte photo paper or thick card, or send the file to any print shop or online print service.
Colors can look slightly different on paper than on screen.

These are original digital artworks made in the manner of Edo period Japanese woodblock prints. They are not reproductions of museum prints.

For personal use only. Please do not resell or share the files.
"""
WALL, NAVY, CORAL = (226, 218, 206), (43, 58, 103), (217, 88, 59)
def framed(p, w2):
    h2 = int(w2*4/3); b = max(8, w2//48); m = int(w2*0.082)
    fr = Image.new("RGB", (w2, h2), (35, 32, 30)); mat = Image.new("RGB", (w2-2*b, h2-2*b), (250, 248, 243)); fr.paste(mat, (b, b))
    art = Image.open(p).convert("RGB").resize((w2-2*b-2*m, h2-2*b-2*m), Image.LANCZOS); fr.paste(art, (b+m, b+m))
    return fr
def place(bg, fr, x, y):
    w2, h2 = fr.size
    sh = Image.new("RGBA", (w2+120, h2+120), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((60, 72, w2+60, h2+72), fill=(60, 45, 30, 115))
    sh = sh.filter(ImageFilter.GaussianBlur(20)); bg.paste(sh, (x-60, y-60), sh); bg.paste(fr, (x, y))
def spaced(d, xy, text, font, fill, sp):
    x, y = xy; tw = sum(d.textlength(c, font=font) for c in text) + sp*(len(text)-1); x -= tw/2
    for c in text:
        d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + sp
def header(bg, W, y, size):
    d = ImageDraw.Draw(bg)
    f1 = ImageFont.truetype(f"{F}/fraunces-latin-400-normal.ttf", size)
    d.text((W//2, y), TITLE, font=f1, fill=NAVY, anchor="mm")
    d.line((W//2-70, y+int(size*0.78), W//2+70, y+int(size*0.78)), fill=CORAL, width=5)
    f2 = ImageFont.truetype(f"{F}/instrument-sans-latin-500-normal.ttf", int(size*0.27))
    spaced(d, (W//2, y+int(size*1.02)), SUB, f2, NAVY, int(size*0.045))
os.makedirs(out, exist_ok=True); d0 = f"{out}/{NAME}"; os.makedirs(d0, exist_ok=True); paths = []
for i, title in enumerate(ITEMS, 1):
    im = Image.open(f"{hi}/{i}.jpg").convert("RGB"); assert im.size == (3072, 4096), im.size
    p = f"{d0}/{title}.jpg"; im.save(p, quality=95, dpi=(300, 300), subsampling=0); paths.append(p); print(title, im.size)
open(f"{d0}/READ_ME.txt", "w").write(README)
with zipfile.ZipFile(f"{out}/{NAME}.zip", "w", zipfile.ZIP_STORED) as z:
    for f in sorted(glob.glob(d0 + "/*")): z.write(f, os.path.basename(f))
# cover 1: all six framed, 2 rows of 3, with title
W, H = 2400, 2400; bg = Image.new("RGB", (W, H), WALL); header(bg, W, 190, 118)
fw = 560; fh = int(fw*4/3); gx = (W-3*fw)//4; top = 430; gy = (H-top-2*fh)//2
for i, p in enumerate(paths):
    place(bg, framed(p, fw), gx + (i % 3)*(fw+gx), top + (i//3)*(fh+gy))
bg.save(f"{out}/cover_1_set.jpg", quality=90)
# cover 2: three large frames
W, H = 2400, 1800; bg = Image.new("RGB", (W, H), WALL); header(bg, W, 170, 104)
fw = 690; fh = int(fw*4/3); gx = (W-3*fw)//4
for k, i in enumerate([4, 0, 1]):
    place(bg, framed(paths[i], fw), gx + k*(fw+gx), 400)
ImageDraw.Draw(bg).rectangle((0, H-70, W, H), fill=(205, 196, 183))
bg.save(f"{out}/cover_2_trio.jpg", quality=90)
print(os.path.getsize(f"{out}/{NAME}.zip")/1e6, "MB")
