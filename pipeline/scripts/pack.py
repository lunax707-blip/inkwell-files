# Generic printable pack builder: coded cover + coloring pages (+ optional extra pages drawn by a hook)
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
cfg = json.load(open(sys.argv[1]))
FONTS = cfg["fonts"]; D = 300
def font(w, s): return ImageFont.truetype(f"{FONTS}/Fredoka-{w}.ttf", s)
def px(i): return int(round(i*D))
def hexc(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
BG, INK, ACC = hexc(cfg["bg"]), hexc(cfg["ink"]), hexc(cfg["accent"])
W, H = px(8.5), px(11)
cv = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(cv)
def fit(t, w, maxw, start):
    s = start
    while d.textlength(t, font=font(w, s)) > maxw: s -= 4
    return font(w, s)
y = px(1.2)
for line in cfg["title"]:
    f = fit(line, 700, px(7.3), 300)
    d.text((W//2, y), line, font=f, fill=hexc(cfg.get("title_fill", cfg["ink"])), anchor="mm", stroke_width=9, stroke_fill=hexc(cfg.get("title_stroke", "#FFFFFF")))
    y += int(f.size*1.02)
y += px(0.02)
f3 = font(600, 74); lab = cfg["label"]; tw = d.textlength(lab, font=f3)
pw, ph = tw + px(0.7), px(0.54)
d.rounded_rectangle((W/2-pw/2, y-ph/2, W/2+pw/2, y+ph/2), radius=ph/2, fill=ACC)
d.text((W//2, y-4), lab, font=f3, fill=(255, 255, 255), anchor="mm")
top = y + px(0.55)
cw = px(3.0); ch = int(cw*4/3)
avail = H - top - px(0.35)
if 2*ch*0.93 > avail:
    ch = int(avail/1.9); cw = int(ch*3/4)
pos = [(W//2 - cw - px(0.28), top, -4), (W//2 + px(0.22), top + px(0.15), 3),
       (W//2 - cw - px(0.12), top + int(ch*0.9), 3), (W//2 + px(0.3), top + int(ch*0.93), -3)]
for p, (x, yy, ang) in zip(cfg["cover_pages"], pos):
    im = Image.open(p).convert("RGB").resize((cw-60, ch-60), Image.LANCZOS)
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, cw-1, ch-1), radius=36, fill=(255, 255, 255))
    card.paste(im, (30, 30))
    cd.rounded_rectangle((0, 0, cw-1, ch-1), radius=36, outline=hexc(cfg.get("card_line", cfg["ink"])), width=10)
    card = card.rotate(ang, expand=True, resample=Image.BICUBIC)
    cv.paste(card, (x, yy), card)
cover = cfg["out"].replace(".pdf", "_cover.jpg")
cv.save(cover, quality=90, dpi=(D, D))
pdfmetrics.registerFont(TTFont("Fredoka", FONTS + "/Fredoka-700.ttf"))
pdfmetrics.registerFont(TTFont("FredokaSB", FONTS + "/Fredoka-600.ttf"))
PW, PH = 8.5*inch, 11*inch
c = canvas.Canvas(cfg["out"], pagesize=(PW, PH)); c.setTitle(cfg["doc_title"])
c.drawImage(cover, 0, 0, PW, PH); c.showPage()
c.setFont("FredokaSB", 13); yy = PH*0.55
for l in cfg["note"]:
    c.drawCentredString(PW/2, yy, l); yy -= 22
c.showPage()
for p in cfg["pages"]:
    aw, ah = 7.5*inch, 10*inch; x, y0 = (PW-aw)/2, (PH-ah)/2
    c.drawImage(p, x, y0, aw, ah); c.setLineWidth(2.2); c.roundRect(x, y0, aw, ah, 14); c.showPage()
import math
def star(c, cx, cy, R, r, n=5, rot=90):
    p = c.beginPath()
    for i in range(2*n):
        a = math.radians(rot + i*180/n); rr = R if i % 2 == 0 else r
        x, y = cx + rr*math.cos(a), cy + rr*math.sin(a)
        p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
    p.close(); c.drawPath(p, stroke=1, fill=0)
def frame(c):
    aw, ah = 7.5*inch, 10*inch; x, y0 = (PW-aw)/2, (PH-ah)/2
    c.setLineWidth(2.2); c.roundRect(x, y0, aw, ah, 14); return x, y0, aw, ah
for extra in cfg.get("extras", []):
    x, y0, aw, ah = frame(c)
    if extra == "deeds":
        c.setFont("Fredoka", 34); c.drawCentredString(PW/2, y0+ah-62, "MY 30 GOOD DEEDS")
        c.setFont("FredokaSB", 14); c.drawCentredString(PW/2, y0+ah-88, "Color one star each day you do something kind")
        cols, rows = 5, 6; gw = aw-50; gh = ah-150
        for i in range(30):
            cx = x+25 + gw/cols*(i % cols + .5); cy = y0+ah-118 - gh/rows*(i//cols + .5)
            c.setLineWidth(2.2); star(c, cx, cy+4, 40, 17)
            c.setFont("Fredoka", 15); c.drawCentredString(cx, cy-1, str(i+1))
    if extra == "goals":
        c.setFont("Fredoka", 34); c.drawCentredString(PW/2, y0+ah-62, "MY RAMADAN GOALS")
        c.setFont("FredokaSB", 14); c.drawCentredString(PW/2, y0+ah-88, "Write or draw what you want to do this month")
        for i in range(6):
            ly = y0+ah-175 - i*92
            c.setLineWidth(2.2); star(c, x+62, ly+10, 24, 10)
            c.setLineWidth(1.3); c.line(x+105, ly, x+aw-40, ly)
        c.setFont("FredokaSB", 13); c.drawCentredString(PW/2, y0+34, "Name: ______________________________")
    c.showPage()
c.save(); print(cfg["out"], 2 + len(cfg["pages"]) + len(cfg.get("extras", [])), "pages")
