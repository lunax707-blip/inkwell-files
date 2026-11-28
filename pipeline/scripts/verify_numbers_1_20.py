# Independent check of Numbers 1 to 20 Worksheets. Reads the manifest written by numbers_1_20.py
# (every object and ten frame dot as it was drawn, plus the printed answer key) and recomputes every answer
# without using the builder's own answer logic. Also reads the PDF text for banned characters and page counts.
# Must print FAILURES 0 before listing.
import json, subprocess, sys, collections

OUT = '/home/claude/book/out/numbers/'
WORDS = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split()
fails = 0; checks = 0


def ok(cond, msg):
    global fails, checks
    checks += 1
    if not cond: fails += 1; print('FAIL', msg)


for fn in ['Numbers_1_to_20_Worksheets_US_Letter', 'Numbers_1_to_20_Worksheets_A4']:
    d = json.load(open(OUT + fn + '.json')); key = d['key']; marks = d['marks']
    cnt = collections.Counter((m['page'], str(m['item']), m['type']) for m in marks)
    kinds = collections.defaultdict(set)
    for m in marks:
        if m['type'] == 'obj': kinds[(m['page'], str(m['item']))].add(m['kind'])
    for e in key:
        p, t, data, note = e['page'], e['title'], e['data'], e['note']
        tag = '%s p%s %s' % (fn[-6:], p, t)
        if e['kind'] == 'shown':                                   # chart pages
            for n in data:
                ok(cnt[(p, 'row%d' % n, 'dot')] == n, tag + ' chart dots %d' % n)
                if n <= 10: ok(cnt[(p, 'obj%d' % n, 'obj')] == n, tag + ' chart objects %d' % n)
        elif isinstance(note, dict) and 'finds' in note:           # number pages
            for f, a in zip(note['finds'], data):
                n = f['n']; pg = f['page']
                ok(f['row'].count(n) == f['count'] and len(f['row']) == 10, tag + ' find row %d' % n)
                ok(a.startswith('%d:' % n) and a.endswith('circle %d' % f['row'].count(n)), tag + ' find key %d' % n)
                if n > 10: ok('10 and %d,' % (n - 10) in a, tag + ' ten and %d' % n)
                ok(cnt[(pg, 'frame', 'dot')] == n, tag + ' hero frame %d' % n)
                if n <= 10: ok(cnt[(pg, 'hero', 'obj')] == n, tag + ' hero objects %d' % n)
                ok(all(1 <= v <= 20 for v in f['row']), tag + ' find range')
            ok(len(note['finds']) == 10, tag + ' ten number pages')
        elif isinstance(note, dict) and 'count' in note:
            for i, a in enumerate(data):
                ok(cnt[(p, str(i + 1), 'obj')] == int(a), tag + ' item %d' % (i + 1)); ok(len(kinds[(p, str(i + 1))]) == 1, tag + ' one kind')
        elif isinstance(note, dict) and 'choose' in note:
            for i, (a, opts) in enumerate(zip(data, note['choose'])):
                ok(cnt[(p, str(i + 1), 'obj')] == int(a), tag + ' item %d' % (i + 1))
                ok(opts.count(int(a)) == 1 and len(set(opts)) == 3 and all(1 <= o <= 20 for o in opts), tag + ' options %d' % (i + 1))
        elif isinstance(note, dict) and 'match' in note:
            right = note['match']; letters = 'ABCDEFGH'
            ok(sorted(right) == sorted(note['left']) and len(set(right)) == len(right), tag + ' match sets')
            for i, a in enumerate(data):
                c_ = cnt[(p, str(i + 1), 'obj')]; L = a.split(' ')[0]
                ok(c_ == note['left'][i], tag + ' drawn %d' % (i + 1))
                ok(right[letters.index(L)] == c_ and a == '%s (%d)' % (L, c_), tag + ' match %d' % (i + 1))
                ok(letters.index(L) != i, tag + ' not straight across %d' % (i + 1))
        elif note == 'frames':
            for i, a in enumerate(data): ok(cnt[(p, str(i + 1), 'dot')] == int(a), tag + ' frame %d' % (i + 1))
        elif note == 'fill':
            for a in data: ok(1 <= int(a.split()[0]) <= 20, tag + ' fill')
        elif isinstance(note, dict) and 'tenmore' in note:
            for i, (a, n) in enumerate(zip(data, note['tenmore'])):
                ok(cnt[(p, str(i + 1), 'dot')] == n and a == '10 and %d make %d' % (n - 10, 10 + (n - 10)), tag + ' ten more %d' % (i + 1))
        elif isinstance(note, dict) and any(k in note for k in ('missing', 'backwards', 'counton')):
            k = [k for k in ('missing', 'backwards', 'counton') if k in note][0]
            for i, (a, (seq, hid)) in enumerate(zip(data, note[k])):
                step = -1 if k == 'backwards' else 1
                ok(all(seq[j + 1] - seq[j] == step for j in range(len(seq) - 1)), tag + ' sequence %d' % (i + 1))
                ok(a == ', '.join(str(seq[0] + step * j) for j in hid), tag + ' missing %d' % (i + 1))
                ok(len(hid) < len(seq) and all(1 <= v <= 20 for v in seq), tag + ' range %d' % (i + 1))
                if k == 'counton': ok(0 not in hid, tag + ' start shown')
        elif isinstance(note, dict) and 'neighbors' in note:
            for i, (a, (n, md)) in enumerate(zip(data, note['neighbors'])):
                want = {'after': str(n + 1), 'before': str(n - 1), 'both': '%d and %d' % (n - 1, n + 1), 'between': str(n)}[md]
                ok(a == want and 1 <= n - 1 and n + 1 <= 21, tag + ' neighbor %d' % (i + 1))
                if md in ('after', 'both', 'between'): ok(n + 1 <= 20, tag + ' stays in 1 to 20 (%d)' % (i + 1))
        elif isinstance(note, dict) and 'ask' in note:
            for i, (a, (x, y)) in enumerate(zip(data, note['pairs'])):
                ca = cnt[(p, '%dA' % (i + 1), 'obj')]; cb = cnt[(p, '%dB' % (i + 1), 'obj')]
                ok((ca, cb) == (x, y) and ca != cb, tag + ' drawn %d' % (i + 1))
                want = ('A' if ca > cb else 'B') if note['ask'] == 'more' else ('A' if ca < cb else 'B')
                ok(a == want, tag + ' more or fewer %d' % (i + 1))
        elif isinstance(note, dict) and 'compare' in note:
            for i, (a, (x, y)) in enumerate(zip(data, note['pairs'])):
                ok(x != y and int(a) == (max(x, y) if note['compare'] == 'bigger' else min(x, y)), tag + ' compare %d' % (i + 1))
        elif isinstance(note, dict) and 'order' in note:
            for i, (a, st) in enumerate(zip(data, note['order'])):
                ok(a == ', '.join(map(str, sorted(st))) and len(set(st)) == len(st) and list(st) != sorted(st), tag + ' order %d' % (i + 1))
        elif isinstance(note, dict) and 'words' in note:
            pr = note['words']
            ok(sorted(v for v, _ in pr) == sorted(w for _, w in pr), tag + ' words sets'); ok(all(v != w for v, w in pr), tag + ' words not straight across')
            for a in data: n, w = a.split(' '); ok(WORDS[int(n)] == w, tag + ' word ' + a)
        elif isinstance(note, dict) and 'dots' in note:
            ok(note['dots'] in (10, 20), tag + ' dot count')
        elif isinstance(note, dict) and 'maze' in note:
            g = note['maze']; path = [tuple(q) for q in note['path']]; R = len(g); C = len(g[0])
            ok([g[y][x] for x, y in path] == list(range(1, 21)), tag + ' maze path values')
            # walk it without the path: from 1, exactly one neighbour may hold the next number
            pos = [(x, y) for y in range(R) for x in range(C) if g[y][x] == 1]; ok(len(pos) >= 1, tag + ' has a 1')
            cur = path[0]; walked = [cur]; unique = True
            for v in range(2, 21):
                nb = [(cur[0] + dx, cur[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                nb = [q for q in nb if 0 <= q[0] < C and 0 <= q[1] < R and g[q[1]][q[0]] == v]
                if len(nb) != 1: unique = False; break
                cur = nb[0]; walked.append(cur)
            ok(unique and walked == path, tag + ' maze has one route')
            mv = {(1, 0): 'right', (-1, 0): 'left', (0, 1): 'down', (0, -1): 'up'}
            steps = [mv[(b[0] - a[0], b[1] - a[1])] for a, b in zip(path, path[1:])]
            printed = ' '.join(data).replace('From 1 go ', '').replace(' to 20.', '').replace(',', ' ').split()
            ok(printed == steps, tag + ' maze key steps')
        elif isinstance(note, dict) and 'spy' in note:
            for a, (n, k) in zip(data, note['spy']):
                ok(cnt[(p, k, 'obj')] == n and a.startswith('%d ' % n), tag + ' spy ' + k)
            ok(len(set(n for n, _ in note['spy'])) == len(note['spy']), tag + ' spy counts differ')
        elif e['title'].startswith('Before') or True:
            ok(False, tag + ' has no checker')
    # every answer bearing page is covered, and the PDF itself
    txt = subprocess.run(['pdftotext', '-layout', OUT + fn + '.pdf', '-'], capture_output=True, text=True).stdout
    pages = txt.split('\f')
    ok(d['pages'] == len(pages) - 1 or d['pages'] == len(pages), fn + ' page count %d vs %d' % (d['pages'], len(pages)))
    ok(d['pages'] >= 50, fn + ' at least 50 pages')
    for ch, nm in [('—', 'em dash'), ('–', 'en dash'), ('·', 'middle dot'), ('•', 'bullet')]:
        ok(ch not in txt, fn + ' contains ' + nm)
    for i, pg in enumerate(pages[:d['pages']]):
        if 2 <= i + 1: ok(('%d' % (i + 1)) in pg or i + 1 == 60, fn + ' page number %d' % (i + 1))
    info = subprocess.run(['pdfinfo', OUT + fn + '.pdf'], capture_output=True, text=True).stdout
    size = [l for l in info.splitlines() if l.startswith('Page size')][0]
    ok(('612 x 792' in size) if 'Letter' in fn else ('595.2' in size and '841.8' in size), fn + ' ' + size)
    print(fn, 'pages', d['pages'], 'key entries', len(key), 'marks', len(marks))

print('CHECKS', checks)
print('FAILURES', fails)
sys.exit(1 if fails else 0)
