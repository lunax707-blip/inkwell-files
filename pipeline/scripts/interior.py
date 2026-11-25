# Build KDP interior (8.5 x 11 in, no bleed) and the printable download PDF
import sys, glob, os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
clean, fonts, out = sys.argv[1], sys.argv[2], sys.argv[3]
cover_jpg = sys.argv[4] if len(sys.argv) > 4 else None
pdfmetrics.registerFont(TTFont("Fredoka", fonts + "/Fredoka-700.ttf"))
pdfmetrics.registerFont(TTFont("FredokaSB", fonts + "/Fredoka-600.ttf"))
W, H = 8.5*inch, 11*inch
pages = sorted(glob.glob(clean + "/p*.png"))
TITLE1, TITLE2 = "THINGS THAT GO", "and Places to See"
SUB = "A Coloring Book for Kids Ages 4 to 8"

def art(c, f, right=True):
    # 7.5 x 10 in art box; wider margin on the binding (gutter) side
    aw, ah = 7.4*inch, 7.4*inch*4/3
    gutter = 0.6*inch
    x = gutter if right else W - gutter - aw
    y = (H - ah)/2
    c.drawImage(f, x, y, aw, ah)
    c.setLineWidth(2.2); c.setStrokeGray(0)
    c.roundRect(x, y, aw, ah, 14, stroke=1, fill=0)

def title_page(c):
    c.setFillGray(0)
    c.setFont("Fredoka", 54); c.drawCentredString(W/2, H*0.62, TITLE1)
    c.setFont("FredokaSB", 30); c.drawCentredString(W/2, H*0.62 - 46, TITLE2)
    c.setFont("FredokaSB", 17); c.drawCentredString(W/2, H*0.62 - 96, SUB)
    # name plate
    bw, bh = 5.2*inch, 1.5*inch
    bx, by = (W-bw)/2, H*0.2
    c.setLineWidth(2.2); c.roundRect(bx, by, bw, bh, 16)
    c.setFont("FredokaSB", 15); c.drawString(bx+22, by+bh-34, "This book belongs to")
    c.setLineWidth(1.2); c.line(bx+22, by+34, bx+bw-22, by+34)

def note_page(c, kdp):
    c.setFillGray(0); c.setFont("FredokaSB", 13)
    y = H*0.5
    lines = ["Each picture is printed on one side only,",
             "so markers will not spoil the next page." if kdp else "so you can print just the pages you want.",
             "", "Tip: slip a spare sheet of paper behind the page you are coloring." if kdp else "Tip: print on thicker paper if you are using markers.",
             "", "Copyright 2026. All rights reserved.",
             "No part of this book may be reproduced or shared without permission."]
    for l in lines:
        c.drawCentredString(W/2, y, l); y -= 22

# 1) KDP interior: title, note, then art on right-hand pages with blank backs
c = canvas.Canvas(out + "/KDP_interior_8.5x11.pdf", pagesize=(W, H))
c.setTitle("Things That Go and Places to See - Coloring Book"); c.setAuthor("")
title_page(c); c.showPage()
note_page(c, True); c.showPage()
for f in pages:
    art(c, f, right=True); c.showPage()
    c.showPage()  # blank back
c.save()

# 2) Download PDF: cover, title, note, then every page (no blanks)
c = canvas.Canvas(out + "/Things_That_Go_printable.pdf", pagesize=(W, H))
c.setTitle("Things That Go and Places to See - Printable Coloring Pages")
if cover_jpg:
    c.drawImage(cover_jpg, 0, 0, W, H); c.showPage()
title_page(c); c.showPage()
note_page(c, False); c.showPage()
for f in pages:
    aw, ah = 7.5*inch, 10*inch
    x, y = (W-aw)/2, (H-ah)/2
    c.drawImage(f, x, y, aw, ah)
    c.setLineWidth(2.2); c.roundRect(x, y, aw, ah, 14)
    c.showPage()
c.save()
print("done")
