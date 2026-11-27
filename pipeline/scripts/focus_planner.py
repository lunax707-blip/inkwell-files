# The Focus Planner: ADHD friendly undated planner for freelancers (big type, few boxes).
# Builds 4 PDFs (US Letter and A4, Monday start and Sunday start) into /home/claude/book/out/focus/
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F = '/home/claude/fonts/ttf/'
for n, f in [('Fr', 'fraunces-latin-300-normal'), ('FrM', 'fraunces-latin-400-normal'), ('FrI', 'fraunces-latin-300-italic'),
             ('In', 'instrument-sans-latin-400-normal'), ('InM', 'instrument-sans-latin-500-normal'), ('InB', 'instrument-sans-latin-600-normal')]:
    pdfmetrics.registerFont(TTFont(n, F + f + '.ttf'))

INK = HexColor('#20294A'); SOFT = HexColor('#666B82'); LINE = HexColor('#A9ADBD'); HAIR = HexColor('#D9DBE4')
CORAL = HexColor('#D9583B'); TINT = HexColor('#F6F0E6'); TEAL = HexColor('#1F6F78'); MUST = HexColor('#C4871C')
SAGE = HexColor('#5E8468'); NAVY = HexColor('#2B3A67'); WHITE = HexColor('#FFFFFF')
SEC = {'Start here': CORAL, 'Set up': NAVY, 'Capture': TEAL, 'Week': MUST, 'Day': CORAL, 'Projects': TEAL,
       'Money and admin': MUST, 'Month': SAGE, 'Extras': NAVY}
NAME = 'The Focus Planner'
FULL = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
WARN = []
sw = pdfmetrics.stringWidth
PAGES = 48


