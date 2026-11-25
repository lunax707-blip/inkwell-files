# independent check of the recalculated workbook against plain Python arithmetic
import sys, datetime as dt, re, importlib.util, io, contextlib
from openpyxl import load_workbook
src, rec = sys.argv[1], sys.argv[2]
wb = load_workbook(rec, data_only=True); wf = load_workbook(src)
errs = 0
# 1. no error values anywhere, no banned characters
for ws in wb:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and (v.startswith('#') or 'Err:' in v): print('ERROR VALUE', ws.title, c.coordinate, v); errs += 1
for ws in wf:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and any(ch in v for ch in '—–·•'): print('BANNED CHAR', ws.title, c.coordinate, v); errs += 1
nform = sum(1 for ws in wf for row in ws.iter_rows() for c in row if isinstance(c.value, str) and c.value.startswith('='))
print('formulas in file:', nform)
inv, cl, db, se, pr = wb['Invoices'], wb['Clients'], wb['Dashboard'], wb['Settings'], wb['Invoice']
today = dt.date.today()
year, terms, tax, soon = se['C7'].value, se['C8'].value, se['C9'].value, se['C10'].value
def d(v): return v.date() if isinstance(v, dt.datetime) else v
rows = []
for r in range(6, 306):
    no, client, proj, issue, t, amt, pdate, paid = [inv.cell(r, c).value for c in (1, 2, 3, 4, 5, 7, 8, 9)]
    if amt in (None, ''): 
        for c in (6, 10, 11, 12, 13, 15):
            v = inv.cell(r, c).value
            if c == 6 and issue: continue
            if v not in (None, ''): print('blank row not blank', r, c, v); errs += 1
        continue
    issue, pdate = d(issue), d(pdate)
    due = issue + dt.timedelta(days=t if t not in (None, '') else terms)
    bal = amt - (paid or 0)
    if bal <= 0: stt = 'Paid'
    elif due < today: stt = 'Overdue'
    elif (paid or 0) > 0: stt = 'Part paid'
    elif (due - today).days <= soon: stt = 'Due soon'
    else: stt = 'Open'
    late = (today - due).days if stt == 'Overdue' else None
    dtp = (pdate - issue).days if stt == 'Paid' and pdate else None
    got = (d(inv.cell(r, 6).value), inv.cell(r, 10).value, inv.cell(r, 11).value, inv.cell(r, 12).value or None, inv.cell(r, 13).value)
    got = (got[0], got[1], got[2], got[3], None if got[4] in ('', None) else got[4])
    exp = (due, bal, stt, late, dtp)
    if got != exp: print('ROW MISMATCH', r, got, exp); errs += 1
    rows.append(dict(r=r, no=no, client=client, proj=proj, issue=issue, due=due, amt=amt, pdate=pdate, paid=paid or 0, bal=bal, st=stt, late=late, dtp=dtp))
print('invoice rows checked:', len(rows), {s: sum(1 for x in rows if x['st'] == s) for s in ('Paid', 'Part paid', 'Open', 'Due soon', 'Overdue')})
def chk(name, got, exp):
    global errs
    ok = (abs(got - exp) < 1e-6) if isinstance(exp, (int, float)) and isinstance(got, (int, float)) else got == exp
    if not ok: print('MISMATCH', name, repr(got), repr(exp)); errs += 1
iy = [x for x in rows if x['issue'].year == year]
py = [x for x in rows if x['pdate'] and x['pdate'].year == year]
chk('invoiced', db['B6'].value, sum(x['amt'] for x in iy))
chk('received', db['E6'].value, sum(x['paid'] for x in py))
chk('outstanding', db['H6'].value, sum(x['bal'] for x in rows if x['bal'] > 0))
chk('overdue', db['K6'].value, sum(x['bal'] for x in rows if x['st'] == 'Overdue'))
chk('sub1', db['B7'].value, f"{len(iy)} invoices sent")
paidn = sum(1 for x in iy if x['st'] == 'Paid')
pct = f"{round(paidn / len(iy) * 100) if iy else 0}%"
chk('sub2', db['E7'].value, f"By date paid. {pct} of this year's invoices paid in full")
chk('sub3', db['H7'].value, f"{sum(1 for x in rows if x['bal'] > 0)} invoices not fully paid")
chk('sub4', db['K7'].value, f"{sum(1 for x in rows if x['st'] == 'Overdue')} invoices past their due date")
chk('paid count', db['B10'].value, paidn)
dl = [x['dtp'] for x in rows if x['dtp'] is not None]
chk('avg days', db['E10'].value, sum(dl) / len(dl) if dl else 0)
chk('due soon', db['H10'].value, sum(x['bal'] for x in rows if x['bal'] > 0 and today <= x['due'] <= today + dt.timedelta(days=soon)))
chk('tax', db['K10'].value, sum(x['paid'] for x in py) * tax)
for m in range(1, 13):
    r = 14 + m
    im = [x for x in iy if x['issue'].month == m]
    chk(f'm{m} inv', db.cell(r, 3).value, sum(x['amt'] for x in im))
    chk(f'm{m} rec', db.cell(r, 4).value, sum(x['paid'] for x in py if x['pdate'].month == m))
    chk(f'm{m} cnt', db.cell(r, 5).value, len(im))
    chk(f'm{m} owed', db.cell(r, 6).value, sum(x['bal'] for x in im if x['bal'] > 0))
