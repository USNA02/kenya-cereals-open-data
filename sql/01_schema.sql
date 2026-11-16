CREATE SCHEMA IF NOT EXISTS kenya;

CREATE TABLE IF NOT EXISTS kenya.indicator (
  code text PRIMARY KEY,
  name text NOT NULL,
  unit text NOT NULL,
  source_url text NOT NULL,
  license text NOT NULL
);

CREATE TABLE IF NOT EXISTS kenya.observation (
  country_code char(2) NOT NULL,
  indicator_code text NOT NULL REFERENCES kenya.indicator (code),
  year integer NOT NULL CHECK (year BETWEEN 1960 AND 2100),
  value numeric,
  PRIMARY KEY (country_code, indicator_code, year)
);

COMMENT ON TABLE kenya.observation IS
  'National cereal and agriculture series. Not county-level. Retrieved 2026-11-16.';