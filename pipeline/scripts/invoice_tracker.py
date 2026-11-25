# Freelance Invoice Tracker workbook (rotation A). Usage: python3 invoice_tracker.py out.xlsx [empty]
# Tabs: Start Here, Dashboard, Invoices, Clients, Invoice (printable), Settings.
# Only functions that exist in both Excel and Google Sheets are used.
import sys, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.utils import get_column_letter as L

out = sys.argv[1]
EMPTY = len(sys.argv) > 2 and sys.argv[2] == "empty"

NAVY, CREAM, CORAL, MUST, TEAL, SAGE = "2B3A67", "F4E9D8", "D9583B", "E8A33D", "1F6F78", "9DB5A0"
INPUT, CALC, WHITE, LINE, INK = "FBF5EA", "EEF0F4", "FFFFFF", "D9D3C7", "1E2745"
HEAD, BODY = "Georgia", "Arial"
N0, N1 = 6, 305          # invoice rows
C0, C1 = 6, 55           # client rows
MONEY, DATE = '#,##0.00', 'd mmm yyyy'

def fill(c): return PatternFill("solid", start_color=c, end_color=c)
def font(size=10, bold=False, color=INK, name=BODY, italic=False): return Font(name=name, size=size, bold=bold, color=color, italic=italic)
thin = Side(style="thin", color=LINE)
box = Border(left=thin, right=thin, top=thin, bottom=thin)
bottom = Border(bottom=thin)

wb = Workbook()
wb.properties.title = "Freelance Invoice Tracker"
wb.properties.creator = "Inkwell and Co"
st = wb.active; st.title = "Start Here"
db = wb.create_sheet("Dashboard")
inv = wb.create_sheet("Invoices")
cl = wb.create_sheet("Clients")
pr = wb.create_sheet("Invoice")
se = wb.create_sheet("Settings")
for ws, col in ((st, NAVY), (db, CORAL), (inv, TEAL), (cl, MUST), (pr, SAGE), (se, "8A8FA3")):
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = col

def banner(ws, title, sub, last_col, col=2):
    for r in (1, 2, 3):
        for c in range(1, last_col + 1):
            ws.cell(r, c).fill = fill(NAVY)
    ws.row_dimensions[1].height = 10; ws.row_dimensions[2].height = 34; ws.row_dimensions[3].height = 20
    t = ws.cell(2, col, title); t.font = font(22, False, CREAM, HEAD); t.alignment = Alignment(vertical="center")
    s = ws.cell(3, col, sub); s.font = font(10, False, "E8A33D"); s.alignment = Alignment(vertical="top")

# ---------------------------------------------------------------- Settings
se.column_dimensions["A"].width = 3; se.column_dimensions["B"].width = 34; se.column_dimensions["C"].width = 44; se.column_dimensions["D"].width = 58
banner(se, "Settings", "Fill this in once. Every other tab reads from here.", 4)
rows = [
    (5, "Business name", "Your Name Studio", "Shown on the dashboard and on the printable invoice."),
    (6, "Currency label", "USD", "Text only, for example USD, EUR, GBP, SAR. Shown in column headings."),
    (7, "Year for the dashboard", 2026, "Change this each January. Old invoices stay in the log."),
    (8, "Default payment terms (days)", 30, "Used when the Terms cell of an invoice is left empty."),
    (9, "Tax set aside rate", 0.25, "Share of money received to put aside. Ask your accountant for your rate."),
    (10, "Due soon window (days)", 7, "An unpaid invoice shows Due soon this many days before its due date."),
    (12, "Address line 1", "12 Example Street", "Printed on the invoice."),
    (13, "Address line 2", "City, Country", "Printed on the invoice."),
    (14, "Email", "hello@yourstudio.com", "Printed on the invoice."),
    (15, "Tax or registration number", "", "Optional. Printed on the invoice when filled in."),
    (16, "How to pay", "Bank transfer. Account name: Your Name Studio. IBAN: add yours here.", "Printed at the bottom of the invoice."),
    (17, "Closing note", "Thank you for your business.", "Printed at the bottom of the invoice."),
]
se.cell(4, 2, "TRACKER").font = font(9, True, TEAL); se.cell(11, 2, "PRINTABLE INVOICE").font = font(9, True, TEAL)
for r, lab, val, note in rows:
    a = se.cell(r, 2, lab); a.font = font(10, True); a.alignment = Alignment(vertical="center")
    b = se.cell(r, 3, val); b.fill = fill(INPUT); b.border = box; b.font = font(10); b.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    n = se.cell(r, 4, note); n.font = font(9, color="6B7088", italic=True); n.alignment = Alignment(vertical="center", indent=1)
    se.row_dimensions[r].height = 22
