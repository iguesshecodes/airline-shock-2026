"""Add a matched-month window flag to fact_traffic.

Why: the shock window (Mar to Aug 2026) and the 2025 comparison window
(Mar to Aug 2025) do not hold the same months for every brand. Sep 2026 is
missing for the UK brands and Air India, and SpiceJet has no 2025 data.
Summing raw capacity over unequal windows makes capacity look about 14% lower
(6 months vs 7 months) when it is not. Fix: only compare months that exist
for the brand in BOTH years.

window = "Shock"    brand has this 2026 month AND the same month in 2025
         "Baseline" brand has this 2025 month AND the same month in 2026
         "Other"    everything else (outside Mar to Aug, or unmatched)
"""
import pandas as pd

path = "powerbi/data/fact_traffic.csv"
f = pd.read_csv(path, parse_dates=["month"])
if "window" in f.columns:
    f = f.drop(columns="window")

keys = set(zip(f["brand_id"], f["month"]))
shift = lambda m, n: m + pd.DateOffset(years=n)

def window(r):
    m = r["month"]
    if pd.Timestamp("2026-03-01") <= m <= pd.Timestamp("2026-08-01") and (r["brand_id"], shift(m, -1)) in keys:
        return "Shock"
    if pd.Timestamp("2025-03-01") <= m <= pd.Timestamp("2025-08-01") and (r["brand_id"], shift(m, 1)) in keys:
        return "Baseline"
    return "Other"

f["window"] = f.apply(window, axis=1)
f["month"] = f["month"].dt.strftime("%Y-%m-%d")
f.to_csv(path, index=False)
print(f.groupby(["window"]).size())
