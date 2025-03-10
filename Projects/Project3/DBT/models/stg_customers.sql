WITH customers AS (
    SELECT
        customer_id,
        name,
        NULLIF(LOWER(email), '') AS email, 
        CASE 
            WHEN LOWER(country) = 'unknown' THEN NULL 
            ELSE country 
        END AS country, 
        created_at
    FROM {{ source('dbt_demo_sample', 'raw_customers') }}
),

cleaned_customers AS (
    SELECT
        customer_id, 
        name,
        CASE 
            WHEN LOWER(email) = 'nan' THEN NULL
            ELSE email
        END AS email, 
        country, 
        created_at
    FROM customers
),

deduplicated_customers AS {{ deduplicate('cleaned_customers', 'customer_id', 'created_at') }}

SELECT 
    customer_id, 
    name, 
    email, 
    country, 
    created_at
FROM deduplicated_customers
WHERE row_num = 1 
AND customer_id IS NOT NULL