se.row_dimensions[16].height = 34
se["C9"].number_format = "0%"
se["C7"].number_format = "0"; se["C8"].number_format = "0"; se["C10"].number_format = "0"
YEAR, TERMS, TAX, SOON, CUR = "Settings!$C$7", "Settings!$C$8", "Settings!$C$9", "Settings!$C$10", "Settings!$C$6"

# ---------------------------------------------------------------- Clients
banner(cl, "Clients", "Add each client once in column A. The grey columns fill themselves from the Invoices tab.", 11, 1)
cw = [3, 28, 20, 34, 26, 10, 15, 15, 15, 15, 13, 15]
heads = ["Client", "Contact person", "Email", "Notes", "Invoices", None, None, None, None, "Avg days to pay", "Last invoice"]
for i, w in enumerate(cw[1:], start=1):
    cl.column_dimensions[L(i)].width = w
cl.column_dimensions["L"].width = 3; cl.column_dimensions["L"].hidden = True
k = cl.cell(4, 1, "Cream cells are yours to type in. Grey cells are calculated, please leave them."); k.font = font(9, color="6B7088", italic=True)
for i, h in enumerate(heads, start=1):
    c = cl.cell(5, i, h); c.fill = fill(TEAL); c.font = font(10, True, WHITE); c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = box
cl["F5"] = '="Invoiced ("&%s&")"' % CUR; cl["G5"] = '="Received ("&%s&")"' % CUR
cl["H5"] = '="Outstanding ("&%s&")"' % CUR; cl["I5"] = '="Overdue ("&%s&")"' % CUR
cl.row_dimensions[5].height = 30
IB, IG, II, IJ, IK, IM, ID = [f"Invoices!${x}${N0}:${x}${N1}" for x in "BGIJKMD"]
for r in range(C0, C1 + 1):
    for c in range(1, 5):
        x = cl.cell(r, c); x.fill = fill(INPUT); x.border = box; x.font = font(10)
    f = {
        5: f'=IF($A{r}="","",COUNTIF({IB},$A{r}))',
        6: f'=IF($A{r}="","",SUMIF({IB},$A{r},{IG}))',
        7: f'=IF($A{r}="","",SUMIF({IB},$A{r},{II}))',
        8: f'=IF($A{r}="","",SUMIFS({IJ},{IB},$A{r},{IJ},">0"))',
        9: f'=IF($A{r}="","",SUMIFS({IJ},{IB},$A{r},{IK},"Overdue"))',
        10: f'=IF($A{r}="","",IFERROR(AVERAGEIF({IB},$A{r},{IM}),""))',
        11: f'=IF($A{r}="","",IF(E{r}=0,"",SUMPRODUCT(MAX(({IB}=$A{r})*{ID}))))',
        12: f'=IF($A{r}="","",F{r}+ROW()/1000000)',
    }
    for c, v in f.items():
        x = cl.cell(r, c, v); x.fill = fill(CALC); x.border = box; x.font = font(10)
        x.number_format = {5: "0", 10: "0", 11: DATE}.get(c, MONEY)
        x.alignment = Alignment(horizontal="center" if c in (5, 10, 11) else "right")
cl.freeze_panes = "B6"
cl.conditional_formatting.add(f"I{C0}:I{C1}", CellIsRule(operator="greaterThan", formula=["0"], font=Font(name=BODY, size=10, bold=True, color=CORAL)))

sample_clients = [
    ("Harbor and Pine Studio", "Studio manager", "accounts@harborandpine.example", "Brand and web work"),
    ("Lumen Labs", "Product lead", "finance@lumenlabs.example", "Monthly retainer"),
    ("Atlas Coffee Roasters", "Owner", "hello@atlascoffee.example", "Packaging, pays late"),
    ("Marigold Events", "Operations", "billing@marigoldevents.example", "Seasonal projects"),
    ("Fieldnote Magazine", "Editor", "editor@fieldnote.example", "Articles, pays on 45 days"),
    ("Kite Analytics", "Marketing", "ap@kiteanalytics.example", "Reports and decks"),
    ("Saffron Kitchen", "Owner", "team@saffronkitchen.example", "Menu and social"),
    ("Tidewater Architects", "Office manager", "office@tidewater.example", "Website rebuild"),
]
if not EMPTY:
    for i, row in enumerate(sample_clients):
        for j, v in enumerate(row):
            cl.cell(C0 + i, j + 1, v)

# ---------------------------------------------------------------- Invoices
banner(inv, "Invoices", "One row per invoice. Type in the cream columns. Due date, balance and status work themselves out.", 14, 1)
iw = [13, 26, 30, 13, 8, 13, 13, 13, 13, 13, 12, 10, 10, 34, 3]
ih = ["Invoice no", "Client", "Project or description", "Issue date", "Terms (days)", "Due date", None, "Date paid", None, None, "Status", "Days late", "Days to pay", "Notes"]
for i, w in enumerate(iw, start=1):
    inv.column_dimensions[L(i)].width = w
