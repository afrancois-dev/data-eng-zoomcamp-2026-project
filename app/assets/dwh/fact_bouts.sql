/* @bruin

name: dwh.fact_bouts
tags:
  - fact
  - bouts

materialization:
  type: table
  strategy: time_interval
  partition_by: date
  cluster_by:
    - event_id
    - fighter_1_id
    - fighter_2_id
  incremental_key: date
  time_granularity: date

depends:
  - staging.bouts
  - dwh.dim_fighters
  - dwh.dim_events

columns:
  - name: bout_id
    type: STRING
    primary_key: true
  - name: event_id
    type: STRING
  - name: date
    type: DATE
  - name: fighter_1_id
    type: STRING
  - name: fighter_2_id
    type: STRING
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
    bout_id,
    event_id,
    fighter_1_id,
    fighter_2_id,
    winner_id,
    weight_class,
    method,
    round,
    time,
    date
FROM staging.bouts
