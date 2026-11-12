"""Generate the Power BI project (PBIP, PBIR + TMDL) for the airline shock dashboard.
Run from repo root:  python3 tools/build_pbip.py
"""
import json, os, uuid, shutil

ROOT = "powerbi"
RAW = "https://raw.githubusercontent.com/iguesshecodes/airline-shock-2026/main/powerbi/data/"
NAME = "AirlineShock"
SM = f"{ROOT}/{NAME}.SemanticModel"
RP = f"{ROOT}/{NAME}.Report"
SCH = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition"

COBALT, INK, GREY, LINE, PAGE = "#0047FF", "#111111", "#6B7280", "#E5E7EB", "#F3F5FA"

if os.path.exists(SM): shutil.rmtree(SM)
if os.path.exists(RP): shutil.rmtree(RP)

def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

def wj(path, obj):
    w(path, json.dumps(obj, indent=2))

# ------------------------------------------------------------------ project files
wj(f"{ROOT}/{NAME}.pbip", {"version": "1.0", "artifacts": [{"report": {"path": f"{NAME}.Report"}}],
                           "settings": {"enableAutoRecovery": True}})
wj(f"{RP}/definition.pbir", {"version": "4.0", "datasetReference": {"byPath": {"path": f"../{NAME}.SemanticModel"}}})
wj(f"{SM}/definition.pbism", {"version": "4.0", "settings": {}})
w(f"{ROOT}/.gitignore", "**/.pbi/\n**/*.pbix\n")

# ------------------------------------------------------------------ semantic model (TMDL)
T = "\t"
def m_source(csv, cols, ncols):
    types = ", ".join('{"%s", %s}' % (c, t) for c, t in cols)
    return (f'{T*4}let\n'
            f'{T*5}Source = Csv.Document(Web.Contents("{RAW}{csv}"), [Delimiter=",", Columns={ncols}, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\n'
            f'{T*5}Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n'
            f'{T*5}Typed = Table.TransformColumnTypes(Promoted, {{{types}}}, "en-US")\n'
            f'{T*4}in\n{T*5}Typed')

def column(name, dtype, fmt=None, summarize="none", hidden=False, sort=None):
    s = f"{T}column {name}\n{T*2}dataType: {dtype}\n"
    if fmt: s += f"{T*2}formatString: {fmt}\n"
    if hidden: s += f"{T*2}isHidden\n"
    s += f"{T*2}summarizeBy: {summarize}\n{T*2}sourceColumn: {name}\n"
    if sort: s += f"{T*2}sortByColumn: {sort}\n"
    return s + "\n"

def measure(name, expr, fmt=None, folder=None, desc=None):
    q = f"'{name}'" if any(c in name for c in " ()%") else name
    lines = expr.strip("\n").split("\n")
    s = ""
    if desc: s += f"{T}/// {desc}\n"
    if len(lines) == 1:
        s += f"{T}measure {q} = {lines[0]}\n"
    else:
        s += f"{T}measure {q} =\n" + "".join(f"{T*3}{l}\n" for l in lines)
    if fmt: s += f"{T*2}formatString: {fmt}\n"
    if folder: s += f"{T*2}displayFolder: {folder}\n"
    return s + "\n"

# dim_brand
w(f"{SM}/definition/tables/dim_brand.tmdl",
  "table dim_brand\n\n" +
  column("brand", "string") + column("home_market", "string") +
  column("brand_id", "int64", hidden=True) + column("business_model", "string") +
  f"{T}partition dim_brand = m\n{T*2}mode: import\n{T*2}source =\n" +
  m_source("dim_brand.csv", [("brand", "type text"), ("home_market", "type text"),
                             ("brand_id", "Int64.Type"), ("business_model", "type text")], 4) + "\n")

# dim_date
w(f"{SM}/definition/tables/dim_date.tmdl",
  "table dim_date\n\n" +
  column("month", "dateTime", fmt="mmm yyyy") + column("year", "int64") +
  column("month_num", "int64", hidden=True) + column("month_name", "string", sort="month_num") +
  column("in_shock_window", "int64", hidden=True) + column("compare_window", "int64", hidden=True) +
  f"{T}partition dim_date = m\n{T*2}mode: import\n{T*2}source =\n" +
  m_source("dim_date.csv", [("month", "type date"), ("year", "Int64.Type"), ("month_num", "Int64.Type"),
                            ("month_name", "type text"), ("in_shock_window", "Int64.Type"),
                            ("compare_window", "Int64.Type")], 6) + "\n")

