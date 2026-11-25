# Telling Time Worksheets: kids worksheet bundle (rotation C).
# Builds US Letter and A4 PDFs into /home/claude/book/out/time/ and a manifest JSON
# (every clock drawn with hands, every answer) that verify_telling_time.py checks.
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
RINGS = [CORAL, TEAL, MUST, NAVY, SAGE]
NAME = 'Telling Time Worksheets'
OUT = '/home/claude/book/out/time/'
WARN = []
sw = pdfmetrics.stringWidth


def fmt(h, m): return '%d:%02d' % (h, m)
def nxt(h): return h % 12 + 1
def prv(h): return (h - 2) % 12 + 1


def words(h, m):
    if m == 0: return "%d o'clock" % h
    if m == 30: return 'half past %d' % h
    if m == 15: return 'quarter past %d' % h
    if m == 45: return 'quarter to %d' % nxt(h)
    return fmt(h, m)


def add(h, m, mins):
    t = ((h % 12) * 60 + m + mins) % 720
    hh = t // 60
    return (12 if hh == 0 else hh), t % 60


def dur(mins):
    h, m = divmod(mins, 60); p = []
    if h: p.append('%d hour%s' % (h, '' if h == 1 else 's'))
    if m: p.append('%d minutes' % m)
    return ' '.join(p)


