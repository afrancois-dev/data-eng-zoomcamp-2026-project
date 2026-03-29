/* @bruin

name: staging.events
type: duckdb.sql

materialization:
  type: table
  strategy: create+replace

depends:
  - raw.events

columns:
  - name: name
    type: VARCHAR
    checks:
      - name: not_null
      - name: unique
  - name: url
    type: VARCHAR
    checks:
      - name: not_null
      - name: unique
  - name: date
    type: DATE
    checks:
      - name: not_null
  - name: location
    type: VARCHAR
    checks:
      - name: not_null

@bruin */

SELECT * FROM raw.events
