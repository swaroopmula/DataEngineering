{{ config(materialized='table') }}


WITH raw_customers AS (
    SELECT
        customer_id,
        name,
        NULLIF(email, '') AS email, 
        CASE 
            WHEN country = 'Unknown' THEN NULL 
            ELSE country 
        END AS country, 
        created_at
    FROM {{ source('dbt_demo_sample', 'customers') }}
),

deduplicated_customers AS (
    SELECT 
        customer_id, 
        name, 
        email, 
        country, 
        created_at,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) AS row_num
    FROM raw_customers
)

SELECT 
    customer_id, 
    name, 
    email, 
    country, 
    created_at
FROM deduplicated_customers
WHERE row_num = 1 
AND customer_id IS NOT NULL


