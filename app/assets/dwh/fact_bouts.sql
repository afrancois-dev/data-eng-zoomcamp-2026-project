/* @bruin

name: dwh.fact_bouts
type: duckdb.sql
tags:
  - fact
  - bouts

materialization:
  type: table
  strategy: create+replace

depends:
  - staging.bouts
  - dwh.dim_fighters
  - dwh.dim_events

columns:
  - name: bout_id
    type: VARCHAR
    primary_key: true
  - name: event_id
    type: VARCHAR
  - name: fighter_1_id
    type: VARCHAR
  - name: fighter_2_id
    type: VARCHAR
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
    bout_id,
    event_id,
    fighter_1_id,
    fighter_2_id,
    winner_id,
    weight_class,
    method,
    round,
    time
FROM staging.bouts
