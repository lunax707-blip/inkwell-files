# Coded listing covers for Numbers 1 to 20 Worksheets (no Magnific background).
# Usage: python3 numberscover.py pages_dir out_dir   (pages rendered with pdftoppm -r 110 as p-01.png ...)
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
pg, out = sys.argv[1:3]
F = "/home/claude/fonts/ttf/"
NAVY, CORAL, TEAL, MUST, SAGE, CREAM, INK = (43, 58, 103), (217, 88, 59), (31, 111, 120), (232, 163, 61), (157, 181, 160), (244, 233, 216), (32, 41, 74)
W, H = 2688, 1520
def f(name, sz): return ImageFont.truetype(F + name, sz)
def card(n, w, rot=0):
    im = Image.open(f"{pg}/p-{n:02d}.png").convert("RGB")
    im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS).convert("RGBA")
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    return im
def place(cv, c, x, y, blur=24, dy=24, op=0.34):
    sh = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    a = c.split()[3].point(lambda v: int(v * op))
    sh.paste((70, 52, 36, 255), (x + 8, y + dy), a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    cv = Image.alpha_composite(cv.convert("RGBA"), sh)
    cv.alpha_composite(c, (x, y)); return cv.convert("RGB")
def pill(d, x, y, lab, fill, fl):
    w = d.textlength(lab, font=fl)
    d.rounded_rectangle((x, y, x + w + 56, y + 62), radius=31, fill=fill); d.text((x + 28, y + 31), lab, font=fl, fill=(255, 255, 255), anchor="lm")
    return w + 56

# cover 1: title left, four pages right ------------------------------------
cv = Image.new("RGB", (W, H), (246, 239, 228))
d = ImageDraw.Draw(cv)
d.ellipse((1250, -260, 2950, 1440), fill=(238, 226, 207))
d.ellipse((2200, 1000, 2900, 1700), fill=TEAL)
d.ellipse((1040, 1200, 1400, 1560), fill=MUST)
d.rectangle((0, 0, W, 26), fill=CORAL)
cv = place(cv, card(54, 520, 7), 1200, 250)
cv = place(cv, card(33, 540, -5), 2060, 140)
cv = place(cv, card(38, 540, 4), 2010, 720)
cv = place(cv, card(11, 640, -2), 1500, 330)
d = ImageDraw.Draw(cv)
x, y = 140, 250
fl = f("instrument-sans-latin-600-normal.ttf", 34)
pw = pill(d, x, y, "AGES 3 TO 6", CORAL, fl)
pill(d, x + pw + 18, y, "PRESCHOOL AND KINDERGARTEN", TEAL, fl)
d.text((x - 6, y + 96), "Numbers", font=f("fraunces-latin-400-normal.ttf", 168), fill=NAVY)
d.text((x - 6, y + 280), "1 to 20", font=f("fraunces-latin-300-italic.ttf", 168), fill=CORAL)
fs = f("fraunces-latin-300-italic.ttf", 58)
d.text((x, y + 520), "Trace, count and write.", font=fs, fill=TEAL); d.text((x, y + 594), "One number at a time.", font=fs, fill=TEAL)
fb = f("instrument-sans-latin-500-normal.ttf", 33)
d.text((x, y + 730), "63 page printable PDF   |   US Letter and A4", font=fb, fill=NAVY)
d.text((x, y + 780), "Ten frames, puzzles, answer key and certificate", font=fb, fill=NAVY)
d.text((x, H - 110), "INKWELL AND CO", font=f("instrument-sans-latin-600-normal.ttf", 26), fill=INK)
cv.save(f"{out}/numbers-1-to-20_cover1.jpg", quality=92)

# cover 2: what is inside, 12 pages ----------------------------------------
cv = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(cv)
d.text((120, 96), "What is inside", font=f("fraunces-latin-400-normal.ttf", 96), fill=CREAM)
tw = d.textlength("What is inside", font=f("fraunces-latin-400-normal.ttf", 96))
d.text((120 + tw + 40, 134), "63 pages, from 1 all the way to 20", font=f("fraunces-latin-300-italic.ttf", 54), fill=MUST)
picks = [(3, "Number charts"), (8, "A page per number"), (15, "Count and write"), (18, "Ten frames"), (23, "More or fewer"), (32, "Teen numbers"),
         (44, "Ten and some more"), (45, "Missing numbers"), (51, "Dot to dot"), (52, "Number path"), (53, "Color by number"), (60, "Certificate")]
cols = 6; gx = 44; cw = (W - 240 - gx * (cols - 1)) // cols; ch = int(cw * 11 / 8.5)
fl = f("instrument-sans-latin-500-normal.ttf", 28)
for i, (n, lab) in enumerate(picks):
    x = 120 + (i % cols) * (cw + gx); y = 290 + (i // cols) * (ch + 96)
    cv = place(cv, card(n, cw), x, y, blur=14, dy=12, op=0.5)
    d = ImageDraw.Draw(cv); d.text((x + cw / 2, y + ch + 34), lab, font=fl, fill=CREAM, anchor="mm")
cv.save(f"{out}/numbers-1-to-20_cover2.jpg", quality=92)
print("ok")
