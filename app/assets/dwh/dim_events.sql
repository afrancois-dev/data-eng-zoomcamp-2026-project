/* @bruin

name: dwh.dim_events
type: duckdb.sql
tags:
  - dim
  - events

materialization:
  type: table
  strategy: scd2_by_column

depends:
  - staging.events

columns:
  - name: id
    type: VARCHAR
    primary_key: true
  - name: name
    type: VARCHAR
  - name: date
    type: DATE
  - name: location
    type: VARCHAR

@bruin */

SELECT
    id,
    name,
    date,
    location
FROM staging.events
