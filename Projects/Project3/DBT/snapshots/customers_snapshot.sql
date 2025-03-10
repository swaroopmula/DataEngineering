{% snapshot customers_snapshot %}

{{ config(
    target_schema='customers_country_history',
    unique_key='customer_id',
    strategy='check',
    check_cols=['country'],
    invalidate_hard_deletes=True
) }}

SELECT
    customer_id,
    country,
    created_at
FROM {{ ref('stg_customers') }}

{% endsnapshot %}