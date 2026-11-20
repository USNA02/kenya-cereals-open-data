# Kenya cereals, 2000 Onwards

## Question

How have Kenya's cereal harvest, cereal yield, and the gap between
agricultural jobs and agricultural GDP moved since 2000?

## What this is not

National cereals harvested as dry grain: wheat, rice, maize, sorghum,
millet, and mixed grains. Not maize alone. Not a county table.
Not a price series. Not a farm survey.

## Sources and license

Figures are from the World Bank World Development Indicators, read
through Our World in Data grapher files and the DataHub WDI mirror.
License: CC BY 4.0. Cite the World Bank and Our World in Data.
Downloaded: 16 November 2026.

## Findings

Exact values are in `data/processed/observations.csv`.

- In 2024 Kenya produced 4,978,020 tonnes of cereals, up from
  4,227,113 tonnes in 2014. The high year in that window was 2023,
  at 5,145,991 tonnes. The 2024 figure is lower than 2023, not a
  collapse.
- Cereal yield in 2024 was 1.693 tonnes per hectare (1,693 kg/ha).
  In 2014 it was 1.583 tonnes per hectare. The path is uneven:
  2020 reached 1.843, and 2022 fell to 1.477.
- In 2024 agriculture accounted for 46.5% of employment and 22.5%
  of GDP. In 2000 those shares were 60.4% and 28.7%. Employment's
  share has fallen. Both series are modelled national figures, not
  a farm survey, so this is not a measure of farm efficiency.
- Among the five countries in this file, 2024 cereal yield ranked
  Ethiopia 2.632, Uganda 1.920, Tanzania 1.872, Rwanda 1.784, and
  Kenya 1.693 tonnes per hectare. This is a five-country comparison,
  not a regional average.
- For 2018–2023, production divided by yield matches reported cereal
  area within about 70 hectares. The 2024 area has not been published
  in the dataset and is left blank.

## Reproduce the data workflow

From this folder, in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python python\01_fetch.py
python python\02_tidy.py
python python\03_analysis.py
```

The database is `kenya_lab`. Create the tables from
`sql\01_schema.sql`, load indicator names from `sql\02_load.sql`,
then import the observations:

```powershell
psql -U postgres -d kenya_lab -c "\copy kenya.observation (country_code, indicator_code, year, value) FROM 'data/processed/observations.csv' WITH (FORMAT csv, HEADER true)"
```

Run the five queries in `sql\03_analysis.sql`.

## Reproduce the portfolio charts

Install Matplotlib and run the visualization script from the repository
root:

```powershell
python -m pip install matplotlib
python python\04_visualize.py
```

Four 4:3, high-resolution PNG charts are saved in `reports/figures/`:

1. `01_kenya_production_yield_2000_2024.png` — aligned production and
   yield trend panels, keeping their different units separate.
2. `02_east_africa_yield_comparison_2024.png` — five-country yield
   comparison for 2024.
3. `03_agriculture_employment_gdp_shares.png` — agriculture's share
   of employment and GDP over time.
4. `04_harvested_area_validation.png` — implied versus reported area
   validation for 2018–2023.

All charts are generated from `data/processed/observations.csv`.
No observations are manually re-entered in the visualization script.

## Project structure

- `python/01_fetch.py`: downloads source data.
- `python/02_tidy.py`: standardizes, combines, filters, and exports data.
- `python/03_analysis.py`: answers five analytical questions in pandas.
- `python/04_visualize.py`: creates portfolio-ready figures.
- `sql/01_schema.sql`, `sql/02_load.sql`, `sql/03_analysis.sql`:
  PostgreSQL schema, indicator loading, and analytical queries.
- `data/processed/observations.csv`: tidy long-form analysis dataset.

## Tools

Python, Pandas, Matplotlib, PostgreSQL, SQL, Git, and GitHub.
