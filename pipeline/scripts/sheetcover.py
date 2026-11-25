# Listing cover for spreadsheet products: Magnific flat lay background + real tab renders.
# Usage: python3 sheetcover.py bg.png tabs_dir out.jpg
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
bg, tabs, out = sys.argv[1:4]
F = "/home/claude/fonts/ttf/"
NAVY, CORAL, TEAL, CREAM = (43, 58, 103), (217, 88, 59), (31, 111, 120), (244, 233, 216)
cv = Image.open(bg).convert("RGB").resize((2688, 1520), Image.LANCZOS)
def card(path, w, bar=True, rot=0, pad=26):
    im = Image.open(path).convert("RGB")
    im = im.resize((w - 2 * pad, int((w - 2 * pad) * im.height / im.width)), Image.LANCZOS)
    top = 46 if bar else pad
    c = Image.new("RGBA", (w, im.height + top + pad), (255, 255, 255, 255))
    d = ImageDraw.Draw(c)
    if bar:
        d.rectangle((0, 0, w, 34), fill=(236, 232, 224))
        for i, col in enumerate((CORAL, (232, 163, 61), (157, 181, 160))): d.ellipse((18 + i * 26, 10, 32 + i * 26, 24), fill=col)
    c.paste(im, (pad, top))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=18, fill=255)
    c.putalpha(m)
    if rot: c = c.rotate(rot, expand=True, resample=Image.BICUBIC)
    return c
def place(c, x, y):
    global cv
    sh = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    a = c.split()[3].point(lambda v: int(v * 0.42))
    sh.paste((40, 30, 20, 255), (x + 10, y + 26), a)
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    cv = Image.alpha_composite(cv.convert("RGBA"), sh)
    cv.alpha_composite(c, (x, y)); cv = cv.convert("RGB")
place(card(f"{tabs}/invoices.png", 1300), 1340, 96)
place(card(f"{tabs}/dash.png", 1130), 1170, 262)
place(card(f"{tabs}/invoice.png", 500, bar=False, rot=-4), 2150, 880)
d = ImageDraw.Draw(cv)
def f(name, s): return ImageFont.truetype(F + name, s)
x, y = 150, 320
lab = "FOR FREELANCERS"; fl = f("instrument-sans-latin-600-normal.ttf", 34)
w = d.textlength(lab, font=fl)
d.rounded_rectangle((x, y, x + w + 56, y + 62), radius=31, fill=CORAL); d.text((x + 28, y + 31), lab, font=fl, fill=(255, 255, 255), anchor="lm")
ft = f("fraunces-latin-400-normal.ttf", 108)
d.text((x - 5, y + 92), "Freelance", font=ft, fill=NAVY); d.text((x - 5, y + 210), "Invoice Tracker", font=ft, fill=NAVY)
fs = f("fraunces-latin-300-italic.ttf", 50)
d.text((x, y + 362), "See who owes you and who to chase", font=fs, fill=TEAL)
fb = f("instrument-sans-latin-500-normal.ttf", 32)
d.text((x, y + 452), "Google Sheets and Excel   |   6 tabs   |   Printable invoice", font=fb, fill=NAVY)
cv.save(out, quality=92)
cv.resize((1280, 724), Image.LANCZOS).save(out.replace(".jpg", "_small.jpg"), quality=88)
print(cv.size)
