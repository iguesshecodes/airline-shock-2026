"""Draws the three dashboard page backgrounds (1280x720 @2x) with Geist.
Native Power BI visuals sit on top at the coordinates used in build_pbip.py."""
import os, sys, base64
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
COBALT, INK, GREY, LINE, PAGE = "#0047FF", "#0B0B0C", "#6B7280", "#E3E7EF", "#F2F4F9"

def font(w, n):
    b = base64.b64encode(open(f"{HERE}/fonts/Geist-{n}.woff2","rb").read()).decode()
    return f"@font-face{{font-family:Geist;font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
CSS = f"""{font(400,'Regular')}{font(500,'Medium')}{font(600,'SemiBold')}{font(700,'Bold')}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1280px;height:720px;background:{PAGE};font-family:Geist;color:{INK};position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}}
.a{{position:absolute}}
.hdr{{left:0;top:0;width:1280px;height:64px;background:{INK}}}
.bar{{left:0;top:64px;width:1280px;height:4px;background:{COBALT}}}
.t{{left:24px;top:12px;color:#fff;font-weight:700;font-size:22px;letter-spacing:-0.02em}}
.st{{left:24px;top:40px;color:#9DB6FF;font-size:12px;font-weight:500}}
.nt{{right:24px;top:24px;color:#9DB6FF;font-size:11.5px;text-align:right;font-weight:500}}
.card{{background:#fff;border:1px solid {LINE};border-radius:8px}}
.hero{{background:{COBALT};border:1px solid {COBALT};border-radius:8px}}
.lb{{font-size:11.5px;font-weight:600;color:{GREY};letter-spacing:0.01em}}
.sb{{font-size:11px;color:{GREY};font-weight:400}}
.h{{font-size:15px;font-weight:600;letter-spacing:-0.01em}}
.hs{{font-size:11.5px;color:{GREY}}}
.hl{{color:#CFDBFF !important}}
"""
def header(sub):
    return f"""<div class="a hdr"></div><div class="a bar"></div>
<div class="a t">The 2026 airline shock: who handled it best?</div>
<div class="a st">{sub}</div>
<div class="a nt">Like for like: Mar to Aug 2026 vs Mar to Aug 2025<br>SpiceJet excluded (no 2025 data)</div>"""
def box(x,y,w,h,cls="card"): return f'<div class="a {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></div>'
def txt(x,y,cls,s,w=None): return f'<div class="a {cls}" style="left:{x}px;top:{y}px;{f"width:{w}px;" if w else ""}">{s}</div>'

def overview():
    h = header("Overview")
    h += box(24,80,200,112) + txt(40,92,"lb","MARKET") + txt(40,170,"sb","Filter every page")
    kp = [("Load factor","all months, all airlines","card"),("Load factor change","points, shock vs baseline","hero"),
          ("Capacity change","seats offered, matched months","card"),("Passenger change","passengers carried, matched months","card")]
    for i,(a,b,c) in enumerate(kp):
        x = 236 + i*(246+12)
        h += box(x,80,246,112,c) + txt(x+16,92,"lb hl" if c=="hero" else "lb",a.upper()) + txt(x+16,168,"sb hl" if c=="hero" else "sb",b)
    h += box(24,204,620,492) + txt(40,216,"h","Did cutting capacity protect load factor?") + txt(40,238,"hs","Each dot is an airline. Left of centre means seats were cut. Higher means load factor improved.")
    h += box(656,204,600,300) + txt(672,216,"h","Resilience score by airline") + txt(672,238,"hs","Passenger change (%) plus load factor change (pts). Higher is better.")
    h += box(656,516,600,180) + txt(672,526,"h","Monthly load factor by market")
    return h
def playbook():
    h = header("Brand playbook")
    h += box(24,80,1232,300) + txt(40,92,"h","Brand playbook") + txt(40,114,"hs","Every airline on the same like for like months, ranked by resilience score.")
    h += box(24,392,610,304) + txt(40,404,"h","Passenger change vs 2025") + txt(40,426,"hs","Percent, matched months")
    h += box(646,392,610,304) + txt(662,404,"h","Load factor change") + txt(662,426,"hs","Percentage points, matched months")
    return h
def findings():
    h = header("Findings and recommendations")
    def panel(x,y,w,hh,title,items,hero=False,big=False):
        s = box(x,y,w,hh,"hero" if hero else "card")
        col = "#fff" if hero else INK; sub = "#DCE6FF" if hero else "#374151"
        s += txt(x+20,y+16,"h",f'<span style="color:{col}">{title}</span>')
        yy = y+60; step = (hh-76)/len(items)
        for it in items:
            num, hd, body = it
            tx = x+20
            if num:
                s += txt(x+20,yy-2,"",f'<div style="font-size:38px;font-weight:700;letter-spacing:-0.03em;color:{COBALT};width:170px">{num}</div>')
                tx = x+210
            tw = w-(tx-x)-24
            s += txt(tx,yy,"",f'<div style="font-size:15px;font-weight:600;color:{col};width:{tw}px;line-height:1.3">{hd}</div><div style="font-size:13.5px;line-height:1.55;color:{sub};margin-top:6px;width:{tw}px">{body}</div>')
            yy += step
        return s
    h += panel(24,80,740,616,"Three findings",[
      ("+0.2%","1. Like for like, the shock was mild overall.","Capacity +0.7%, passengers +0.2%, load factor -0.5 pts (Mar to Aug 2026 vs 2025). The average hides large differences between airlines."),
      ("+8.9%","2. Adding capacity worked only where demand followed.","Jet2 grew seats 5.7% and passengers 8.9% while load factor rose 1.2 pts. easyJet added 7.2% more seats and lost 3.6 pts of load factor."),
      ("-7.2%","3. Cutting capacity protected load factor but cost passengers.","Air India Group cut seats 9.0% and Ryanair UK 7.6%. Both held load factor (+0.5 and +0.3 pts) and lost 7.2% and 5.2% of passengers. TUI Airways is the exception: seats -3.7% and load factor -2.9 pts.")])
    h += panel(776,80,480,300,"Two recommendations",[
      (None,"1. Treat load factor as a guardrail, not the goal.","Cutting seats held load factor at Ryanair UK and Air India but cost 5 to 7% of passengers. Cut only where the volume lost is worth less than the cost saved."),
      (None,"2. Add capacity only where demand is proven.","Jet2 shows growth can fill planes. easyJet shows it can dilute them. Review load factor monthly.")],hero=True)
    h += panel(776,392,480,304,"Limits and assumptions",[
      (None,"Simulated brief","Head of Network and Revenue at a mid-size airline. Descriptive, not causal."),
      (None,"Data","10 airlines, 6 months. UK (CAA) and India (DGCA) definitions differ. No fare or yield data, so profit and pricing are not assessed."),
      (None,"Open question","Wizz Air UK passengers rose while seat-km fell, probably shorter routes. Not verified.")])
    return h

os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1280,"height":720}, device_scale_factor=2)
    for name, fn in (("bg_overview",overview),("bg_playbook",playbook),("bg_findings",findings)):
        pg.set_content(f"<style>{CSS}</style><body>{fn()}</body>")
        pg.wait_for_timeout(300); pg.screenshot(path=f"{OUT}/{name}.png")
    b.close()
print("backgrounds ->", OUT)
