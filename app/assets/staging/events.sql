/* @bruin

name: staging.events
tags:
  - events

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.events

columns:
  - name: id
    type: STRING
    checks:
      - name: not_null
      - name: unique
  - name: name
    type: STRING
    checks:
      - name: not_null
      - name: unique
  - name: date
    type: DATE
    checks:
      - name: not_null
  - name: location
    type: STRING
    checks:
      - name: not_null

@bruin */

SELECT
    {{ generate_surrogate_key(['url']) }} as id,
    name,
    date,
    location
FROM raw.events
