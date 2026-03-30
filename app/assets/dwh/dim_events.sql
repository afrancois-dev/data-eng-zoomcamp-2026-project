/* @bruin

name: dwh.dim_events
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
    type: STRING
    primary_key: true
  - name: name
    type: STRING
  - name: date
    type: DATE
  - name: location
    type: STRING

@bruin */

SELECT
    id,
    name,
    date,
    location
FROM staging.events
