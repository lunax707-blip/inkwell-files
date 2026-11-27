# Coded listing covers for The Focus Planner (no Magnific background: used when image generation is unavailable).
# Usage: python3 focuscover.py pages_dir out_dir   (pages rendered with pdftoppm -r 110 as p-01.png ...)
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
d.ellipse((2180, 980, 2880, 1680), fill=SAGE)
d.ellipse((1040, 1180, 1400, 1540), fill=MUST)
d.rectangle((0, 0, W, 26), fill=NAVY)
cv = place(cv, card(21, 520, 7), 1210, 250)
cv = place(cv, card(12, 540, -5), 2060, 150)
cv = place(cv, card(20, 540, 4), 2010, 720)
cv = place(cv, card(17, 640, -2), 1500, 330)
d = ImageDraw.Draw(cv)
x, y = 140, 300
fl = f("instrument-sans-latin-600-normal.ttf", 34)
pw = pill(d, x, y, "FOR FREELANCERS", CORAL, fl)
pill(d, x + pw + 18, y, "ADHD FRIENDLY", TEAL, fl)
d.text((x - 6, y + 96), "The Focus", font=f("fraunces-latin-400-normal.ttf", 150), fill=NAVY)
d.text((x - 6, y + 258), "Planner", font=f("fraunces-latin-300-italic.ttf", 150), fill=CORAL)
fs = f("fraunces-latin-300-italic.ttf", 56)
d.text((x, y + 470), "Big type. Few boxes.", font=fs, fill=TEAL); d.text((x, y + 540), "One page at a time.", font=fs, fill=TEAL)
fb = f("instrument-sans-latin-500-normal.ttf", 33)
d.text((x, y + 668), "48 page printable PDF   |   US Letter and A4", font=fb, fill=NAVY)
d.text((x, y + 718), "Undated   |   Monday and Sunday start", font=fb, fill=NAVY)
d.text((x, H - 110), "INKWELL AND CO", font=f("instrument-sans-latin-600-normal.ttf", 26), fill=INK)
cv.save(f"{out}/focus-planner_cover1.jpg", quality=92)

# cover 2: what is inside, 12 pages ----------------------------------------
cv = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(cv)
d.text((120, 96), "What is inside", font=f("fraunces-latin-400-normal.ttf", 96), fill=CREAM)
tw = d.textlength("What is inside", font=f("fraunces-latin-400-normal.ttf", 96))
d.text((120 + tw + 40, 134), "48 pages, each with one job", font=f("fraunces-latin-300-italic.ttf", 54), fill=MUST)
picks = [(17, "Today, simple"), (9, "Brain dump"), (12, "Week on a page"), (19, "Focus sprints"), (20, "Getting unstuck"), (21, "Low energy day"),
         (22, "All too much"), (27, "Working backwards"), (29, "Hard messages"), (36, "Money check"), (40, "Habit tracker"), (46, "Routine cards")]
cols = 6; gx = 44; cw = (W - 240 - gx * (cols - 1)) // cols; ch = int(cw * 11 / 8.5)
fl = f("instrument-sans-latin-500-normal.ttf", 28)
for i, (n, lab) in enumerate(picks):
    x = 120 + (i % cols) * (cw + gx); y = 290 + (i // cols) * (ch + 96)
    cv = place(cv, card(n, cw), x, y, blur=14, dy=12, op=0.5)
    d = ImageDraw.Draw(cv); d.text((x + cw / 2, y + ch + 34), lab, font=fl, fill=CREAM, anchor="mm")
cv.save(f"{out}/focus-planner_cover2.jpg", quality=92)
print("ok")
