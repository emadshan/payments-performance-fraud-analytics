-- Project: Razorpay Payments Intelligence & Business Optimization
-- Purpose: Compare payment outcomes on weekdays and weekends.
-- Data: Synthetic dataset; not actual Razorpay internal data.

CREATE OR REPLACE VIEW analytics.v_weekend_payment_kpis AS
SELECT
    CASE
        WHEN is_weekend IS TRUE THEN 'Weekend'
        WHEN is_weekend IS FALSE THEN 'Weekday'
        ELSE 'Unknown'
    END AS day_category,
    COUNT(*) AS total_attempts,
    COUNT(*) FILTER (WHERE status = 'Success') AS successful_attempts,
    COUNT(*) FILTER (WHERE status = 'Failed') AS failed_attempts,
    COUNT(*) FILTER (WHERE status = 'Pending') AS pending_attempts,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'Failed')
        / NULLIF(COUNT(*), 0), 2
    ) AS failure_rate_pct,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'Success')
        / NULLIF(COUNT(*), 0), 2
    ) AS success_rate_pct
FROM analytics.transactions
GROUP BY 1;
