"""Turn raw downloads into one tidy table. Units are part of the name."""
from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

PEERS = {"KEN": "KE", "UGA": "UG", "TZA": "TZ", "ETH": "ET", "RWA": "RW"}

def owid(path, indicator, value_col, countries):
    df = pd.read_csv(RAW / path)
    df = df[df["Code"].isin(countries)].copy()
    df["country_code"] = df["Code"].map(countries)
    df["indicator_code"] = indicator
    df["year"] = df["Year"].astype(int)
    df["value"] = pd.to_numeric(df[value_col], errors="coerce")
    return df[["country_code", "indicator_code", "year", "value"]]

def datahub_kenya(path, indicator):
    df = pd.read_csv(RAW / path)
    df = df[df["Country Code"] == "KEN"].copy()
    df["country_code"] = "KE"
    df["indicator_code"] = indicator
    df["year"] = df["Year"].astype(int)
    df["value"] = pd.to_numeric(df["Value"], errors="coerce")
    return df[["country_code", "indicator_code", "year", "value"]]

frames = [
    owid("cereal_yield.csv", "cereal_yield_t_ha",
         "Cereals - Yield (tonnes per hectare)", PEERS),
    owid("cereal_production.csv", "cereal_production_t",
         "Cereals - Production (tonnes)", PEERS),
    owid("ag_employment.csv", "ag_employment_pct", "Agriculture", {"KEN": "KE"}),
    owid("ag_land.csv", "ag_land_ha",
         "Agricultural land - Area (hectares)", {"KEN": "KE"}),
    datahub_kenya("cereal_area.csv", "cereal_area_ha"),
    datahub_kenya("ag_gdp.csv", "ag_gdp_pct"),
    datahub_kenya("fertilizer.csv", "fertilizer_kg_ha"),
    datahub_kenya("rural.csv", "rural_pop_pct"),
    datahub_kenya("ag_land_pct.csv", "ag_land_pct"),
]

tidy = pd.concat(frames, ignore_index=True)
tidy = tidy.dropna(subset=["value"])
tidy = tidy[(tidy["year"] >= 2000) & (tidy["year"] <= 2024)]
tidy = tidy.drop_duplicates(["country_code", "indicator_code", "year"])
tidy = tidy.sort_values(["indicator_code", "country_code", "year"])
tidy.to_csv(OUT / "observations.csv", index=False)
print(tidy.groupby("indicator_code")["year"].agg(["min", "max", "count"]))