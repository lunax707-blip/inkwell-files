import os, csv
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='/home/claude/fonts/ttf/'
def fr(s,st='300-normal'): return ImageFont.truetype(F+'fraunces-latin-%s.ttf'%st,s)
def ins(s,w='600'): return ImageFont.truetype(F+'instrument-sans-latin-%s-normal.ttf'%w,s)
W,H=1000,1500
WALL=(246,243,236); INK=(32,41,74); CORAL=(217,88,59); CREAM=(244,233,216); TEAL=(31,111,120); MUST=(232,163,61); SOFT=(106,111,130)
O='/home/claude/book/out/'
def caps(d,xy,s,f,fill,sp=4,right=False):
    x,y=xy; s=s.upper()
    if right: x-=sum(d.textlength(c,font=f)+sp for c in s)-sp
    for c in s: d.text((x,y),c,font=f,fill=fill,anchor='ls'); x+=d.textlength(c,font=f)+sp
def shadow(im,img,xy,blur=22,off=(0,18),alpha=90,angle=0):
    if angle: img=img.convert('RGBA').rotate(angle,expand=True,resample=Image.BICUBIC)
    else: img=img.convert('RGBA')
    sh=Image.new('RGBA',im.size,(0,0,0,0)); m=Image.new('L',img.size,0); m.paste(alpha,mask=img.split()[3])
    sh.paste((15,18,35,255),(xy[0]+off[0],xy[1]+off[1]),m); sh=sh.filter(ImageFilter.GaussianBlur(blur))
    im.paste(sh,(0,0),sh); im.paste(img,xy,img)
def fitw(img,w): return img.resize((w,int(img.height*w/img.width)),Image.LANCZOS)
def headline(d,x,y,lines,accent,size,col,acol,lh=1.02):
    for l in lines: d.text((x,y),l,font=fr(size),fill=col,anchor='ls'); y+=int(size*lh)
    d.text((x,y),accent,font=fr(size,'300-italic'),fill=acol,anchor='ls'); return y
