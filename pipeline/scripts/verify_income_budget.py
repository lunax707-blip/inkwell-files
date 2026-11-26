# Independent check of the Irregular Income Budget workbook.
# Usage: python3 verify_income_budget.py source.xlsx recalculated.xlsx
#        python3 verify_income_budget.py --stress workdir     (builds stress files, recalculates them in LibreOffice, checks each)
# Reads the typed inputs from the recalculated copy, redoes every calculation in plain Python and compares with what LibreOffice worked out.
import sys, os, subprocess, random, datetime as dt
from decimal import Decimal, ROUND_HALF_UP
from openpyxl import load_workbook

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def d(v): return v.date() if isinstance(v, dt.datetime) else v
def num(v): return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0
def q(x, pat="0"):
    v = Decimal(repr(round(float(x), 7))).quantize(Decimal(pat), rounding=ROUND_HALF_UP)
    if v == 0: v = abs(v)
    return v
def t0(x): return f"{q(x):,}"                # TEXT(x,"#,##0")
def t1(x): return f"{q(x, '0.1')}"            # TEXT(x,"0.0")
def tp(x): return f"{q(x * 100)}%"            # TEXT(x,"0%")

def check(src, rec, quiet=False):
    wb = load_workbook(rec, data_only=True); wf = load_workbook(src)
    errs = [0]
    def bad(*a):
        errs[0] += 1
        if errs[0] <= 40: print("  PROBLEM", *a)
    def eq(name, got, exp):
        if isinstance(exp, (int, float)) and isinstance(got, (int, float)): ok = abs(got - exp) < 1e-6
        elif exp in ("", None): ok = got in ("", None)
        else: ok = got == exp
        if not ok: bad(name, "got", repr(got), "expected", repr(exp))
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and (v.startswith("#") or "Err:" in v): bad("error value", ws.title, c.coordinate, v)
    nform = 0
    for ws in wf:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str):
                    if v.startswith("="): nform += 1
                    if any(ch in v for ch in "—–·•"): bad("banned character", ws.title, c.coordinate, v)
    se, inc, ex, bu, pp, db = wb["Settings"], wb["Income"], wb["Expenses"], wb["Budget"], wb["Pay Plan"], wb["Dashboard"]
    today = dt.date.today()
    name, cur, year = se["C5"].value, se["C6"].value, se["C7"].value
    tax, pay, buf0, goal, pot0, cush, month = [num(se[f"C{r}"].value) for r in range(8, 15)]
    month = se["C14"].value
    NM = max(0, min(12, (today.year - year) * 12 + today.month)); NC = max(0, min(12, (today.year - year) * 12 + today.month - 1))
    SM = month if month not in (None, "") else (1 if NM == 0 else NM)
    eq("months so far", se["C17"].value, NM); eq("full months", se["C18"].value, NC); eq("dashboard month", se["C19"].value, SM)

    def inm(x, m): return isinstance(x, dt.date) and x.year == year and x.month == m
    incs = [(d(inc.cell(r, 1).value), inc.cell(r, 4).value) for r in range(6, 306)]
    cats = []                                   # (row, name, group, budget)
    for r in range(6, 36): cats.append((r, bu.cell(r, 1).value, bu.cell(r, 2).value, bu.cell(r, 3).value))
    def group_of(cat):
        if cat in (None, ""): return ""
        for _, n, g, _ in cats:
            if n not in (None, "") and str(n).lower() == str(cat).lower(): return "" if g is None else str(g)
        return "Not in budget"
    exps = []
    for r in range(6, 506):
        dte, cat, amt = d(ex.cell(r, 1).value), ex.cell(r, 3).value, ex.cell(r, 4).value
        g = group_of(cat); eq(f"expense group row {r}", ex.cell(r, 5).value, g)
        exps.append((dte, cat, amt, g))

    # budget tab
    key = {}
    tot = {c: 0 for c in (3, 4, 5, 7, 8, 9)}
    brow = {}
    for r, n, g, b in cats:
        got = [bu.cell(r, c).value for c in range(4, 11)]
        if n in (None, ""):
            if any(v not in (None, "") for v in got): bad("budget blank row not blank", r, got)
            continue
        mine = [e for e in exps if e[1] not in (None, "") and str(e[1]).lower() == str(n).lower()]
        spent = sum(num(e[2]) for e in mine if inm(e[0], SM))
        ytd = sum(num(e[2]) for e in mine if isinstance(e[0], dt.date) and e[0].year == year)
        bb = num(b)
        exp = [spent, bb - spent, "" if bb == 0 else spent / bb, ytd, bb * NM, bb * NM - ytd, "" if spent == 0 else spent + r / 1000000]
        for c, (gv, ev) in enumerate(zip(got, exp), start=4): eq(f"budget {n} col {c}", gv, ev)
        if spent != 0: key[r] = spent + r / 1000000
        brow[r] = (n, g, bb, spent)
        for c, v in zip((3, 4, 5, 7, 8, 9), (bb, spent, bb - spent, ytd, bb * NM, bb * NM - ytd)): tot[c] += v
    for c, v in tot.items(): eq(f"budget total col {c}", bu.cell(36, c).value, v)

    # pay plan
    P = []
    pb, pt = buf0, pot0
    for m in range(1, 13):
        r = 5 + m
        B = sum(num(a) for x, a in incs if inm(x, m)); C = B * tax
        Dc = sum(num(e[2]) for e in exps if inm(e[0], m) and e[3] == "Business"); E = B - C - Dc
        K = sum(num(e[2]) for e in exps if inm(e[0], m) and e[3] == "Personal")
        ov, tp_ = pp.cell(r, 6).value, pp.cell(r, 9).value
        if m > NM: G = H = J = Lf = st = ""
        else:
            G = ov if ov not in (None, "") else max(0, min(pay, pb + E)); H = pb + E - G; J = pt + C - num(tp_); Lf = G - K
            st = "Buffer empty" if H < 0 else "Short pay" if G < pay else "Buffer grew" if E >= G else "Buffer used"
            pb, pt = H, J
        exp = {2: B, 3: C, 4: Dc, 5: E, 7: G, 8: H, 10: J, 11: K, 12: Lf, 13: st, 14: E if m <= NC else "", 15: B if m <= NC else ""}
        for c, v in exp.items(): eq(f"pay plan {MONTHS[m - 1]} col {c}", pp.cell(r, c).value, v)
        eq(f"pay plan label {m}", pp.cell(r, 1).value, MONTHS[m - 1])
        P.append(dict(B=B, C=C, D=Dc, E=E, G=G, H=H, J=J, K=K, L=Lf, I=num(tp_)))
    for c, k in ((2, "B"), (3, "C"), (4, "D"), (5, "E"), (7, "G"), (9, "I"), (11, "K"), (12, "L")):
        eq(f"pay plan total {k}", pp.cell(18, c).value, sum(num(x[k]) for x in P))

    # dashboard
    buf_now = buf0 if NM == 0 else P[NM - 1]["H"]; pot_now = pot0 if NM == 0 else P[NM - 1]["J"]
    done = P[:NC]
    afford = 0 if NC == 0 else max(0, sum(x["E"] for x in done) / NC * (1 - cush))
    pay_sel = num(P[SM - 1]["G"]); per_sel = P[SM - 1]["K"]; MN = MONTHS[SM - 1]
    npay = sum(1 for x, a in incs if isinstance(x, dt.date) and x.year == year and a not in (None, ""))
    eq("banner", db["B3"].value, ("" if name in (None, "") else f"{name}   |   ") + f"Year {year}   |   Amounts in {cur}   |   Budget month: {MN}")
    eq("income year", db["B6"].value, sum(x["B"] for x in P)); eq("income sub", db["B7"].value, f"Payments logged: {npay}")
    eq("paid year", db["E6"].value, sum(num(x["G"]) for x in P)); eq("paid sub", db["E7"].value, f"Steady pay of {t0(pay)} a month")
    eq("buffer now", db["H6"].value, buf_now); eq("buffer sub", db["H7"].value, f"Goal {t0(goal * pay)} ({t1(goal)} months of pay)")
    eq("tax pot", db["K6"].value, pot_now); eq("tax sub", db["K7"].value, f"{tp(tax)} of income set aside, less tax paid")
    eq("months of pay", db["B10"].value, buf_now / pay if pay > 0 else 0)
    eq("afford", db["E10"].value, afford); eq("afford sub", db["E11"].value, f"Average finished month, less {tp(cush)} cushion")
    eq("leanest", db["H10"].value, 0 if NC == 0 else min(x["B"] for x in done))
    eq("leanest sub", db["H11"].value, "Needs one finished month" if NC == 0 else f"Best {t0(max(x['B'] for x in done))}, average {t0(sum(x['B'] for x in done) / NC)}")
    eq("left from pay", db["K10"].value, pay_sel - per_sel); eq("left sub", db["K11"].value, f"Pay minus personal spending, {MN}")
    for m in range(1, 13):
        r = 14 + m; x = P[m - 1]
        for c, k in zip((3, 4, 5, 6, 7), "BCDGH"): eq(f"dash {MONTHS[m - 1]} {k}", db.cell(r, c).value, x[k])
    for c, k in zip((3, 4, 5, 6), "BCDG"): eq(f"dash total {k}", db.cell(27, c).value, sum(num(x[k]) for x in P))
    eq("dash total buffer", db["G27"].value, buf_now)
    eq("budget title", db["B29"].value, f"Budget for {MN}"); eq("where title", db["I29"].value, f"Where the money went in {MN}")
    gb = {g: sum(v[2] for v in brow.values() if v[1] == g) for g in ("Business", "Personal")}
    gs = {g: sum(v[3] for v in brow.values() if v[1] == g) for g in ("Business", "Personal")}
    for i, g in enumerate(("Business", "Personal")):
        eq(f"{g} budget", db.cell(31 + i, 5).value, gb[g]); eq(f"{g} spent", db.cell(31 + i, 6).value, gs[g]); eq(f"{g} left", db.cell(31 + i, 7).value, gb[g] - gs[g])
    eq("all budget", db["E33"].value, sum(gb.values())); eq("all spent", db["F33"].value, sum(gs.values())); eq("all left", db["G33"].value, sum(gb.values()) - sum(gs.values()))
    eq("paid this month", db["F34"].value, pay_sel); eq("left this month", db["F35"].value, pay_sel - per_sel)
    top = sorted(key.items(), key=lambda kv: -kv[1])[:5]
    for i in range(5):
        r = 31 + i
        got = (db.cell(r, 9).value, db.cell(r, 11).value, db.cell(r, 12).value, db.cell(r, 13).value)
        if i < len(top):
            n, g, bb, sp = brow[top[i][0]]
            eq(f"top {i} name", got[0], n); eq(f"top {i} group", got[1], "" if g is None else g); eq(f"top {i} spent", got[2], sp); eq(f"top {i} budget", got[3], bb)
        elif any(v not in (None, "") for v in got): bad("extra top category", got)
    if pay <= 0: l1 = "Buffer: type your monthly pay on the Settings tab to see how long your buffer lasts."
    else:
        l1 = f"Buffer: {t0(buf_now)} covers {t1(buf_now / pay)} months of pay. Your goal is {t1(goal)} months ({t0(goal * pay)}). "
        l1 += "Goal reached." if buf_now >= goal * pay else f"Still to build: {t0(goal * pay - buf_now)}."
    if pay <= 0: l2 = f"Pay: type your monthly pay on the Settings tab. Your income so far supports about {t0(afford)} a month."
    elif NC == 0: l2 = "Pay: once one full month is logged, this line tells you whether your pay matches your income."
    elif pay <= afford: l2 = f"Pay: {t0(pay)} a month is within what your income has supported so far ({t0(afford)})."
    else: l2 = f"Pay: {t0(pay)} a month is more than your income has supported so far ({t0(afford)}). Lower it, or expect the buffer to shrink."
    PB = gb["Personal"]
    l3 = f"Budget: your personal budget adds up to {t0(PB)} a month. Set your pay to see whether it fits." if pay <= 0 else f"Budget: your personal budget of {t0(PB)} a month fits inside your pay." if PB <= pay else f"Budget: your personal budget of {t0(PB)} a month is higher than your pay. Trim {t0(PB - pay)} or raise your pay."
    l4 = "Tax: your tax pot is below zero. Check the Tax paid from pot column on the Pay Plan tab." if pot_now < 0 else f"Tax: your pot holds {t0(pot_now)}. Keep it in a separate account so it is there when the bill comes."
    unc = sum(1 for e in exps if isinstance(e[2], (int, float)) and e[3] not in ("Business", "Personal"))
    l5 = "Log: every expense has a category from the Budget tab." if unc == 0 else f"Log: expense rows with no category, or one that is not on the Budget tab: {unc}. They are left out of the totals until fixed."
    for i, l in enumerate((l1, l2, l3, l4, l5)): eq(f"health line {i + 1}", db.cell(38 + i, 2).value, l)
    if not quiet:
        print("  formulas in file:", nform, "| today", today, "| months counted", NM, "finished", NC, "dashboard month", SM)
        print("  income rows", sum(1 for x, a in incs if a not in (None, "")), "| expense rows", sum(1 for e in exps if e[2] not in (None, "")), "| categories", len(brow))
        print("  cards:", [db[c].value for c in ("B6", "E6", "H6", "K6", "B10", "E10", "H10", "K10")])
    print("  RESULT:", "ALL OK" if errs[0] == 0 else f"{errs[0]} PROBLEMS", "|", os.path.basename(rec))
    return errs[0]

