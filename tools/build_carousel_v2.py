"""LinkedIn carousel v2 (1080x1350, dark editorial collage). Uses real Power BI PDF crops in portfolio/assets and real repo code.
Run: python3 tools/build_carousel_v2.py OUT_DIR"""
import os, sys, base64, csv
from playwright.sync_api import sync_playwright
from pygments import highlight
from pygments.lexers import SqlLexer, PythonLexer
from pygments.formatters import HtmlFormatter
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); OUT=sys.argv[1]
CB,INK,LB="#0047FF","#0A0B10","#0047FF"
def b64(p): return base64.b64encode(open(p,"rb").read()).decode()
def ff(fam,w,n,style="normal"): return f"@font-face{{font-family:{fam};font-weight:{w};font-style:{style};src:url(data:font/woff2;base64,{b64(f'{HERE}/fonts/{n}.woff2')}) format('woff2')}}"
def img(n): return "data:image/png;base64,"+b64(f"{ROOT}/portfolio/assets/{n}.png")
CSS=(ff("Geist",500,"Geist-Medium")+ff("Geist",700,"Geist-Bold")+ff("Mono",500,"GeistMono-Medium")+ff("Mono",600,"GeistMono-SemiBold")+ff("Hand",700,"Caveat-Bold")+ff("Stix",400,"StixTwo-Italic","italic")+ff("Stix",400,"StixTwo-Regular")+
f"""*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Geist;color:{INK};background:#F4F6FB;-webkit-font-smoothing:antialiased}}
.a{{position:absolute}} .h{{font-weight:700;letter-spacing:-0.06em;line-height:.92}}
.mono{{font-family:Mono;font-weight:600;letter-spacing:.03em}}
.hand{{font-family:Hand;font-weight:700;color:{LB}}}
.fm{{font-family:Stix;font-style:italic;color:rgba(10,11,16,.85);white-space:nowrap}} .fm sub{{font-size:.62em}}
.tag{{border-radius:14px;padding:9px 18px 11px;font-weight:700;letter-spacing:-0.03em;white-space:nowrap;border:4px solid #fff;box-shadow:0 8px 0 rgba(0,40,160,.25),0 0 0 2px #0A0B10}}
.blk{{background:{CB};color:#fff;display:inline-block;padding:2px 18px 10px}} .wht{{background:{INK};color:#fff;display:inline-block;padding:2px 18px 10px}}
.glow{{background-color:#F4F6FB;background-image:linear-gradient(#DDE3F0 1px,transparent 1px),linear-gradient(90deg,#DDE3F0 1px,transparent 1px);background-size:30px 30px}}
.shot{{background:#fff;border:6px solid #fff;border-radius:16px;box-shadow:0 14px 0 rgba(0,45,180,.22),0 0 0 3px #0A0B10;overflow:hidden}}
.shot img{{display:block;width:100%}}
.code{{background:#14161C;border-radius:16px;border:3px solid #fff;box-shadow:0 14px 0 rgba(0,45,180,.5);overflow:hidden}}
.code .t{{background:#000;padding:10px 18px;font-family:Mono;font-weight:600;font-size:16px;color:#9AA4B8}}
.code pre{{margin:0;padding:14px 20px;font-family:Mono;font-weight:500;line-height:1.38;color:#E8EAF0;white-space:pre-wrap}}
"""+HtmlFormatter(style="monokai").get_style_defs(".hl")+".hl{background:none}")
STAR='<svg width="{s}" height="{s}" viewBox="0 0 100 100"><path d="M50 2 C54 34 66 46 98 50 C66 54 54 66 50 98 C46 66 34 54 2 50 C34 46 46 34 50 2Z" fill="{c}" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>'
def star(x,y,s,c=CB,rot=0): return f'<div class="a" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">{STAR.format(s=s,c=c)}</div>'
CUR='<svg width="{s}" height="{s}" viewBox="0 0 22 30" shape-rendering="crispEdges"><path d="M0 0h2v2h2v2h2v2h2v2h2v2h2v2h2v2h-6v2h2v6h-4v-6h-2v-2h-2v2h-2V0z" fill="#fff" stroke="#000" stroke-width="1.5"/><path d="M2 3v17h2v-2h2v-2h2v2h2v6h1v-6h-2v-4h5v-1h-2v-2h-2v-2h-2v-2h-2V5H6V3z" fill="#000"/></svg>'
def cur(x,y,s=84): return f'<div class="a" style="left:{x}px;top:{y}px;filter:drop-shadow(5px 6px 0 rgba(0,70,255,.6))">{CUR.format(s=s)}</div>'
def tag(x,y,t,rot=0,bg="#fff",col=INK,fs=30,bd="#fff"): return f'<div class="a tag" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);font-size:{fs}px;background:{bg};color:{col};border-color:{bd};line-height:1.05;text-align:center">{t}</div>'
def fm(x,y,t,fs=40,rot=0,op=1): return f'<div class="a fm" style="left:{x}px;top:{y}px;font-size:{fs}px;transform:rotate({rot}deg);opacity:{op}">{t}</div>'
def arrow(d,c=LB,w=7): return f'<svg class="a" style="left:0;top:0" width="1080" height="1350"><path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def foot(n): return f'<div class="a mono" style="left:60px;bottom:40px;font-size:21px;color:{INK}">VARESH NIRBHAVNE</div><div class="a mono" style="right:60px;bottom:40px;font-size:21px">{n} / 4</div>'
def chip(x,y,t,rot): return f'<div class="a tag" style="left:{x}px;top:{y}px;transform:rotate({rot}deg);font-family:Mono;font-size:24px;background:#fff;color:#000;border-radius:16px;padding:10px 20px">{t}</div>'
def code_src(path,a,b): return "".join(open(f"{ROOT}/{path}").read().splitlines(True)[a:b])
def code_block(path,lexer,a,b): return highlight(code_src(path,a,b),lexer,HtmlFormatter(nowrap=True,style="monokai"))
def codebox(x,y,w,title,body,fs,rot,hh=None):
    st=f"height:{hh}px;" if hh else ""
    return f'<div class="a code" style="left:{x}px;top:{y}px;width:{w}px;{st}transform:rotate({rot}deg)"><div class="t">{title}</div><pre class="hl" style="font-size:{fs}px">{body}</pre></div>'

