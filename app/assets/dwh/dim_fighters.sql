/* @bruin

name: dwh.dim_fighters
type: duckdb.sql
tags:
  - dim
  - fighters

materialization:
  type: table
  strategy: scd2_by_column

depends:
  - staging.fighters

columns:
  - name: id
    type: VARCHAR
    primary_key: true
  - name: first_name
    type: VARCHAR
  - name: last_name
    type: VARCHAR
  - name: nick_name
    type: VARCHAR
  - name: height
    type: VARCHAR
  - name: weight
    type: VARCHAR
  - name: wins
    type: BIGINT

@bruin */

SELECT * FROM staging.fighters
