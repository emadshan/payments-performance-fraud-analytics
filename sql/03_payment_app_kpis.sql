-- Project: Razorpay Payments Intelligence & Business Optimization
-- Purpose: Compare payment success and failure by payment app.
-- Data: Synthetic dataset; not actual Razorpay internal data.

CREATE OR REPLACE VIEW analytics.v_payment_app_kpis AS
SELECT
    payment_app,
    COUNT(*) AS total_attempts,
    COUNT(*) FILTER (WHERE status = 'Success') AS successful_attempts,
    COUNT(*) FILTER (WHERE status = 'Failed') AS failed_attempts,
    COUNT(*) FILTER (WHERE status = 'Pending') AS pending_attempts,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'Success')
        / NULLIF(COUNT(*), 0), 2
    ) AS success_rate_pct,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'Failed')
        / NULLIF(COUNT(*), 0), 2
    ) AS failure_rate_pct,
    ROUND(
        SUM(amount) FILTER (WHERE status = 'Success'), 2
    ) AS successful_payment_value
FROM analytics.transactions
GROUP BY payment_app;