# fact_traffic with measures
M = []
M.append(measure("Passengers", "SUM(fact_traffic[passengers])", "#,0", "1 Base"))
M.append(measure("Load Factor", "DIVIDE(SUM(fact_traffic[rpk_k]), SUM(fact_traffic[ask_k]))", "0.0%", "1 Base",
                 "Passenger-km divided by seat-km. Always recomputed from sums, never averaged."))
M.append(measure("Capacity (ASK m)", "SUM(fact_traffic[ask_k]) / 1000", "#,0", "1 Base"))
M.append(measure("LF Shock", 'CALCULATE([Load Factor], fact_traffic[window] = "Shock")', "0.0%", "2 Shock vs baseline"))
M.append(measure("LF Baseline", 'CALCULATE([Load Factor], fact_traffic[window] = "Baseline")', "0.0%", "2 Shock vs baseline"))
M.append(measure("LF Change (pts)",
    "IF(ISBLANK([LF Shock]) || ISBLANK([LF Baseline]), BLANK(), ([LF Shock] - [LF Baseline]) * 100)",
    "\"+0.0;-0.0;0.0\"", "2 Shock vs baseline",
    "Load factor change in percentage points, matched months only."))
M.append(measure("ASK Shock", 'CALCULATE(SUM(fact_traffic[ask_k]), fact_traffic[window] = "Shock")', "#,0", "2 Shock vs baseline"))
M.append(measure("ASK Baseline", 'CALCULATE(SUM(fact_traffic[ask_k]), fact_traffic[window] = "Baseline")', "#,0", "2 Shock vs baseline"))
M.append(measure("Capacity Change %", "DIVIDE([ASK Shock] - [ASK Baseline], [ASK Baseline])", "\"+0.0%;-0.0%;0.0%\"",
                 "2 Shock vs baseline", "Seat-km change, same months in both years."))
M.append(measure("Pax Shock", 'CALCULATE(SUM(fact_traffic[passengers]), fact_traffic[window] = "Shock")', "#,0", "2 Shock vs baseline"))
M.append(measure("Pax Baseline", 'CALCULATE(SUM(fact_traffic[passengers]), fact_traffic[window] = "Baseline")', "#,0", "2 Shock vs baseline"))
M.append(measure("Passenger Change %", "DIVIDE([Pax Shock] - [Pax Baseline], [Pax Baseline])", "\"+0.0%;-0.0%;0.0%\"",
                 "2 Shock vs baseline"))
M.append(measure("Resilience Score",
    "IF(ISBLANK([Passenger Change %]) || ISBLANK([LF Change (pts)]), BLANK(), [Passenger Change %] * 100 + [LF Change (pts)])",
    "\"+0.0;-0.0;0.0\"", "3 Scoring",
    "Passenger change in % points plus load factor change in points, equal weights. A simple, documented rule, not a model."))
M.append(measure("Resilience Rank",
    "VAR s = [Resilience Score]\nRETURN IF(ISBLANK(s), BLANK(), RANKX(ALLSELECTED(dim_brand[brand]), [Resilience Score], , DESC, Dense))",
    "0", "3 Scoring"))
M.append(measure("Capacity Stance",
    'VAR c = [Capacity Change %]\nRETURN IF(ISBLANK(c), "No matched data", IF(c >= 0.02, "Added capacity", IF(c <= -0.02, "Cut capacity", "Held capacity")))',
    None, "3 Scoring", "Cut or added means a change of 2% or more."))
M.append(measure("Matched Months",
    'CALCULATE(DISTINCTCOUNT(fact_traffic[month]), fact_traffic[window] = "Shock")', "0", "3 Scoring",
    "Months compared like for like (6 for every brand with 2025 data)."))

w(f"{SM}/definition/tables/fact_traffic.tmdl",
  "table fact_traffic\n\n" +
  column("month", "dateTime", fmt="mmm yyyy", hidden=True) + column("brand_id", "int64", hidden=True) +
  column("passengers", "double", fmt="#,0", summarize="sum", hidden=True) +
  column("rpk_k", "double", fmt="#,0", summarize="sum", hidden=True) +
  column("ask_k", "double", fmt="#,0", summarize="sum", hidden=True) +
  column("window", "string", hidden=True) + "".join(M) +
  f"{T}partition fact_traffic = m\n{T*2}mode: import\n{T*2}source =\n" +
  m_source("fact_traffic.csv", [("month", "type date"), ("brand_id", "Int64.Type"), ("passengers", "type number"),
                                ("rpk_k", "type number"), ("ask_k", "type number"), ("window", "type text")], 6) + "\n")

