/* @bruin

name: staging.bouts
type: duckdb.sql

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.bouts

columns:
  - name: bout_url
    type: VARCHAR
    checks:
      - name: not_null
  - name: event_url
    type: VARCHAR
    checks:
      - name: not_null
  - name: fighter_1
    type: VARCHAR
    checks:
      - name: not_null
  - name: fighter_2
    type: VARCHAR
    checks:
      - name: not_null
  - name: winner
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
    {{ generate_surrogate_key(['bout_url']) }} as id,
    {{ generate_surrogate_key(['event_url']) }} as event_id,
    fighter_1,
    fighter_2,
    winner,
    weight_class,
    method,
    time,
    CAST(round AS INTEGER) AS round
FROM raw.bouts