def pinA(p):
    im=Image.new('RGB',(W,H),WALL); d=ImageDraw.Draw(im)
    caps(d,(60,84),'Inkwell and Co',ins(20),INK); caps(d,(W-60,84),p['kind'],ins(20),SOFT,right=True)
    y=headline(d,60,210,p['h'],p['a'],86,INK,CORAL)
    img=Image.open(O+p['img']).convert('RGB')
    if img.width>img.height:
        t=fitw(img,W); top=y+70; im.paste(t,(0,top)); by=top+t.height
    else:
        t=fitw(img,560); top=y+60; shadow(im,t,((W-560)//2,top)); by=top+t.height
    ly=min(by+54,H-170)
    d.rectangle([60,ly,520,ly+118],fill=(255,255,255),outline=(205,205,212))
    caps(d,(80,ly+34),p['l1'],ins(17),SOFT); d.text((80,ly+78),p['l2'],font=fr(30,'400-normal'),fill=INK,anchor='ls')
    d.text((480,ly+100),p['price'],font=fr(30,'400-normal'),fill=CORAL,anchor='rs')
    caps(d,(W-60,H-60),'inkwellandco.gumroad.com',ins(18),INK,sp=3,right=True)
    return im
def pinB(p,bg,fg,ac):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    caps(d,(60,84),'Inkwell and Co',ins(20),fg); caps(d,(W-60,84),'Instant download',ins(20),fg,right=True)
    img=Image.open(O+p['img2']).convert('RGB')
    if img.width>img.height: t=fitw(img,900); shadow(im,t,(50,150),alpha=120)
    else: t=fitw(img,600); shadow(im,t,(200,130),alpha=120,angle=-4)
    y=H-150-int(96*1.02)*len(p['h2'])
    headline(d,60,y,p['h2'],p['a2'],96,fg,ac)
    caps(d,(60,H-56),'Print at home today',ins(20),fg); caps(d,(W-60,H-56),'inkwellandco.gumroad.com',ins(18),fg,sp=3,right=True)
    return im
U='https://inkwellandco.gumroad.com/l/'
P=[
 dict(slug='desert-light-prints',kind='Wall art',h=['Desert sunset','wall art,'],a='set of six.',img='wallart/Desert_Light_Landscape_Prints_preview.jpg',img2='wallart/Desert_Light_Landscape_Prints_preview.jpg',l1='Printable set of 6',l2='Desert Light',price='$8',h2=['Warm desert','gallery wall'],a2='you can print.',
   t='Desert Sunset Wall Art Set of 6, Printable Landscape Paintings',dsc='Six warm desert landscape paintings as an instant download. Print at home or at a print shop, frame up to 18 x 24 inches. Boho gallery wall, living room decor, terracotta and sunset tones.'),
 dict(slug='abstract-art-prints',kind='Wall art',h=['Abstract','art prints,'],a='set of six.',img='wallart/Abstract_Art_Prints_preview.jpg',img2='wallart/Abstract_Art_Prints_preview.jpg',l1='Printable set of 6',l2='Abstract Art Prints',price='$8',h2=['Modern abstract','gallery wall'],a2='in one download.',
   t='Abstract Wall Art Set of 6, Printable Modern Paintings',dsc='Six modern abstract paintings in rust, navy and mustard. Instant download, print at home, frame up to 18 x 24 inches. Mid century style gallery wall for living room, bedroom or office.'),
 dict(slug='geometric-pattern-prints',kind='Wall art',h=['Geometric','pattern prints,'],a='set of six.',img='wallart/Geometric_Pattern_Prints_preview.jpg',img2='wallart/Geometric_Pattern_Prints_preview.jpg',l1='Printable set of 6',l2='Geometric Pattern Prints',price='$8',h2=['Bold pattern','posters'],a2='for any wall.',
   t='Geometric Pattern Wall Art Set of 6, Printable Posters',dsc='Six bold geometric pattern posters in teal, mustard, coral and navy. Vector sharp at 18 x 24 inches. Instant download printable wall art for a colorful gallery wall.'),
 dict(slug='kids-room-transport-prints',kind='Kids room',h=['Kids room','wall art,'],a='things that go.',img='wallart/Kids_Room_Transport_Prints_preview.jpg',img2='wallart/Kids_Room_Transport_Prints_preview.jpg',l1='Printable set of 6',l2='Things That Go',price='$8',h2=['Nursery prints','with rockets'],a2='and trains.',
   t='Kids Room Wall Art Set of 6, Printable Transport Nursery Prints',dsc='Rocket, hot air balloon, train, truck, sailboat and plane. Six soft colored prints for a nursery or playroom. Instant download, print at home, frame up to 18 x 24 inches.'),
 dict(slug='things-that-go-coloring',kind='Coloring',h=['30 coloring','pages for'],a='ages 4 to 8.',img='front_cover.jpg',img2='front_cover.jpg',l1='Printable PDF, 30 pages',l2='Things That Go',price='$5',h2=['Trucks, trains','and rockets'],a2='to color.',
   t='Printable Coloring Book for Kids Ages 4 to 8, Trucks Trains Rockets',dsc='30 bold, simple coloring pages of vehicles and places. One PDF, instant download, print as many times as you like. Screen free activity for rainy days, travel and classrooms.'),
 dict(slug='geometric-patterns-coloring',kind='Coloring',h=['Geometric','coloring pages'],a='for calm.',img='Geometric_Patterns_cover.jpg',img2='Geometric_Patterns_cover.jpg',l1='Printable PDF, 20 patterns',l2='Geometric Patterns',price='$5',h2=['20 patterns','to color'],a2='slowly.',
   t='Geometric Pattern Coloring Pages for Adults and Teens, Printable PDF',dsc='20 geometric patterns to color: stars, rosettes, honeycomb, mandalas. Relaxing printable coloring book for adults and teens. Instant download PDF.'),
 dict(slug='trucks-and-diggers-coloring',kind='Coloring',h=['Trucks and','diggers'],a='coloring pages.',img='minipacks/Trucks_and_Diggers_coloring_pages_cover.jpg',img2='minipacks/Trucks_and_Diggers_coloring_pages_cover.jpg',l1='Printable PDF, 10 pages',l2='Trucks and Diggers',price='$2',h2=['10 truck','coloring pages'],a2='for $2.',
   t='Truck and Digger Coloring Pages for Kids, Printable PDF',dsc='10 construction truck and digger coloring pages for ages 4 to 8. Bold lines, easy to color. Instant download, print at home.'),
 dict(slug='sky-sea-space-coloring',kind='Coloring',h=['Sky, sea and','space'],a='coloring pages.',img='minipacks/Sky_Sea_and_Space_coloring_pages_cover.jpg',img2='minipacks/Sky_Sea_and_Space_coloring_pages_cover.jpg',l1='Printable PDF, 10 pages',l2='Sky, Sea and Space',price='$2',h2=['Rockets, boats','and planes'],a2='to color.',
   t='Rocket, Boat and Plane Coloring Pages for Kids, Printable PDF',dsc='10 coloring pages of rockets, planes, boats and submarines for ages 4 to 8. Instant download PDF, print as often as you like.'),
 dict(slug='places-to-see-coloring',kind='Coloring',h=['Places to see','coloring'],a='pages.',img='minipacks/Places_to_See_coloring_pages_cover.jpg',img2='minipacks/Places_to_See_coloring_pages_cover.jpg',l1='Printable PDF, 10 pages',l2='Places to See',price='$2',h2=['Castles and','windmills'],a2='to color.',
   t='Castle and Windmill Coloring Pages for Kids, Printable PDF',dsc='10 coloring pages of castles, lighthouses, windmills and treehouses for ages 4 to 8. Instant download PDF, print at home.'),
]
BG=[(INK,CREAM,MUST),(TEAL,CREAM,MUST),(CORAL,CREAM,INK),(MUST,INK,CORAL)]
rows=[]
for i,p in enumerate(P):
    a=pinA(p); n1='%02d_%s_A.jpg'%(i+1,p['slug']); a.save(O+'pins/'+n1,quality=90)
    b=pinB(p,*BG[i%4]); n2='%02d_%s_B.jpg'%(i+1,p['slug']); b.save(O+'pins/'+n2,quality=90)
    rows.append([n1,p['t'],p['dsc'],U+p['slug']]); rows.append([n2,p['t'],p['dsc'],U+p['slug']])
csv.writer(open(O+'pins/pins.csv','w',newline='')).writerows([['Image','Title','Description','Link']]+rows)
import glob
fs=sorted(glob.glob(O+'pins/*.jpg')); s=Image.new('RGB',(6*260+10,3*385+10),(120,120,120))
for j,f in enumerate(fs): s.paste(Image.open(f).resize((250,375)),(10+(j%6)*260,10+(j//6)*385))
s.save(O+'pins_sheet.png'); print(len(fs))