def s1():
    h='<div class="a glow" style="inset:0"></div>'
    h+=f'<div class="a mono" style="left:60px;top:60px;font-size:22px;color:{CB}">10 AIRLINES / UK + INDIA / MAR TO AUG 2026 VS 2025</div>'
    h+='<div class="a h" style="left:52px;top:130px;font-size:132px">Half cut seats.</div>'
    h+='<div class="a h" style="left:52px;top:262px;font-size:132px">Half <span class="blk">added them.</span></div>'
    h+='<div class="a" style="left:60px;top:420px;width:760px;font-size:40px;font-weight:500;letter-spacing:-0.04em;line-height:1.12">Who came out ahead after the 2026 shock?</div>'
    h+=f'<div class="a shot" style="left:50px;top:560px;width:980px;transform:rotate(-1.5deg)"><img src="{img("overview")}"></div>'
    h+=tag(700,500,f'Jet2 carried<br><span style="color:{CB};font-size:48px">+8.9%</span> more passengers',3,fs=24,col=INK)
    h+=f'<div class="a hand" style="left:70px;top:1180px;font-size:48px">real data, real Power BI</div>'
    h+=arrow("M470 1215 C 520 1200, 570 1215, 600 1240",c=CB,w=7)
    h+=foot(1); return h

def s2():
    h='<div class="a glow" style="inset:0"></div>'
    h+='<div class="a h" style="left:52px;top:52px;font-size:98px">Cutting seats</div>'
    h+='<div class="a h" style="left:52px;top:150px;font-size:98px"><span class="blk">protected</span> load factor.</div>'
    h+='<div class="a h" style="left:52px;top:248px;font-size:98px"><span class="wht">It cost passengers.</span></div>'
    h+=fm(560,366,'ΔLF = LF<sub>2026</sub> − LF<sub>2025</sub>',36,2,.85)
    h+=f'<div class="a shot" style="left:100px;top:430px;width:880px;transform:rotate(1.3deg)"><img src="{img("scatter")}"></div>'
    h+=tag(385,690,'Air India Group<br>cut 9.0% of seats.<br>Lost 7.2% of passengers',-4,fs=24,col=INK)
    h+=arrow("M388 722 C 340 715, 290 690, 255 648",c=CB,w=8); 
    h+=tag(560,1150,f'easyJet UK added 7.2% of seats.<br><span style="color:{LB}">Load factor fell 3.6 pts</span>',-2,bg=INK,col="#fff",fs=24)
    h+=arrow("M860 1145 C 900 1100, 920 1060, 915 1010",c=CB,w=8)
    h+=star(950,296,70,rot=10)+cur(935,1035,60)
    h+=f'<div class="a hand" style="left:70px;top:1168px;font-size:42px;line-height:1">seats vs passengers:<br>+0.78 correlation (n=10)</div>'
    h+=foot(2); return h

