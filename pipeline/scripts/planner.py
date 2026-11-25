import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = '/home/claude/fonts/ttf/'
for n, f in [('Fr', 'fraunces-latin-300-normal'), ('FrM', 'fraunces-latin-400-normal'), ('FrI', 'fraunces-latin-300-italic'),
             ('In', 'instrument-sans-latin-400-normal'), ('InM', 'instrument-sans-latin-500-normal'), ('InB', 'instrument-sans-latin-600-normal')]:
    pdfmetrics.registerFont(TTFont(n, F + f + '.ttf'))

INK = HexColor('#20294A'); SOFT = HexColor('#7C8196'); LINE = HexColor('#B9BCC8'); HAIR = HexColor('#D9DBE3')
CORAL = HexColor('#D9583B'); TINT = HexColor('#F4EFE6')


class P:
    def __init__(self, path, size, tag):
        self.c = canvas.Canvas(path, pagesize=size)
        self.W, self.H = size
        self.m = 46
        self.tag = tag
        self.n = 0
        self.c.setTitle('The Everyday Planner Pack'); self.c.setAuthor('Inkwell and Co')

    # primitives
    def caps(self, x, y, s, size=6.6, col=SOFT, font='InB', right=False, sp=1.3):
        c = self.c; c.setFillColor(col); c.setFont(font, size)
        s = s.upper()
        w = pdfmetrics.stringWidth(s, font, size) + sp * (len(s) - 1)
        t = c.beginText(x - w if right else x, y); t.setFont(font, size); t.setCharSpace(sp); t.textOut(s); c.drawText(t)
        return w

    def hl(self, x1, x2, y, col=LINE, w=0.5, dash=None):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(w); c.setDash(dash or [])
        c.line(x1, y, x2, y); c.setDash([])

    def vl(self, x, y1, y2, col=LINE, w=0.5):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(w); c.line(x, y1, x, y2)

    def box(self, x, y, w, h, col=INK, lw=0.6, fill=None, r=0):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(lw)
        if fill: c.setFillColor(fill)
        if r: c.roundRect(x, y, w, h, r, stroke=1, fill=1 if fill else 0)
        else: c.rect(x, y, w, h, stroke=1, fill=1 if fill else 0)

    def check(self, x, y, s=8):
        self.box(x, y, s, s, col=INK, lw=0.6, r=1.5)

    def field(self, x, y, label, w):
        lw = self.caps(x, y, label)
        self.hl(x + lw + 6, x + w, y - 1.5, col=INK, w=0.5)

    def lines(self, x1, x2, ytop, ybot, step=20, col=LINE):
        y = ytop
        while y >= ybot - 0.1:
            self.hl(x1, x2, y, col=col); y -= step

    def head(self, title, accent, sub=None):
        """Draw header, return y of content top."""
        c = self.c; m = self.m; self.n += 1
        top = self.H - m
        self.caps(m, top - 4, 'Inkwell and Co', col=INK)
        self.caps(self.W - m, top - 4, sub or 'The Everyday Planner', right=True)
        y = top - 44
        c.setFillColor(INK); c.setFont('Fr', 30); c.drawString(m, y, title)
        w = pdfmetrics.stringWidth(title, 'Fr', 30) + 9
        c.setFillColor(CORAL); c.setFont('FrI', 30); c.drawString(m + w, y, accent)
        self.hl(m, self.W - m, y - 14, col=INK, w=0.9)
        # footer
        self.caps(m, m - 18, 'For personal use', size=5.6, col=LINE)
        self.caps(self.W - m, m - 18, '%02d' % self.n, size=5.6, col=LINE, right=True)
        return y - 14

    def done(self): self.c.showPage()

    # pages ---------------------------------------------------------
    def cover(self):
        c = self.c; m = self.m; W, H = self.W, self.H
        c.setFillColor(TINT); c.rect(0, 0, W, H, stroke=0, fill=1)
        self.caps(m, H - m - 4, 'Inkwell and Co', col=INK)
        self.caps(W - m, H - m - 4, 'Undated, print any time', right=True)
        c.setFillColor(INK); c.setFont('Fr', 64)
        c.drawString(m, H - 250, 'The'); c.drawString(m, H - 316, 'Everyday')
        c.setFillColor(CORAL); c.setFont('FrI', 64); c.drawString(m, H - 382, 'Planner.')
        self.hl(m, W - m, H - 420, col=INK, w=0.9)
        items = ['Year at a glance', 'Month, Sunday start', 'Month, Monday start', 'Week', 'Day', 'Habit tracker',
                 'Monthly budget', 'Expense log', 'Bill tracker', 'Savings goal', 'To do list', 'Goals', 'Lined notes', 'Dot grid notes']
        y = H - 452; colw = (W - 2 * m) / 2
        for i, it in enumerate(items):
            x = m + (i % 2) * colw; yy = y - (i // 2) * 24
            c.setFillColor(CORAL); c.setFont('FrI', 11); c.drawString(x, yy, '%02d' % (i + 1))
            c.setFillColor(INK); c.setFont('In', 11); c.drawString(x + 24, yy, it)
            self.hl(x, x + colw - 18, yy - 8, col=LINE)
        c.setFillColor(SOFT); c.setFont('In', 8.5)
        c.drawString(m, m + 14, 'Print the pages you need, as many times as you like. ' + self.tag + ' size.')
        c.drawString(m, m, 'Copyright 2026 Inkwell and Co. For personal use. Please do not resell or share the file.')
        self.done()

    def year(self):
        top = self.head('Year at a', 'glance'); m = self.m
        self.field(m, top - 22, 'Year', 150)
        gt = top - 40; gb = m; cols, rows = 3, 4; g = 10
        cw = (self.W - 2 * m - g * (cols - 1)) / cols; ch = (gt - gb - g * (rows - 1)) / rows
        for i in range(12):
            x = m + (i % cols) * (cw + g); y = gt - (i // cols) * (ch + g) - ch
            self.box(x, y, cw, ch, col=INK, lw=0.6)
            self.c.setFillColor(CORAL); self.c.setFont('FrI', 13); self.c.drawString(x + 9, y + ch - 19, '%02d' % (i + 1))
            self.hl(x + 32, x + cw - 9, y + ch - 20, col=INK)
            self.lines(x + 9, x + cw - 9, y + ch - 42, y + 12, step=(ch - 54) / 5.0)
        self.done()

    def month(self, days, label):
        top = self.head('This', 'month', sub=label); m = self.m
        self.field(m, top - 22, 'Month', 190); self.field(m + 210, top - 22, 'Year', 110)
        nw = 118; gx = m; gw = self.W - 2 * m - nw - 12
        gt = top - 40; hh = 16; gb = m + 0; rows = 6
        cw = gw / 7; ch = (gt - hh - gb) / rows
        for i, d in enumerate(days):
            self.c.setFillColor(TINT); self.c.rect(gx + i * cw, gt - hh, cw, hh, stroke=0, fill=1)
            self.caps(gx + i * cw + 5, gt - hh + 5, d, col=INK, size=6.2)
        for r in range(rows + 1): self.hl(gx, gx + gw, gt - hh - r * ch, col=INK if r in (0, rows) else LINE)
        self.hl(gx, gx + gw, gt, col=INK)
        for i in range(8): self.vl(gx + i * cw, gb, gt, col=INK if i in (0, 7) else LINE)
        nx = gx + gw + 12
        self.caps(nx, gt - 11, 'Focus', col=INK)
        self.lines(nx, nx + nw, gt - 34, gt - 34 - 3 * 20, col=LINE)
        self.caps(nx, gt - 124, 'Do not forget', col=INK)
        for i in range(7):
            self.check(nx, gt - 150 - i * 20); self.hl(nx + 13, nx + nw, gt - 150 - i * 20, col=LINE)
        ny = gt - 150 - 7 * 20 - 16
        self.caps(nx, ny, 'Notes', col=INK)
        self.lines(nx, nx + nw, ny - 22, gb, col=LINE)
        self.done()

    def week(self):
        top = self.head('This', 'week'); m = self.m
        self.field(m, top - 22, 'Week of', 200)
        lw = (self.W - 2 * m) * 0.62; rx = m + lw + 16; rw = self.W - m - rx
        gt = top - 40; gb = m; dh = (gt - gb) / 7
        for i, d in enumerate(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']):
            y = gt - i * dh
            self.hl(m, m + lw, y, col=INK, w=0.7)
            self.caps(m, y - 13, d, col=INK)
            n = 3; st = (dh - 22) / n
            for k in range(1, n + 1): self.hl(m + 70, m + lw, y - 22 - (k - 1) * st - st * 0.45, col=HAIR)
        self.hl(m, m + lw, gb, col=INK, w=0.7)
        self.caps(rx, gt - 13, 'Top three', col=CORAL)
        for i in range(3):
            self.c.setFillColor(INK); self.c.setFont('FrI', 15); self.c.drawString(rx, gt - 42 - i * 26, str(i + 1))
            self.hl(rx + 16, rx + rw, gt - 44 - i * 26, col=INK)
        y = gt - 136; self.caps(rx, y, 'To do', col=INK)
        for i in range(10):
            self.check(rx, y - 26 - i * 20); self.hl(rx + 13, rx + rw, y - 26 - i * 20, col=LINE)
        y = y - 26 - 10 * 20 - 14; self.caps(rx, y, 'Notes', col=INK)
        self.box(rx, gb, rw, y - 10 - gb, col=INK, lw=0.6)
        self.done()

    def day(self):
        top = self.head('Daily', 'plan'); m = self.m
        self.field(m, top - 22, 'Date', 190)
        lw = (self.W - 2 * m) * 0.46; rx = m + lw + 20; rw = self.W - m - rx
        gt = top - 44; gb = m; hrs = list(range(6, 23)); st = (gt - gb) / len(hrs)
        self.caps(m, gt + 4, 'Schedule', col=INK)
        for i, h in enumerate(hrs):
            y = gt - i * st - 14
            lab = '%d %s' % ((h - 1) % 12 + 1, 'am' if h < 12 else 'pm')
            self.c.setFillColor(SOFT); self.c.setFont('In', 7.5); self.c.drawRightString(m + 28, y - st + 16, lab)
            self.hl(m + 34, m + lw, y - st + 14, col=LINE)
            self.hl(m + 34, m + lw, y - st / 2 + 14, col=HAIR, dash=[1, 2])
        self.caps(rx, gt + 4, 'Top three', col=CORAL)
        for i in range(3):
            self.c.setFillColor(INK); self.c.setFont('FrI', 15); self.c.drawString(rx, gt - 24 - i * 26, str(i + 1))
            self.hl(rx + 16, rx + rw, gt - 26 - i * 26, col=INK)
        y = gt - 112; self.caps(rx, y, 'To do', col=INK)
        for i in range(9):
            self.check(rx, y - 26 - i * 20); self.hl(rx + 13, rx + rw, y - 26 - i * 20, col=LINE)
        y = y - 26 - 9 * 20 - 12; self.caps(rx, y, 'Grateful for', col=INK)
        self.lines(rx, rx + rw, y - 24, y - 24 - 2 * 20, col=LINE)
        y = y - 24 - 2 * 20 - 22; self.caps(rx, y, 'Notes', col=INK)
        self.box(rx, gb, rw, y - 10 - gb, col=INK, lw=0.6)
        self.done()

    def habits(self):
        top = self.head('Habit', 'tracker'); m = self.m
        self.field(m, top - 22, 'Month', 190)
        gt = top - 44; rows = 14; lab = 122; gw = self.W - 2 * m - lab; cw = gw / 31; hh = 16
        rh = min(cw * 1.5, (gt - hh - m - 70) / rows)
        self.caps(m, gt - 11, 'Habit', col=INK)
        for d in range(31):
            self.c.setFillColor(SOFT); self.c.setFont('InM', 6); self.c.drawCentredString(m + lab + d * cw + cw / 2, gt - 11, str(d + 1))
        for r in range(rows + 1):
            y = gt - hh - r * rh; self.hl(m, self.W - m, y, col=INK if r in (0, rows) else LINE)
        for d in range(32):
            x = m + lab + d * cw; self.vl(x, gt - hh - rows * rh, gt - hh, col=INK if d in (0, 31) else (LINE if d % 7 == 0 else HAIR))
        y = gt - hh - rows * rh - 26
        self.caps(m, y, 'How did the month go', col=INK)
        self.lines(m, self.W - m, y - 24, m, col=LINE)
        self.done()

    def table(self, x, ytop, w, cols, rows, rh=19, total=None):
        """cols: list of (label, fraction). returns y bottom"""
        hh = 16
        self.c.setFillColor(TINT); self.c.rect(x, ytop - hh, w, hh, stroke=0, fill=1)
        cx = x
        for lab, fr in cols:
            self.caps(cx + 5, ytop - hh + 5, lab, col=INK, size=6); cx += fr * w
        n = rows + (1 if total else 0)
        for r in range(n + 1): self.hl(x, x + w, ytop - hh - r * rh, col=INK if r in (0, n) or (total and r == rows) else LINE)
        self.hl(x, x + w, ytop, col=INK)
        cx = x; yb = ytop - hh - n * rh
        for i, (lab, fr) in enumerate(cols):
            self.vl(cx, yb, ytop, col=INK if i == 0 else LINE); cx += fr * w
        self.vl(x + w, yb, ytop, col=INK)
        if total: self.caps(x + 5, yb + 6, total, col=CORAL, size=6)
        return yb

    def budget(self):
        top = self.head('Monthly', 'budget'); m = self.m
        self.field(m, top - 22, 'Month', 190)
        g = 16; cw = (self.W - 2 * m - g) / 2; gt = top - 60; x2 = m + cw + g
        c3 = [('Item', .5), ('Planned', .25), ('Actual', .25)]
        self.caps(m, gt + 6, 'Income', col=CORAL)
        y = self.table(m, gt, cw, c3, 4, total='Total')
        self.caps(m, y - 20, 'Fixed bills', col=CORAL)
        yl = self.table(m, y - 26, cw, c3, 10, total='Total')
        self.caps(x2, gt + 6, 'Everyday spending', col=CORAL)
        y = self.table(x2, gt, cw, c3, 11, total='Total')
        self.caps(x2, y - 20, 'Saving and giving', col=CORAL)
        yr = self.table(x2, y - 26, cw, c3, 3, total='Total')
        yb = min(yl, yr) - 26
        self.caps(m, yb, 'The month in four numbers', col=INK)
        bw = (self.W - 2 * m - 3 * 10) / 4; bh = min(62, yb - 12 - m)
        for i, t in enumerate(['Money in', 'Money out', 'Saved', 'Left over']):
            x = m + i * (bw + 10); self.box(x, yb - 12 - bh, bw, bh, col=INK, lw=0.6)
            self.caps(x + 7, yb - 12 - 13, t, col=SOFT, size=6)
        self.done()

    def expenses(self):
        top = self.head('Expense', 'log'); m = self.m
        self.field(m, top - 22, 'Month', 190)
        gt = top - 44; rows = int((gt - 16 - m) / 19) - 1
        self.table(m, gt, self.W - 2 * m, [('Date', .12), ('What', .4), ('Category', .2), ('Paid with', .14), ('Amount', .14)], rows, total='Total')
        self.done()

    def bills(self):
        top = self.head('Bill', 'tracker'); m = self.m
        self.field(m, top - 22, 'Year', 150)
        gt = top - 44; w = self.W - 2 * m; mons = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
        cols = [('Bill', .3), ('Due', .1), ('Amount', .14)] + [(x, .46 / 12) for x in mons]
        rows = int((gt - 16 - m - 60) / 19)
        y = self.table(m, gt, w, cols, rows)
        self.c.setFillColor(SOFT); self.c.setFont('In', 8.5)
        self.c.drawString(m, y - 18, 'Tick the month once the bill is paid.')
        self.done()

    def savings(self):
        top = self.head('Savings', 'goal'); m = self.m; w = self.W - 2 * m
        y = top - 26
        self.field(m, y, 'Saving for', w * .58); self.field(m + w * .62, y, 'Target', w * .38)
        y -= 26
        self.field(m, y, 'Start date', w * .3); self.field(m + w * .34, y, 'Goal date', w * .3); self.field(m + w * .68, y, 'Each box is worth', w * .32)
        y -= 30
        self.caps(m, y, 'Shade one box every time you save', col=CORAL)
        cols, rows = 20, 5; s = w / cols; gy = y - 12
        for r in range(rows + 1): self.hl(m, m + w, gy - r * s, col=INK if r in (0, rows) else LINE)
        for c_ in range(cols + 1): self.vl(m + c_ * s, gy - rows * s, gy, col=INK if c_ in (0, cols) else LINE)
        for r in range(rows):
            self.c.setFillColor(LINE); self.c.setFont('InM', 5.5)
            self.c.drawRightString(m + w - 3, gy - r * s - s + 3, str((r + 1) * 20))
        ty = gy - rows * s - 30
        self.caps(m, ty + 6, 'Deposits', col=CORAL)
        rws = int((ty - 16 - m) / 19) - 0
        g = 16; cw = (w - g) / 2; cc = [('Date', .3), ('Amount', .32), ('Total so far', .38)]
        self.table(m, ty, cw, cc, rws); self.table(m + cw + g, ty, cw, cc, rws)
        self.done()

    def todo(self):
        top = self.head('To do', 'list'); m = self.m; w = self.W - 2 * m
        g = 22; cw = (w - g) / 2; gt = top - 36
        for k, t in enumerate(['Must do', 'Would be nice']):
            x = m + k * (cw + g); self.caps(x, gt, t, col=CORAL if k == 0 else INK)
            y = gt - 26
            while y > m + 2:
                self.check(x, y); self.hl(x + 14, x + cw, y, col=LINE); y -= 22
        self.done()

    def goals(self):
        top = self.head('Three', 'goals'); m = self.m; w = self.W - 2 * m
        gt = top - 20; g = 14; bh = (gt - m - 2 * g) / 3
        for i in range(3):
            yt = gt - i * (bh + g); yb = yt - bh
            self.box(m, yb, w, bh, col=INK, lw=0.6)
            self.c.setFillColor(CORAL); self.c.setFont('FrI', 30); self.c.drawString(m + 12, yt - 34, str(i + 1))
            self.field(m + 40, yt - 24, 'Goal', w - 190); self.field(m + w - 136, yt - 24, 'By when', 124)
            self.caps(m + 12, yt - 58, 'Why it matters', col=INK)
            self.lines(m + 12, m + w * .46, yt - 80, yb + 14, step=20)
            x = m + w * .5; self.caps(x, yt - 58, 'Next steps', col=INK)
            y = yt - 80
            while y > yb + 10:
                self.check(x, y); self.hl(x + 14, m + w - 12, y, col=LINE); y -= 20
        self.done()

    def lined(self):
        top = self.head('Notes', '', sub='Lined'); m = self.m
        self.lines(m, self.W - m, top - 30, m, step=22)
        self.done()

    def dots(self):
        top = self.head('Notes', '', sub='Dot grid'); m = self.m; c = self.c
        c.setFillColor(LINE); s = 14.17
        n = int((self.W - 2 * m) / s); off = (self.W - 2 * m - n * s) / 2
        y = top - 18
        while y > m:
            for i in range(n + 1): c.circle(m + off + i * s, y, 0.55, stroke=0, fill=1)
            y -= s
        self.done()

    def build(self):
        self.cover(); self.year()
        self.month(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], 'Sunday start')
        self.month(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], 'Monday start')
        self.week(); self.day(); self.habits(); self.budget(); self.expenses(); self.bills(); self.savings()
        self.todo(); self.goals(); self.lined(); self.dots()
        self.c.save()


out = '/home/claude/book/out/planner/'
import os; os.makedirs(out, exist_ok=True)
P(out + 'Everyday_Planner_US_Letter.pdf', letter, 'US Letter').build()
P(out + 'Everyday_Planner_A4.pdf', A4, 'A4').build()
print('ok')
