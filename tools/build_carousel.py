"""3-slide LinkedIn carousel (1080x1350). Numbers come from /tmp/results.csv built from powerbi/data."""
import os, sys, base64, csv
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]
CB, INK, PAPER, GREY = "#0047FF", "#0B0B0C", "#F4F6FB", "#5B6475"
def ff(fam, w, n):
    b = base64.b64encode(open(f"{HERE}/fonts/{n}.woff2","rb").read()).decode()
    return f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
R = list(csv.DictReader(open("/tmp/results.csv")))
CSS = ff("Geist",500,"Geist-Medium")+ff("Geist",600,"Geist-SemiBold")+ff("Geist",700,"Geist-Bold")+ff("Mono",500,"GeistMono-Medium")+ff("Mono",600,"GeistMono-SemiBold")+ff("Hand",700,"Caveat-Bold")+f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Geist;color:{INK};-webkit-font-smoothing:antialiased}}
.a{{position:absolute}}
.grid{{background-color:{PAPER};background-image:linear-gradient(#DDE3F0 1px,transparent 1px),linear-gradient(90deg,#DDE3F0 1px,transparent 1px);background-size:30px 30px}}
.h{{font-weight:700;letter-spacing:-0.065em;line-height:.9}}
.mono{{font-family:Mono;font-weight:600;letter-spacing:.02em}}
.hand{{font-family:Hand;font-weight:700;color:{CB}}}
.stk{{background:#fff;border:5px solid #fff;border-radius:16px;box-shadow:0 10px 0 rgba(0,36,140,.18),0 0 0 2px {INK};padding:10px 18px;font-weight:700;letter-spacing:-0.03em;white-space:nowrap}}
.blk{{background:{CB};color:#fff;padding:2px 18px 10px;display:inline-block}}
.ink{{background:{INK};color:#fff;padding:2px 18px 10px;display:inline-block}}
"""
STAR='<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 2 C54 34 66 46 98 50 C66 54 54 66 50 98 C46 66 34 54 2 50 C34 46 46 34 50 2Z" fill="{c}" stroke="{k}" stroke-width="4" stroke-linejoin="round"/></svg>'
def star(x,y,s,c=CB,k=INK,rot=0): return f'<div class="a" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">{STAR.format(s=s,c=c,k=k)}</div>'
CURSOR='<svg width="{s}" height="{s}" viewBox="0 0 22 30" shape-rendering="crispEdges"><path d="M0 0h2v2h2v2h2v2h2v2h2v2h2v2h2v2h-6v2h2v6h-4v-6h-2v-2h-2v2h-2V0z" fill="#fff" stroke="{k}" stroke-width="1.5"/><path d="M2 3v17h2v-2h2v-2h2v2h2v6h1v-6h-2v-4h5v-1h-2v-2h-2v-2h-2v-2h-2V5H6V3z" fill="{k}"/></svg>'
def cursor(x,y,s=84,k=INK): return f'<div class="a" style="left:{x}px;top:{y}px;filter:drop-shadow(5px 6px 0 rgba(0,36,140,.25))">{CURSOR.format(s=s,k=k)}</div>'
def stk(x,y,t,rot=0,bg="#fff",col=INK,fs=34,extra=""): return f'<div class="a stk" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);font-size:{fs}px;background:{bg};color:{col};{extra}">{t}</div>'
def squig(x,y,w,c=CB): return f'<svg class="a" style="left:{x}px;top:{y}px" width="{w}" height="26" viewBox="0 0 {w} 26"><path d="M4 16 C{w*.12} 2,{w*.2} 24,{w*.32} 12 S{w*.52} 2,{w*.64} 14 S{w*.86} 4,{w-6} 12" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/></svg>'
def arrow(d,c=CB,w=8): return f'<svg class="a" style="left:0;top:0" width="1080" height="1350"><path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def foot(n,dark=False):
    c = "#fff" if dark else INK
    return f'<div class="a mono" style="left:60px;bottom:44px;font-size:22px;color:{c}">VARESH NIRBHAVNE</div><div class="a mono" style="right:60px;bottom:44px;font-size:22px;color:{c}">{n} / 4</div>'

def s1():
    h = f'<div class="grid a" style="inset:0"></div>'
    h += f'<div class="a mono" style="left:60px;top:56px;font-size:22px">10 AIRLINES. UK + INDIA. MAR TO AUG 2026 VS 2025.</div>'
    h += f'<div class="a h" style="left:52px;top:150px;font-size:178px">Cut seats</div>'
    h += f'<div class="a h" style="left:52px;top:318px;font-size:178px">or add</div>'
    h += f'<div class="a h" style="left:52px;top:486px;font-size:178px"><span class="blk">seats?</span></div>'
    h += squig(60,690,330)
    h += f'<div class="a" style="left:60px;top:742px;width:620px;font-size:40px;font-weight:600;letter-spacing:-0.04em;line-height:1.12">I compared how 10 airlines handled the 2026 shock. Half cut capacity. Half added it. <span style="color:{CB}">The results split hard.</span></div>'
    # stickers collage
    h += stk(815,120,"Jet2<br><span style='color:%s;font-size:46px'>+8.9%%</span> pax"%CB,5,fs=28,extra="line-height:1.05;text-align:center")
    h += stk(825,300,"Air India Group<br><span style='color:%s;font-size:46px'>-7.2%%</span> pax"%INK,-6,fs=26,extra="line-height:1.05;text-align:center")
    h += stk(770,520,"easyJet UK<br><span style='color:%s;font-size:46px'>-3.6</span> pts LF"%CB,4,bg=INK,col="#fff",fs=26,extra="line-height:1.05;text-align:center")
    h += star(740,28,80,rot=8)+star(40,640,70,rot=-12)+star(950,640,80,rot=14)
    h += cursor(960,440)
    # mini chart card
    h += '<div class="a" style="left:60px;top:960px;width:960px;height:290px;background:#fff;border-radius:22px;box-shadow:0 12px 0 rgba(0,36,140,.18),0 0 0 3px %s"></div>'%INK
    h += '<div class="a mono" style="left:96px;top:990px;font-size:22px;color:%s">RESILIENCE SCORE (PAX CHANGE + LOAD FACTOR CHANGE)</div>'%GREY
    srt = sorted(R,key=lambda r:-float(r['score']))
    mx=11.0  # zero axis x
    for i,r in enumerate(srt):
        sc=float(r['score']); y=1034+i*21
        w=abs(sc)/mx*240; x0 = 700 if sc>=0 else 700-w
        col = CB if sc>=0 else INK
        h += f'<div class="a" style="left:{x0}px;top:{y}px;width:{w}px;height:15px;background:{col};border-radius:3px"></div>'
        h += f'<div class="a mono" style="left:96px;top:{y-4}px;font-size:16px;width:300px">{r["brand"].upper()}</div>'
        lab = f'{sc:+.1f}'
        lx = x0+w+10 if sc>=0 else x0-70
        h += f'<div class="a mono" style="left:{lx}px;top:{y-4}px;font-size:16px;color:{col}">{lab}</div>'
    h += f'<div class="a" style="left:699px;top:1030px;width:2px;height:215px;background:{INK}"></div>'
    h += f'<div class="a hand" style="left:740px;top:1150px;font-size:44px;transform:rotate(-5deg)">swipe for why</div>'
    h += arrow("M930 1200 C 960 1190, 985 1205, 992 1232")
    h += foot(1)
    return h

def s2():
    h = f'<div class="grid a" style="inset:0"></div>'
    h += f'<div class="a h" style="left:52px;top:52px;font-size:96px">Cutting seats</div>'
    h += f'<div class="a h" style="left:52px;top:150px;font-size:96px"><span class="blk">protected</span> load factor.</div>'
    h += f'<div class="a h" style="left:52px;top:250px;font-size:96px"><span class="ink">It cost passengers.</span></div>'
    # chart card
    X0,Y0,W,H = 60,430,960,600
    h += f'<div class="a" style="left:{X0}px;top:{Y0}px;width:{W}px;height:{H}px;background:#fff;border-radius:22px;box-shadow:0 12px 0 rgba(0,36,140,.18),0 0 0 3px {INK}"></div>'
    px0,px1,py0,py1 = X0+70,X0+W-40,Y0+40,Y0+H-90
    xd0,xd1,yd0,yd1 = -10.5,9.5,-4.2,2.0
    fx=lambda v: px0+(v-xd0)/(xd1-xd0)*(px1-px0); fy=lambda v: py1-(v-yd0)/(yd1-yd0)*(py1-py0)
    svg = f'<svg class="a" style="left:0;top:0" width="1080" height="1350">'
    for v in (-10,-5,0,5): svg += f'<line x1="{fx(v)}" y1="{py0}" x2="{fx(v)}" y2="{py1}" stroke="#E3E7EF" stroke-width="2"/>'
    for v in (-4,-2,0,2): svg += f'<line x1="{px0}" y1="{fy(v)}" x2="{px1}" y2="{fy(v)}" stroke="#E3E7EF" stroke-width="2"/>'
    svg += f'<line x1="{fx(0)}" y1="{py0}" x2="{fx(0)}" y2="{py1}" stroke="{INK}" stroke-width="3"/><line x1="{px0}" y1="{fy(0)}" x2="{px1}" y2="{fy(0)}" stroke="{INK}" stroke-width="3"/>'
    for v in (-10,-5,0,5): svg += f'<text x="{fx(v)}" y="{py1+34}" text-anchor="middle" font-family="Mono" font-weight="600" font-size="20" fill="{GREY}">{v:+d}%</text>'.replace('+0%','0%')
    for v in (-4,-2,0,2): svg += f'<text x="{px0-12}" y="{fy(v)+7}" text-anchor="end" font-family="Mono" font-weight="600" font-size="20" fill="{GREY}">{v:+d}</text>'.replace('+0','0')
    svg += f'<text x="{(px0+px1)/2}" y="{py1+68}" text-anchor="middle" font-family="Mono" font-weight="600" font-size="20" fill="{INK}">SEAT CAPACITY CHANGE vs 2025</text>'
    svg += f'<text transform="translate({X0+22},{(py0+py1)/2}) rotate(-90)" text-anchor="middle" font-family="Mono" font-weight="600" font-size="20" fill="{INK}">LOAD FACTOR CHANGE (PTS)</text></svg>'
    h += svg
    lab = {"Jet2":(-40,-58),"Akasa Air":(-60,20),"Wizz Air UK":(-20,52),"British Airways":(-150,-52),"Virgin Atlantic":(20,-52),
           "easyJet UK":(-80,-62),"IndiGo":(-50,20),"Ryanair UK":(-60,20),"Air India Group":(-40,-58),"TUI Airways":(-180,-16)}
    for r in R:
        cx,cy = fx(float(r['cap'])),fy(float(r['lfchg'])); good = float(r['lfchg'])>=0
        h += f'<div class="a" style="left:{cx-13}px;top:{cy-13}px;width:26px;height:26px;border-radius:50%;background:{CB if good else INK};border:4px solid #fff;box-shadow:0 0 0 2px {INK}"></div>'
        dx,dy = lab[r['brand']]
        h += f'<div class="a mono" style="left:{cx+dx}px;top:{cy+dy}px;font-size:19px;background:{INK if not good else CB};color:#fff;padding:3px 10px;border-radius:6px;white-space:nowrap">{r["brand"].upper()}</div>'
    h += f'<div class="a hand" style="left:{fx(-9.8)}px;top:{fy(-0.9)}px;font-size:40px;line-height:1;transform:rotate(-4deg);color:{CB}">cut seats,<br>held load factor</div>'
    h += f'<div class="a hand" style="left:{fx(0.5)}px;top:{fy(-2.75)}px;font-size:40px;line-height:1;transform:rotate(-3deg);color:{INK}">added seats,<br>diluted it</div>'
    h += star(930,Y0-40,90,rot=10)
    # stat strip
    h += stk(60,1052,"Air India Group",-3,fs=30)
    h += f'<div class="a h" style="left:64px;top:1128px;font-size:90px;color:{CB}">-9.0%</div><div class="a mono" style="left:66px;top:1220px;font-size:19px">SEATS</div>'
    h += f'<div class="a h" style="left:340px;top:1128px;font-size:90px;color:{CB}">+0.5</div><div class="a mono" style="left:342px;top:1220px;font-size:19px">LOAD FACTOR PTS</div>'
    h += f'<div class="a h" style="left:650px;top:1128px;font-size:90px">-7.2%</div><div class="a mono" style="left:652px;top:1220px;font-size:19px">PASSENGERS</div>'
    h += cursor(960,1090,70)
    h += foot(2)
    return h

def s3():
    h = f'<div class="a" style="inset:0;background:{CB}"></div>'
    h += f'<div class="a" style="inset:0;background-image:radial-gradient(rgba(255,255,255,.28) 2px,transparent 2px);background-size:30px 30px"></div>'
    h += f'<div class="a h" style="left:52px;top:56px;font-size:122px;color:#fff;width:980px">Load factor is a <span style="background:#fff;color:{INK};padding:0 16px 8px;display:inline-block">guardrail</span>, not the goal.</div>'
    # cards
    def card(x,y,w,hh,title,body,rot,bg="#fff",col=INK,sub="#374151"):
        return f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{hh}px;background:{bg};border-radius:22px;box-shadow:0 12px 0 rgba(0,20,90,.35),0 0 0 3px {INK};transform:rotate({rot}deg);padding:34px 38px"><div style="font-size:48px;font-weight:700;letter-spacing:-0.05em;line-height:1;color:{col}">{title}</div><div style="margin-top:16px;font-size:30px;font-weight:500;letter-spacing:-0.02em;line-height:1.25;color:{sub}">{body}</div></div>'
    h += card(60,500,470,330,"Cut only where volume is cheap to lose","Ryanair UK and Air India held load factor but lost 5 to 7% of passengers.",-2)
    h += card(550,520,470,330,"Add only where demand is proven","Jet2 grew seats 5.7% and filled them. easyJet UK added 7.2% and lost 3.6 pts.",2,bg=INK,col="#fff",sub="#C9D6FF")
    h += star(900,440,100,c="#fff",rot=10)+star(30,880,70,c="#fff",rot=-10)
    # honest limits + CTA
    h += f'<div class="a" style="left:60px;top:900px;width:960px;background:#fff;border-radius:22px;box-shadow:0 12px 0 rgba(0,20,90,.35),0 0 0 3px {INK};padding:30px 38px"><div class="mono" style="font-size:22px;color:{CB}">THE HONEST BIT</div><div style="margin-top:10px;font-size:30px;font-weight:500;letter-spacing:-0.02em;line-height:1.3">Descriptive, not causal. No fare data, so no profit view. UK CAA and India DGCA define load factor slightly differently. SpiceJet left out (no 2025 data).</div></div>'
    h += f'<div class="a h" style="left:60px;top:1150px;font-size:70px;color:#fff">Built in Power BI, SQL, Python.</div>'
    h += stk(60,1236,"github.com/iguesshecodes/airline-shock-2026",-1.5,fs=30)
    h += cursor(880,1225,70)
    h += f'<div class="a mono" style="right:60px;bottom:44px;font-size:22px;color:#fff">4 / 4</div>'
    return h

os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1350},device_scale_factor=1.5)
    for i,fn in enumerate((s1,s2,s3),1):
        pg.set_content(f"<style>{CSS}</style><body>{fn()}</body>"); pg.wait_for_timeout(400)
        pg.screenshot(path=f"{OUT}/slide_{i if i<3 else 4}.png")
    b.close()
print("ok")

# ---- slide 4: code proof (real code from the repo), optional Power BI screenshot ----
from pygments import highlight
from pygments.lexers import SqlLexer, PythonLexer
from pygments.formatters import HtmlFormatter
ROOT=os.path.dirname(HERE)
def code_html(path,lexer,lines):
    src="".join(open(f"{ROOT}/{path}").read().splitlines(True)[lines[0]:lines[1]])
    return highlight(src,lexer,HtmlFormatter(nowrap=True,style="monokai"))
sql=code_html("sql/02_capacity_vs_load_factor.sql",SqlLexer(),(1,22))
py=code_html("notebooks/05_matched_windows.py",PythonLexer(),(20,32))
pbi=os.path.join(ROOT,"portfolio/assets/powerbi_overview.png")
pbi_html=""
if os.path.exists(pbi):
    b=base64.b64encode(open(pbi,"rb").read()).decode()
    pbi_html=f'<div class="a" style="left:60px;top:1010px;width:960px;border-radius:14px;overflow:hidden;box-shadow:0 12px 0 rgba(0,36,140,.18),0 0 0 3px {INK}"><img src="data:image/png;base64,{b}" style="width:100%;display:block"></div>'
def s4():
    h='<div class="grid a" style="inset:0"></div>'
    h+=f'<div class="a h" style="left:52px;top:52px;font-size:96px">Not just a chart.</div><div class="a h" style="left:52px;top:150px;font-size:96px"><span class="blk">The work</span> behind it.</div>'
    box=lambda x,y,w,hh,title,code,fs: f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{hh}px;background:#16181D;border-radius:18px;box-shadow:0 12px 0 rgba(0,36,140,.25),0 0 0 3px {INK};overflow:hidden"><div style="background:#0B0B0C;padding:12px 20px;font-family:Mono;font-weight:600;font-size:17px;color:#9AA4B8;letter-spacing:.03em">{title}</div><pre class="hl" style="margin:0;padding:16px 22px;font-family:Mono;font-weight:500;font-size:{fs}px;line-height:1.38;color:#E8EAF0;white-space:pre-wrap">{code}</pre></div>'
    h+=box(60,290,960,540,"sql/02_capacity_vs_load_factor.sql",sql,15)
    h+=box(60,850,960,400,"notebooks/05_matched_windows.py",py,15)
    h+=pbi_html
    h+=star(930,240,80,rot=10)+foot(3)
    return h
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1350},device_scale_factor=1.5)
    pg.set_content(f"<style>{CSS}{HtmlFormatter(style='monokai').get_style_defs('.hl')}.hl{{background:none}}</style><body>{s4()}</body>"); pg.wait_for_timeout(400)
    pg.screenshot(path=f"{OUT}/slide_3.png"); b.close()
