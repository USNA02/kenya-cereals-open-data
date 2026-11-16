INSERT INTO kenya.indicator (code, name, unit, source_url, license) VALUES
  ('cereal_yield_t_ha', 'Cereal yield', 'tonnes per hectare', 'https://ourworldindata.org/grapher/cereal-yield', 'CC BY 4.0'),
  ('cereal_production_t', 'Cereal production', 'tonnes', 'https://ourworldindata.org/grapher/cereal-production', 'CC BY 4.0'),
  ('ag_employment_pct', 'Employment in agriculture', 'percent of employment', 'https://ourworldindata.org/grapher/share-of-the-labor-force-employed-in-agriculture', 'CC BY 4.0'),
  ('ag_land_ha', 'Agricultural land', 'hectares', 'https://ourworldindata.org/grapher/agricultural-land', 'CC BY 4.0'),
  ('cereal_area_ha', 'Land under cereal production', 'hectares', 'https://data.worldbank.org/indicator/AG.LND.CREL.HA', 'CC BY 4.0'),
  ('ag_gdp_pct', 'Agriculture, forestry, and fishing', 'percent of GDP', 'https://data.worldbank.org/indicator/NV.AGR.TOTL.ZS', 'CC BY 4.0'),
  ('fertilizer_kg_ha', 'Fertilizer consumption', 'kg per hectare of arable land', 'https://data.worldbank.org/indicator/AG.CON.FERT.ZS', 'CC BY 4.0'),
  ('rural_pop_pct', 'Rural population', 'percent of population', 'https://data.worldbank.org/indicator/SP.RUR.TOTL.ZS', 'CC BY 4.0'),
  ('ag_land_pct', 'Agricultural land', 'percent of land area', 'https://data.worldbank.org/indicator/AG.LND.AGRI.ZS', 'CC BY 4.0')
ON CONFLICT (code) DO NOTHING;