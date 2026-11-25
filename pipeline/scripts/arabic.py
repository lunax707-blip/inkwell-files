import os
from PIL import Image, ImageDraw, ImageFont

F = '/home/claude/fonts/ttf/'
R = ImageFont.Layout.RAQM
def ar(size, bold=True): return ImageFont.truetype(F + 'noto-naskh-arabic-arabic-%s-normal.ttf' % ('700' if bold else '400'), size, layout_engine=R)
def kufi(size, w='600'): return ImageFont.truetype(F + 'noto-kufi-arabic-arabic-%s-normal.ttf' % w, size, layout_engine=R)
def fr(size, st='300-normal'): return ImageFont.truetype(F + 'fraunces-latin-%s.ttf' % st, size)
def ins(size, w='600'): return ImageFont.truetype(F + 'instrument-sans-latin-%s-normal.ttf' % w, size)

W, H = 2550, 3300
M = 170
INK = (20, 20, 20); GREY = (196, 196, 196); MID = (120, 120, 120); RULE = (150, 150, 150); FAINT = (205, 205, 205)

L = [('ا', 'ألف', 'Alif'), ('ب', 'باء', 'Ba'), ('ت', 'تاء', 'Ta'), ('ث', 'ثاء', 'Tha'), ('ج', 'جيم', 'Jim'), ('ح', 'حاء', 'Ha'), ('خ', 'خاء', 'Kha'),
     ('د', 'دال', 'Dal'), ('ذ', 'ذال', 'Dhal'), ('ر', 'راء', 'Ra'), ('ز', 'زاي', 'Zay'), ('س', 'سين', 'Sin'), ('ش', 'شين', 'Shin'), ('ص', 'صاد', 'Sad'),
     ('ض', 'ضاد', 'Dad'), ('ط', 'طاء', 'Ta'), ('ظ', 'ظاء', 'Dha'), ('ع', 'عين', 'Ayn'), ('غ', 'غين', 'Ghayn'), ('ف', 'فاء', 'Fa'), ('ق', 'قاف', 'Qaf'),
     ('ك', 'كاف', 'Kaf'), ('ل', 'لام', 'Lam'), ('م', 'ميم', 'Mim'), ('ن', 'نون', 'Nun'), ('ه', 'هاء', 'Ha'), ('و', 'واو', 'Waw'), ('ي', 'ياء', 'Ya')]
NOJOIN = set('ادذرزو')
T = 'ـ'

def forms(ch):
    if ch in NOJOIN: return [ch, ch, T + ch, T + ch]
    return [ch, ch + T, T + ch + T, T + ch]

def A(d, xy, s, font, fill=INK, anchor='ms'):
    d.text(xy, s, font=font, fill=fill, anchor=anchor, direction='rtl', language='ar')

def E(d, xy, s, font, fill=INK, anchor='ls', sp=0):
    if not sp: d.text(xy, s, font=font, fill=fill, anchor=anchor); return
    x, y = xy
    if anchor[0] == 'r': x -= sum(d.textlength(c, font=font) + sp for c in s) - sp
    for c in s:
        d.text((x, y), c, font=font, fill=fill, anchor='ls'); x += d.textlength(c, font=font) + sp

def dash(d, x1, x2, y, col=RULE, w=3, on=14, off=14):
    x = x1
    while x < x2:
        d.line([(x, y), (min(x + on, x2), y)], fill=col, width=w); x += on + off

def guide(d, y_base, h):
    """writing row: solid baseline, dashed top line, faint descender line"""
    d.line([(M, y_base), (W - M, y_base)], fill=RULE, width=4)
    dash(d, M, W - M, y_base - h)
    dash(d, M, W - M, y_base + int(h * 0.55), col=FAINT, w=2, on=6, off=14)

def fit(text, maxw, maxh, start, bold=True):
    s = start
    while s > 40:
        f = ar(s, bold); b = f.getbbox(text, direction='rtl', language='ar')
        if b[2] - b[0] <= maxw and b[3] - b[1] <= maxh: return f
        s -= 10
    return ar(s, bold)

def center_in(d, box, text, font, fill=INK):
    x0, y0, x1, y1 = box
    b = d.textbbox((0, 0), text, font=font, anchor='ls', direction='rtl', language='ar')
    x = x0 + (x1 - x0 - (b[2] - b[0])) / 2 - b[0]; y = y0 + (y1 - y0 - (b[3] - b[1])) / 2 - b[1]
    d.text((x, y), text, font=font, fill=fill, anchor='ls', direction='rtl', language='ar')

