with raw as (
    select * from {{ ref('RAW_ORDERS') }}
)

select
    order_id,
    customer,
    amount,
    event_time
from raw