inv.column_dimensions["O"].hidden = True
k = inv.cell(4, 1, "Cream cells are yours to type in. Grey cells are calculated, please leave them. Pick the client from the list (add new clients on the Clients tab first)."); k.font = font(9, color="6B7088", italic=True)
calc_cols = (6, 10, 11, 12, 13)
for i, h in enumerate(ih, start=1):
    c = inv.cell(5, i, h); c.fill = fill(NAVY if i in calc_cols else TEAL); c.font = font(10, True, WHITE)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = box
inv["G5"] = '="Amount ("&%s&")"' % CUR; inv["I5"] = '="Amount paid ("&%s&")"' % CUR; inv["J5"] = '="Balance ("&%s&")"' % CUR
inv.row_dimensions[5].height = 30
for r in range(N0, N1 + 1):
    for c in (1, 2, 3, 4, 5, 7, 8, 9, 14):
        x = inv.cell(r, c); x.fill = fill(INPUT); x.border = box; x.font = font(10)
        if c in (4, 8): x.number_format = DATE; x.alignment = Alignment(horizontal="center")
        if c in (7, 9): x.number_format = MONEY
        if c == 5: x.number_format = "0"; x.alignment = Alignment(horizontal="center")
    f = {
        6: f'=IF(D{r}="","",D{r}+IF(E{r}="",{TERMS},E{r}))',
        10: f'=IF(G{r}="","",G{r}-I{r})',
        11: f'=IF(OR(G{r}="",D{r}=""),"",IF(J{r}<=0,"Paid",IF(F{r}<TODAY(),"Overdue",IF(I{r}>0,"Part paid",IF(F{r}-TODAY()<={SOON},"Due soon","Open")))))',
        12: f'=IF(K{r}="Overdue",TODAY()-F{r},"")',
        13: f'=IF(AND(K{r}="Paid",H{r}<>""),H{r}-D{r},"")',
        15: f'=IF(K{r}="Overdue",L{r}+ROW()/1000000,"")',
    }
    for c, v in f.items():
        x = inv.cell(r, c, v); x.fill = fill(CALC); x.border = box; x.font = font(10)
        x.number_format = {6: DATE, 10: MONEY}.get(c, "0")
        x.alignment = Alignment(horizontal="right" if c == 10 else "center")
inv.freeze_panes = "C6"
inv.auto_filter.ref = f"A5:N{N1}"
rng = f"K{N0}:K{N1}"
def status_rule(word, bg, fg, bold=True):
    inv.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=[f'"{word}"'], fill=fill(bg), font=Font(name=BODY, size=10, bold=bold, color=fg)))
status_rule("Paid", "DCE7DE", "2F5D46"); status_rule("Overdue", "F6D5CC", "A3311A"); status_rule("Part paid", "FAE7C6", "8A5A0B")
status_rule("Due soon", "FAE7C6", "8A5A0B"); status_rule("Open", "DDE3F0", NAVY)
dv = DataValidation(type="list", formula1=f"=Clients!$A${C0}:$A${C1}", allow_blank=True, showErrorMessage=False)
inv.add_data_validation(dv); dv.add(f"B{N0}:B{N1}")

