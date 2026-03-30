/* @bruin

name: staging.bouts
tags:
  - bouts

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.bouts

columns:
  - name: bout_id
    type: STRING
    primary_key: true
    checks:
      - name: not_null
  - name: event_id
    type: STRING
    checks:
      - name: not_null
  - name: date
    type: DATE
    checks:
      - name: not_null
  - name: fighter_1_id
    type: STRING
    checks:
      - name: not_null
  - name: fighter_2_id
    type: STRING
    checks:
      - name: not_null
  - name: winner_id
    type: STRING
  - name: weight_class
    type: STRING
  - name: method
    type: STRING
  - name: round
    type: INT64
  - name: time
    type: STRING

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
    date,
    CAST(round AS INT64) AS round
FROM raw.bouts
