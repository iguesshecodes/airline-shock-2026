import glob
import pandas as pd

files = sorted(glob.glob("raw/caa/caa_table03_*.csv"))
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

df = df[df["type_of_operations"] == "Passenger"].copy()
df["month"] = pd.to_datetime(df["reporting_period"].astype(str), format="%Y%m")
df["airline_name"] = df["airline_name"].str.strip()

keep = ["month", "airline_name", "total_passengers_uplifted",
        "seat_km_available_x1000", "seat_km_used_x1000"]
df = df[keep].sort_values(["month", "airline_name"])

df.to_csv("clean/caa_passenger.csv", index=False)
print(len(files), "files loaded")
print(df.shape)
print(df["month"].min().date(), "to", df["month"].max().date())
