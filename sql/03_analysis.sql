-- 1. Latest value for each Kenya series.
-- DISTINCT ON keeps the first row after ORDER BY, per indicator.
SELECT DISTINCT ON (indicator_code)
  indicator_code,
  year,
  value
FROM kenya.observation
WHERE country_code = 'KE'
ORDER BY indicator_code, year DESC;

-- 2. Kenya cereal harvest and yield, 2014-2024.
-- FILTER pivots the long table. Production is tonnes.
-- Yield is tonnes per hectare.
SELECT
  year,
  MAX(value) FILTER (WHERE indicator_code = 'cereal_production_t') AS production_t,
  MAX(value) FILTER (WHERE indicator_code = 'cereal_yield_t_ha') AS yield_t_ha
FROM kenya.observation
WHERE country_code = 'KE'
  AND year BETWEEN 2014 AND 2024
  AND indicator_code IN ('cereal_production_t', 'cereal_yield_t_ha')
GROUP BY year
ORDER BY year;

-- 3. East Africa cereal yield in 2024.
-- Kenya is one country in this list, not the average of the list.
SELECT
  country_code,
  year,
  value AS yield_t_ha,
  RANK() OVER (ORDER BY value DESC) AS yield_rank
FROM kenya.observation
WHERE indicator_code = 'cereal_yield_t_ha'
  AND year = 2024
ORDER BY value DESC;

-- 4. Share of jobs against share of GDP.
-- Both are modelled national series, not a farm survey.
SELECT
  year,
  MAX(value) FILTER (WHERE indicator_code = 'ag_employment_pct') AS employment_pct,
  MAX(value) FILTER (WHERE indicator_code = 'ag_gdp_pct') AS gdp_pct
FROM kenya.observation
WHERE country_code = 'KE'
  AND year IN (2000, 2010, 2020, 2024)
GROUP BY year
ORDER BY year;

-- 5. Harvested area should equal production / yield.
-- A small gap is rounding. A large gap means stop.
-- 2024 has no reported area yet, so that column stays empty.
SELECT
  year,
  MAX(value) FILTER (WHERE indicator_code = 'cereal_production_t') AS production_t,
  MAX(value) FILTER (WHERE indicator_code = 'cereal_yield_t_ha') AS yield_t_ha,
  MAX(value) FILTER (WHERE indicator_code = 'cereal_area_ha') AS reported_area_ha,
  MAX(value) FILTER (WHERE indicator_code = 'cereal_production_t')
    / NULLIF(MAX(value) FILTER (WHERE indicator_code = 'cereal_yield_t_ha'), 0)
    AS implied_area_ha
FROM kenya.observation
WHERE country_code = 'KE'
  AND year BETWEEN 2018 AND 2024
GROUP BY year
ORDER BY year;