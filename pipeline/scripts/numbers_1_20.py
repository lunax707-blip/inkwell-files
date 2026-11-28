# Numbers 1 to 20 Worksheets: kids worksheet bundle (rotation C).
# Builds US Letter and A4 PDFs into /home/claude/book/out/numbers/ and a manifest JSON
# (every counted object and ten frame dot as drawn, every answer) that verify_numbers_1_20.py checks.
import json, math, random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = '/home/claude/fonts/ttf/'
for n, f in [('Fr', 'fraunces-latin-300-normal'), ('FrM', 'fraunces-latin-400-normal'), ('FrB', 'fraunces-latin-500-normal'),
             ('FrI', 'fraunces-latin-300-italic'), ('In', 'instrument-sans-latin-400-normal'),
             ('InM', 'instrument-sans-latin-500-normal'), ('InB', 'instrument-sans-latin-600-normal')]:
    pdfmetrics.registerFont(TTFont(n, F + f + '.ttf'))

INK = HexColor('#20294A'); SOFT = HexColor('#646A82'); LINE = HexColor('#AEB2C2'); HAIR = HexColor('#DCDEE6')
CORAL = HexColor('#D9583B'); CREAM = HexColor('#F7EFE2'); TEAL = HexColor('#1F6F78'); MUST = HexColor('#E8A33D')
SAGE = HexColor('#7FA086'); NAVY = HexColor('#2B3A67'); WHITE = HexColor('#FFFFFF'); TINT = HexColor('#F4EFE6')
BROWN = HexColor('#7A5A44'); DOT = HexColor('#9299AE'); ORANGE = HexColor('#E57E2E')
RINGS = [CORAL, TEAL, MUST, NAVY, SAGE]
NAME = 'Numbers 1 to 20 Worksheets'
OUT = '/home/claude/book/out/numbers/'
WARN = []
sw = pdfmetrics.stringWidth

WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
         'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']
PLURAL = {'star': 'stars', 'apple': 'apples', 'balloon': 'balloons', 'car': 'cars', 'boat': 'boats', 'flower': 'flowers',
          'leaf': 'leaves', 'kite': 'kites', 'ball': 'balls', 'house': 'houses', 'tree': 'trees', 'cupcake': 'cupcakes',
          'rocket': 'rockets', 'umbrella': 'umbrellas', 'heart': 'hearts'}
KINDS = list(PLURAL)
PAT = {1: [1], 2: [2], 3: [3], 4: [2, 2], 5: [3, 2], 6: [3, 3], 7: [4, 3], 8: [4, 4], 9: [3, 3, 3], 10: [4, 3, 3]}

# Single stroke digits for tracing, in a box 0.6 wide and 1 high. Each stroke: start point, then segments.
K = 0.5523
DIG = {
    0: [[(0.30, 1.0), ('C', 0.30 - 0.26 * K, 1.0, 0.04, 0.5 + 0.5 * K, 0.04, 0.5), ('C', 0.04, 0.5 - 0.5 * K, 0.30 - 0.26 * K, 0.0, 0.30, 0.0),
         ('C', 0.30 + 0.26 * K, 0.0, 0.56, 0.5 - 0.5 * K, 0.56, 0.5), ('C', 0.56, 0.5 + 0.5 * K, 0.30 + 0.26 * K, 1.0, 0.30, 1.0)]],
    1: [[(0.12, 0.78), ('L', 0.34, 1.0), ('L', 0.34, 0.0)]],
    2: [[(0.06, 0.76), ('C', 0.08, 1.07, 0.55, 1.08, 0.55, 0.74), ('C', 0.55, 0.50, 0.22, 0.28, 0.04, 0.0), ('L', 0.57, 0.0)]],
    3: [[(0.06, 0.84), ('C', 0.14, 1.05, 0.54, 1.06, 0.54, 0.76), ('C', 0.54, 0.60, 0.40, 0.53, 0.24, 0.53),
         ('C', 0.44, 0.53, 0.57, 0.43, 0.57, 0.27), ('C', 0.57, -0.07, 0.12, -0.06, 0.03, 0.16)]],
    4: [[(0.14, 1.0), ('L', 0.04, 0.36), ('L', 0.58, 0.36)], [(0.44, 1.0), ('L', 0.44, 0.0)]],
    5: [[(0.14, 1.0), ('L', 0.10, 0.56), ('C', 0.20, 0.66, 0.57, 0.70, 0.57, 0.32), ('C', 0.57, -0.08, 0.12, -0.06, 0.03, 0.14)],
        [(0.14, 1.0), ('L', 0.54, 1.0)]],
    6: [[(0.48, 1.0), ('C', 0.22, 0.86, 0.04, 0.60, 0.04, 0.30), ('C', 0.04, 0.13, 0.16, 0.0, 0.305, 0.0),
         ('C', 0.45, 0.0, 0.57, 0.13, 0.57, 0.30), ('C', 0.57, 0.47, 0.45, 0.60, 0.305, 0.60), ('C', 0.18, 0.60, 0.07, 0.50, 0.04, 0.33)]],
    7: [[(0.04, 1.0), ('L', 0.57, 1.0), ('L', 0.22, 0.0)]],
    8: [[(0.50, 0.82), ('C', 0.42, 1.05, 0.07, 1.03, 0.07, 0.76), ('C', 0.07, 0.52, 0.57, 0.55, 0.57, 0.25),
         ('C', 0.57, -0.08, 0.03, -0.08, 0.03, 0.25), ('C', 0.03, 0.55, 0.53, 0.52, 0.53, 0.76), ('C', 0.53, 0.79, 0.52, 0.80, 0.50, 0.82)]],
    9: [[(0.56, 0.71), ('C', 0.56, 0.87, 0.45, 1.0, 0.30, 1.0), ('C', 0.15, 1.0, 0.04, 0.87, 0.04, 0.71), ('C', 0.04, 0.55, 0.15, 0.43, 0.30, 0.43),
         ('C', 0.45, 0.43, 0.56, 0.55, 0.56, 0.71), ('L', 0.56, 1.0)], [(0.56, 0.71), ('L', 0.56, 0.0)]],
}
DIG[9] = [[(0.56, 0.74), ('C', 0.56, 0.89, 0.45, 1.0, 0.30, 1.0), ('C', 0.15, 1.0, 0.04, 0.88, 0.04, 0.72), ('C', 0.04, 0.56, 0.15, 0.44, 0.30, 0.44),
           ('C', 0.45, 0.44, 0.56, 0.56, 0.56, 0.74), ('L', 0.56, 0.98), ('L', 0.56, 0.0)]]


def numw(n, h): return len(str(n)) * 0.6 * h + (len(str(n)) - 1) * 0.2 * h