class P:
    def __init__(self, path, size, tag, days, toc=None):
        self.c = canvas.Canvas(path, pagesize=size)
        self.W, self.H = size
        self.m = 50; self.B = 58
        self.w = self.W - 2 * self.m
        self.tag = tag; self.days = days; self.toc = toc or []; self.seen = []
        self.n = 1; self.sec = 'Start here'; self.ac = CORAL
        self.c.setTitle(NAME + ' for Freelancers (' + tag + ')'); self.c.setAuthor('Inkwell and Co')
        self.c.setSubject('Undated ADHD friendly planner for freelancers. For personal use.')

    # primitives ----------------------------------------------------
    def caps(self, x, y, s, size=7.4, col=SOFT, font='InB', right=False, sp=1.2, maxw=None, center=False):
        c = self.c; s = s.upper()
        w = sw(s, font, size) + sp * (len(s) - 1)
        if maxw is not None and w > maxw: WARN.append('caps too wide: %s (%.0f > %.0f) p%d %s' % (s, w, maxw, self.n, self.tag))
        x0 = x - w if right else (x - w / 2 if center else x)
        t = c.beginText(x0, y); t.setFont(font, size); t.setFillColor(col); t.setCharSpace(sp); t.textOut(s); t.setCharSpace(0); c.drawText(t)
        return w

    def text(self, x, y, s, font='In', size=11, col=INK, right=False, maxw=None, center=False):
        c = self.c; c.setFillColor(col); c.setFont(font, size)
        tw = sw(s, font, size)
        if maxw is not None and tw > maxw: WARN.append('text too wide: %s (%.0f > %.0f) p%d %s' % (s, tw, maxw, self.n, self.tag))
        if right: c.drawRightString(x, y, s)
        elif center: c.drawCentredString(x, y, s)
        else: c.drawString(x, y, s)
        return tw

    def para(self, x, y, w, s, font='In', size=11, lead=16, col=INK):
        words = s.split(); line = ''
        for wd in words:
            t = (line + ' ' + wd).strip()
            if sw(t, font, size) > w: self.text(x, y, line, font, size, col); y -= lead; line = wd
            else: line = t
        if line: self.text(x, y, line, font, size, col); y -= lead
        return y

    def hl(self, x1, x2, y, col=LINE, w=0.7):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(w); c.line(x1, y, x2, y)

    def vl(self, x, y1, y2, col=LINE, w=0.7):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(w); c.line(x, y1, x, y2)

    def box(self, x, y, w, h, col=INK, lw=0.9, fill=None, r=7, dash=None):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(lw)
        if dash: c.setDash(*dash)
        if fill: c.setFillColor(fill)
        if r: c.roundRect(x, y, w, h, r, stroke=1, fill=1 if fill else 0)
        else: c.rect(x, y, w, h, stroke=1, fill=1 if fill else 0)
        if dash: c.setDash()

    def check(self, x, y, s=13):
        self.box(x, y, s, s, col=INK, lw=0.9, r=3, fill=WHITE)

    def circ(self, x, y, r=7, fill=None, col=INK, lw=0.9):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(lw)
        if fill: c.setFillColor(fill)
        c.circle(x, y, r, stroke=1, fill=1 if fill else 0)

    def sq(self, x, y, s=8, col=None):
        self.c.setFillColor(col or self.ac); self.c.rect(x, y, s, s, stroke=0, fill=1)

    def label(self, x, y, s, col=None, maxw=None, size=7.6):
        return self.caps(x, y, s, col=col or self.ac, size=size, maxw=maxw)

    def field(self, x, y, label, w):
        lw = self.caps(x, y, label, col=INK, maxw=w - 36)
        self.hl(x + lw + 7, x + w, y - 2, col=INK, w=0.7)

    def fields(self, y, items, gap=18):
        x = self.m; tot = self.w - gap * (len(items) - 1)
        for lab, fr in items:
            self.field(x, y, lab, tot * fr); x += tot * fr + gap
        return y - 24

    def lines(self, x1, x2, ytop, ybot, step=26, col=LINE):
        y = ytop
        while y >= ybot - 0.1:
            self.hl(x1, x2, y, col=col); y -= step

    def lbox(self, x, yt, w, h, label, hint=None, step=26, fill=None, lines=True, checks=False, pad=14):
        """Rounded box with a caps label, an optional italic hint and wide writing lines."""
        self.box(x, yt - h, w, h, fill=fill)
        self.label(x + pad, yt - 20, label, maxw=w - 2 * pad)
        y0 = yt - 26
        if hint:
            self.text(x + pad, yt - 36, hint, 'FrI', 10.3, SOFT, maxw=w - 2 * pad); y0 = yt - 42
        if not lines: return y0
        y = y0 - step + 2
        while y > yt - h + 10:
            if checks:
                self.check(x + pad, y + 2); self.hl(x + pad + 20, x + w - pad, y)
            else:
                self.hl(x + pad, x + w - pad, y)
            y -= step
        return y0

    def grid(self, yt, yb, items, cols=2, g=14, step=26, checks=False, fill=None):
        rows = (len(items) + cols - 1) // cols
        cw = (self.w - g * (cols - 1)) / cols; bh = (yt - yb - g * (rows - 1)) / rows
        for i, it in enumerate(items):
            a, b = it if isinstance(it, tuple) else (it, None)
            self.lbox(self.m + (i % cols) * (cw + g), yt - (i // cols) * (bh + g), cw, bh, a, hint=b, step=step, checks=checks, fill=fill)

    def checklist(self, x, yt, w, items=None, n=0, step=26, ybot=None, size=11):
        y = yt
        rows = list(items or []) + [''] * n
        if ybot is not None:
            while y - (len(rows) + 1) * step >= ybot - 0.5: rows.append('')
        for it in rows:
            self.check(x, y - 15)
            if it: self.text(x + 21, y - 12, it, 'In', size, INK, maxw=w - 22)
            else: self.hl(x + 21, x + w, y - 15)
            y -= step
        return y

    def table(self, yt, cols, rows=None, rh=28, yb=None, total=None, first=None, x=None, w=None, checkcol=None, italic_first=0):
        """Open table: strong top rule, caps header, wide rows. checkcol: index of a column that gets a tick box."""
        x = self.m if x is None else x; w = self.w if w is None else w; hh = 22
        if rows is None:
            avail = yt - hh - yb; rows = int(avail / rh + 0.001) - (1 if total else 0)
            rh = avail / (rows + (1 if total else 0))
        if checkcol is not None and not isinstance(checkcol, (list, tuple)): checkcol = [checkcol]
        self.hl(x, x + w, yt, col=INK, w=1.2)
        self.hl(x, x + w, yt - hh, col=INK, w=0.7)
        cx = x; xs = []
        for i, (lab, fr) in enumerate(cols):
            cw = w * fr; xs.append((cx, cw))
            self.caps(cx + (6 if i else 2), yt - 14.5, lab, size=6.9, col=INK, sp=0.9, maxw=cw - 8)
            if i: self.vl(cx, yt - hh - rows * rh, yt - hh, col=HAIR)
            cx += cw
        for r in range(1, rows + 1):
            y = yt - hh - r * rh
            self.hl(x, x + w, y, col=INK if r == rows else LINE, w=1.0 if r == rows else 0.7)
            if first and r <= len(first) and first[r - 1]:
                vals = first[r - 1] if isinstance(first[r - 1], (list, tuple)) else [first[r - 1]]
                for k, v in enumerate(vals):
                    if v: self.text(xs[k][0] + (6 if k else 2), y + rh / 2 - 4, v, 'FrI' if r <= italic_first else 'In', 10.4,
                                    SOFT if r <= italic_first else INK, maxw=xs[k][1] - 8)
            for cc in (checkcol or []):
                cx0, cw0 = xs[cc]; self.check(cx0 + cw0 / 2 - 6.5, y + rh / 2 - 6.5)
        yb2 = yt - hh - rows * rh
        if total:
            self.caps(x + 2, yb2 - rh / 2 - 3, total, size=7.4, col=self.ac)
            self.hl(x, x + w, yb2 - rh, col=INK, w=1.2)
            yb2 -= rh
        return yb2

    def stats(self, yt, labels, h=58, gap=12, fill=TINT):
        bw = (self.w - gap * (len(labels) - 1)) / len(labels)
        for i, t in enumerate(labels):
            x = self.m + i * (bw + gap); self.box(x, yt - h, bw, h, fill=fill)
            self.caps(x + 11, yt - 17, t, size=6.8, col=INK, maxw=bw - 18)
        return yt - h

    def note(self, text, h=40):
        """Tinted strip at the bottom of the page with one short reminder."""
        m = self.m; self.c.setFillColor(TINT); self.c.roundRect(m, self.B, self.w, h, 7, stroke=0, fill=1)
        self.sq(m + 14, self.B + h / 2 - 4)
        self.text(m + 32, self.B + h / 2 - 4, text, 'FrI', 11.2, INK, maxw=self.w - 46)
        return self.B + h + 14

    def options(self, x, y, items, w, r=6.5, size=10.6):
        """Circles with printed choices on one line, evenly spread."""
        tot = sum(sw(t, 'In', size) + 2 * r + 7 for t in items)
        gap = (w - tot) / max(1, len(items) - 1)
        if gap < 8: WARN.append('options too tight: %s p%d %s' % (items[0], self.n, self.tag))
        for t in items:
            self.circ(x + r, y + 3.6, r); self.text(x + 2 * r + 7, y, t, 'In', size, INK)
            x += sw(t, 'In', size) + 2 * r + 7 + gap

    def head(self, title, accent='', sec=None, when=None, toc=True):
        c = self.c; m = self.m; self.n += 1
        if sec: self.sec = sec; self.ac = SEC[sec]
        if toc: self.seen.append((self.sec, (title + ' ' + accent).strip(), self.n))
        top = self.H - 44
        self.caps(m, top - 4, 'Inkwell and Co', col=INK, size=6.6)
        lw = self.caps(self.W - m, top - 4, self.sec, right=True, col=INK, size=6.6)
        self.sq(self.W - m - lw - 14, top - 5.5, 8)
        y = top - 50
        c.setFillColor(INK); c.setFont('Fr', 34); c.drawString(m - 1, y, title)
        w = sw(title, 'Fr', 34) + 10
        if accent:
            c.setFillColor(self.ac); c.setFont('FrI', 34); c.drawString(m - 1 + w, y, accent)
            if w + sw(accent, 'FrI', 34) > self.w: WARN.append('title too wide: ' + title + ' ' + accent)
        y -= 16
        self.hl(m, self.W - m, y, col=INK, w=1.3)
        if when:
            y = self.para(m, y - 21, self.w, when, 'FrI', 11.6, 16.5, SOFT) + 16.5 - 6
        self.caps(m, 30, NAME, size=6, col=SOFT)
        self.caps(self.W - m, 30, '%02d' % self.n, size=6.6, col=INK, right=True)
        return y - 18

    def done(self): self.c.showPage()

    # start here ----------------------------------------------------
    def cover(self):
        c = self.c; m = self.m; W, H = self.W, self.H
        c.setFillColor(TINT); c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(NAVY); c.rect(0, H - 16, W, 16, stroke=0, fill=1)
        self.caps(m, H - 62, 'Inkwell and Co', col=INK, size=6.8)
        self.caps(W - m, H - 62, 'Undated, start any day', right=True, col=INK, size=6.8)
        c.setFillColor(INK); c.setFont('Fr', 78)
        c.drawString(m - 4, H - 232, 'The'); c.drawString(m - 4, H - 312, 'Focus')
        c.setFillColor(CORAL); c.setFont('FrI', 78); c.drawString(m - 4, H - 392, 'Planner.')
        self.text(m, H - 434, 'An ADHD friendly planner for freelancers.', 'FrI', 19, TEAL)
        self.hl(m, W - m, H - 462, col=INK, w=1.3)
        big = ['Big type.', 'Few boxes.', 'One page at a time.']
        x = m
        for i, t in enumerate(big):
            self.sq(x, H - 496, 9, [CORAL, MUST, TEAL][i]); x += 17
            x += self.text(x, H - 497, t, 'FrM', 15.5, INK) + 24
        secs = [('Set up', 'How you work best, routines, a home for everything', NAVY), ('Capture', 'Brain dump, sort the pile, waiting on', TEAL),
                ('Week', 'Three priorities, time blocks, early deadlines', MUST), ('Day', 'One thing, sprints, low energy days, getting unstuck', CORAL),
                ('Projects', 'Small steps, time guesses, words for hard messages', TEAL), ('Money and admin', 'Admin hour, invoices, money dates, tax pot', MUST),
                ('Month', 'Calendar, focus, habits, wins, rest menu', SAGE), ('Extras', 'Call notes, routine cards, notes pages', NAVY)]
        y = H - 546; colw = self.w / 2
        for i, (a, b, col) in enumerate(secs):
            x = m + (i % 2) * colw; yy = y - (i // 2) * 44
            self.sq(x, yy - 1, 8, col)
            self.text(x + 18, yy - 1, a, 'FrM', 13.5, INK)
            self.text(x + 18, yy - 16, b, 'In', 8.9, SOFT, maxw=colw - 24)
        self.text(m, 62, '%d pages. %s, %s start. Print the pages you need, as many times as you like.' % (PAGES, self.tag, FULL[self.days[0]]), 'In', 9.2, SOFT)
        self.text(m, 47, 'Copyright 2026 Inkwell and Co. For personal use. Please do not resell or share the file.', 'In', 9.2, SOFT)
        self.done()

    def howto(self):
        top = self.head('How to use', 'this planner', 'Start here', toc=False); m = self.m; w = self.w
        y = top - 12
        y = self.para(m, y, w, 'Most planners ask you to fill in forty boxes a day, then make you feel bad when you do not. This one asks for less. '
                      'Each page does one job, the type is large, and nothing has a date on it, so a skipped week costs you nothing.', 'Fr', 13.4, 20, INK)
        y -= 16
        steps = [('Start with one page', 'Print "Today, simple". Use only that page for three days before you add anything else.'),
                 ('Empty your head first', 'When everything feels urgent, do a Brain dump, then turn the page and Sort the pile.'),
                 ('Plan the week in ten minutes', 'Week on a page holds three priorities and one main thing a day. That is enough.'),
                 ('Set up slowly', 'The Set up pages help you notice how you work best. Fill them in over a week or two, not in one sitting.'),
                 ('Skip pages without guilt', 'Use what helps and ignore the rest. Come back on any day. The planner does not keep score.')]
        for i, (t, b) in enumerate(steps):
            self.text(m, y - 8, '%d' % (i + 1), 'FrI', 32, self.ac)
            self.text(m + 40, y, t, 'FrM', 14.5, INK)
            y = self.para(m + 40, y - 18, w - 40, b, 'In', 10.8, 15.5, SOFT) - 15 - (self.H - 792) / 8
        g = 14; cw = (w - g) / 2; bh = 104
        rh_ = [('Every day', 'Two minutes', 'Fill in Today, simple.'), ('Every week', 'Twenty minutes', 'Do the Weekly reset.'),
               ('Every month', 'Twenty five minutes', 'Money check, Month review.')]
        yt = y + 2 - (self.H - 792) / 8; g3 = 12; bw = (w - 2 * g3) / 3; rhh = yt - (self.B + bh + 14) - 24
        self.label(m, yt - 4, 'A rhythm that is enough', col=INK)
        for i, (t1, t2, t3) in enumerate(rh_):
            x = m + i * (bw + g3); self.box(x, yt - 18 - rhh, bw, rhh)
            self.caps(x + 12, yt - 18 - 20, t1, size=6.8, col=INK)
            self.text(x + 12, yt - 18 - rhh / 2 - 8, t2, 'FrI', 15.5, self.ac, maxw=bw - 20)
            self.text(x + 12, yt - 18 - rhh + 13, t3, 'In', 9.2, SOFT, maxw=bw - 20)
        if rhh < 70: WARN.append('howto rhythm too short %s %.0f' % (self.tag, rhh))
        for i, (lab, txt) in enumerate([('Printing', 'Print at 100 percent or choose "fit to page". The margins leave room for a hole punch. '
                                         'The pages also work in any tablet app that lets you write on a PDF.'),
                                        ('Good to know', 'This is a planning tool made with ADHD in mind. It is not medical advice, a diagnosis or a treatment. '
                                         'The money pages help you keep records and are not tax advice.')]):
            x = m + i * (cw + g); self.box(x, self.B, cw, bh, fill=TINT, col=TINT)
            self.label(x + 14, self.B + bh - 22, lab)
            yy = self.para(x + 14, self.B + bh - 40, cw - 28, txt, 'In', 9.8, 14, INK)
            if yy < self.B + 2: WARN.append('howto box overflow ' + self.tag)
        self.done()

    def contents(self):
        top = self.head('What is', 'inside', 'Start here', toc=False); m = self.m; w = self.w
        g = 30; cw = (w - g) / 2; lead = 14.4
        groups = []
        for s, t, n in self.toc:
            if not groups or groups[-1][0] != s: groups.append((s, []))
            groups[-1][1].append((t, n))
        heights = [24 + lead * len(g_[1]) + 8 for g_ in groups]
        split = min(range(1, max(2, len(groups))), key=lambda k: max(sum(heights[:k]), sum(heights[k:])))
        fh = 92
        if max(sum(heights[:split]), sum(heights[split:])) - 12 > top - 8 - self.B - fh - 8: WARN.append('contents overflow ' + self.tag)
        pg = {t: n for _, t, n in self.toc}
        self.box(m, self.B, w, fh, fill=TINT, col=TINT)
        self.label(m + 14, self.B + fh - 20, 'Find your page fast', col=INK)
        find = [('Everything feels urgent', 'Brain dump'), ('I cannot get started', 'Getting unstuck'), ('The tank is empty', 'Low energy day'),
                ('I am drowning', 'When it is all too much'), ('I do not know what to say', 'Words for hard messages'), ('Money feels foggy', 'Ten minute money check')]
        fg = 18; fw = (w - 28 - 2 * fg) / 3
        for i, (a_, b_) in enumerate(find):
            x = m + 14 + (i % 3) * (fw + fg); yy = self.B + fh - 39 - (i // 3) * 30
            self.text(x, yy, a_, 'FrI', 10.8, INK, maxw=fw)
            tw = self.text(x, yy - 12.5, b_, 'In', 8.8, SOFT)
            self.text(x + fw, yy - 12.5, '%02d' % pg.get(b_, 0), 'FrI', 10, self.ac, right=True)
            if tw + 16 > fw: WARN.append('find too wide: ' + b_ + ' ' + self.tag)
            if self.toc and b_ not in pg: WARN.append('find missing: ' + b_)
        col = 0; y = top - 8
        for gi, (s, items) in enumerate(groups):
            if gi == split: col = 1; y = top - 8
            x = m + col * (cw + g)
            self.sq(x, y - 1.5, 7, SEC[s])
            self.caps(x + 14, y - 1, s, size=7.4, col=INK)
            self.hl(x, x + cw, y - 9, col=INK, w=0.9)
            y -= 24
            for t, n in items:
                self.text(x, y, t, 'In', 10.6, INK); self.text(x + cw, y, '%02d' % n, 'FrI', 11, SEC[s], right=True)
                y -= lead
            y -= 8
        self.done()

    # set up --------------------------------------------------------
    def howiwork(self):
        top = self.head('How I', 'work best', 'Set up', 'Fill this in over a few days. Guess first, correct later.')
        strip = 64; g = 14
        self.grid(top, self.B + strip + g, [('My best hours', 'When my head is clearest'), ('My slow hours', 'When hard work should not be booked'),
                                           ('What pulls me off track', 'Apps, places, kinds of task'), ('What gets me started', 'Music, a timer, a call, a deadline'),
                                           ('Work I get lost in', 'The good kind of lost'), ('Work I avoid', 'And what makes it easier')])
        self.box(self.m, self.B, self.w, strip, fill=TINT)
        self.label(self.m + 14, self.B + strip - 20, 'One thing I will stop expecting of myself')
        self.hl(self.m + 14, self.m + self.w - 14, self.B + 16, col=INK)
        self.done()

    def energymap(self):
        top = self.head('My energy', 'map', 'Set up', 'For one week, mark each block as full, half or empty. Then book hard work where the full blocks are.')
        m = self.m; w = self.w; rowsn = ['Early', 'Morning', 'Midday', 'Afternoon', 'Evening', 'Late']
        lw_ = 74; cw = (w - lw_) / 7; bot = 150; gt = top
        rh = (gt - 22 - self.B - bot - 16) / len(rowsn)
        for i, d in enumerate(self.days):
            self.caps(m + lw_ + i * cw + cw / 2, gt - 13, d, size=7.4, col=INK, center=True)
        for r, name in enumerate(rowsn):
            y = gt - 22 - r * rh
            self.text(m, y - rh / 2 - 4, name, 'FrM', 12, INK, maxw=lw_ - 6)
            for i in range(7):
                self.box(m + lw_ + i * cw + 3, y - rh + 3, cw - 6, rh - 6, col=LINE, lw=0.8, r=6)
        yk = gt - 22 - len(rowsn) * rh - 22
        self.label(m, yk, 'Key', col=INK)
        x = m + 44
        for t, f_ in [('Full', self.ac), ('Half', HexColor('#AEB6CC')), ('Empty', WHITE)]:
            self.box(x, yk - 4, 15, 15, col=INK, lw=0.8, r=4, fill=f_); x += 22
            x += self.text(x, yk, t, 'In', 10.6, INK) + 22
        g = 14; cw2 = (w - g) / 2; h = yk - 22 - self.B
        self.lbox(m, yk - 22, cw2, h, 'What I notice'); self.lbox(m + cw2 + g, yk - 22, cw2, h, 'What I will change')
        self.done()

    def routines(self):
        top = self.head('Start and', 'shutdown', 'Set up', 'Five steps or fewer. Short routines get done.')
        m = self.m; w = self.w; g = 14; cw = (w - g) / 2; ideas = 86
        h = top - self.B - ideas - g
        cols = [('Start of work', 'How I open the working day'), ('End of work', 'How I close it, so my head can rest')]
        for i, (a, b) in enumerate(cols):
            x = m + i * (cw + g); self.box(x, top - h, cw, h)
            self.label(x + 14, top - 20, a); self.text(x + 14, top - 36, b, 'FrI', 10.3, SOFT, maxw=cw - 28)
            step = (h - 56 - 40) / 5
            for k in range(5):
                y = top - 56 - (k + 1) * step
                self.text(x + 14, y + 6, '%d' % (k + 1), 'FrI', 24, self.ac)
                self.hl(x + 40, x + cw - 14, y + 4, col=INK if False else LINE)
            self.caps(x + 14, top - h + 16, 'Takes about', col=INK, size=6.8)
            self.hl(x + 80, x + cw - 70, top - h + 14, col=INK); self.caps(x + cw - 14, top - h + 16, 'minutes', col=INK, size=6.8, right=True)
        self.box(m, self.B, w, ideas, fill=TINT, col=TINT)
        self.label(m + 14, self.B + ideas - 21, 'Ideas to borrow')
        self.text(m + 14, self.B + ideas - 40, 'Start: fill a glass of water, open the Today page, set a timer for the first sprint, keep email closed until 11.', 'In', 9.6, INK, maxw=w - 28)
        self.text(m + 14, self.B + ideas - 56, 'End: write tomorrow\'s one thing, log your hours, close every tab, clear the desk, say "done" out loud.', 'In', 9.6, INK, maxw=w - 28)
        self.text(m + 14, self.B + ideas - 72, 'Tape the finished routine where you will see it, or use the Routine cards at the back.', 'FrI', 10, SOFT, maxw=w - 28)
        self.done()

    def ifthen(self):
        top = self.head('If this,', 'then that', 'Set up', 'Decide once, on a calm day, so you do not have to decide in the moment.')
        m = self.m; w = self.w; g = 14; cw = (w - g) / 2
        ex = [('a client asks for a call today', 'offer two times tomorrow'), ('I pick up my phone mid sprint', 'put it in another room until the timer rings'),
              ('a new idea shows up mid task', 'write it in the Parking lot and go back')]
        n = 8; rh = (top - self.B) / n
        for r in range(n):
            y = top - r * rh
            for k in range(2):
                x = m + k * (cw + g)
                self.box(x, y - rh + 10, cw, rh - 10, fill=TINT if r < 3 else None, col=INK if r >= 3 else TINT)
                self.label(x + 12, y - 17, ['If', 'Then I will'][k], col=self.ac if r >= 3 else INK)
                if r < 3: self.text(x + 12, y - rh / 2 - 9, ex[r][k], 'FrI', 10.6, INK, maxw=cw - 22)
                else: self.hl(x + 12, x + cw - 12, y - rh + 24)
            self.text(m + cw + g / 2, y - rh / 2 - 3, '>', 'FrM', 12, SOFT, center=True)
        self.done()

    def homes(self):
        top = self.head('A home for', 'everything', 'Set up', 'Looking for things eats hours. Give each one a single home and write it down here.')
        first = ['Client briefs', 'Contracts', 'Invoices I sent', 'Receipts', 'Passwords', 'Working files', 'Final files', 'Notes from calls', 'Ideas', 'To do lists']
        yb = self.note('One home each. If a thing has two homes, it has none.')
        self.table(top, [('Thing', .30), ('Where it lives', .52), ('Tidy', .18)], yb=yb, first=first, rh=30, checkcol=2)
        self.done()

    # capture -------------------------------------------------------
    def dotarea(self, x, yb, w, yt, s=17):
        c = self.c; c.setFillColor(HexColor('#9499AD'))
        n = int(w / s); off = (w - n * s) / 2; y = yt
        while y >= yb:
            for i in range(n + 1): c.circle(x + off + i * s, y, 0.65, stroke=0, fill=1)
            y -= s

    def braindump(self):
        top = self.head('Brain', 'dump', 'Capture', 'Set a timer for ten minutes. Write down everything in your head, work and life. Do not sort yet.')
        yb = self.note('Finished? Turn the page and sort the pile.')
        self.box(self.m, yb, self.w, top - yb)
        self.dotarea(self.m + 16, yb + 16, self.w - 32, top - 18)
        self.done()

    def sortpile(self):
        top = self.head('Sort the', 'pile', 'Capture', 'Move every line of the brain dump into one of four places. Nothing stays in your head.')
        self.grid(top, self.B, [('Do this week', 'Three to five things, no more'), ('Put on the calendar', 'It has a date, and the date is not this week'),
                               ('Ask or hand off', 'Someone else can do it or answer it'), ('Let it go', 'Cross it out. You are allowed.')], checks=True)
        self.done()

    def waiting(self):
        top = self.head('Waiting', 'on', 'Capture', 'Things you have handed over still need a place to sit. Check this page at every weekly reset.')
        self.table(top, [('What I am waiting for', .40), ('From', .20), ('Asked on', .14), ('Nudge on', .14), ('Got it', .12)], yb=self.B, rh=30, checkcol=4)
        self.done()

    # week ----------------------------------------------------------
    def weekpage(self):
        top = self.head('Week on', 'a page', 'Week'); m = self.m; w = self.w
        self.field(m, top - 2, 'Week of', w * 0.42)
        y = top - 24; ph = 112
        self.box(m, y - ph, w, ph, fill=TINT)
        self.label(m + 14, y - 20, 'Three priorities. If these get done, the week was a good one.', maxw=w - 28)
        for k in range(3):
            yy = y - 46 - k * 26
            self.text(m + 14, yy - 4, '%d' % (k + 1), 'FrI', 19, self.ac); self.hl(m + 36, m + w - 14, yy - 4, col=INK)
        y -= ph + 12
        rh = (y - self.B) / 7; dw = 92; aw = w * 0.30
        self.caps(m + dw, y - 2, 'The main thing', size=6.8, col=INK); self.caps(m + w - aw + 12, y - 2, 'Calls and appointments', size=6.8, col=INK, maxw=aw - 12)
        y -= 8; rh = (y - self.B) / 7
        for i, d in enumerate(self.days):
            yy = y - i * rh
            self.hl(m, m + w, yy, col=INK, w=1.2 if i == 0 else 0.7)
            self.text(m, yy - rh / 2 - 5, FULL[d], 'FrM', 13.5, INK, maxw=dw - 6)
            self.check(m + dw, yy - rh / 2 - 7)
            self.hl(m + dw + 22, m + w - aw, yy - rh / 2 - 7)
            self.vl(m + w - aw + 6, yy - rh + 7, yy - 7, col=HAIR)
            self.hl(m + w - aw + 12, m + w, yy - rh / 2 - 7, col=LINE)
        self.hl(m, m + w, y - 7 * rh, col=INK, w=1.2)
        self.done()

    def timeblocks(self):
        top = self.head('Time', 'blocks', 'Week', 'Four blocks a day, not twenty time slots. Give each block one kind of work, and leave one block empty every day.')
        m = self.m; w = self.w; rowsn = ['Morning', 'Midday', 'Afternoon', 'Evening']
        lw_ = 76; cw = (w - lw_) / 7; keyh = 52
        rh = (top - 22 - self.B - keyh) / 4
        for i, d in enumerate(self.days):
            self.caps(m + lw_ + i * cw + cw / 2, top - 13, d, size=7.4, col=INK, center=True)
        for r, name in enumerate(rowsn):
            y = top - 22 - r * rh
            self.text(m, y - 20, name, 'FrM', 12, INK, maxw=lw_ - 6)
            for i in range(7):
                self.box(m + lw_ + i * cw + 3, y - rh + 3, cw - 6, rh - 6, col=LINE, lw=0.8, r=6)
        self.label(m, self.B + 22, 'Kinds of block', col=INK)
        ks = ['Deep work', 'Client calls', 'Admin', 'Errands', 'Rest']; x = m
        for i, k in enumerate(ks):
            self.box(x, self.B, 14, 14, r=4, lw=0.8); x += 20
            x += self.text(x, self.B + 3, k, 'In', 10.4, INK) + 22
        self.text(m + w, self.B + 22, 'Color the squares to make your own key.', 'FrI', 10, SOFT, right=True)
        if x - 22 > m + w: WARN.append('timeblocks key too wide ' + self.tag)
        self.done()

    def deadlines(self):
        top = self.head('Real and', 'early deadlines', 'Week', 'Write the real due date. Then give yourself a date two days earlier and work to that one.')
        yb = self.note('The gap between the two dates is your buffer. Guard it.')
        self.table(top, [('Project or task', .30), ('Client', .16), ('Real due', .12), ('My date', .12), ('First small step', .22), ('Done', .08)], yb=yb, rh=32, checkcol=5)
        self.done()

    def reset(self):
        top = self.head('Weekly', 'reset', 'Week', 'Same day, same time, every week. About twenty minutes. Put on music you like.')
        m = self.m; w = self.w; g = 22; cw = (w - g) / 2
        y = self.fields(top - 2, [('My reset day', .5), ('Time', .5)]) - 6
        groups = [('Clear', ['Brain dump everything on my mind', 'Sort the pile', 'Clear the desk and the downloads folder', 'Check Waiting on and send nudges']),
                  ('Money', ['Send invoices for finished work', 'Chase invoices that are late', 'Move tax money to the tax pot']),
                  ('Plan', ['Look at the calendar, two weeks ahead', 'Check Real and early deadlines', 'Choose three priorities', 'Fill in Week on a page']),
                  ('Kind', ['Plan one thing to look forward to', 'Write one win on the Wins page'])]
        pos = [(0, y), (1, y)]
        hgt = lambda items, extra: 22 + (len(items) + extra) * 26 + 16
        extras = [2, 2, 2, 3]; st = min(34, (y - self.B - 86 - 2 * 54) / 11)
        ys = [y, y]
        for gi, (lab, items) in enumerate(groups):
            col = 0 if gi in (0, 1) else 1
            x = m + col * (cw + g); yy = ys[col]
            self.sq(x, yy - 9, 8); self.caps(x + 15, yy - 8, lab, size=8, col=INK)
            self.hl(x, x + cw, yy - 16, col=INK, w=1.0)
            yy = self.checklist(x, yy - 22, cw, items, n=extras[gi], size=10.4, step=st)
            ys[col] = yy - 16
        if min(ys) < self.B - 20: WARN.append('reset overflow %s %.0f' % (self.tag, min(ys)))
        yb = min(ys) + 6
        if yb - self.B > 44:
            h = min(yb - self.B - 6, 104)
            self.box(m, self.B, w, h, fill=TINT, col=TINT)
            self.label(m + 14, self.B + h - 21, 'The one thing next week is really about')
            self.hl(m + 14, m + w - 14, self.B + 15, col=INK)
        self.done()

    def weekreview(self):
        top = self.head('Week', 'review', 'Week', 'Five minutes. Honest, short and kind.'); m = self.m; w = self.w
        sh = 78
        self.grid(top, self.B + sh + 14, [('What went well', None), ('What got in the way', None),
                                         ('Carrying over to next week', 'Only what still matters'), ('One thing I will do differently', None)])
        self.box(m, self.B, w, sh, fill=TINT, col=TINT)
        self.label(m + 14, self.B + sh - 24, 'My energy', col=INK)
        self.options(m + 110, self.B + sh - 26, ['Empty', 'Low', 'Fine', 'Good', 'Full'], w - 124)
        self.label(m + 14, self.B + 20, 'My workload', col=INK)
        self.options(m + 110, self.B + 18, ['Too little', 'About right', 'Too much'], w - 124)
        self.done()

    # day -----------------------------------------------------------
    def today(self):
        top = self.head('Today,', 'simple', 'Day'); m = self.m; w = self.w
        self.field(m, top - 2, 'Date', w * 0.42)
        y = top - 26; oh = 118
        self.box(m, y - oh, w, oh, fill=TINT)
        self.label(m + 16, y - 22, 'The one thing')
        self.text(m + 16, y - 39, 'If only this gets done, today counts.', 'FrI', 10.6, SOFT)
        self.check(m + 16, y - oh + 24, 20); self.hl(m + 48, m + w - 16, y - oh + 24, col=INK, w=0.9)
        y -= oh + 22
        self.label(m, y, 'Then, if there is time'); y -= 6
        for k in range(3):
            y -= 30; self.check(m, y); self.hl(m + 22, m + w, y)
        y -= 30
        g = 14; cw = (w - g) / 2; fh = 46; h = y - self.B - fh - 10
        self.lbox(m, y, cw, h, 'Calls and appointments', step=28)
        self.lbox(m + cw + g, y, cw, h, 'Not today', hint='Things I am allowed to leave', step=28)
        self.label(m, self.B + 14, 'Breaks taken', col=INK)
        for k in range(4): self.circ(m + 96 + k * 24, self.B + 17, 7.5)
        self.field(m + w * 0.56, self.B + 14, 'I stopped work at', w * 0.44)
        self.done()

    def timebox(self):
        top = self.head('Today,', 'time boxed', 'Day', 'For days with many moving parts. Write your own hours down the left side.'); m = self.m; w = self.w
        y = self.fields(top - 2, [('Date', .34), ('The one thing', .66)]) - 2
        tw = 64; a = (w - tw) * 0.5
        rows = 11; rh = (y - 22 - self.B) / rows
        self.hl(m, m + w, y, col=INK, w=1.2); self.hl(m, m + w, y - 22, col=INK)
        self.caps(m + 2, y - 14.5, 'Hour', size=6.9, col=INK); self.caps(m + tw + 8, y - 14.5, 'The plan', size=6.9, col=INK)
        self.caps(m + tw + a + 8, y - 14.5, 'What really happened', size=6.9, col=INK)
        for r in range(1, rows + 1):
            yy = y - 22 - r * rh; self.hl(m, m + w, yy, col=INK if r == rows else LINE, w=1.0 if r == rows else 0.7)
        self.vl(m + tw, y - 22 - rows * rh, y - 22, col=HAIR); self.vl(m + tw + a, y - 22 - rows * rh, y - 22, col=HAIR)
        self.done()

    def lowenergy(self):
        top = self.head('Low energy', 'day', 'Day', 'Some days the tank is empty. Do the minimum, keep clients informed, and rest without guilt.')
        m = self.m; w = self.w; g = 14; cw = (w - g) / 2
        hh = 92; sh = 64
        h1 = (top - self.B - hh - sh - 3 * g) / 2
        self.lbox(m, top, w, h1, 'The bare minimum', hint='Only what would cause a real problem tomorrow if I skipped it', checks=True)
        y = top - h1 - g
        self.lbox(m, y, cw, h1, 'Messages to send', hint='So no one is left waiting', checks=True)
        self.lbox(m + cw + g, y, cw, h1, 'Easy tasks', hint='Things I can do on autopilot', checks=True)
        y -= h1 + g
        self.box(m, y - hh, w, hh, fill=TINT, col=TINT)
        self.label(m + 14, y - 21, 'What would help right now', col=INK)
        self.options(m + 14, y - 47, ['Food', 'Water', 'Fresh air', 'A nap', 'A walk'], w - 28)
        self.options(m + 14, y - 73, ['A shower', 'Music', 'Quiet', 'A call with a friend'], w - 28)
        y -= hh + g
        self.box(m, self.B, w, sh)
        self.label(m + 14, self.B + sh - 20, 'Moved to another day, on purpose')
        self.hl(m + 14, m + w - 14, self.B + 16)
        self.done()

    def overwhelm(self):
        top = self.head('When it is', 'all too much', 'Day', 'Work down the page, one step at a time. You only need the next ten minutes.')
        m = self.m; w = self.w; nh = 54
        avail = top - self.B - nh - 14
        steps = [('Breathe out slowly, five times.', 'c', 1.0), ('Write the three things making the most noise.', 'l3', 2.0),
                 ('Circle the one with the nearest real deadline.', None, 0.72), ('Who needs a short message from me?', 'l2', 1.6),
                 ('What will I do in the next ten minutes?', 'l1', 1.25)]
        unit = avail / sum(s[2] for s in steps); y = top
        for i, (t, kind, k) in enumerate(steps):
            h = unit * k
            self.hl(m, m + w, y, col=INK, w=1.2 if i == 0 else 0.7)
            self.text(m, y - 36, '%d' % (i + 1), 'FrI', 34, self.ac)
            self.text(m + 44, y - 28, t, 'FrM', 14.5, INK, maxw=w - 44)
            if kind == 'c':
                for q in range(5): self.circ(m + 54 + q * 30, y - 52, 9)
            elif kind:
                n = int(kind[1]); st = min(28, (h - 44) / n)
                for q in range(n): self.hl(m + 44, m + w, y - 40 - (q + 1) * st + 4)
            y -= h
        self.hl(m, m + w, y, col=INK, w=1.2)
        self.c.setFillColor(TINT); self.c.roundRect(m, self.B, w, nh, 7, stroke=0, fill=1)
        self.text(m + w / 2, self.B + nh / 2 - 5, 'Everything else can wait until tomorrow.', 'FrI', 15, INK, center=True)
        self.done()

    def sprints(self):
        top = self.head('Focus', 'sprints', 'Day', 'Pick one task. Set a timer. Work until it rings, then take the break. Fill one circle for each sprint.')
        m = self.m; w = self.w
        y = self.fields(top - 2, [('Date', .34), ('Sprint length', .33), ('Break length', .33)]) - 4
        ph = 124; n = 6; rh = (y - self.B - ph - 14) / n; cwid = 4 * 26 + 6
        self.caps(m + 2, y - 2, 'Task', size=6.9, col=INK); self.caps(m + w, y - 2, 'Sprints done', size=6.9, col=INK, right=True)
        y -= 9
        for r in range(n):
            yy = y - r * rh
            self.hl(m, m + w, yy, col=INK, w=1.2 if r == 0 else 0.7)
            self.text(m, yy - rh / 2 - 8, '%d' % (r + 1), 'FrI', 22, self.ac)
            self.hl(m + 30, m + w - cwid - 14, yy - rh / 2 - 8)
            for q in range(4): self.circ(m + w - cwid + 13 + q * 26, yy - rh / 2 - 2, 9)
        self.hl(m, m + w, y - n * rh, col=INK, w=1.2)
        self.lbox(m, self.B + ph, w, ph, 'Thoughts that tried to interrupt', hint='Park them here and go back to the task. They will keep.', fill=None)
        self.done()

    def unstuck(self):
        top = self.head('Getting', 'unstuck', 'Day', 'For the task you keep avoiding. Make the first step so small it feels silly.')
        m = self.m; w = self.w; g = 16; n = 2
        bh = (top - self.B - g * (n - 1)) / n
        for k in range(n):
            yt = top - k * (bh + g); self.box(m, yt - bh, w, bh)
            x = m + 16; iw = w - 32
            rows = [('The task I keep avoiding', 'line'), ('It feels', 'opt'), ('The first two minutes', 'line'), ('After that', 'line'), ('My reward when it is done', 'line')]
            step = (bh - 20) / len(rows)
            for i, (lab, kind) in enumerate(rows):
                yy = yt - 12 - i * step
                self.label(x, yy - 12, lab, col=self.ac if i in (0, 2) else INK)
                if kind == 'opt': self.options(x, yy - 34, ['Too big', 'Unclear', 'Boring', 'Scary', 'Blocked'], iw)
                else: self.hl(x, x + iw, yy - step + 14, col=INK if i == 2 else LINE, w=0.9 if i == 2 else 0.7)
        self.done()

    def donelist(self):
        top = self.head('Done', 'list', 'Day', 'Write things down after you do them. On days that feel like nothing happened, this page says otherwise.')
        m = self.m; w = self.w
        self.field(m, top - 2, 'Date or week', w * 0.42)
        y = top - 26; yb = self.note('Small things count. Answering that email counts.')
        step = 30; n = int((y - yb) / step)
        for k in range(n):
            yy = y - (k + 1) * step + 4
            self.c.setFillColor(self.ac); self.c.circle(m + 4, yy + 5, 3.2, stroke=0, fill=1)
            self.hl(m + 18, m + w, yy)
        self.done()

    # projects ------------------------------------------------------
    def project(self):
        top = self.head('Project on', 'a page', 'Projects'); m = self.m; w = self.w
        y = self.fields(top - 2, [('Project', .6), ('Client', .4)])
        y = self.fields(y, [('Due date', .34), ('My early date', .33), ('Fee', .33)]) - 4
        g = 14; cw = (w - g) / 2
        mh = 150; bh = (y - self.B - mh - 2 * g) / 2
        self.lbox(m, y, w, bh, 'Done looks like', hint='What the client will have in their hands at the end')
        y -= bh + g
        self.box(m, y - mh, w, mh, fill=TINT, col=TINT)
        self.label(m + 14, y - 21, 'Three milestones', col=INK); self.caps(m + w - 14, y - 21, 'By when', col=INK, size=6.8, right=True)
        for k in range(3):
            yy = y - 54 - k * 36
            self.check(m + 14, yy); self.text(m + 38, yy + 1, '%d' % (k + 1), 'FrI', 18, self.ac)
            self.hl(m + 58, m + w - 120, yy, col=INK); self.hl(m + w - 104, m + w - 14, yy, col=INK)
        y -= mh + g
        self.lbox(m, y, cw, bh, 'People and links', hint='Contacts, folders, logins')
        self.lbox(m + cw + g, y, cw, bh, 'What could slow this down', hint='And what I will do about it')
        self.done()

    def breakdown(self):
        top = self.head('Break it', 'down', 'Projects', 'List steps small enough to finish in one sitting. If a step needs more than two hours, split it.')
        y = self.fields(top - 2, [('Project', .5), ('The very first step', .5)]) - 4
        self.table(y, [('No.', .08), ('Step', .50), ('Time guess', .15), ('Real time', .15), ('Done', .12)], yb=self.B, rh=30, checkcol=4)
        self.done()

    def timeguess(self):
        top = self.head('Time guess', 'and real time', 'Projects', 'Guess before you start. Write the real time after. Ten tasks in, you will know your multiplier.')
        sh = 62; yb = self.note('Multiply every future quote and deadline by your number.') + sh + 2
        self.stats(yb - 2, ['Total guessed', 'Total real', 'Real divided by guess'], h=sh, fill=None)
        self.table(top, [('Task', .46), ('My guess', .18), ('Real time', .18), ('Difference', .18)], yb=yb + 12, rh=28)
        self.done()

    def backwards(self):
        top = self.head('Working', 'backwards', 'Projects', 'Start from the due date and plan back to today. The buffer goes in first, not last.')
        m = self.m; w = self.w
        y = self.fields(top - 2, [('Project', .6), ('Client', .4)]) - 6
        rows = [('Due date', 'The date the client expects it'), ('Buffer', 'Two or more spare days. Do not plan work here.'), ('Final check and send', 'Proofread, export, write the handover note'),
                ('Changes from the client', 'Time for them to reply, and for me to revise'), ('First version to the client', 'Good enough to react to, not perfect'),
                ('Halfway check', 'Am I on track? If not, tell the client now.'), ('Start', 'The first small step, on a real date')]
        rh = (y - self.B) / len(rows); dw = 104; lx = m + 34
        self.vl(m + 10, y - rh / 2, y - rh * (len(rows) - 0.5), col=INK, w=1.2)
        for i, (a, b) in enumerate(rows):
            yy = y - i * rh; cy = yy - rh / 2
            self.circ(m + 10, cy, 8, fill=self.ac if i in (0, len(rows) - 1) else WHITE)
            self.text(lx, cy + 6, a, 'FrM', 13.5, INK); self.text(lx, cy - 10, b, 'FrI', 10, SOFT, maxw=w - 34 - dw - 14)
            self.box(m + w - dw, cy - 17, dw, 34, r=6, fill=TINT if i == 1 else None)
            self.caps(m + w - dw + 8, cy + 7, 'Date', size=5.8, col=SOFT)
            if i: self.hl(lx, m + w, yy, col=HAIR)
        self.done()

    def messages(self):
        top = self.head('Messages', 'to answer', 'Projects', 'Read it once, write it here, close the inbox. Answer them all in one batch.')
        yb = self.note('Stuck on what to say? The next page has words you can borrow.')
        self.table(top, [('From', .22), ('About', .42), ('Reply by', .18), ('Sent', .18)], yb=yb, rh=30, checkcol=3)
        self.done()

    def scripts(self):
        top = self.head('Words for', 'hard messages', 'Projects', 'Borrow these, change the parts in brackets, and send before you can overthink it.')
        m = self.m; w = self.w
        items = [('I need more time', 'Hi [name], I want to give this the care it needs. I can deliver on [new date] instead of [old date]. Does that work for you?'),
                 ('That is extra work', 'Happy to add that. It is outside what we agreed, so it would add [fee] and [days] to the project. Shall I go ahead?'),
                 ('The invoice is late', 'Hi [name], a quick reminder that invoice [number] for [amount] was due on [date]. Could you tell me when it will be paid?'),
                 ('I cannot take this on', 'Thank you for thinking of me. I am not able to take this project on right now. I hope it goes really well.'),
                 ('Sorry I went quiet', 'Sorry for the slow reply. Here is where things stand: [update]. You will hear from me next on [date].')]
        bh = (top - self.B) / len(items)
        for i, (a, b) in enumerate(items):
            y = top - i * bh
            self.hl(m, m + w, y, col=INK, w=1.2 if i == 0 else 0.7)
            self.sq(m, y - 24, 8); self.text(m + 16, y - 25, a, 'FrM', 14, INK)
            yy = self.para(m + 16, y - 45, w - 16, b, 'FrI', 11.2, 16, INK)
            self.caps(m + 16, y - bh + 14, 'My version', size=6.4, col=SOFT)
            self.hl(m + 84, m + w, y - bh + 12)
            if yy < y - bh + 22: WARN.append('script overflow %d %s' % (i, self.tag))
        self.hl(m, m + w, top - len(items) * bh, col=INK, w=1.2)
        self.done()

    def parking(self):
        top = self.head('Parking', 'lot', 'Projects', 'New ideas are welcome, just not right now. Park them here and look again at the month review.')
        self.table(top, [('The idea', .36), ('Why it excites me', .32), ('Look again on', .16), ('Verdict', .16)], yb=self.B, rh=34)
        self.done()

    # money and admin -----------------------------------------------
    def adminhour(self):
        top = self.head('Admin', 'power hour', 'Money and admin', 'One hour, one timer, once a week. Start at the top and stop when it rings.')
        m = self.m; w = self.w; g = 22; cw = (w - g) * 0.56; rw = w - g - cw
        y = self.fields(top - 2, [('My admin day', .5), ('Time', .5)]) - 4
        items = ['Send invoices for finished work', 'Chase invoices past their due date', 'Log income and move tax money', 'File or photograph receipts',
                 'Answer the messages on my list', 'Send proposals and follow ups', 'Check Money dates for the next ten days', 'Back up current project files']
        self.sq(m, y - 9, 8); self.caps(m + 15, y - 8, 'Every week', size=8, col=INK); self.hl(m, m + cw, y - 16, col=INK, w=1.0)
        self.checklist(m, y - 22, cw, items, ybot=self.B, size=10.4, step=28)
        x = m + cw + g
        self.lbox(x, y, rw, y - self.B, 'This week only', hint='Odd jobs that came up', checks=True, step=28)
        self.done()

    def invoices(self):
        top = self.head('Invoices', 'out', 'Money and admin', 'Send the invoice the day the work is done. Check this page at every admin hour.')
        self.table(top, [('Client', .22), ('For', .24), ('Amount', .14), ('Sent', .11), ('Due', .11), ('Chased', .10), ('Paid', .08)], yb=self.B, rh=30, checkcol=6, total='Still owed to me')
        self.done()

    def moneydates(self):
        top = self.head('Money', 'dates', 'Money and admin', 'Write every date that money leaves or a form is due. Then set a phone reminder three days before each one.')
        m = self.m; w = self.w
        yh = 22 + 4 * 28 + 30
        self.label(m, top - 2, 'Every month')
        yb = self.table(top - 12, [('Day', .12), ('What', .42), ('Amount', .18), ('Auto pay', .14), ('Reminder', .14)], yb=self.B + yh + 14, rh=28, checkcol=4)
        y2 = self.B + yh
        self.label(m, y2 - 2, 'Once a year')
        self.table(y2 - 12, [('Date', .18), ('What', .50), ('Amount', .18), ('Reminder', .14)], rows=4, rh=28, checkcol=3,
                   first=['', '', '', ''])
        self.done()

    def subs(self):
        top = self.head('Bills and', 'subscriptions', 'Money and admin', 'List everything that renews on its own. Cancel what you have not opened in a month.')
        self.table(top, [('Name', .30), ('Cost', .15), ('How often', .18), ('Renews on', .19), ('Keep', .09), ('Cancel', .09)], yb=self.B, rh=30, total='Total each month', checkcol=[4, 5])
        self.done()

    def income(self):
        top = self.head('Income this', 'month', 'Money and admin'); m = self.m; w = self.w
        y = self.fields(top - 2, [('Month', .4), ('Tax pot percent', .3), ('Target', .3)]) - 4
        sh = 62
        self.stats(self.B + sh, ['Received', 'In the tax pot', 'Still to reach my target'], h=sh)
        self.table(y, [('Date', .14), ('Client', .34), ('Amount', .18), ('To tax pot', .18), ('Moved', .16)], yb=self.B + sh + 16, rh=29, checkcol=4, total='Total')
        self.done()

    def moneycheck(self):
        top = self.head('Ten minute', 'money check', 'Money and admin', 'Once a month. Open the bank app, fill in six numbers, close the app. That is the whole job.')
        m = self.m; w = self.w; bw = 150; sh = 78
        rows = [('In my business account today', None), ('Invoices still owed to me', 'From the Invoices out page'), ('Bills due before the month ends', 'From Money dates'),
                ('In the tax pot', 'Do not count this as yours'), ('Earned this month so far', 'From Income this month'), ('What I can pay myself', 'Account, minus bills, minus tax')]
        rh = (top - self.B - sh - 16) / len(rows)
        for i, (a, b) in enumerate(rows):
            y = top - i * rh; last = i == len(rows) - 1
            self.hl(m, m + w, y, col=INK, w=1.2 if i == 0 else 0.7)
            self.text(m, y - rh / 2 - 8, '%d' % (i + 1), 'FrI', 26, self.ac)
            self.text(m + 36, y - rh / 2 + (2 if b else -4), a, 'FrM', 13.5, INK)
            if b: self.text(m + 36, y - rh / 2 - 13, b, 'FrI', 10, SOFT)
            self.box(m + w - bw, y - rh + 9, bw, rh - 18, fill=TINT if last else None, lw=1.2 if last else 0.9)
        self.hl(m, m + w, top - len(rows) * rh, col=INK, w=1.2)
        self.box(m, self.B, w, sh)
        self.label(m + 14, self.B + sh - 21, 'One money task for this week')
        self.check(m + 14, self.B + 16); self.hl(m + 36, m + w - 14, self.B + 16)
        self.done()

    # month ---------------------------------------------------------
    def mcal(self):
        top = self.head('Month at', 'a glance', 'Month'); m = self.m; w = self.w
        y = self.fields(top - 2, [('Month', .42), ('One word for this month', .58)]) - 2
        cw = w / 7; rows = 6; rh = (y - 20 - self.B) / rows
        for i, d in enumerate(self.days):
            self.caps(m + i * cw + 5, y - 12, d, size=7.2, col=INK)
        gy = y - 20
        self.c.setStrokeColor(INK); self.c.setLineWidth(1.0); self.c.roundRect(m, gy - rows * rh, w, rows * rh, 7, stroke=1, fill=0)
        for r in range(1, rows): self.hl(m, m + w, gy - r * rh, col=LINE)
        for i in range(1, 7): self.vl(m + i * cw, gy - rows * rh, gy, col=LINE)
        self.done()

    def mfocus(self):
        top = self.head('Month', 'focus', 'Month', 'One theme, three outcomes, and a short list of things you are choosing not to do.'); m = self.m; w = self.w
        g = 14; cw = (w - g) / 2; th = 76; oh = 146
        self.box(m, top - th, w, th, fill=TINT)
        self.label(m + 14, top - 21, 'This month is about'); self.hl(m + 14, m + w - 14, top - th + 18, col=INK)
        y = top - th - g
        self.box(m, y - oh, w, oh)
        self.label(m + 14, y - 21, 'Three outcomes'); self.text(m + 14, y - 37, 'Things I can point to at the end of the month', 'FrI', 10.3, SOFT)
        for k in range(3):
            yy = y - 66 - k * 30
            self.check(m + 14, yy); self.hl(m + 36, m + w - 14, yy)
        y -= oh + g
        sh = 66; bh = y - self.B - sh - g
        self.lbox(m, y, cw, bh, 'Not this month', hint='Good ideas that have to wait')
        self.lbox(m + cw + g, y, cw, bh, 'Dates I must not miss', hint='Deadlines, renewals, birthdays')
        self.box(m, self.B, w, sh)
        self.label(m + 14, self.B + sh - 20, 'Something to look forward to'); self.hl(m + 14, m + w - 14, self.B + 16)
        self.done()

    def quarter(self):
        top = self.head('Thirteen', 'weeks', 'Month', 'A quarter on one page. One line a week is plenty.')
        self.table(top, [('Week', .09), ('Starts', .14), ('Main focus', .47), ('Big deadline', .30)], yb=self.B, rows=13,
                   rh=(top - 22 - self.B) / 13, first=['%d' % i for i in range(1, 14)])
        self.done()

    def habits(self):
        top = self.head('Habit', 'tracker', 'Month', 'Five habits at most. A missed day means nothing. Just fill in the next circle.')
        m = self.m; w = self.w
        y = self.fields(top - 2, [('Month', .42)]) + 4
        yb = self.note('Start with one habit. Add a second when the first feels easy.')
        n = 5; bh = (y - yb) / n; cs = w / 16
        for k in range(n):
            yt = y - k * bh
            self.text(m, yt - 22, '%d' % (k + 1), 'FrI', 22, self.ac); self.hl(m + 26, m + w, yt - 22, col=INK)
            r = min(cs / 2 - 3.2, (bh - 46) / 4 - 2.5)
            for d in range(31):
                row, col = divmod(d, 16)
                cx = m + col * cs + cs / 2; cy = yt - 34 - r - row * (2 * r + 5) - 4
                self.circ(cx, cy, r, col=LINE, lw=0.8)
                self.text(cx, cy - 2.6, '%d' % (d + 1), 'In', 7.2, SOFT, center=True)
        self.done()

    def wins(self):
        top = self.head('Wins', '', 'Month', 'Small ones count. Sending the invoice counts. Read this page when your brain says you did nothing.')
        self.table(top, [('Date', .18), ('The win', .82)], yb=self.B, rh=32)
        self.done()

    def restmenu(self):
        top = self.head('Rest', 'menu', 'Month', 'Choose your breaks before you need them. A tired brain reaches for the phone.')
        m = self.m; w = self.w; g = 14; sh = 118
        cw = (w - 2 * g) / 3; h = top - self.B - sh - g
        for i, (a, b) in enumerate([('Five minutes', 'Between sprints'), ('Half an hour', 'A real break'), ('Half a day', 'A proper reset')]):
            self.lbox(m + i * (cw + g), top, cw, h, a, hint=b, step=30)
        self.lbox(m, self.B + sh, w, sh, 'Signs that I need a break', hint='How my body and my work tell me, before I notice', fill=TINT)
        self.done()

    def mreview(self):
        top = self.head('Month', 'review', 'Month', 'Fifteen minutes with a drink you like. Look back first, then forward.'); m = self.m; w = self.w
        sh = 58; g = 14
        self.stats(top, ['Earned', 'Invoices still out', 'Days off taken'], h=sh)
        y = top - sh - g
        self.grid(y, self.B, [('I am proud of', None), ('This was hard', None), ('Keep doing', None), ('Stop doing', None),
                             ('Try next month', None), ('From the Parking lot', 'One idea worth a closer look')])
        self.done()

    # extras --------------------------------------------------------
    def callnotes(self):
        top = self.head('Call', 'notes', 'Extras'); m = self.m; w = self.w
        y = self.fields(top - 2, [('With', .42), ('About', .34), ('Date', .24)]) - 4
        g = 14; cw = (w - g) / 2; bh = 96; ah = 150
        self.lbox(m, y, w, bh, 'Before the call', hint='What I need to find out or agree')
        y -= bh + g
        nh = y - self.B - ah - g
        self.lbox(m, y, w, nh, 'Notes')
        y -= nh + g
        self.lbox(m, y, cw, ah, 'I will do', checks=True); self.lbox(m + cw + g, y, cw, ah, 'They will do', checks=True)
        self.done()

    def cowork(self):
        top = self.head('Work with me', 'sessions', 'Extras', 'Working next to someone, in a room or on a video call, makes starting easier. Log your sessions here.')
        yb = self.note('Say out loud what you will do. Then do only that.')
        self.table(top, [('Date', .14), ('With', .20), ('I said I would', .52), ('Did it', .14)], yb=yb, rh=32, checkcol=3)
        self.done()

    def cards(self):
        top = self.head('Routine', 'cards', 'Extras', 'Cut along the dashed lines, fill them in, and stand them where you work.')
        m = self.m; w = self.w; g = 16
        names = ['Start of work', 'End of work', 'Weekly reset', 'When I am stuck']
        cw = (w - g) / 2; ch = (top - self.B - g) / 2
        for i, nm in enumerate(names):
            x = m + (i % 2) * (cw + g); yt = top - (i // 2) * (ch + g)
            self.box(x, yt - ch, cw, ch, col=SOFT, lw=0.9, dash=(4, 3), r=10)
            self.c.setFillColor(TINT); self.c.roundRect(x + 10, yt - 46, cw - 20, 36, 6, stroke=0, fill=1)
            self.sq(x + 22, yt - 32, 8, [NAVY, CORAL, MUST, TEAL][i]); self.text(x + 38, yt - 33, nm, 'FrM', 14, INK)
            n = 5; st = (ch - 62) / n
            for k in range(n):
                yy = yt - 52 - (k + 1) * st + 8
                self.text(x + 20, yy + 2, '%d' % (k + 1), 'FrI', 17, SOFT); self.hl(x + 40, x + cw - 20, yy)
        self.done()

    def lined(self):
        top = self.head('Notes', '', 'Extras')
        self.lines(self.m, self.m + self.w, top - 22, self.B, step=28)
        self.done()

    def dots(self):
        top = self.head('Dot', 'grid', 'Extras')
        self.dotarea(self.m, self.B, self.w, top - 8)
        self.done()

    def build(self):
        self.n = 1; self.cover(); self.howto(); self.contents()
        self.howiwork(); self.energymap(); self.routines(); self.ifthen(); self.homes()
        self.braindump(); self.sortpile(); self.waiting()
        self.weekpage(); self.timeblocks(); self.deadlines(); self.reset(); self.weekreview()
        self.today(); self.timebox(); self.sprints(); self.unstuck(); self.lowenergy(); self.overwhelm(); self.donelist()
        self.project(); self.breakdown(); self.timeguess(); self.backwards(); self.messages(); self.scripts(); self.parking()
        self.adminhour(); self.invoices(); self.income(); self.moneydates(); self.subs(); self.moneycheck()
        self.mcal(); self.mfocus(); self.quarter(); self.habits(); self.wins(); self.restmenu(); self.mreview()
        self.callnotes(); self.cowork(); self.cards(); self.lined(); self.dots()
        self.c.save()
        return self.seen


if __name__ == '__main__':
    out = '/home/claude/book/out/focus/'
    os.makedirs(out, exist_ok=True)
    MON = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']; SUN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for size, tag, fn in [(letter, 'US Letter', 'US_Letter'), (A4, 'A4', 'A4')]:
        for days, dn in [(MON, 'Monday_Start'), (SUN, 'Sunday_Start')]:
            path = out + 'Focus_Planner_%s_%s.pdf' % (fn, dn)
            toc = P('/tmp/_toc.pdf', size, tag, days).build()
            seen = P(path, size, tag, days, toc).build()
            print(path, 'pages', seen[-1][2])
            if seen[-1][2] != PAGES: WARN.append('page count %d != %d' % (seen[-1][2], PAGES))
    print('WARNINGS', len(WARN))
    for x in sorted(set(WARN)): print(' ', x)
