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
  - name: nick_name
    type: VARCHAR
  - name: height
    type: VARCHAR
  - name: weight
    type: VARCHAR
  - name: wins
    type: BIGINT
    checks:
      - name: min
        value: 0

@bruin */

WITH source AS (
    SELECT
        *,
        CONCAT(first_name, '_', last_name, '_', nick_name) AS id
    FROM raw.fighters
)

SELECT * FROM source
