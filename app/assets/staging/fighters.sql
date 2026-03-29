/* @bruin

name: staging.fighters
type: duckdb.sql

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.fighters

columns:
  - name: id
    type: VARCHAR
    primary_key: true
    checks:
      - name: not_null
  - name: first_name
    type: VARCHAR
    checks:
      - name: not_null
  - name: last_name
    type: VARCHAR
    checks:
      - name: not_null
  - name: wins
    type: BIGINT
    checks:
      - name: min
        value: 0

@bruin */

WITH source AS (
    SELECT
        first_name,
        last_name,
        wins,
        COALESCE(first_name, last_name) AS id
    FROM raw.fighters
)

SELECT * FROM source
