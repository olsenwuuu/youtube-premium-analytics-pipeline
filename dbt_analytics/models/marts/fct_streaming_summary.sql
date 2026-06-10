{{ config(materialized='table') }}

with base_data as (
    -- Direct query to your clean database table
    select * from stg_streaming_activity
),

aggregated_metrics as (
    select
        -- Dimensions (How you will group your data in Notebook 3)
        user_id,
        activity_date,
        device_type,
        plan_type,
        status as account_status,
        signup_date,
        cancellation_date,
        
        -- Fact Metrics (The pre-calculated answers for your business questions)
        count(log_id) as total_streaming_sessions,
        sum(cast(minutes_streamed as real)) as total_minutes_streamed,
        sum(cast(ad_clicks_avoided as integer)) as total_ads_avoided
    from base_data
    group by 1, 2, 3, 4, 5, 6, 7
)

select * from aggregated_metrics