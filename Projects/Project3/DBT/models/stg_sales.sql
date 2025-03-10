WITH sales AS (
    SELECT
        sale_id,
        CAST(customer_id AS INT64) AS customer_id,
        CAST(REGEXP_REPLACE(CAST(amount AS STRING), r'[^0-9.-]', '') AS FLOAT64) AS amount,
        sale_date
    FROM {{ source('dbt_demo_sample', 'raw_sales') }}
    WHERE
        sale_id IS NOT NULL
        AND customer_id IS NOT NULL
        AND CAST(REGEXP_REPLACE(CAST(amount AS STRING), r'[^0-9.-]', '') AS FLOAT64) > 0 
),

cleaned_sales AS (
    SELECT
        sale_id,
        customer_id,
        ROUND(amount, 2) AS amount,
        CAST(sale_date AS DATE) AS sale_date
    FROM sales
),

deduplicated_sales AS {{ deduplicate('cleaned_sales','sale_id','sale_date')}}

SELECT
    sale_id,
    customer_id,
    amount,
    sale_date
FROM deduplicated_sales
ORDER BY sale_date DESC