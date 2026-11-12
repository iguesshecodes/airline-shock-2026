import sqlite3
import pandas as pd

uk = pd.read_csv("clean/uk_brands_monthly.csv", parse_dates=["month"])
uk["home_market"] = "UK"
india = pd.read_csv("clean/india_brands_monthly.csv", parse_dates=["month"])
india = india.rename(columns={"rpk": "rpk_k", "ask": "ask_k"})
india["home_market"] = "India"
uk = uk.rename(columns={"ask_k": "ask_k", "rpk_k": "rpk_k"})

cols = ["month", "brand", "home_market", "passengers", "rpk_k", "ask_k"]
fact = pd.concat([uk[cols], india[cols]], ignore_index=True)

model = {"IndiGo": "Low-cost", "Akasa Air": "Low-cost", "SpiceJet": "Low-cost",
         "Air India Group": "Full-service", "easyJet UK": "Low-cost",
         "Ryanair UK": "Low-cost", "Wizz Air UK": "Low-cost", "Jet2": "Leisure",
         "TUI Airways": "Leisure", "British Airways": "Full-service",
         "Virgin Atlantic": "Full-service"}
dim_brand = (fact[["brand", "home_market"]].drop_duplicates()
             .sort_values(["home_market", "brand"]).reset_index(drop=True))
dim_brand["brand_id"] = dim_brand.index + 1
dim_brand["business_model"] = dim_brand["brand"].map(model)

months = sorted(fact["month"].unique())
dim_date = pd.DataFrame({"month": months})
dim_date["year"] = dim_date["month"].dt.year
dim_date["month_num"] = dim_date["month"].dt.month
dim_date["month_name"] = dim_date["month"].dt.strftime("%b")
dim_date["in_shock_window"] = ((dim_date["month"] >= "2026-03-01") &
                               (dim_date["month"] <= "2026-09-01")).astype(int)
dim_date["compare_window"] = ((dim_date["month"] >= "2025-03-01") &
                              (dim_date["month"] <= "2025-09-01")).astype(int)

f = fact.merge(dim_brand[["brand", "home_market", "brand_id"]], on=["brand", "home_market"])
f = f[["month", "brand_id", "passengers", "rpk_k", "ask_k"]]

con = sqlite3.connect("clean/airline.db")
for name, d in [("dim_brand", dim_brand), ("dim_date", dim_date), ("fact_traffic", f)]:
    d = d.copy()
    if "month" in d.columns:
        d["month"] = d["month"].dt.strftime("%Y-%m-%d")
    d.to_sql(name, con, if_exists="replace", index=False)
con.close()
print(len(dim_brand), "brands,", len(dim_date), "months,", len(f), "fact rows")
print(dim_brand.to_string(index=False))