def header(d, right_ar, left_en, num=None):
    E(d, (M, M + 10), 'INKWELL AND CO', ins(30), sp=6)
    if num: E(d, (W - M, M + 10), num, ins(30), fill=MID, anchor='rs', sp=6)

def letter_page(i):
    ch, name, en = L[i]
    im = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
    header(d, None, None, 'LETTER %02d OF 28' % (i + 1))
    # title row
    A(d, (W - M, M + 172), name, kufi(120), anchor='rs')
    E(d, (M, M + 172), en, fr(120))
    d.line([(M, M + 240), (W - M, M + 240)], fill=INK, width=5)
    # hero box (right) and forms (left)
    top = M + 300; hb = 640
    hx0 = W - M - hb
    d.rounded_rectangle([hx0, top, W - M, top + hb], radius=28, outline=INK, width=6)
    center_in(d, (hx0 + 60, top + 60, W - M - 60, top + hb - 60), ch, fit(ch, hb - 170, hb - 170, 560))
    fx0 = M; fw = hx0 - 60 - fx0; g = 40; bw = (fw - g) // 2; bh = (hb - g) // 2
    labs = [('منفرد', 'ALONE'), ('أول الكلمة', 'START'), ('وسط الكلمة', 'MIDDLE'), ('آخر الكلمة', 'END')]
    fs = forms(ch)
    for k in range(4):
        col = 1 - (k % 2); row = k // 2   # right to left
        x = fx0 + col * (bw + g); y = top + row * (bh + g)
        d.rounded_rectangle([x, y, x + bw, y + bh], radius=22, outline=RULE, width=3)
        A(d, (x + bw - 30, y + 62), labs[k][0], kufi(38, '400'), fill=MID, anchor='rs')
        E(d, (x + 30, y + 58), labs[k][1], ins(24), fill=MID, sp=4)
        center_in(d, (x + 40, y + 90, x + bw - 40, y + bh - 30), fs[k], fit(fs[k], bw - 120, bh - 150, 260))
    # trace rows
    y = top + hb + 120
    A(d, (W - M, y), 'تتبع الحرف', kufi(50), anchor='rs'); E(d, (M, y), 'TRACE THE LETTER', ins(30), fill=MID, sp=6)
    rows = 3; rh = 262; lh = 150; n = 6
    f = fit(ch, (W - 2 * M) // n - 90, 250, 250)
    cellw = (W - 2 * M) / n
    y += 70
    for r in range(rows):
        base = y + r * rh + 172
        guide(d, base, lh)
        for k in range(n):
            cx = W - M - cellw * (k + 0.5)
            A(d, (cx, base), ch, f, fill=INK if k == 0 else GREY, anchor='ms')
    y += rows * rh + 70
    A(d, (W - M, y), 'تتبع الأشكال', kufi(50), anchor='rs'); E(d, (M, y), 'TRACE THE SHAPES', ins(30), fill=MID, sp=6)
    base = y + 70 + 172; guide(d, base, lh)
    seq = [fs[1], fs[2], fs[3], fs[1], fs[2], fs[3]]
    f2 = fit(max(seq, key=len), int(cellw) - 110, 250, 240)
    for k, s in enumerate(seq):
        cx = W - M - cellw * (k + 0.5)
        A(d, (cx, base), s, f2, fill=INK if k < 3 else GREY, anchor='ms')
    y = base + 150
    A(d, (W - M, y), 'اكتب بنفسك', kufi(50), anchor='rs'); E(d, (M, y), 'YOUR TURN', ins(30), fill=MID, sp=6)
    for r in range(2):
        b = y + 70 + 172 + r * rh
        if b < H - M: guide(d, b, lh)
    E(d, (M, H - 90), 'FOR PERSONAL USE', ins(22), fill=FAINT, sp=5)
    E(d, (W - M, H - 90), '%02d' % (i + 3), ins(22), fill=FAINT, anchor='rs', sp=5)
    return im

PAL = [(31, 111, 120), (232, 163, 61), (217, 88, 59), (43, 58, 103), (157, 181, 160)]
CREAM = (244, 233, 216); NAVY = (43, 58, 103)

def cover():
    im = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(im)
    E(d, (M, M + 10), 'INKWELL AND CO', ins(34), fill=NAVY, sp=7)
    E(d, (W - M, M + 10), 'PRINTABLE WORKSHEETS', ins(34), fill=NAVY, anchor='rs', sp=7)
    A(d, (W - M, 640), 'أكتب الحروف', kufi(250), fill=NAVY, anchor='rs')
    A(d, (W - M, 960), 'العربية', kufi(250), fill=(217, 88, 59), anchor='rs')
    E(d, (M, 1150), 'Arabic Alphabet Tracing', fr(120), fill=NAVY)
    E(d, (M, 1260), '28 letter worksheets for little hands', fr(72, '300-italic'), fill=(217, 88, 59))
    # tile grid 7 x 4 rtl
    gx0 = M; gy0 = 1400; g = 26; tw = (W - 2 * M - 6 * g) // 7
    for i, (ch, _, _) in enumerate(L):
        col = 6 - (i % 7); row = i // 7
        x = gx0 + col * (tw + g); y = gy0 + row * (tw + g)
        c = PAL[(i + row) % 5]
        d.rounded_rectangle([x, y, x + tw, y + tw], radius=30, fill=c)
        center_in(d, (x + 50, y + 50, x + tw - 50, y + tw - 50), ch, fit(ch, tw - 130, tw - 130, 230), fill=CREAM if c != (232, 163, 61) and c != (157, 181, 160) else NAVY)
    E(d, (M, H - M), 'Big model letter, four letter shapes, tracing rows and free practice lines on every page.', ins(40, '400'), fill=NAVY)
    return im

def chart():
    im = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
    header(d, None, None, 'THE ALPHABET')
    A(d, (W - M, M + 172), 'الحروف العربية', kufi(120), anchor='rs')
    E(d, (M, M + 172), 'All 28 letters', fr(120))
    d.line([(M, M + 240), (W - M, M + 240)], fill=INK, width=5)
    g = 26; tw = (W - 2 * M - 3 * g) // 4; gy0 = M + 310; th = (H - M - 60 - gy0 - 6 * g) // 7
    for i, (ch, name, en) in enumerate(L):
        col = 3 - (i % 4); row = i // 4
        x = M + col * (tw + g); y = gy0 + row * (th + g)
        d.rounded_rectangle([x, y, x + tw, y + th], radius=22, outline=RULE, width=3)
        center_in(d, (x + tw // 2, y + 20, x + tw - 30, y + th - 20), ch, fit(ch, tw // 2 - 80, th - 110, 200))
        A(d, (x + tw // 2 - 20, y + th // 2 - 4), name, kufi(50, '400'), anchor='rs')
        E(d, (x + tw // 2 - 20, y + th // 2 + 62), en.upper(), ins(26), fill=MID, anchor='rs', sp=4)
        E(d, (x + 28, y + 52), '%02d' % (i + 1), ins(24), fill=FAINT, sp=3)
    E(d, (M, H - 90), 'FOR PERSONAL USE', ins(22), fill=FAINT, sp=5)
    E(d, (W - M, H - 90), '02', ins(22), fill=FAINT, anchor='rs', sp=5)
    return im

out = '/home/claude/book/out/arabic/'; os.makedirs(out, exist_ok=True)
cv = cover(); cv.save(out + 'Arabic_Alphabet_Tracing_cover.jpg', quality=90)
pages = [cv, chart().convert('RGB')] + [letter_page(i).convert('RGB') for i in range(28)]
pages[0].save(out + 'Arabic_Alphabet_Tracing_28_worksheets.pdf', save_all=True, append_images=pages[1:], resolution=300, quality=88)
# contact sheets
th = [p.resize((510, 660)) for p in pages]
for k in range(0, 30, 10):
    s = Image.new('RGB', (5 * 520 + 10, 2 * 670 + 10), (130, 130, 130))
    for j, t in enumerate(th[k:k + 10]): s.paste(t, (10 + (j % 5) * 520, 10 + (j // 5) * 670))
    s.save(out + 'sheet%d.png' % (k // 10))
pages[3].resize((1275, 1650)).save(out + 'p_ba.png'); pages[19].resize((1275, 1650)).save(out + 'p_ayn.png')
print(len(pages), os.path.getsize(out + 'Arabic_Alphabet_Tracing_28_worksheets.pdf') // 1024, 'KB')