D = dt.date
sample_inv = [  # no, client, project, issue, terms, amount, paid date, amount paid, notes
    ("INV-001", 1, "Retainer, January", D(2026, 1, 5), 14, 1800, D(2026, 1, 16), 1800, ""),
    ("INV-002", 0, "Brand refresh, phase 1", D(2026, 1, 19), None, 2400, D(2026, 2, 20), 2400, ""),
    ("INV-003", 4, "Feature article, 1,800 words", D(2026, 2, 2), 45, 720, D(2026, 3, 24), 720, ""),
    ("INV-004", 1, "Retainer, February", D(2026, 2, 4), 14, 1800, D(2026, 2, 17), 1800, ""),
    ("INV-005", 2, "Bag label design", D(2026, 2, 23), None, 950, D(2026, 4, 30), 950, "Paid after two reminders"),
    ("INV-006", 1, "Retainer, March", D(2026, 3, 4), 14, 1800, D(2026, 3, 19), 1800, ""),
    ("INV-007", 5, "Quarterly report design", D(2026, 3, 16), None, 1350, D(2026, 4, 10), 1350, ""),
    ("INV-008", 3, "Spring gala invitation suite", D(2026, 4, 1), 15, 1100, D(2026, 4, 14), 1100, ""),
    ("INV-009", 1, "Retainer, April", D(2026, 4, 6), 14, 1800, D(2026, 4, 21), 1800, ""),
    ("INV-010", 0, "Brand refresh, phase 2", D(2026, 4, 27), None, 3200, D(2026, 5, 29), 3200, ""),
    ("INV-011", 6, "Menu redesign", D(2026, 5, 11), None, 640, D(2026, 6, 2), 640, ""),
    ("INV-012", 1, "Retainer, May", D(2026, 5, 4), 14, 1800, D(2026, 5, 15), 1800, ""),
    ("INV-013", 4, "Interview feature", D(2026, 6, 1), 45, 680, D(2026, 7, 20), 680, ""),
    ("INV-014", 5, "Sales deck", D(2026, 6, 15), None, 1500, D(2026, 7, 9), 1500, ""),
    ("INV-015", 1, "Retainer, June and July", D(2026, 7, 6), 14, 3600, D(2026, 7, 22), 3600, ""),
    ("INV-016", 7, "Website rebuild, deposit", D(2026, 7, 20), 15, 2800, D(2026, 8, 3), 2800, "40 percent deposit"),
    ("INV-017", 3, "Autumn festival signage", D(2026, 8, 17), 15, 1450, D(2026, 9, 4), 1450, ""),
    ("INV-018", 2, "Seasonal packaging set", D(2026, 9, 7), None, 1900, None, None, "Reminder sent 20 Oct and 9 Nov"),
    ("INV-019", 1, "Retainer, August and September", D(2026, 9, 14), 14, 3600, D(2026, 9, 30), 3600, ""),
    ("INV-020", 7, "Website rebuild, build stage", D(2026, 10, 5), 60, 2800, D(2026, 11, 2), 1400, "Half received, rest promised"),
    ("INV-021", 6, "Social media templates", D(2026, 10, 19), None, 780, None, None, "Reminder sent 19 Nov"),
    ("INV-022", 5, "Year end report design", D(2026, 10, 26), None, 1650, None, None, ""),
    ("INV-023", 1, "Retainer, October and November", D(2026, 11, 9), 14, 3600, None, None, ""),
    ("INV-024", 0, "Holiday campaign assets", D(2026, 11, 16), None, 2100, None, None, ""),
]
if not EMPTY:
    for i, (no, ci, proj, issue, terms, amt, pd_, pa, note) in enumerate(sample_inv):
        r = N0 + i
        inv.cell(r, 1, no); inv.cell(r, 2, sample_clients[ci][0]); inv.cell(r, 3, proj); inv.cell(r, 4, issue)
        if terms is not None: inv.cell(r, 5, terms)
        inv.cell(r, 7, amt)
        if pd_: inv.cell(r, 8, pd_)
        if pa is not None: inv.cell(r, 9, pa)
        if note: inv.cell(r, 14, note)

# ranges used by the dashboard
A_, B_, D_, F_, G_, H_, I_, J_, K_, L_, M_, O_ = [f"Invoices!${x}${N0}:${x}${N1}" for x in "ABDFGHIJKLMO"]
Y0, Y1 = f'">="&DATE({YEAR},1,1)', f'"<="&DATE({YEAR},12,31)'

# ---------------------------------------------------------------- Dashboard
db.column_dimensions["A"].width = 3
for c in range(2, 14): db.column_dimensions[L(c)].width = 13.5
db.column_dimensions["N"].width = 3
banner(db, "Invoice and Payment Dashboard", None, 14)
db["B3"] = f'=Settings!$C$5&"   |   Year "&{YEAR}&"   |   Amounts in "&{CUR}'

def card(r, c, label, formula, sub, fmt=MONEY, accent=NAVY):
    db.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 2)
    db.merge_cells(start_row=r + 1, start_column=c, end_row=r + 1, end_column=c + 2)
    db.merge_cells(start_row=r + 2, start_column=c, end_row=r + 2, end_column=c + 2)
    for rr in range(r, r + 3):
        for cc in range(c, c + 3):
            x = db.cell(rr, cc); x.fill = fill(CREAM)
            x.border = Border(left=Side(style="thick", color=accent) if cc == c else None)
    a = db.cell(r, c, label); a.font = font(9, True, "6B7088"); a.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    v = db.cell(r + 1, c, formula); v.font = font(20, False, accent, HEAD); v.number_format = fmt; v.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    s = db.cell(r + 2, c, sub); s.font = font(9, color="6B7088"); s.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    db.row_dimensions[r].height = 20; db.row_dimensions[r + 1].height = 32; db.row_dimensions[r + 2].height = 20

