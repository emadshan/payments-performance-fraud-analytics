-- Project: Razorpay Payments Intelligence & Business Optimization
-- Purpose: Analyze payment outcomes by hour of day.
-- Data: Synthetic dataset; not actual Razorpay internal data.

CREATE OR REPLACE VIEW analytics.v_hourly_payment_kpis AS
SELECT
    hour_of_day,
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
WHERE hour_of_day BETWEEN 0 AND 23
GROUP BY hour_of_day;
