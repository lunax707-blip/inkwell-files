# Irregular Income Budget for Freelancers workbook (rotation A).
# Usage: python3 income_budget.py out.xlsx [empty]      (PREVIEW=1 adds tight print areas for rendering tabs)
# Or import and call build(out, empty=False, data=None) with a data dict (used by the verify script for stress files).
# Tabs: Start Here, Dashboard, Pay Plan, Income, Expenses, Budget, Settings.
# Only functions that exist in both Excel and Google Sheets are used.
import sys, os, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L

NAVY, CREAM, CORAL, MUST, TEAL, SAGE = "2B3A67", "F4E9D8", "D9583B", "E8A33D", "1F6F78", "9DB5A0"
INPUT, CALC, WHITE, LINE, INK, GREY = "FBF5EA", "EEF0F4", "FFFFFF", "D9D3C7", "1E2745", "6B7088"
HEAD, BODY = "Georgia", "Arial"
I0, I1 = 6, 305          # income rows
E0, E1 = 6, 505          # expense rows
B0, B1 = 6, 35           # budget category rows
P0 = 6                   # pay plan: January row (rows 6 to 17, total on 18)
MONEY, DATE = '#,##0.00', 'd mmm yyyy'
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
D = dt.date

def fill(c): return PatternFill("solid", start_color=c, end_color=c)
def font(size=10, bold=False, color=INK, name=BODY, italic=False): return Font(name=name, size=size, bold=bold, color=color, italic=italic)
thin = Side(style="thin", color=LINE)
box = Border(left=thin, right=thin, top=thin, bottom=thin)
bottom = Border(bottom=thin)

# ------------------------------------------------------------------ sample data
BUSINESS = [("Software and subscriptions", 85), ("Coworking or office", 120), ("Payment and bank fees", 110), ("Equipment", 40),
            ("Professional fees", 30), ("Marketing and website", 20), ("Training and books", 20), ("Travel for work", 15)]
PERSONAL = [("Rent or mortgage", 850), ("Groceries", 320), ("Utilities", 110), ("Transport", 90), ("Phone and internet", 60), ("Health", 50),
            ("Eating out", 110), ("Subscriptions", 35), ("Clothing", 50), ("Fun and hobbies", 80), ("Savings", 150), ("Gifts and giving", 40)]

def sample():
    inc = [
        (D(2026, 1, 5), "Lumen Labs", "Retainer, January", 1800), (D(2026, 1, 22), "Harbor and Pine Studio", "Brand refresh, deposit", 2400),
        (D(2026, 2, 9), "Lumen Labs", "Retainer, February", 1800), (D(2026, 2, 24), "Fieldnote Magazine", "Feature article", 720),
        (D(2026, 3, 6), "Lumen Labs", "Retainer, March", 1800), (D(2026, 3, 27), "Kite Analytics", "Quarterly report design", 1350),
        (D(2026, 4, 7), "Lumen Labs", "Retainer, April", 1800), (D(2026, 4, 14), "Marigold Events", "Spring invitation suite", 1100),
        (D(2026, 4, 29), "Harbor and Pine Studio", "Brand refresh, final payment", 3200),
        (D(2026, 5, 8), "Lumen Labs", "Retainer, May", 1800), (D(2026, 5, 21), "Saffron Kitchen", "Menu redesign", 640),
        (D(2026, 6, 5), "Lumen Labs", "Retainer, June", 1800), (D(2026, 6, 23), "Template shop", "Sales payout", 380),
        (D(2026, 7, 9), "Kite Analytics", "Sales deck", 1500), (D(2026, 7, 20), "Tidewater Architects", "Website rebuild, deposit", 2800),
        (D(2026, 7, 28), "Lumen Labs", "Retainer, July, plus extra hours", 2100),
        (D(2026, 8, 18), "Atlas Coffee Roasters", "Bag label design", 950), (D(2026, 8, 27), "Template shop", "Sales payout", 500),
        (D(2026, 9, 4), "Marigold Events", "Autumn festival signage", 1450), (D(2026, 9, 15), "Lumen Labs", "Retainer, August and September", 3600),
        (D(2026, 9, 29), "Fieldnote Magazine", "Short column", 450),
        (D(2026, 10, 12), "Tidewater Architects", "Website rebuild, part payment", 1400), (D(2026, 10, 26), "Saffron Kitchen", "Social media templates", 700),
        (D(2026, 11, 3), "Lumen Labs", "Retainer, October", 1800), (D(2026, 11, 17), "Kite Analytics", "Year end report design", 1650),
        (D(2026, 11, 24), "Template shop", "Sales payout", 150),
    ]
    by_month = {}
    for d, _, _, a in inc: by_month[d.month] = by_month.get(d.month, 0) + a
    exp = []
    extra = {  # month: [(day, description, category, amount)]
        1: [(19, "New year sale jacket", "Clothing", 78)], 2: [(11, "Portfolio hosting, yearly", "Marketing and website", 96), (14, "Birthday gift", "Gifts and giving", 45)],
        3: [(12, "Monitor arm", "Equipment", 85), (21, "Dentist", "Health", 90)], 4: [(16, "Accountant, yearly return", "Professional fees", 300), (25, "Concert tickets", "Fun and hobbies", 70)],
        5: [(9, "Running shoes", "Clothing", 95), (18, "Pottery class", "Fun and hobbies", 60)], 6: [(10, "Online course", "Training and books", 120), (27, "Pharmacy", "Health", 28)],
        7: [(13, "Weekend trip", "Fun and hobbies", 210), (22, "Wedding gift", "Gifts and giving", 80)], 8: [(6, "Laptop repair", "Equipment", 240), (20, "Eye test", "Health", 40)],
        9: [(8, "Train to client workshop", "Travel for work", 64), (19, "Autumn coat", "Clothing", 120)], 10: [(15, "Design book", "Training and books", 38), (23, "Museum pass", "Fun and hobbies", 45)],
        11: [(12, "Stock photo pack", "Marketing and website", 29), (20, "Pharmacy", "Health", 22)],
    }
    for m in range(1, 12):
        v = (m * 7) % 5                                   # small steady variation, 0 to 4
        rows = [
            (1, "Rent", "Rent or mortgage", 850), (1, "Coworking desk", "Coworking or office", 120), (2, "Transfer to savings", "Savings", 150),
            (3, "Design software plan", "Software and subscriptions", 62), (3, "Cloud storage and domain", "Software and subscriptions", 18),
            (4, "Phone and home internet", "Phone and internet", 60), (5, "Groceries", "Groceries", 148 + v * 6), (7, "Bus pass and fuel", "Transport", 78 + v * 4),
            (9, "Electricity and water", "Utilities", 96 + ((m * 5) % 7) * 4), (10, "Streaming and music", "Subscriptions", 35),
            (13, "Dinner out", "Eating out", 46 + v * 5), (17, "Groceries", "Groceries", 139 + ((m * 3) % 5) * 7),
            (23, "Payment processor fees", "Payment and bank fees", round(by_month[m] * 0.029, 2)), (24, "Lunch and coffee", "Eating out", 38 + ((m * 2) % 5) * 6),
        ]
        rows += extra.get(m, [])
        for day, desc, cat, amt in sorted(rows):
            if D(2026, m, day) <= D(2026, 11, 24): exp.append((D(2026, m, day), desc, cat, amt))
    return dict(
        settings=dict(name="Your Name Studio", currency="USD", year=2026, tax=0.25, pay=2000, buffer=2400, goal=3, taxpot=0, cushion=0.1, month=None),
        income=inc, expenses=exp,
        budget=[(n, "Business", a) for n, a in BUSINESS] + [(n, "Personal", a) for n, a in PERSONAL],
        override={}, taxpaid={4: 2000, 7: 2500, 10: 2400},
    )

