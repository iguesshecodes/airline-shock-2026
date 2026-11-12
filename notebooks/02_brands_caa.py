import pandas as pd

df = pd.read_csv("clean/caa_passenger.csv", parse_dates=["month"])

brand_map = {
    "BRITISH AIRWAYS PLC": "British Airways",
    "BA CITYFLYER LTD": "British Airways",
    "BA EUROFLYER LTD DBA BRITISH AIRWAYS": "British Airways",
    "EASYJET UK LTD": "easyJet UK",
    "JET2.COM LTD": "Jet2",
    "TUI AIRWAYS LTD": "TUI Airways",
    "VIRGIN ATLANTIC AIRWAYS LTD": "Virgin Atlantic",
    "VIRGIN ATLANTIC INTERNATIONAL": "Virgin Atlantic",
    "WIZZ AIR UK LTD": "Wizz Air UK",
    "RYANAIR UK LTD": "Ryanair UK",
}
df["brand"] = df["airline_name"].map(brand_map)
df = df.dropna(subset=["brand"])

g = df.groupby(["month", "brand"], as_index=False).agg(
    passengers=("total_passengers_uplifted", "sum"),
    ask_k=("seat_km_available_x1000", "sum"),
    rpk_k=("seat_km_used_x1000", "sum"),
)
g["load_factor"] = (g["rpk_k"] / g["ask_k"] * 100).round(1)
g["market"] = "UK"

g.to_csv("clean/uk_brands_monthly.csv", index=False)
print(g.shape)
print(g[g["month"] == "2026-08-01"].to_string(index=False))
