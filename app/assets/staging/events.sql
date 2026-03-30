/* @bruin

name: staging.events
type: duckdb.sql
tags:
  - events

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.events

columns:
  - name: id
    type: VARCHAR
    checks:
      - name: not_null
      - name: unique
  - name: name
    type: VARCHAR
    checks:
      - name: not_null
      - name: unique
  - name: date
    type: DATE
    checks:
      - name: not_null
  - name: location
    type: VARCHAR
    checks:
      - name: not_null

@bruin */

SELECT
    {{ generate_surrogate_key(['url']) }} as id,
    name,
    date,
    location
FROM raw.events
