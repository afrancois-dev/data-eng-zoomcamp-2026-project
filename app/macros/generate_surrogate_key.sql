-- based on bruin doc
-- compatible for both duckdb and bigquery 
-- not hashed in md5 at this moment -> TODO
-- nb for bruin developer -> environment should be in built-in method
{% macro generate_surrogate_key(columns) -%}
CONCAT(
    {%- for col in columns %}
        CAST({{ col }} AS STRING)
        {%- if not loop.last %}, '||', {% endif %}
    {%- endfor %}
)
{%- endmacro %}