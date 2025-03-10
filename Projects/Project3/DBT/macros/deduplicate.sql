{% macro deduplicate(source_table, unique_key, timestamp_column) %}
(
    SELECT * FROM (
        SELECT 
            *, 
            ROW_NUMBER() OVER (PARTITION BY {{ unique_key }} ORDER BY {{ timestamp_column }} DESC) AS row_num
        FROM {{ source_table }}
    ) 
    WHERE row_num = 1
)
{% endmacro %}