w(f"{SM}/definition/relationships.tmdl",
  f"relationship {uuid.uuid4()}\n{T}fromColumn: fact_traffic.brand_id\n{T}toColumn: dim_brand.brand_id\n\n"
  f"relationship {uuid.uuid4()}\n{T}fromColumn: fact_traffic.month\n{T}toColumn: dim_date.month\n")
w(f"{SM}/definition/database.tmdl", "database\n\tcompatibilityLevel: 1600\n")
w(f"{SM}/definition/model.tmdl",
  "model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tdiscourageImplicitMeasures\n\n"
  "ref table dim_brand\nref table dim_date\nref table fact_traffic\n")

# ------------------------------------------------------------------ report
theme = {
    "name": "Airline Shock Cobalt",
    "dataColors": [COBALT, INK, "#7FA3FF", GREY, "#BFD1FF", "#374151", "#2E6BFF", "#A3A3A3"],
    "background": "#FFFFFF", "foreground": INK, "tableAccent": COBALT,
    "good": COBALT, "bad": INK, "neutral": GREY,
    "textClasses": {
        "title": {"fontFace": "Segoe UI Semibold", "fontSize": 13, "color": INK},
        "label": {"fontFace": "Segoe UI", "fontSize": 10, "color": GREY},
        "callout": {"fontFace": "Segoe UI Semibold", "fontSize": 28, "color": COBALT}},
}
wj(f"{RP}/StaticResources/RegisteredResources/cobalt-theme.json", theme)
wj(f"{RP}/definition/version.json", {"$schema": f"{SCH}/versionMetadata/1.0.0/schema.json", "version": "2.0.0"})
wj(f"{RP}/definition/report.json", {
    "$schema": f"{SCH}/report/1.0.0/schema.json",
    "themeCollection": {
        "baseTheme": {"name": "CY24SU10", "reportVersionAtImport": "5.59", "type": "SharedResources"},
        "customTheme": {"name": "cobalt-theme.json", "reportVersionAtImport": "5.59", "type": "RegisteredResources"}},
    "resourcePackages": [{"name": "RegisteredResources", "type": "RegisteredResources",
        "items": [{"name": "cobalt-theme.json", "path": "cobalt-theme.json", "type": "CustomTheme"}]}],
    "layoutOptimization": "None"})

lit = lambda v: {"expr": {"Literal": {"Value": v}}}
S = lambda s: lit("'" + s + "'")
solid = lambda hexc: {"solid": {"color": S(hexc)}}

def col(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}
def mea(prop, entity="fact_traffic"):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}
def proj(field, entity, prop, active=False):
    p = {"field": field, "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}
    pass
    return p
def C(prop): return proj(col("dim_brand" if prop in ("brand", "home_market", "business_model") else "dim_date", prop),
                          "dim_brand" if prop in ("brand", "home_market", "business_model") else "dim_date", prop)
def D(prop): return proj(col("dim_date", prop), "dim_date", prop, True)
def B(prop): return proj(col("dim_brand", prop), "dim_brand", prop, True)
def MS(prop): return proj(mea(prop), "fact_traffic", prop)

def container(name, x, y, wd, ht, z, visual, title=None, card=False):
    vco = {}
    if title:
        vco["title"] = [{"properties": {"show": lit("true"), "text": S(title), "fontColor": solid(INK),
                                         "fontSize": lit("12D")}}]
    if card or title:
        vco["background"] = [{"properties": {"show": lit("true"), "color": solid("#FFFFFF"), "transparency": lit("0D")}}]
        vco["border"] = [{"properties": {"show": lit("true"), "color": solid(LINE), "radius": lit("6D")}}]
    if vco: visual["visualContainerObjects"] = vco
    return {"$schema": f"{SCH}/visualContainer/1.0.0/schema.json", "name": name,
            "position": {"x": x, "y": y, "width": wd, "height": ht, "z": z, "tabOrder": z}, "visual": visual}

def vis(vtype, roles, sort=None, objects=None):
    v = {"visualType": vtype, "query": {"queryState": {r: {"projections": p} for r, p in roles.items()}},
         "drillFilterOtherVisuals": True}
    if sort:
        v["query"]["sortDefinition"] = {"sort": [{"field": mea(sort), "direction": "Descending"}], "isDefaultSort": True}
    if objects: v["objects"] = objects
    return v

def textbox(runs):
    return {"visualType": "textbox", "drillFilterOtherVisuals": True,
            "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": runs}]}}]}}