def stress(work):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import income_budget as ib
    os.makedirs(work, exist_ok=True)
    ty = dt.date.today().year
    files = []
    def variant(tag, seed, year, **kw):
        rnd = random.Random(seed)
        names = [n for n, _ in ib.BUSINESS + ib.PERSONAL] + [f"Extra category {i}" for i in range(1, 11)]
        budget = []
        for i, n in enumerate(names):
            g = "Business" if i < 8 or (i >= 20 and i % 2 == 0) else "Personal"
            if kw.get("oddgroups") and i in (22, 25): g = None
            budget.append((n, g, None if rnd.random() < 0.1 else round(rnd.uniform(10, 900), 2)))
        if kw.get("gaps"): budget[5] = (None, None, None); budget[13] = (None, "Personal", 50)
        n_inc, n_exp = kw.get("n_inc", 300), kw.get("n_exp", 500)
        def rdate(): return dt.date(year, 1, 1) + dt.timedelta(days=rnd.randint(-40, 400))
        income = [(rdate() if rnd.random() > 0.02 else None, f"Client {rnd.randint(1, 30)}", "Work", round(rnd.uniform(50, 4000) * kw.get("scale", 1), 2) if rnd.random() > 0.02 else None) for _ in range(n_inc)]
        pool = [b[0] for b in budget if b[0]] + (["Mystery", None] if kw.get("uncat") else [])
        expenses = [(rdate() if rnd.random() > 0.02 else None, "Thing", rnd.choice(pool), round(rnd.uniform(-20, 400), 2) if rnd.random() > 0.03 else None) for _ in range(n_exp)]
        data = dict(settings=dict(name=kw.get("name", "Stress Test Studio"), currency="EUR", year=year, tax=kw.get("tax", 0.3), pay=kw.get("pay", 2500), buffer=kw.get("buffer", 1000),
                                  goal=kw.get("goal", 4.5), taxpot=kw.get("taxpot", 750.5), cushion=kw.get("cushion", 0.15), month=kw.get("month")),
                    income=income, expenses=expenses, budget=budget,
                    override={m: round(rnd.uniform(0, 6000), 2) for m in kw.get("ov", ())}, taxpaid={m: round(rnd.uniform(100, 9000), 2) for m in kw.get("tp", ())})
        p = os.path.join(work, f"stress_{tag}.xlsx"); ib.build(p, data=data); files.append(p)
    variant("full_this_year", 1, ty, uncat=True, ov=(2, 6), tp=(4, 9), gaps=True, oddgroups=True)
    variant("last_year", 2, ty - 1, month=3, ov=(12,), tp=(1, 12), uncat=True)
    variant("next_year", 3, ty + 1, month=7)
    variant("lean_buffer_runs_dry", 4, ty, scale=0.03, pay=3000, buffer=0, taxpot=None, tp=(2, 3))
    variant("no_pay_set", 5, ty, pay=None, tax=None, buffer=None, cushion=None, goal=None, name=None)
    variant("tiny", 6, ty, n_inc=3, n_exp=4, month=1)
    variant("rich", 7, ty, scale=4, pay=1200, goal=1, month=12)
    out = os.path.join(work, "recalc"); os.makedirs(out, exist_ok=True)
    subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", out] + files, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    total = 0
    for p in files:
        total += check(p, os.path.join(out, os.path.basename(p)), quiet=True)
    print("FAILURES", total)
    return total

if __name__ == "__main__":
    if sys.argv[1] == "--stress": sys.exit(1 if stress(sys.argv[2]) else 0)
    sys.exit(1 if check(sys.argv[1], sys.argv[2]) else 0)
