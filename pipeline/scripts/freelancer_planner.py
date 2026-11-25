# The Freelancer Planner: 52 page undated business planner.
# Builds 4 PDFs (US Letter and A4, Monday start and Sunday start) into /home/claude/book/out/fplanner/
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

INK = HexColor('#20294A'); SOFT = HexColor('#6F748A'); LINE = HexColor('#B9BCC8'); HAIR = HexColor('#DCDEE6')
CORAL = HexColor('#D9583B'); TINT = HexColor('#F4EFE6'); TEAL = HexColor('#1F6F78'); MUST = HexColor('#C4871C')
SAGE = HexColor('#5E8468'); NAVY = HexColor('#2B3A67'); WHITE = HexColor('#FFFFFF')
SEC = {'Start here': CORAL, 'Foundation': NAVY, 'Quarter': CORAL, 'Month': MUST, 'Week': TEAL, 'Day': SAGE,
       'Clients and projects': CORAL, 'Pipeline': TEAL, 'Money': MUST, 'Time': NAVY, 'Growth': SAGE,
       'Boundaries': CORAL, 'Notes': NAVY}
NAME = 'The Freelancer Planner'
WARN = []
sw = pdfmetrics.stringWidth


class P:
    def __init__(self, path, size, tag, days, toc=None):
        self.c = canvas.Canvas(path, pagesize=size)
        self.W, self.H = size
        self.m = 46; self.B = 46
        self.w = self.W - 2 * self.m
        self.tag = tag; self.days = days; self.toc = toc or []; self.seen = []
        self.n = 1; self.sec = 'Start here'; self.ac = CORAL
        self.c.setTitle(NAME + ' (' + tag + ')'); self.c.setAuthor('Inkwell and Co')
        self.c.setSubject('Undated business planner for freelancers. For personal use.')

    # primitives ----------------------------------------------------
    def caps(self, x, y, s, size=6.4, col=SOFT, font='InB', right=False, sp=1.2, maxw=None):
        c = self.c; s = s.upper()
        w = sw(s, font, size) + sp * (len(s) - 1)
        if maxw is not None and w > maxw: WARN.append('caps too wide: %s (%.0f > %.0f) p%d %s' % (s, w, maxw, self.n, self.tag))
        t = c.beginText(x - w if right else x, y); t.setFont(font, size); t.setFillColor(col); t.setCharSpace(sp); t.textOut(s); t.setCharSpace(0); c.drawText(t)
        return w

    def text(self, x, y, s, font='In', size=9.5, col=INK, right=False, maxw=None):
        c = self.c; c.setFillColor(col); c.setFont(font, size)
        if maxw is not None and sw(s, font, size) > maxw: WARN.append('text too wide: %s p%d %s' % (s, self.n, self.tag))
        (c.drawRightString if right else c.drawString)(x, y, s)
        return sw(s, font, size)

    def para(self, x, y, w, s, font='In', size=9.5, lead=14, col=INK):
        words = s.split(); line = ''
        for wd in words:
            t = (line + ' ' + wd).strip()
            if sw(t, font, size) > w: self.text(x, y, line, font, size, col); y -= lead; line = wd
            else: line = t
        if line: self.text(x, y, line, font, size, col); y -= lead
        return y

    def hl(self, x1, x2, y, col=LINE, w=0.5):
        c = self.c; c.setStrokeColor(col); c.setLineWidth(w); c.line(x1, y, x2, y)

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
        lw = self.caps(x, y, label, maxw=w - 30)
        self.hl(x + lw + 6, x + w, y - 1.5, col=INK, w=0.5)

    def fields(self, y, items, gap=14):
        """items: [(label, frac)] across the full width."""
        x = self.m; tot = self.w - gap * (len(items) - 1)
        for lab, fr in items:
            self.field(x, y, lab, tot * fr); x += tot * fr + gap

    def lines(self, x1, x2, ytop, ybot, step=20, col=LINE):
        y = ytop
        while y >= ybot - 0.1:
            self.hl(x1, x2, y, col=col); y -= step

    def label(self, x, y, s, col=None, maxw=None):
        return self.caps(x, y, s, col=col or self.ac, size=6.8, maxw=maxw)

    def lbox(self, x, yt, w, h, label, step=20, hint=None):
        """Outlined box with a caps label and writing lines."""
        self.box(x, yt - h, w, h)
        self.label(x + 10, yt - 16, label, maxw=w - 20)
        y0 = yt - 26
        if hint:
            self.text(x + 10, yt - 29, hint, 'FrI', 8.5, SOFT, maxw=w - 20); y0 = yt - 38
        y = y0 - step + 4
        while y > yt - h + 8:
            self.hl(x + 10, x + w - 10, y); y -= step

    def stat(self, x, yt, w, h, label):
        self.box(x, yt - h, w, h)
        self.caps(x + 8, yt - 14, label, size=6, col=SOFT, maxw=w - 14)

    def stats(self, yt, labels, h=50, gap=10):
        bw = (self.w - gap * (len(labels) - 1)) / len(labels)
        for i, t in enumerate(labels): self.stat(self.m + i * (bw + gap), yt, bw, h, t)
        return yt - h

    def checklist(self, x, yt, w, items=None, n=None, step=20, ybot=None):
        """Printed items (list of str) and or blank rows. Returns y below the last row."""
        y = yt
        rows = list(items or []) + [''] * (n or 0)
        if ybot is not None:
            while y - len(rows) * step > ybot + step - 6: rows.append('')
        for it in rows:
            self.check(x, y - 9)
            if it: self.text(x + 15, y - 8, it, 'In', 9.2, INK, maxw=w - 16)
            self.hl(x + 15, x + w, y - 11.5, col=LINE if not it else HAIR)
            y -= step
        return y

    def table(self, x, yt, w, cols, rows=None, rh=20, yb=None, total=None, first=None, hsize=6.0):
        c = self.c; hh = 18
        if rows is None: rows = int((yt - hh - yb - (rh if total else 0)) / rh)
        self.hl(x, x + w, yt, col=INK, w=0.8)
        self.hl(x, x + w, yt - hh, col=INK, w=0.5)
        cx = x
        for i, (lab, fr) in enumerate(cols):
            cw = w * fr
            self.caps(cx + 5, yt - 12, lab, size=hsize, col=INK, sp=0.9, maxw=cw - 7)
            if i: self.vl(cx, yt - hh - rows * rh, yt, col=HAIR)
            cx += cw
        for r in range(1, rows + 1):
            y = yt - hh - r * rh
            self.hl(x, x + w, y, col=INK if r == rows else LINE, w=0.6 if r == rows else 0.5)
            if first and r <= len(first):
                self.text(x + 5, y + rh / 2 - 3, first[r - 1], 'InM', 8.5, SOFT, maxw=w * cols[0][1] - 7)
        yb2 = yt - hh - rows * rh
        if total:
            self.caps(x + 5, yb2 - rh / 2 - 2, total, size=6.4, col=self.ac)
            self.hl(x, x + w, yb2 - rh, col=INK, w=0.8)
            yb2 -= rh
        return yb2

    def head(self, title, accent='', sec=None, toc=True):
        c = self.c; m = self.m; self.n += 1
        if sec: self.sec = sec; self.ac = SEC[sec]
        if toc: self.seen.append((self.sec, (title + ' ' + accent).strip(), self.n))
        top = self.H - m
        self.caps(m, top - 4, 'Inkwell and Co', col=INK)
        lw = self.caps(self.W - m, top - 4, self.sec, right=True, col=INK)
        c.setFillColor(self.ac); c.rect(self.W - m - lw - 13, top - 5, 7, 7, stroke=0, fill=1)
        y = top - 46
        c.setFillColor(INK); c.setFont('Fr', 30); c.drawString(m, y, title)
        w = sw(title, 'Fr', 30) + 9
        if accent:
            c.setFillColor(self.ac); c.setFont('FrI', 30); c.drawString(m + w, y, accent)
            if w + sw(accent, 'FrI', 30) > self.w: WARN.append('title too wide: ' + title + ' ' + accent)
        self.hl(m, self.W - m, y - 14, col=INK, w=0.9)
        self.caps(m, m - 20, NAME, size=5.6, col=SOFT)
        self.caps(self.W - m, m - 20, '%02d' % self.n, size=5.6, col=SOFT, right=True)
        return y - 14

    def done(self): self.c.showPage()

    # start here ----------------------------------------------------
    def cover(self):
        c = self.c; m = self.m; W, H = self.W, self.H
        c.setFillColor(TINT); c.rect(0, 0, W, H, stroke=0, fill=1)
        c.setFillColor(NAVY); c.rect(0, H - 14, W, 14, stroke=0, fill=1)
        self.caps(m, H - m - 12, 'Inkwell and Co', col=INK)
        self.caps(W - m, H - m - 12, 'Undated, start any day', right=True, col=INK)
        c.setFillColor(INK); c.setFont('Fr', 66)
        c.drawString(m - 3, H - 236, 'The'); c.drawString(m - 3, H - 304, 'Freelancer')
        c.setFillColor(CORAL); c.setFont('FrI', 66); c.drawString(m - 3, H - 372, 'Planner.')
        self.text(m, H - 408, 'A 90 day system for clients, projects, money and time.', 'FrI', 15, TEAL)
        self.hl(m, W - m, H - 432, col=INK, w=0.9)
        secs = [('Foundation', 'Rates, capacity and your ideal week', NAVY), ('Quarter', 'Goals, a 13 week roadmap, income plan', CORAL),
                ('Month', 'Three months of plans and money checks', MUST), ('Week and day', 'Plan, schedule, focus and review', TEAL),
                ('Clients and projects', 'Briefs, timelines, scope and wrap up', CORAL), ('Pipeline', 'Leads, outreach, proposals and calls', TEAL),
                ('Money', 'Income, invoices, expenses and tax set aside', MUST), ('Time and growth', 'Hours, marketing, wins and time off', SAGE)]
        y = H - 462; colw = self.w / 2
        for i, (a, b, col) in enumerate(secs):
            x = m + (i % 2) * colw; yy = y - (i // 2) * 40
            c.setFillColor(col); c.rect(x, yy - 1, 7, 7, stroke=0, fill=1)
            self.text(x + 16, yy - 1, a, 'FrM', 12.5, INK)
            self.text(x + 16, yy - 15, b, 'In', 8.3, SOFT, maxw=colw - 22)
        self.text(m, m + 14, '52 pages. ' + self.tag + ', ' + ('Monday' if self.days[0] == 'Mon' else 'Sunday') + ' start. Print the pages you need, as many times as you like.', 'In', 8.5, SOFT)
        self.text(m, m, 'Copyright 2026 Inkwell and Co. For personal use. Please do not resell or share the file.', 'In', 8.5, SOFT)
        self.done()

    def howto(self):
        top = self.head('How to use', 'this planner', 'Start here', toc=False); m = self.m; w = self.w
        y = top - 28
        y = self.para(m, y, w, 'Freelance work has no manager, no payroll and no fixed week. This planner gives your business the '
                      'structure an employer would: a plan for the quarter, a rhythm for each month and week, and one place for '
                      'clients, money and time. It is undated, so you can start today.', 'Fr', 12.5, 18, INK)
        y -= 14
        steps = [('Set your foundation once', 'Fill in the four Foundation pages first. Your minimum rate, your capacity and your ideal week shape every later decision.'),
                 ('Plan the quarter', 'Choose three goals, sketch the 13 week roadmap and work out how much income is already booked and how much is still to find.'),
                 ('Open each month', 'Use the calendar and the month plan on day one. Close the month with the review and money check before you plan the next.'),
                 ('Run each week', 'Print the three Week pages 13 times for a full quarter. Plan on your first working day and review on your last.'),
                 ('Use the day pages when you need them', 'Daily focus is for busy days. Focus sessions is for deep work you keep putting off.'),
                 ('Keep the trackers open', 'Clients, pipeline, money and time pages are running logs. Print more copies whenever one fills up.')]
        for i, (t, b) in enumerate(steps):
            self.text(m, y - 4, '%d' % (i + 1), 'FrI', 26, self.ac)
            self.text(m + 34, y, t, 'FrM', 12.5, INK)
            y = self.para(m + 34, y - 15, w - 34, b, 'In', 9.5, 13.5, SOFT) - 13
        y -= 4
        self.hl(m, m + w, y + 6, col=INK, w=0.6)
        g = 20; cw = (w - g) / 2; y -= 14
        self.label(m, y, 'Printing'); self.label(m + cw + g, y, 'Good to know')
        a = self.para(m, y - 16, cw, 'Print at 100 percent or choose "fit to page". Margins are wide enough for a hole punch or a disc binder. '
                      'Print single pages as often as you like.', 'In', 9, 13, INK)
        self.para(m + cw + g, y - 16, cw, 'The pages also work in any tablet app that lets you write on a PDF. The money pages help you keep '
                  'records. They are not tax or legal advice, so check local rules with an accountant.', 'In', 9, 13, INK)
        yb = min(a, y - 16 - 39) - 22
        self.label(m, yb, 'A simple rhythm')
        rh_ = [('Every day', '5 minutes', 'Pick the one thing. Log your hours.'), ('Every week', '20 minutes', 'Plan on day one. Review on the last.'),
               ('Every month', '45 minutes', 'Money check, review, next month plan.'), ('Every quarter', '2 hours', 'Review, new goals, new roadmap.')]
        gg = 10; bw = (w - 3 * gg) / 4; bh = min(104, yb - 12 - self.B)
        for i, (t1, t2, t3) in enumerate(rh_):
            x = m + i * (bw + gg); self.box(x, yb - 12 - bh, bw, bh, fill=TINT)
            self.caps(x + 10, yb - 30, t1, size=6.2, col=INK)
            self.text(x + 10, yb - 56, t2, 'FrI', 17, self.ac)
            self.para(x + 10, yb - 74, bw - 18, t3, 'In', 8.4, 11.5, SOFT)
        self.done()

    def contents(self):
        top = self.head('What is', 'inside', 'Start here', toc=False); m = self.m; w = self.w
        g = 26; cw = (w - g) / 2
        groups = []
        for s, t, n in self.toc:
            if not groups or groups[-1][0] != s: groups.append((s, []))
            groups[-1][1].append((t, n))
        # balance two columns
        heights = [22 + 13.5 * len(g_[1]) + 9 for g_ in groups]
        split = min(range(1, max(2, len(groups))), key=lambda k: max(sum(heights[:k]), sum(heights[k:])))
        if max(sum(heights[:split]), sum(heights[split:])) > top - 30 - self.B: WARN.append('contents overflow ' + self.tag)
        col = 0; y = top - 30; acc = 0
        for gi, ((s, items), hgt) in enumerate(zip(groups, heights)):
            if gi == split: col = 1; y = top - 30
            x = m + col * (cw + g)
            self.c.setFillColor(SEC[s]); self.c.rect(x, y - 1, 6, 6, stroke=0, fill=1)
            self.caps(x + 12, y - 1, s, size=6.8, col=INK)
            self.hl(x, x + cw, y - 8, col=INK, w=0.6)
            y -= 22
            for t, n in items:
                self.text(x, y, t, 'In', 9.3, INK); self.text(x + cw, y, '%02d' % n, 'FrI', 9.5, SEC[s], right=True)
                y -= 13.5
            y -= 9; acc += hgt
        self.done()

    # foundation ----------------------------------------------------
    def business(self):
        top = self.head('My business', 'on one page', 'Foundation'); m = self.m; w = self.w
        g = 12; cw = (w - g) / 2; strip = 62
        bh = (top - 16 - self.B - strip - 3 * g) / 3
        items = [('What I do', 'The services I sell'), ('Who I do it for', 'My best fit client'),
                 ('What I charge', 'Rates, packages, minimum project'), ('Why clients choose me', 'What I do better or differently'),
                 ('Where clients find me', 'Referrals, platforms, content'), ('What I do not do', 'Work and clients I turn down')]
        for i, (a, b) in enumerate(items):
            self.lbox(m + (i % 2) * (cw + g), top - 16 - (i // 2) * (bh + g), cw, bh, a, hint=b)
        yt = self.B + strip
        self.box(m, self.B, w, strip, fill=TINT, col=INK)
        self.label(m + 10, yt - 16, 'This year in one sentence')
        self.hl(m + 10, m + w - 10, yt - 42, col=INK)
        self.done()

    def rate(self):
        top = self.head('Rate and', 'capacity', 'Foundation'); m = self.m; w = self.w
        y = top - 24
        y = self.para(m, y, w, 'Work through the lines in order. The result is the lowest rate that keeps your business healthy. Quote above it.', 'FrI', 10.5, 15, SOFT)
        rows = [('A', 'Income I need for myself each year', 'Rent, food, savings, everything personal'),
                ('B', 'Business costs each year', 'Software, equipment, fees, training'),
                ('C', 'Tax to set aside each year', 'Your best estimate or your accountant\'s figure'),
                ('D', 'Total I must earn', 'A + B + C'),
                ('E', 'Weeks I will work', '52 minus holidays, sick days and quiet weeks'),
                ('F', 'Billable hours per week', 'Client hours only, not admin or marketing'),
                ('G', 'Billable hours per year', 'E x F'),
                ('H', 'Minimum hourly rate', 'D divided by G'),
                ('I', 'Minimum day rate', 'H x billable hours in a day')]
        bot_h = 150
        rh = min(44, (y - 6 - self.B - bot_h) / len(rows)); bw = 128
        y -= 4
        for k, (a, b, cc) in enumerate(rows):
            res = a in 'DGHI'
            if res: self.c.setFillColor(TINT); self.c.rect(m, y - rh, w, rh, stroke=0, fill=1)
            self.hl(m, m + w, y, col=INK if k == 0 else LINE, w=0.8 if k == 0 else 0.5)
            self.text(m + 8, y - rh / 2 - 7, a, 'FrI', 20, self.ac if res else INK)
            self.text(m + 40, y - rh / 2 + 2, b, 'InM' if res else 'In', 10.2, INK)
            self.text(m + 40, y - rh / 2 - 10, cc, 'In', 8, SOFT, maxw=w - 40 - bw - 16)
            self.box(m + w - bw - 8, y - rh + 7, bw, rh - 14, col=INK, lw=0.9 if res else 0.5, fill=WHITE)
            y -= rh
        self.hl(m, m + w, y, col=INK, w=0.8)
        y -= 16; g = 12; cw = (w - g) / 2; h = y - self.B
        self.lbox(m, y, cw, h, 'My capacity', hint='Projects at once, hours I protect, busiest months')
        self.lbox(m + cw + g, y, cw, h, 'My pricing rules', hint='Minimum project fee, rush fee, when I raise rates')
        self.done()

    def idealweek(self):
        top = self.head('My ideal', 'week', 'Foundation'); m = self.m; w = self.w
        y = top - 22
        self.para(m, y, w, 'Block the week you want before clients fill it. Write your own hours down the left side.', 'FrI', 10.5, 15, SOFT)
        gt = y - 22; tw = 46; cw = (w - tw) / 7; key_h = 44
        rows = 15; rh = (gt - 18 - self.B - key_h - 12) / rows
        self.hl(m, m + w, gt, col=INK, w=0.8); self.hl(m, m + w, gt - 18, col=INK)
        self.caps(m + 4, gt - 12, 'Time', size=6, col=INK)
        for i, dname in enumerate(self.days):
            x = m + tw + i * cw
            self.caps(x + 5, gt - 12, dname, size=6, col=INK); self.vl(x, gt - 18 - rows * rh, gt, col=HAIR)
        for r in range(1, rows + 1):
            self.hl(m, m + w, gt - 18 - r * rh, col=INK if r == rows else LINE)
        yk = self.B + key_h
        self.label(m, yk - 12, 'Color key')
        ks = ['Client work', 'Admin', 'Marketing', 'Learning', 'Rest and life']; kw = w / len(ks)
        for i, k in enumerate(ks):
            self.box(m + i * kw, self.B + 2, 12, 12, r=2); self.text(m + i * kw + 18, self.B + 5, k, 'In', 8.8, INK, maxw=kw - 20)
        self.done()

    def yearglance(self):
        top = self.head('Year at a', 'glance', 'Foundation'); m = self.m; w = self.w
        self.fields(top - 24, [('Year', .22), ('Income goal for the year', .44), ('Monthly average needed', .34)])
        gt = top - 46; sh = 54
        cols = [('Month', .16), ('Income target', .14), ('Invoiced', .14), ('Received', .14), ('Expenses', .14), ('Tax set aside', .14), ('Paid myself', .14)]
        rh = (gt - 18 - self.B - sh - 16) / 13
        yb = self.table(m, gt, w, cols, rows=12, rh=rh, total='Year total')
        self.stats(self.B + sh, ['Best month', 'Slowest month', 'Average month', 'Biggest client share'], h=sh)
        self.done()

    # quarter -------------------------------------------------------
    def qgoals(self):
        top = self.head('Quarter', 'goals', 'Quarter'); m = self.m; w = self.w
        self.fields(top - 24, [('Quarter', .3), ('From', .35), ('To', .35)])
        gt = top - 40; g = 12; bh = (gt - self.B - 2 * g) / 3
        for i in range(3):
            yt = gt - i * (bh + g); yb = yt - bh
            self.box(m, yb, w, bh)
            self.text(m + 12, yt - 36, str(i + 1), 'FrI', 30, self.ac)
            self.field(m + 42, yt - 24, 'Goal', w - 54)
            self.field(m + 42, yt - 46, 'How I will measure it', w * .56); self.field(m + 42 + w * .56 + 12, yt - 46, 'By when', w - 54 - w * .56 - 12)
            self.caps(m + 12, yt - 70, 'Why it matters', col=INK)
            self.lines(m + 12, m + w * .46, yt - 90, yb + 12, step=19)
            x = m + w * .5; self.caps(x, yt - 70, 'Steps to get there', col=INK)
            self.checklist(x, yt - 78, w * .5 - 12, ybot=yb + 4, step=19)
        self.done()

    def roadmap(self):
        top = self.head('13 week', 'roadmap', 'Quarter'); m = self.m; w = self.w
        gt = top - 16; rh = (gt - 18 - self.B) / 13
        cols = [('Week', .08), ('Dates', .14), ('Main focus', .34), ('Client deadlines', .28), ('Income due', .16)]
        self.table(m, gt, w, cols, rows=13, rh=rh, first=['%02d' % i for i in range(1, 14)])
        self.done()

    def qincome(self):
        top = self.head('Quarter', 'income plan', 'Quarter'); m = self.m; w = self.w
        y = self.stats(top - 16, ['Income target', 'Already booked', 'Likely, not signed', 'Gap to fill'], h=52)
        gt = y - 30; self.label(m, gt + 8, 'Booked and expected work')
        low = 150
        cols = [('Client', .22), ('Project', .26), ('Status', .13), ('Month one', .13), ('Month two', .13), ('Month three', .13)]
        yb = self.table(m, gt, w, cols, yb=self.B + low + 16, total='Total')
        g = 12; cw = (w - g) / 2; h = yb - 16 - self.B
        self.lbox(m, yb - 16, cw, h, 'How I will fill the gap', hint='Past clients to contact, offers, referrals')
        self.lbox(m + cw + g, yb - 16, cw, h, 'If a client leaves', hint='My plan when income drops')
        self.done()

    def qreview(self):
        top = self.head('Quarter', 'review', 'Quarter'); m = self.m; w = self.w
        y = self.stats(top - 16, ['Income target', 'Income received', 'New clients', 'Hours a week', 'Rate earned'], h=52)
        g = 12; cw = (w - g) / 2; cw3 = (w - 2 * g) / 3
        low = (y - g - self.B) * .36; bh = (y - g - self.B - low - 2 * g) / 2
        its = [('What worked', None), ('What did not', None), ('Best clients and why', None), ('Goals: what happened', None)]
        for i, (a, b) in enumerate(its):
            self.lbox(m + (i % 2) * (cw + g), y - g - (i // 2) * (bh + g), cw, bh, a)
        yt = self.B + low
        for i, a in enumerate(['Stop', 'Start', 'Keep']):
            self.lbox(m + i * (cw3 + g), yt, cw3, low, a)
        self.done()

    # month ---------------------------------------------------------
    def mcal(self, k):
        top = self.head('Month ' + k, 'calendar', 'Month'); m = self.m; w = self.w
        self.fields(top - 24, [('Month', .4), ('Year', .22), ('Income target', .38)])
        gt = top - 42; low = 112; cw = w / 7
        rh = (gt - 16 - self.B - low - 14) / 6
        self.hl(m, m + w, gt, col=INK, w=0.8)
        for i, dname in enumerate(self.days): self.caps(m + i * cw + 5, gt - 11, dname, size=6, col=INK)
        for r in range(7): self.hl(m, m + w, gt - 16 - r * rh, col=INK if r in (0, 6) else LINE)
        for i in range(8): self.vl(m + i * cw, gt - 16 - 6 * rh, gt - 16 if i not in (0, 7) else gt, col=INK if i in (0, 7) else LINE)
        g = 12; cw3 = (w - 2 * g) / 3
        for i, a in enumerate(['Deadlines', 'Invoices to send or chase', 'Days off']):
            self.lbox(m + i * (cw3 + g), self.B + low, cw3, low, a, step=19)
        self.done()

    def mplan(self, k):
        top = self.head('Month ' + k, 'plan', 'Month'); m = self.m; w = self.w
        y = self.stats(top - 16, ['Income target', 'Booked so far', 'Gap to fill', 'Hours I can bill'], h=50)
        y -= 24; self.label(m, y, 'Top three priorities')
        for i in range(3):
            self.text(m, y - 26 - i * 24, str(i + 1), 'FrI', 15, self.ac); self.hl(m + 18, m + w, y - 28 - i * 24, col=INK)
        y -= 28 + 3 * 24
        self.label(m, y, 'Projects this month')
        low = 190
        cols = [('Project', .34), ('Client', .24), ('Due', .14), ('Fee', .14), ('Invoiced', .14)]
        yb = self.table(m, y - 8, w, cols, yb=self.B + low + 22)
        g = 14; cw3 = (w - 2 * g) / 3; yt = yb - 24
        for i, a in enumerate(['Marketing actions', 'Admin and money', 'Personal']):
            x = m + i * (cw3 + g); self.label(x, yt, a); self.checklist(x, yt - 10, cw3, ybot=self.B, step=20)
        self.done()

    def mreview(self, k):
        top = self.head('Month ' + k, 'review', 'Month'); m = self.m; w = self.w
        g = 16; lw = w * .44; rw = w - lw - g
        yt = top - 28; self.label(m, yt, 'Money check')
        rows = ['Invoiced', 'Received', 'Still owed to me', 'Expenses', 'Tax set aside', 'Paid myself', 'Added to buffer', 'Hours worked', 'Billable hours', 'Effective hourly rate']
        rh = 25; y = yt - 10
        for i, r in enumerate(rows):
            self.hl(m, m + lw, y, col=INK if i == 0 else LINE, w=0.8 if i == 0 else 0.5)
            self.text(m + 4, y - rh / 2 - 3, r, 'In', 9.4, INK)
            self.vl(m + lw * .58, y - rh, y, col=HAIR); y -= rh
        self.hl(m, m + lw, y, col=INK, w=0.8)
        self.text(m, y - 16, 'Effective rate = received divided by hours worked.', 'FrI', 8.6, SOFT, maxw=lw)
        x = m + lw + g; hh = (yt + 6 - (y - 20) - 12) / 2
        self.lbox(x, yt + 6, rw, hh, 'Wins this month'); self.lbox(x, yt + 6 - hh - 12, rw, hh, 'What I learned')
        y2 = y - 34; cw = (w - 12) / 2; h = (y2 - self.B - 12) / 2
        its = ['Best client or project', 'What drained me', 'Someone to thank or follow up', 'Carry over to next month']
        for i, a in enumerate(its):
            self.lbox(m + (i % 2) * (cw + 12), y2 - (i // 2) * (h + 12), cw, h, a)
        self.done()

    # week ----------------------------------------------------------
    def wplan(self):
        top = self.head('Week', 'plan', 'Week'); m = self.m; w = self.w
        self.fields(top - 24, [('Week of', .36), ('Week number', .28), ('Income due this week', .36)])
        y = top - 50; self.label(m, y, 'Three things that make this week a success')
        for i in range(3):
            self.text(m, y - 26 - i * 24, str(i + 1), 'FrI', 15, self.ac); self.hl(m + 18, m + w, y - 28 - i * 24, col=INK)
        y -= 28 + 3 * 24
        self.label(m, y, 'Client work')
        low = 170
        cols = [('Client', .22), ('Task or deliverable', .42), ('Due', .12), ('Hours planned', .14), ('Done', .10)]
        yb = self.table(m, y - 8, w, cols, yb=self.B + low + 22)
        g = 14; cw3 = (w - 2 * g) / 3; yt = yb - 24
        for i, a in enumerate(['Admin and invoices', 'Pipeline and marketing', 'Waiting on']):
            x = m + i * (cw3 + g); self.label(x, yt, a); self.checklist(x, yt - 10, cw3, ybot=self.B, step=20)
        self.done()

    def wsched(self):
        top = self.head('Week', 'schedule', 'Week'); m = self.m; w = self.w
        full = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
        gt = top - 14; bh = (gt - self.B) / 7; lw = 86; hw = 62
        for i, dname in enumerate(self.days):
            yt = gt - i * bh
            if i: self.hl(m, m + w, yt, col=INK, w=0.6)
            self.text(m, yt - 22, full[dname], 'Fr', 15, INK)
            self.caps(m, yt - 36, 'Date', size=5.8); self.hl(m + 24, m + lw - 12, yt - 37.5, col=LINE)
            n = int((bh - 14) / 19)
            for r in range(n):
                yy = yt - 24 - r * 19
                self.check(m + lw, yy - 2); self.hl(m + lw + 14, m + w - hw - 12, yy - 2)
            self.box(m + w - hw, yt - bh + 10, hw, bh - 20)
            self.caps(m + w - hw + 7, yt - 23, 'Hours', size=5.8)
        self.hl(m, m + w, self.B, col=INK, w=0.6)
        self.done()

    def wreview(self):
        top = self.head('Week', 'review', 'Week'); m = self.m; w = self.w
        self.fields(top - 24, [('Week of', .4), ('Hours worked', .3), ('Billable hours', .3)])
        g = 16; lw = w * .5; rw = w - lw - g; yt = top - 52
        self.label(m, yt, 'Hours by client')
        yb = self.table(m, yt - 8, lw, [('Client', .52), ('Hours', .22), ('Billed', .26)], rows=7, rh=21, total='Total')
        x = m + lw + g; self.label(x, yt, 'Money this week')
        y = yt - 8
        for i, r in enumerate(['Invoices sent', 'Payments received', 'Overdue and chased', 'Expenses logged', 'Tax moved aside']):
            self.hl(x, x + rw, y, col=INK if i == 0 else LINE, w=0.8 if i == 0 else 0.5)
            self.text(x + 4, y - 15, r, 'In', 9.2, INK); self.vl(x + rw * .64, y - 23, y, col=HAIR); y -= 23
        self.hl(x, x + rw, y, col=INK, w=0.8)
        self.label(x, y - 22, 'Energy this week')
        for i in range(5):
            self.c.setStrokeColor(INK); self.c.setLineWidth(0.6); self.c.circle(x + 9 + i * 30, y - 44, 9, stroke=1, fill=0)
            self.text(x + 6.3 + i * 30, y - 47.2, str(i + 1), 'InM', 8.5, SOFT)
        y2 = yb - 18; cw = (w - 12) / 2; h = (y2 - self.B - 12) / 2
        for i, a in enumerate(['What went well', 'What dragged or slipped', 'One thing to change', 'First task next week']):
            self.lbox(m + (i % 2) * (cw + 12), y2 - (i // 2) * (h + 12), cw, h, a)
        self.done()

    # day -----------------------------------------------------------
    def daily(self):
        top = self.head('Daily', 'focus', 'Day'); m = self.m; w = self.w
        self.fields(top - 24, [('Date', .34), ('Day', .26), ('Working hours today', .40)])
        y = top - 44; self.box(m, y - 50, w, 50, fill=TINT)
        self.label(m + 10, y - 16, 'The one thing that makes today a win'); self.hl(m + 10, m + w - 10, y - 38, col=INK)
        y -= 70; g = 18; lw = w * .40; rw = w - lw - g
        self.label(m, y, 'Schedule'); rows = 14; rh = (y - 10 - self.B) / rows
        for r in range(rows + 1):
            yy = y - 10 - r * rh; self.hl(m, m + lw, yy, col=INK if r in (0, rows) else LINE)
        self.vl(m + 40, self.B, y - 10, col=HAIR)
        x = m + lw + g; foot = 48; avail = y - self.B - foot - 14
        secs = [('Top three', 3), ('Client tasks', 6), ('Messages and follow ups', 4), ('Admin', 3)]
        tot = sum(n for _, n in secs); step = min(21, (avail - len(secs) * 26) / tot); yy = y
        for a, n in secs:
            self.label(x, yy, a); yy = self.checklist(x, yy - 10, rw, n=n, step=step) - 16
        bw = (rw - 10) / 2
        self.stat(x, self.B + foot, bw, foot, 'Hours billed'); self.stat(x + bw + 10, self.B + foot, bw, foot, 'Stopped work at')
        self.done()

    def focus(self):
        top = self.head('Focus', 'sessions', 'Day'); m = self.m; w = self.w
        self.fields(top - 24, [('Date', .4), ('Project', .6)])
        low = 150; gt = top - 40; g = 10; bh = (gt - self.B - low - 14 - 3 * g) / 4
        for i in range(4):
            yt = gt - i * (bh + g); yb = yt - bh
            self.box(m, yb, w, bh)
            self.text(m + 12, yt - 32, str(i + 1), 'FrI', 26, self.ac)
            self.field(m + 40, yt - 22, 'I will work on', w - 52)
            self.fields2(m + 40, yt - 46, w - 52, [('Start', .22), ('End', .22), ('Finished', .56)])
            self.caps(m + 40, yb + 14, 'Distractions, one mark each', size=5.8)
            for j in range(12): self.box(m + 200 + j * 16, yb + 9, 11, 11, col=LINE, r=2)
        g2 = 12; cw = (w - g2) / 2; yt = self.B + low
        self.label(m, yt - 4, 'Shutdown routine')
        self.checklist(m, yt - 14, cw, items=['Log today\'s hours', 'Send client updates', 'Check tomorrow\'s deadlines', 'Write tomorrow\'s first task', 'Close the laptop'], n=1, step=21)
        self.lbox(m + cw + g2, yt + 6, cw, low + 6, 'Ideas to park for later')
        self.done()

    def fields2(self, x, y, w, items, gap=12):
        tot = w - gap * (len(items) - 1)
        for lab, fr in items:
            self.field(x, y, lab, tot * fr); x += tot * fr + gap

    # generic tracker -------------------------------------------------
    def tracker(self, title, accent, cols, sec=None, fields=None, note=None, total=None, rh=21, stats=None):
        top = self.head(title, accent, sec); m = self.m; w = self.w
        y = top - 16
        if note: y = self.para(m, top - 22, w, note, 'FrI', 10, 14, SOFT) - 2
        if fields: self.fields(y - 10, fields); y -= 30
        yb = self.B + ((stats and 64) or 0)
        self.table(m, y, w, cols, yb=yb, total=total, rh=rh)
        if stats: self.stats(self.B + 50, stats, h=50)
        self.done()

    # clients and projects ------------------------------------------
    def cprofile(self):
        top = self.head('Client', 'profile', None); m = self.m; w = self.w
        y = top - 26
        self.fields(y, [('Client', .5), ('Company', .5)]); y -= 24
        self.fields(y, [('Email', .5), ('Phone', .25), ('Time zone', .25)]); y -= 24
        self.fields(y, [('How they found me', .5), ('Client since', .25), ('Rate', .25)]); y -= 22
        g = 12; cw = (w - g) / 2; bh = 118
        self.lbox(m, y, cw, bh, 'Billing', hint='Invoice to, terms, how they pay')
        self.lbox(m + cw + g, y, cw, bh, 'How they like to work', hint='Channel, feedback style, who approves')
        y -= bh + 26; self.label(m, y, 'Projects')
        low = 118
        yb = self.table(m, y - 8, w, [('Project', .40), ('Dates', .22), ('Fee', .14), ('Paid', .10), ('Went well?', .14)], yb=self.B + low + 14)
        self.lbox(m, yb - 14, w, yb - 14 - self.B, 'Notes', hint='Preferences, people, things to remember')
        self.done()

    def onboarding(self):
        top = self.head('New client', 'checklist', None); m = self.m; w = self.w
        self.fields(top - 24, [('Client', .5), ('Project', .5)])
        g = 20; cw = (w - g) / 2; yt = top - 54
        a = ['Discovery call held', 'Needs and budget confirmed', 'Proposal sent', 'Proposal accepted', 'Contract sent', 'Contract signed by both sides',
             'Deposit invoice sent', 'Deposit received']
        b = ['Brief agreed in writing', 'Files and access received', 'Timeline shared', 'Kickoff date set', 'Main contact confirmed',
             'How and when we talk agreed', 'Added to client roster', 'Welcome message sent']
        self.label(m, yt, 'Before I start'); self.label(m + cw + g, yt, 'Getting set up')
        y1 = self.checklist(m, yt - 12, cw, items=a, n=2, step=23)
        self.checklist(m + cw + g, yt - 12, cw, items=b, n=2, step=23)
        y = y1 - 14; self.label(m, y, 'Key dates')
        low = 120
        yb = self.table(m, y - 8, w, [('What', .5), ('Date', .25), ('Done', .25)], yb=self.B + low + 14)
        self.lbox(m, yb - 14, w, yb - 14 - self.B, 'First impressions and things to watch')
        self.done()

    def brief(self):
        top = self.head('Project', 'brief', None); m = self.m; w = self.w
        y = top - 26
        self.fields(y, [('Project', .5), ('Client', .5)]); y -= 24
        self.fields(y, [('Start', .22), ('Deadline', .22), ('Fee', .2), ('Deposit', .18), ('Revisions', .18)]); y -= 22
        self.lbox(m, y, w, 84, 'The goal', hint='What the client wants this work to achieve')
        y -= 84 + 24; g = 16; cw = (w - g) / 2; low = 132
        self.label(m, y, 'Deliverables'); self.label(m + cw + g, y, 'What I need from the client')
        self.checklist(m, y - 12, cw, ybot=self.B + low + 20, step=21)
        yb = self.checklist(m + cw + g, y - 12, cw, ybot=self.B + low + 20, step=21)
        self.lbox(m, self.B + low, cw, low, 'Not included', hint='Say it now, avoid scope creep later')
        self.lbox(m + cw + g, self.B + low, cw, low, 'How we will know it worked')
        self.done()

    def timeline(self):
        top = self.head('Project', 'timeline', None); m = self.m; w = self.w
        self.fields(top - 24, [('Project', .5), ('Client', .3), ('Deadline', .2)])
        y = top - 54; self.label(m, y, 'Phases and tasks')
        low = 180
        yb = self.table(m, y - 8, w, [('Phase', .18), ('Task', .40), ('Start', .13), ('Due', .13), ('Done', .08), ('Hours', .08)], yb=self.B + low + 26)
        y = yb - 26; self.label(m, y, 'Payment schedule')
        self.table(m, y - 8, w, [('Milestone', .36), ('Amount', .16), ('Invoice sent', .16), ('Due', .16), ('Paid on', .16)], yb=self.B, total='Total')
        self.done()

    def wrapup(self):
        top = self.head('Project', 'wrap up', None); m = self.m; w = self.w
        self.fields(top - 24, [('Project', .5), ('Client', .3), ('Finished on', .2)])
        g = 20; cw = (w - g) / 2; yt = top - 54
        self.label(m, yt, 'Closing checklist')
        its = ['Final files delivered', 'Final invoice sent', 'Final payment received', 'Files backed up and archived', 'Client access removed',
               'Asked for a testimonial', 'Asked for a referral', 'Permission to show the work', 'Added to portfolio', 'Follow up date set']
        y1 = self.checklist(m, yt - 12, cw, items=its, step=22)
        x = m + cw + g; self.label(x, yt, 'The numbers')
        y = yt - 10
        for i, r in enumerate(['Fee quoted', 'Fee received', 'Hours estimated', 'Hours spent', 'Effective hourly rate', 'Rounds of revisions']):
            self.hl(x, x + cw, y, col=INK if i == 0 else LINE, w=0.8 if i == 0 else 0.5)
            self.text(x + 4, y - 15, r, 'In', 9.2, INK); self.vl(x + cw * .62, y - 23, y, col=HAIR); y -= 23
        self.hl(x, x + cw, y, col=INK, w=0.8)
        self.lbox(x, y - 14, cw, y - 14 - (y1 + 12), 'Follow up plan')
        y2 = y1 - 4; h = (y2 - self.B - 12) / 2
        for i, a in enumerate(['What went well', 'What I would change', 'Kind words from the client', 'Would I work with them again?']):
            self.lbox(m + (i % 2) * (cw + g), y2 - (i // 2) * (h + 12), cw, h, a)
        self.done()

    # pipeline ------------------------------------------------------
    def call(self):
        top = self.head('Discovery', 'call notes', None); m = self.m; w = self.w
        y = top - 26
        self.fields(y, [('Name', .4), ('Company', .36), ('Date', .24)]); y -= 24
        self.fields(y, [('Where they found me', .5), ('Email or phone', .5)]); y -= 22
        g = 12; cw = (w - g) / 2; low = 96
        qs = [('What do they need?', None), ('Why now?', None), ('Deadline and key dates', None), ('Budget', 'Ask. Do not guess.'),
              ('Who decides and who approves?', None), ('What does success look like?', None)]
        bh = (y - self.B - low - 3 * g) / 3
        for i, (a, b) in enumerate(qs):
            self.lbox(m + (i % 2) * (cw + g), y - (i // 2) * (bh + g), cw, bh, a, hint=b)
        cw3 = (w - 2 * g) / 3
        for i, a in enumerate(['Red flags', 'Good signs', 'Next step and date']):
            self.lbox(m + i * (cw3 + g), self.B + low, cw3, low, a)
        self.done()

    # money ---------------------------------------------------------
    def steady(self):
        top = self.head('Steady pay', 'plan', None); m = self.m; w = self.w
        y = self.para(m, top - 22, w, 'Irregular income feels calmer when you pay yourself the same amount every month and let a buffer absorb the swings.', 'FrI', 10, 14, SOFT)
        y = self.stats(y - 2, ['Personal costs', 'Business costs', 'Steady pay I draw', 'Buffer target'], h=50)
        y -= 24; self.label(m, y, 'Buffer progress: shade a box for each step saved')
        cols_, s = 24, w / 24; gy = y - 10
        for r in range(3): self.hl(m, m + w, gy - r * s, col=INK if r in (0, 2) else LINE)
        for i in range(cols_ + 1): self.vl(m + i * s, gy - 2 * s, gy, col=INK if i in (0, cols_) else LINE)
        self.fields(gy - 2 * s - 22, [('Each box is worth', .34), ('Months of pay the full buffer covers', .66)])
        yt = gy - 2 * s - 46
        cols = [('Month', .16), ('Received', .14), ('Tax set aside', .14), ('Business costs', .14), ('Paid myself', .14), ('Buffer move', .14), ('Buffer total', .14)]
        self.table(m, yt, w, cols, rows=12, rh=(yt - 18 - self.B) / 12)
        self.done()

    def taxlog(self):
        top = self.head('Tax', 'set aside', None); m = self.m; w = self.w
        y = self.para(m, top - 22, w, 'Move a fixed share of every payment the day it arrives. Ask an accountant which percentage fits where you live.', 'FrI', 10, 14, SOFT)
        self.fields(y - 10, [('My set aside rate', .3), ('Tax account', .4), ('Next payment due', .3)])
        self.table(m, y - 32, w, [('Date', .13), ('Payment from', .27), ('Amount received', .17), ('Set aside', .15), ('Moved', .1), ('Running total', .18)],
                   yb=self.B, total='Total', rh=21)
        self.done()

    # time, growth, boundaries --------------------------------------
    def hoursweek(self):
        top = self.head('Hours', 'by client', None); m = self.m; w = self.w
        self.fields(top - 24, [('Week of', .4), ('Billable target', .3), ('Billable actual', .3)])
        gt = top - 46; low = 132
        cols = [('Client or project', .30)] + [(dn, .07) for dn in self.days] + [('Total', .10), ('Billed', .11)]
        yb = self.table(m, gt, w, cols, yb=self.B + low + 14, total='Total', rh=22)
        g = 12; cw = (w - g) / 2
        self.lbox(m, self.B + low, cw, low, 'Where the unpaid hours went', hint='Admin, calls, revisions, chasing')
        self.lbox(m + cw + g, self.B + low, cw, low, 'What I will change next week')
        self.done()

    def marketing(self):
        top = self.head('Marketing', 'plan', 'Growth'); m = self.m; w = self.w
        self.fields(top - 24, [('Month', .3), ('This month I want to be known for', .7)])
        gt = top - 46; low = 150
        cols = [('Week', .08), ('Idea or topic', .36), ('Format', .16), ('Where', .16), ('Date', .12), ('Done', .12)]
        rows = 12; rh = (gt - 18 - self.B - low - 16) / rows
        self.table(m, gt, w, cols, rows=rows, rh=rh, first=sum([['%d' % k, '', ''] for k in range(1, 5)], []))
        g = 12; cw = (w - g) / 2
        self.lbox(m, self.B + low, cw, low, 'Ideas bank'); self.lbox(m + cw + g, self.B + low, cw, low, 'What brought enquiries')
        self.done()

    def rates_up(self):
        top = self.head('Skills and', 'rates', None); m = self.m; w = self.w
        y = top - 28; self.label(m, y, 'Skills to build')
        low = 250
        yb = self.table(m, y - 8, w, [('Skill', .26), ('Why it pays', .28), ('Course or resource', .22), ('Cost', .10), ('Finish by', .14)], yb=self.B + low + 20)
        y = yb - 24; self.label(m, y, 'Rate rise plan')
        self.fields(y - 24, [('Current rate', .3), ('New rate', .3), ('From date', .4)])
        g = 16; cw = (w - g) / 2; yt = y - 54
        self.label(m, yt, 'Clients to tell'); self.label(m + cw + g, yt, 'Before I announce')
        self.checklist(m, yt - 12, cw, ybot=self.B, step=20)
        self.checklist(m + cw + g, yt - 12, cw, items=['New rate checked against my minimum', 'Notice period decided', 'Message drafted', 'Website and proposals updated'], ybot=self.B, step=20)
        self.done()

    def timeoff(self):
        top = self.head('Time off', 'planner', 'Boundaries'); m = self.m; w = self.w
        self.fields(top - 24, [('Year', .25), ('Days off I am aiming for', .4), ('Days taken', .35)])
        y = top - 50; self.label(m, y, 'Shade every day you take off. Write the month on the left.')
        lw = 62; s = (w - lw) / 31; gy = y - 12; rr = 21
        for d in range(31):
            if (d + 1) % 5 == 0 or d == 0: self.text(m + lw + d * s + s / 2 - 3, gy - 8, str(d + 1), 'InM', 5.6, SOFT)
        gy -= 12
        for r in range(13): self.hl(m, m + w, gy - r * rr, col=INK if r in (0, 12) else LINE)
        for d in range(32): self.vl(m + lw + d * s, gy - 12 * rr, gy, col=INK if d in (0, 31) else HAIR)
        self.vl(m, gy - 12 * rr, gy, col=INK)
        yt = gy - 12 * rr - 26; self.label(m, yt, 'Planned breaks')
        self.table(m, yt - 8, w, [('Dates away', .24), ('Days', .1), ('Clients told', .16), ('Auto reply set', .16), ('Work handed over or paused', .34)], yb=self.B)
        self.done()

    def rules(self):
        top = self.head('How I', 'work', None); m = self.m; w = self.w
        y = self.para(m, top - 22, w, 'Decide your rules once, on a calm day. Then you only have to follow them.', 'FrI', 10.5, 15, SOFT)
        g = 16; cw = (w - g) / 2; yt = y - 8
        self.label(m, yt, 'Working hours'); yy = yt - 10
        full = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
        for i, dn in enumerate(self.days):
            self.hl(m, m + cw, yy, col=INK if i == 0 else LINE, w=0.8 if i == 0 else 0.5)
            self.text(m + 4, yy - 15, full[dn], 'In', 9.2, INK); self.vl(m + cw * .42, yy - 23, yy, col=HAIR); yy -= 23
        self.hl(m, m + cw, yy, col=INK, w=0.8)
        x = m + cw + g; self.label(x, yt, 'My terms'); y2 = yt - 10
        for i, r in enumerate(['I reply within', 'Payment terms', 'Deposit', 'Late fee', 'Revisions included', 'Rush fee', 'Minimum project']):
            self.hl(x, x + cw, y2, col=INK if i == 0 else LINE, w=0.8 if i == 0 else 0.5)
            self.text(x + 4, y2 - 15, r, 'In', 9.2, INK); self.vl(x + cw * .46, y2 - 23, y2, col=HAIR); y2 -= 23
        self.hl(x, x + cw, y2, col=INK, w=0.8)
        y3 = yy - 16; h = (y3 - self.B - 12) / 2
        for i, a in enumerate(['I say yes to', 'I say no to', 'When a client pushes a boundary', 'What I do when work is quiet']):
            self.lbox(m + (i % 2) * (cw + g), y3 - (i // 2) * (h + 12), cw, h, a)
        self.done()

    def lined(self):
        top = self.head('Notes', '', 'Notes'); self.seen[-1] = ('Notes', 'Lined notes', self.n)
        self.lines(self.m, self.W - self.m, top - 30, self.B, step=22); self.done()

    def dots(self):
        top = self.head('Notes', '', 'Notes'); self.seen[-1] = ('Notes', 'Dot grid notes', self.n); m = self.m; c = self.c
        c.setFillColor(LINE); s = 14.17; n = int(self.w / s); off = (self.w - n * s) / 2; y = top - 18
        while y > self.B:
            for i in range(n + 1): c.circle(m + off + i * s, y, 0.55, stroke=0, fill=1)
            y -= s
        self.done()

    def build(self):
        T = self.tracker
        self.n = 0
        self.n = 1; self.cover(); self.howto(); self.contents()
        self.business(); self.rate(); self.idealweek(); self.yearglance()
        self.qgoals(); self.roadmap(); self.qincome(); self.qreview()
        for k in ['one', 'two', 'three']: self.mcal(k); self.mplan(k); self.mreview(k)
        self.wplan(); self.wsched(); self.wreview()
        self.daily(); self.focus()
        T('Client', 'roster', [('Client', .20), ('Contact', .16), ('Email or phone', .22), ('Type of work', .16), ('Rate', .10), ('Since', .08), ('Active', .08)],
          sec='Clients and projects', rh=22)
        self.cprofile(); self.onboarding(); self.brief(); self.timeline()
        T('Scope and', 'change log', [('Date', .10), ('What the client asked for', .36), ('In scope?', .10), ('Extra time', .12), ('Extra fee', .12), ('Agreed in writing', .20)],
          fields=[('Project', .5), ('Client', .5)], note='Write down every request that was not in the brief. Small extras are how projects lose money.', rh=24)
        self.wrapup()
        T('Leads', 'tracker', [('Lead', .18), ('Where from', .14), ('What they need', .22), ('Worth', .10), ('Stage', .12), ('Next step', .14), ('Follow up', .10)],
          sec='Pipeline', rh=22, stats=['New leads', 'Calls booked', 'Proposals sent', 'Won'])
        T('Outreach', 'log', [('Date', .10), ('Who', .20), ('Channel', .12), ('What I sent', .28), ('Reply', .12), ('Follow up on', .18)], rh=22,
          note='A few messages every week beats a panic when work dries up.')
        T('Proposal', 'tracker', [('Sent', .10), ('Client', .20), ('Project', .26), ('Amount', .12), ('Follow up', .12), ('Result', .10), ('Why', .10)], rh=22,
          stats=['Proposals sent', 'Won', 'Win rate', 'Average value'])
        self.call()
        T('Income', 'log', [('Date', .11), ('Client', .23), ('Invoice no.', .13), ('For', .21), ('Amount', .13), ('Set aside', .11), ('Kept', .08)],
          sec='Money', fields=[('Month', .4), ('Income target', .3), ('Received so far', .3)], total='Total', rh=21)
        T('Invoice', 'tracker', [('Invoice no.', .12), ('Client', .22), ('Sent', .11), ('Due', .11), ('Amount', .13), ('Reminder sent', .14), ('Paid on', .17)], total='Total owed', rh=21)
        T('Expense', 'log', [('Date', .11), ('What', .31), ('Category', .18), ('Paid with', .14), ('Amount', .14), ('Receipt', .12)],
          fields=[('Month', .4), ('Budget for the month', .6)], total='Total', rh=21)
        self.taxlog(); self.steady()
        T('Tools and', 'subscriptions', [('Tool', .22), ('What I use it for', .26), ('Cost', .11), ('Billed', .11), ('Renews on', .14), ('Keep?', .16)], rh=22,
          note='Review this list every quarter. Cancel anything you have not opened in a month.', stats=['Cost each month', 'Cost each year', 'To cancel'])
        T('Time', 'log', [('Date', .11), ('Client', .18), ('Task', .31), ('Start', .10), ('End', .10), ('Hours', .10), ('Billable', .10)], sec='Time', total='Total', rh=21)
        self.hoursweek()
        self.marketing()
        T('Portfolio', 'tracker', [('Project', .24), ('Client', .18), ('Result worth showing', .26), ('Permission', .11), ('Images', .09), ('Published', .12)], rh=24,
          note='Turn finished work into proof. Note the result while you still remember the numbers.')
        T('Wins and', 'kind words', [('Date', .12), ('Win, result or kind words', .62), ('From', .26)], rh=30,
          note='Read this page before you quote a price or doubt yourself.')
        self.rates_up()
        self.timeoff(); self.rules()
        self.lined(); self.dots()
        self.c.save()
        return self.seen


out = '/home/claude/book/out/fplanner/'
os.makedirs(out, exist_ok=True)
MON = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']; SUN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
for size, tag, fn in [(letter, 'US Letter', 'US_Letter'), (A4, 'A4', 'A4')]:
    for days, dn in [(MON, 'Monday_Start'), (SUN, 'Sunday_Start')]:
        path = out + 'Freelancer_Planner_%s_%s.pdf' % (fn, dn)
        toc = P('/tmp/_toc.pdf', size, tag, days).build()
        seen = P(path, size, tag, days, toc).build()
        print(path, 'pages', seen[-1][2])
print('WARNINGS', len(WARN))
for x in sorted(set(WARN)): print(' ', x)