def blank():
    return dict(settings=dict(name="", currency="USD", year=2026, tax=None, pay=None, buffer=None, goal=3, taxpot=None, cushion=0.1, month=None),
                income=[], expenses=[], budget=[(n, "Business", None) for n, _ in BUSINESS] + [(n, "Personal", None) for n, _ in PERSONAL], override={}, taxpaid={})

# ------------------------------------------------------------------ workbook
def build(out, empty=False, data=None):
    data = data or (blank() if empty else sample())
    S = data["settings"]
    wb = Workbook()
    wb.properties.title = "Irregular Income Budget for Freelancers"; wb.properties.creator = "Inkwell and Co"
    st = wb.active; st.title = "Start Here"
    db = wb.create_sheet("Dashboard"); pp = wb.create_sheet("Pay Plan"); inc = wb.create_sheet("Income")
    ex = wb.create_sheet("Expenses"); bu = wb.create_sheet("Budget"); se = wb.create_sheet("Settings")
    for ws, col in ((st, NAVY), (db, CORAL), (pp, TEAL), (inc, MUST), (ex, MUST), (bu, SAGE), (se, "8A8FA3")):
        ws.sheet_view.showGridLines = False; ws.sheet_properties.tabColor = col

    def banner(ws, title, sub, last_col, col=2):
        for r in (1, 2, 3):
            for c in range(1, last_col + 1): ws.cell(r, c).fill = fill(NAVY)
        ws.row_dimensions[1].height = 10; ws.row_dimensions[2].height = 34; ws.row_dimensions[3].height = 20
        t = ws.cell(2, col, title); t.font = font(22, False, CREAM, HEAD); t.alignment = Alignment(vertical="center", indent=1 if col == 1 else 0)
        s = ws.cell(3, col, sub); s.font = font(10, False, MUST); s.alignment = Alignment(vertical="top", indent=1 if col == 1 else 0)
    def key(ws, text, col=1):
        k = ws.cell(4, col, text); k.font = font(9, color=GREY, italic=True); k.alignment = Alignment(vertical="center")
    def heads(ws, labels, calc=(), row=5, h=32):
        for i, lab in enumerate(labels, start=1):
            c = ws.cell(row, i, lab); c.fill = fill(NAVY if i in calc else TEAL); c.font = font(10, True, WHITE)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = box
        ws.row_dimensions[row].height = h
    def inp(ws, r, c, v=None, fmt=None, align=None):
        x = ws.cell(r, c, v); x.fill = fill(INPUT); x.border = box; x.font = font(10)
        if fmt: x.number_format = fmt
        if align: x.alignment = Alignment(horizontal=align)
        return x
    def calc(ws, r, c, v, fmt=MONEY, align="right", bold=False):
        x = ws.cell(r, c, v); x.fill = fill(CALC); x.border = box; x.font = font(10, bold); x.number_format = fmt; x.alignment = Alignment(horizontal=align)
        return x

    # ---------------------------------------------------------------- Settings
    for c, w in zip("ABCD", (3, 38, 26, 78)): se.column_dimensions[c].width = w
    banner(se, "Settings", "Fill this in once. Every other tab reads from here.", 4)
    rows = [
        (5, "Business name", S["name"], None, "Shown on the dashboard."),
        (6, "Currency label", S["currency"], None, "Text only, for example USD, EUR, GBP, SAR."),
        (7, "Year", S["year"], "0", "The year this file tracks. Save a fresh copy each January and change this."),
        (8, "Tax set aside rate", S["tax"], "0%", "Share of every payment you move to your tax pot. Ask your accountant for your rate."),
        (9, "Monthly pay to yourself", S["pay"], MONEY, "The steady amount you move to your personal account each month, whatever the month earned."),
        (10, "Buffer balance at the start of the year", S["buffer"], MONEY, "Money already sitting in your business account or buffer savings on 1 January."),
        (11, "Buffer goal (months of pay)", S["goal"], "0.0", "How many months of pay you want in reserve. Three is a common first goal."),
        (12, "Tax pot balance at the start of the year", S["taxpot"], MONEY, "Money already set aside for tax on 1 January. Leave empty if none."),
        (13, "Safety cushion", S["cushion"], "0%", "Taken off your average month when the dashboard works out the pay you can afford."),
        (14, "Month to show on the dashboard", S["month"], "0", "A number from 1 to 12. Leave empty to follow the current month."),
    ]
    se.cell(4, 2, "YOUR NUMBERS").font = font(9, True, TEAL)
    for r, lab, val, fmt, note in rows:
        a = se.cell(r, 2, lab); a.font = font(10, True); a.alignment = Alignment(vertical="center")
        b = inp(se, r, 3, val, fmt); b.alignment = Alignment(horizontal="left", vertical="center")
        n = se.cell(r, 4, note); n.font = font(9, color=GREY, italic=True); n.alignment = Alignment(vertical="center", indent=1)
        se.row_dimensions[r].height = 22
    dvm = DataValidation(type="whole", operator="between", formula1="1", formula2="12", allow_blank=True, showErrorMessage=True, error="Type a month number from 1 to 12, or leave empty.")
    se.add_data_validation(dvm); dvm.add("C14")
    se.cell(16, 2, "WORKED OUT FOR YOU (PLEASE LEAVE)").font = font(9, True, TEAL)
    helpers = [
        (17, "Months counted so far", "=MAX(0,MIN(12,(YEAR(TODAY())-$C$7)*12+MONTH(TODAY())))", "Months of the year that have started. The pay plan fills in one month at a time."),
        (18, "Full months finished", "=MAX(0,MIN(12,(YEAR(TODAY())-$C$7)*12+MONTH(TODAY())-1))", "Averages on the dashboard use finished months only, so a half month does not drag them down."),
        (19, "Dashboard month in use", "=IF($C$14=\"\",IF($C$17=0,1,$C$17),$C$14)", "The month the budget figures are showing."),
    ]
    for r, lab, f, note in helpers:
        a = se.cell(r, 2, lab); a.font = font(10, True); a.alignment = Alignment(vertical="center")
        b = calc(se, r, 3, f, "0", "left"); b.alignment = Alignment(horizontal="left", vertical="center")
        n = se.cell(r, 4, note); n.font = font(9, color=GREY, italic=True); n.alignment = Alignment(vertical="center", indent=1)
        se.row_dimensions[r].height = 22
    NAME, CUR, YEAR, TAX, PAY, BUF0, GOAL, POT0, CUSH = ["Settings!$C$%d" % r for r in range(5, 14)]
    NM, NC, SM = "Settings!$C$17", "Settings!$C$18", "Settings!$C$19"

    # ---------------------------------------------------------------- Income
    banner(inc, "Income", "One row for every payment that lands in your account. Use the date the money arrived.", 5, 1)
    for i, w in enumerate((14, 30, 38, 15, 40), start=1): inc.column_dimensions[L(i)].width = w
    key(inc, "Type in the cream cells. Amounts are what you actually received, before tax.")
    heads(inc, ["Date received", "Client or source", "What it was for", "Amount", "Notes"])
    inc["D5"] = '="Amount ("&%s&")"' % CUR
    for r in range(I0, I1 + 1):
        inp(inc, r, 1, fmt=DATE, align="center"); inp(inc, r, 2); inp(inc, r, 3); inp(inc, r, 4, fmt=MONEY); inp(inc, r, 5)
    for i, row in enumerate(data["income"]):
        for j, v in enumerate(row):
            if v is not None: inc.cell(I0 + i, j + 1, v)
    inc.freeze_panes = "A6"; inc.auto_filter.ref = f"A5:E{I1}"
    ID, IA = f"Income!$A${I0}:$A${I1}", f"Income!$D${I0}:$D${I1}"

    # ---------------------------------------------------------------- Budget (inputs first, formulas after Expenses ranges exist)
    XD, XC, XA, XG = [f"Expenses!${c}${E0}:${c}${E1}" for c in "ACDE"]
    BA, BG, BB, BS, BK = [f"Budget!${c}${B0}:${c}${B1}" for c in "ABCDJ"]
    banner(bu, "Budget", None, 9, 1)
    bu["A3"] = '="Your spending categories and a monthly amount for each. Showing "&INDEX(\'Pay Plan\'!$A$%d:$A$%d,%s)&" "&%s&". Amounts in "&%s&"."' % (P0, P0 + 11, SM, YEAR, CUR)
    for i, w in enumerate((30, 13, 16, 16, 16, 11, 16, 18, 17, 3), start=1): bu.column_dimensions[L(i)].width = w
    bu.column_dimensions["J"].hidden = True
    key(bu, "Cream cells are yours: rename, add or remove categories and mark each one Business or Personal. Grey cells are calculated. Use each category name once.")
    heads(bu, ["Category", "Group", "Monthly budget", "Spent this month", "Left this month", "Used", "Spent this year", "Budget so far this year", "Ahead or behind"], calc=(4, 5, 6, 7, 8, 9))
    lo, hi = f'">="&DATE({YEAR},{SM},1)', f'"<"&DATE({YEAR},{SM}+1,1)'
    y0, y1 = f'">="&DATE({YEAR},1,1)', f'"<"&DATE({YEAR}+1,1,1)'
    for r in range(B0, B1 + 1):
        inp(bu, r, 1); inp(bu, r, 2, align="center"); inp(bu, r, 3, fmt=MONEY)
        calc(bu, r, 4, f'=IF($A{r}="","",SUMIFS({XA},{XC},$A{r},{XD},{lo},{XD},{hi}))')
        calc(bu, r, 5, f'=IF($A{r}="","",C{r}-D{r})')
        calc(bu, r, 6, f'=IF($A{r}="","",IF(C{r}=0,"",D{r}/C{r}))', "0%", "center")
        calc(bu, r, 7, f'=IF($A{r}="","",SUMIFS({XA},{XC},$A{r},{XD},{y0},{XD},{y1}))')
        calc(bu, r, 8, f'=IF($A{r}="","",C{r}*{NM})')
        calc(bu, r, 9, f'=IF($A{r}="","",H{r}-G{r})')
        bu.cell(r, 10, f'=IF($A{r}="","",IF(D{r}=0,"",D{r}+ROW()/1000000))')
    for i, (n, g, a) in enumerate(data["budget"]):
        bu.cell(B0 + i, 1, n); bu.cell(B0 + i, 2, g)
        if a is not None: bu.cell(B0 + i, 3, a)
    dvg = DataValidation(type="list", formula1='"Business,Personal"', allow_blank=True, showErrorMessage=True, error="Pick Business or Personal.")
    bu.add_data_validation(dvg); dvg.add(f"B{B0}:B{B1}")
    red = Font(name=BODY, size=10, bold=True, color="A3311A")
    bu.conditional_formatting.add(f"E{B0}:E{B1}", CellIsRule(operator="lessThan", formula=["0"], font=red, fill=fill("F6D5CC")))
    bu.conditional_formatting.add(f"I{B0}:I{B1}", CellIsRule(operator="lessThan", formula=["0"], font=red))
    BT = B1 + 1
    t = bu.cell(BT, 1, "All categories"); t.font = font(10, True, WHITE); t.fill = fill(NAVY); t.border = box; t.alignment = Alignment(horizontal="left", indent=1)
    for c in range(2, 10):
        x = bu.cell(BT, c); x.fill = fill(CREAM); x.border = box; x.font = font(10, True); x.number_format = MONEY; x.alignment = Alignment(horizontal="right")
        if c in (4, 5, 7, 8, 9): x.value = f"=SUM({L(c)}{B0}:{L(c)}{B1})"
        if c == 3: x.value = f'=SUMIFS(C{B0}:C{B1},A{B0}:A{B1},"<>")'
    bu.row_dimensions[BT].height = 22
    bu.freeze_panes = "B6"

    # ---------------------------------------------------------------- Expenses
    banner(ex, "Expenses", "One row for everything you spend, business and personal. Pick the category from the list.", 6, 1)
    for i, w in enumerate((14, 36, 28, 15, 14, 36), start=1): ex.column_dimensions[L(i)].width = w
    key(ex, "Type in the cream cells. The Group column fills itself from the Budget tab. Add new categories on the Budget tab first.")
    heads(ex, ["Date", "What it was", "Category", "Amount", "Group", "Notes"], calc=(5,))
    ex["D5"] = '="Amount ("&%s&")"' % CUR
    for r in range(E0, E1 + 1):
        inp(ex, r, 1, fmt=DATE, align="center"); inp(ex, r, 2); inp(ex, r, 3); inp(ex, r, 4, fmt=MONEY); inp(ex, r, 6)
        calc(ex, r, 5, f'=IF(C{r}="","",IFERROR(INDEX({BG},MATCH(C{r},{BA},0))&"","Not in budget"))', "@", "center")
    for i, row in enumerate(data["expenses"]):
        for j, v in zip((1, 2, 3, 4), row):
            if v is not None: ex.cell(E0 + i, j, v)
    dvc = DataValidation(type="list", formula1=f"={BA}", allow_blank=True, showErrorMessage=False)
    ex.add_data_validation(dvc); dvc.add(f"C{E0}:C{E1}")
    ex.conditional_formatting.add(f"E{E0}:E{E1}", CellIsRule(operator="equal", formula=['"Not in budget"'], font=red, fill=fill("F6D5CC")))
    ex.freeze_panes = "A6"; ex.auto_filter.ref = f"A5:F{E1}"

    # ---------------------------------------------------------------- Pay Plan
    banner(pp, "Pay Plan", None, 13, 1)
    pp["A3"] = '="Uneven income in, steady pay out. Your buffer absorbs the difference. Year "&%s&", amounts in "&%s&"."' % (YEAR, CUR)
    for i, w in enumerate((10, 15, 15, 15, 16, 15, 15, 15, 15, 15, 15, 15, 16, 3, 3), start=1): pp.column_dimensions[L(i)].width = w
    pp.column_dimensions["N"].hidden = True; pp.column_dimensions["O"].hidden = True
    key(pp, "Only two cream columns to type in here, both optional. Everything else comes from the Income, Expenses and Settings tabs.")
    heads(pp, ["Month", "Income received", "Tax set aside", "Business costs", "Left after tax and costs", "Pay override (optional)", "Paid to you", "Buffer balance",
               "Tax paid from pot", "Tax pot balance", "Personal spending", "Left from your pay", "What happened"], calc=(2, 3, 4, 5, 7, 8, 10, 11, 12, 13), h=36)
    for c in (6, 9): pp.cell(5, c).fill = fill(TEAL)
    for m in range(1, 13):
        r = P0 + m - 1
        mlo, mhi = f'">="&DATE({YEAR},{m},1)', f'"<"&DATE({YEAR},{m + 1},1)'
        pb = BUF0 if m == 1 else f"H{r - 1}"; pt = POT0 if m == 1 else f"J{r - 1}"
        a = pp.cell(r, 1, MONTHS[m - 1]); a.font = font(10, True); a.border = box; a.alignment = Alignment(horizontal="left", indent=1); a.fill = fill(CALC)
        calc(pp, r, 2, f"=SUMIFS({IA},{ID},{mlo},{ID},{mhi})")
        calc(pp, r, 3, f"=B{r}*{TAX}")
        calc(pp, r, 4, f'=SUMIFS({XA},{XD},{mlo},{XD},{mhi},{XG},"Business")')
        calc(pp, r, 5, f"=B{r}-C{r}-D{r}")
        inp(pp, r, 6, data["override"].get(m), MONEY)
        calc(pp, r, 7, f'=IF({m}>{NM},"",IF(F{r}<>"",F{r},MAX(0,MIN({PAY}+0,{pb}+E{r}))))', bold=True)
        calc(pp, r, 8, f'=IF({m}>{NM},"",{pb}+E{r}-G{r})', bold=True)
        inp(pp, r, 9, data["taxpaid"].get(m), MONEY)
        calc(pp, r, 10, f'=IF({m}>{NM},"",{pt}+C{r}-I{r})')
        calc(pp, r, 11, f'=SUMIFS({XA},{XD},{mlo},{XD},{mhi},{XG},"Personal")')
        calc(pp, r, 12, f'=IF({m}>{NM},"",G{r}-K{r})')
        calc(pp, r, 13, f'=IF({m}>{NM},"",IF(H{r}<0,"Buffer empty",IF(G{r}<{PAY},"Short pay",IF(E{r}>=G{r},"Buffer grew","Buffer used"))))', "@", "center")
        pp.cell(r, 14, f'=IF({m}>{NC},"",E{r})'); pp.cell(r, 15, f'=IF({m}>{NC},"",B{r})')
        pp.row_dimensions[r].height = 20
    T = P0 + 12
    t = pp.cell(T, 1, "Year"); t.font = font(10, True, WHITE); t.fill = fill(NAVY); t.border = box; t.alignment = Alignment(horizontal="left", indent=1)
    for c in range(2, 14):
        x = pp.cell(T, c); x.fill = fill(CREAM); x.border = box; x.font = font(10, True); x.number_format = MONEY; x.alignment = Alignment(horizontal="right")
        if c in (2, 3, 4, 5, 7, 9, 11, 12): x.value = f"=SUM({L(c)}{P0}:{L(c)}{T - 1})"
    pp.row_dimensions[T].height = 22
    PR = lambda c: f"'Pay Plan'!${c}${P0}:${c}${P0 + 11}"
    rngM = f"M{P0}:M{P0 + 11}"
    def status_rule(word, bg, fg):
        pp.conditional_formatting.add(rngM, CellIsRule(operator="equal", formula=[f'"{word}"'], fill=fill(bg), font=Font(name=BODY, size=10, bold=True, color=fg)))
    status_rule("Buffer grew", "DCE7DE", "2F5D46"); status_rule("Buffer used", "FAE7C6", "8A5A0B"); status_rule("Short pay", "F6D5CC", "A3311A"); status_rule("Buffer empty", "F6D5CC", "A3311A")
    for col in "HJL":
        pp.conditional_formatting.add(f"{col}{P0}:{col}{P0 + 11}", CellIsRule(operator="lessThan", formula=["0"], font=red))
    notes = [
        ("How to read a row", ""),
        ("Income received", "Everything on the Income tab dated in that month."),
        ("Tax set aside", "Income times your tax rate. Move this amount to a separate tax account as soon as a payment lands."),
        ("Left after tax and costs", "What the month really earned for you, once tax and business costs are out."),
        ("Paid to you", "Your steady monthly pay from Settings. If the buffer cannot cover it, you get what is there. Type a number in Pay override to record a different amount for one month."),
        ("Buffer balance", "Last month's buffer, plus what this month earned, minus what you paid yourself. Big months fill it, lean months draw on it."),
        ("Tax pot balance", "Tax set aside so far, minus any tax bills you typed in Tax paid from pot."),
        ("Left from your pay", "Your pay minus your personal spending for the month. Months that have not started yet stay empty."),
    ]
    r = T + 2
    for i, (a, b) in enumerate(notes):
        x = pp.cell(r, 1, a); x.font = font(13, False, NAVY, HEAD) if i == 0 else font(10, True)
        if i == 0:
            for c in range(1, 14): pp.cell(r, c).border = Border(bottom=Side(style="medium", color=NAVY))
            pp.row_dimensions[r].height = 24
        else:
            y = pp.cell(r, 3, b); y.font = font(10)
            pp.row_dimensions[r].height = 18
        r += 1
    pp.freeze_panes = "B6"

    # ---------------------------------------------------------------- Dashboard
    db.column_dimensions["A"].width = 3
    for c in range(2, 14): db.column_dimensions[L(c)].width = 13.5
    db.column_dimensions["N"].width = 3
    banner(db, "Irregular Income Dashboard", None, 14)
    MN = f"INDEX({PR('A')},{SM})"
    db["B3"] = f'=IF({NAME}="","",{NAME}&"   |   ")&"Year "&{YEAR}&"   |   Amounts in "&{CUR}&"   |   Budget month: "&{MN}'

    def card(r, c, label, formula, sub, fmt=MONEY, accent=NAVY):
        for k in range(3): db.merge_cells(start_row=r + k, start_column=c, end_row=r + k, end_column=c + 2)
        for rr in range(r, r + 3):
            for cc in range(c, c + 3):
                x = db.cell(rr, cc); x.fill = fill(CREAM); x.border = Border(left=Side(style="thick", color=accent) if cc == c else None)
        a = db.cell(r, c, label); a.font = font(9, True, GREY); a.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        v = db.cell(r + 1, c, formula); v.font = font(20, False, accent, HEAD); v.number_format = fmt; v.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        s = db.cell(r + 2, c, sub); s.font = font(9, color=GREY); s.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        db.row_dimensions[r].height = 20; db.row_dimensions[r + 1].height = 32; db.row_dimensions[r + 2].height = 20

    Q = '"#,##0"'
    buf_now = f"IF({NM}=0,{BUF0},INDEX({PR('H')},{NM}))"
    pot_now = f"IF({NM}=0,{POT0},INDEX({PR('J')},{NM}))"
    afford = f"IF({NC}=0,0,MAX(0,IFERROR(AVERAGE({PR('N')}),0)*(1-{CUSH})))"
    pay_sel = f"IFERROR(INDEX({PR('G')},{SM})+0,0)"
    per_sel = f"INDEX({PR('K')},{SM})"
    card(5, 2, "INCOME THIS YEAR", f"=SUM({PR('B')})", f'="Payments logged: "&COUNTIFS({ID},{y0},{ID},{y1},{IA},"<>")', accent=NAVY)
    card(5, 5, "PAID TO YOU THIS YEAR", f"=SUM({PR('G')})", f'="Steady pay of "&TEXT({PAY},{Q})&" a month"', accent=TEAL)
    card(5, 8, "BUFFER NOW", f"={buf_now}", f'="Goal "&TEXT({GOAL}*{PAY},{Q})&" ("&TEXT({GOAL},"0.0")&" months of pay)"', accent=MUST)
    card(5, 11, "TAX POT NOW", f"={pot_now}", f'=TEXT({TAX},"0%")&" of income set aside, less tax paid"', accent=CORAL)
    db.row_dimensions[8].height = 8
    card(9, 2, "MONTHS OF PAY IN THE BUFFER", f"=IF({PAY}>0,H6/{PAY},0)", '="How long you could pay yourself with no income"', fmt="0.0", accent=NAVY)
    card(9, 5, "PAY YOU CAN AFFORD", f"={afford}", f'="Average finished month, less "&TEXT({CUSH},"0%")&" cushion"', accent=TEAL)
    card(9, 8, "LEANEST MONTH SO FAR", f"=IF({NC}=0,0,MIN({PR('O')}))", f'=IF({NC}=0,"Needs one finished month","Best "&TEXT(MAX({PR("O")}),{Q})&", average "&TEXT(AVERAGE({PR("O")}),{Q}))', accent=MUST)
    card(9, 11, "LEFT FROM YOUR PAY", f"={pay_sel}-{per_sel}", f'="Pay minus personal spending, "&{MN}', accent=CORAL)
    db.row_dimensions[12].height = 10

    def section(r, c, text, span):
        x = db.cell(r, c, text); x.font = font(13, False, NAVY, HEAD)
        for cc in range(c, c + span): db.cell(r, cc).border = Border(bottom=Side(style="medium", color=NAVY))
        db.row_dimensions[r].height = 24
    def thead(r, c, labels, spans=None):
        cc = c
        for i, lab in enumerate(labels):
            sp = spans[i] if spans else 1
            if sp > 1: db.merge_cells(start_row=r, start_column=cc, end_row=r, end_column=cc + sp - 1)
            x = db.cell(r, cc, lab); x.font = font(9, True, WHITE); x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            for k2 in range(cc, cc + sp): db.cell(r, k2).fill = fill(TEAL)
            cc += sp
        db.row_dimensions[r].height = 26
    def tcell(r, c, v, fmt=None, span=1, align="right", bold=False, color=INK, bg=None):
        if span > 1: db.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + span - 1)
        x = db.cell(r, c, v); x.font = font(10, bold, color); x.alignment = Alignment(horizontal=align, vertical="center", indent=1 if align == "left" else 0)
        if fmt: x.number_format = fmt
        for k2 in range(c, c + span):
            db.cell(r, k2).border = bottom
            if bg: db.cell(r, k2).fill = fill(bg)
        return x

    section(13, 2, "Month by month", 6); section(13, 9, "Income against your steady pay", 5)
    thead(14, 2, ["Month", "Income", "Tax set aside", "Business costs", "Paid to you", "Buffer"])
    for m in range(1, 13):
        r = 14 + m; pr = P0 + m - 1
        tcell(r, 2, MONTHS[m - 1], align="left", bold=True)
        for c, col in zip((3, 4, 5, 6, 7), "BCDGH"):
            tcell(r, c, f"='Pay Plan'!{col}{pr}", MONEY, bold=(c == 7))
    tcell(27, 2, "Year", align="left", bold=True, bg=CREAM)
    for c in (3, 4, 5, 6): tcell(27, c, f"=SUM({L(c)}15:{L(c)}26)", MONEY, bold=True, bg=CREAM)
    tcell(27, 7, "=H6", MONEY, bold=True, bg=CREAM)
    db.conditional_formatting.add("G15:G27", CellIsRule(operator="lessThan", formula=["0"], font=red))
    ch = BarChart(); ch.type = "col"; ch.grouping = "clustered"; ch.overlap = -10; ch.gapWidth = 60
    ch.add_data(Reference(db, min_col=3, min_row=14, max_row=26), titles_from_data=True)
    ch.add_data(Reference(db, min_col=6, min_row=14, max_row=26), titles_from_data=True)
    ch.set_categories(Reference(db, min_col=2, min_row=15, max_row=26))
    ch.series[0].graphicalProperties.solidFill = NAVY; ch.series[0].graphicalProperties.line.solidFill = NAVY
    ch.series[1].graphicalProperties.solidFill = MUST; ch.series[1].graphicalProperties.line.solidFill = MUST
    ch.legend.position = "b"; ch.height = 7.9; ch.width = 13.2
    ch.y_axis.number_format = '#,##0'; ch.y_axis.majorGridlines.spPr = None
    ch.x_axis.delete = False; ch.y_axis.delete = False
    db.add_chart(ch, "I14")

    db.row_dimensions[28].height = 10
    db["B29"] = f'="Budget for "&{MN}'; section(29, 2, None, 6); db["B29"].font = font(13, False, NAVY, HEAD)
    db["I29"] = f'="Where the money went in "&{MN}'; section(29, 9, None, 5); db["I29"].font = font(13, False, NAVY, HEAD)
    thead(30, 2, ["", "Budget", "Spent", "Left"], [3, 1, 1, 1])
    for i, g in enumerate(("Business", "Personal")):
        r = 31 + i
        tcell(r, 2, "Business costs" if i == 0 else "Personal spending", span=3, align="left", bold=True)
        tcell(r, 5, f'=SUMIFS({BB},{BG},"{g}",{BA},"<>")', MONEY); tcell(r, 6, f'=SUMIF({BG},"{g}",{BS})', MONEY); tcell(r, 7, f"=E{r}-F{r}", MONEY, bold=True)
    tcell(33, 2, "All spending", span=3, align="left", bold=True, bg=CREAM)
    for c in (5, 6, 7): tcell(33, c, f"=SUM({L(c)}31:{L(c)}32)", MONEY, bold=True, bg=CREAM)
    tcell(34, 2, "Paid to you this month", span=3, align="left"); tcell(34, 5, "", MONEY); tcell(34, 6, f"={pay_sel}", MONEY); tcell(34, 7, "", MONEY)
    tcell(35, 2, "Left from your pay", span=3, align="left"); tcell(35, 5, "", MONEY); tcell(35, 6, "=K10", MONEY, bold=True); tcell(35, 7, "", MONEY)
    db.conditional_formatting.add("G31:G33", CellIsRule(operator="lessThan", formula=["0"], font=red))
    db.conditional_formatting.add("F35", CellIsRule(operator="lessThan", formula=["0"], font=red))
    thead(30, 9, ["Category", "Group", "Spent", "Budget"], [2, 1, 1, 1])
    for n in range(1, 6):
        r = 30 + n
        mt = f"MATCH(LARGE({BK},{n}),{BK},0)"
        tcell(r, 9, f'=IFERROR(INDEX({BA},{mt}),"")', span=2, align="left", bold=True)
        tcell(r, 11, f'=IFERROR(INDEX({BG},{mt})&"","")', align="center")
        tcell(r, 12, f'=IFERROR(INDEX({BS},{mt}),"")', MONEY)
        tcell(r, 13, f'=IFERROR(INDEX({BB},{mt})+0,"")', MONEY)

    db.row_dimensions[36].height = 10
    section(37, 2, "Health check", 12)
    PB = f'SUMIFS({BB},{BG},"Personal",{BA},"<>")'
    uncat = f'(COUNT({XA})-COUNTIFS({XG},"Business",{XA},"<>")-COUNTIFS({XG},"Personal",{XA},"<>"))'
    lines = [
        f'=IF({PAY}<=0,"Buffer: type your monthly pay on the Settings tab to see how long your buffer lasts.","Buffer: "&TEXT(H6,{Q})&" covers "&TEXT(H6/{PAY},"0.0")&" months of pay. Your goal is "&TEXT({GOAL},"0.0")&" months ("&TEXT({GOAL}*{PAY},{Q})&"). "&IF(H6>={GOAL}*{PAY},"Goal reached.","Still to build: "&TEXT({GOAL}*{PAY}-H6,{Q})&"."))',
        f'=IF({PAY}<=0,"Pay: type your monthly pay on the Settings tab. Your income so far supports about "&TEXT(E10,{Q})&" a month.",IF({NC}=0,"Pay: once one full month is logged, this line tells you whether your pay matches your income.",IF({PAY}<=E10,"Pay: "&TEXT({PAY},{Q})&" a month is within what your income has supported so far ("&TEXT(E10,{Q})&").","Pay: "&TEXT({PAY},{Q})&" a month is more than your income has supported so far ("&TEXT(E10,{Q})&"). Lower it, or expect the buffer to shrink.")))',
        f'=IF({PAY}<=0,"Budget: your personal budget adds up to "&TEXT({PB},{Q})&" a month. Set your pay to see whether it fits.",IF({PB}<={PAY},"Budget: your personal budget of "&TEXT({PB},{Q})&" a month fits inside your pay.","Budget: your personal budget of "&TEXT({PB},{Q})&" a month is higher than your pay. Trim "&TEXT({PB}-{PAY},{Q})&" or raise your pay."))',
        f'=IF(K6<0,"Tax: your tax pot is below zero. Check the Tax paid from pot column on the Pay Plan tab.","Tax: your pot holds "&TEXT(K6,{Q})&". Keep it in a separate account so it is there when the bill comes.")',
        f'=IF({uncat}=0,"Log: every expense has a category from the Budget tab.","Log: expense rows with no category, or one that is not on the Budget tab: "&{uncat}&". They are left out of the totals until fixed.")',
    ]
    for i, f in enumerate(lines):
        r = 38 + i
        db.merge_cells(start_row=r, start_column=2, end_row=r, end_column=13)
        x = db.cell(r, 2, f); x.font = font(10); x.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        for c in range(2, 14): db.cell(r, c).border = bottom
        db.row_dimensions[r].height = 22
    n = db.cell(44, 2, "Nothing to type on this page. It updates when you edit the Income, Expenses, Budget, Pay Plan and Settings tabs."); n.font = font(9, color=GREY, italic=True)
    db.page_setup.orientation = "portrait"; db.page_setup.fitToWidth = 1; db.page_setup.fitToHeight = 1; db.sheet_properties.pageSetUpPr.fitToPage = True
    db.print_area = "A1:N44"

    # ---------------------------------------------------------------- Start Here
    st.column_dimensions["A"].width = 3; st.column_dimensions["B"].width = 5; st.column_dimensions["C"].width = 108; st.column_dimensions["D"].width = 3
    banner(st, "Irregular Income Budget for Freelancers", "Turn uneven client payments into steady monthly pay. Works in Google Sheets and Excel.", 4)
    R = [5]
    def h(text):
        r = R[0]; x = st.cell(r, 2, text); x.font = font(13, False, NAVY, HEAD); st.row_dimensions[r].height = 26
        for c in (2, 3): st.cell(r, c).border = Border(bottom=Side(style="medium", color=NAVY))
        R[0] += 1
    def step(n, text):
        r = R[0]; a = st.cell(r, 2, n); a.font = font(11, True, CORAL if isinstance(n, int) else TEAL); a.alignment = Alignment(horizontal="center", vertical="center")
        b = st.cell(r, 3, text); b.font = font(10); b.alignment = Alignment(wrap_text=True, vertical="center")
        st.row_dimensions[r].height = 14 * (-(-len(text) // 104)) + 10; R[0] += 1
    def gap():
        st.row_dimensions[R[0]].height = 8; R[0] += 1
    h("The idea in one minute")
    step(">", "Freelance income arrives in lumps. Bills do not. This file treats your business account as a buffer: every payment goes in, a share is set aside for tax, business costs come out, and you pay yourself the same amount every month. Big months fill the buffer. Lean months draw on it.")
    gap()
    h("Set up in ten minutes")
    step(1, "Settings tab: type your currency, the year, your tax set aside rate, the monthly pay you want, and what is in your buffer today. Not sure what pay to pick? Start low. The dashboard will tell you what your income can support.")
    step(2, "Budget tab: check the list of categories. Rename them, delete the ones you do not need, add your own, and mark each one Business or Personal. Type a monthly amount for each.")
    step(3, "Income tab: add a row each time a payment lands. Date, who paid, what for, how much.")
    step(4, "Expenses tab: add a row for what you spend and pick its category. Once a week is enough.")
    step(5, "Pay Plan tab: read across the month. It shows what came in, what to move to tax, what the month really earned, what you paid yourself and what is left in the buffer. Type a tax bill in Tax paid from pot when you pay one.")
    step(6, "Dashboard tab: nothing to type. It shows your year, the pay you can afford, how many months of pay your buffer holds, your budget for the month and a plain language health check.")
    gap()
    h("A simple monthly routine")
    step(">", "When a payment lands: log it on the Income tab, then move the Tax set aside share to a separate account.")
    step(">", "On the first of the month: pay yourself the amount in Paid to you. That is your personal money for the month.")
    step(">", "At the end of the month: check Left from your pay and the budget table. Adjust next month, not this one.")
    step(">", "Every three months: compare your pay with Pay you can afford on the dashboard and raise or lower it on the Settings tab.")
    gap()
    h("Clearing the sample data")
    step(1, "The first file arrives with a sample year so you can see how everything reads. A second, blank file is included if you would rather start clean.")
    step(2, "To clear the sample yourself: on the Income and Expenses tabs select the CREAM cells from row 6 down and press Delete. On the Pay Plan tab clear the two cream columns. Then put your own numbers on the Settings and Budget tabs.")
    step(3, "Leave the GREY cells alone. They hold the formulas. If you delete one by accident, copy the same cell from the row above and paste it back.")
    gap()
    h("Opening the file")
    step(">", "Google Sheets: upload the file to Google Drive, open it, then choose File, Save as Google Sheets.")
    step(">", "Excel: open the file directly (Excel 2010 or later, Windows or Mac). If you see Protected View, click Enable Editing.")
    step(">", "Dates: type them the way your computer normally writes dates. If a row is missing from the totals, its date was read as text, so retype it.")
    gap()
    h("Good to know")
    step(">", "The file holds 300 payments, 500 expenses and 30 categories for one year. The Pay Plan fills in a month once that month has started, using today's date.")
    step(">", "Averages use finished months only. Pay you can afford is your average finished month after tax and business costs, less the safety cushion from Settings.")
    step(">", "The tax figures are a savings reminder based on the rate you typed. This file is not tax or financial advice.")
    step(">", "For personal and single business use. Please do not share or resell the file. Made by Inkwell and Co.")
    st.sheet_view.zoomScale = 110

    for ws in (inc, ex, bu, pp, se, st):
        ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
    inc.print_title_rows = "5:5"; ex.print_title_rows = "5:5"
    if os.environ.get("PREVIEW"):
        inc.print_area = "A1:E32"; ex.print_area = "A1:F34"; bu.print_area = "A1:I26"; pp.print_area = "A1:M27"; se.print_area = "A1:D20"; st.print_area = f"A1:D{R[0]}"
        for ws in (inc, ex, bu, pp, se, st): ws.page_setup.fitToHeight = 1
    wb.active = 0
    wb.save(out)
    return out

if __name__ == "__main__":
    print("saved", build(sys.argv[1], empty=len(sys.argv) > 2 and sys.argv[2] == "empty"))
