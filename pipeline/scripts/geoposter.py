# Six colored geometric posters, vector PDF at 18 x 24 in
import sys, math
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
out = sys.argv[1]
PW, PH = 18*inch, 24*inch
M = 1.5*inch
AX, AY, AW, AH = M, M, PW-2*M, PH-2*M
CX, CY = PW/2, PH/2
S3 = math.sqrt(3)
TEAL, MUST, CORAL, CREAM, NAVY, SAGE = [HexColor(h) for h in ("#1F6F78", "#E8A33D", "#D9583B", "#F4E9D8", "#2B3A67", "#9DB5A0")]
def poly(c, pts, fill):
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.setFillColor(fill); c.drawPath(p, stroke=1, fill=1)
def ngon(cx, cy, r, n, rot=0):
    return [(cx + r*math.cos(math.radians(rot + 360*i/n)), cy + r*math.sin(math.radians(rot + 360*i/n))) for i in range(n)]
def starpts(cx, cy, R, r, n, rot=0):
    return [(cx + (R if i % 2 == 0 else r)*math.cos(math.radians(rot + 180*i/n)), cy + (R if i % 2 == 0 else r)*math.sin(math.radians(rot + 180*i/n))) for i in range(2*n)]
def circ(c, x, y, r, fill, stroke=1):
    c.setFillColor(fill); c.circle(x, y, r, stroke=stroke, fill=1)

def d_star_cross(c):
    c.setFillColor(CREAM); c.rect(AX, AY, AW, AH, stroke=0, fill=1); s = 216
    for i in range(-4, 5):
        for j in range(-6, 7):
            x, y = CX + i*s, CY + j*s
            poly(c, ngon(x, y, s/2, 4, 0), TEAL if (i + j) % 2 == 0 else MUST)
            poly(c, ngon(x, y, s/2, 4, 45), CORAL if (i + j) % 2 else TEAL)
            poly(c, ngon(x, y, s*0.293, 8, 22.5), MUST if (i*j) % 2 == 0 else CREAM)
            circ(c, x, y, s*0.09, NAVY, 0)
def d_oct(c):
    c.setFillColor(CORAL); c.rect(AX, AY, AW, AH, stroke=0, fill=1); s = 180
    a = s/(1 + math.sqrt(2)); r = a/(2*math.sin(math.pi/8))
    for i in range(-5, 6):
        for j in range(-7, 8):
            x, y = CX + i*s, CY + j*s
            poly(c, ngon(x, y, r, 8, 22.5), TEAL if (i + j) % 2 == 0 else NAVY)
            poly(c, starpts(x, y, r*0.72, r*0.42, 8, 22.5), CREAM if (i + j) % 2 == 0 else MUST)
            circ(c, x, y, r*0.16, CORAL, 0)
def d_hex(c):
    c.setFillColor(CREAM); c.rect(AX, AY, AW, AH, stroke=0, fill=1); s = 100; d = s*S3
    cols = (TEAL, MUST, CORAL)
    for j in range(-12, 13):
        for i in range(-7, 8):
            x = CX + i*d + (d/2 if j % 2 else 0); y = CY + j*d*S3/2
            q = i - (j - (j & 1))//2
            col = cols[(q - j) % 3]
            poly(c, ngon(x, y, s, 6, 30), col)
            poly(c, starpts(x, y, s*0.78, s*0.45, 6, 30), CREAM)
            poly(c, ngon(x, y, s*0.3, 6, 30), NAVY)
def d_scallop(c):
    c.setFillColor(NAVY); c.rect(AX, AY, AW, AH, stroke=0, fill=1); r = 108
    cols = (TEAL, MUST, CORAL, SAGE)
    for j in range(14, -15, -1):
        for i in range(-6, 7):
            x = CX + i*2*r + (r if j % 2 else 0); y = CY + j*r
            col = cols[j % 4]
            circ(c, x, y, r, col); circ(c, x, y, r*0.66, CREAM); circ(c, x, y, r*0.36, col); circ(c, x, y, r*0.12, NAVY, 0)
def d_diamond(c):
    c.setFillColor(CREAM); c.rect(AX, AY, AW, AH, stroke=0, fill=1); w, h = 190, 300
    for j in range(-12, 13):
        for i in range(-6, 7):
            x = CX + i*w + (w/2 if j % 2 else 0); y = CY + j*h/2
            sets = ((NAVY, MUST, CREAM, CORAL), (TEAL, CREAM, CORAL, NAVY))[(i + j//2) % 2]
            for k, col in zip((1, 0.72, 0.46, 0.2), sets):
                poly(c, [(x, y + h/2*k), (x + w/2*k, y), (x, y - h/2*k), (x - w/2*k, y)], col)
def d_mandala(c):
    c.setFillColor(NAVY); c.rect(AX, AY, AW, AH, stroke=0, fill=1)
    R = 500
    def petal(a, r1, r2, wdt, col):
        p = c.beginPath()
        bx, by = CX + r1*math.cos(a), CY + r1*math.sin(a); tx, ty = CX + r2*math.cos(a), CY + r2*math.sin(a)
        mx, my = (bx+tx)/2, (by+ty)/2; nx, ny = -math.sin(a)*wdt, math.cos(a)*wdt
        p.moveTo(bx, by); p.curveTo(mx+nx, my+ny, mx+nx, my+ny, tx, ty); p.curveTo(mx-nx, my-ny, mx-nx, my-ny, bx, by)
        c.setFillColor(col); c.drawPath(p, stroke=1, fill=1)
    circ(c, CX, CY, R, CREAM)
    for r1, r2, n, wd, off, col in ((0.64, 0.97, 24, 0.105, 0, TEAL), (0.38, 0.75, 16, 0.16, 0.5, MUST), (0.155, 0.49, 12, 0.13, 0, CORAL), (0, 0.245, 8, 0.09, 0.5, SAGE)):
        for i in range(n): petal(2*math.pi*(i+off)/n, r1*R, r2*R, wd*R, col)
    circ(c, CX, CY, R*0.07, NAVY)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = CX + sx*(AW/2 - 120), CY + sy*(AH/2 - 120)
            poly(c, starpts(x, y, 78, 40, 8, 0), MUST); circ(c, x, y, 16, CORAL, 0)

DESIGNS = [("01_Star_and_Cross", d_star_cross, NAVY), ("02_Octagon_Stars", d_oct, CREAM), ("03_Honeycomb", d_hex, NAVY),
           ("04_Scallops", d_scallop, CREAM), ("05_Diamonds", d_diamond, NAVY), ("06_Mandala", d_mandala, CREAM)]
for name, fn, line in DESIGNS:
    c = canvas.Canvas(f"{out}/Geometric_Print_{name}.pdf", pagesize=(PW, PH)); c.setTitle(name.replace("_", " "))
    c.setFillColor(CREAM); c.rect(0, 0, PW, PH, stroke=0, fill=1)
    c.saveState(); p = c.beginPath(); p.rect(AX, AY, AW, AH); c.clipPath(p, stroke=0, fill=0)
    c.setStrokeColor(line); c.setLineWidth(4); c.setLineJoin(1); fn(c); c.restoreState()
    c.setStrokeColor(NAVY); c.setLineWidth(5); c.rect(AX, AY, AW, AH, stroke=1, fill=0)
    c.showPage(); c.save()
print("ok")