inv_year = f"SUMIFS({G_},{D_},{Y0},{D_},{Y1})"
rec_year = f"SUMIFS({I_},{H_},{Y0},{H_},{Y1})"
cnt_year = f"COUNTIFS({D_},{Y0},{D_},{Y1},{G_},\"<>\")"
card(5, 2, "INVOICED THIS YEAR", f"={inv_year}", f'={cnt_year}&" invoices sent"', accent=NAVY)
card(5, 5, "RECEIVED THIS YEAR", f"={rec_year}", f'="By date paid. "&TEXT(IFERROR(B10/{cnt_year},0),"0%")&" of this year\'s invoices paid in full"', accent=TEAL)
card(5, 8, "OUTSTANDING", f'=SUMIF({J_},">0")', f'=COUNTIF({J_},">0")&" invoices not fully paid"', accent=MUST)
card(5, 11, "OVERDUE", f'=SUMIFS({J_},{K_},"Overdue")', f'=COUNTIF({K_},"Overdue")&" invoices past their due date"', accent=CORAL)
db.row_dimensions[8].height = 8
card(9, 2, "INVOICES PAID IN FULL THIS YEAR", f'=COUNTIFS({D_},{Y0},{D_},{Y1},{K_},"Paid")', f'="Out of "&{cnt_year}&" sent this year"', fmt="0", accent=NAVY)
card(9, 5, "AVERAGE DAYS TO GET PAID", f'=IFERROR(AVERAGE({M_}),0)', "From issue date to date paid, all paid invoices", fmt="0", accent=TEAL)
card(9, 8, "DUE SOON", f'=SUMIFS({J_},{F_},">="&TODAY(),{F_},"<="&TODAY()+{SOON},{J_},">0")', f'="Unpaid and due within "&{SOON}&" days"', accent=MUST)
card(9, 11, "SET ASIDE FOR TAX", f"={rec_year}*{TAX}", f'=TEXT({TAX},"0%")&" of money received this year"', accent=CORAL)
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
        x = db.cell(r, cc, lab); x.font = font(9, True, WHITE); x.fill = fill(TEAL); x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for k2 in range(cc, cc + sp): db.cell(r, k2).fill = fill(TEAL)
        cc += sp
def tcell(r, c, v, fmt=None, span=1, align="right", bold=False, color=INK, bg=None):
    if span > 1: db.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + span - 1)
    x = db.cell(r, c, v); x.font = font(10, bold, color); x.alignment = Alignment(horizontal=align, vertical="center", indent=1 if align == "left" else 0)
    if fmt: x.number_format = fmt
    for k2 in range(c, c + span):
        db.cell(r, k2).border = bottom
        if bg: db.cell(r, k2).fill = fill(bg)
    return x

# monthly table
section(13, 2, "Month by month", 5); section(13, 8, "Invoiced and received", 6)
thead(14, 2, ["Month", "Invoiced", "Received", "Invoices sent", "Still owed"])
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for m in range(1, 13):
    r = 14 + m
    lo, hi = f'">="&DATE({YEAR},{m},1)', f'"<"&DATE({YEAR},{m + 1},1)'
    tcell(r, 2, months[m - 1], align="left", bold=True)
    tcell(r, 3, f"=SUMIFS({G_},{D_},{lo},{D_},{hi})", MONEY)
    tcell(r, 4, f"=SUMIFS({I_},{H_},{lo},{H_},{hi})", MONEY)
    tcell(r, 5, f'=COUNTIFS({D_},{lo},{D_},{hi},{G_},"<>")', "0", align="center")
    tcell(r, 6, f'=SUMIFS({J_},{D_},{lo},{D_},{hi},{J_},">0")', MONEY)
tcell(27, 2, "Total", align="left", bold=True, bg=CREAM)
for c in (3, 4, 5, 6):
    tcell(27, c, f"=SUM({L(c)}15:{L(c)}26)", "0" if c == 5 else MONEY, bold=True, bg=CREAM, align="center" if c == 5 else "right")
ch = BarChart(); ch.type = "col"; ch.grouping = "clustered"; ch.overlap = -10; ch.gapWidth = 60
ch.add_data(Reference(db, min_col=3, max_col=4, min_row=14, max_row=26), titles_from_data=True)
ch.set_categories(Reference(db, min_col=2, min_row=15, max_row=26))
ch.series[0].graphicalProperties.solidFill = NAVY; ch.series[0].graphicalProperties.line.solidFill = NAVY
ch.series[1].graphicalProperties.solidFill = MUST; ch.series[1].graphicalProperties.line.solidFill = MUST
ch.legend.position = "b"; ch.height = 7.6; ch.width = 15.6
ch.y_axis.number_format = '#,##0'; ch.y_axis.majorGridlines.spPr = None
ch.x_axis.delete = False; ch.y_axis.delete = False
db.add_chart(ch, "H14")

