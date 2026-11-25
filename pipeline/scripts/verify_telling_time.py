# Independent check of Telling Time Worksheets: decodes every drawn clock from its hand angles
# and recomputes every answer with its own arithmetic, then compares with the printed answer key.
import json, sys, subprocess, re
OUT = '/home/claude/book/out/time/'
bad = 0
def fail(*a):
    global bad; bad += 1; print('FAIL', *a)
def decode(ck):
    mi = ck['minute_angle'] / 6.0
    if abs(mi - round(mi)) > 1e-6: fail('minute hand between marks', ck)
    mi = int(round(mi)); hh = int(ck['hour_angle'] // 30) or 12
    if abs(ck['hour_angle'] - ((hh % 12) * 30 + mi / 2)) > 1e-6: fail('hour hand does not agree with minute hand', ck)
    return hh, mi
def f(h, m): return '%d:%02d' % (h, m)
def say(h, m):
    nx = h % 12 + 1
    return {0: "%d o'clock" % h, 30: 'half past %d' % h, 15: 'quarter past %d' % h, 45: 'quarter to %d' % nx}[m]
def mins(s):
    h, m = s.split(':'); return (int(h) % 12) * 60 + int(m)
def unmins(t):
    t %= 720; return f(t // 60 or 12, t % 60)
def dur(d):
    h, m = divmod(d, 60); p = []
    if h: p.append('%d hour%s' % (h, '' if h == 1 else 's'))
    if m: p.append('%d minutes' % m)
    return ' '.join(p)
for fn in ['Telling_Time_Worksheets_US_Letter', 'Telling_Time_Worksheets_A4']:
    d = json.load(open(OUT + fn + '.json')); n = 0
    clocks = {}
    for ck in d['clocks']: clocks.setdefault(ck['page'], {})[str(ck['item'])] = decode(ck)
    txt = subprocess.run(['pdftotext', '-layout', OUT + fn + '.pdf', '-'], capture_output=True, text=True).stdout
    pages = txt.split('\f')
    if len(pages) - 1 != d['pages']: fail('page count', len(pages) - 1, d['pages'])
    for ch_, nm in [('—', 'em dash'), ('–', 'en dash'), ('·', 'middle dot'), ('•', 'bullet')]:
        if ch_ in txt: fail(nm, 'found in', fn)
    for e in d['key']:
        pg, data, note = e['page'], e['data'], e['note']; cs = clocks.get(pg, {}); n += 1
        if e['kind'] == 'shown':
            got = [f(*cs['big'])] + [f(*cs['ex%d' % k]) for k in range(1, len(data))]
            if got != data: fail(pg, 'learn page clocks', got, data)
            for g in got:
                if g not in pages[pg - 1] and say(*map(int, g.split(':'))) not in pages[pg - 1] if int(g.split(':')[1]) in (0, 15, 30, 45) else g not in pages[pg - 1]: fail(pg, 'caption missing', g)
        elif e['kind'] == 'clocks':
            for h, m in data:
                if not (1 <= h <= 12 and 0 <= m < 60): fail(pg, 'bad time', h, m)
                if f(h, m) not in pages[pg - 1] and (m not in (0, 15, 30, 45) or say(h, m) not in pages[pg - 1]): fail(pg, 'label not printed', h, m)
            if len(set(map(tuple, data))) != len(data): fail(pg, 'repeated time on draw page')
        elif isinstance(note, dict) and 'read' in note:
            got = [(f if note['read'] == 'digital' else say)(*cs[str(i + 1)]) for i in range(len(data))]
            if got != data: fail(pg, 'read', got, data)
            if len(set(got)) != len(got): fail(pg, 'repeated clock on read page')
        elif isinstance(note, dict) and 'match' in note:
            fn_ = f if note['match'] == 'digital' else say
            for i, a in enumerate(data):
                want = fn_(*cs[str(i + 1)]); L = 'ABCDEFGH'[note['right'].index(want)]
                if a != '%s (%s)' % (L, want): fail(pg, 'match', i + 1, a, want, L)
                if note['right'].count(want) != 1: fail(pg, 'match option not unique', want)
        elif isinstance(note, dict) and 'choose' in note:
            for i, a in enumerate(data):
                h, m = cs[str(i + 1)]; opts = note['choose'][i]
                right = [o for o in opts if o == f(h, m) or (m in (0, 15, 30, 45) and o == say(h, m))]
                if len(opts) != 3 or len(set(opts)) != 3 or right != [a]: fail(pg, 'choose', i + 1, a, opts, (h, m))
                # no two options may describe the same moment
                def norm(o):
                    if ':' in o: return mins(o)
                    for hh in range(1, 13):
                        for mm in (0, 15, 30, 45):
                            if say(hh, mm) == o: return mins(f(hh, mm))
                if len({norm(o) for o in opts}) != 3: fail(pg, 'two options mean the same time', opts)
        elif isinstance(note, dict) and 'delta' in note:
            for i, a in enumerate(data):
                if unmins(mins(f(*cs[str(i + 1)])) + note['delta']) != a: fail(pg, 'later', i + 1, a)
        elif isinstance(note, dict) and 'rows' in note:
            for i, a in enumerate(data):
                ts = [mins(f(*cs['%d%s' % (i + 1, k)])) for k in 'abcd']
                if len(set(ts)) != 4: fail(pg, 'order tie')
                if any(t < 60 for t in ts): fail(pg, 'order row contains 12 something, ambiguous')
                if ' '.join(str(sorted(ts).index(t) + 1) for t in ts) != a: fail(pg, 'order', i + 1, a, ts)
        elif isinstance(note, dict) and 'pairs' in note:
            for i, a in enumerate(data):
                t1 = mins(f(*cs['%da' % (i + 1)])); t2 = mins(f(*cs['%db' % (i + 1)]))
                if dur((t2 - t1) % 720) != a: fail(pg, 'elapsed', i + 1, a, t1, t2)
        elif isinstance(note, dict) and 'trains' in note:
            tr = {nm: (mins(a), mins(b)) for nm, a, b, dd in note['trains']}
            for nm, a, b, dd in note['trains']:
                if mins(b) - mins(a) != dd or dd <= 0: fail(pg, 'train row', nm)
            want = [unmins(tr['Green train'][0]), [k for k, v in tr.items() if v[0] == mins('10:30')][0], unmins(tr['Blue train'][1]),
                    dur(tr['Red train'][1] - tr['Red train'][0]), max(tr, key=lambda k: tr[k][1] - tr[k][0]),
                    [k for k, v in tr.items() if v[1] == mins('10:00')][0], min((k for k in tr if tr[k][0] >= mins('9:00')), key=lambda k: tr[k][0])]
            if want != data: fail(pg, 'timetable', want, data)
            if len([k for k, v in tr.items() if v[1] == mins('10:00')]) != 1: fail(pg, 'timetable q6 not unique')
        elif note == 'hour':
            if [str(cs[str(i + 1)][0]) for i in range(len(data))] != data: fail(pg, 'hour hand page')
            if any(cs[str(i + 1)][1] for i in range(len(data))): fail(pg, 'hour hand page not on the hour')
        elif note == 'fives':
            if data != [str(k) for k in range(15, 60, 5)]: fail(pg, 'fives')
        elif e['title'] == 'Time stories':
            if data != ['4:00', '9:00', '1 hour', '5:30', '2:30', '4 hours']: fail(pg, 'stories', data)
        elif e['title'] == 'a.m. or p.m.?':
            if data != ['a.m.'] * 3 + ['p.m.'] * 5: fail(pg, 'am pm', data)
        elif e['title'] == 'Fill in the missing numbers':
            for row in data:
                if not all(1 <= int(k) <= 12 for k in row.split(', ')): fail(pg, 'missing numbers')
        elif e['title'] == 'The parts of a clock':
            if data != ['hour', 'minute', '12']: fail(pg, 'parts')
        else: fail(pg, 'unchecked entry', e['title'])
        # every answer string must appear in the printed answer key pages
        if e['kind'] != 'shown':
            keytxt = ' '.join(' '.join(pages[k].split()) for k in range(len(pages)) if 'Answer key' in pages[k][:400])
            if 'Page %d' % pg not in keytxt: fail(pg, 'not in printed key')
            for a in (data if e['kind'] == 'text' else [f(*x) for x in data]):
                if str(a) not in keytxt: fail(pg, 'answer not printed in key', a)
    info = subprocess.run(['pdfinfo', OUT + fn + '.pdf'], capture_output=True, text=True).stdout
    fonts = subprocess.run(['pdffonts', OUT + fn + '.pdf'], capture_output=True, text=True).stdout
    emb = all(l.split()[-5] == 'yes' for l in fonts.splitlines()[2:])
    print(fn, '| entries checked', n, '| clocks decoded', len(d['clocks']), '|', re.search(r'Page size:.*', info).group(0), '| pages', d['pages'], '| fonts embedded', emb)
print('FAILURES', bad); sys.exit(1 if bad else 0)
