"""Same five questions as the SQL file, in pandas."""
import pandas as pd

df = pd.read_csv("data/processed/observations.csv")
ke = df[df["country_code"] == "KE"]
wide = ke.pivot(index="year", columns="indicator_code", values="value").sort_index()

# 1. Latest Kenya reading
latest = ke.sort_values("year").groupby("indicator_code").tail(1)
print(latest[["indicator_code", "year", "value"]].to_string(index=False))

# 2. Production and yield
print(wide.loc[2014:2024, ["cereal_production_t", "cereal_yield_t_ha"]])

# 3. East Africa yield in 2024
y = df[df["indicator_code"] == "cereal_yield_t_ha"]
print(y[y["year"] == 2024].sort_values("value", ascending=False).to_string(index=False))

# 4. Jobs vs GDP
print(wide.loc[[2000, 2010, 2020, 2024], ["ag_employment_pct", "ag_gdp_pct"]])

# 5. Area should equal production / yield.
# dropna removes 2024, because reported area is missing. That is correct.
check = wide[["cereal_production_t", "cereal_yield_t_ha", "cereal_area_ha"]].dropna()
check = check.copy()
check["implied_area_ha"] = check["cereal_production_t"] / check["cereal_yield_t_ha"]
check["gap_ha"] = check["implied_area_ha"] - check["cereal_area_ha"]
print(check.tail(6).round(1))