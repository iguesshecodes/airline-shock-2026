import glob, re
import pandas as pd

names = {"air_india": "Air India Group", "air_india_express": "Air India Group",
         "akasa_air": "Akasa Air", "indigo": "IndiGo", "spicejet": "SpiceJet"}
rows = []
for f in sorted(glob.glob("raw/dgca/dgca_*.xlsx")):
    m = re.match(r"raw/dgca/dgca_(\d{4})_(.+)\.xlsx", f)
    year, key = int(m.group(1)), m.group(2)
    key = "indigo" if key.startswith("indigo") else key
    if key not in names:
        continue
    raw = pd.read_excel(f, header=None)
    block = raw.iloc[3:15, [0, 4, 5, 6]]
    block.columns = ["m", "passengers", "rpk", "ask"]
    for i, r in enumerate(block.itertuples(index=False)):
        if pd.notna(r.passengers) and float(r.ask) > 0:
            rows.append({"month": pd.Timestamp(year, i + 1, 1), "brand": names[key],
                         "passengers": float(r.passengers), "rpk": float(r.rpk), "ask": float(r.ask)})
d = pd.DataFrame(rows)
# Air India Group needs both Air India and Air India Express to be complete
d["src"] = 1
cnt = d.groupby(["month", "brand"])["src"].transform("sum")
d = d[~((d["brand"] == "Air India Group") & (cnt < 2))].drop(columns="src")
g = d.groupby(["month", "brand"], as_index=False)[["passengers", "rpk", "ask"]].sum()
g["load_factor"] = (g["rpk"] / g["ask"] * 100).round(1)
g["market"] = "India (domestic)"
g.to_csv("clean/india_brands_monthly.csv", index=False)
print(g.shape)
print(g[g["month"] == "2026-08-01"].to_string(index=False))
