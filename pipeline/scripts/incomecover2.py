# Second listing image for the Irregular Income Budget: "What is inside" grid of real tab renders.
# Usage: python3 incomecover2.py tabs_dir out.jpg
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
tabs, out = sys.argv[1:3]
F = "/home/claude/fonts/ttf/"
NAVY, CORAL, TEAL, CREAM, SOFT = (43, 58, 103), (217, 88, 59), (31, 111, 120), (244, 233, 216), (106, 111, 130)
W, H = 2688, 1520
cv = Image.new("RGB", (W, H), (246, 240, 229))
def f(name, s): return ImageFont.truetype(F + name, s)
def tile(path, x, y, w, h, label, note):
    global cv
    im = Image.open(path).convert("RGB")
    sc = w / im.width; im = im.resize((w, int(im.height * sc)), Image.LANCZOS)
    bg = Image.new("RGB", (w, h), (255, 255, 255)); bg.paste(im.crop((0, 0, w, min(h, im.height))), (0, max(0, (h - im.height) // 2))); im = bg
    c = Image.new("RGBA", (w + 28, h + 28), (255, 255, 255, 255)); c.paste(im, (14, 14))
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=16, fill=255); c.putalpha(m)
    sh = Image.new("RGBA", cv.size, (0, 0, 0, 0)); sh.paste((40, 30, 20, 255), (x + 6, y + 18), m.point(lambda v: int(v * 0.30))); sh = sh.filter(ImageFilter.GaussianBlur(20))
    cv = Image.alpha_composite(cv.convert("RGBA"), sh); cv.alpha_composite(c, (x, y)); cv = cv.convert("RGB")
    d = ImageDraw.Draw(cv)
    d.text((x + 6, y + h + 58), label, font=f("fraunces-latin-400-normal.ttf", 44), fill=NAVY)
    d.text((x + 6, y + h + 118), note, font=f("instrument-sans-latin-400-normal.ttf", 29), fill=SOFT)
d = ImageDraw.Draw(cv)
fl = f("instrument-sans-latin-600-normal.ttf", 30)
d.text((120, 96), "IRREGULAR INCOME BUDGET FOR FREELANCERS", font=fl, fill=CORAL)
d.text((116, 140), "What is inside", font=f("fraunces-latin-400-normal.ttf", 92), fill=NAVY)
d.text((W - 120, 196), "One .xlsx file with a sample year, plus a blank copy", font=f("fraunces-latin-300-italic.ttf", 44), fill=TEAL, anchor="rs")
tw, th, gx = 780, 470, 54
x0 = (W - 3 * tw - 2 * gx - 28) // 2
tile(f"{tabs}/dash.png", x0, 300, tw, th, "Dashboard", "Your year, your buffer, the pay you can afford")
tile(f"{tabs}/payplan.png", x0 + tw + gx, 300, tw, th, "Pay Plan", "Uneven income in, steady pay out, month by month")
tile(f"{tabs}/budget.png", x0 + 2 * (tw + gx), 300, tw, th, "Budget", "Business and personal categories, budget against spent")
y2 = 300 + th + 190
tile(f"{tabs}/income.png", x0, y2, tw, 330, "Income log", "Every payment, by the date it landed")
tile(f"{tabs}/expenses.png", x0 + tw + gx, y2, tw, 330, "Expense log", "Pick a category, the rest sorts itself")
tile(f"{tabs}/start.png", x0 + 2 * (tw + gx), y2, tw, 330, "Start Here and Settings", "Ten minute setup, written in plain language")
cv.save(out, quality=92)
cv.resize((1280, 724), Image.LANCZOS).save(out.replace(".jpg", "_small.jpg"), quality=88)
print(cv.size)