class Book:
    def __init__(self, path, size, tag, toc=None):
        self.c = canvas.Canvas(path, pagesize=size)
        self.W, self.H = size; self.m = 46; self.w = self.W - 2 * self.m
        self.tag = tag; self.toc = toc or []; self.seen = []
        self.n = 1; self.sec = ''; self.ac = CORAL; self.title = ''
        self.key = []; self.man = []; self.rng = random.Random(2026)
        self.c.setTitle(NAME + ' (' + tag + ')'); self.c.setAuthor('Inkwell and Co')
        self.c.setSubject('Printable telling time worksheets for kids. For personal use.')

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

    # decoration (objects only) -----------------------------------------
    def star(self, cx, cy, r, col):
        c = self.c; p = c.beginPath()
        for i in range(10):
            a = math.radians(90 + i * 36); rr = r if i % 2 == 0 else r * 0.45
            (p.moveTo if i == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
        p.close(); c.setFillColor(col); c.drawPath(p, stroke=0, fill=1)

    def sun(self, cx, cy, r, col=MUST):
        c = self.c; c.setFillColor(col); c.circle(cx, cy, r * 0.56, stroke=0, fill=1)
        c.setStrokeColor(col); c.setLineWidth(r * 0.13); c.setLineCap(1)
        for i in range(10):
            a = math.radians(i * 36)
            c.line(cx + r * 0.74 * math.cos(a), cy + r * 0.74 * math.sin(a), cx + r * math.cos(a), cy + r * math.sin(a))
        c.setLineCap(0)

    def moon(self, cx, cy, r, col=NAVY, bg=WHITE):
        c = self.c; c.setFillColor(col); c.circle(cx, cy, r, stroke=0, fill=1)
        c.setFillColor(bg); c.circle(cx + r * 0.42, cy + r * 0.22, r * 0.84, stroke=0, fill=1)

    def cloud(self, cx, cy, r, col=HAIR):
        c = self.c; c.setFillColor(col)
        for dx, dy, k in [(-0.9, 0, 0.55), (-0.2, 0.3, 0.75), (0.6, 0.12, 0.6)]:
            c.circle(cx + dx * r, cy + dy * r, k * r, stroke=0, fill=1)
        c.roundRect(cx - 1.45 * r, cy - 0.55 * r, 2.65 * r, 0.62 * r, 0.3 * r, stroke=0, fill=1)

    # clock -------------------------------------------------------------
    def clock(self, cx, cy, r, h=None, m=None, ring=None, minticks=True, hide=(), rec=None, face=WHITE, big=False):
        c = self.c; ring = ring or self.ac
        c.setFillColor(ring); c.circle(cx, cy, r, stroke=0, fill=1)
        c.setFillColor(face); c.circle(cx, cy, r * 0.885, stroke=0, fill=1)
        c.setStrokeColor(INK); c.setLineCap(1)
        for i in range(60):
            a = math.radians(90 - i * 6); hr = i % 5 == 0
            if not hr and not minticks: continue
            r1 = r * (0.795 if hr else 0.822); c.setLineWidth(r * (0.026 if hr else 0.011))
            c.setStrokeColor(INK if hr else SOFT)
            c.line(cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + r * 0.85 * math.cos(a), cy + r * 0.85 * math.sin(a))
        if h is not None:
            ha = (h % 12) * 30 + m * 0.5; ma = m * 6.0
            a = math.radians(90 - ma); c.setStrokeColor(CORAL); c.setLineWidth(max(0.7, r * 0.016))
            c.line(cx, cy, cx + r * 0.80 * math.cos(a), cy + r * 0.80 * math.sin(a))
            for ang, ln, wd, col in [(ma, 0.52, 0.05, CORAL), (ha, 0.36, 0.08, NAVY)]:
                a = math.radians(90 - ang); c.setStrokeColor(col); c.setLineWidth(r * wd)
                c.line(cx - r * 0.08 * math.cos(a), cy - r * 0.08 * math.sin(a), cx + r * ln * math.cos(a), cy + r * ln * math.sin(a))
            if rec is not None: self.man.append({'page': self.n, 'item': rec, 'hour_angle': ha, 'minute_angle': ma})
        fs = r * 0.20
        for k in range(1, 13):
            a = math.radians(90 - k * 30); x = cx + r * 0.675 * math.cos(a); y = cy + r * 0.675 * math.sin(a)
            if k in hide:
                c.setStrokeColor(LINE); c.setLineWidth(0.8); c.setDash(2, 2); c.circle(x, y, r * 0.105, stroke=1, fill=0); c.setDash()
            else:
                self.text(x, y - fs * 0.36, str(k), 'InB', fs, INK, 'c')
        c.setLineCap(0)
        c.setFillColor(INK); c.circle(cx, cy, r * 0.06, stroke=0, fill=1)
        c.setFillColor(WHITE); c.circle(cx, cy, r * 0.02, stroke=0, fill=1)

    def wbox(self, cx, y, w=92, h=32):
        """Blank box for writing a time, with a printed colon."""
        self.rbox(cx - w / 2, y, w, h, r=8, col=INK, lw=1.1)
        self.text(cx, y + h * 0.27, ':', 'InB', h * 0.6, LINE, 'c')

    def dig(self, cx, y, s, w=92, h=32, font='InB', size=None, fill=TINT):
        size = size or h * 0.56
        self.rbox(cx - w / 2, y, w, h, r=8, col=None, fill=fill)
        self.text(cx, y + h / 2 - size * 0.36, s, font, size, INK, 'c', maxw=w - 10)

    # page frame ---------------------------------------------------------
    def start(self, sec, col):
        self.sec = sec; self.ac = col

    def head(self, title, instr, name=True, toc=False):
        c = self.c; m = self.m; y = self.H - m
        self.title = title
        if toc or self.sec not in [s for s, _ in self.seen]:
            if self.sec not in [s for s, _ in self.seen]: self.seen.append((self.sec, self.n))
        lab = self.sec.upper(); lw = sw(lab, 'InB', 7.6) + 0.9 * (len(lab) - 1)
        self.rbox(m, y - 17, lw + 22, 17, r=8.5, col=None, fill=self.ac)
        t = c.beginText(m + 11, y - 11.6); t.setFont('InB', 7.6); t.setFillColor(WHITE); t.setCharSpace(0.9); t.textOut(lab); t.setCharSpace(0); c.drawText(t)
        if name:
            self.text(self.W - m - 168, y - 13, 'Name', 'InM', 9.5, SOFT)
            self.hl(self.W - m - 136, self.W - m, y - 15, col=INK, w=0.8)
        self.text(m - 1, y - 50, title, 'FrM', 25, INK, maxw=self.w)
        yy = self.para(m, y - 70, self.w, instr, 'In', 11.5, 16, SOFT)
        return min(yy - 2, y - 92)

    def foot(self):
        m = self.m; y = m - 14
        self.hl(m, self.W - m, y + 16, col=HAIR, w=0.6)
        self.text(m, y, NAME, 'InM', 7.5, SOFT)
        self.text(self.W - m, y, 'Inkwell and Co   |   For personal use', 'In', 7.5, SOFT, 'r')
        self.text(self.W / 2, y, str(self.n), 'InB', 8.5, INK, 'c')
        self.c.showPage(); self.n += 1

    def area(self, top): return top, self.m + 14

    def ans(self, kind, data, note=None):
        self.key.append({'page': self.n, 'title': self.title, 'kind': kind, 'data': data, 'note': note})

    def cells(self, top, cols, rows):
        top, bot = self.area(top); cw = self.w / cols; ch = (top - bot) / rows
        return [(self.m + (i % cols) * cw, top - (i // cols) * ch, cw, ch) for i in range(cols * rows)]

    # worksheet types ----------------------------------------------------
    def read_page(self, title, instr, times, cols, rows, minticks=True, mode='digital'):
        top = self.head(title, instr)
        extra = 58
        for i, ((x, yt, cw, ch), (h, m)) in enumerate(zip(self.cells(top, cols, rows), times)):
            r = min(cw * 0.43, (ch - extra - 14) / 2); cx = x + cw / 2; yt -= (ch - 2 * r - extra - 8) * 0.5; cy = yt - 8 - r
            self.clock(cx, cy, r, h, m, ring=RINGS[i % 5], minticks=minticks, rec=i + 1)
            self.badge(x + cw / 2 - r - 2, yt - 14, i + 1, col=INK)
            if mode == 'digital': self.wbox(cx, cy - r - 46)
            else: self.hl(cx - cw * 0.40, cx + cw * 0.40, cy - r - 36, col=INK, w=0.9)
        self.ans('text', [fmt(h, m) if mode == 'digital' else words(h, m) for h, m in times], note={'read': mode})
        self.foot()

    def draw_page(self, title, instr, times, cols, rows, minticks=True, mode='digital'):
        top = self.head(title, instr)
        for i, ((x, yt, cw, ch), (h, m)) in enumerate(zip(self.cells(top, cols, rows), times)):
            r = min(cw * 0.43, (ch - 72) / 2); cx = x + cw / 2; yt -= (ch - 2 * r - 66) * 0.5; cy = yt - 8 - r
            self.clock(cx, cy, r, ring=RINGS[(i + 2) % 5], minticks=minticks)
            self.badge(x + cw / 2 - r - 2, yt - 14, i + 1, col=INK)
            if mode == 'digital': self.dig(cx, cy - r - 46, fmt(h, m))
            else: self.dig(cx, cy - r - 44, words(h, m), w=min(cw - 14, 150), h=28, font='InM', size=12.5)
        self.ans('clocks', [[h, m] for h, m in times], note=[fmt(h, m) for h, m in times])
        self.foot()

    def match_page(self, title, instr, times, mode='digital', minticks=True):
        top = self.head(title, instr); top, bot = self.area(top)
        n = len(times); rh = (top - bot) / n; r = min(rh * 0.43, 58)
        order = list(range(n))
        while any(order[i] == i for i in range(n)): self.rng.shuffle(order)
        xl = self.m + r + 30; xr = self.W - self.m - 100
        pairs = []
        for i, (h, m) in enumerate(times):
            cy = top - rh * (i + 0.5)
            self.badge(self.m + 10, cy, i + 1, col=INK)
            self.clock(xl + 8, cy, r, h, m, ring=RINGS[i % 5], minticks=minticks, rec=i + 1)
            self.c.setFillColor(INK); self.c.circle(xl + r + 30, cy, 3.2, stroke=0, fill=1)
            j = order[i]; hh, mm = times[j]; L = 'ABCDEFGH'[i]
            self.c.circle(xr - 96, cy, 3.2, stroke=0, fill=1)
            s = fmt(hh, mm) if mode == 'digital' else words(hh, mm)
            self.dig(xr + 2, cy - 19, s, w=150, h=38, font='InB' if mode == 'digital' else 'InM', size=20 if mode == 'digital' else 14.5)
            self.badge(self.W - self.m - 10, cy, L, col=self.ac)
            pairs.append((j, L, s))
        self.ans('text', ['%s (%s)' % (L, s) for _, L, s in sorted(pairs)], note={'match': mode, 'right': [s for _, _, s in pairs]})
        self.foot()

    def choose_page(self, title, instr, items, minticks=True):
        """items: [((h, m), [three option strings], index of the right one)]"""
        top = self.head(title, instr); res = []
        for i, ((x, yt, cw, ch), ((h, m), opts, good)) in enumerate(zip(self.cells(top, 3, 2), items)):
            r = min(cw * 0.42, (ch - 112) / 2); cx = x + cw / 2; yt -= (ch - 2 * r - 112) * 0.5; cy = yt - 8 - r
            self.clock(cx, cy, r, h, m, ring=RINGS[(i + 1) % 5], minticks=minticks, rec=i + 1)
            self.badge(cx - r - 2, yt - 14, i + 1, col=INK)
            y = cy - r - 36; bw = min(cw - 18, 144)
            for k, o in enumerate(opts):
                self.rbox(cx - bw / 2, y - 4, bw, 25, r=12.5, col=LINE, lw=0.9)
                self.c.setStrokeColor(INK); self.c.setLineWidth(1); self.c.circle(cx - bw / 2 + 14, y + 8.5, 5.5, stroke=1, fill=0)
                self.text(cx + 8, y + 4, o, 'InM', 12.5, INK, 'c', maxw=bw - 34)
                y -= 30
            res.append(opts[good])
        self.ans('text', res, note={'choose': [o for _, o, _ in items]})
        self.foot()

    def later_page(self, title, instr, times, delta, label):
        top = self.head(title, instr); res = []
        for i, ((x, yt, cw, ch), (h, m)) in enumerate(zip(self.cells(top, 2, 3), times)):
            r = min(ch * 0.38, 58); cx = x + r + 18; cy = yt - ch / 2
            self.rbox(x + 3, yt - ch + 6, cw - 6, ch - 12, r=14, col=HAIR, lw=1)
            self.clock(cx, cy, r, h, m, ring=RINGS[i % 5], rec=i + 1)
            self.badge(x + 19, yt - 23, i + 1, col=INK)
            zx = cx + r + 10; zw = x + cw - 12 - zx; mx = zx + zw / 2
            self.text(mx, cy + 34, label, 'InB', 10.5, self.ac, 'c', maxw=zw)
            c = self.c; c.setStrokeColor(self.ac); c.setLineWidth(1.8); c.setLineCap(1)
            c.line(mx - 26, cy + 20, mx + 26, cy + 20); c.line(mx + 26, cy + 20, mx + 19, cy + 25.5); c.line(mx + 26, cy + 20, mx + 19, cy + 14.5); c.setLineCap(0)
            self.wbox(mx, cy - 30, w=min(92, zw))
            res.append(fmt(*add(h, m, delta)))
        self.ans('text', res, note={'delta': delta, 'from': [fmt(h, m) for h, m in times]})
        self.foot()

    def order_page(self, title, instr, rowsets):
        top = self.head(title, instr); top, bot = self.area(top); rh = (top - bot) / len(rowsets); res = []
        for i, row in enumerate(rowsets):
            yt = top - i * rh; cw = (self.w - 30) / 4; r = min(cw * 0.39, (rh - 62) / 2)
            self.rbox(self.m, yt - rh + 8, self.w, rh - 14, r=14, col=HAIR, lw=1)
            self.badge(self.m + 18, yt - 22, i + 1, col=INK)
            rank = sorted(range(4), key=lambda k: row[k][0] % 12 * 60 + row[k][1])
            for k, (h, m) in enumerate(row):
                cx = self.m + 30 + cw * (k + 0.5); cy = yt - 16 - r
                self.clock(cx, cy, r, h, m, ring=RINGS[(i + k) % 5], rec='%d%s' % (i + 1, 'abcd'[k]))
                self.rbox(cx - 15, cy - r - 40, 30, 30, r=7, col=INK, lw=1.1)
            res.append(' '.join(str(rank.index(k) + 1) for k in range(4)))
        self.ans('text', res, note={'rows': [[fmt(h, m) for h, m in row] for row in rowsets]})
        self.foot()

    def elapsed_page(self, title, instr, pairs):
        top = self.head(title, instr); top, bot = self.area(top); rh = (top - bot) / len(pairs); res = []
        for i, ((h1, m1), mins) in enumerate(pairs):
            h2, m2 = add(h1, m1, mins)
            yt = top - i * rh; r = min((rh - 46) / 2, 54); cy = yt - 12 - r
            self.badge(self.m + 10, yt - 16, i + 1, col=INK)
            x1 = self.m + 30 + r; x2 = x1 + 2 * r + 62
            self.clock(x1, cy, r, h1, m1, ring=RINGS[i % 5], rec='%da' % (i + 1))
            self.clock(x2, cy, r, h2, m2, ring=RINGS[i % 5], rec='%db' % (i + 1))
            self.text(x1, cy - r - 17, 'Start', 'InM', 10, SOFT, 'c'); self.text(x2, cy - r - 17, 'End', 'InM', 10, SOFT, 'c')
            c = self.c; c.setStrokeColor(self.ac); c.setLineWidth(1.6); c.setLineCap(1)
            a, b = x1 + r + 10, x2 - r - 10
            c.line(a, cy, b, cy); c.line(b, cy, b - 7, cy + 5); c.line(b, cy, b - 7, cy - 5); c.setLineCap(0)
            x = x2 + r + 22; wd = self.W - self.m - x
            self.text(x, cy + 24, 'How much time passed?', 'InM', 11.5, INK, maxw=wd)
            self.hl(x, x + 36, cy - 12, col=INK, w=0.9); self.text(x + 41, cy - 10, 'hours', 'In', 11, SOFT)
            self.hl(x + 78, x + 114, cy - 12, col=INK, w=0.9); self.text(x + 119, cy - 10, 'minutes', 'In', 11, SOFT, maxw=wd - 119)
            res.append(dur(mins))
        self.ans('text', res, note={'pairs': [[fmt(h, m), fmt(*add(h, m, d)), d] for (h, m), d in pairs]})
        self.foot()

    def learn_page(self, title, instr, big, points, examples, minticks=True, cap=None):
        top = self.head(title, instr, name=False); top, bot = self.area(top)
        r = self.w * 0.215; cx = self.m + r + 6; cy = top - r - 14
        self.clock(cx, cy, r, big[0], big[1], minticks=minticks, rec='big')
        self.dig(cx, cy - r - 52, cap or fmt(*big), w=150, h=38, size=20 if not cap else 15)
        x = cx + r + 34; y = top - 26; wd = self.W - self.m - x
        for k, p in enumerate(points):
            self.badge(x + 10, y + 4, k + 1, col=self.ac, r=10)
            y = self.para(x + 30, y, wd - 30, p, 'In', 12.5, 18.5, INK) - 12
        ey = cy - r - 82
        self.hl(self.m, self.W - self.m, ey, col=HAIR, w=1)
        self.text(self.m, ey - 24, 'More examples', 'FrM', 15, INK)
        n = len(examples); cw = self.w / n; rr = min(cw * 0.36, (ey - 96 - bot) / 2)
        for k, (h, m) in enumerate(examples):
            ex = self.m + cw * (k + 0.5); ecy = ey - 44 - rr
            self.clock(ex, ecy, rr, h, m, ring=RINGS[(k + 1) % 5], minticks=minticks, rec='ex%d' % (k + 1))
            self.text(ex, ecy - rr - 22, fmt(h, m), 'InB', 15, INK, 'c')
            if words(h, m) != fmt(h, m): self.text(ex, ecy - rr - 38, words(h, m), 'In', 10.5, SOFT, 'c', maxw=cw - 6)
        self.ans('shown', [fmt(*big)] + [fmt(h, m) for h, m in examples])
        self.foot()


# ---------------------------------------------------------------- content
def pick(rng, pool, n):
    return rng.sample(pool, n)


def wrongs(rng, h, m, level):
    """Two tempting wrong answers that stay inside what the section has taught."""
    if level == 'hour': cand = [(nxt(h), 0), (prv(h), 0)] if rng.random() < 0.5 else [(prv(h), 0), (nxt(nxt(h)), 0)]
    elif level == 'half': cand = [(nxt(h), m), (h, 30 - m), (prv(h), m)]
    else:
        sh = 12 if m == 0 else max(1, round(m / 5)); smn = (h % 12) * 5
        cand = [(sh, smn), (nxt(h), m), (prv(h), m), (h, (m + 30) % 60)]
    out = []
    for cnd in cand:
        if cnd != (h, m) and cnd not in out: out.append(cnd)
    return out[:2]


def choose_digital(rng, times, level='five'):
    items = []
    for h, m in times:
        opts = [(h, m)] + wrongs(rng, h, m, level); rng.shuffle(opts)
        items.append(((h, m), [fmt(*o) for o in opts], opts.index((h, m))))
    return items


def choose_words(rng, times):
    items = []
    for h, m in times:
        good = words(h, m)
        pool = [words(h, 15), words(h, 45), words(h, 30), words(prv(h), 45), words(nxt(h), 15), words(h, 0), words(nxt(h), 0)]
        pool = [p for p in dict.fromkeys(pool) if p != good]
        opts = [good] + pool[:2]; rng.shuffle(opts)
        items.append(((h, m), opts, opts.index(good)))
    return items


def build(path, size, tag, toc=None):
    b = Book(path, size, tag, toc); c = b.c; W, H, M = b.W, b.H, b.m; rng = b.rng
    HRS = list(range(1, 13))

    # 1 cover ------------------------------------------------------------
    c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)
    b.sun(W - 104, H - 112, 46); b.cloud(120, H - 120, 30, WHITE); b.cloud(W - 150, H * 0.56, 22, WHITE)
    b.moon(92, H * 0.47, 24, NAVY, CREAM)
    for x, y, r, col in [(0.2, 0.60, 9, MUST), (0.84, 0.44, 11, CORAL), (0.13, 0.36, 7, TEAL), (0.9, 0.67, 7, SAGE), (0.76, 0.33, 6, MUST), (0.27, 0.42, 5, CORAL)]:
        b.star(W * x, H * y, r, col)
    b.clock(W / 2, H * 0.535, W * 0.235, 10, 10, ring=CORAL)
    b.text(W / 2, H - 150, 'PRINTABLE WORKSHEETS', 'InB', 11, TEAL, 'c')
    b.text(W / 2, H - 208, 'Telling Time', 'FrM', 58, INK, 'c')
    b.text(W / 2, H * 0.535 - W * 0.235 - 58, "From o'clock to the minute", 'FrI', 25, CORAL, 'c')
    COVER_Y = H * 0.535 - W * 0.235 - 96
    tw = 0; chips = ['Ages 5 to 8', '%d pages', 'Answer key inside']
    b._chips = (chips, COVER_Y)
    b.text(W / 2, 52, 'Inkwell and Co', 'FrM', 13, INK, 'c')
    total = toc[-1][1] if toc else 0
    labs = [chips[0], '%d pages' % total, chips[2]]; ws = [sw(s, 'InB', 11) + 30 for s in labs]; x = W / 2 - (sum(ws) + 20) / 2
    for s, w_, col in zip(labs, ws, [TEAL, NAVY, CORAL]):
        b.rbox(x, COVER_Y - 8, w_, 27, r=13.5, col=None, fill=col); b.text(x + w_ / 2, COVER_Y + 1.5, s, 'InB', 11, WHITE, 'c'); x += w_ + 10
    c.showPage(); b.n += 1

    # 2 for grown ups + contents ----------------------------------------------
    b.start('Start here', NAVY)
    top = b.head('For the grown ups', 'A quick guide to getting the most out of these pages.', name=False)
    y = top - 6; colw = b.w * 0.54
    tips = [('Go in order.', 'Each part builds on the one before it. Start with the hour, then half past, quarters, five minutes and single minutes.'),
            ('Short and often.', 'One or two pages a day is plenty. Stop while it is still fun.'),
            ('Build the practice clock.', 'Page %d has a clock to cut out. Moving real hands makes every other page easier.' % dict(toc or []).get('_cut', 0)),
            ('Say it out loud.', 'Ask for the time in two ways: "three thirty" and "half past three".'),
            ('Check together.', 'The answer key starts on page %d. Let children mark their own work.' % dict(toc or []).get('Answer key', 0)),
            ('Print again.', 'Print any page as many times as you like for your own family or class.')]
    for k, (hd, tx) in enumerate(tips):
        b.badge(M + 11, y - 5, k + 1, col=RINGS[k % 5], r=11)
        b.text(M + 34, y - 9, hd, 'InB', 13, INK)
        y = b.para(M + 34, y - 28, colw - 46, tx, 'In', 11.5, 17, SOFT) - 20
    x = M + colw + 10; wd = b.w - colw - 10; yy = top - 2
    b.rbox(x, M + 30, wd, yy - M - 30, r=14, col=None, fill=TINT)
    b.text(x + 18, yy - 32, "What's inside", 'FrM', 17, INK)
    ty = yy - 62
    for s_, p in [t for t in (toc or []) if not t[0].startswith('_') and t[0] != 'Start here']:
        b.text(x + 18, ty, s_, 'InM', 11.5, INK, maxw=wd - 60); b.text(x + wd - 18, ty, str(p), 'InB', 11.5, CORAL, 'r')
        b.hl(x + 18, x + wd - 18, ty - 9, col=LINE, w=0.5, dash=(1, 2)); ty -= 29
    ty -= 18
    b.text(x + 18, ty, 'You will need', 'FrM', 17, INK); ty -= 28
    for it in ['A pencil and an eraser', 'Scissors and glue', 'Thin card', 'One paper fastener', 'Red and blue pencils']:
        c.setFillColor(CORAL); c.circle(x + 22, ty + 3.5, 2.6, stroke=0, fill=1)
        b.text(x + 34, ty, it, 'In', 11.5, INK, maxw=wd - 50); ty -= 22
    b.text(x + 18, M + 66, 'Hour hand: short and blue.', 'InM', 10, NAVY, maxw=wd - 30)
    b.text(x + 18, M + 50, 'Minute hand: long and red.', 'InM', 10, CORAL, maxw=wd - 30)
    b.foot()

    # 3 meet the clock -----------------------------------------------------
    b.start('Meet the clock', CORAL)
    top = b.head('The parts of a clock', 'Read the labels. Then point to each part and say its name.')
    top, bot = b.area(top); r = b.w * 0.235; cx = W / 2; cy = top - r - 26
    b.clock(cx, cy, r, 5, 0, minticks=True, rec='big')
    def lab(side, px, py, s1, s2, col):
        al = 'l' if side < 0 else 'r'; x0 = M if side < 0 else W - M; ly = py - 4
        w1 = b.text(x0, ly, s1, 'InB', 13, col, al); b.text(x0, ly - 16, s2, 'In', 10.5, SOFT, al)
        sx = x0 + (w1 + 8) * (1 if side < 0 else -1)
        c.setStrokeColor(col); c.setLineWidth(1.2); c.line(sx, py, px, py); c.setFillColor(col); c.circle(px, py, 3.2, stroke=0, fill=1)
    lab(-1, cx - 1, cy + r * 0.18, 'Minute hand', 'Long. It shows minutes.', CORAL)
    lab(-1, cx - r * 0.80, cy - r * 0.50, 'Clock face', 'The round front.', TEAL)
    lab(1, cx + r * 0.68, cy + r * 0.34, 'Numbers', '1 to 12 show the hours.', INK)
    lab(1, cx + r * 0.13, cy - r * 0.21, 'Hour hand', 'Short. It shows the hour.', NAVY)
    yb = cy - r + 12
    y = yb - 46; b.hl(M, W - M, y, col=HAIR, w=1); y -= 34
    b.text(M, y, 'Finish the sentences', 'FrM', 17, INK); y -= 38
    for k, (s1, s2) in enumerate([('The short hand is the', 'hand.'), ('The long hand is the', 'hand.'), ('A clock has the numbers 1 to', '.')]):
        b.badge(M + 10, y + 4, k + 1, col=INK)
        w1 = b.text(M + 30, y, s1, 'In', 14, INK); b.hl(M + 36 + w1, M + 36 + w1 + 120, y - 2, col=INK, w=0.9)
        b.text(M + 42 + w1 + 120, y, s2, 'In', 14, INK); y -= 40
    b.ans('text', ['hour', 'minute', '12'])
    b.foot()

    top = b.head('Fill in the missing numbers', 'Some numbers have fallen off these clocks. Write them back in the circles.')
    hides = [(3, 6, 9, 12), (1, 4, 7, 10, 11), (2, 5, 6, 8, 9, 12), (1, 2, 3, 5, 7, 8, 10, 11)]
    for i, ((x, yt, cw, ch), hd) in enumerate(zip(b.cells(top, 2, 2), hides)):
        r = min(cw * 0.42, (ch - 24) / 2); b.clock(x + cw / 2, yt - ch / 2, r, ring=RINGS[i], hide=hd, minticks=False)
        b.badge(x + cw / 2 - r - 2, yt - ch / 2 + r - 6, i + 1, col=INK)
    b.ans('text', [', '.join(str(k) for k in hd) for hd in hides])
    b.foot()

    t = [(h, 0) for h in pick(rng, HRS, 6)]
    top = b.head('Find the hour hand', 'The short blue hand is the hour hand. Which number does it point to? Write it in the box.')
    for i, ((x, yt, cw, ch), (h, m)) in enumerate(zip(b.cells(top, 3, 2), t)):
        r = min(cw * 0.43, (ch - 72) / 2); cx = x + cw / 2; yt -= (ch - 2 * r - 66) * 0.5; cy = yt - 8 - r
        b.clock(cx, cy, r, h, m, ring=RINGS[i % 5], minticks=False, rec=i + 1); b.badge(cx - r - 2, yt - 14, i + 1, col=INK)
        b.rbox(cx - 22, cy - r - 48, 44, 34, r=8, col=INK, lw=1.1)
    b.ans('text', [str(h) for h, m in t], note='hour')
    b.foot()

    top = b.head('Count by fives', 'Each number on the clock is 5 more minutes. Start at 12 and count by fives. Write the minutes in the boxes.')
    top, bot = b.area(top); r = min(b.w * 0.33, (top - bot) * 0.36); cx = W / 2; cy = (top + bot) / 2 + 4
    b.clock(cx, cy, r, ring=TEAL, minticks=True)
    for k in range(1, 13):
        a = math.radians(90 - k * 30); x = cx + r * 1.27 * math.cos(a); y = cy + r * 1.27 * math.sin(a)
        pre = {12: '0', 1: '5', 2: '10'}.get(k)
        b.rbox(x - 21, y - 14, 42, 28, r=7, col=INK if not pre else None, lw=1.1, fill=TINT if pre else None)
        if pre: b.text(x, y - 5.5, pre, 'InB', 15, INK, 'c')
    b.ans('text', [str(k * 5) for k in range(3, 12)], note='fives')
    b.foot()

    b.seen.append(('_cut', b.n))
    top = b.head('Make your own clock', 'Glue this page onto thin card. Cut out the clock and the two hands. Ask a grown up to join the hands to the middle with a paper fastener.', name=False)
    top, bot = b.area(top); r = min(b.w * 0.40, (top - bot - 96) / 2); cx = W / 2; cy = top - r - 6
    c.setStrokeColor(LINE); c.setLineWidth(0.9); c.setDash(4, 3); c.circle(cx, cy, r + 7, stroke=1, fill=0); c.setDash()
    b.clock(cx, cy, r, ring=CORAL, minticks=True)
    hy = bot + 26
    for x0, ln, wd, col, nm in [(M + 20, b.w * 0.36, 26, NAVY, 'Hour hand'), (M + b.w * 0.46, b.w * 0.50, 20, CORAL, 'Minute hand')]:
        p = c.beginPath(); p.moveTo(x0, hy - wd / 2); p.lineTo(x0 + ln - wd, hy - wd / 2); p.lineTo(x0 + ln, hy); p.lineTo(x0 + ln - wd, hy + wd / 2); p.lineTo(x0, hy + wd / 2)
        p.arcTo(x0 - wd / 2, hy - wd / 2, x0 + wd / 2, hy + wd / 2, 90, 180); p.close()
        c.setFillColor(col); c.drawPath(p, stroke=0, fill=1)
        c.setFillColor(WHITE); c.circle(x0 + 2, hy, 3.2, stroke=0, fill=1)
        b.text(x0 + ln / 2, hy - 3.5, nm, 'InB', 9.5, WHITE, 'c')
        c.setStrokeColor(LINE); c.setLineWidth(0.9); c.setDash(4, 3); c.roundRect(x0 - wd / 2 - 6, hy - wd / 2 - 6, ln + wd / 2 + 12, wd + 12, 8, stroke=1, fill=0); c.setDash()
    b.foot()

    # o'clock --------------------------------------------------------------
    b.start("O'clock", TEAL)
    b.learn_page("What does o'clock mean?", "When the long minute hand points straight up to 12, it is something o'clock.", (3, 0),
                 ['Look at the long red minute hand. It points to 12.', 'Look at the short blue hour hand. It points to 3.',
                  "So the time is 3 o'clock. We write it as 3:00."], [(7, 0), (10, 0), (12, 0)], minticks=False, cap="3 o'clock")
    for k in range(2):
        b.read_page('What time is it?', 'The minute hand is on 12. Find the hour hand and write the time.', [(h, 0) for h in pick(rng, HRS, 6)], 3, 2, minticks=False)
    b.read_page('Say it in words', "Write each time in words, like this: 4 o'clock.", [(h, 0) for h in pick(rng, HRS, 6)], 3, 2, minticks=False, mode='words')
    for k in range(2):
        b.draw_page('Draw the hands', 'Draw a long minute hand to the 12. Draw a short hour hand to the hour.', [(h, 0) for h in pick(rng, HRS, 6)], 3, 2, minticks=False)
    b.match_page('Match the clocks', 'Draw a line from each clock to the same time on the right.', [(h, 0) for h in pick(rng, HRS, 5)], minticks=False)
    b.choose_page('Pick the right time', 'Fill in the circle next to the time each clock shows.', choose_digital(rng, [(h, 0) for h in pick(rng, HRS, 6)], 'hour'), minticks=False)

    # half past ------------------------------------------------------------
    b.start('Half past', MUST)
    b.learn_page('What does half past mean?', 'When the minute hand points straight down to 6, it has gone half way round the clock.', (3, 30),
                 ['The long minute hand points to 6. That is 30 minutes.', 'The short hour hand is half way between 3 and 4. It has not reached 4 yet.',
                  'So the time is half past 3. We write it as 3:30.'], [(1, 30), (8, 30), (11, 30)], minticks=False, cap='half past 3')
    for k in range(2):
        b.read_page('What time is it?', 'The minute hand is on 6. Which hour did the short hand just pass? Write the time.', [(h, 30) for h in pick(rng, HRS, 6)], 3, 2, minticks=False)
    b.read_page('Say it in words', 'Write each time in words, like this: half past 4.', [(h, 30) for h in pick(rng, HRS, 6)], 3, 2, minticks=False, mode='words')
    for k in range(2):
        b.draw_page('Draw the hands', 'Draw the minute hand to the 6. Draw the hour hand half way to the next number.', [(h, 30) for h in pick(rng, HRS, 6)], 3, 2, minticks=False)
    mix = [(h, m) for h, m in zip(pick(rng, HRS, 5), [0, 30, 30, 0, 30])]
    b.match_page('Match the clocks', "Draw a line from each clock to the same time. Watch out for o'clock and half past.", mix, minticks=False)
    mix = [(h, m) for h, m in zip(pick(rng, HRS, 6), [30, 0, 30, 30, 0, 30])]
    b.choose_page("O'clock or half past?", 'Fill in the circle next to the time each clock shows.', choose_digital(rng, mix, 'half'), minticks=False)

    # quarters -------------------------------------------------------------
    b.start('Quarter hours', SAGE)
    b.learn_page('Quarter past', 'A quarter is one of four equal parts. When the minute hand reaches 3, a quarter of an hour has passed.', (2, 15),
                 ['The minute hand points to 3. That is 15 minutes.', 'The hour hand has moved a little past 2.',
                  'So the time is quarter past 2. We write it as 2:15.'], [(5, 15), (9, 15), (12, 15)], cap='quarter past 2')
    b.learn_page('Quarter to', 'When the minute hand reaches 9, there is one quarter of an hour left before the next hour.', (2, 45),
                 ['The minute hand points to 9. That is 45 minutes.', 'The hour hand is nearly at 3, but it is still the 2 hour.',
                  'So the time is quarter to 3. We write it as 2:45.'], [(4, 45), (7, 45), (10, 45)], cap='quarter to 3')
    qm = lambda n, ms: [(h, m) for h, m in zip(pick(rng, HRS, n), ms)]
    b.read_page('What time is it?', 'Is the minute hand on 3 or on 9? Write each time with numbers.', qm(6, [15, 45, 15, 15, 45, 45]), 3, 2)
    b.read_page('What time is it?', "This page mixes o'clock, quarter past, half past and quarter to.", qm(9, [15, 30, 45, 0, 45, 15, 30, 45, 15]), 3, 3)
    b.draw_page('Draw the hands', 'Read the words. Draw the minute hand first, then the hour hand.', qm(6, [15, 45, 45, 15, 45, 15]), 3, 2, mode='words')
    b.draw_page('Draw the hands', 'Remember: at quarter to, the hour hand is nearly at the next number.', qm(6, [45, 15, 45, 15, 15, 45]), 3, 2)
    b.match_page('Match the words', 'Draw a line from each clock to the words that say its time.', qm(5, [15, 45, 30, 45, 15]), mode='words')
    b.choose_page('Past or to?', 'Fill in the circle next to the words that match each clock.', choose_words(rng, qm(6, [45, 15, 45, 15, 45, 30])))

    # five minutes ---------------------------------------------------------
    b.start('Five minutes', CORAL)
    b.learn_page('Counting the minutes in fives', 'Each number on the clock stands for 5 minutes. Count by fives from the 12 to the minute hand.', (4, 20),
                 ['The minute hand points to 4. Count: 5, 10, 15, 20. That is 20 minutes.', 'The hour hand is past 4 and has not reached 5.',
                  'So the time is 4:20. We say four twenty.'], [(1, 5), (6, 40), (9, 55)])
    F5 = [5, 10, 20, 25, 35, 40, 50, 55]
    fm = lambda n, extra=(): [(h, m) for h, m in zip(pick(rng, HRS, n), (pick(rng, F5, 8) + list(extra))[:n])]
    b.read_page('What time is it?', 'Count by fives to find the minutes. Then write the time.', fm(6), 3, 2)
    b.read_page('What time is it?', 'Count by fives to find the minutes. Then write the time.', fm(9, [15]), 3, 3)
    b.read_page('What time is it?', 'Take care when the hour hand is close to the next number. Which hour is it still?', [(h, m) for h, m in zip(pick(rng, HRS, 9), [50, 55, 45, 40, 55, 50, 35, 40, 55])], 3, 3)
    b.draw_page('Draw the hands', 'Count by fives to place the minute hand. Then draw the hour hand.', fm(6), 3, 2)
    b.draw_page('Draw the hands', 'Count by fives to place the minute hand. Then draw the hour hand.', fm(9, [30]), 3, 3)
    b.match_page('Match the clocks', 'Draw a line from each clock to the same time on the right.', fm(5))
    b.choose_page('Pick the right time', 'Fill in the circle next to the time each clock shows.', choose_digital(rng, fm(6)))

    # to the minute ----------------------------------------------------------
    b.start('To the minute', NAVY)
    b.learn_page('Every little mark is one minute', 'The small marks between the numbers are single minutes. Count by fives, then count on by ones.', (8, 23),
                 ['Count by fives to the number just before the minute hand: 5, 10, 15, 20.', 'Count on by ones for each small mark: 21, 22, 23.',
                  'The hour hand is past 8. So the time is 8:23.'], [(2, 7), (5, 41), (11, 58)])
    M1 = [m for m in range(1, 60) if m % 5]
    mm = lambda n: [(h, m) for h, m in zip([rng.choice(HRS) for _ in range(n)], pick(rng, M1, n))]
    b.read_page('What time is it?', 'Count by fives, then count on by ones. Write the time.', mm(6), 3, 2)
    b.read_page('What time is it?', 'Count by fives, then count on by ones. Write the time.', mm(9), 3, 3)
    b.draw_page('Draw the hands', 'Use the small marks to place the minute hand exactly.', mm(6), 3, 2)
    b.draw_page('Draw the hands', 'Use the small marks to place the minute hand exactly.', mm(9), 3, 3)

    # puzzles ----------------------------------------------------------------
    b.start('Time puzzles', TEAL)
    b.later_page('One hour later', 'Look at each clock. What time will it be one hour later? Write it in the box.', qm(6, [0, 30, 0, 15, 30, 45]), 60, '1 hour later')
    b.later_page('Half an hour later', 'What time will it be 30 minutes later? Write it in the box.', qm(6, [0, 30, 0, 30, 15, 30]), 30, '30 minutes later')
    b.later_page('One hour earlier', 'Go back in time. What time was it one hour earlier?', qm(6, [0, 30, 15, 0, 45, 30]), -60, '1 hour earlier')
    rows = []
    for base, ms in [(7, [0, 0, 0, 0]), (2, [30, 0, 30, 0]), (4, [15, 45, 30, 0])]:
        hs = pick(rng, [base + k for k in range(5)], 4); rows.append([(hh, mnt) for hh, mnt in zip(hs, pick(rng, ms, 4))])
    b.order_page('Earliest to latest', 'All the clocks in a row show times on the same morning. Number them 1, 2, 3, 4 from the earliest to the latest.', rows)
    b.elapsed_page('How long did it take?', 'Look at the start clock and the end clock. Work out how much time went by.', [((2, 0), 60), ((9, 0), 120), ((4, 30), 60), ((7, 0), 30)])
    b.elapsed_page('How long did it take?', 'These are a little harder. Count the hours first, then the minutes.', [((1, 0), 90), ((6, 30), 45), ((10, 15), 150), ((3, 45), 75)])

    top = b.head('a.m. or p.m.?', 'Times from midnight to noon are a.m. Times from noon to midnight are p.m. Circle a.m. or p.m. for each one.')
    top, bot = b.area(top)
    bw = b.w; by = top - 64
    b.rbox(M, by, bw / 2, 44, r=12, col=None, fill=HexColor('#FBE9C8')); b.rbox(M + bw / 2, by, bw / 2, 44, r=12, col=None, fill=HexColor('#DCE3F0'))
    b.sun(M + 30, by + 22, 15); b.moon(W - M - 30, by + 22, 11, NAVY, HexColor('#DCE3F0'))
    b.text(M + 56, by + 25, 'a.m.', 'InB', 14, INK); b.text(M + 56, by + 10, 'midnight to noon', 'In', 9.5, SOFT)
    b.text(W - M - 54, by + 25, 'p.m.', 'InB', 14, INK, 'r'); b.text(W - M - 54, by + 10, 'noon to midnight', 'In', 9.5, SOFT, 'r')
    ev = [('The sun comes up', '6:15', 'a.m.'), ('Breakfast is on the table', '7:30', 'a.m.'), ('The school bus arrives', '8:00', 'a.m.'),
          ('Lunch time at school', '12:30', 'p.m.'), ('School finishes for the day', '3:15', 'p.m.'), ('Dinner is ready', '6:30', 'p.m.'),
          ('The street lights switch on', '7:00', 'p.m.'), ('The stars are out and it is bedtime', '8:30', 'p.m.')]
    rh = (by - 16 - bot) / len(ev); y = by - 16
    for k, (s, tm, ap) in enumerate(ev):
        cy = y - rh / 2
        b.badge(M + 10, cy, k + 1, col=INK); b.text(M + 30, cy - 4.5, s, 'In', 12.5, INK, maxw=b.w - 250)
        b.dig(W - M - 178, cy - 14, tm, w=70, h=28, size=14)
        for j, o in enumerate(['a.m.', 'p.m.']):
            b.rbox(W - M - 126 + j * 66, cy - 14, 58, 28, r=14, col=LINE, lw=0.9); b.text(W - M - 97 + j * 66, cy - 4.5, o, 'InM', 12.5, INK, 'c')
        if k < len(ev) - 1: b.hl(M + 30, W - M, y - rh, col=HAIR, w=0.6)
        y -= rh
    b.ans('text', [ap for _, _, ap in ev])
    b.foot()

    top = b.head('The train timetable', 'Use the timetable to answer the questions. All the trains leave in the morning.')
    top, bot = b.area(top)
    tr = [('Red train', 'Harbor', (8, 0), 30), ('Blue train', 'Hill Town', (8, 30), 60), ('Green train', 'Lakeside', (9, 15), 45),
          ('Yellow train', 'Old Bridge', (10, 0), 90), ('Orange train', 'Garden City', (10, 30), 20)]
    cols = [0.0, 0.27, 0.54, 0.77]; hdr = ['Train', 'Going to', 'Leaves', 'Arrives']; y = top - 8; rh = 30
    b.rbox(M, y - rh, b.w, rh, r=8, col=None, fill=TEAL)
    for cc, hh in zip(cols, hdr): b.text(M + b.w * cc + 16, y - 19.5, hh, 'InB', 11.5, WHITE)
    tcol = {'Red': CORAL, 'Blue': NAVY, 'Green': SAGE, 'Yellow': MUST, 'Orange': HexColor('#E57E2E')}
    for k, (nm, to, (h, m), d) in enumerate(tr):
        yy = y - rh * (k + 2)
        if k % 2 == 0: b.rbox(M, yy, b.w, rh, r=6, col=None, fill=TINT)
        c.setFillColor(tcol[nm.split()[0]]); c.roundRect(M + 14, yy + 9, 20, 12, 3, stroke=0, fill=1)
        b.text(M + 42, yy + 10.5, nm, 'InM', 12, INK); b.text(M + b.w * cols[1] + 16, yy + 10.5, to, 'In', 12, INK)
        b.text(M + b.w * cols[2] + 16, yy + 10.5, fmt(h, m), 'InB', 12.5, INK); b.text(M + b.w * cols[3] + 16, yy + 10.5, fmt(*add(h, m, d)), 'InB', 12.5, INK)
    qs = [('What time does the Green train leave?', fmt(9, 15)), ('Which train leaves at 10:30?', 'Orange train'),
          ('What time does the Blue train arrive at Hill Town?', fmt(*add(8, 30, 60))), ('How long is the Red train ride?', dur(30)),
          ('Which train has the longest ride?', 'Yellow train'), ('Which train arrives at 10:00?', 'Green train'),
          ('You get to the station at 9:00. Which train leaves next?', 'Green train')]
    y = y - rh * 6 - 30; qh = (y - bot) / len(qs)
    for k, (q, a) in enumerate(qs):
        cy = y - qh * k - qh / 2
        b.badge(M + 10, cy + 3, k + 1, col=INK); wq = b.text(M + 30, cy - 1, q, 'In', 12, INK, maxw=b.w - 150)
        b.hl(max(M + 40 + wq, W - M - 150), W - M, cy - 3, col=INK, w=0.9)
    b.ans('text', [a for q, a in qs], note={'trains': [[nm, fmt(h, m), fmt(*add(h, m, d)), d] for nm, to, (h, m), d in tr]})
    b.foot()

    top = b.head('Time stories', 'Read each story. Work out the answer and write it on the line. Use your practice clock to help.')
    top, bot = b.area(top)
    st = [('The cake goes into the oven at 3:00. It bakes for 1 hour. What time is it ready?', fmt(*add(3, 0, 60))),
          ('The bus leaves at 8:30. The ride takes 30 minutes. What time does it arrive?', fmt(*add(8, 30, 30))),
          ('The film starts at 5:15 and ends at 6:15. How long is the film?', dur(60)),
          ('Swimming class starts at 4:45. It lasts 45 minutes. What time does it end?', fmt(*add(4, 45, 45))),
          ('The train should arrive at 2:20. It is 10 minutes late. What time does it arrive?', fmt(*add(2, 20, 10))),
          ('The bakery opens at 7:00 in the morning and closes at 11:00 in the morning. How many hours is it open?', dur(240))]
    sh = (top - bot) / len(st)
    for k, (q, a) in enumerate(st):
        yt = top - sh * k
        b.rbox(M, yt - sh + 8, b.w, sh - 12, r=12, col=HAIR, lw=1)
        b.badge(M + 20, yt - 24, k + 1, col=RINGS[k % 5])
        yq = b.para(M + 40, yt - 28, b.w - 60, q, 'In', 12.5, 18, INK)
        b.text(M + 40, yt - sh + 24, 'Answer', 'InM', 10, SOFT); b.hl(M + 82, M + 260, yt - sh + 22, col=INK, w=0.9)
    b.ans('text', [a for q, a in st])
    b.foot()

    # review -----------------------------------------------------------------
    b.start('Show what you know', MUST)
    b.read_page('Mixed review: read the clocks', 'You have learned every kind of time. Write the time on each clock.',
                [(h, m) for h, m in zip(pick(rng, HRS, 9), [0, 30, 15, 45, 20, 55, 5, 37, 12])], 3, 3)
    b.draw_page('Mixed review: draw the hands', 'Draw both hands on every clock. Take your time with the last three.',
                [(h, m) for h, m in zip(pick(rng, HRS, 9), [30, 0, 45, 15, 10, 50, 35, 26, 48])], 3, 3)
    # certificate
    b.seen.append(('Show what you know', b.n)) if False else None
    c.setFillColor(CREAM); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(NAVY); c.setLineWidth(2.2); c.roundRect(30, 30, W - 60, H - 60, 18, stroke=1, fill=0)
    c.setStrokeColor(CORAL); c.setLineWidth(0.9); c.roundRect(40, 40, W - 80, H - 80, 12, stroke=1, fill=0)
    for x, y, r, col in [(0.16, 0.86, 10, MUST), (0.84, 0.86, 10, MUST), (0.2, 0.60, 6, CORAL), (0.8, 0.60, 6, TEAL), (0.16, 0.14, 8, TEAL), (0.84, 0.14, 8, CORAL)]:
        b.star(W * x, H * y, r, col)
    b.text(W / 2, H - 122, 'CERTIFICATE', 'InB', 12, TEAL, 'c')
    b.text(W / 2, H - 176, 'I can tell the time!', 'FrM', 40, INK, 'c')
    b.clock(W / 2, H * 0.535, W * 0.17, 12, 0, ring=CORAL)
    y = H * 0.535 - W * 0.17 - 56
    b.text(W / 2, y, 'This certificate goes to', 'FrI', 17, SOFT, 'c')
    b.hl(W * 0.24, W * 0.76, y - 54, col=INK, w=1)
    b.text(W / 2, y - 84, "for learning to read the clock from o'clock to the minute.", 'In', 12, INK, 'c', maxw=W - 110)
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
        if e['kind'] == 'clocks':
            per = 9; rws = (len(e['data']) + per - 1) // per; need = 24 + rws * 68
        else:
            items = ['%d.  %s' % (i + 1, a) for i, a in enumerate(e['data'])]
            if e['note'] == 'fives': items = ['Clockwise from 3:  ' + ', '.join(e['data'])]
            lines = []; line = ''
            for it in items:
                tline = (line + '      ' + it) if line else it
                if sw(tline, 'In', 10.5) > b.w - 12: lines.append(line); line = it
                else: line = tline
            if line: lines.append(line)
            need = 22 + len(lines) * 16 + 2
        if y - need < bot:
            b.foot(); y = khead()
        b.rbox(M, y - 15, 54, 17, r=8.5, col=None, fill=TINT); b.text(M + 27, y - 10.8, 'Page %d' % e['page'], 'InB', 8.5, INK, 'c')
        b.text(M + 64, y - 11, e['title'], 'InM', 10.5, INK)
        yy = y - 24
        if e['kind'] == 'clocks':
            cw = b.w / 9
            for i, (h, m) in enumerate(e['data']):
                cx = M + cw * (i % 9 + 0.5); cy = yy - 25 - (i // 9) * 68
                b.clock(cx, cy, 23, h, m, ring=RINGS[(i + 2) % 5], minticks=False)
                b.text(cx, cy - 35, fmt(h, m), 'InM', 9, INK, 'c')
        else:
            for ln in lines:
                yy -= 12; b.text(M + 6, yy, ln, 'In', 10.5, INK); yy -= 4
        y -= need + 6
        b.hl(M, W - M, y + 4, col=HAIR, w=0.6)
    if y - bot > 106:
        bh = 96; by = bot + 2
        b.rbox(M, by, b.w, bh, r=14, col=None, fill=TINT)
        b.star(M + 38, by + bh / 2, 15, MUST); b.star(M + 62, by + bh / 2 + 22, 7, CORAL); b.star(M + 60, by + bh / 2 - 24, 6, TEAL)
        b.text(M + 92, by + bh - 40, 'Well done, time teller!', 'FrM', 20, INK)
        b.text(M + 92, by + bh - 62, 'Keep practicing with the real clocks around you, at home and at school.', 'In', 10.5, SOFT, maxw=b.w - 104)
        b.text(M + 92, by + bh - 80, 'More printables at inkwellandco.gumroad.com', 'InM', 10.5, CORAL)
    b.foot()
    b.seen.append(('_total', b.n - 1))
    c.save()
    return b


if __name__ == '__main__':
    import os
    os.makedirs(OUT, exist_ok=True)
    for size, tag, fn in [(letter, 'US Letter', 'Telling_Time_Worksheets_US_Letter.pdf'), (A4, 'A4', 'Telling_Time_Worksheets_A4.pdf')]:
        b = build(OUT + fn, size, tag)                                  # pass 1 collects page numbers
        toc = [(s, p) for s, p in b.seen if not s.startswith('_total')] + [('_total', b.n - 1)]
        toc = [t for t in toc if t[0] != '_total'] + [('_pages', b.n - 1)]
        toc_final = [t for t in toc if t[0] != '_pages'] + [('_pages_total', b.n - 1)]
        b = build(OUT + fn, size, tag, toc=[t for t in toc_final])
        print(tag, 'pages', b.n - 1, 'sections', [t for t in b.seen if not t[0].startswith('_')])
        json.dump({'key': b.key, 'clocks': b.man, 'pages': b.n - 1}, open(OUT + fn.replace('.pdf', '.json'), 'w'), indent=1)
    for w_ in WARN: print('WARN', w_)
    print('warnings:', len(WARN))
