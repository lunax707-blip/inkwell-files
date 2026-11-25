# Geometric pattern coloring book: 20 vector patterns drawn with code
import sys, math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
out = sys.argv[1]
GF = "/usr/share/fonts/truetype/google-fonts"
pdfmetrics.registerFont(TTFont("Mont", GF + "/Poppins-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Body", GF + "/Poppins-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lora", GF + "/Lora-Italic-Variable.ttf"))
PW, PH = 8.5*inch, 11*inch
AW, AH = 7.5*inch, 10*inch
X0, Y0 = (PW-AW)/2, (PH-AH)/2
CX, CY = PW/2, PH/2
S3 = math.sqrt(3)

def poly(c, pts, fill=0, stroke=1):
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, stroke=stroke, fill=fill)
def ngon(cx, cy, r, n, rot=0):
    return [(cx + r*math.cos(math.radians(rot + 360*i/n)), cy + r*math.sin(math.radians(rot + 360*i/n))) for i in range(n)]
def starpoly(cx, cy, R, r, n, rot=0):
    pts = []
    for i in range(2*n):
        a = math.radians(rot + 180*i/n); rr = R if i % 2 == 0 else r
        pts.append((cx + rr*math.cos(a), cy + rr*math.sin(a)))
    return pts
def sq_grid(s):
    nx, ny = int(AW/s/2) + 2, int(AH/s/2) + 2
    return [(CX + i*s, CY + j*s) for i in range(-nx, nx+1) for j in range(-ny, ny+1)]
def tri_grid(s):
    pts = []; ny = int(AH/(s*S3/2)/2) + 2; nx = int(AW/s/2) + 2
    for j in range(-ny, ny+1):
        for i in range(-nx, nx+1):
            pts.append((CX + i*s + (s/2 if j % 2 else 0), CY + j*s*S3/2))
    return pts

def p_star_cross(c, s=92):
    for x, y in sq_grid(s):
        poly(c, ngon(x, y, s/2, 4, 0)); poly(c, ngon(x, y, s/2, 4, 45))
def p_star_cross_dots(c, s=118):
    for x, y in sq_grid(s):
        poly(c, ngon(x, y, s/2, 4, 0)); poly(c, ngon(x, y, s/2, 4, 45)); c.circle(x, y, s*0.13)
        poly(c, ngon(x + s/2, y + s/2, s*0.146, 4, 0))
def p_hexagram(c, s=118):
    for x, y in tri_grid(s):
        R = s/S3
        poly(c, ngon(x, y, R, 6, 30)); poly(c, ngon(x, y, R, 3, 90)); poly(c, ngon(x, y, R, 3, 270)); c.circle(x, y, R*0.2)
def p_oct_square(c, s=84):
    a = s/(1 + math.sqrt(2)); r = a/(2*math.sin(math.pi/8))
    for x, y in sq_grid(s):
        poly(c, ngon(x, y, r, 8, 22.5)); poly(c, ngon(x, y, r*0.52, 8, 22.5))
def p_flower(c, r=62):
    for x, y in tri_grid(r):
        c.circle(x, y, r)
def p_quatrefoil(c, d=72):
    for x, y in sq_grid(d):
        c.circle(x, y, d/math.sqrt(2))
def p_honeycomb(c, s=62):
    for x, y in tri_grid(s*S3):
        h = ngon(x, y, s, 6, 30); poly(c, h); poly(c, ngon(x, y, s*0.5, 6, 30))
        for (a, b), (e, f) in zip(h, ngon(x, y, s*0.5, 6, 30)): c.line(a, b, e, f)
def p_triangles(c, s=96):
    hgt = s*S3/2; ny = int(AH/hgt/2) + 2; nx = int(AW/s) + 2
    for j in range(-ny, ny+1):
        for i in range(-nx, nx+1):
            x = CX + i*s/2; y = CY + j*hgt; up = (i + j) % 2 == 0
            cy = y + (hgt/3 if up else 2*hgt/3)
            rot = 90 if up else 270
            poly(c, ngon(x, cy, s/S3, 3, rot)); poly(c, ngon(x, cy, s/S3*0.45, 3, rot + 180))
def p_nested_sq(c, s=120):
    for x, y in sq_grid(s):
        r = s/math.sqrt(2)
        for k in range(4):
            poly(c, ngon(x, y, r, 4, 45 + 45*k)); r /= math.sqrt(2)
def p_rosette(c, n=8, rings=((86, 86), (172, 86))):
    c.circle(CX, CY, 20)
    for dist, r in rings:
        for i in range(n if dist < 150 else n*2):
            a = 2*math.pi*i/(n if dist < 150 else n*2)
            c.circle(CX + dist*math.cos(a), CY + dist*math.sin(a), r)
    c.circle(CX, CY, 258)