class Book:
    def __init__(self, path, size, tag, toc=None):
        self.c = canvas.Canvas(path, pagesize=size)
        self.W, self.H = size; self.m = 46; self.w = self.W - 2 * self.m
        self.tag = tag; self.toc = toc or {}; self.seen = []
        self.n = 1; self.sec = ''; self.ac = CORAL; self.title = ''
        self.key = []; self.man = []; self.rng = random.Random(1220)
        self.c.setTitle(NAME + ' (' + tag + ')'); self.c.setAuthor('Inkwell and Co')
        self.c.setSubject('Printable numbers 1 to 20 worksheets for kids. For personal use.')

    # text -----------------------------------------------------------
    def text(self, x, y, s, font='In', size=11, col=INK, align='l', maxw=None):
        c = self.c; c.setFillColor(col); c.setFont(font, size)
        if maxw is not None and sw(s, font, size) > maxw + 0.5:
            WARN.append('too wide: "%s" p%d %s (%.0f > %.0f)' % (s, self.n, self.tag, sw(s, font, size), maxw))
        {'l': c.drawString, 'r': c.drawRightString, 'c': c.drawCentredString}[align](x, y, s)
        return sw(s, font, size)

    def para(self, x, y, w, s, font='In', size=11, lead=16, col=INK):
        line = ''
        for wd in s.split():
            t = (line + ' ' + wd).strip()
            if sw(t, font, size) > w: self.text(x, y, line, font, size, col); y -= lead; line = wd
            else: line = t
        if line: self.text(x, y, line, font, size, col); y -= lead
        return y

    def hl(self, x1, x2, y, col=LINE, w=0.7, dash=None):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(w)
        if dash: c.setDash(*dash)
        c.line(x1, y, x2, y); c.setDash()

    def rbox(self, x, y, w, h, r=8, col=INK, lw=1, fill=None, dash=None):
        c = self.c; c.setStrokeColor(col or WHITE); c.setLineWidth(lw)
        if fill: c.setFillColor(fill)
        if dash: c.setDash(*dash)
        c.roundRect(x, y, w, h, r, stroke=1 if col else 0, fill=1 if fill else 0); c.setDash()

    def badge(self, cx, cy, s, col=None, r=9.5):
        c = self.c; c.setFillColor(col or self.ac); c.circle(cx, cy, r, stroke=0, fill=1)
        self.text(cx, cy - r * 0.37, str(s), 'InB', r * 1.05, WHITE, 'c')

    def num(self, cx, y, n, size, col=INK, font='InB'):
        """A printed number centred on cx with its baseline at y."""
        self.text(cx, y, str(n), font, size, col, 'c')

    def tile(self, cx, cy, s, n, col, size=None, tcol=WHITE):
        size = size or s * (0.62 if n < 10 else 0.5)
        self.rbox(cx - s / 2, cy - s / 2, s, s, r=s * 0.2, col=None, fill=col)
        self.text(cx, cy - size * 0.355, str(n), 'InB', size, tcol, 'c')

    def wbox(self, cx, y, w=46, h=38):
        self.rbox(cx - w / 2, y, w, h, r=8, col=INK, lw=1.1)

    # icons (objects and plants only) ------------------------------------
    def icon(self, kind, cx, cy, s, col=CORAL, outline=False, rec=None):
        c = self.c; u = s / 2.0; lw = max(0.9, s * 0.04)
        X = lambda x: cx + x * u
        Y = lambda y: cy + y * u
        c.setLineJoin(1); c.setLineCap(1)

        def paint(p, colr):
            if outline:
                c.setStrokeColor(INK); c.setLineWidth(lw); c.setFillColor(WHITE); c.drawPath(p, stroke=1, fill=1)
            else:
                c.setFillColor(colr); c.drawPath(p, stroke=0, fill=1)

        def poly(pts, colr):
            p = c.beginPath(); p.moveTo(X(pts[0][0]), Y(pts[0][1]))
            for x, y in pts[1:]: p.lineTo(X(x), Y(y))
            p.close(); paint(p, colr)

        def curve(start, segs, colr):
            p = c.beginPath(); p.moveTo(X(start[0]), Y(start[1]))
            for sg in segs:
                if len(sg) == 2: p.lineTo(X(sg[0]), Y(sg[1]))
                else: p.curveTo(X(sg[0]), Y(sg[1]), X(sg[2]), Y(sg[3]), X(sg[4]), Y(sg[5]))
            p.close(); paint(p, colr)

        def circ(x, y, r, colr):
            p = c.beginPath(); p.circle(X(x), Y(y), r * u); paint(p, colr)

        def blob(cs, colr):
            if outline:
                c.setStrokeColor(INK); c.setLineWidth(lw * 2); c.setFillColor(WHITE)
                for x, y, r in cs: c.circle(X(x), Y(y), r * u, stroke=1, fill=0)
                for x, y, r in cs: c.circle(X(x), Y(y), r * u, stroke=0, fill=1)
            else:
                c.setFillColor(colr)
                for x, y, r in cs: c.circle(X(x), Y(y), r * u, stroke=0, fill=1)

        def stroke(pts, colr, wd, bez=None):
            c.setStrokeColor(INK if outline else colr); c.setLineWidth(lw if outline else wd * u)
            p = c.beginPath(); p.moveTo(X(pts[0][0]), Y(pts[0][1]))
            if bez: p.curveTo(X(bez[0]), Y(bez[1]), X(bez[2]), Y(bez[3]), X(bez[4]), Y(bez[5]))
            else:
                for x, y in pts[1:]: p.lineTo(X(x), Y(y))
            c.drawPath(p, stroke=1, fill=0)

        if kind == 'star':
            pts = []
            for i in range(10):
                a = math.radians(90 + i * 36); rr = 1.0 if i % 2 == 0 else 0.46
                pts.append((rr * math.cos(a), rr * math.sin(a) - 0.05))
            poly(pts, col)
        elif kind == 'apple':
            stroke([(0, 0.42), (0.1, 0.92)], BROWN, 0.11)
            curve((0.1, 0.66), [(0.2, 0.98, 0.5, 1.0, 0.68, 0.9), (0.56, 0.64, 0.3, 0.58, 0.1, 0.66)], SAGE)
            curve((0, 0.45), [(-0.35, 0.75, -0.95, 0.5, -0.95, -0.05), (-0.95, -0.6, -0.5, -1.0, 0, -0.85),
                              (0.5, -1.0, 0.95, -0.6, 0.95, -0.05), (0.95, 0.5, 0.35, 0.75, 0, 0.45)], col)
        elif kind == 'balloon':
            stroke([(0, -0.6)], SOFT, 0.05, bez=(-0.12, -0.75, 0.14, -0.86, 0.02, -1.0))
            poly([(0, -0.5), (-0.12, -0.68), (0.12, -0.68)], col)
            curve((0, 1.0), [(-0.42, 1.0, -0.7, 0.66, -0.7, 0.24), (-0.7, -0.2, -0.36, -0.56, 0, -0.56),
                             (0.36, -0.56, 0.7, -0.2, 0.7, 0.24), (0.7, 0.66, 0.42, 1.0, 0, 1.0)], col)
            if not outline: c.setFillColor(WHITE); c.setFillAlpha(0.45); c.circle(X(-0.3), Y(0.52), 0.12 * u, stroke=0, fill=1); c.setFillAlpha(1)
        elif kind == 'car':
            curve((-0.52, 0.02), [(-0.36, 0.52), (0.3, 0.52), (0.6, 0.02)], col)
            p = c.beginPath(); p.roundRect(X(-1), Y(-0.5), 2 * u, 0.56 * u, 0.16 * u); paint(p, col)
            if not outline:
                poly([(-0.36, 0.08), (-0.27, 0.4), (-0.03, 0.4), (-0.03, 0.08)], WHITE); poly([(0.06, 0.08), (0.06, 0.4), (0.24, 0.4), (0.44, 0.08)], WHITE)
            for x in (-0.55, 0.55):
                circ(x, -0.5, 0.26, INK)
                if not outline: c.setFillColor(WHITE); c.circle(X(x), Y(-0.5), 0.1 * u, stroke=0, fill=1)
        elif kind == 'boat':
            stroke([(0, -0.4), (0, 0.98)], BROWN, 0.09)
            poly([(0.1, 0.92), (0.1, -0.22), (0.82, -0.22)], col); poly([(-0.1, 0.6), (-0.1, -0.22), (-0.66, -0.22)], MUST if col != MUST else TEAL)
            poly([(-0.95, -0.38), (0.95, -0.38), (0.62, -0.9), (-0.62, -0.9)], NAVY if col != NAVY else TEAL)
        elif kind == 'flower':
            for i in range(6):
                a = math.radians(i * 60 + 30); circ(0.56 * math.cos(a), 0.56 * math.sin(a), 0.36, col)
            circ(0, 0, 0.3, MUST if col != MUST else CORAL)
        elif kind == 'leaf':
            curve((-0.82, -0.82), [(-0.92, 0.3, 0.1, 0.95, 0.86, 0.86), (0.95, 0.0, 0.3, -0.95, -0.82, -0.82)], col)
            if outline: stroke([(-0.82, -0.82), (0.5, 0.5)], INK, 0.05)
            else: stroke([(-0.6, -0.6), (0.5, 0.5)], WHITE, 0.07)
        elif kind == 'kite':
            stroke([(0, -0.55)], SOFT, 0.05, bez=(0.3, -0.7, -0.1, -0.86, 0.26, -1.0))
            poly([(0, 1.0), (0.64, 0.3), (0, -0.56), (-0.64, 0.3)], col)
            if outline: stroke([(0, 1.0), (0, -0.56)], INK, 0.05); stroke([(-0.64, 0.3), (0.64, 0.3)], INK, 0.05)
            else: stroke([(0, 0.94), (0, -0.5)], WHITE, 0.06); stroke([(-0.58, 0.3), (0.58, 0.3)], WHITE, 0.06)
        elif kind == 'ball':
            circ(0, 0, 0.92, col)
            for bz, st in [((-0.4, 0.42, 0.4, 0.42, 0.86, 0.3), (-0.86, 0.3)), ((-0.4, -0.18, 0.4, -0.18, 0.86, -0.3), (-0.86, -0.3))]:
                stroke([st], WHITE, 0.09, bez=bz)
        elif kind == 'house':
            poly([(-0.7, -0.92), (0.7, -0.92), (0.7, 0.12), (-0.7, 0.12)], col)
            poly([(-0.98, 0.1), (0, 0.98), (0.98, 0.1)], NAVY if col != NAVY else CORAL)
            poly([(-0.5, -0.92), (-0.12, -0.92), (-0.12, -0.3), (-0.5, -0.3)], MUST if col != MUST else WHITE)
            poly([(0.12, -0.5), (0.5, -0.5), (0.5, -0.12), (0.12, -0.12)], WHITE)
        elif kind == 'tree':
            poly([(-0.13, -0.98), (0.13, -0.98), (0.13, -0.2), (-0.13, -0.2)], BROWN)
            blob([(0, 0.42, 0.55), (-0.42, 0.06, 0.44), (0.42, 0.06, 0.44)], col)
        elif kind == 'cupcake':
            poly([(-0.62, 0.02), (0.62, 0.02), (0.44, -0.96), (-0.44, -0.96)], MUST if col != MUST else TEAL)
            blob([(-0.4, 0.2, 0.34), (0.4, 0.2, 0.34), (0, 0.38, 0.44)], col)
            circ(0, 0.84, 0.15, CORAL if col != CORAL else NAVY)
        elif kind == 'rocket':
            poly([(-0.22, -0.6), (0.22, -0.6), (0, -1.0)], MUST)
            poly([(0.4, -0.1), (0.86, -0.78), (0.38, -0.6)], NAVY if col != NAVY else CORAL); poly([(-0.4, -0.1), (-0.86, -0.78), (-0.38, -0.6)], NAVY if col != NAVY else CORAL)
            curve((0, 1.0), [(0.56, 0.6, 0.5, -0.3, 0.4, -0.62), (-0.4, -0.62), (-0.5, -0.3, -0.56, 0.6, 0, 1.0)], col)
            circ(0, 0.22, 0.2, WHITE)
        elif kind == 'umbrella':
            c.setStrokeColor(INK if outline else BROWN); c.setLineWidth(lw if outline else 0.1 * u)
            p = c.beginPath(); p.moveTo(X(0), Y(0.2)); p.lineTo(X(0), Y(-0.72)); p.curveTo(X(0), Y(-1.0), X(0.36), Y(-1.0), X(0.36), Y(-0.72)); c.drawPath(p, stroke=1, fill=0)
            curve((-0.96, 0.1), [(-0.96, 0.75, -0.45, 0.96, 0, 0.96), (0.45, 0.96, 0.96, 0.75, 0.96, 0.1),
                                 (0.8, 0.32, 0.45, 0.32, 0.32, 0.1), (0.2, 0.32, -0.2, 0.32, -0.32, 0.1), (-0.45, 0.32, -0.8, 0.32, -0.96, 0.1)], col)
        elif kind == 'heart':
            curve((0, 0.45), [(-0.3, 1.05, -1.1, 0.8, -1.0, 0.15), (-0.95, -0.35, -0.3, -0.6, 0, -0.92),
                              (0.3, -0.6, 0.95, -0.35, 1.0, 0.15), (1.1, 0.8, 0.3, 1.05, 0, 0.45)], col)
        c.setLineCap(0); c.setLineJoin(0)
        if rec is not None: self.man.append({'page': self.n, 'item': rec, 'type': 'obj', 'kind': kind})

    def group(self, x, y, w, h, n, kind, rec, layout='pat', col=CORAL, cap=44, outline=False, flush=False):
        """n icons inside the box whose lower left corner is (x, y)."""
        if layout == 'pat': rows = PAT[n] if n in PAT else [5] * (n // 5) + ([n % 5] if n % 5 else [])
        elif layout == 'rows5': rows = [5] * (n // 5) + ([n % 5] if n % 5 else [])
        elif layout == 'rows10': rows = [10] * (n // 10) + ([n % 10] if n % 10 else [])
        if layout == 'scatter' and n <= 4: layout = 'pat'; rows = PAT[n]; cap = min(cap, 38)
        if layout == 'scatter':
            cols = 3 if n <= 6 else 4; nr = 2 if n <= 6 else 3
            if n > cols * nr: cols += 1
            cells = self.rng.sample(range(cols * nr), n); cw = w / cols; ch = h / nr; s = min(cw, ch, cap / 0.78) * 0.70
            for k in cells:
                jx = (self.rng.random() - 0.5) * (cw - s) * 0.7; jy = (self.rng.random() - 0.5) * (ch - s) * 0.7
                self.icon(kind, x + cw * (k % cols + 0.5) + jx, y + h - ch * (k // cols + 0.5) + jy, s, col, outline, rec)
            return
        mc = max(rows); left = layout != 'pat'
        s = min(w / mc, h / len(rows), cap / 0.80); isz = s * 0.80
        y0 = y + h / 2 + s * len(rows) / 2
        for ri, k in enumerate(rows):
            x0 = x if flush else x + (w - s * (mc if left else k)) / 2
            for j in range(k): self.icon(kind, x0 + s * (j + 0.5), y0 - s * (ri + 0.5), isz, col, outline, rec)

    # ten frames ---------------------------------------------------------
    def frame(self, x, y, cell, n, col, rec=None):
        """One ten frame with its top left corner at (x, y) and n dots, filled along the top row first."""
        c = self.c; c.setFillColor(WHITE); c.setStrokeColor(INK); c.setLineWidth(max(0.8, cell * 0.05))
        c.rect(x, y - 2 * cell, 5 * cell, 2 * cell, stroke=1, fill=1)
        c.setLineWidth(max(0.5, cell * 0.03)); c.line(x, y - cell, x + 5 * cell, y - cell)
        for i in range(1, 5): c.line(x + i * cell, y, x + i * cell, y - 2 * cell)
        for i in range(n):
            c.setFillColor(col); c.circle(x + (i % 5 + 0.5) * cell, y - (i // 5 + 0.5) * cell, cell * 0.33, stroke=0, fill=1)
            if rec is not None: self.man.append({'page': self.n, 'item': rec, 'type': 'dot'})

    def frames(self, cx, ytop, cell, n, col, rec=None, double=False, side=False):
        """One or two ten frames centred on cx. Returns the y of the bottom edge."""
        if not double: self.frame(cx - 2.5 * cell, ytop, cell, n, col, rec); return ytop - 2 * cell
        a, b = min(n, 10), max(0, n - 10); gap = cell * 0.5
        if side:
            self.frame(cx - 5 * cell - gap / 2, ytop, cell, a, col, rec); self.frame(cx + gap / 2, ytop, cell, b, col, rec); return ytop - 2 * cell
        self.frame(cx - 2.5 * cell, ytop, cell, a, col, rec); self.frame(cx - 2.5 * cell, ytop - 2 * cell - gap, cell, b, col, rec)
        return ytop - 4 * cell - gap

    # tracing ------------------------------------------------------------
    def trace(self, x, y, h, n, mode='dash'):
        """Number n as single strokes, left edge x, baseline y, height h. Returns the width."""
        c = self.c; c.setLineCap(1); c.setLineJoin(1)
        for d in str(n):
            for st in DIG[int(d)]:
                p = c.beginPath(); p.moveTo(x + st[0][0] * h, y + st[0][1] * h)
                for sg in st[1:]:
                    if sg[0] == 'L': p.lineTo(x + sg[1] * h, y + sg[2] * h)
                    else: p.curveTo(x + sg[1] * h, y + sg[2] * h, x + sg[3] * h, y + sg[4] * h, x + sg[5] * h, y + sg[6] * h)
                if mode == 'dash': c.setStrokeColor(DOT); c.setLineWidth(h * 0.055); c.setDash([0.01, h * 0.115])
                else: c.setStrokeColor(INK); c.setLineWidth(h * 0.075)
                c.drawPath(p, stroke=1, fill=0); c.setDash()
            for k, st in enumerate(DIG[int(d)]):
                if mode == 'solid' or k == 0:
                    c.setFillColor(CORAL); c.circle(x + st[0][0] * h, y + st[0][1] * h, h * (0.06 if mode == 'solid' else 0.05), stroke=0, fill=1)
            x += 0.8 * h
        c.setLineCap(0); c.setLineJoin(0)
        return numw(n, h)

    def guides(self, x1, x2, y, h):
        self.hl(x1, x2, y + h, col=LINE, w=0.7); self.hl(x1, x2, y + h / 2, col=LINE, w=0.6, dash=(3, 3)); self.hl(x1, x2, y, col=SOFT, w=0.9)

    def label(self, x, y, s, col=None):
        c = self.c; t = c.beginText(x, y); t.setFont('InB', 8.2); t.setFillColor(col or self.ac); t.setCharSpace(1.0); t.textOut(s.upper()); t.setCharSpace(0); c.drawText(t)

    # page frame ---------------------------------------------------------
    def start(self, sec, col):
        self.sec = sec; self.ac = col

    def head(self, title, instr, name=True):
        c = self.c; m = self.m; y = self.H - m
        self.title = title
        if self.sec not in [s for s, _ in self.seen]: self.seen.append((self.sec, self.n))
        lab = self.sec.upper(); lw = sw(lab, 'InB', 7.6) + 0.9 * (len(lab) - 1)
        self.rbox(m, y - 17, lw + 22, 17, r=8.5, col=None, fill=self.ac)
        t = c.beginText(m + 11, y - 11.6); t.setFont('InB', 7.6); t.setFillColor(WHITE); t.setCharSpace(0.9); t.textOut(lab); t.setCharSpace(0); c.drawText(t)
        if name:
            self.text(self.W - m - 168, y - 13, 'Name', 'InM', 9.5, SOFT)
            self.hl(self.W - m - 136, self.W - m, y - 15, col=INK, w=0.8)
        self.text(m - 1, y - 50, title, 'FrM', 25, INK, maxw=self.w)
        yy = self.para(m, y - 70, self.w, instr, 'In', 12, 16.5, SOFT)
        return min(yy - 2, y - 92)

    def foot(self):
        m = self.m; y = m - 14
        self.hl(m, self.W - m, y + 16, col=HAIR, w=0.6)
        self.text(m, y, NAME, 'InM', 7.5, SOFT)
        self.text(self.W - m, y, 'Inkwell and Co   |   For personal use', 'In', 7.5, SOFT, 'r')
        self.text(self.W / 2, y, str(self.n), 'InB', 8.5, INK, 'c')
        self.c.showPage(); self.n += 1

    def area(self, top): return top, self.m + 14

    def ans(self, kind, data, note=None, page=None, title=None):
        self.key.append({'page': page or self.n, 'title': title or self.title, 'kind': kind, 'data': data, 'note': note})

    def cells(self, top, cols, rows):
        top, bot = self.area(top); cw = self.w / cols; ch = (top - bot) / rows
        return [(self.m + (i % cols) * cw, top - (i // cols) * ch, cw, ch) for i in range(cols * rows)]

    def panel(self, x, yt, cw, ch, pad=5, fill=None):
        self.rbox(x + pad, yt - ch + pad, cw - 2 * pad, ch - 2 * pad, r=14, col=HAIR if not fill else None, lw=1, fill=fill)

    # number pages -------------------------------------------------------
    def number_page(self, n, kind, col):
        teen = n > 10
        top = self.head('Number %d' % n, 'Say the number. Trace it with your finger first, then with a pencil.' if not teen else
                        'Say the number. It is one full ten and %s more.' % ('%d' % (n - 10) if n < 20 else 'ten'))
        top, bot = self.area(top); m = self.m; W = self.W
        hero = 150; th = 62 if not teen else 58; blk = th + 30; colh = 68 if not teen else 96; findh = 54
        gap = (top - bot - hero - 2 * blk - colh - findh) / 4.0
        if gap < 9: WARN.append('number page %d too tight (%s) gap %.1f' % (n, self.tag, gap))
        # hero
        y = top - hero
        self.tile(m + hero / 2, y + hero / 2, hero, n, col, size=112 if n < 10 else 88)
        pw = 158; mx = m + hero + 22; mw = self.w - hero - 22 - pw - 14
        self.text(mx, top - 34, WORDS[n], 'FrM', 31 if not teen else 27, INK, maxw=mw + 6)
        cell = min(24, mw / 5.0)
        if not teen:
            self.frames(mx + 2.5 * cell, top - 62, cell, n, col, rec='frame')
            self.text(mx, top - 62 - 2 * cell - 22, 'Count:  ' + '  '.join(str(k) for k in range(1, n + 1)), 'InM', 10.5 if n < 10 else 9.6, SOFT, maxw=mw + 4)
        else: self.frames(mx + 2.5 * cell, top - 50, min(cell, 18.5), n, col, rec='frame', double=True)
        px = W - m - pw
        self.rbox(px, y, pw, hero, r=16, col=None, fill=TINT)
        if not teen: self.group(px + 10, y + 10, pw - 20, hero - 20, n, kind, 'hero', 'pat', col, cap=40)
        else:
            self.text(px + pw / 2, top - 30, 'Ten and some more', 'InB', 9.5, SOFT, 'c')
            self.tile(px + 34, y + 84, 40, 10, NAVY if col != NAVY else TEAL, size=19); self.text(px + pw / 2 - 1, y + 78, 'and', 'In', 12, INK, 'c')
            self.rbox(px + pw - 54, y + 64, 40, 40, r=8, col=INK, lw=1.1, fill=WHITE)
            self.text(px + pw / 2, y + 34, 'make', 'In', 12, INK, 'c'); self.text(px + pw / 2, y + 12, str(n), 'InB', 21, col if col != MUST else INK, 'c')
        # trace
        y = top - hero - gap
        for bi, lab in enumerate(['Trace', 'Write']):
            self.label(m, y - 9, lab + ' the number %d' % n); by = y - 22 - th
            self.guides(m, W - m, by, th)
            slots = 7 if n < 10 else 5; sw_ = self.w / slots; nw = numw(n, th)
            for k in range(slots):
                x = m + sw_ * k + (sw_ - nw) / 2
                if bi == 0: self.trace(x, by, th, n, 'solid' if k == 0 else 'dash')
                elif k == 0: self.trace(x, by, th, n, 'dash')
                elif k < slots: self.c.setFillColor(HAIR); self.c.circle(m + sw_ * k + sw_ / 2, by + th / 2, 1.6, stroke=0, fill=1)
            y -= blk + gap
        # count and color
        self.label(m, y - 9, 'Color %d %s' % (n, PLURAL[kind] if n > 1 else kind))
        tot = 10 if not teen else 20
        self.group(m, y - colh, self.w, colh - 16, tot, kind, None, 'rows10', col, cap=40 if not teen else 34, outline=True)
        y -= colh + gap
        # find
        self.label(m, y - 9, 'Circle every %d' % n)
        pool = [k for k in (range(1, 11) if not teen else range(10, 21)) if k != n and not (n == 1 and k == 10)]
        reps = self.rng.choice([3, 4, 5]); row = [n] * reps + [self.rng.choice(pool) for _ in range(10 - reps)]
        while True:
            self.rng.shuffle(row)
            if all(not (row[i] == n and row[i + 1] == n and row[i + 2] == n) for i in range(8)): break
        cw = self.w / 10.0
        for k, v in enumerate(row): self.text(m + cw * (k + 0.5), y - 43, str(v), 'InB', 22, INK, 'c')
        self.finds.append({'n': n, 'row': row, 'count': reps, 'page': self.n})
        self.foot()

    def chart_page(self, title, instr, nums):
        top = self.head(title, instr, name=False); top, bot = self.area(top); m = self.m
        rh = (top - bot) / len(nums); shown = []
        for i, n in enumerate(nums):
            yt = top - rh * i; cy = yt - rh / 2; col = RINGS[i % 5]
            if i % 2 == 0: self.rbox(m, yt - rh + 2, self.w, rh - 4, r=12, col=None, fill=TINT)
            self.tile(m + 34, cy, rh - 14, n, col)
            self.text(m + 74, cy - 6.5, WORDS[n], 'FrM', 19, INK)
            cell = min(11.5, (rh - 16) / 2)
            if n <= 10:
                self.frame(m + 168, cy + cell, cell, n, col, rec='row%d' % n)
                self.group(m + 250, cy - rh / 2 + 6, self.w - 262, rh - 12, n, KINDS[i % len(KINDS)], 'obj%d' % n, 'rows10', col, cap=25, flush=True)
            else:
                self.frames(m + 178 + 5.25 * cell, cy + cell, cell, n, col, rec='row%d' % n, double=True, side=True)
                x = m + 178 + 10.5 * cell + 26
                self.text(x, cy - 5, '10 and %d more' % (n - 10), 'InM', 13.5, INK, maxw=self.W - m - x - 8)
            shown.append(n)
        self.ans('shown', shown)
        self.foot()

    # worksheet types ----------------------------------------------------
    def count_write(self, title, instr, items, cols, rows, layout='scatter'):
        top = self.head(title, instr)
        for i, ((x, yt, cw, ch), (n, kind)) in enumerate(zip(self.cells(top, cols, rows), items)):
            self.panel(x, yt, cw, ch); self.badge(x + 22, yt - 22, i + 1, col=INK)
            self.group(x + 34, yt - ch + 58, cw - 52, ch - 74, n, kind, i + 1, layout, RINGS[i % 5], cap=40 if layout == 'scatter' else 36)
            self.wbox(x + cw / 2, yt - ch + 14, w=52, h=38)
        self.ans('text', [str(n) for n, _ in items], note={'count': [k for _, k in items]})
        self.foot()

    def count_match(self, title, instr, items, layout='rows5'):
        top = self.head(title, instr); top, bot = self.area(top); m = self.m
        n = len(items); rh = (top - bot) / n; order = list(range(n))
        while any(order[i] == i for i in range(n)): self.rng.shuffle(order)
        pw = self.w * 0.56; pairs = []
        for i, (cnt, kind) in enumerate(items):
            yt = top - rh * i; cy = yt - rh / 2
            self.badge(m + 10, cy, i + 1, col=INK)
            self.rbox(m + 28, yt - rh + 6, pw, rh - 12, r=14, col=HAIR, lw=1)
            self.group(m + 38, yt - rh + 12, pw - 20, rh - 24, cnt, kind, i + 1, layout, RINGS[i % 5], cap=32)
            self.c.setFillColor(INK); self.c.circle(m + 28 + pw + 16, cy, 3.2, stroke=0, fill=1)
            j = order[i]; L = 'ABCDEFGH'[i]; xr = self.W - m - 70
            self.c.circle(xr - 44, cy, 3.2, stroke=0, fill=1)
            self.tile(xr, cy, min(52, rh - 22), items[j][0], TINT, tcol=INK)
            self.badge(self.W - m - 10, cy, L, col=self.ac)
            pairs.append((j, L, items[j][0]))
        self.ans('text', ['%s (%d)' % (L, v) for _, L, v in sorted(pairs)], note={'match': [v for _, _, v in pairs], 'left': [c_ for c_, _ in items]})
        self.foot()

    def choose_count(self, title, instr, items, lo, hi, layout='scatter'):
        top = self.head(title, instr); res = []; allopts = []
        for i, ((x, yt, cw, ch), (n, kind)) in enumerate(zip(self.cells(top, 2, 3), items)):
            self.panel(x, yt, cw, ch); self.badge(x + 22, yt - 22, i + 1, col=INK)
            self.group(x + 34, yt - ch + 62, cw - 52, ch - 78, n, kind, i + 1, layout, RINGS[(i + 1) % 5], cap=36)
            cand = [v for v in (n - 2, n - 1, n + 1, n + 2) if lo <= v <= hi]; opts = [n] + self.rng.sample(cand, 2); opts.sort()
            if self.rng.random() < 0.5: opts.reverse()
            for k, o in enumerate(opts):
                cx = x + cw / 2 + (k - 1) * 58
                self.c.setStrokeColor(LINE); self.c.setLineWidth(1); self.c.circle(cx, yt - ch + 34, 19, stroke=1, fill=0)
                self.text(cx, yt - ch + 27.5, str(o), 'InB', 18, INK, 'c')
            res.append(str(n)); allopts.append(opts)
        self.ans('text', res, note={'choose': allopts})
        self.foot()

    def frame_read(self, title, instr, nums, cols, rows, double=False):
        top = self.head(title, instr)
        for i, ((x, yt, cw, ch), n) in enumerate(zip(self.cells(top, cols, rows), nums)):
            self.panel(x, yt, cw, ch); self.badge(x + 22, yt - 22, i + 1, col=INK)
            cell = min((cw - 60) / 5.0, (ch - 84) / (4.5 if double else 2.0), 30)
            fh = cell * (4.5 if double else 2); yy = yt - 14 - (ch - 70 - fh) / 2
            self.frames(x + cw / 2 + 6, yy, cell, n, RINGS[i % 5], rec=i + 1, double=double)
            self.wbox(x + cw / 2 + 6, yt - ch + 14, w=52, h=38)
        self.ans('text', [str(n) for n in nums], note='frames')
        self.foot()

    def frame_fill(self, title, instr, nums, cols, rows, double=False):
        top = self.head(title, instr)
        for i, ((x, yt, cw, ch), n) in enumerate(zip(self.cells(top, cols, rows), nums)):
            self.panel(x, yt, cw, ch); self.badge(x + 22, yt - 22, i + 1, col=INK)
            cell = min((cw - 60) / 5.0, (ch - 88) / (4.5 if double else 2.0), 30)
            self.tile(x + cw / 2 + 6, yt - 36, 42, n, RINGS[(i + 2) % 5])
            fh = cell * (4.5 if double else 2); yy = yt - 62 - (ch - 74 - fh) / 2
            self.frames(x + cw / 2 + 6, yy, cell, 0, INK, double=double)
        self.ans('text', ['%d dots' % n if n != 1 else '1 dot' for n in nums], note='fill')
        self.foot()

    def draw_page(self, title, instr, items):
        top = self.head(title, instr)
        for i, ((x, yt, cw, ch), (n, shape)) in enumerate(zip(self.cells(top, 2, 3), items)):
            self.panel(x, yt, cw, ch); self.badge(x + 22, yt - 22, i + 1, col=INK)
            self.tile(x + 60, yt - 23, 30, n, RINGS[i % 5], size=16)
            self.text(x + 84, yt - 28, 'Draw %d %s' % (n, shape if n > 1 else shape[:-1]), 'InM', 13, INK, maxw=cw - 96)
        self.foot()

    def seq_page(self, title, instr, rows, note='missing'):
        """rows: (list of numbers, set of hidden positions)"""
        top = self.head(title, instr); top, bot = self.area(top); m = self.m; res = []
        rh = (top - bot) / len(rows); mx = max(len(s) for s, _ in rows); bw = min(46 if mx > 6 else 58, (self.w - 34) / mx - 6); st = bw + 6
        for i, (seq, hid) in enumerate(rows):
            cy = top - rh * (i + 0.5); self.badge(m + 10, cy, i + 1, col=INK)
            x0 = m + 34 + (self.w - 34 - st * len(seq) + 6) / 2
            self.hl(x0 + bw / 2, x0 + st * (len(seq) - 1) + bw / 2, cy, col=LINE, w=1.6)
            col = RINGS[i % 5]
            for k, v in enumerate(seq):
                x = x0 + st * k
                if k in hid: self.rbox(x, cy - bw / 2, bw, bw, r=9, col=INK, lw=1.1, fill=WHITE)
                else:
                    self.rbox(x, cy - bw / 2, bw, bw, r=9, col=None, fill=col)
                    self.text(x + bw / 2, cy - bw * 0.16, str(v), 'InB', bw * 0.46, WHITE, 'c')
            res.append(', '.join(str(seq[k]) for k in sorted(hid)))
        self.ans('text', res, note={note: [[s, sorted(h)] for s, h in rows]})
        self.foot()

    def neighbors(self, title, instr, items):
        """items: (number, mode) with mode after, before, both or between"""
        top = self.head(title, instr); res = []; lab = {'after': 'What comes after?', 'before': 'What comes before?', 'both': 'Before and after', 'between': 'What comes between?'}
        for i, ((x, yt, cw, ch), (n, mode)) in enumerate(zip(self.cells(top, 2, 4), items)):
            self.panel(x, yt, cw, ch); self.badge(x + 22, yt - 22, i + 1, col=INK)
            self.text(x + 40, yt - 26, lab[mode], 'InM', 11, SOFT)
            bw = min(50, ch - 62); cy = yt - ch / 2 - 10; cx = x + cw / 2; col = RINGS[i % 5]
            trio = [n - 1, n, n + 1]; blank = {'after': [2], 'before': [0], 'both': [0, 2], 'between': [1]}[mode]
            show = [k for k in range(3) if k not in blank]
            if mode in ('after',): show = [1]
            if mode in ('before',): show = [1]
            cx += {'after': -1, 'before': 1}.get(mode, 0) * (bw + 12) / 2
            self.hl(cx - bw - 10, cx + bw + 10, cy, col=LINE, w=1.6)
            for k in range(3):
                bx = cx + (k - 1) * (bw + 12) - bw / 2
                if k in blank: self.rbox(bx, cy - bw / 2, bw, bw, r=9, col=INK, lw=1.1, fill=WHITE)
                elif k in show:
                    self.rbox(bx, cy - bw / 2, bw, bw, r=9, col=None, fill=col); self.text(bx + bw / 2, cy - bw * 0.16, str(trio[k]), 'InB', bw * 0.46, WHITE, 'c')
                else: self.c.setFillColor(WHITE); self.c.rect(bx - 7, cy - 3, bw + 14, 6, stroke=0, fill=1)
            res.append(' and '.join(str(trio[k]) for k in blank))
        self.ans('text', res, note={'neighbors': [[n, md] for n, md in items]})
        self.foot()

    def more_page(self, title, instr, pairs, ask='more'):
        top = self.head(title, instr); top, bot = self.area(top); m = self.m; res = []
        rh = (top - bot) / len(pairs); pw = (self.w - 34 - 14) / 2
        for i, (a, ka, b_, kb) in enumerate(pairs):
            yt = top - rh * i; self.badge(m + 10, yt - rh / 2, i + 1, col=INK)
            for j, (cnt, kind, L) in enumerate([(a, ka, 'A'), (b_, kb, 'B')]):
                x = m + 34 + j * (pw + 14)
                self.rbox(x, yt - rh + 6, pw, rh - 12, r=14, col=HAIR, lw=1)
                self.badge(x + 18, yt - 24, L, col=self.ac, r=9)
                self.group(x + 34, yt - rh + 12, pw - 46, rh - 24, cnt, kind, '%d%s' % (i + 1, L), 'rows5', RINGS[(i + j * 2) % 5], cap=30)
            res.append('A' if (a > b_) == (ask == 'more') else 'B')
        self.ans('text', res, note={'ask': ask, 'pairs': [[a, b_] for a, _, b_, _ in pairs]})
        self.foot()

    def compare_page(self, title, instr, pairs, ask='bigger'):
        top = self.head(title, instr); res = []
        for i, ((x, yt, cw, ch), (a, b_)) in enumerate(zip(self.cells(top, 3, 4), pairs)):
            self.panel(x, yt, cw, ch, pad=4); self.badge(x + 20, yt - 20, i + 1, col=INK, r=8.5)
            r = min(26, ch * 0.26)
            for j, v in enumerate((a, b_)):
                cx = x + cw / 2 + (j - 0.5) * (2 * r + 14) + 4; cy = yt - ch / 2 - 4
                self.c.setStrokeColor(RINGS[(i + j) % 5]); self.c.setLineWidth(2.2); self.c.setFillColor(WHITE); self.c.circle(cx, cy, r, stroke=1, fill=1)
                self.text(cx, cy - r * 0.27, str(v), 'InB', r * 0.78, INK, 'c')
            res.append(str(max(a, b_) if ask == 'bigger' else min(a, b_)))
        self.ans('text', res, note={'compare': ask, 'pairs': [list(p) for p in pairs]})
        self.foot()

    def order_page(self, title, instr, sets):
        top = self.head(title, instr); top, bot = self.area(top); m = self.m; res = []; rh = (top - bot) / len(sets)
        for i, st in enumerate(sets):
            yt = top - rh * i; cy = yt - rh / 2; self.badge(m + 10, cy, i + 1, col=INK)
            self.rbox(m + 28, yt - rh + 6, self.w - 28, rh - 12, r=14, col=HAIR, lw=1)
            bw = min(44, rh - 34); half = (self.w - 28) / 2
            for k, v in enumerate(st):
                cx = m + 28 + half * (k + 0.5) / len(st) * 0.92 + 10
                self.tile(cx, cy, bw, v, RINGS[(i + k) % 5])
            ax = m + 28 + half * 0.96 + 2
            c = self.c; c.setStrokeColor(self.ac); c.setLineWidth(1.8); c.setLineCap(1)
            c.line(ax, cy, ax + 24, cy); c.line(ax + 24, cy, ax + 17, cy + 5.5); c.line(ax + 24, cy, ax + 17, cy - 5.5); c.setLineCap(0)
            for k in range(len(st)):
                cx = ax + 40 + (self.W - m - 12 - ax - 40) * (k + 0.5) / len(st)
                self.rbox(cx - bw / 2, cy - bw / 2, bw, bw, r=9, col=INK, lw=1.1)
            res.append(', '.join(str(v) for v in sorted(st)))
        self.ans('text', res, note={'order': [list(s) for s in sets]})
        self.foot()

    def words_page(self, title, instr, blocks):
        top = self.head(title, instr); top, bot = self.area(top); m = self.m; res = []; bwid = (self.w - 20) / len(blocks); allr = []
        for bi, nums in enumerate(blocks):
            x = m + bi * (bwid + 20); n = len(nums); rh = (top - bot) / n
            self.rbox(x, bot + 4, bwid, top - bot - 8, r=16, col=HAIR, lw=1)
            order = list(range(n))
            while any(order[i] == i for i in range(n)): self.rng.shuffle(order)
            for i, v in enumerate(nums):
                cy = top - rh * (i + 0.5)
                self.tile(x + 40, cy, min(46, rh - 20), v, RINGS[(i + bi) % 5])
                self.c.setFillColor(INK); self.c.circle(x + 78, cy, 3.2, stroke=0, fill=1)
                wv = nums[order[i]]; wx = x + bwid - 14
                self.c.circle(wx - 104, cy, 3.2, stroke=0, fill=1)
                self.rbox(wx - 94, cy - 16, 94, 32, r=16, col=None, fill=TINT)
                self.text(wx - 47, cy - 4.8, WORDS[wv], 'InM', 14, INK, 'c', maxw=86)
                allr.append([v, wv])
            res += ['%d %s' % (v, WORDS[v]) for v in nums]
        self.ans('text', res, note={'words': allr})
        self.foot()

    def ten_more(self, title, instr, nums):
        top = self.head(title, instr); res = []
        for i, ((x, yt, cw, ch), n) in enumerate(zip(self.cells(top, 2, 3), nums)):
            self.panel(x, yt, cw, ch); self.badge(x + 22, yt - 22, i + 1, col=INK)
            cell = min((cw - 70) / 5.0, (ch - 96) / 4.5, 24); col = RINGS[i % 5]
            self.frames(x + cw / 2 + 6, yt - 20, cell, n, col, rec=i + 1, double=True)
            y = yt - ch + 22; cx = x + cw / 2 + 6
            self.text(cx - 84, y, '10 and', 'InM', 14, INK); self.rbox(cx - 34, y - 9, 34, 32, r=7, col=INK, lw=1.1)
            self.text(cx + 8, y, 'make', 'InM', 14, INK); self.rbox(cx + 50, y - 9, 40, 32, r=7, col=INK, lw=1.1)
            res.append('10 and %d make %d' % (n - 10, n))
        self.ans('text', res, note={'tenmore': nums})
        self.foot()

    def dots_page(self, title, instr, pts, answer, extra=None):
        top = self.head(title, instr); top, bot = self.area(top); c = self.c
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; bw = self.w - 110; bh = top - bot - 90
        sc = min(bw / (max(xs) - min(xs)), bh / (max(ys) - min(ys)))
        ox = self.W / 2 - (max(xs) + min(xs)) / 2 * sc; oy = (top + bot) / 2 + 18 - (max(ys) + min(ys)) / 2 * sc
        P = [(ox + x * sc, oy + y * sc) for x, y in pts]; gx = sum(p[0] for p in P) / len(P); gy = sum(p[1] for p in P) / len(P)
        if extra: extra(self, ox, oy, sc)
        for i, (x, y) in enumerate(P):
            c.setFillColor(CORAL if i == 0 else INK); c.circle(x, y, 3.4 if i else 4.6, stroke=0, fill=1)
            d = math.hypot(x - gx, y - gy) or 1; lx = x + (x - gx) / d * 17; ly = y + (y - gy) / d * 17
            self.text(lx, ly - 4.5, str(i + 1), 'InB', 13, INK, 'c')
        self.text(self.m, bot + 18, 'What did you draw?', 'InM', 12.5, INK); self.hl(self.m + 124, self.m + 330, bot + 16, col=INK, w=0.9)
        self.ans('text', [answer], note={'dots': len(pts)})
        self.foot()

    def maze_page(self, title, instr, cols, rows, length):
        top = self.head(title, instr); top, bot = self.area(top); rng = self.rng; c = self.c
        while True:                                   # a path that never touches itself
            path = [(rng.randrange(cols), 0)]
            while len(path) < length:
                x, y = path[-1]; nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                nb = [p for p in nb if 0 <= p[0] < cols and 0 <= p[1] < rows and p not in path]
                if not nb: break
                path.append(rng.choice(nb))
            if len(path) == length and path[-1][1] == rows - 1: break
        grid = {p: i + 1 for i, p in enumerate(path)}
        for y in range(rows):
            for x in range(cols):
                if (x, y) in grid: continue
                bad = set()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (x + dx, y + dy)
                    if q in grid and q in path: bad.update([grid[q] + 1, grid[q] - 1])
                grid[(x, y)] = rng.choice([v for v in range(1, length + 1) if v not in bad])
        cs = min((self.w - 20) / cols, (top - bot - 40) / rows); x0 = self.W / 2 - cs * cols / 2; y0 = top - 22
        for y in range(rows):
            for x in range(cols):
                v = grid[(x, y)]; bx = x0 + x * cs; by = y0 - (y + 1) * cs
                st = (x, y) == path[0]; en = (x, y) == path[-1]
                self.rbox(bx + 3, by + 3, cs - 6, cs - 6, r=12, col=CORAL if st else (TEAL if en else LINE), lw=2.4 if st or en else 1, fill=TINT if st or en else None)
                self.text(bx + cs / 2, by + cs / 2 - cs * 0.13, str(v), 'InB', cs * 0.36, INK, 'c')
        sx = x0 + path[0][0] * cs + cs / 2; ex = x0 + path[-1][0] * cs + cs / 2
        self.text(sx, y0 + 6, 'Start', 'InB', 10.5, CORAL, 'c'); self.text(ex, y0 - rows * cs - 14, 'Finish', 'InB', 10.5, TEAL, 'c')
        mv = {(1, 0): 'right', (-1, 0): 'left', (0, 1): 'down', (0, -1): 'up'}
        steps = [mv[(b_[0] - a[0], b_[1] - a[1])] for a, b_ in zip(path, path[1:])]
        self.ans('plain', ['From 1 go ' + ', '.join(steps[:6]) + ','] + [', '.join(steps[6:13]) + ','] + [', '.join(steps[13:]) + ' to 20.'], note={'maze': [[grid[(x, y)] for x in range(cols)] for y in range(rows)], 'path': [list(p) for p in path]})
        self.foot()

    def quilt_page(self, title, instr):
        top = self.head(title, instr); top, bot = self.area(top); c = self.c; m = self.m
        key = [(1, 'red', CORAL), (2, 'blue', NAVY), (3, 'yellow', MUST), (4, 'green', SAGE)]
        kw = self.w / 4
        for i, (n, nm, col) in enumerate(key):
            x = m + kw * i; self.rbox(x + 4, top - 40, kw - 8, 34, r=10, col=None, fill=TINT)
            self.text(x + 22, top - 29, str(n), 'InB', 17, INK, 'c'); c.setFillColor(col); c.circle(x + 46, top - 23, 9, stroke=0, fill=1)
            self.text(x + 62, top - 27.5, nm, 'InM', 12.5, INK)
        cols = 4; rows = 5; s = min((self.w - 10) / cols, (top - 56 - bot) / rows); x0 = self.W / 2 - s * cols / 2; y0 = top - 52 - ((top - 56 - bot) - s * rows) / 2
        c.setStrokeColor(INK); c.setLineJoin(1)
        for j in range(rows):
            for i in range(cols):
                x = x0 + i * s; y = y0 - (j + 1) * s; cx = x + s / 2; cy = y + s / 2
                a, b_ = (1, 2) if (i + j) % 2 == 0 else (3, 4)
                c.setLineWidth(1.1); c.line(x, y, x + s, y + s); c.line(x, y + s, x + s, y)
                c.setFillColor(WHITE); c.setLineWidth(1.1); c.rect(cx - s * 0.16, cy - s * 0.16, s * 0.32, s * 0.32, stroke=1, fill=1)
                for dx, dy, v in [(0, 0.33, a), (0, -0.33, a), (-0.33, 0, b_), (0.33, 0, b_), (0, 0, 4 if a == 1 else 2)]:
                    self.text(cx + dx * s, cy + dy * s - 4.6, str(v), 'InM', 13, SOFT, 'c')
        c.setLineWidth(2); c.rect(x0, y0 - rows * s, cols * s, rows * s, stroke=1, fill=0)
        c.setLineWidth(1.1)
        for i in range(1, cols): c.line(x0 + i * s, y0, x0 + i * s, y0 - rows * s)
        for j in range(1, rows): c.line(x0, y0 - j * s, x0 + cols * s, y0 - j * s)
        c.setLineJoin(0)
        self.foot()

    def spy_page(self, title, instr, items):
        top = self.head(title, instr); top, bot = self.area(top); m = self.m; rng = self.rng
        ah = 150; sy = bot + ah + 10; sh = top - sy - 4
        self.rbox(m, sy, self.w, sh, r=18, col=None, fill=TINT)
        s = 31; placed = []
        todo = [(k, col) for (cnt, k), col in zip(items, RINGS + [ORANGE]) for _ in range(cnt)]; rng.shuffle(todo)
        for kind, col in todo:
            for _ in range(4000):
                x = m + 24 + rng.random() * (self.w - 48); y = sy + 24 + rng.random() * (sh - 48)
                if all(math.hypot(x - px, y - py) > s * 1.22 for px, py in placed): break
            else: WARN.append('spy placement failed ' + self.tag)
            placed.append((x, y)); self.icon(kind, x, y, s, col, rec=kind)
        cw = self.w / len(items)
        for i, ((cnt, kind), col) in enumerate(zip(items, RINGS + [ORANGE])):
            x = m + cw * i; self.rbox(x + 4, bot + 4, cw - 8, ah - 4, r=14, col=HAIR, lw=1)
            self.icon(kind, x + cw / 2, bot + ah - 34, 34, col)
            self.text(x + cw / 2, bot + ah - 72, PLURAL[kind], 'InM', 11.5, INK, 'c', maxw=cw - 12)
            self.wbox(x + cw / 2, bot + 16, w=min(52, cw - 24), h=40)
        self.ans('text', ['%d %s' % (cnt, PLURAL[k]) for cnt, k in items], note={'spy': [[cnt, k] for cnt, k in items]})
        self.foot()


# ---------------------------------------------------------------- content
STAR10 = [((1.0 if i % 2 == 0 else 0.42) * math.cos(math.radians(90 - i * 36)), (1.0 if i % 2 == 0 else 0.42) * math.sin(math.radians(90 - i * 36))) for i in range(10)]
ROCKET = [(0, 10), (1.3, 8.6), (1.9, 7.0), (2, 5.2), (2, 3.6), (2, 2.0), (3.9, 0.4), (3.9, -1.8), (2, -0.6), (1.4, -2.1), (0, -1.3),
          (-1.4, -2.1), (-2, -0.6), (-3.9, -1.8), (-3.9, 0.4), (-2, 2.0), (-2, 3.6), (-2, 5.2), (-1.9, 7.0), (-1.3, 8.6)]


def rocket_extra(b, ox, oy, sc):
    c = b.c; c.setStrokeColor(LINE); c.setLineWidth(1.6); c.setFillColor(WHITE); c.circle(ox, oy + 5.6 * sc, 0.95 * sc, stroke=1, fill=1)
    for x, y, r, col in [(-5.4, 9, 9, MUST), (5.6, 6.6, 7, TEAL), (-5.8, 4.2, 6, CORAL), (5.2, 10, 5, CORAL)]: b.icon('star', ox + x * sc, oy + y * sc, r * 2, col)


def star_extra(b, ox, oy, sc):
    for x, y, r, col in [(-1.05, 0.95, 7, TEAL), (1.08, 0.9, 6, MUST), (1.0, -0.95, 7, SAGE), (-1.02, -0.9, 5, NAVY)]: b.icon('star', ox + x * sc, oy + y * sc, r * 2, col)


def build(path, size, tag, toc=None):
    b = Book(path, size, tag, toc); c = b.c; W, H, M = b.W, b.H, b.m; rng = b.rng; b.finds = []
    toc = toc or {}

    # 1 cover ------------------------------------------------------------
    c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)
    b.text(W / 2, H - 132, 'PRINTABLE WORKSHEETS', 'InB', 11, TEAL, 'c')
    b.text(W / 2, H - 196, 'Numbers 1 to 20', 'FrM', 58, INK, 'c')
    b.text(W / 2, H - 238, 'Trace, count and write', 'FrI', 25, CORAL, 'c')
    ts = W * 0.235; gy = H * 0.455
    for k, (n, col) in enumerate([(1, CORAL), (2, TEAL), (3, MUST)]):
        cx = W / 2 + (k - 1) * (ts + 16); b.tile(cx, gy, ts, n, col, size=ts * 0.7)
    for kind, x, y, s, col in [('star', 0.12, 0.905, 30, MUST), ('balloon', 0.885, 0.90, 46, CORAL), ('kite', 0.115, 0.635, 44, TEAL), ('star', 0.885, 0.64, 26, TEAL), ('star', 0.27, 0.615, 14, CORAL), ('star', 0.74, 0.625, 12, MUST),
                               ('apple', 0.15, 0.255, 40, CORAL), ('boat', 0.85, 0.26, 46, CORAL), ('star', 0.30, 0.285, 18, NAVY), ('flower', 0.69, 0.275, 30, SAGE),
                               ('rocket', 0.5, 0.265, 50, NAVY)]:
        b.icon(kind, W * x, H * y, s, col)
    labs = ['Ages 3 to 6', '%d pages' % toc.get('_pages', 0), 'Answer key inside']; ws = [sw(s, 'InB', 11) + 30 for s in labs]; x = W / 2 - (sum(ws) + 20) / 2; cy_ = H * 0.165
    for s, w_, col in zip(labs, ws, [TEAL, NAVY, CORAL]):
        b.rbox(x, cy_ - 8, w_, 27, r=13.5, col=None, fill=col); b.text(x + w_ / 2, cy_ + 1.5, s, 'InB', 11, WHITE, 'c'); x += w_ + 10
    b.text(W / 2, 52, 'Inkwell and Co', 'FrM', 13, INK, 'c')
    c.showPage(); b.n += 1

    # 2 for grown ups + contents ----------------------------------------------
    b.start('Start here', NAVY)
    top = b.head('For the grown ups', 'A quick guide to getting the most out of these pages.', name=False)
    y = top - 6; colw = b.w * 0.54
    tips = [('Go in order.', 'Start with 1 to 10. Move on to 11 to 20 only when the first ten feel easy.'),
            ('Finger first.', 'On each number page, trace the big number with a finger before picking up a pencil. Every stroke starts at the red dot.'),
            ('Touch and count.', 'Ask your child to touch each picture as they say the number. Crossing pictures out helps with bigger groups.'),
            ('Use the ten frames.', 'A full frame is always ten. From 11 on, count "ten" and then the extra dots.'),
            ('Short and often.', 'One or two pages a day is plenty. Stop while it is still fun.'),
            ('Check together.', 'The answer key starts on page %d. Print any page again for more practice.' % toc.get('Answer key', 0))]
    for k, (hd, tx) in enumerate(tips):
        b.badge(M + 11, y - 5, k + 1, col=RINGS[k % 5], r=11)
        b.text(M + 34, y - 9, hd, 'InB', 13, INK)
        y = b.para(M + 34, y - 28, colw - 46, tx, 'In', 11.5, 17, SOFT) - 16
    x = M + colw + 10; wd = b.w - colw - 10; yy = top - 2
    b.rbox(x, M + 30, wd, yy - M - 30, r=14, col=None, fill=TINT)
    b.text(x + 18, yy - 32, "What's inside", 'FrM', 17, INK)
    ty = yy - 62
    for s_, p in [t for t in toc.items() if not t[0].startswith('_') and t[0] != 'Start here']:
        b.text(x + 18, ty, s_, 'InM', 11.5, INK, maxw=wd - 60); b.text(x + wd - 18, ty, str(p), 'InB', 11.5, CORAL, 'r')
        b.hl(x + 18, x + wd - 18, ty - 9, col=LINE, w=0.5, dash=(1, 2)); ty -= 29
    ty -= 18
    b.text(x + 18, ty, 'You will need', 'FrM', 17, INK); ty -= 28
    for it in ['A pencil and an eraser', 'Crayons or colored pencils', 'Red, blue, yellow and green', 'Counters or buttons (optional)']:
        c.setFillColor(CORAL); c.circle(x + 22, ty + 3.5, 2.6, stroke=0, fill=1)
        b.text(x + 34, ty, it, 'In', 11.5, INK, maxw=wd - 50); ty -= 22
    b.foot()

    # numbers 1 to 10 -------------------------------------------------------
    b.start('Numbers 1 to 10', CORAL)
    b.chart_page('Numbers 1 to 10 at a glance', 'Read each row out loud: the number, the word, the dots and the pictures.', list(range(1, 11)))
    first = b.n
    for n, kind in zip(range(1, 11), ['rocket', 'boat', 'balloon', 'car', 'star', 'apple', 'flower', 'kite', 'leaf', 'ball']):
        b.number_page(n, kind, RINGS[(n - 1) % 5])
    b.ans('plain', ['%d: circle %d' % (f['n'], f['count']) for f in b.finds], note={'finds': b.finds[:]}, page='%d to %d' % (first, b.n - 1),
          title='Number pages 1 to 10: how many to circle in the last row')

    # count to 10 -----------------------------------------------------------
    b.start('Count to 10', TEAL)
    kd = lambda ns: [(n, k) for n, k in zip(ns, rng.sample(KINDS, len(ns)))]
    b.count_write('Count and write', 'Touch each picture and count. Write the number in the box.', kd([3, 1, 5, 2, 4, 6]), 2, 3)
    b.count_write('Count and write', 'Count slowly. Cross out each picture as you count it.', kd([7, 9, 6, 10, 8, 5]), 2, 3)
    b.choose_count('Count and choose', 'Count the pictures. Color the circle with the right number.', kd([4, 7, 2, 9, 6, 10]), 1, 10)
    b.count_match('Count and match', 'Count each group. Draw a line to its number.', kd([5, 3, 8, 1, 10]), layout='rows5')
    b.frame_read('How many dots?', 'Count the dots in each ten frame. Write the number.', [3, 5, 8, 6, 10, 7], 2, 3)
    b.frame_fill('Fill the ten frame', 'Read the number. Draw that many dots in the frame. Start at the top left.', [2, 4, 7, 5, 9, 6], 2, 3)
    b.draw_page('Draw and count', 'Read the number. Draw that many shapes in the box.', [(3, 'circles'), (5, 'lines'), (2, 'squares'), (7, 'dots'), (4, 'triangles'), (10, 'circles')])
    b.seq_page('Missing numbers', 'Some numbers are missing. Count along each row and write them in.',
               [(list(range(1, 11)), {2, 5, 8}), (list(range(1, 11)), {1, 3, 6, 9}), (list(range(1, 11)), {0, 4, 7}), (list(range(1, 11)), {2, 3, 6, 7, 9}), (list(range(1, 11)), {1, 2, 4, 5, 7, 8})])
    b.neighbors('Before and after', 'Which number comes just before? Which comes just after? Write it in the empty box.',
                [(3, 'after'), (6, 'after'), (5, 'before'), (9, 'before'), (2, 'both'), (7, 'both'), (4, 'between'), (8, 'between')])
    b.more_page('Which group has more?', 'Count both groups. Circle the group that has more.', [(5, 'star', 3, 'apple'), (4, 'car', 7, 'balloon'), (9, 'leaf', 6, 'heart'), (8, 'flower', 10, 'ball')])
    b.more_page('Which group has fewer?', 'Count both groups. Circle the group that has fewer.', [(2, 'boat', 4, 'kite'), (6, 'tree', 5, 'house'), (7, 'cupcake', 9, 'star'), (10, 'apple', 8, 'umbrella')], ask='fewer')
    b.words_page('Number words', 'Draw a line from each number to its word.', [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    b.dots_page('Dot to dot: 1 to 10', 'Start at the red dot. Join the dots in order from 1 to 10, then back to 1.', STAR10, 'A star', star_extra)

    # numbers 11 to 20 ------------------------------------------------------
    b.start('Numbers 11 to 20', MUST)
    b.chart_page('Numbers 11 to 20 at a glance', 'Each of these numbers is one full ten and some more. Read each row out loud.', list(range(11, 21)))
    first = b.n; b.finds = []
    for n, kind in zip(range(11, 21), ['cupcake', 'house', 'tree', 'umbrella', 'heart', 'star', 'apple', 'balloon', 'car', 'flower']):
        b.number_page(n, kind, RINGS[(n - 1) % 5])
    b.ans('plain', ['%d: 10 and %d, circle %d' % (f['n'], f['n'] - 10, f['count']) for f in b.finds], note={'finds': b.finds[:]}, page='%d to %d' % (first, b.n - 1),
          title='Number pages 11 to 20: the missing number, and how many to circle')

    # count to 20 -----------------------------------------------------------
    b.start('Count to 20', NAVY)
    b.count_write('Count and write', 'The pictures are in rows of five. Count them and write the number.', kd([12, 15, 11, 18, 14, 20]), 2, 3, layout='rows5')
    b.count_write('Count and write', 'Count carefully. Cross out each picture as you count it.', kd([13, 17, 19, 16, 11, 15]), 2, 3, layout='rows5')
    b.choose_count('Count and choose', 'Count the pictures. Color the circle with the right number.', kd([14, 12, 19, 16, 13, 20]), 11, 20, layout='rows5')
    b.count_match('Count and match', 'Count each group. Draw a line to its number.', kd([15, 11, 18, 13, 20]), layout='rows10')
    b.frame_read('How many dots?', 'The top frame is full, so it is ten. Count on from ten and write the number.', [13, 11, 16, 19, 14, 20], 2, 3, double=True)
    b.frame_fill('Fill the ten frames', 'Read the number. Fill the top frame first, then draw the extra dots below.', [12, 15, 17, 11, 18, 14], 2, 3, double=True)
    b.ten_more('Ten and some more', 'Count the dots in the bottom frame. Fill in both boxes.', [14, 11, 17, 13, 19, 16])
    b.seq_page('Missing numbers', 'Count along each row and write in the missing numbers.',
               [(list(range(1, 11)), {3, 7}), (list(range(11, 21)), {1, 4, 8}), (list(range(11, 21)), {0, 2, 5, 9}), (list(range(6, 16)), {2, 5, 6, 8}), (list(range(11, 21)), {1, 2, 4, 6, 7, 9})])
    b.neighbors('Before, after and between', 'Write the number that belongs in each empty box.',
                [(12, 'after'), (17, 'after'), (15, 'before'), (20, 'before'), (11, 'both'), (18, 'both'), (14, 'between'), (16, 'between')])
    b.compare_page('Which number is bigger?', 'Look at the two numbers. Circle the bigger one.',
                   [(12, 15), (9, 6), (17, 14), (11, 19), (20, 13), (8, 18), (16, 10), (15, 17), (13, 12), (7, 11), (19, 20), (14, 4)])
    b.compare_page('Which number is smaller?', 'Look at the two numbers. Circle the smaller one.',
                   [(14, 11), (5, 8), (18, 20), (13, 16), (10, 7), (19, 12), (15, 13), (6, 16), (17, 18), (20, 9), (11, 12), (3, 14)], ask='smaller')
    b.order_page('Smallest to biggest', 'Write each set of numbers again in order, from the smallest to the biggest.',
                 [(7, 3, 9, 5), (12, 10, 15, 13), (18, 14, 11, 16), (20, 8, 17, 12), (19, 6, 13, 2)])
    b.words_page('Number words', 'Draw a line from each number to its word.', [[11, 12, 13, 14, 15], [16, 17, 18, 19, 20]])

    # number fun -------------------------------------------------------------
    b.start('Number fun', SAGE)
    b.dots_page('Dot to dot: 1 to 20', 'Start at the red dot. Join the dots in order from 1 to 20, then back to 1.', ROCKET, 'A rocket', rocket_extra)
    b.maze_page('Number path', 'Start at 1. Move up, down, left or right to the next number each time. Color the path all the way to 20.', 5, 6, 20)
    b.quilt_page('Color by number', 'Look at the number in each shape. Use the key to pick the color.')
    b.spy_page('Count the picture', 'How many of each thing can you find? Count them and write the numbers below.',
               [(7, 'star'), (4, 'balloon'), (9, 'apple'), (5, 'car'), (12, 'leaf'), (3, 'kite')])
    b.seq_page('Count backwards', 'These rows count down. Write in the missing numbers. Then say each row like a rocket launch.',
               [(list(range(10, 0, -1)), {2, 5, 8}), (list(range(10, 0, -1)), {1, 3, 4, 7, 9}), (list(range(20, 10, -1)), {2, 6}), (list(range(20, 10, -1)), {1, 3, 5, 8}), (list(range(15, 5, -1)), {2, 4, 5, 7, 9})],
               note='backwards')
    b.seq_page('Count on', 'Start at the first number and keep counting. Write the next numbers.',
               [(list(range(4, 10)), {2, 3, 4, 5}), (list(range(8, 14)), {2, 3, 4, 5}), (list(range(11, 17)), {2, 3, 4, 5}), (list(range(15, 21)), {1, 2, 3, 4, 5}), (list(range(13, 19)), {1, 2, 3, 4, 5})],
               note='counton')

    # review -----------------------------------------------------------------
    b.start('Show what you know', CORAL)
    b.count_write('Mixed review: count and write', 'Count each group and write the number.', kd([8, 13, 6, 17, 10, 20]), 2, 3, layout='rows5')
    b.frame_read('Mixed review: ten frames', 'Write the number that each pair of ten frames shows.', [9, 12, 20, 7, 15, 18], 2, 3, double=True)
    b.seq_page('Mixed review: 1 to 20', 'Fill in every missing number from 1 to 20.',
               [(list(range(1, 11)), {1, 4, 6, 8}), (list(range(11, 21)), {0, 3, 5, 7, 9}), (list(range(1, 11)), {0, 2, 3, 5, 7, 9}), (list(range(11, 21)), {1, 2, 4, 6, 8, 9})])
    # certificate
    c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(NAVY); c.setLineWidth(2.2); c.roundRect(30, 30, W - 60, H - 60, 18, stroke=1, fill=0)
    c.setStrokeColor(CORAL); c.setLineWidth(0.9); c.roundRect(40, 40, W - 80, H - 80, 12, stroke=1, fill=0)
    for x, y, r, col in [(0.16, 0.86, 10, MUST), (0.84, 0.86, 10, MUST), (0.16, 0.14, 8, TEAL), (0.84, 0.14, 8, CORAL)]:
        b.icon('star', W * x, H * y, r * 2, col)
    b.text(W / 2, H - 122, 'CERTIFICATE', 'InB', 12, TEAL, 'c')
    b.text(W / 2, H - 176, 'I can count to 20!', 'FrM', 40, INK, 'c')
    ts = W * 0.2
    for k, (n, col) in enumerate([(10, TEAL), (20, CORAL)]): b.tile(W / 2 + (k - 0.5) * (ts + 16), H * 0.585, ts, n, col)
    for kind, x, col in [('balloon', 0.2, MUST), ('rocket', 0.8, NAVY)]: b.icon(kind, W * x, H * 0.585, 46, col)
    y = H * 0.585 - ts / 2 - 60
    b.text(W / 2, y, 'This certificate goes to', 'FrI', 17, SOFT, 'c')
    b.hl(W * 0.24, W * 0.76, y - 54, col=INK, w=1)
    b.text(W / 2, y - 84, 'for learning to count, read and write the numbers 1 to 20.', 'In', 12, INK, 'c', maxw=W - 110)
    b.hl(W * 0.18, W * 0.44, 96, col=INK, w=0.8); b.text(W * 0.31, 80, 'Date', 'InM', 9.5, SOFT, 'c')
    b.hl(W * 0.56, W * 0.82, 96, col=INK, w=0.8); b.text(W * 0.69, 80, 'Signed', 'InM', 9.5, SOFT, 'c')
    c.showPage(); b.n += 1

    # answer key -------------------------------------------------------------
    b.start('Answer key', NAVY)
    entries = [e for e in b.key if e['kind'] != 'shown']
    def khead():
        return b.head('Answer key', 'Answers are listed in the same order as the numbers on each page.', name=False) - 4
    y = khead(); bot = M + 22
    for e in entries:
        single = len(e['data']) == 1
        items = [a if single or e['kind'] == 'plain' else '%d.  %s' % (i + 1, a) for i, a in enumerate(e['data'])]
        lines = []; line = ''
        for it in items:
            tline = (line + '      ' + it) if line else it
            if sw(tline, 'In', 10.5) > b.w - 12: lines.append(line); line = it
            else: line = tline
        if line: lines.append(line)
        need = 22 + len(lines) * 16 + 2
        if y - need < bot:
            b.foot(); y = khead()
        lab = 'Page %s' % e['page'] if isinstance(e['page'], int) else 'Pages %s' % e['page']
        lw_ = sw(lab, 'InB', 8.5) + 18
        b.rbox(M, y - 15, lw_, 17, r=8.5, col=None, fill=TINT); b.text(M + lw_ / 2, y - 10.8, lab, 'InB', 8.5, INK, 'c')
        b.text(M + lw_ + 10, y - 11, e['title'], 'InM', 10.5, INK, maxw=b.w - lw_ - 10)
        yy = y - 24
        for ln in lines:
            yy -= 12; b.text(M + 6, yy, ln, 'In', 10.5, INK, maxw=b.w - 6); yy -= 4
        y -= need + 6
        b.hl(M, W - M, y + 4, col=HAIR, w=0.6)
    if y - bot > 106:
        bh = 96; by = bot + 2
        b.rbox(M, by, b.w, bh, r=14, col=None, fill=TINT)
        b.icon('star', M + 38, by + bh / 2, 30, MUST); b.icon('star', M + 62, by + bh / 2 + 22, 14, CORAL); b.icon('star', M + 60, by + bh / 2 - 24, 12, TEAL)
        b.text(M + 92, by + bh - 40, 'Well done, number expert!', 'FrM', 20, INK)
        b.text(M + 92, by + bh - 62, 'Keep counting the things around you: stairs, spoons, cars, trees.', 'In', 10.5, SOFT, maxw=b.w - 104)
        b.text(M + 92, by + bh - 80, 'More printables at inkwellandco.gumroad.com', 'InM', 10.5, CORAL)
    b.foot()
    c.save()
    return b


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    for size, tag, fn in [(letter, 'US Letter', 'Numbers_1_to_20_Worksheets_US_Letter.pdf'), (A4, 'A4', 'Numbers_1_to_20_Worksheets_A4.pdf')]:
        b = build(OUT + fn, size, tag)                                  # pass 1 collects page numbers
        toc = dict(b.seen); toc['_pages'] = b.n - 1
        WARN[:] = []
        b = build(OUT + fn, size, tag, toc=toc)
        print(tag, 'pages', b.n - 1, 'sections', b.seen)
        json.dump({'key': b.key, 'marks': b.man, 'pages': b.n - 1}, open(OUT + fn.replace('.pdf', '.json'), 'w'), indent=1)
    for w_ in WARN: print('WARN', w_)
    print('WARNINGS', len(WARN))