# ageing + top clients
db.row_dimensions[28].height = 10
section(29, 2, "How old is the money you are owed", 5); section(29, 8, "Top clients, all time", 6)
thead(30, 2, ["Unpaid balance", "Amount", "Invoices"], [3, 1, 1])
T = "TODAY()"
age = [
    ("Not due yet", f'=SUMIFS({J_},{F_},">="&{T},{J_},">0")', f'=COUNTIFS({F_},">="&{T},{J_},">0")'),
    ("1 to 30 days late", f'=SUMIFS({J_},{F_},"<"&{T},{F_},">="&{T}-30,{J_},">0")', f'=COUNTIFS({F_},"<"&{T},{F_},">="&{T}-30,{J_},">0")'),
    ("31 to 60 days late", f'=SUMIFS({J_},{F_},"<"&{T}-30,{F_},">="&{T}-60,{J_},">0")', f'=COUNTIFS({F_},"<"&{T}-30,{F_},">="&{T}-60,{J_},">0")'),
    ("61 to 90 days late", f'=SUMIFS({J_},{F_},"<"&{T}-60,{F_},">="&{T}-90,{J_},">0")', f'=COUNTIFS({F_},"<"&{T}-60,{F_},">="&{T}-90,{J_},">0")'),
    ("More than 90 days late", f'=SUMIFS({J_},{F_},"<"&{T}-90,{J_},">0")', f'=COUNTIFS({F_},"<"&{T}-90,{J_},">0")'),
]
for i, (lab, a, n) in enumerate(age):
    r = 31 + i
    tcell(r, 2, lab, span=3, align="left", bold=True, color=CORAL if i >= 2 else INK)
    tcell(r, 5, a, MONEY); tcell(r, 6, n, "0", align="center")
tcell(36, 2, "Total outstanding", span=3, align="left", bold=True, bg=CREAM)
tcell(36, 5, "=SUM(E31:E35)", MONEY, bold=True, bg=CREAM); tcell(36, 6, "=SUM(F31:F35)", "0", bold=True, bg=CREAM, align="center")

thead(30, 8, ["Client", "Invoiced", "Outstanding", "Avg days to pay"], [3, 1, 1, 1])
CA, CF, CH, CJ, CL_ = [f"Clients!${x}${C0}:${x}${C1}" for x in "AFHJL"]
for n in range(1, 6):
    r = 30 + n
    mt = f"MATCH(LARGE({CL_},{n}),{CL_},0)"
    tcell(r, 8, f'=IFERROR(INDEX({CA},{mt}),"")', span=3, align="left", bold=True)
    tcell(r, 11, f'=IFERROR(INDEX({CF},{mt}),"")', MONEY)
    tcell(r, 12, f'=IFERROR(INDEX({CH},{mt}),"")', MONEY)
    tcell(r, 13, f'=IFERROR(INDEX({CJ},{mt}),"")', "0", align="center")
tcell(36, 8, "Full list on the Clients tab", span=6, align="left", color="6B7088", bg=CREAM)

# chase list
db.row_dimensions[37].height = 10
section(38, 2, "Chase these first (most overdue)", 12)
thead(39, 2, ["Invoice no", "Client", "Project", "Due date", "Days late", "Balance"], [2, 3, 3, 2, 1, 1])
C_ = f"Invoices!$C${N0}:$C${N1}"
for n in range(1, 6):
    r = 39 + n
    mt = f"MATCH(LARGE({O_},{n}),{O_},0)"
    tcell(r, 2, f'=IFERROR(INDEX({A_},{mt}),"")', span=2, align="left", bold=True)
    tcell(r, 4, f'=IFERROR(INDEX({B_},{mt}),"")', span=3, align="left")
    tcell(r, 7, f'=IFERROR(INDEX({C_},{mt}),"")', span=3, align="left")
    tcell(r, 10, f'=IFERROR(INDEX({F_},{mt}),"")', DATE, span=2, align="center")
    tcell(r, 12, f'=IFERROR(INDEX({L_},{mt}),"")', "0", align="center", bold=True, color=CORAL)
    tcell(r, 13, f'=IFERROR(INDEX({J_},{mt}),"")', MONEY)
n = db.cell(46, 2, "Nothing listed above means nothing is overdue. Everything on this page updates when you edit the Invoices tab."); n.font = font(9, color="6B7088", italic=True)
db.page_setup.orientation = "portrait"; db.page_setup.fitToWidth = 1; db.page_setup.fitToHeight = 1; db.sheet_properties.pageSetUpPr.fitToPage = True
db.print_area = "A1:N46"

