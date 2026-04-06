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
  - name: bout_sk
    type: STRING
    primary_key: true
    checks:
      - name: not_null
  - name: event_sk
    type: STRING
    checks:
      - name: not_null
  - name: date
    type: DATE
    checks:
      - name: not_null
  - name: fighter_1_sk
    type: STRING
    checks:
      - name: not_null
  - name: fighter_2_sk
    type: STRING
    checks:
      - name: not_null
  - name: fighter_1_full_name
    type: STRING
  - name: fighter_2_full_name
    type: STRING
  - name: winner_sk
    type: STRING
  - name: winner_full_name
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
    {{ generate_surrogate_key(['bout_url']) }} as bout_sk,
    {{ generate_surrogate_key(['event_url']) }} as event_sk,
    {{ generate_surrogate_key(['fighter_1_url']) }} as fighter_1_sk,
    {{ generate_surrogate_key(['fighter_2_url']) }} as fighter_2_sk,
    {{ generate_surrogate_key(['winner_url']) }} as winner_sk,
    weight_class,
    method,
    time,
    date,
    CAST(round AS INT64) AS round
FROM raw.bouts