def header(page_title_suffix=""):
    out = []
    out.append(container("hdr_bg", 0, 0, 1280, 72, 0, {
        "visualType": "shape", "drillFilterOtherVisuals": True,
        "objects": {"shape": [{"properties": {"tileShape": S("rectangle")}}],
                    "fill": [{"properties": {"fillColor": solid(INK), "transparency": lit("0D")}}],
                    "outline": [{"properties": {"show": lit("false")}}]}}))
    out.append(container("hdr_title", 24, 10, 820, 52, 1, textbox([{
        "value": "The 2026 airline shock: who handled it best?",
        "textStyle": {"fontFamily": "Segoe UI Semibold", "fontWeight": "bold", "fontSize": "22pt", "color": "#FFFFFF"}}])))
    out.append(container("hdr_note", 860, 14, 396, 48, 2, textbox([{
        "value": "Mar to Aug 2026 vs Mar to Aug 2025, like for like. SpiceJet excluded (no 2025 data).",
        "textStyle": {"fontSize": "9pt", "color": "#BFD1FF"}}])))
    return out

def page(name, display, visuals, order=None):
    d = f"{RP}/definition/pages/{name}"
    wj(f"{d}/page.json", {
        "$schema": f"{SCH}/page/1.0.0/schema.json", "name": name, "displayName": display,
        "displayOption": "FitToPage", "height": 720, "width": 1280,
        "objects": {"background": [{"properties": {"color": solid(PAGE), "transparency": lit("0D")}}]}})
    for v in visuals:
        wj(f"{d}/visuals/{v['name']}/visual.json", v)

# page 1 : overview
p1 = header()
p1.append(container("slicer_market", 24, 84, 220, 96, 3, vis("slicer", {"Values": [B("home_market")]}), title="Market", card=True))
kp = [("kpi_lf", "Load factor (all)", "Load Factor"),
      ("kpi_lfchg", "Load factor change (pts)", "LF Change (pts)"),
      ("kpi_cap", "Capacity change", "Capacity Change %"),
      ("kpi_pax", "Passenger change", "Passenger Change %")]
for i, (n, t, m) in enumerate(kp):
    p1.append(container(n, 260 + i * 252, 84, 240, 96, 4 + i,
                        vis("card", {"Values": [MS(m)]}), title=t, card=True))
p1.append(container("scatter", 24, 192, 620, 504, 8, vis("scatterChart", {
    "Category": [B("brand")], "Series": [proj(col("dim_brand", "home_market"), "dim_brand", "home_market")],
    "X": [MS("Capacity Change %")], "Y": [MS("LF Change (pts)")]}),
    title="Did cutting capacity protect load factor? (each dot is a brand)", card=True))
p1.append(container("bar_resilience", 656, 192, 600, 246, 9, vis("clusteredBarChart", {
    "Category": [B("brand")], "Y": [MS("Resilience Score")]}, sort="Resilience Score"),
    title="Resilience score by brand (higher is better)", card=True))
p1.append(container("line_lf", 656, 450, 600, 246, 10, vis("lineChart", {
    "Category": [D("month")], "Y": [MS("Load Factor")],
    "Series": [proj(col("dim_brand", "home_market"), "dim_brand", "home_market")]}),
    title="Monthly load factor by market", card=True))
page("overview", "Overview", p1)

# page 2 : brand playbook
p2 = header()
p2.append(container("tbl_playbook", 24, 84, 1232, 330, 3, vis("tableEx", {"Values": [
    B("brand"), proj(col("dim_brand", "home_market"), "dim_brand", "home_market"),
    proj(col("dim_brand", "business_model"), "dim_brand", "business_model"),
    MS("Capacity Stance"), MS("Capacity Change %"), MS("Passenger Change %"),
    MS("LF Change (pts)"), MS("Resilience Score"), MS("Resilience Rank"), MS("Matched Months")]}),
    title="Brand playbook (ranked by resilience, matched months only)", card=True))
p2.append(container("bar_pax", 24, 426, 610, 270, 4, vis("clusteredBarChart", {
    "Category": [B("brand")], "Y": [MS("Passenger Change %")]}, sort="Passenger Change %"),
    title="Passenger change vs 2025", card=True))
p2.append(container("bar_lf", 646, 426, 610, 270, 5, vis("clusteredBarChart", {
    "Category": [B("brand")], "Y": [MS("LF Change (pts)")]}, sort="LF Change (pts)"),
    title="Load factor change (pts)", card=True))
page("playbook", "Brand playbook", p2)

wj(f"{RP}/definition/pages/pages.json", {
    "$schema": f"{SCH}/pagesMetadata/1.0.0/schema.json",
    "pageOrder": ["overview", "playbook"], "activePageName": "overview"})
print("PBIP written under", ROOT)