def p_rosette12(c):
    for i in range(12):
        a = 2*math.pi*i/12; c.circle(CX + 130*math.cos(a), CY + 130*math.sin(a), 130)
    c.circle(CX, CY, 260)
    for i in range(12):
        a = 2*math.pi*(i+0.5)/12; c.circle(CX + 65*math.cos(a), CY + 65*math.sin(a), 65)
def p_starburst(c):
    for R, r, n, rot in ((255, 160, 16, 0), (190, 105, 16, 11.25), (125, 58, 8, 0), (66, 28, 8, 22.5)):
        c.setFillColor(white); poly(c, starpoly(CX, CY, R, r, n, rot), fill=1)
    c.circle(CX, CY, 258); c.setFillColor(white); c.circle(CX, CY, 16, stroke=1, fill=1)
    for cx, cy in ((X0+70, Y0+70), (X0+AW-70, Y0+70), (X0+70, Y0+AH-70), (X0+AW-70, Y0+AH-70)):
        poly(c, starpoly(cx, cy, 58, 26, 8, 0)); c.circle(cx, cy, 10)
def p_star12(c):
    for k, R in ((5, 256), (4, 205), (3, 152)):
        pts = ngon(CX, CY, R, 12, 15)
        for i in range(12):
            c.line(*pts[i], *pts[(i + k) % 12])
        c.circle(CX, CY, R)
    c.circle(CX, CY, 60); poly(c, ngon(CX, CY, 60, 6, 0))
def p_chevron(c, w=75, h=52):
    ny = int(AH/h/2) + 3; nx = int(AW/w/2) + 2
    for j in range(-ny, ny+1):
        p = c.beginPath(); first = True
        for i in range(-nx*2, nx*2+1):
            x = CX + i*w/2; y = CY + j*h + (h*0.9 if i % 2 else 0)
            p.moveTo(x, y) if first else p.lineTo(x, y); first = False
        c.drawPath(p)
    for i in range(-nx*2, nx*2+1):
        if i % 2 == 0: c.line(CX + i*w/2, Y0-200, CX + i*w/2, Y0+AH+200)
def p_scallop(c, r=52):
    ny = int(AH/(r)/1) + 3; nx = int(AW/(2*r)/2) + 2
    for j in range(ny, -ny-1, -1):
        for i in range(-nx, nx+1):
            x = CX + i*2*r + (r if j % 2 else 0); y = CY + j*r
            c.setFillColor(white); c.circle(x, y, r, stroke=1, fill=1); c.circle(x, y, r*0.62, stroke=1, fill=0); c.circle(x, y, r*0.28, stroke=1, fill=0)
def p_diamonds(c, w=92, h=140):
    for j in range(-12, 13):
        for i in range(-8, 9):
            x = CX + i*w + (w/2 if j % 2 else 0); y = CY + j*h/2
            for k in (1, 0.6, 0.25):
                poly(c, [(x, y + h/2*k), (x + w/2*k, y), (x, y - h/2*k), (x - w/2*k, y)])
def p_basket(c, s=45):
    n = 14
    for j in range(-n, n+1):
        for i in range(-n, n+1):
            x = CX + i*2*s; y = CY + j*2*s
            if (i + j) % 2 == 0:
                for k in range(3): c.rect(x - s, y - s + k*2*s/3, 2*s, 2*s/3)
            else:
                for k in range(3): c.rect(x - s + k*2*s/3, y - s, 2*s/3, 2*s)
def p_trihex(c, s=58):
    for x, y in tri_grid(2*s):
        poly(c, ngon(x, y, s, 6, 0)); poly(c, starpoly(x, y, s*0.72, s*0.36, 6, 0))
def p_pinwheel(c, s=96):
    for x, y in sq_grid(s):
        h = s/2
        poly(c, [(x-h, y-h), (x+h, y-h), (x+h, y+h), (x-h, y+h)])
        for k in range(4):
            a = math.radians(90*k); b = math.radians(90*k + 90)
            poly(c, [(x, y), (x + h*math.cos(a), y + h*math.sin(a)), (x + h*(math.cos(a)+math.cos(b)), y + h*(math.sin(a)+math.sin(b)))])
        c.setFillColor(white); c.circle(x, y, s*0.14, stroke=1, fill=1)
