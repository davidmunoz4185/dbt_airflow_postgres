with 

source as (

    select * from {{ ref('stripe_payments') }}

),

transformed as (

  select

    id as payment_id,
    order_id,
    created as payment_created_at,
    status as payment_status,
    payment_method,
    round(amount / 100.0, 2) as payment_amount

  from source

)

select * from transformed