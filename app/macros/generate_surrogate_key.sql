-- based on bruin docs
{% macro generate_surrogate_key(columns) -%}
MD5(CONCAT_WS('||',
    {%- for col in columns %}
        CAST({{ col }} AS VARCHAR)
        {%- if not loop.last %}, {% endif %}
    {%- endfor %}
))
{%- endmacro %}