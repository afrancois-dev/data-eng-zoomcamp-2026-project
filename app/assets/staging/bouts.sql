/* @bruin

name: staging.bouts
type: duckdb.sql
tags:
  - bouts

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.bouts

columns:
  - name: bout_id
    type: VARCHAR
    primary_key: true
    checks:
      - name: not_null
  - name: event_id
    type: VARCHAR
    checks:
      - name: not_null
  - name: fighter_1_id
    type: VARCHAR
    checks:
      - name: not_null
  - name: fighter_2_id
    type: VARCHAR
    checks:
      - name: not_null
  - name: winner_id
    type: VARCHAR
  - name: weight_class
    type: VARCHAR
  - name: method
    type: VARCHAR
  - name: round
    type: INTEGER
  - name: time
    type: VARCHAR

@bruin */

SELECT
    {{ generate_surrogate_key(['bout_url']) }} as bout_id,
    {{ generate_surrogate_key(['event_url']) }} as event_id,
    {{ generate_surrogate_key(['fighter_1']) }} as fighter_1_id,
    {{ generate_surrogate_key(['fighter_2']) }} as fighter_2_id,
    {{ generate_surrogate_key(['winner']) }} as winner_id,
    weight_class,
    method,
    time,
    CAST(round AS INTEGER) AS round
FROM raw.bouts
