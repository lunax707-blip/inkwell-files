import sys, os, zipfile, glob, subprocess
from PIL import Image, ImageDraw, ImageFilter
hi, geo, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
SETS = {
 "Desert_Light_Landscape_Prints": [("L1","01_Dunes_at_Sunset"),("L2","02_Misty_Mountains"),("L3","03_Moon_over_Sea"),("L4","04_Desert_Night"),("L5","05_Blue_Door"),("L6","06_Oasis")],
 "Abstract_Art_Prints": [("A1","01_Arches"),("A2","02_Stones"),("A3","03_Half_Circle"),("A4","04_Horizon"),("A5","05_Currents"),("A6","06_Blocks")],
 "Kids_Room_Transport_Prints": [("K1","01_Rocket"),("K2","02_Hot_Air_Balloon"),("K3","03_Train"),("K4","04_Dump_Truck"),("K5","05_Sailboat"),("K6","06_Airplane")],
}
README = """Thank you for your purchase.

These are high resolution 3:4 ratio files. They print well at 6 x 8, 9 x 12 and 12 x 16 inches (15 x 20, 30 x 40 cm) with no cropping.
For A4, A3 or 8 x 10 frames, choose 'fill page' or 'fit to frame' when printing and a small edge will be trimmed.

Print at home on matte photo paper or thick card, or send the file to any print shop or online print service.
Colors can look slightly different on paper than on screen.

For personal use only. Please do not resell or share the files.
"""
def mock(paths, dst):
    W, H = 2400, 1800
    bg = Image.new("RGB", (W, H), (226, 218, 206))
    fw = 620; fh = int(fw*4/3)
    gapx = (W - 3*fw)//4; gapy = (H - 2*fh*0.86)//3
    for i, p in enumerate(paths):
        scale = 0.86; w2, h2 = int(fw*scale), int(fh*scale)
        x = gapx + (i % 3)*(fw + gapx) + (fw - w2)//2; y = int(gapy + (i//3)*(h2 + gapy))
        sh = Image.new("RGBA", (w2+80, h2+80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((40, 48, w2+40, h2+48), fill=(60, 45, 30, 110))
        sh = sh.filter(ImageFilter.GaussianBlur(16)); bg.paste(sh, (x-40, y-40), sh)
        fr = Image.new("RGB", (w2, h2), (35, 32, 30)); mat = Image.new("RGB", (w2-22, h2-22), (250, 248, 243)); fr.paste(mat, (11, 11))
        art = Image.open(p).convert("RGB"); m = 44; art = art.resize((w2-22-2*m, h2-22-2*m), Image.LANCZOS); fr.paste(art, (11+m, 11+m))
        bg.paste(fr, (x, y))
    bg.save(dst, quality=90)
for name, items in SETS.items():
    d = f"{out}/{name}"; os.makedirs(d, exist_ok=True); paths = []
    for code, title in items:
        im = Image.open(f"{hi}/{code}.jpg").convert("RGB"); print(name, title, im.size)
        p = f"{d}/{title}.jpg"; im.save(p, quality=95, dpi=(300, 300), subsampling=0); paths.append(p)
    open(f"{d}/READ_ME.txt", "w").write(README)
    with zipfile.ZipFile(f"{out}/{name}.zip", "w", zipfile.ZIP_STORED) as z:
        for f in sorted(glob.glob(d + "/*")): z.write(f, os.path.basename(f))
    mock(paths, f"{out}/{name}_preview.jpg")
# geometric set: vector PDFs + 200 dpi JPGs
name = "Geometric_Pattern_Prints"; d = f"{out}/{name}"; os.makedirs(d, exist_ok=True); paths = []
for pdf in sorted(glob.glob(geo + "/Geometric_Print_*.pdf")):
    base = os.path.basename(pdf)[:-4]
    subprocess.run(["cp", pdf, f"{d}/{base}.pdf"], check=True)
    subprocess.run(["pdftoppm", "-r", "200", "-jpeg", "-jpegopt", "quality=93", "-singlefile", pdf, f"{d}/{base}"], check=True)
    paths.append(f"{d}/{base}.jpg")
open(f"{d}/READ_ME.txt", "w").write(README.replace("These are high resolution 3:4 ratio files.", "Each design comes as a vector PDF (sharp at any size, up to 18 x 24 inches and beyond) and a JPG. Both are 3:4 ratio."))
with zipfile.ZipFile(f"{out}/{name}.zip", "w", zipfile.ZIP_STORED) as z:
    for f in sorted(glob.glob(d + "/*")): z.write(f, os.path.basename(f))
mock(paths, f"{out}/{name}_preview.jpg")
for f in sorted(glob.glob(out + "/*.zip")): print(os.path.basename(f), round(os.path.getsize(f)/1e6, 1), "MB")
