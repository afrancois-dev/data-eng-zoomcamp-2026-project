/* @bruin

name: dwh.dim_fighters
type: duckdb.sql

materialization:
  type: table

depends:
  - staging.fighters

@bruin */

SELECT * FROM staging.fighters
-- UNION ALL default fighter
