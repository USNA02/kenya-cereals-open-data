# Kenya cereals, 2000 Onwards

## Question

How have Kenya’s cereal harvest, cereal yield, and the gap between
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
Downloaded 16 November 2026. National cereals, not maize alone.
Exact values are in data/processed/observations.csv.

In 2024 Kenya produced 4,978,020 tonnes of cereals, up from
4,227,113 tonnes in 2014. The high year in that window was 2023,
at 5,145,991 tonnes. The 2024 figure is lower than 2023, not a
collapse.

Cereal yield in 2024 was 1.693 tonnes per hectare, which is
1,693 kilograms per hectare. In 2014 it was 1.583 tonnes per
hectare. The path is uneven: 2020 reached 1.843, and 2022 fell
to 1.477.

In 2024 agriculture accounted for 46.5 percent of employment and
22.5 percent of GDP. In 2000 those shares were 60.4 percent and
28.7 percent. Employment's share has fallen. It is still about
twice the GDP share. Both series are modelled national figures,
not a farm survey, so this is not a measure of farm efficiency.

Among the five countries in this file, 2024 cereal yield ranked
Ethiopia 2.632, Uganda 1.920, Tanzania 1.872, Rwanda 1.784, and
Kenya 1.693 tonnes per hectare. Kenya is one country in that
list, not the average of it.

For 2018–2023, production divided by yield matches reported
cereal area within about 70 hectares. The 2024 area has not
been published. It is left blank.

## Reproduce
From this folder, in PowerShell:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python python\01_fetch.py
    python python\02_tidy.py
    python python\03_analysis.py

The database is kenya_lab. Create the tables from sql\01_schema.sql.
Load the indicator names from sql\02_load.sql.
psql reads the CSV. pgAdmin's importer often cannot open a file
in Documents. From this folder:

    psql -U postgres -d kenya_lab -c "\copy kenya.observation (country_code, indicator_code, year, value) FROM 'data/processed/observations.csv' WITH (FORMAT csv, HEADER true)"

Then run the five queries in sql\03_analysis.sql.