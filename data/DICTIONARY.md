# Data dictionary

One row in observations.csv is one country, one indicator, one year.
Blank cells were dropped. They are not zero.
UG, TZ, ET, and RW appear only on cereal_yield_t_ha and cereal_production_t.
Every other indicator is Kenya only.

| indicator_code | unit | countries | min | max | count | source file |
|---|---|---|---|---|---|---|
| ag_employment_pct | percent of employment | KE | 2000 | 2024 | 25 | ag_employment.csv |
| ag_gdp_pct | percent of GDP | KE | 2000 | 2024 | 25 | ag_gdp.csv |
| ag_land_ha | hectares | KE | 2000 | 2023 | 24 | ag_land.csv |
| ag_land_pct | percent of land area | KE | 2000 | 2023 | 24 | ag_land_pct.csv |
| cereal_area_ha | hectares | KE | 2000 | 2023 | 24 | cereal_area.csv |
| cereal_production_t | tonnes | KE UG TZ ET RW | 2000 | 2024 | 125 | cereal_production.csv |
| cereal_yield_t_ha | tonnes per hectare | KE UG TZ ET RW | 2000 | 2024 | 125 | cereal_yield.csv |
| fertilizer_kg_ha | kg per hectare of arable land | KE | 2000 | 2023 | 24 | fertilizer.csv |
| rural_pop_pct | percent of population | KE | 2000 | 2024 | 25 | rural.csv |

Yield is tonnes per hectare. Do not mix it with the World Bank kilogram series.
Count 125 means five countries across 2000–2024.
Count 24 means the publisher has no 2024 value yet.

License: CC BY 4.0. Cite the World Bank World Development Indicators
and Our World in Data. Downloaded: 16 November 2026.