def p_mandala(c):
    def petal(a, r1, r2, wdt):
        p = c.beginPath()
        bx, by = CX + r1*math.cos(a), CY + r1*math.sin(a); tx, ty = CX + r2*math.cos(a), CY + r2*math.sin(a)
        mx, my = (bx+tx)/2, (by+ty)/2; nx, ny = -math.sin(a)*wdt, math.cos(a)*wdt
        p.moveTo(bx, by); p.curveTo(mx+nx, my+ny, mx+nx, my+ny, tx, ty); p.curveTo(mx-nx, my-ny, mx-nx, my-ny, bx, by)
        c.setFillColor(white); c.drawPath(p, stroke=1, fill=1)
    c.circle(CX, CY, 258)
    for r1, r2, n, wd, off in ((166, 252, 24, 27, 0), (99, 193, 16, 41, 0.5), (40, 126, 12, 34, 0), (0, 63, 8, 23, 0.5)):
        for i in range(n): petal(2*math.pi*(i+off)/n, r1, r2, wd)
    c.setFillColor(white); c.circle(CX, CY, 18, stroke=1, fill=1)
def p_interlace(c, s=110):
    for x, y in sq_grid(s):
        c.circle(x, y, s*0.5); c.circle(x, y, s*0.36)
        poly(c, ngon(x + s/2, y + s/2, s*0.21, 4, 0))

PATTERNS = [p_star_cross, p_flower, p_oct_square, lambda c: p_rosette(c), p_hexagram, p_nested_sq, p_mandala, p_honeycomb,
            p_quatrefoil, p_starburst, p_triangles, p_diamonds, p_rosette12, p_star_cross_dots, p_scallop, p_star12,
            p_trihex, p_pinwheel, p_chevron, p_interlace]

def clip_frame(c):
    p = c.beginPath(); p.roundRect(X0, Y0, AW, AH, 14); c.clipPath(p, stroke=0, fill=0)
def page(c, fn, lw=1.7):
    c.saveState(); clip_frame(c); c.setLineWidth(lw); c.setStrokeColor(black); c.setLineJoin(1); fn(c); c.restoreState()
    c.setLineWidth(2.4); c.setStrokeColor(black); c.roundRect(X0, Y0, AW, AH, 14); c.showPage()

def cover(c):
    pal = [HexColor(h) for h in ("#1F6F78", "#E8A33D", "#D9583B", "#F4E9D8", "#2B3A67")]
    c.setFillColor(HexColor("#F4E9D8")); c.rect(0, 0, PW, PH, stroke=0, fill=1)
    s = 102; c.setStrokeColor(HexColor("#2B3A67")); c.setLineWidth(2.2)
    nx, ny = 5, 7
    for i in range(-nx, nx+1):
        for j in range(-ny, ny+1):
            x, y = PW/2 + i*s, PH/2 + j*s
            c.setFillColor(pal[(i + j) % 2]); poly(c, ngon(x, y, s/2, 4, 0), fill=1)
            c.setFillColor(pal[2 if (i + j) % 2 else 0]); poly(c, ngon(x, y, s/2, 4, 45), fill=1)
            c.setFillColor(pal[1 if (i * j) % 2 == 0 else 3]); poly(c, ngon(x, y, s*0.293, 8, 22.5), fill=1)
            c.setFillColor(pal[4]); c.circle(x, y, s*0.09, stroke=0, fill=1)
    bw, bh = 5.9*inch, 3.5*inch; bx, by = (PW-bw)/2, (PH-bh)/2
    c.setFillColor(HexColor("#F4E9D8")); c.setStrokeColor(HexColor("#2B3A67")); c.setLineWidth(3)
    c.roundRect(bx, by, bw, bh, 10, stroke=1, fill=1); c.setLineWidth(1.2); c.roundRect(bx+9, by+9, bw-18, bh-18, 6, stroke=1, fill=0)
    c.setFillColor(HexColor("#2B3A67"))
    c.setFont("Mont", 40); c.drawCentredString(PW/2, PH/2 + 46, "GEOMETRIC"); c.drawCentredString(PW/2, PH/2 - 4, "PATTERNS")
    c.setFillColor(HexColor("#D9583B")); c.setFont("Lora", 23); c.drawCentredString(PW/2, PH/2 - 52, "A calming coloring book")
    c.setFillColor(HexColor("#2B3A67")); c.setFont("Mont", 11.5); c.drawCentredString(PW/2, PH/2 - 92, "20 DESIGNS FOR TEENS AND ADULTS")
    c.showPage()

c = canvas.Canvas(out, pagesize=(PW, PH)); c.setTitle("Geometric Patterns: A Calming Coloring Book")
cover(c)
c.setFillColor(black); c.setFont("Body", 11); yy = PH*0.55
for l in ["Print the pages you want, as many times as you like, for your own use.",
          "Fine tip pens and pencils work best. Use thicker paper for markers.", "",
          "Copyright 2026. All rights reserved.", "Please do not resell or share the file."]:
    c.drawCentredString(PW/2, yy, l); yy -= 20
c.showPage()
for fn in PATTERNS: page(c, fn)
c.save(); print("geo pages", 2 + len(PATTERNS))
