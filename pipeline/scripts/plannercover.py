# Listing cover for planner products: Magnific flat lay background + real page renders.
# Usage: python3 plannercover.py bg.png pages_dir out.jpg
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
bg, pg, out = sys.argv[1:4]
F = "/home/claude/fonts/ttf/"
NAVY, CORAL, TEAL = (43, 58, 103), (217, 88, 59), (31, 111, 120)
W, H = 2688, 1520
b = Image.open(bg).convert("RGB"); s = 1.26
b = b.resize((int(W * s), int(H * s)), Image.LANCZOS)
cv = b.crop((0, (b.height - H) // 2, W, (b.height - H) // 2 + H))
def card(n, w, rot=0):
    im = Image.open(f"{pg}/p-{n:02d}.png").convert("RGB")
    im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS).convert("RGBA")
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    return im
def place(c, x, y):
    global cv
    sh = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    a = c.split()[3].point(lambda v: int(v * 0.40))
    sh.paste((60, 45, 30, 255), (x + 8, y + 22), a)
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    cv = Image.alpha_composite(cv.convert("RGBA"), sh)
    cv.alpha_composite(c, (x, y)); cv = cv.convert("RGB")
place(card(5, 560, 6), 1070, 150)
place(card(21, 560, -3), 1550, 110)
place(card(14, 540, 3), 1170, 700)
place(card(1, 600, -2), 1470, 560)
d = ImageDraw.Draw(cv)
def f(name, sz): return ImageFont.truetype(F + name, sz)
x, y = 140, 330
lab = "FOR FREELANCERS"; fl = f("instrument-sans-latin-600-normal.ttf", 34)
w = d.textlength(lab, font=fl)
d.rounded_rectangle((x, y, x + w + 56, y + 62), radius=31, fill=CORAL); d.text((x + 28, y + 31), lab, font=fl, fill=(255, 255, 255), anchor="lm")
ft = f("fraunces-latin-400-normal.ttf", 124)
d.text((x - 6, y + 96), "The Freelancer", font=ft, fill=NAVY)
d.text((x - 6, y + 232), "Planner", font=f("fraunces-latin-300-italic.ttf", 124), fill=CORAL)
fs = f("fraunces-latin-300-italic.ttf", 50)
d.text((x, y + 410), "A 90 day system for clients,", font=fs, fill=TEAL); d.text((x, y + 472), "projects, money and time", font=fs, fill=TEAL)
fb = f("instrument-sans-latin-500-normal.ttf", 32)
d.text((x, y + 580), "52 page printable PDF   |   US Letter and A4", font=fb, fill=NAVY)
d.text((x, y + 628), "Undated   |   Monday and Sunday start", font=fb, fill=NAVY)
cv.save(out, quality=92)
cv.resize((1280, 724), Image.LANCZOS).save(out.replace(".jpg", "_small.jpg"), quality=88)
print(cv.size)
