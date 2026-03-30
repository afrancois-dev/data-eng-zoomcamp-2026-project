/* @bruin

name: dwh.dim_fighters
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
    type: STRING
    primary_key: true
  - name: first_name
    type: STRING
  - name: last_name
    type: STRING
  - name: nick_name
    type: STRING
  - name: height
    type: STRING
  - name: weight
    type: STRING
  - name: wins
    type: INT64

@bruin */

SELECT * FROM staging.fighters