# ---------------------------------------------------------------- Printable invoice
for c, w in zip("ABCDEFG", (3, 20, 20, 16, 16, 18, 3)): pr.column_dimensions[c].width = w
pr["B1"] = "Pick an invoice number in the cream cell, then print or save as PDF."; pr["B1"].font = font(9, color="6B7088", italic=True)
pr["E2"] = "Invoice no"; pr["E2"].font = font(9, True, "6B7088"); pr["E2"].alignment = Alignment(horizontal="right", vertical="center", indent=1)
pr["F2"] = "" if EMPTY else "INV-020"; pr["F2"].fill = fill(INPUT); pr["F2"].border = box; pr["F2"].font = font(12, True, NAVY); pr["F2"].alignment = Alignment(horizontal="center", vertical="center")
dv2 = DataValidation(type="list", formula1=f"=Invoices!$A${N0}:$A${N1}", allow_blank=True, showErrorMessage=False)
pr.add_data_validation(dv2); dv2.add("F2")
pr.row_dimensions[2].height = 24
pr["B2"] = "INVOICE"; pr["B2"].font = font(26, False, NAVY, HEAD); pr["B2"].alignment = Alignment(vertical="center")
for c in "BCDEF": pr[f"{c}3"].border = Border(bottom=Side(style="medium", color=NAVY))
MT = f"MATCH($F$2,{A_},0)"
def get(col): return f'IFERROR(INDEX(Invoices!${col}${N0}:${col}${N1},{MT}),"")'
def lab(cell, text):
    pr[cell] = text; pr[cell].font = font(8, True, TEAL)
def val(cell, formula, fmt=None, bold=False, size=10, align="left"):
    pr[cell] = formula; pr[cell].font = font(size, bold); pr[cell].alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
    if fmt: pr[cell].number_format = fmt