def s3():
    sql=code_src("sql/02_capacity_vs_load_factor.sql",1,22)
    dim=highlight(sql*3,SqlLexer(),HtmlFormatter(nowrap=True))
    h='<div class="a glow" style="inset:0"></div>'
    h+=f'<pre class="a hl" style="left:-20px;top:20px;font-family:Mono;font-size:30px;line-height:1.3;color:#0A0B10;opacity:.05;white-space:pre;transform:rotate(-4deg)">{sql*3}</pre>'
    h+='<div class="a h" style="left:52px;top:52px;font-size:98px">Not just a chart.</div>'
    h+='<div class="a h" style="left:52px;top:150px;font-size:98px"><span class="blk">The work</span> behind it.</div>'
    h+=f'<div class="a shot" style="left:40px;top:330px;width:1000px;transform:rotate(-1.4deg)"><img src="{img("playbook")}"></div>'
    h+=tag(40,300,"Power BI",-4,bg=CB,col="#fff",fs=26)
    h+=codebox(50,650,540,"sql/02_capacity_vs_load_factor.sql",code_block("sql/02_capacity_vs_load_factor.sql",SqlLexer(),1,11),15,-1.5)
    h+=codebox(540,700,490,"notebooks/05_matched_windows.py",code_block("notebooks/05_matched_windows.py",PythonLexer(),22,31),13,2)
    h+=tag(420,622,"SQL",3,bg=CB,col="#fff",fs=26)+tag(940,676,"Python",-3,bg=CB,col="#fff",fs=26)
    h+=f'<div class="a h" style="left:56px;top:1000px;font-size:62px;width:640px">Star schema.<br>16 DAX measures.<br><span class="blk">Matched months.</span></div>'
    h+=fm(700,1030,'LF = Σ RPK / Σ ASK',40,-3,.9)+fm(690,1100,'Cap% = ASK<sub>26</sub> / ASK<sub>25</sub> − 1',34,-2,.7)
    h+=f'<div class="a hand" style="left:690px;top:1180px;font-size:44px;line-height:1">so seasonality<br>cancels out</div>'
    h+=star(960,1190,66,rot=12)+cur(585,1195,60)
    h+=foot(3); return h

def s4():
    h=f'<div class="a" style="inset:0;background:{CB}"></div><div class="a" style="inset:0;background-image:radial-gradient(rgba(255,255,255,.28) 2px,transparent 2px);background-size:30px 30px"></div>'
    h+='<div class="a h" style="left:52px;top:56px;font-size:122px;width:980px">Load factor is a <span class="wht">guardrail</span>, not the goal.</div>'
    def card(x,y,w,hh,t,b,rot,bg="#fff",col=INK,sub="#374151"): return f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{hh}px;background:{bg};border-radius:22px;box-shadow:0 12px 0 rgba(0,20,90,.45),0 0 0 3px #000;transform:rotate({rot}deg);padding:34px 38px"><div style="font-size:48px;font-weight:700;letter-spacing:-0.05em;line-height:1;color:{col}">{t}</div><div style="margin-top:16px;font-size:30px;font-weight:500;letter-spacing:-0.02em;line-height:1.25;color:{sub}">{b}</div></div>'
    h+=card(60,500,470,330,"Cut only where volume is cheap to lose","Ryanair UK and Air India held load factor but lost 5 to 7% of passengers.",-2)
    h+=card(550,520,470,330,"Add only where demand is proven","Jet2 grew seats 5.7% and filled them. easyJet UK added 7.2% and lost 3.6 pts.",2,bg="#000",col="#fff",sub="#C9D6FF")
    h+=star(900,440,100,c="#fff",rot=10)
    h+=f'<div class="a" style="left:60px;top:900px;width:960px;background:#fff;color:#000;border-radius:22px;box-shadow:0 12px 0 rgba(0,20,90,.45),0 0 0 3px #000;padding:30px 38px"><div class="mono" style="font-size:22px;color:{CB}">THE HONEST BIT</div><div style="margin-top:10px;font-size:30px;font-weight:500;letter-spacing:-0.02em;line-height:1.3">Descriptive, not causal. No fare data, so no profit view. UK CAA and India DGCA define load factor slightly differently. SpiceJet left out (no 2025 data).</div></div>'
    h+='<div class="a h" style="left:60px;top:1150px;font-size:70px">Built in Power BI, SQL, Python.</div>'
    h+=tag(60,1236,"github.com/iguesshecodes/airline-shock-2026",-1.5,fs=28,col=INK)
    h+=cur(880,1225,60)
    h+=f'<div class="a mono" style="right:60px;bottom:40px;font-size:21px;opacity:0">.</div>'
    h+=f'<div class="a mono" style="right:60px;bottom:40px;font-size:21px">4 / 4</div>'
    return '<div style="color:#fff">'+h+'</div>'
os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1350},device_scale_factor=1.5)
    for i,fn in enumerate((s1,s2,s3,s4),1):
        pg.set_content(f"<style>{CSS}</style><body>{fn()}</body>"); pg.wait_for_timeout(500)
        pg.screenshot(path=f"{OUT}/slide_{i}.png")
    b.close()
print("ok")
