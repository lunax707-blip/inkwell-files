# Listing covers for Telling Time Worksheets: (1) Magnific flat lay + real page renders, (2) coded 12 page grid.
# Usage: python3 timecover.py bg.png pages_dir out_prefix
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
bg, pg, out = sys.argv[1:4]
F = "/home/claude/fonts/ttf/"
NAVY, CORAL, TEAL, CREAM, INK = (43, 58, 103), (217, 88, 59), (31, 111, 120), (247, 239, 226), (32, 41, 74)
W, H = 2688, 1520
def f(name, sz): return ImageFont.truetype(F + name, sz)
def card(n, w, rot=0):
    im = Image.open(f"{pg}/p-{n:02d}.png").convert("RGB")
    im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS).convert("RGBA")
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    return im
def place(cv, c, x, y, blur=22, op=0.38):
    sh = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    a = c.split()[3].point(lambda v: int(v * op))
    sh.paste((60, 45, 30, 255), (x + 8, y + 20), a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    cv = Image.alpha_composite(cv.convert("RGBA"), sh); cv.alpha_composite(c, (x, y)); return cv.convert("RGB")
def title(d, x, y, big=124):
    lab = "FOR KIDS AGES 5 TO 8"; fl = f("instrument-sans-latin-600-normal.ttf", 34)
    w = d.textlength(lab, font=fl)
    d.rounded_rectangle((x, y, x + w + 56, y + 62), radius=31, fill=CORAL); d.text((x + 28, y + 31), lab, font=fl, fill=(255, 255, 255), anchor="lm")
    d.text((x - 6, y + 96), "Telling Time", font=f("fraunces-latin-400-normal.ttf", big), fill=NAVY)
    d.text((x - 6, y + 96 + int(big * 1.1)), "Worksheets", font=f("fraunces-latin-300-italic.ttf", big), fill=CORAL)
    fs = f("fraunces-latin-300-italic.ttf", 50); yy = y + 96 + int(big * 2.2) + 46
    d.text((x, yy), "From o'clock to the minute,", font=fs, fill=TEAL); d.text((x, yy + 62), "one small step at a time", font=fs, fill=TEAL)
    fb = f("instrument-sans-latin-500-normal.ttf", 32)
    d.text((x, yy + 170), "61 page printable PDF   |   US Letter and A4", font=fb, fill=NAVY)
    d.text((x, yy + 218), "Answer key and cut out practice clock included", font=fb, fill=NAVY)
# cover 1
cv = Image.open(bg).convert("RGB").resize((W, H), Image.LANCZOS)
cv = place(cv, card(32, 540, 5), 1150, 120)
cv = place(cv, card(48, 540, -4), 1660, 90)
cv = place(cv, card(7, 520, 3), 1290, 720)
cv = place(cv, card(1, 590, -2), 1640, 560)
title(ImageDraw.Draw(cv), 140, 300)
cv.save(out + "_cover.jpg", quality=92); cv.resize((1280, 724), Image.LANCZOS).save(out + "_cover_small.jpg", quality=88)
# cover 2: what is inside grid
g = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(g)
d.text((120, 96), "What's inside", font=f("fraunces-latin-400-normal.ttf", 92), fill=NAVY)
d.text((120, 214), "61 pages in 8 parts, each one building on the last", font=f("fraunces-latin-300-italic.ttf", 44), fill=TEAL)
picks = [3, 6, 7, 9, 14, 16, 23, 28, 31, 37, 42, 48, 49, 52, 53, 56]
cw = 292; gap = 30; x0 = (W - 8 * cw - 7 * gap) // 2; y0 = 350
for i, n in enumerate(picks):
    c = card(n, cw); x = x0 + (i % 8) * (cw + gap); y = y0 + (i // 8) * (c.height + 64)
    g = place(g, c, x, y, blur=12, op=0.28)
d = ImageDraw.Draw(g); fb = f("instrument-sans-latin-500-normal.ttf", 34)
d.text((W // 2, H - 130), "Meet the clock   |   O'clock   |   Half past   |   Quarter hours   |   Five minutes   |   To the minute   |   Time puzzles   |   Review", font=fb, fill=INK, anchor="mm")
g.save(out + "_inside.jpg", quality=92); g.resize((1280, 724), Image.LANCZOS).save(out + "_inside_small.jpg", quality=88)
print("ok")
