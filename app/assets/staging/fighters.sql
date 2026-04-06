/* @bruin

name: staging.fighters
tags:
  - fighters

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.fighters

columns:
  - name: fighter_sk
    type: STRING
    primary_key: true
    checks:
      - name: not_null
  - name: first_name
    type: STRING
    checks:
      - name: not_null
  - name: last_name
    type: STRING
    checks:
      - name: not_null
  - name: nick_name
    type: STRING
  - name: height
    type: STRING
  - name: weight
    type: STRING
  - name: wins
    type: INT64
    checks:
      - name: min
        value: 0

@bruin */

SELECT
  {{ generate_surrogate_key(['url']) }} AS fighter_sk,
  first_name,
  last_name,
  nick_name,
  height,
  weight,
  wins
FROM raw.fighters
