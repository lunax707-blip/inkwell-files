# KDP paperback wrap cover (back + spine + front) at 300 dpi, plus a front-only image
import sys
from PIL import Image, ImageDraw, ImageFont
art_path, clean, fonts, out, npages = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
D = 300
def px(i): return int(round(i*D))
spine = npages * 0.002252
Wi, Hi = 0.125 + 8.5 + spine + 8.5 + 0.125, 11.25
art = Image.open(art_path).convert("RGB")
print("art", art.size, "spine in", round(spine, 4), "wrap in", round(Wi, 4), Hi)
# background yellow sampled from the empty top band of the art
band = art.crop((0, 0, art.width, art.height//12)).resize((1, 1), Image.BOX)
bg = band.getpixel((0, 0)); print("bg", bg)
cv = Image.new("RGB", (px(Wi), px(Hi)), bg)
# front: art scaled to 8.625 x 11.5 in, top 0.25 in cropped away
fw, fh = px(8.625), px(11.5)
a = art.resize((fw, fh), Image.LANCZOS).crop((0, px(0.25), fw, fh))
fx = px(0.125 + 8.5 + spine)
cv.paste(a, (fx, 0))
d = ImageDraw.Draw(cv)
NAVY, RED, WHITE = (23, 37, 90), (226, 48, 44), (255, 255, 255)
def font(w, size): return ImageFont.truetype(f"{fonts}/Fredoka-{w}.ttf", size)
def fit(text, w, maxw, start):
    s = start
    while d.textlength(text, font=font(w, s)) > maxw: s -= 4
    return font(w, s)
cx = fx + px(8.5)//2          # centre of front trim area
top = px(0.125)
f1 = fit("THINGS THAT GO", 700, px(7.3), 330)
d.text((cx, top + px(1.25)), "THINGS THAT GO", font=f1, fill=NAVY, anchor="mm", stroke_width=10, stroke_fill=WHITE)
f2 = font(700, 150)
d.text((cx, top + px(2.2)), "and Places to See", font=f2, fill=RED, anchor="mm", stroke_width=8, stroke_fill=WHITE)
f3 = font(600, 78)
label = "COLORING BOOK FOR KIDS AGES 4 TO 8"
tw = d.textlength(label, font=f3)
pw, ph = tw + px(0.7), px(0.56)
py = top + px(3.02)
d.rounded_rectangle((cx - pw/2, py - ph/2, cx + pw/2, py + ph/2), radius=ph/2, fill=NAVY)
d.text((cx, py - 4), label, font=f3, fill=WHITE, anchor="mm")
# back cover
bx0 = px(0.125); bcx = bx0 + px(8.5)//2
d.text((bcx, top + px(1.15)), "30 big, bold pictures to color", font=fit("30 big, bold pictures to color", 700, px(7.0), 170), fill=NAVY, anchor="mm")
lines = ["Trucks, trains, rockets, boats, castles and more",
         "Thick lines and simple shapes for small hands",
         "One picture per sheet, so markers stay off the next page"]
f4 = font(600, 62)
y = top + px(1.85)
for l in lines:
    d.text((bcx, y), l, font=f4, fill=NAVY, anchor="mm"); y += px(0.36)
# four sample pages as tilted white cards
picks = ["p01", "p05", "p16", "p22"]
cw = px(2.5); chh = int(cw*4/3)
pos = [(bx0 + px(1.45), top + px(3.05), -4), (bx0 + px(4.6), top + px(2.95), 3),
       (bx0 + px(0.6), top + px(6.6), 3), (bx0 + px(3.45), top + px(6.75), -3)]
for p, (x, yy, ang) in zip(picks, pos):
    im = Image.open(f"{clean}/{p}.png").convert("RGB").resize((cw - 60, chh - 60), Image.LANCZOS)
    card = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, cw-1, chh-1), radius=36, fill=WHITE, outline=NAVY, width=10)
    card.paste(im, (30, 30))
    cd.rounded_rectangle((0, 0, cw-1, chh-1), radius=36, outline=NAVY, width=10)
    card = card.rotate(ang, expand=True, resample=Image.BICUBIC)
    cv.paste(card, (x, yy), card)
cv.save(f"{out}/KDP_cover_wrap.pdf", "PDF", resolution=D)
cv.save(f"{out}/cover_wrap_preview.jpg", quality=88)
front = cv.crop((fx, px(0.125), fx + px(8.5), px(0.125) + px(11)))
front.save(f"{out}/front_cover.jpg", quality=92, dpi=(D, D))
print("wrap px", cv.size, "front px", front.size)
