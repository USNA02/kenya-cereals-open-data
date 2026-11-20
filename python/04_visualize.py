"""Create publication-ready Fiverr portfolio charts from the processed project data.

Run from the repository root:
    python -m pip install -r requirements.txt matplotlib
    python python/04_visualize.py

Outputs are saved to reports/figures/ at 1600x1200 (4:3) resolution.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "observations.csv"
OUT = ROOT / "reports" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA)
ke = df[df["country_code"] == "KE"].copy()
wide = ke.pivot(index="year", columns="indicator_code", values="value").sort_index()

plt.rcParams.update({
    "figure.figsize": (10.67, 8),
    "figure.dpi": 120,
    "savefig.dpi": 150,
    "font.size": 11,
    "axes.titlesize": 17,
    "axes.labelsize": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def save(fig, filename):
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=150, facecolor="white")
    plt.close(fig)
    print(f"Saved {OUT / filename}")

# 1. Kenya production and yield, 2000-2024: separate aligned panels
# prevent the different units/scales from being conflated.
d = wide.loc[2000:2024, ["cereal_production_t", "cereal_yield_t_ha"]].dropna()
fig, axes = plt.subplots(2, 1, sharex=True, figsize=(10.67, 8))
axes[0].plot(d.index, d["cereal_production_t"] / 1_000_000, marker="o", linewidth=2)
axes[0].set_title("Kenya cereal production and yield | 2000–2024", loc="left", weight="bold")
axes[0].set_ylabel("Production (million tonnes)")
axes[0].grid(axis="y", alpha=.25)
axes[0].annotate("2023 peak: 5.15m tonnes",
                 xy=(2023, d.loc[2023, "cereal_production_t"] / 1_000_000),
                 xytext=(-115, -30), textcoords="offset points",
                 arrowprops={"arrowstyle": "->", "lw": 1})
axes[1].plot(d.index, d["cereal_yield_t_ha"], marker="o", linewidth=2)
axes[1].set_ylabel("Yield (tonnes/hectare)")
axes[1].set_xlabel("Year")
axes[1].grid(axis="y", alpha=.25)
axes[1].annotate("2024: 1.693 t/ha",
                 xy=(2024, d.loc[2024, "cereal_yield_t_ha"]),
                 xytext=(-110, 22), textcoords="offset points",
                 arrowprops={"arrowstyle": "->", "lw": 1})
fig.text(.01, .005, "National cereals harvested as dry grain; not maize alone. Source: World Bank WDI via OWID/DataHub.",
         fontsize=8, color="dimgray")
save(fig, "01_kenya_production_yield_2000_2024.png")

# 2. Five-country 2024 yield comparison.
peer = df[(df["indicator_code"] == "cereal_yield_t_ha") & (df["year"] == 2024)].copy()
country_names = {"ET": "Ethiopia", "UG": "Uganda", "TZ": "Tanzania", "RW": "Rwanda", "KE": "Kenya"}
peer["country"] = peer["country_code"].map(country_names)
peer = peer.sort_values("value")
fig, ax = plt.subplots(figsize=(10.67, 8))
bars = ax.barh(peer["country"], peer["value"])
ax.set_title("Cereal yield across five East African countries | 2024", loc="left", weight="bold")
ax.set_xlabel("Tonnes per hectare")
ax.set_xlim(0, max(peer["value"]) * 1.22)
ax.grid(axis="x", alpha=.25)
for bar, value in zip(bars, peer["value"]):
    ax.text(value + .035, bar.get_y() + bar.get_height()/2, f"{value:.3f}", va="center")
ax.text(.01, -.13, "Country comparison from the project dataset; not a regional average. Source: World Bank WDI via OWID.",
        transform=ax.transAxes, fontsize=8, color="dimgray")
save(fig, "02_east_africa_yield_comparison_2024.png")

# 3. Employment and GDP shares over time: same unit, percentage of national totals.
d = wide.loc[2000:2024, ["ag_employment_pct", "ag_gdp_pct"]].dropna()
fig, ax = plt.subplots(figsize=(10.67, 8))
ax.plot(d.index, d["ag_employment_pct"], marker="o", markevery=4, linewidth=2,
        label="Agriculture share of employment")
ax.plot(d.index, d["ag_gdp_pct"], marker="s", markevery=4, linewidth=2,
        label="Agriculture share of GDP")
ax.set_title("Agriculture's share of employment and GDP | Kenya, 2000–2024", loc="left", weight="bold")
ax.set_ylabel("Share (%)")
ax.set_xlabel("Year")
ax.grid(axis="y", alpha=.25)
ax.legend(frameon=False, loc="best")
ax.annotate("2000: 60.4% jobs | 28.7% GDP",
            xy=(2000, d.loc[2000, "ag_employment_pct"]), xytext=(25, -35),
            textcoords="offset points", arrowprops={"arrowstyle": "->", "lw": 1})
ax.annotate("2024: 46.5% jobs | 22.5% GDP",
            xy=(2024, d.loc[2024, "ag_employment_pct"]), xytext=(-170, 18),
            textcoords="offset points", arrowprops={"arrowstyle": "->", "lw": 1})
ax.text(.01, -.13,
        "Modelled national indicators; not a farm survey or a direct measure of farm productivity/efficiency.",
        transform=ax.transAxes, fontsize=8, color="dimgray")
save(fig, "03_agriculture_employment_gdp_shares.png")

# 4. Data-quality check: reported cereal area vs production / yield.
area = wide[["cereal_production_t", "cereal_yield_t_ha", "cereal_area_ha"]].dropna().copy()
area["implied_area_ha"] = area["cereal_production_t"] / area["cereal_yield_t_ha"]
area["gap_ha"] = area["implied_area_ha"] - area["cereal_area_ha"]
area = area.loc[2018:2023]
fig, ax = plt.subplots(figsize=(10.67, 8))
ax.bar(area.index.astype(str), area["gap_ha"])
ax.axhline(0, linewidth=1)
ax.set_title("Cereal harvested-area validation | Kenya, 2018–2023", loc="left", weight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Implied area minus reported area (hectares)")
ax.grid(axis="y", alpha=.25)
for x, value in enumerate(area["gap_ha"]):
    ax.text(x, value, f"{value:,.0f} ha", ha="center",
            va="bottom" if value >= 0 else "top", fontsize=9)
ax.text(.01, -.13,
        "Implied area = production ÷ yield. Small differences may reflect rounding. 2024 reported area is unavailable.",
        transform=ax.transAxes, fontsize=8, color="dimgray")
save(fig, "04_harvested_area_validation.png")

print("All four charts use data/processed/observations.csv; no manually entered observations.")