lab("B5", "FROM"); val("B6", "=Settings!$C$5", bold=True, size=11); val("B7", '=Settings!$C$12&""'); val("B8", '=Settings!$C$13&""'); val("B9", '=Settings!$C$14&""')
val("B10", '=IF(Settings!$C$15="","","Reg no "&Settings!$C$15)')
lab("E5", "BILL TO"); val("E6", "=" + get("B"), bold=True, size=11)
val("E7", f'=IFERROR(INDEX(Clients!$B${C0}:$B${C1},MATCH($E$6,Clients!$A${C0}:$A${C1},0))&"","")')
val("E8", f'=IFERROR(INDEX(Clients!$C${C0}:$C${C1},MATCH($E$6,Clients!$A${C0}:$A${C1},0))&"","")')
for rr in (6, 7, 8):
    pr.merge_cells(f"E{rr}:F{rr}"); pr[f"E{rr}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=False)
lab("B12", "INVOICE NO"); val("B13", '=$F$2&""', bold=True)
lab("C12", "ISSUE DATE"); val("C13", "=" + get("D"), DATE)
lab("D12", "DUE DATE"); val("D13", "=" + get("F"), DATE)
lab("F12", "STATUS"); val("F13", "=" + get("K"), bold=True)
for c in "BCDEF":
    x = pr[f"{c}15"]; x.fill = fill(NAVY); x.font = font(9, True, WHITE); x.alignment = Alignment(vertical="center", indent=1)
pr.merge_cells("B15:E15"); pr["B15"] = "DESCRIPTION"; pr["F15"] = '="AMOUNT ("&%s&")"' % CUR; pr["F15"].alignment = Alignment(horizontal="right", vertical="center", indent=1)
pr.merge_cells("B16:E16"); val("B16", "=" + get("C")); val("F16", "=" + get("G"), MONEY, align="right")
pr.row_dimensions[15].height = 22; pr.row_dimensions[16].height = 34
for c in "BCDEF": pr[f"{c}16"].border = bottom
for r, t, f, b in ((18, "Total", "=F16", False), (19, "Paid to date", "=" + get("I"), False), (20, "Balance due", "=" + get("J"), True)):
    pr[f"E{r}"] = t; pr[f"E{r}"].font = font(10 if not b else 11, b, NAVY if b else INK); pr[f"E{r}"].alignment = Alignment(horizontal="right", vertical="center", indent=1)
    val(f"F{r}", f, MONEY, bold=b, size=10 if not b else 12, align="right")
    pr.row_dimensions[r].height = 20
for c in "EF":
    pr[f"{c}20"].fill = fill(CREAM); pr[f"{c}20"].border = Border(top=Side(style="medium", color=NAVY))
lab("B22", "HOW TO PAY"); pr.merge_cells("B23:F24"); val("B23", '=Settings!$C$16&""'); pr["B23"].alignment = Alignment(wrap_text=True, vertical="top")
pr.merge_cells("B26:F26"); val("B26", '=Settings!$C$17&""'); pr["B26"].font = font(11, False, NAVY, HEAD, italic=True)
pr.print_area = "A2:G27"; pr.page_setup.orientation = "portrait"; pr.page_setup.fitToWidth = 1; pr.page_setup.fitToHeight = 1; pr.sheet_properties.pageSetUpPr.fitToPage = True
pr.print_options.horizontalCentered = True

# ---------------------------------------------------------------- Start Here
st.column_dimensions["A"].width = 3; st.column_dimensions["B"].width = 5; st.column_dimensions["C"].width = 104; st.column_dimensions["D"].width = 3
banner(st, "Freelance Invoice Tracker", "Know who owes you, how much, and who to chase first. Works in Google Sheets and Excel.", 4)
r = 5
def h(text):
    global r
    x = st.cell(r, 2, text); x.font = font(13, False, NAVY, HEAD); st.row_dimensions[r].height = 26
    for c in (2, 3): st.cell(r, c).border = Border(bottom=Side(style="medium", color=NAVY))
    r += 1
def step(n, text, lines=1):
    global r
    a = st.cell(r, 2, n); a.font = font(11, True, CORAL); a.alignment = Alignment(horizontal="center", vertical="top")
    b = st.cell(r, 3, text); b.font = font(10); b.alignment = Alignment(wrap_text=True, vertical="top")
    lines = -(-len(text) // 100)
    a.alignment = Alignment(horizontal="center", vertical="center"); b.alignment = Alignment(wrap_text=True, vertical="center")
    st.row_dimensions[r].height = 14 * lines + 10; r += 1
def gap():
    global r
    st.row_dimensions[r].height = 8; r += 1
h("Set up in five minutes")
step(1, "Settings tab: type your business name, currency label, the year, your usual payment terms and the share of income you put aside for tax.")
step(2, "Clients tab: list each client once in column A. Contact person and email are optional and appear on the printable invoice.")
step(3, "Invoices tab: add one row for every invoice you send. Fill the invoice number, pick the client, type the issue date and the amount. Leave Terms empty to use your default, or type a number of days for that invoice.", 2)
step(4, "When money arrives, type the date and the amount in Date paid and Amount paid. A part payment keeps the invoice open and shows the balance. When the rest arrives, update the amount paid to the full total and the date to the latest payment.", 2)
step(5, "Dashboard tab: read your year. Nothing to type here. It shows what you invoiced, what you received, what is outstanding, what is overdue, how long clients take to pay, and the five invoices to chase first.", 2)
step(6, "Invoice tab: pick an invoice number and a clean one page invoice fills itself in, ready to print or save as PDF.")
gap()
h("What the statuses mean")
for word, text in (("Paid", "The balance is zero."), ("Part paid", "Some money received, not yet past the due date."), ("Open", "Sent, not paid, not yet close to the due date."),
                   ("Due soon", "Unpaid and inside the due soon window you set in Settings (7 days to start with)."), ("Overdue", "Unpaid or part paid and past the due date. Days late counts up every day.")):
    a = st.cell(r, 3, f"{word}:  {text}"); a.font = font(10); a.alignment = Alignment(wrap_text=True, vertical="center"); st.row_dimensions[r].height = 20
    st.cell(r, 2, ">").font = font(10, True, TEAL); st.cell(r, 2).alignment = Alignment(horizontal="center", vertical="center")
    r += 1
gap()
h("Clearing the sample data")
step(1, "The file arrives with sample clients and invoices so you can see how the dashboard reads. To start fresh, delete the contents of the CREAM cells only.")
step(2, "Invoices tab: select the cream cells from row 6 down (columns A to E, G to I and N) and press Delete. Clients tab: do the same for columns A to D. Then replace the sample details on the Settings tab.", 2)
step(3, "Leave the GREY cells alone. They hold the formulas. If you delete one by accident, copy the same cell from the row above and paste it back.")
gap()
h("Opening the file")
step(">", "Google Sheets: upload the file to Google Drive, open it, then choose File, Save as Google Sheets. Or in a blank sheet choose File, Import, Upload.")
step(">", "Excel: open the file directly (Excel 2010 or later, Windows or Mac). If you see Protected View, click Enable Editing.")
step(">", "Dates: type them the way your computer normally writes dates. If Due date shows an error, the issue date was read as text, so retype it.")
gap()
h("Good to know")
step(">", "The log holds 300 invoices and 50 clients. Statuses and days late use today's date, so they update each time you open the file.")
step(">", "Received this year counts money by the date it was paid. Invoiced this year counts invoices by their issue date. An invoice sent in December and paid in January counts in both years, once each way.", 2)
step(">", "The tax figure is a savings reminder based on the rate you typed. It is not tax advice.")
step(">", "For personal and single business use. Please do not share or resell the file. Made by Inkwell and Co.")
st.sheet_view.zoomScale = 110

# print setup (and tighter print areas when PREVIEW=1, used only to render listing images)
import os
for ws in (inv, cl, se, st):
    ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0; ws.sheet_properties.pageSetUpPr.fitToPage = True
inv.print_title_rows = "5:5"; cl.print_title_rows = "5:5"
if os.environ.get("PREVIEW"):
    inv.print_area = "A1:N32"; cl.print_area = "A1:K16"; se.print_area = "A1:D18"; st.print_area = "A1:D40"
    for ws in (inv, cl, se, st): ws.page_setup.fitToHeight = 1

wb.active = 0
wb.save(out)
print("saved", out)
