"""Interview-prep + portfolio PDF. Run: python3 tools/build_casebook.py out.pdf"""
import os,sys,base64,csv
from playwright.sync_api import sync_playwright
H=os.path.dirname(os.path.abspath(__file__)); OUT=sys.argv[1]
def ff(w,n):
    b=base64.b64encode(open(f"{H}/fonts/{n}.woff2","rb").read()).decode()
    return f"@font-face{{font-family:Geist;font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
def mono(n,w):
    b=base64.b64encode(open(f"{H}/fonts/{n}.woff2","rb").read()).decode()
    return f"@font-face{{font-family:Mono;font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
R=sorted(csv.DictReader(open("/tmp/results.csv")),key=lambda r:-float(r['score']))
rows="".join(f"<tr><td>{r['brand']}</td><td>{r['market']}</td><td>{r['model']}</td><td class=n>{float(r['cap']):+.1f}%</td><td class=n>{float(r['pax']):+.1f}%</td><td class=n>{float(r['lf_b']):.1f} to {float(r['lf_s']):.1f}</td><td class=n>{float(r['lfchg']):+.1f}</td><td class='n b'>{float(r['score']):+.1f}</td></tr>" for r in R)
css=ff(400,"Geist-Regular")+ff(500,"Geist-Medium")+ff(700,"Geist-Bold")+mono("GeistMono-Medium",500)+mono("GeistMono-SemiBold",600)+"""
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Geist;color:#111;font-size:10.6pt;line-height:1.5}
.pg{width:210mm;height:297mm;padding:18mm 17mm 16mm;position:relative;page-break-after:always;overflow:hidden}
.cover{background:#0047FF;color:#fff}
h1{font-weight:700;letter-spacing:-0.05em;line-height:.92;font-size:58pt}
h2{font-weight:700;letter-spacing:-0.04em;font-size:25pt;line-height:1;margin-bottom:5mm}
h3{font-weight:700;letter-spacing:-0.02em;font-size:12pt;margin:5mm 0 1.5mm}
.m{font-family:Mono;font-weight:600;font-size:8pt;letter-spacing:.04em;text-transform:uppercase}
.tag{display:inline-block;background:#0047FF;color:#fff;padding:0 3mm 1mm}
p{margin-bottom:2.5mm;max-width:165mm}ul{margin:0 0 3mm 5mm}li{margin-bottom:1.2mm}
table{border-collapse:collapse;width:100%;font-size:9pt;margin:3mm 0}
th{background:#111;color:#fff;text-align:left;font-weight:500;padding:2mm 2.5mm;font-size:8.2pt}
td{padding:1.8mm 2.5mm;border-bottom:1px solid #E5E7EB;vertical-align:top}td.n{text-align:right;font-family:Mono;font-weight:500}td.b{color:#0047FF;font-weight:600}
.box{border:1.5px solid #111;border-radius:3mm;padding:4mm 5mm;margin:3mm 0;background:#F4F6FB}
.blue{background:#0047FF;color:#fff;border-color:#0047FF}
code{font-family:Mono;font-size:8.4pt;background:#EEF1F8;padding:0 1mm}
pre{font-family:Mono;font-size:7.8pt;background:#111;color:#fff;padding:3.5mm;border-radius:2mm;margin:2mm 0 3mm;white-space:pre-wrap;line-height:1.45}
.qa{margin-bottom:3.5mm;break-inside:avoid}.q{font-weight:700;letter-spacing:-0.01em}
.foot{position:absolute;bottom:9mm;left:17mm;right:17mm;display:flex;justify-content:space-between}
"""
def page(n,body,cls=""): return f'<div class="pg {cls}">{body}<div class="foot m"><span>Varesh Nirbhavne / Airline shock 2026</span><span>{n}</span></div></div>'
pages=[]
pages.append(f'''<div class="pg cover"><div class="m">Portfolio case study / interview prep</div>
<h1 style="margin-top:38mm">The 2026<br>airline shock.</h1>
<h1 style="margin-top:4mm;color:#111"><span style="background:#fff;padding:0 3mm 2mm;display:inline-block">Who handled<br>it best?</span></h1>
<p style="margin-top:14mm;font-size:14pt;max-width:130mm;font-weight:500;letter-spacing:-0.02em">10 airlines, UK and India. Real public traffic data, SQL, Python and Power BI, built to answer one decision for a simulated Head of Network and Revenue.</p>
<div style="position:absolute;bottom:18mm;left:17mm" class="m">Varesh Nirbhavne / MSc Marketing, University of Birmingham<br>github.com/iguesshecodes/airline-shock-2026</div></div>''')
pages.append(page(2,f'''<h2>The project in one page</h2>
<div class="box blue"><div class="m" style="margin-bottom:2mm">The answer</div><p style="font-size:14pt;font-weight:700;letter-spacing:-0.03em;line-height:1.15;margin:0">Cutting seats protected load factor, but it cost passengers. Load factor is a guardrail, not the goal.</p></div>
<h3>Business question</h3><p>A simulated Head of Network and Revenue at a mid-size airline must choose when fuel costs and regional disruption hit: cut capacity, raise fares, or accept a lower load factor. I wrote the brief myself and say so in the repo. No client was involved.</p>
<h3>What I did</h3><ul><li>Pulled monthly traffic from UK CAA (Table 03) and India DGCA, Jan 2025 to Sep 2026, 211 brand-month rows.</li><li>Built a small star schema (dim_brand, dim_date, fact_traffic) and a SQL layer for passenger change, capacity vs load factor and recovery.</li><li>Used Python for cleaning, a matched-month comparison and the checks.</li><li>Built a 3-page Power BI report: Overview, Brand playbook, Findings.</li></ul>
<h3>Headline numbers (Mar to Aug 2026 vs Mar to Aug 2025, 10 airlines)</h3>
<table><tr><th>Whole sample</th><th>Capacity (seats)</th><th>Passengers</th><th>Load factor</th></tr><tr><td>Change</td><td class=n>+0.7%</td><td class=n>+0.2%</td><td class=n>-0.5 pts</td></tr></table>
<ul><li>Jet2: seats +5.7%, passengers +8.9%, load factor +1.2 pts. Best score, +10.1.</li><li>Air India Group: seats -9.0%, passengers -7.2%, load factor +0.5 pts.</li><li>easyJet UK: seats +7.2%, load factor -3.6 pts.</li><li>TUI Airways: seats -3.7%, passengers -5.7%, load factor -2.9 pts. Lowest score, -8.6.</li></ul>
<h3>Tools</h3><p>SQL (SQLite), Python (pandas), Power BI (PBIP project, DAX, star schema), GitHub.</p>'''))
pages.append(page(3,f'''<h2>Data, method and results</h2>
<h3>Sources</h3><ul><li><b>UK CAA Table 03.</b> UK-registered carriers only, so Ryanair UK and easyJet UK are the UK entities, not the groups.</li><li><b>India DGCA monthly statistics.</b> IndiGo, Air India Group, Akasa Air.</li><li>Emirates, Ryanair and IndiGo company releases are logged in docs/sources_log.md but are not used in the matched-window result.</li></ul>
<h3>Matched-month method</h3><p>The shock window is Mar to Aug 2026. The baseline is Mar to Aug 2025, same months, so seasonality cancels. Only brands with data in both windows are included. SpiceJet is excluded because it has no 2025 data. Load factor is always SUM(passenger-km) / SUM(seat-km), never an average of monthly percentages.</p>
<h3>Results</h3>
<table><tr><th>Airline</th><th>Market</th><th>Model</th><th>Seats</th><th>Pax</th><th>Load factor</th><th>LF pts</th><th>Score</th></tr>{rows}</table>
<p style="font-size:9pt">Resilience score = passenger change % x 100 + load factor change in points. Total shock-window passengers across the 10 airlines: 156,509,291.</p>
<div class="box"><b>Pattern.</b> Across the 10 airlines, capacity change and passenger change move together (correlation about +0.78). Capacity change and load factor change move against each other (about -0.30). n = 10, so this is descriptive, not a statistical claim.</div>'''))
pages.append(page(4,f'''<h2>Model and DAX</h2>
<p>Star schema loaded from CSVs on GitHub. Relationships: fact_traffic[brand_id] to dim_brand[brand_id], fact_traffic[month] to dim_date[month]. Auto date/time is switched off in the model so Power BI does not add hidden date tables.</p>
<table><tr><th>Measure</th><th>Logic</th></tr>
<tr><td>Load Factor</td><td>SUM(rpk_k) / SUM(ask_k)</td></tr>
<tr><td>LF Change (pts)</td><td>LF Shock minus LF Baseline, in points</td></tr>
<tr><td>Capacity Change %</td><td>ASK Shock / ASK Baseline - 1</td></tr>
<tr><td>Passenger Change %</td><td>Pax Shock / Pax Baseline - 1</td></tr>
<tr><td>Resilience Score</td><td>Passenger Change % x 100 + LF Change (pts)</td></tr>
<tr><td>Resilience Rank</td><td>RANKX over ALLSELECTED(dim_brand), with a HASONEVALUE guard</td></tr>
<tr><td>Capacity Stance</td><td>Cut, Hold or Add, from Capacity Change %</td></tr>
<tr><td>Matched Months</td><td>Count of months present in both windows</td></tr></table>
<h3>SQL layer</h3><ul><li><code>01_passenger_change.sql</code> passenger change by brand, shock vs baseline.</li><li><code>02_capacity_vs_load_factor.sql</code> did cutting seats protect load factor.</li><li><code>03_recovery.sql</code> recovery from each brand's low point.</li></ul>
<h3>Python layer</h3><ul><li>01 to 03: load and clean CAA and DGCA files, map brands.</li><li>04: build the SQLite database.</li><li>05: tag every row Shock, Baseline or Other (the matched windows).</li></ul>
<h3>Report design</h3><p>Three pages. Overview answers the question (scatter of capacity vs load factor, resilience bars, KPI cards, market slicer). Brand playbook is the ranked table with a stance per airline. Findings states 3 findings, 2 recommendations and the limits.</p>'''))
pages.append(page(5,f'''<h2>Findings, recommendations, limits</h2>
<h3>Three findings</h3><ul><li><b>Capacity cuts traded passengers for load factor.</b> Air India Group, Ryanair UK and Wizz Air UK cut seats and held or lifted load factor. Air India and Ryanair UK still lost 7.2% and 5.2% of passengers.</li><li><b>Adding seats only worked where demand was proven.</b> Jet2 added 5.7% and filled them. easyJet UK added 7.2% and lost 3.6 load factor points.</li><li><b>TUI Airways was the worst of both.</b> Fewer seats, fewer passengers and lower load factor.</li></ul>
<h3>Two recommendations (to the simulated stakeholder)</h3><ul><li>Cut capacity only on routes where the volume is cheap to lose. Do not cut to protect a load factor number.</li><li>Add capacity only where demand is already proven, and set a load factor floor as a guardrail.</li></ul>
<h3>Limits I state openly</h3><ul><li>Descriptive, not causal. No forecast.</li><li>No fare or yield data, so no profit view. The brief's yield question is only answerable where airlines disclose it.</li><li>UK CAA covers UK-registered carriers only. CAA and DGCA define load factor slightly differently.</li><li>SpiceJet excluded (no 2025 data). Emirates is not in the matched result.</li><li>10 airlines is a small sample.</li></ul>
<h3>What I would do next</h3><ul><li>Add route-level data to see where cuts were cheap.</li><li>Add yield from company releases for the airlines that disclose it.</li><li>Add a drill-through page per airline and tooltips in Power BI.</li></ul>'''))
qa=[("Walk me through the project in 60 seconds.","I set myself a decision brief for a Head of Network and Revenue: when costs spike, cut seats, raise fares or accept lower load factor. I took UK CAA and India DGCA traffic, compared Mar to Aug 2026 with the same months of 2025 for 10 airlines, and found that cutting seats protected load factor but cost passengers, while adding seats only worked at Jet2. I built it in SQL, Python and a 3-page Power BI report."),
("Why did you compare the same months instead of year to date?","Airline traffic is seasonal. Comparing March to August with March to August removes seasonality, so the change is the shock and not the calendar."),
("Why is load factor not just averaged?","Averaging monthly percentages gives small months the same weight as big ones. Summing passenger-km and seat-km first, then dividing, weights by real size."),
("Why did you exclude SpiceJet and Emirates?","SpiceJet has no 2025 data, so it cannot be matched. Emirates is only available from company releases and not in the matched dataset. I log both in the sources log rather than hide them."),
("Your stakeholder is simulated. Is that a problem?","I say it in the first line of the brief. The point is to show the habit: start from a decision, write definitions and assumptions, and end with findings and a recommendation. I would swap in a real stakeholder at once."),
("What does the resilience score mean and why that formula?","It adds passenger change in percent to load factor change in points, so an airline gets credit for both keeping volume and filling seats. It is a simple ranking aid. The weights are a judgement call and I would test alternatives with a real stakeholder."),
("Is the capacity and load factor relationship causal?","No. With 10 airlines the correlation is about -0.30, and other things moved at the same time. I describe the pattern and say it is descriptive."),
("What would you do with fare data?","Compute yield per passenger-km and check whether higher fares offset the lost load factor, which is the bonus question in the brief. Without it I cannot say who made more money."),
("How did you design the Power BI report?","Star schema, 16 DAX measures, three pages. Drawn backgrounds for a consistent header and panels, native visuals for the data so it stays interactive, one cobalt accent with black and white."),
("What went wrong and what did you learn?","Auto date/time created hidden date tables that broke loading, so I disabled it in the model. Shape text did not render reliably, so I used textboxes and drawn backgrounds. I learned to test the project in Power BI early.")]
qh="".join(f'<div class="qa"><div class="q">{q}</div><div>{a}</div></div>' for q,a in qa)
pages.append(page(6,f'<h2>Interview Q and A</h2>{qh}'))
pages.append(page(7,f'''<h2>How to reproduce</h2>
<pre>git clone https://github.com/iguesshecodes/airline-shock-2026
cd airline-shock-2026
python3 notebooks/04_build_db.py
python3 notebooks/05_matched_windows.py
python3 tools/build_pbip.py      # regenerates the Power BI project</pre>
<p>Open <code>powerbi/AirlineShock.pbip</code> in Power BI Desktop. Download the repo as a ZIP and use Extract All into a new empty folder first.</p>
<h3>Repo map</h3><ul><li><code>docs/brief.md</code> simulated brief, definitions, assumptions.</li><li><code>docs/sources_log.md</code> sources, licences, methodology note.</li><li><code>sql/</code> three analysis queries.</li><li><code>notebooks/</code> Python steps 01 to 05.</li><li><code>powerbi/</code> data CSVs and the PBIP project.</li><li><code>portfolio/</code> carousel slides and this document.</li></ul>
<h3>Sources</h3><ul><li>UK Civil Aviation Authority, airport and airline statistics, Table 03.</li><li>India Directorate General of Civil Aviation, monthly domestic traffic statistics.</li></ul>'''))
html=f"<style>{css}</style>"+"".join(pages)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.set_content(html); pg.wait_for_timeout(500)
    pg.pdf(path=OUT,width="210mm",height="297mm",print_background=True); b.close()