chk('tot inv', db['C27'].value, sum(x['amt'] for x in iy)); chk('tot rec', db['D27'].value, sum(x['paid'] for x in py))
def bucket(x):
    n = (today - x['due']).days
    return 0 if n <= 0 else 1 if n <= 30 else 2 if n <= 60 else 3 if n <= 90 else 4
for i in range(5):
    b = [x for x in rows if x['bal'] > 0 and bucket(x) == i]
    chk(f'age{i}', db.cell(31 + i, 5).value, sum(x['bal'] for x in b)); chk(f'agen{i}', db.cell(31 + i, 6).value, len(b))
chk('age total', db['E36'].value, db['H6'].value)
# clients
cstats = {}
for r in range(6, 56):
    name = cl.cell(r, 1).value
    if not name:
        for c in range(5, 13):
            if cl.cell(r, c).value not in (None, ''): print('client blank not blank', r, c); errs += 1
        continue
    mine = [x for x in rows if x['client'] == name]
    dd = [x['dtp'] for x in mine if x['dtp'] is not None]
    exp = (len(mine), sum(x['amt'] for x in mine), sum(x['paid'] for x in mine), sum(x['bal'] for x in mine if x['bal'] > 0), sum(x['bal'] for x in mine if x['st'] == 'Overdue'))
    got = tuple(cl.cell(r, c).value for c in (5, 6, 7, 8, 9))
    if any(abs(a - b) > 1e-6 for a, b in zip(got, exp)): print('CLIENT MISMATCH', name, got, exp); errs += 1
    ga = cl.cell(r, 10).value
    if dd: chk('cl avg ' + name, ga, sum(dd) / len(dd))
    elif ga not in ('', None): print('client avg should be blank', name, ga); errs += 1
    gl = d(cl.cell(r, 11).value)
    chk('cl last ' + name, gl if mine else (gl or None), max(x['issue'] for x in mine) if mine else None)
    cstats[name] = (exp[1], exp[3], r)
top = sorted(cstats.items(), key=lambda kv: (-kv[1][0], -kv[1][2]))[:5]
for i in range(5):
    gn = db.cell(31 + i, 8).value or None
    if i < len(top):
        chk(f'top{i}', gn, top[i][0]); chk(f'top{i} amt', db.cell(31 + i, 11).value, top[i][1][0]); chk(f'top{i} out', db.cell(31 + i, 12).value, top[i][1][1])
    elif gn: print('extra top client', gn); errs += 1
od = sorted([x for x in rows if x['st'] == 'Overdue'], key=lambda x: (-x['late'], -x['r']))[:5]
for i in range(5):
    gn = db.cell(40 + i, 2).value or None
    if i < len(od):
        x = od[i]
        chk(f'chase{i}', (gn, db.cell(40 + i, 4).value, d(db.cell(40 + i, 10).value), db.cell(40 + i, 12).value, db.cell(40 + i, 13).value), (x['no'], x['client'], x['due'], x['late'], x['bal']))
    elif gn: print('extra chase', gn); errs += 1
# printable invoice
sel = pr['F2'].value
if sel:
    x = next(y for y in rows if y['no'] == sel)
    chk('print', (pr['E6'].value, d(pr['C13'].value), d(pr['D13'].value), pr['F13'].value, pr['B16'].value, pr['F16'].value, pr['F19'].value, pr['F20'].value),
        (x['client'], x['issue'], x['due'], x['st'], x['proj'], x['amt'], x['paid'], x['bal']))
print('today', today, '| dashboard:', [db[c].value for c in ('B6', 'E6', 'H6', 'K6', 'B10', 'E10', 'H10', 'K10')])
print('RESULT:', 'ALL OK' if errs == 0 else f'{errs} PROBLEMS')
